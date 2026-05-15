#!/usr/bin/env python3
"""Emit a runtime-smoke JSON artifact for the current Agent Brain checkout."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator

SANDBOX_WRITE_MODES = {"read_only", "workspace_write", "approval_gated", "unrestricted", "unknown"}
BRAIN_COMMAND_MODES = {"native_commands", "markdown_specs", "mixed", "unknown"}
RUN_SCOPES = {"read_only_smoke", "full_validation"}
SMOKE_RESULTS = {"pass", "blocked", "fail"}
FULL_VALIDATION_GATE_COMMANDS = [
    "rm -rf scripts/__pycache__ tests/__pycache__",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
]


def _run_git(root: Path, *args: str) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception as exc:  # pragma: no cover - defensive around host git setup
        return False, str(exc)

    output = (completed.stdout or completed.stderr).strip()
    if completed.returncode != 0:
        return False, output or f"git {' '.join(args)} exited {completed.returncode}"
    return True, output


def git_freshness_result(root: Path) -> str:
    head_ok, head = _run_git(root, "rev-parse", "HEAD")
    origin_ok, origin = _run_git(root, "rev-parse", "origin/main")
    if not head_ok or not origin_ok:
        reason = head if not head_ok else origin
        return f"unavailable: {reason}"
    if head == origin:
        return f"fresh: HEAD equals origin/main at {head}"
    return f"stale: HEAD {head} differs from origin/main {origin}"


def writable_temp_dir_status(root: Path) -> str:
    try:
        with tempfile.NamedTemporaryFile(prefix="agentbrain-smoke-", dir=root, delete=True) as handle:
            handle.write(b"ok")
            handle.flush()
        return "writable"
    except OSError:
        return "blocked"


def section_body(text: str, section: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line != section:
            continue
        body_lines: list[str] = []
        for following_line in lines[index + 1 :]:
            if following_line.startswith("## "):
                break
            body_lines.append(following_line)
        return "\n".join(body_lines)
    return ""


def command_declared_skills(command_path: Path) -> set[str]:
    body = section_body(command_path.read_text(encoding="utf-8"), "## Skills to load")
    return set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", body))


def build_report(
    *,
    root: Path,
    runtime: str,
    version: str,
    sandbox_write_mode: str,
    brain_command_mode: str,
    run_scope: str,
    blocked_commands: list[str],
    exact_command: str,
    command_exit_status: int = 0,
    smoke_result: str = "pass",
    transcript_path: str = "not_captured_stdout_only",
    selected_command: str = "unknown",
    loaded_skills: list[str] | None = None,
    adapter_path: str = "unknown",
    validation_commands: list[str] | None = None,
) -> dict[str, object]:
    root = Path(root)
    if sandbox_write_mode not in SANDBOX_WRITE_MODES:
        raise ValueError(f"unsupported sandbox_write_mode: {sandbox_write_mode}")
    if brain_command_mode not in BRAIN_COMMAND_MODES:
        raise ValueError(f"unsupported brain_command_mode: {brain_command_mode}")
    if run_scope not in RUN_SCOPES:
        raise ValueError(f"unsupported run_scope: {run_scope}")
    if smoke_result not in SMOKE_RESULTS:
        raise ValueError(f"unsupported smoke_result: {smoke_result}")

    scope_label = run_scope.replace("read_only", "read-only").replace("_", " ")
    command_label = brain_command_mode.replace("_", " ")
    loaded_skills = loaded_skills or []
    validation_commands = validation_commands or []
    freshness = git_freshness_result(root)
    evidence = [
        f"Runtime smoke captured for {runtime} {version} as {scope_label}.",
        f"Python executable: {sys.executable}",
        f"/brain-* command mode: {command_label}.",
        f"Selected command: {selected_command}",
        f"Loaded skills: {', '.join(loaded_skills) if loaded_skills else 'none'}",
        f"Adapter path: {adapter_path}",
        f"Git freshness result: {freshness}",
        f"Command exit status: {command_exit_status}",
        f"Smoke result: {smoke_result}",
        f"Transcript path: {transcript_path}",
        f"Blocked commands recorded: {', '.join(blocked_commands) if blocked_commands else 'none'}.",
        f"Validation commands: {', '.join(validation_commands) if validation_commands else 'none'}.",
    ]

    return {
        "runtime": runtime,
        "version": version,
        "python_executable": sys.executable,
        "writable_temp_dir_status": writable_temp_dir_status(root),
        "git_freshness_result": freshness,
        "exact_command": exact_command,
        "command_exit_status": command_exit_status,
        "smoke_result": smoke_result,
        "transcript_path": transcript_path,
        "sandbox_write_mode": sandbox_write_mode,
        "brain_command_mode": brain_command_mode,
        "selected_command": selected_command,
        "loaded_skills": loaded_skills,
        "adapter_path": adapter_path,
        "blocked_commands": blocked_commands,
        "run_scope": run_scope,
        "validation_commands": validation_commands,
        "evidence": evidence,
    }


def exact_command_has_flag_value(exact_command: object, flag: str, value: str) -> bool:
    if not isinstance(exact_command, str):
        return False
    return f"{flag} {value}" in exact_command or f"{flag}={value}" in exact_command


def validate_report_against_schema(
    report: dict[str, object], schema_path: Path, *, root: Path | None = None
) -> list[str]:
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = [error.message for error in sorted(validator.iter_errors(report), key=lambda error: list(error.path))]

    blocked_commands = report.get("blocked_commands")
    blocked_count = len(blocked_commands) if isinstance(blocked_commands, list) else 0
    if report.get("run_scope") == "full_validation" and blocked_count:
        errors.append("full_validation cannot list blocked_commands; use read_only_smoke or remove blockers")
    if report.get("smoke_result") == "blocked" and blocked_count == 0:
        errors.append("blocked smoke_result must list at least one blocked command")
    if report.get("smoke_result") == "pass" and report.get("command_exit_status") != 0:
        errors.append("pass smoke_result requires command_exit_status 0")
    if report.get("smoke_result") == "pass":
        selected_command = report.get("selected_command")
        if not (isinstance(selected_command, str) and selected_command.startswith("/brain-")):
            errors.append("pass smoke_result requires a selected /brain-* command")
        elif not exact_command_has_flag_value(report.get("exact_command"), "--selected-command", selected_command):
            errors.append(f"exact_command must record selected command flag: --selected-command {selected_command}")
        loaded_skills = report.get("loaded_skills")
        if not (isinstance(loaded_skills, list) and any(isinstance(skill, str) and skill for skill in loaded_skills)):
            errors.append("pass smoke_result requires at least one loaded skill")
        elif isinstance(loaded_skills, list):
            for skill in loaded_skills:
                if isinstance(skill, str) and skill and not exact_command_has_flag_value(
                    report.get("exact_command"), "--loaded-skill", skill
                ):
                    errors.append(f"exact_command must record loaded skill flag: --loaded-skill {skill}")
        if report.get("adapter_path") == "unknown":
            errors.append("pass smoke_result requires an adapter_path")
    if report.get("run_scope") == "full_validation" and report.get("smoke_result") != "pass":
        errors.append("full_validation requires smoke_result pass")
    if report.get("run_scope") == "full_validation" and report.get("sandbox_write_mode") == "read_only":
        errors.append("full_validation requires a write-capable sandbox; use read_only_smoke for read_only runs")
    if report.get("run_scope") == "full_validation" and report.get("transcript_path") == "not_captured_stdout_only":
        errors.append("full_validation requires a durable transcript_path instead of not_captured_stdout_only")
    if report.get("run_scope") == "full_validation" and report.get("brain_command_mode") == "unknown":
        errors.append("full_validation requires brain_command_mode to be proven as native_commands, markdown_specs, or mixed")
    if report.get("run_scope") == "full_validation" and report.get("selected_command") == "unknown":
        errors.append("full_validation requires a selected /brain-* command")
    loaded_skills = report.get("loaded_skills")
    if report.get("run_scope") == "full_validation" and not (
        isinstance(loaded_skills, list) and any(isinstance(skill, str) and skill for skill in loaded_skills)
    ):
        errors.append("full_validation requires at least one loaded skill")
    if report.get("run_scope") == "full_validation" and report.get("adapter_path") == "unknown":
        errors.append("full_validation requires an adapter_path for the runtime boundary")
    git_freshness = report.get("git_freshness_result")
    if report.get("run_scope") == "full_validation" and not (
        isinstance(git_freshness, str) and git_freshness.startswith("fresh: HEAD equals origin/main")
    ):
        errors.append("full_validation requires fresh git checkout with HEAD equal to origin/main")
    if report.get("run_scope") == "full_validation" and report.get("writable_temp_dir_status") != "writable":
        errors.append("full_validation requires writable temporary directory evidence")
    validation_commands = report.get("validation_commands")
    recorded_validation_commands = validation_commands if isinstance(validation_commands, list) else []
    if report.get("run_scope") == "full_validation":
        for required_command in FULL_VALIDATION_GATE_COMMANDS:
            if required_command not in recorded_validation_commands:
                errors.append(f"full_validation must record successful local gate command: {required_command}")
    if root is not None and report.get("smoke_result") == "pass":
        adapter_path = report.get("adapter_path")
        if isinstance(adapter_path, str) and adapter_path != "unknown" and not (Path(root) / adapter_path).is_file():
            errors.append(f"adapter file is missing: {adapter_path}")
        selected_command = report.get("selected_command")
        if isinstance(selected_command, str) and selected_command.startswith("/brain-"):
            command_rel = f"commands/{selected_command.removeprefix('/')}.md"
            command_path = Path(root) / command_rel
            if not command_path.is_file():
                errors.append(f"selected command file is missing: {command_rel}")
            elif isinstance(loaded_skills, list):
                declared_skills = command_declared_skills(command_path)
                loaded_skill_names = {skill for skill in loaded_skills if isinstance(skill, str) and skill}
                for skill in loaded_skills:
                    if not (isinstance(skill, str) and skill):
                        continue
                    skill_rel = f"skills/{skill}/SKILL.md"
                    if not (Path(root) / skill_rel).is_file():
                        errors.append(f"loaded skill file is missing: {skill_rel}")
                    if skill not in declared_skills:
                        errors.append(f"loaded skill is not named by selected command {selected_command}: {skill}")
                if report.get("run_scope") == "full_validation":
                    for missing_skill in sorted(declared_skills - loaded_skill_names):
                        errors.append(
                            f"selected command {selected_command} declared skill was not loaded: {missing_skill}"
                        )

    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", required=True, help="Neutral runtime name, for example generic-cli-runtime")
    parser.add_argument("--version", required=True, help="Runtime version string reported by the runtime")
    parser.add_argument("--sandbox-write-mode", choices=sorted(SANDBOX_WRITE_MODES), default="unknown")
    parser.add_argument("--brain-command-mode", choices=sorted(BRAIN_COMMAND_MODES), default="markdown_specs")
    parser.add_argument("--selected-command", default="unknown", help="Agent Brain command route selected by the runtime, for example /brain-start")
    parser.add_argument("--loaded-skill", action="append", default=[], help="Skill loaded during the smoke run; repeat for multiple skills")
    parser.add_argument("--adapter-path", default="unknown", help="Adapter README or integration note used for this smoke run, for example adapters/read-only-cli/README.md")
    parser.add_argument("--run-scope", choices=sorted(RUN_SCOPES), default="read_only_smoke")
    parser.add_argument("--command-exit-status", type=int, default=0, help="Exit status of the smoke command or validation command")
    parser.add_argument("--smoke-result", choices=sorted(SMOKE_RESULTS), default="pass")
    parser.add_argument("--transcript-path", default="not_captured_stdout_only", help="Path or durable location for the runtime transcript/log captured during smoke")
    parser.add_argument("--blocked-command", action="append", default=[], help="Command that was blocked or intentionally skipped")
    parser.add_argument(
        "--validation-command",
        action="append",
        default=[],
        help="Successful local gate command completed during full validation; repeat for each gate command",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root to inspect")
    parser.add_argument("--schema", type=Path, help="Runtime-smoke schema path; defaults to <root>/schemas/runtime-smoke.schema.json")
    parser.add_argument("--output", type=Path, help="Optional JSON output path; stdout is used when omitted")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    exact_command = "python scripts/runtime_smoke.py " + " ".join(sys.argv[1:] if argv is None else argv)
    report = build_report(
        root=args.root,
        runtime=args.runtime,
        version=args.version,
        sandbox_write_mode=args.sandbox_write_mode,
        brain_command_mode=args.brain_command_mode,
        run_scope=args.run_scope,
        blocked_commands=args.blocked_command,
        exact_command=exact_command,
        command_exit_status=args.command_exit_status,
        smoke_result=args.smoke_result,
        transcript_path=args.transcript_path,
        selected_command=args.selected_command,
        loaded_skills=args.loaded_skill,
        adapter_path=args.adapter_path,
        validation_commands=args.validation_command,
    )
    schema_path = args.schema or (args.root / "schemas" / "runtime-smoke.schema.json")
    errors = validate_report_against_schema(report, schema_path, root=args.root)
    if errors:
        sys.stderr.write("runtime smoke schema validation failed:\n")
        for error in errors:
            sys.stderr.write(f"- {error}\n")
        return 1

    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

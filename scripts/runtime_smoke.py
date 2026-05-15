#!/usr/bin/env python3
"""Emit a runtime-smoke JSON artifact for the current Agent Brain checkout."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator

SANDBOX_WRITE_MODES = {"read_only", "workspace_write", "approval_gated", "unrestricted", "unknown"}
BRAIN_COMMAND_MODES = {"native_commands", "markdown_specs", "mixed", "unknown"}
RUN_SCOPES = {"read_only_smoke", "full_validation"}
SMOKE_RESULTS = {"pass", "blocked", "fail"}


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
        "evidence": evidence,
    }


def validate_report_against_schema(report: dict[str, object], schema_path: Path) -> list[str]:
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = [error.message for error in sorted(validator.iter_errors(report), key=lambda error: list(error.path))]

    blocked_commands = report.get("blocked_commands")
    blocked_count = len(blocked_commands) if isinstance(blocked_commands, list) else 0
    if report.get("run_scope") == "full_validation" and blocked_count:
        errors.append("full_validation cannot list blocked_commands; use read_only_smoke or remove blockers")
    if report.get("smoke_result") == "blocked" and blocked_count == 0:
        errors.append("blocked smoke_result must list at least one blocked command")
    if report.get("run_scope") == "full_validation" and report.get("smoke_result") != "pass":
        errors.append("full_validation requires smoke_result pass")
    if report.get("run_scope") == "full_validation" and report.get("transcript_path") == "not_captured_stdout_only":
        errors.append("full_validation requires a durable transcript_path instead of not_captured_stdout_only")

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
    )
    schema_path = args.schema or (args.root / "schemas" / "runtime-smoke.schema.json")
    errors = validate_report_against_schema(report, schema_path)
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

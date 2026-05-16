#!/usr/bin/env python3
"""Emit a runtime-smoke JSON artifact for the current Agent Brain checkout."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator

SANDBOX_WRITE_MODES = {"read_only", "workspace_write", "approval_gated", "unrestricted", "unknown"}
BRAIN_COMMAND_MODES = {"native_commands", "markdown_specs", "mixed", "unknown"}
RUN_SCOPES = {"read_only_smoke", "full_validation"}
SMOKE_RESULTS = {"pass", "blocked", "fail"}
TRANSCRIPT_REDACTION_STATUSES = {"redacted", "no_sensitive_content", "not_captured", "blocked"}
WRITE_FENCE_APPROVAL_STATES = {"approved", "not_required", "blocked", "unknown"}
REQUIRED_EVIDENCE_PREFIXES = [
    "Python executable: ",
    "Writable temp-dir status: ",
    "/brain-* command mode: ",
    "Selected command: ",
    "Loaded skills: ",
    "Adapter path: ",
    "Git fetch result: ",
    "Git freshness result: ",
    "Git worktree status: ",
    "Command exit status: ",
    "Smoke result: ",
    "Transcript path: ",
    "Transcript redaction status: ",
    "Blocked commands recorded: ",
    "Validation commands: ",
    "Capability matrix: ",
    "Write fence: ",
    "Write fence approval state: ",
]
CAPABILITY_NAMES = [
    "read_files",
    "write_files",
    "run_shell",
    "request_approvals",
    "network_access",
    "native_brain_commands",
    "schema_artifacts",
    "blocked_command_reporting",
]
CAPABILITY_STATUSES = {"yes", "no", "unknown", "blocked"}
FULL_VALIDATION_REQUIRED_CAPABILITIES = ["read_files", "write_files", "run_shell", "schema_artifacts"]
SECRET_LIKE_PATTERNS = [
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(
        r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqps?)://"
        r"[^:\s/@]+:[^@\s/]+@",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:api[_-]?(?:key|token)|secret|token|password|passwd|pwd|client[_-]?secret)"
        r"\s*[:=]\s*['\"]?(?!<redacted>|\[redacted\]|redacted|placeholder|example)"
        r"[A-Za-z0-9_./+=:-]{16,}",
        re.IGNORECASE,
    ),
]
PRIVATE_ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9_.-])/(?:Users|home)/[^\s:'\"]+"),
    re.compile(r"\b[A-Za-z]:\\\\Users\\\\[^\s:'\"]+"),
]
FULL_VALIDATION_GATE_COMMANDS = [
    "rm -rf scripts/__pycache__ tests/__pycache__",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
]
SINGLETON_PROVENANCE_FLAGS = [
    "--runtime",
    "--version",
    "--sandbox-write-mode",
    "--brain-command-mode",
    "--selected-command",
    "--adapter-path",
    "--run-scope",
    "--command-exit-status",
    "--smoke-result",
    "--transcript-path",
    "--transcript-redaction-status",
    "--write-fence-rollback-command",
    "--write-fence-approval-state",
    "--root",
    "--schema",
    "--output",
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


def git_fetch_result(root: Path) -> str:
    fetch_ok, fetch_output = _run_git(root, "fetch", "origin", "main")
    if not fetch_ok:
        return f"unavailable: {fetch_output}"
    suffix = f" ({fetch_output})" if fetch_output else ""
    return f"fetched: git fetch origin main succeeded{suffix}"


def git_worktree_status(root: Path) -> str:
    status_ok, status_output = _run_git(root, "status", "--short")
    if not status_ok:
        return f"unavailable: {status_output}"
    if not status_output:
        return "clean"
    changed_paths = [line.strip() for line in status_output.splitlines() if line.strip()]
    return f"dirty: {len(changed_paths)} path(s) changed"


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
    transcript_redaction_status: str = "not_captured",
    selected_command: str = "unknown",
    loaded_skills: list[str] | None = None,
    adapter_path: str = "unknown",
    validation_commands: list[str] | None = None,
    write_fence_allowed_paths: list[str] | None = None,
    write_fence_disallowed_paths: list[str] | None = None,
    write_fence_user_owned_files: list[str] | None = None,
    write_fence_rollback_command: str = "not_applicable",
    write_fence_approval_state: str = "unknown",
    capability_matrix: dict[str, str] | None = None,
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
    if transcript_redaction_status not in TRANSCRIPT_REDACTION_STATUSES:
        raise ValueError(f"unsupported transcript_redaction_status: {transcript_redaction_status}")
    if write_fence_approval_state not in WRITE_FENCE_APPROVAL_STATES:
        raise ValueError(f"unsupported write_fence_approval_state: {write_fence_approval_state}")

    scope_label = run_scope.replace("read_only", "read-only").replace("_", " ")
    command_label = brain_command_mode.replace("_", " ")
    loaded_skills = ["runtime-smoke"] if loaded_skills is None else loaded_skills
    validation_commands = validation_commands if validation_commands is not None else (blocked_commands or ["not_checked"])
    write_fence = {
        "allowed_paths": write_fence_allowed_paths or [],
        "disallowed_paths": write_fence_disallowed_paths or [],
        "user_owned_files": write_fence_user_owned_files or [],
        "rollback_command": write_fence_rollback_command,
        "approval_state": write_fence_approval_state,
    }
    recorded_capability_matrix = {name: "unknown" for name in CAPABILITY_NAMES}
    if capability_matrix:
        for name, status in capability_matrix.items():
            if name not in recorded_capability_matrix:
                raise ValueError(f"unsupported capability name: {name}")
            if status not in CAPABILITY_STATUSES:
                raise ValueError(f"unsupported capability status for {name}: {status}")
            recorded_capability_matrix[name] = status
    fetch_result = git_fetch_result(root)
    freshness = git_freshness_result(root)
    worktree_status = git_worktree_status(root)
    temp_dir_status = writable_temp_dir_status(root)
    evidence = [
        f"Runtime smoke captured for {runtime} {version} as {scope_label}.",
        f"Python executable: {sys.executable}",
        f"Writable temp-dir status: {temp_dir_status}",
        f"/brain-* command mode: {command_label}.",
        f"Selected command: {selected_command}",
        f"Loaded skills: {', '.join(loaded_skills) if loaded_skills else 'none'}",
        f"Adapter path: {adapter_path}",
        f"Git fetch result: {fetch_result}",
        f"Git freshness result: {freshness}",
        f"Git worktree status: {worktree_status}",
        f"Command exit status: {command_exit_status}",
        f"Smoke result: {smoke_result}",
        f"Transcript path: {transcript_path}",
        f"Transcript redaction status: {transcript_redaction_status}",
        f"Blocked commands recorded: {', '.join(blocked_commands) if blocked_commands else 'none'}.",
        f"Validation commands: {', '.join(validation_commands) if validation_commands else 'none'}.",
        "Capability matrix: "
        + ", ".join(f"{name}={recorded_capability_matrix[name]}" for name in CAPABILITY_NAMES)
        + ".",
        "Write fence: "
        f"allowed={', '.join(write_fence['allowed_paths']) if write_fence['allowed_paths'] else 'none'}; "
        f"disallowed={', '.join(write_fence['disallowed_paths']) if write_fence['disallowed_paths'] else 'none'}; "
        f"user-owned={', '.join(write_fence['user_owned_files']) if write_fence['user_owned_files'] else 'none'}; "
        f"rollback={write_fence_rollback_command}.",
        f"Write fence approval state: {write_fence_approval_state}",
    ]

    return {
        "runtime": runtime,
        "version": version,
        "python_executable": sys.executable,
        "writable_temp_dir_status": temp_dir_status,
        "git_fetch_result": fetch_result,
        "git_freshness_result": freshness,
        "git_worktree_status": worktree_status,
        "exact_command": exact_command,
        "command_exit_status": command_exit_status,
        "smoke_result": smoke_result,
        "transcript_path": transcript_path,
        "transcript_redaction_status": transcript_redaction_status,
        "sandbox_write_mode": sandbox_write_mode,
        "brain_command_mode": brain_command_mode,
        "selected_command": selected_command,
        "loaded_skills": loaded_skills,
        "adapter_path": adapter_path,
        "blocked_commands": blocked_commands,
        "run_scope": run_scope,
        "validation_commands": validation_commands,
        "capability_matrix": recorded_capability_matrix,
        "write_fence": write_fence,
        "evidence": evidence,
    }


def adapter_path_is_adapter_readme(adapter_path: str) -> bool:
    return re.fullmatch(r"adapters/[a-z0-9-]+/README\.md", adapter_path) is not None


def transcript_path_is_external_reference(transcript_path: str) -> bool:
    return re.match(r"^[a-z][a-z0-9+.-]*://", transcript_path, flags=re.IGNORECASE) is not None


def exact_command_tokens(exact_command: object) -> list[str]:
    if not isinstance(exact_command, str):
        return []
    try:
        return shlex.split(exact_command)
    except ValueError:
        return exact_command.split()


def exact_command_invokes_runtime_smoke(exact_command: object) -> bool:
    tokens = exact_command_tokens(exact_command)
    return any(Path(token).as_posix().lstrip("./") == "scripts/runtime_smoke.py" for token in tokens)


def exact_command_has_flag_value(exact_command: object, flag: str, value: str) -> bool:
    tokens = exact_command_tokens(exact_command)

    for index, token in enumerate(tokens):
        if token == flag and index + 1 < len(tokens) and tokens[index + 1] == value:
            return True
        if token == f"{flag}={value}":
            return True
    return False


def exact_command_flag_values(exact_command: object, flag: str) -> list[str]:
    if not isinstance(exact_command, str):
        return []
    tokens = exact_command_tokens(exact_command)

    values: list[str] = []
    for index, token in enumerate(tokens):
        if token == flag and index + 1 < len(tokens):
            values.append(tokens[index + 1])
        elif token.startswith(f"{flag}="):
            values.append(token.split("=", 1)[1])
    return values


def capability_name_from_flag_value(flag_value: str) -> str:
    return flag_value.split("=", 1)[0] if "=" in flag_value else flag_value


def path_is_inside_declared_boundary(path_value: str, boundary_values: list[object]) -> bool:
    normalized_path = Path(path_value).as_posix().lstrip("./")
    for boundary_value in boundary_values:
        if not isinstance(boundary_value, str) or not boundary_value.strip():
            continue
        normalized_boundary = Path(boundary_value).as_posix().lstrip("./")
        if not normalized_boundary:
            continue
        if normalized_boundary.endswith("/"):
            if normalized_path.startswith(normalized_boundary):
                return True
        elif normalized_path == normalized_boundary or normalized_path.startswith(f"{normalized_boundary}/"):
            return True
    return False


def contains_secret_like_value(value: object) -> bool:
    if isinstance(value, str):
        return any(pattern.search(value) for pattern in SECRET_LIKE_PATTERNS)
    if isinstance(value, list):
        return any(contains_secret_like_value(item) for item in value)
    if isinstance(value, dict):
        return any(contains_secret_like_value(item) for item in value.values())
    return False


def contains_private_absolute_path(value: object) -> bool:
    if isinstance(value, str):
        return any(pattern.search(value) for pattern in PRIVATE_ABSOLUTE_PATH_PATTERNS)
    if isinstance(value, list):
        return any(contains_private_absolute_path(item) for item in value)
    if isinstance(value, dict):
        return any(contains_private_absolute_path(item) for item in value.values())
    return False


def version_is_concrete(value: object) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.strip().lower()
    return normalized not in {"", "unknown", "n/a", "na", "not_checked", "not checked", "unavailable"}


def parse_capability_flags(values: list[str]) -> dict[str, str]:
    capability_matrix: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"capability must use name=status format: {value}")
        name, status = value.split("=", 1)
        if name not in CAPABILITY_NAMES:
            raise ValueError(f"unsupported capability name: {name}")
        if status not in CAPABILITY_STATUSES:
            raise ValueError(f"unsupported capability status for {name}: {status}")
        capability_matrix[name] = status
    return capability_matrix


def validate_report_against_schema(
    report: dict[str, object], schema_path: Path, *, root: Path | None = None
) -> list[str]:
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = [error.message for error in sorted(validator.iter_errors(report), key=lambda error: list(error.path))]

    for field in ["exact_command", "transcript_path", "blocked_commands", "validation_commands", "write_fence", "evidence"]:
        if contains_secret_like_value(report.get(field)):
            errors.append(f"runtime smoke artifact contains secret-like value in {field}; redact before output")
    for field in ["exact_command", "transcript_path", "blocked_commands", "validation_commands", "write_fence"]:
        if contains_private_absolute_path(report.get(field)):
            errors.append(
                "runtime smoke artifact contains private absolute path in "
                f"{field}; use a repo-relative path or redact before output"
            )
    if not exact_command_invokes_runtime_smoke(report.get("exact_command")):
        errors.append("exact_command must invoke scripts/runtime_smoke.py")
    for flag in SINGLETON_PROVENANCE_FLAGS:
        if len(exact_command_flag_values(report.get("exact_command"), flag)) > 1:
            errors.append(f"exact_command must not contain duplicate singleton provenance flag: {flag}")
    loaded_skill_flag_values = exact_command_flag_values(report.get("exact_command"), "--loaded-skill")
    seen_loaded_skill_flags: set[str] = set()
    for loaded_skill_flag_value in loaded_skill_flag_values:
        if loaded_skill_flag_value in seen_loaded_skill_flags:
            errors.append(f"exact_command must not duplicate loaded skill flag: {loaded_skill_flag_value}")
        seen_loaded_skill_flags.add(loaded_skill_flag_value)
    capability_flag_values = exact_command_flag_values(report.get("exact_command"), "--capability")
    seen_capability_names: set[str] = set()
    for capability_flag_value in capability_flag_values:
        capability_name = capability_name_from_flag_value(capability_flag_value)
        if capability_name in seen_capability_names:
            errors.append(f"exact_command must not duplicate capability name: {capability_name}")
        seen_capability_names.add(capability_name)

    transcript_path = report.get("transcript_path")
    if root is not None and isinstance(transcript_path, str) and not transcript_path_is_external_reference(transcript_path):
        transcript_file = Path(root) / transcript_path
        if transcript_file.is_file():
            try:
                transcript_text = transcript_file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                transcript_text = ""
            if contains_secret_like_value(transcript_text):
                errors.append(
                    "runtime smoke transcript contains secret-like value; redact transcript before trusting artifact"
                )
            if contains_private_absolute_path(transcript_text):
                errors.append(
                    "runtime smoke transcript contains private absolute path; redact transcript before trusting artifact"
                )

    evidence = report.get("evidence")
    if isinstance(evidence, list):
        evidence_lines = [line for line in evidence if isinstance(line, str)]
        for prefix in REQUIRED_EVIDENCE_PREFIXES:
            if not any(line.startswith(prefix) for line in evidence_lines):
                errors.append(f"runtime smoke evidence must include line starting with: {prefix}")

    blocked_commands = report.get("blocked_commands")
    blocked_count = len(blocked_commands) if isinstance(blocked_commands, list) else 0
    if report.get("run_scope") == "full_validation" and blocked_count:
        errors.append("full_validation cannot list blocked_commands; use read_only_smoke or remove blockers")
    if report.get("smoke_result") == "blocked" and blocked_count == 0:
        errors.append("blocked smoke_result must list at least one blocked command")
    if report.get("smoke_result") == "pass" and blocked_count:
        errors.append("pass smoke_result cannot list blocked_commands; use blocked or fail when required commands could not run")
    capability_matrix = report.get("capability_matrix")
    if blocked_count and (
        not isinstance(capability_matrix, dict) or capability_matrix.get("blocked_command_reporting") != "yes"
    ):
        errors.append("blocked_commands require capability_matrix.blocked_command_reporting=yes")
    if blocked_count and isinstance(blocked_commands, list):
        for blocked_command in blocked_commands:
            if isinstance(blocked_command, str) and blocked_command and not exact_command_has_flag_value(
                report.get("exact_command"), "--blocked-command", blocked_command
            ):
                errors.append(
                    "exact_command must record blocked command flag: "
                    f"--blocked-command {blocked_command}"
                )
    runtime = report.get("runtime")
    if isinstance(runtime, str) and not exact_command_has_flag_value(
        report.get("exact_command"), "--runtime", runtime
    ):
        errors.append(f"exact_command must record runtime flag: --runtime {runtime}")
    version = report.get("version")
    if isinstance(version, str) and not exact_command_has_flag_value(
        report.get("exact_command"), "--version", version
    ):
        errors.append(f"exact_command must record version flag: --version {version}")
    selected_command = report.get("selected_command")
    if isinstance(selected_command, str) and selected_command.startswith("/brain-") and not exact_command_has_flag_value(
        report.get("exact_command"), "--selected-command", selected_command
    ):
        errors.append(f"exact_command must record selected command flag: --selected-command {selected_command}")
    loaded_skills = report.get("loaded_skills")
    if isinstance(loaded_skills, list):
        for skill in loaded_skills:
            if isinstance(skill, str) and skill and not exact_command_has_flag_value(
                report.get("exact_command"), "--loaded-skill", skill
            ):
                errors.append(f"exact_command must record loaded skill flag: --loaded-skill {skill}")
    adapter_path = report.get("adapter_path")
    if isinstance(adapter_path, str) and adapter_path != "unknown" and not exact_command_has_flag_value(
        report.get("exact_command"), "--adapter-path", adapter_path
    ):
        errors.append(f"exact_command must record adapter path flag: --adapter-path {adapter_path}")
    sandbox_write_mode = report.get("sandbox_write_mode")
    if isinstance(sandbox_write_mode, str) and not exact_command_has_flag_value(
        report.get("exact_command"), "--sandbox-write-mode", sandbox_write_mode
    ):
        errors.append(f"exact_command must record sandbox write mode flag: --sandbox-write-mode {sandbox_write_mode}")
    brain_command_mode = report.get("brain_command_mode")
    if isinstance(brain_command_mode, str) and not exact_command_has_flag_value(
        report.get("exact_command"), "--brain-command-mode", brain_command_mode
    ):
        errors.append(f"exact_command must record brain command mode flag: --brain-command-mode {brain_command_mode}")
    run_scope = report.get("run_scope")
    if isinstance(run_scope, str) and not exact_command_has_flag_value(report.get("exact_command"), "--run-scope", run_scope):
        errors.append(f"exact_command must record run scope flag: --run-scope {run_scope}")
    smoke_result = report.get("smoke_result")
    if isinstance(smoke_result, str) and not exact_command_has_flag_value(
        report.get("exact_command"), "--smoke-result", smoke_result
    ):
        errors.append(f"exact_command must record smoke result flag: --smoke-result {smoke_result}")
    command_exit_status = report.get("command_exit_status")
    if isinstance(command_exit_status, int) and not exact_command_has_flag_value(
        report.get("exact_command"), "--command-exit-status", str(command_exit_status)
    ):
        errors.append(
            "exact_command must record command exit status flag: "
            f"--command-exit-status {command_exit_status}"
        )
    transcript_redaction_status = report.get("transcript_redaction_status")
    if isinstance(transcript_redaction_status, str) and not exact_command_has_flag_value(
        report.get("exact_command"), "--transcript-redaction-status", transcript_redaction_status
    ):
        errors.append(
            "exact_command must record transcript redaction status flag: "
            f"--transcript-redaction-status {transcript_redaction_status}"
        )
    capability_matrix = report.get("capability_matrix")
    if isinstance(capability_matrix, dict):
        native_brain_command_status = capability_matrix.get("native_brain_commands")
        brain_command_mode = report.get("brain_command_mode")
        sandbox_write_mode = report.get("sandbox_write_mode")
        if sandbox_write_mode == "read_only" and capability_matrix.get("write_files") == "yes":
            errors.append("read_only sandbox_write_mode cannot claim write_files capability yes")
        if brain_command_mode == "native_commands" and native_brain_command_status != "yes":
            errors.append("native_commands mode requires native_brain_commands capability yes")
        if brain_command_mode == "mixed" and native_brain_command_status != "yes":
            errors.append("mixed command mode requires native_brain_commands capability yes")
        if brain_command_mode == "markdown_specs" and native_brain_command_status == "yes":
            errors.append("markdown_specs mode cannot claim native_brain_commands capability yes")
        for capability_name in CAPABILITY_NAMES:
            capability_status = capability_matrix.get(capability_name)
            if not isinstance(capability_status, str):
                continue
            if report.get("smoke_result") == "pass" and capability_status == "unknown":
                errors.append(
                    "pass smoke_result requires concrete capability status: "
                    f"{capability_name} cannot be unknown"
                )
            capability_flag = f"{capability_name}={capability_status}"
            if not exact_command_has_flag_value(report.get("exact_command"), "--capability", capability_flag):
                errors.append(f"exact_command must record capability flag: --capability {capability_flag}")
        if report.get("run_scope") == "full_validation":
            for capability_name in FULL_VALIDATION_REQUIRED_CAPABILITIES:
                if capability_matrix.get(capability_name) != "yes":
                    errors.append(f"full_validation requires proven runtime capability: {capability_name}=yes")
    if report.get("smoke_result") == "pass" and report.get("command_exit_status") != 0:
        errors.append("pass smoke_result requires command_exit_status 0")
    if report.get("smoke_result") == "fail" and report.get("command_exit_status") == 0:
        errors.append("fail smoke_result requires nonzero command_exit_status")
    if report.get("smoke_result") == "pass":
        if not version_is_concrete(report.get("version")):
            errors.append("pass smoke_result requires a concrete runtime version")
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
        adapter_path = report.get("adapter_path")
        if adapter_path == "unknown":
            errors.append("pass smoke_result requires an adapter_path")
        elif isinstance(adapter_path, str) and not exact_command_has_flag_value(
            report.get("exact_command"), "--adapter-path", adapter_path
        ):
            errors.append(f"exact_command must record adapter path flag: --adapter-path {adapter_path}")
        sandbox_write_mode = report.get("sandbox_write_mode")
        if isinstance(sandbox_write_mode, str) and not exact_command_has_flag_value(
            report.get("exact_command"), "--sandbox-write-mode", sandbox_write_mode
        ):
            errors.append(f"exact_command must record sandbox write mode flag: --sandbox-write-mode {sandbox_write_mode}")
        brain_command_mode = report.get("brain_command_mode")
        if isinstance(brain_command_mode, str) and not exact_command_has_flag_value(
            report.get("exact_command"), "--brain-command-mode", brain_command_mode
        ):
            errors.append(f"exact_command must record brain command mode flag: --brain-command-mode {brain_command_mode}")
        run_scope = report.get("run_scope")
        if isinstance(run_scope, str) and not exact_command_has_flag_value(
            report.get("exact_command"), "--run-scope", run_scope
        ):
            errors.append(f"exact_command must record run scope flag: --run-scope {run_scope}")
        transcript_path = report.get("transcript_path")
        if transcript_path == "not_captured_stdout_only":
            errors.append("pass smoke_result requires a durable transcript_path")
        elif root is not None and isinstance(transcript_path, str) and not transcript_path_is_external_reference(transcript_path):
            transcript_file = Path(root) / transcript_path
            if not transcript_file.is_file():
                errors.append(f"pass runtime smoke transcript file is missing: {transcript_path}")
            elif transcript_file.stat().st_size == 0:
                errors.append(f"pass runtime smoke transcript file is empty: {transcript_path}")
        if isinstance(transcript_path, str) and not exact_command_has_flag_value(
            report.get("exact_command"), "--transcript-path", transcript_path
        ):
            errors.append(f"exact_command must record transcript path flag: --transcript-path {transcript_path}")
        transcript_redaction_status = report.get("transcript_redaction_status")
        if transcript_redaction_status not in {"redacted", "no_sensitive_content"}:
            errors.append("pass smoke_result requires reviewed transcript redaction status: redacted or no_sensitive_content")
        smoke_result = report.get("smoke_result")
        if isinstance(smoke_result, str) and not exact_command_has_flag_value(
            report.get("exact_command"), "--smoke-result", smoke_result
        ):
            errors.append(f"exact_command must record smoke result flag: --smoke-result {smoke_result}")
        command_exit_status = report.get("command_exit_status")
        if isinstance(command_exit_status, int) and not exact_command_has_flag_value(
            report.get("exact_command"), "--command-exit-status", str(command_exit_status)
        ):
            errors.append(
                "exact_command must record command exit status flag: "
                f"--command-exit-status {command_exit_status}"
            )
        transcript_redaction_status = report.get("transcript_redaction_status")
        if isinstance(transcript_redaction_status, str) and not exact_command_has_flag_value(
            report.get("exact_command"), "--transcript-redaction-status", transcript_redaction_status
        ):
            errors.append(
                "exact_command must record transcript redaction status flag: "
                f"--transcript-redaction-status {transcript_redaction_status}"
            )
    if report.get("run_scope") == "full_validation" and report.get("smoke_result") != "pass":
        errors.append("full_validation requires smoke_result pass")
    if report.get("run_scope") == "full_validation" and report.get("sandbox_write_mode") == "read_only":
        errors.append("full_validation requires a write-capable sandbox; use read_only_smoke for read_only runs")
    if report.get("run_scope") == "full_validation" and report.get("transcript_path") == "not_captured_stdout_only":
        errors.append("full_validation requires a durable transcript_path instead of not_captured_stdout_only")
    if report.get("run_scope") == "full_validation" and isinstance(report.get("transcript_path"), str):
        transcript_path = report["transcript_path"]
        if root is not None and not transcript_path_is_external_reference(transcript_path):
            transcript_file = Path(root) / transcript_path
            if not transcript_file.is_file():
                errors.append(f"full_validation transcript file is missing: {transcript_path}")
            elif transcript_file.stat().st_size == 0:
                errors.append(f"full_validation transcript file is empty: {transcript_path}")
    if report.get("run_scope") == "full_validation" and report.get("transcript_redaction_status") not in {
        "redacted",
        "no_sensitive_content",
    }:
        errors.append("full_validation requires reviewed transcript redaction status: redacted or no_sensitive_content")
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
    git_fetch = report.get("git_fetch_result")
    if report.get("run_scope") == "full_validation" and not (
        isinstance(git_fetch, str) and git_fetch.startswith("fetched: git fetch origin main succeeded")
    ):
        errors.append("full_validation requires successful git fetch evidence")
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
        for validation_command in recorded_validation_commands:
            if isinstance(validation_command, str) and not exact_command_has_flag_value(
                report.get("exact_command"), "--validation-command", validation_command
            ):
                errors.append(
                    "exact_command must record validation command flag: "
                    f"--validation-command {validation_command}"
                )
        write_fence = report.get("write_fence")
        if not isinstance(write_fence, dict):
            errors.append("full_validation requires write_fence with allowed_paths")
            errors.append("full_validation requires write_fence with rollback_command")
        else:
            required_list_fields = [
                ("allowed_paths", "--write-fence-allowed-path"),
                ("disallowed_paths", "--write-fence-disallowed-path"),
            ]
            for field_name, flag in required_list_fields:
                values = write_fence.get(field_name)
                if not (isinstance(values, list) and any(isinstance(value, str) and value for value in values)):
                    errors.append(f"full_validation requires write_fence with {field_name}")
                    continue
                for value in values:
                    if isinstance(value, str) and value and not exact_command_has_flag_value(
                        report.get("exact_command"), flag, value
                    ):
                        errors.append(f"exact_command must record write fence flag: {flag} {value}")
            user_owned_files = write_fence.get("user_owned_files")
            git_worktree_status_value = report.get("git_worktree_status")
            if isinstance(git_worktree_status_value, str) and git_worktree_status_value.startswith("dirty:") and not (
                isinstance(user_owned_files, list)
                and any(isinstance(value, str) and value for value in user_owned_files)
            ):
                errors.append(
                    "full_validation with dirty worktree must name preserved user-owned files in "
                    "write_fence.user_owned_files"
                )
            if isinstance(user_owned_files, list):
                for value in user_owned_files:
                    if isinstance(value, str) and value and not exact_command_has_flag_value(
                        report.get("exact_command"), "--write-fence-user-owned-file", value
                    ):
                        errors.append(
                            "exact_command must record write fence flag: "
                            f"--write-fence-user-owned-file {value}"
                        )
            rollback_command = write_fence.get("rollback_command")
            if not (isinstance(rollback_command, str) and rollback_command.strip() and rollback_command != "not_applicable"):
                errors.append("full_validation requires write_fence with rollback_command")
            elif not exact_command_has_flag_value(
                report.get("exact_command"), "--write-fence-rollback-command", rollback_command
            ):
                errors.append(
                    "exact_command must record write fence flag: "
                    f"--write-fence-rollback-command {rollback_command}"
                )
            approval_state = write_fence.get("approval_state")
            if approval_state not in {"approved", "not_required"}:
                errors.append("full_validation requires write_fence with approval_state")
            elif report.get("sandbox_write_mode") == "unrestricted" and approval_state != "approved":
                errors.append(
                    "full_validation in unrestricted sandbox requires explicit write_fence approval_state approved"
                )
            elif not exact_command_has_flag_value(
                report.get("exact_command"), "--write-fence-approval-state", str(approval_state)
            ):
                errors.append(
                    "exact_command must record write fence flag: "
                    f"--write-fence-approval-state {approval_state}"
                )
            output_paths = exact_command_flag_values(report.get("exact_command"), "--output")
            allowed_paths = write_fence.get("allowed_paths")
            disallowed_paths = write_fence.get("disallowed_paths")
            for output_path in output_paths:
                if output_path == "-":
                    continue
                output_path_for_boundary = output_path
                if root is not None:
                    try:
                        output_path_for_boundary = Path(output_path).resolve().relative_to(Path(root).resolve()).as_posix()
                    except (OSError, ValueError):
                        output_path_for_boundary = output_path
                if not isinstance(allowed_paths, list) or not path_is_inside_declared_boundary(
                    output_path_for_boundary, allowed_paths
                ):
                    errors.append(
                        "full_validation output path must be inside write_fence.allowed_paths: "
                        f"{output_path}"
                    )
                if isinstance(disallowed_paths, list) and path_is_inside_declared_boundary(
                    output_path_for_boundary, disallowed_paths
                ):
                    errors.append(
                        "full_validation output path must not be inside write_fence.disallowed_paths: "
                        f"{output_path}"
                    )
    if root is not None:
        adapter_path = report.get("adapter_path")
        if isinstance(adapter_path, str) and adapter_path != "unknown":
            if not adapter_path_is_adapter_readme(adapter_path):
                errors.append("adapter_path must point to adapters/<adapter>/README.md")
            elif not (Path(root) / adapter_path).is_file():
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
                if report.get("smoke_result") == "pass":
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
    parser.add_argument(
        "--transcript-redaction-status",
        choices=sorted(TRANSCRIPT_REDACTION_STATUSES),
        default="not_captured",
        help="Whether the runtime transcript was redacted, contained no sensitive content, was not captured, or redaction was blocked",
    )
    parser.add_argument("--blocked-command", action="append", default=[], help="Command that was blocked or intentionally skipped")
    parser.add_argument(
        "--validation-command",
        action="append",
        default=None,
        help="Successful local gate command completed during full validation; repeat for each gate command",
    )
    parser.add_argument(
        "--capability",
        action="append",
        default=[],
        help="Runtime capability as name=status; names are read_files, write_files, run_shell, request_approvals, network_access, native_brain_commands, schema_artifacts, blocked_command_reporting; statuses are yes, no, unknown, blocked",
    )
    parser.add_argument(
        "--write-fence-allowed-path",
        action="append",
        default=[],
        help="Path the full-validation runtime was allowed to write; repeat for each path",
    )
    parser.add_argument(
        "--write-fence-disallowed-path",
        action="append",
        default=[],
        help="Path the full-validation runtime was forbidden to write; repeat for each path",
    )
    parser.add_argument(
        "--write-fence-user-owned-file",
        action="append",
        default=[],
        help="User-owned file or dirty path preserved by the write fence; repeat for each path",
    )
    parser.add_argument(
        "--write-fence-rollback-command",
        default="not_applicable",
        help="Rollback command for full-validation writes",
    )
    parser.add_argument(
        "--write-fence-approval-state",
        choices=sorted(WRITE_FENCE_APPROVAL_STATES),
        default="unknown",
        help="Approval state for full-validation writes: approved, not_required, blocked, or unknown",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root to inspect")
    parser.add_argument("--schema", type=Path, help="Runtime-smoke schema path; defaults to <root>/schemas/runtime-smoke.schema.json")
    parser.add_argument("--output", type=Path, help="Optional JSON output path; stdout is used when omitted")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    raw_argv = sys.argv[1:] if argv is None else argv
    exact_command = "python scripts/runtime_smoke.py " + " ".join(shlex.quote(arg) for arg in raw_argv)
    try:
        capability_matrix = parse_capability_flags(args.capability)
    except ValueError as exc:
        sys.stderr.write(f"runtime smoke argument error: {exc}\n")
        return 2

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
        transcript_redaction_status=args.transcript_redaction_status,
        selected_command=args.selected_command,
        loaded_skills=args.loaded_skill,
        adapter_path=args.adapter_path,
        validation_commands=args.validation_command,
        write_fence_allowed_paths=args.write_fence_allowed_path,
        write_fence_disallowed_paths=args.write_fence_disallowed_path,
        write_fence_user_owned_files=args.write_fence_user_owned_file,
        write_fence_rollback_command=args.write_fence_rollback_command,
        write_fence_approval_state=args.write_fence_approval_state,
        capability_matrix=capability_matrix,
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
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

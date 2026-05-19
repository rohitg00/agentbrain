#!/usr/bin/env python3
"""Check whether an Agent Brain checkout is ready for agent use."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

try:
    import validate_repo
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.doctor
    from scripts import validate_repo

REQUIRED_ENTRYPOINTS = [
    "README.md",
    "AGENTS.md",
    "AGENTBRAIN.md",
    "INSTALL_FOR_AGENTS.md",
    "commands/README.md",
    "commands/registry.json",
    "docs/state-machine.md",
]
ROOT_PUBLIC_DOCS = ["README.md", "AGENTS.md", "INSTALL_FOR_AGENTS.md"]


def run_git(root: Path, *args: str) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception as exc:
        return False, str(exc)

    output = (completed.stdout or completed.stderr).strip()
    if completed.returncode != 0:
        return False, output or f"git {' '.join(args)} exited {completed.returncode}"
    return True, output


def git_info(root: Path) -> dict[str, str]:
    status_ok, status = run_git(root, "status", "--short")
    head_ok, head = run_git(root, "rev-parse", "HEAD")
    origin_ok, origin_main = run_git(root, "rev-parse", "origin/main")

    if head_ok and origin_ok and head == origin_main:
        freshness = "fresh"
    elif head_ok and origin_ok:
        freshness = "stale"
    else:
        freshness = "unknown"

    return {
        "worktree_status": "clean" if status_ok and not status else status or "unavailable",
        "head": head if head_ok else "unavailable",
        "origin_main": origin_main if origin_ok else "unavailable",
        "freshness": freshness,
    }


def entrypoint_status(root: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for rel_path in REQUIRED_ENTRYPOINTS:
        entries.append(
            {
                "path": rel_path,
                "status": "present" if (root / rel_path).exists() else "missing",
            }
        )
    return entries


def public_copy_status(root: Path) -> dict[str, bool]:
    exposed = False
    for rel_path in ROOT_PUBLIC_DOCS:
        path = root / rel_path
        if path.exists() and "scrub_public_copy.py" in path.read_text(errors="ignore"):
            exposed = True
            break
    readme_path = root / "README.md"
    readme_exposes = readme_path.exists() and "scrub_public_copy.py" in readme_path.read_text(errors="ignore")
    return {
        "readme_exposes_local_scrub_command": readme_exposes,
        "root_agent_docs_expose_local_scrub_command": exposed,
    }


def python_is_supported() -> bool:
    return sys.version_info >= (3, 11)


def build_report(root: Path) -> dict[str, object]:
    root = root.resolve()
    validation_errors = validate_repo.validate(root)
    git = git_info(root)
    entrypoints = entrypoint_status(root)
    public_copy = public_copy_status(root)

    blockers: list[str] = []
    warnings: list[str] = []
    next_actions: list[str] = []

    if not python_is_supported():
        blockers.append("Python 3.11 or newer is required")
        next_actions.append("create a Python 3.11 virtual environment and reinstall requirements")

    missing_entrypoints = [entry["path"] for entry in entrypoints if entry["status"] == "missing"]
    for rel_path in missing_entrypoints:
        blockers.append(f"missing required entrypoint: {rel_path}")
    if missing_entrypoints:
        next_actions.append("restore missing entrypoint files before running the harness")

    if validation_errors:
        blockers.append(f"repository validation has {len(validation_errors)} error(s)")
        next_actions.append("run python scripts/validate_repo.py and fix the listed errors")

    if public_copy["root_agent_docs_expose_local_scrub_command"]:
        blockers.append("root public docs expose maintainer-only local scrub command")
        next_actions.append("remove local-only maintenance commands from public setup docs")

    if git["worktree_status"] != "clean":
        warnings.append("working tree is not clean; preserve user changes before editing")
    if git["freshness"] != "fresh":
        warnings.append("HEAD is not confirmed equal to origin/main")

    readiness = "blocked" if blockers else "warn" if warnings else "pass"
    if not next_actions:
        next_actions.append("select a command from commands/registry.json and proceed")

    return {
        "schema_version": "1",
        "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(root),
        "python": {
            "executable": sys.executable,
            "version": platform.python_version(),
            "supported": python_is_supported(),
        },
        "git": git,
        "required_entrypoints": entrypoints,
        "public_copy": public_copy,
        "validator": {
            "status": "pass" if not validation_errors else "fail",
            "error_count": len(validation_errors),
            "errors": validation_errors,
        },
        "readiness": readiness,
        "warnings": warnings,
        "blockers": blockers,
        "next_actions": next_actions,
    }


def validate_report(report: dict[str, object], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [error.message for error in sorted(validator.iter_errors(report), key=lambda item: list(item.path))]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root to inspect")
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path("schemas/doctor-report.schema.json"),
        help="doctor report schema path",
    )
    parser.add_argument("--output", type=Path, help="write JSON report to this path")
    parser.add_argument("--no-fail", action="store_true", help="exit 0 even when readiness is blocked")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    schema_path = args.schema if args.schema.is_absolute() else root / args.schema
    report = build_report(root)
    errors = validate_report(report, schema_path)
    if errors:
        sys.stderr.write("doctor report schema validation failed:\n")
        for error in errors:
            sys.stderr.write(f"- {error}\n")
        return 2

    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else root / args.output
        output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)

    if report["readiness"] == "blocked" and not args.no_fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

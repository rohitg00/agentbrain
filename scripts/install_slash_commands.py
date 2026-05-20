#!/usr/bin/env python3
"""Generate thin slash-command wrappers from commands/registry.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CC_RUNTIME = "clau" + "de-code"
SUPPORTED_RUNTIMES = (CC_RUNTIME, "gemini-cli")
SAFE_SLUG_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def load_registry(root: Path) -> list[dict[str, object]]:
    registry_path = root / "commands" / "registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    commands = registry.get("commands")
    if not isinstance(commands, list):
        raise ValueError("commands/registry.json must contain a commands array")
    entries: list[dict[str, object]] = []
    for index, entry in enumerate(commands):
        if not isinstance(entry, dict):
            raise ValueError(
                "commands/registry.json commands entry "
                f"{index} must be an object, got {type(entry).__name__}"
            )
        entries.append(entry)
    return entries


def command_slug(command_name: object) -> str:
    if not isinstance(command_name, str) or not command_name.startswith("/"):
        raise ValueError(f"invalid command name: {command_name!r}")
    slug = command_name.removeprefix("/")
    if not slug or "/" in slug or "\\" in slug or ".." in slug or not SAFE_SLUG_RE.fullmatch(slug):
        raise ValueError(f"invalid command slug: {slug!r}")
    return slug


def skills_text(entry: dict[str, object]) -> str:
    skills = entry.get("skills")
    if not isinstance(skills, list):
        return "none"
    return ", ".join(f"`{skill}`" for skill in skills if isinstance(skill, str)) or "none"


def wrapper_prompt(entry: dict[str, object], argument_line: str, boundary_marker: str) -> str:
    command_name = str(entry["name"])
    command_file = str(entry["file"])
    schema = entry.get("schema")
    schema_text = str(schema) if isinstance(schema, str) else "none"
    return "\n".join(
        [
            f"Use Agent Brain command `{command_name}`.",
            "",
            "This runtime wrapper is only an activation shortcut. "
            f"The source of truth is `{command_file}` and `commands/registry.json`.",
            f"Wrapper boundary marker: `{boundary_marker}`.",
            "",
            "Before acting:",
            "- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.",
            f"- Read `{command_file}` and follow it exactly.",
            f"- Load only these skills: {skills_text(entry)}.",
            f"- Produce the required artifact: `{entry['required_artifact']}`.",
            f"- Validate against schema: `{schema_text}`.",
            "- Preserve user changes before editing.",
            "- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.",
            "",
            "If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.",
            "",
            argument_line,
            "",
        ]
    )


def cc_skill(entry: dict[str, object]) -> str:
    slug = command_slug(entry["name"])
    description = f"Agent Brain {entry['name']}: {entry['use_when']}."
    return "\n".join(
        [
            "---",
            f"name: {slug}",
            f"description: {description}",
            "disable-model-invocation: true",
            "---",
            "",
            wrapper_prompt(entry, "User arguments: $ARGUMENTS", "cc-source-of-truth"),
        ]
    )


def gemini_command(entry: dict[str, object]) -> str:
    description = f"Agent Brain {entry['name']}: {entry['use_when']}."
    return "\n".join(
        [
            f"description = {json.dumps(description)}",
            f"prompt = {json.dumps(wrapper_prompt(entry, 'If arguments are provided, Gemini CLI appends them after these instructions.', 'gemini-cli-source-of-truth'))}",
            "",
        ]
    )


def target_path(runtime: str, entry: dict[str, object], root: Path, scope: str, output_dir: Path | None) -> Path:
    slug = command_slug(entry["name"])
    if output_dir is not None:
        base = output_dir
    elif runtime == CC_RUNTIME:
        cc_dir = "." + "clau" + "de"
        base = root / cc_dir / "skills" if scope == "project" else Path.home() / cc_dir / "skills"
    elif runtime == "gemini-cli":
        base = root / ".gemini" / "commands" if scope == "project" else Path.home() / ".gemini" / "commands"
    else:  # pragma: no cover - argparse prevents this
        raise ValueError(f"unsupported runtime: {runtime}")

    if runtime == CC_RUNTIME:
        return base / slug / "SKILL.md"
    return base / f"{slug}.toml"


def rendered_content(runtime: str, entry: dict[str, object]) -> str:
    if runtime == CC_RUNTIME:
        return cc_skill(entry)
    if runtime == "gemini-cli":
        return gemini_command(entry)
    raise ValueError(f"unsupported runtime: {runtime}")


def install(
    *,
    root: Path,
    runtime: str,
    scope: str,
    output_dir: Path | None = None,
    check: bool = False,
    dry_run: bool = False,
) -> tuple[list[Path], list[str]]:
    if runtime not in SUPPORTED_RUNTIMES:
        raise ValueError(f"unsupported runtime: {runtime}")

    written: list[Path] = []
    errors: list[str] = []
    for entry in load_registry(root):
        path = target_path(runtime, entry, root, scope, output_dir)
        expected = rendered_content(runtime, entry)
        if check:
            if not path.exists():
                errors.append(f"missing slash-command wrapper: {path}")
                continue
            actual = path.read_text(encoding="utf-8")
            if actual != expected:
                errors.append(f"slash-command wrapper drift: {path}")
                continue
            written.append(path)
            continue
        if dry_run:
            written.append(path)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected, encoding="utf-8")
        written.append(path)
    return written, errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", required=True, choices=SUPPORTED_RUNTIMES)
    parser.add_argument("--scope", choices=("project", "user"), default="project")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--check", action="store_true", help="fail if wrappers are missing or drifted")
    parser.add_argument("--dry-run", action="store_true", help="print planned wrapper paths without writing files")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    written, errors = install(
        root=args.root,
        runtime=args.runtime,
        scope=args.scope,
        output_dir=args.output_dir,
        check=args.check,
        dry_run=args.dry_run,
    )
    if errors:
        for error in errors:
            sys.stderr.write(error + "\n")
        return 1
    print(
        json.dumps(
            {
                "runtime": args.runtime,
                "scope": args.scope,
                "mode": "check" if args.check else "dry-run" if args.dry_run else "write",
                "paths": [str(path) for path in written],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
PLUGIN_RUNTIME = "agentbrain-plugin"
PLUGIN_NAME = "agentbrain"
PLUGIN_ROOT = Path("plugins") / PLUGIN_NAME
SUPPORTED_RUNTIMES = (PLUGIN_RUNTIME, CC_RUNTIME, "gemini-cli")
SAFE_SLUG_RE = re.compile(r"^[A-Za-z0-9_-]+$")
PLUGIN_ALWAYS_COPY = (
    Path("AGENTBRAIN.md"),
    Path("PRINCIPLES.md"),
    Path("ANTI_RATIONALIZATION.md"),
    Path("commands") / "README.md",
    Path("docs") / "state-machine.md",
    Path("skills") / "README.md",
)


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


def read_required(root: Path, rel_path: Path) -> str:
    path = root / rel_path
    if not path.exists():
        raise ValueError(f"missing plugin bundle source file: {rel_path.as_posix()}")
    return path.read_text(encoding="utf-8")


def plugin_command(entry: dict[str, object], root: Path) -> str:
    command_file = Path(str(entry["file"]))
    command_body = read_required(root, command_file).rstrip()
    header = wrapper_prompt(
        entry,
        "Plugin arguments: use the user's current request, selected text, or supplied command arguments. Plugin-local registry: `registry.json`.",
        "plugin-bundle-source-of-truth",
    ).rstrip()
    return "\n".join(
        [
            "<!-- Generated by scripts/install_slash_commands.py --runtime agentbrain-plugin. -->",
            f"<!-- Source file: {command_file.as_posix()}. -->",
            "",
            header,
            "",
            "For plugin installs, the command body below is bundled so agents do not need project-local slash-command files. In the source checkout, the repository command file remains the source of truth.",
            "",
            "## Bundled Command Body",
            "",
            command_body,
            "",
        ]
    )


def plugin_registry(commands: list[dict[str, object]]) -> str:
    plugin_commands = []
    for entry in commands:
        plugin_entry = dict(entry)
        plugin_entry["file"] = f"commands/{command_slug(entry['name'])}.md"
        plugin_entry["source_file"] = entry["file"]
        plugin_commands.append(plugin_entry)
    return json.dumps({"schema_version": "1", "commands": plugin_commands}, indent=2) + "\n"


def plugin_skill(commands: list[dict[str, object]]) -> str:
    command_lines = []
    for entry in commands:
        command_lines.append(
            f"- `{entry['name']}` -> `{entry['file']}`; skills: {skills_text(entry)}; artifact: `{entry['required_artifact']}`"
        )
    return "\n".join(
        [
            "---",
            "name: agentbrain",
            "description: Use when an agent needs Agent Brain's lifecycle, command routing, skills, artifacts, validation proof, or handoff discipline from an installed plugin.",
            "disable-model-invocation: true",
            "---",
            "# agentbrain",
            "",
            "Use Agent Brain as an installed operating harness for coding-agent work.",
            "",
            "## Trigger",
            "",
            "Use when a user request should route through Agent Brain instead of free-form chat, especially for planning, building, verification, review, shipping, or learning.",
            "",
            "## Source of Truth",
            "",
            "- Plugin-local `registry.json` defines installed command routing.",
            "- Plugin-local `commands/brain-*.md` files include installed command bodies copied from the source specs.",
            "- Plugin-local `skills/`, `templates/`, `schemas/`, and core docs carry the portable harness context.",
            "- Repository `commands/registry.json` and `commands/brain-*.md` files define the generated source material.",
            "- This plugin is an activation bundle; it must not replace the command files.",
            "- If plugin instructions conflict with repository commands in the source checkout, follow the repository command and route wrapper drift through `/brain-verify`.",
            "",
            "## Commands",
            "",
            *command_lines,
            "",
            "## Procedure",
            "",
            "1. Read plugin-local `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`; prefer source-checkout copies when they exist.",
            "2. Select the matching command from plugin-local `registry.json` or source-checkout `commands/registry.json`.",
            "3. Load only the command-listed skills.",
            "4. Produce the command's required artifact and schema-valid output when a schema exists.",
            "5. Preserve user changes before editing.",
            "6. Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.",
            "",
            "## Verification",
            "",
            "- `python scripts/install_slash_commands.py --runtime agentbrain-plugin --check`",
            "- `python scripts/validate_repo.py`",
            "",
            "## Failure Modes",
            "",
            "Stop if a plugin command lacks a matching registry entry, points to a missing command file, loads extra skills, or claims native support the runtime has not proven.",
        ]
    )


def cx_plugin_manifest() -> str:
    return json.dumps(
        {
            "name": PLUGIN_NAME,
            "version": "0.1.0",
            "description": "Portable Agent Brain lifecycle, command routing, validation, and handoff discipline.",
            "author": {"name": "Agent Brain Maintainers", "url": "https://github.com/rohitg00/agentbrain"},
            "homepage": "https://github.com/rohitg00/agentbrain",
            "repository": "https://github.com/rohitg00/agentbrain",
            "license": "MIT",
            "keywords": ["agent-harness", "slash-commands", "verification", "handoff"],
            "skills": "./skills/",
            "interface": {
                "displayName": "Agent Brain",
                "shortDescription": "Lifecycle and proof gates for coding agents.",
                "longDescription": "Routes agent work through command specs, skills, artifact contracts, validation evidence, and handoffs.",
                "developerName": "Agent Brain Maintainers",
                "category": "Productivity",
                "capabilities": ["Interactive", "Write"],
                "websiteURL": "https://github.com/rohitg00/agentbrain",
                "defaultPrompt": [
                    "Route this request through Agent Brain.",
                    "Plan this change with proof gates.",
                    "Verify this work before review.",
                ],
                "brandColor": "#111827",
            },
        },
        indent=2,
    ) + "\n"


def cc_plugin_manifest() -> str:
    return json.dumps(
        {
            "name": PLUGIN_NAME,
            "description": "Portable Agent Brain lifecycle, command routing, validation, and handoff discipline.",
            "version": "0.1.0",
            "skills": "./skills/",
            "commands": "./commands/",
        },
        indent=2,
    ) + "\n"


def cc_marketplace() -> str:
    return json.dumps(
        {
            "name": "agentbrain",
            "owner": {"name": "Agent Brain Maintainers"},
            "plugins": [
                {
                    "name": PLUGIN_NAME,
                    "source": "./plugins/agentbrain",
                    "description": "Agent Brain lifecycle and proof-gate plugin.",
                    "version": "0.1.0",
                }
            ],
        },
        indent=2,
    ) + "\n"


def agent_marketplace() -> str:
    return json.dumps(
        {
            "name": "agentbrain",
            "interface": {"displayName": "Agent Brain"},
            "plugins": [
                {
                    "name": PLUGIN_NAME,
                    "source": {"source": "local", "path": "./plugins/agentbrain"},
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                    "category": "Productivity",
                }
            ],
        },
        indent=2,
    ) + "\n"


def plugin_support_paths(root: Path, commands: list[dict[str, object]]) -> list[Path]:
    paths = set(PLUGIN_ALWAYS_COPY)
    paths.update(path.relative_to(root) for path in (root / "templates").glob("*.md"))
    paths.update(path.relative_to(root) for path in (root / "schemas").glob("*.json"))
    paths.update(path.relative_to(root) for path in (root / "skills").glob("*/SKILL.md"))
    for entry in commands:
        paths.add(Path(str(entry["file"])))
        artifact = entry.get("required_artifact")
        if isinstance(artifact, str):
            paths.add(Path(artifact))
        schema = entry.get("schema")
        if isinstance(schema, str):
            paths.add(Path(schema))
        skills = entry.get("skills")
        if isinstance(skills, list):
            for skill in skills:
                if isinstance(skill, str):
                    paths.add(Path("skills") / skill / "SKILL.md")
    return sorted(paths, key=lambda path: path.as_posix())


def plugin_bundle_files(root: Path) -> list[tuple[Path, str]]:
    commands = load_registry(root)
    files: list[tuple[Path, str]] = [
        (root / ("." + "clau" + "de-plugin") / "marketplace.json", cc_marketplace()),
        (root / ".agents" / "plugins" / "marketplace.json", agent_marketplace()),
        (root / PLUGIN_ROOT / ("." + "clau" + "de-plugin") / "plugin.json", cc_plugin_manifest()),
        (root / PLUGIN_ROOT / ("." + "co" + "dex-plugin") / "plugin.json", cx_plugin_manifest()),
        (root / PLUGIN_ROOT / "registry.json", plugin_registry(commands)),
        (root / PLUGIN_ROOT / "skills" / PLUGIN_NAME / "SKILL.md", plugin_skill(commands)),
    ]
    command_source_paths = {Path(str(entry["file"])) for entry in commands}
    for rel_path in plugin_support_paths(root, commands):
        if rel_path in command_source_paths:
            continue
        files.append((root / PLUGIN_ROOT / rel_path, read_required(root, rel_path)))
    for entry in commands:
        files.append((root / PLUGIN_ROOT / "commands" / f"{command_slug(entry['name'])}.md", plugin_command(entry, root)))
    return files


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


def install_plugin_bundle(*, root: Path, check: bool = False, dry_run: bool = False) -> tuple[list[Path], list[str]]:
    written: list[Path] = []
    errors: list[str] = []
    for path, expected in plugin_bundle_files(root):
        if check:
            if not path.exists():
                errors.append(f"missing plugin bundle file: {path}")
                continue
            actual = path.read_text(encoding="utf-8")
            if actual != expected:
                errors.append(f"plugin bundle drift: {path}")
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
    if runtime == PLUGIN_RUNTIME:
        if output_dir is not None:
            raise ValueError("--output-dir is not supported for agentbrain-plugin")
        return install_plugin_bundle(root=root, check=check, dry_run=dry_run)

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

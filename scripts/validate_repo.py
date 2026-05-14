#!/usr/bin/env python3
from pathlib import Path
import json
import sys

from jsonschema import validators

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ROOT = ["README.md", "AGENTBRAIN.md", "PRINCIPLES.md", "ANTI_RATIONALIZATION.md"]
REQUIRED_SKILL_SECTIONS = [
    "## Trigger",
    "## Inputs",
    "## Procedure",
    "## Verification",
    "## Failure Modes",
    "## Example",
]
REQUIRED_COMMAND_SECTIONS = [
    "## Purpose",
    "## When to use",
    "## Input contract",
    "## Workflow",
    "## Output",
    "## Stop conditions",
]
REQUIRED_EVAL_CASE_SECTIONS = ["## User request", "## Expected behavior", "## Failure if"]
BANNED_PUBLIC_COPY_TERMS = ["Garry", "GBrain", "GStack", "Hermes vs", "OpenClaw vs", "Claude vs", "Codex vs"]


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}

    try:
        frontmatter = text.split("---", 2)[1]
    except IndexError:
        return {}

    parsed: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip().strip('"\'')
    return parsed


def validate(root: Path = ROOT) -> list[str]:
    root = Path(root)
    errors: list[str] = []

    for path in sorted((root / "schemas").glob("*.json")):
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            schema_validator = validators.validator_for(schema)
            schema_validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"invalid json schema {rel(path, root)}: {exc}")

    for required_path in REQUIRED_ROOT:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        text = skill.read_text(errors="ignore")
        frontmatter = parse_frontmatter(text)
        expected_name = skill.parent.name
        if frontmatter.get("name") != expected_name:
            errors.append(f"{rel(skill, root)} frontmatter name must be {expected_name}")
        if not frontmatter.get("description"):
            errors.append(f"{rel(skill, root)} frontmatter description is required")
        for section in REQUIRED_SKILL_SECTIONS:
            if section not in text:
                errors.append(f"{rel(skill, root)} missing {section}")

    for command in sorted((root / "commands").glob("*.md")):
        text = command.read_text(errors="ignore")
        expected_heading = f"# /{command.stem}"
        first_line = text.splitlines()[0] if text.splitlines() else ""
        if first_line != expected_heading:
            errors.append(f"{rel(command, root)} heading must be {expected_heading}")
        for section in REQUIRED_COMMAND_SECTIONS:
            if section not in text:
                errors.append(f"{rel(command, root)} missing {section}")

    for case in sorted((root / "evals" / "cases").glob("*.md")):
        text = case.read_text(errors="ignore")
        for section in REQUIRED_EVAL_CASE_SECTIONS:
            if section not in text:
                errors.append(f"{rel(case, root)} missing {section}")

    for markdown_file in sorted(root.rglob("*.md")):
        if ".git" in markdown_file.parts:
            continue
        text = markdown_file.read_text(errors="ignore")
        for term in BANNED_PUBLIC_COPY_TERMS:
            if term in text:
                errors.append(f"{rel(markdown_file, root)} contains banned public-copy term: {term}")

    return errors


def main() -> int:
    errors = validate(ROOT)
    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

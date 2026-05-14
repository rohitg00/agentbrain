#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys

from jsonschema import validators

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ROOT = [
    "README.md",
    "AGENTBRAIN.md",
    "PRINCIPLES.md",
    "ANTI_RATIONALIZATION.md",
    "CONTRIBUTING.md",
]
REQUIRED_FILES = ["requirements-dev.txt"]
REQUIRED_DEV_REQUIREMENTS = ["jsonschema", "pytest"]
REQUIRED_DIRECTORIES = ["schemas"]
REQUIRED_GITIGNORE_PATTERNS = ["__pycache__/", "*.py[cod]", ".pytest_cache/", ".venv/"]
REQUIRED_DOCS = [
    "docs/agent-harness.md",
    "docs/autonomous-goals.md",
    "docs/skill-distillation.md",
]
REQUIRED_SKILLS = [
    "skills/activity-recap/SKILL.md",
    "skills/agent-output-verifier/SKILL.md",
]
REQUIRED_EVAL_CASES = [
    "evals/cases/activity-recap.md",
    "evals/cases/source-to-skill-distillation.md",
    "evals/cases/agent-output-verifier.md",
    "evals/cases/verification-shortcut.md",
    "evals/cases/skill-boundary-creep.md",
    "evals/cases/no-user-defined.md",
    "evals/cases/review-gate-skip.md",
    "evals/cases/plan-slicing.md",
    "evals/cases/context-drift.md",
    "evals/cases/spec-before-build.md",
    "evals/cases/test-first-implementation.md",
    "evals/cases/ship-without-rollback.md",
    "evals/cases/security-risk-feature.md",
]
REQUIRED_EVAL_DOCS = ["evals/README.md"]
REQUIRED_WORKFLOWS = [".github/workflows/quality.yml"]
REQUIRED_QUALITY_WORKFLOW_RUNS = [
    "python -m pip install -r requirements-dev.txt",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
]
REQUIRED_WORKFLOW_TRIGGERS = ["push", "pull_request"]
REQUIRED_README_VALIDATION_COMMANDS = [
    "pip install -r requirements-dev.txt",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
]
REQUIRED_README_HARNESS_SECTIONS = [
    "## Quickstart",
    "## Run as an Agent Harness",
    "## Command Selection Guide",
    "## Edge Cases and Stop Conditions",
    "## Troubleshooting",
]
REQUIRED_AGENT_HARNESS_SECTIONS = [
    "## Install",
    "## Operating Loop",
    "## Handoff Contract",
    "## Stop Conditions",
    "## Troubleshooting",
]
REQUIRED_AGENT_HARNESS_VALIDATION_COMMANDS = [
    "pip install -r requirements-dev.txt",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
]
REQUIRED_CONTRIBUTING_VALIDATION_COMMANDS = ["pytest -q", "git diff --check"]
RESEARCH_WATCHLIST_REQUIRED_SOURCES = [
    "autonomous-goal runtime docs",
    "service-layer skill pattern",
    "small composable engineering skills",
    "methodology skill library",
    "harness integration skill library",
]
REQUIRED_SKILL_SECTIONS = [
    "## Trigger",
    "## Inputs",
    "## Procedure",
    "## Verification",
    "## Failure Modes",
    "## Example",
]
REQUIRED_SKILL_TEMPLATE_SECTIONS = [
    "## Trigger",
    "## Inputs",
    "## Procedure",
    "## Anti-Rationalization",
    "## Verification",
    "## Output Artifact",
    "## Failure Modes",
    "## Example",
]
REQUIRED_COMMAND_SECTIONS = [
    "## Purpose",
    "## When to use",
    "## Input contract",
    "## Skills to load",
    "## Workflow",
    "## Output",
    "## Stop conditions",
    "## Quality bar",
]
REQUIRED_EVAL_CASE_SECTIONS = ["## User request", "## Expected behavior", "## Failure if"]
REQUIRED_EVAL_RUBRIC_SECTIONS = ["## Dimensions", "## Interpretation"]
BANNED_PUBLIC_COPY_TERMS = [
    "G" + "arry",
    "G" + "Brain",
    "G" + "Stack",
    "Her" + "mes vs",
    "Open" + "Claw vs",
    "Clau" + "de",
    "Co" + "dex",
    "Open" + "AI",
    "Anth" + "ropic",
]
PUBLIC_COPY_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
PUBLIC_COPY_EXCLUDED_PARTS = {
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "venv",
}
LOWERCASE_KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def has_delimited_frontmatter(text: str) -> bool:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return False
    for line in lines[1:]:
        if line == "---":
            return True
        if line.startswith("# "):
            return False
    return False


def parse_frontmatter(text: str) -> dict[str, str]:
    if not has_delimited_frontmatter(text):
        return {}

    frontmatter = text.split("---", 2)[1]

    parsed: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip().strip('"\'')
    return parsed


def markdown_h1_headings(text: str) -> list[str]:
    headings: list[str] = []
    in_fenced_code = False
    for line in text.splitlines():
        if line.startswith("```") or line.startswith("~~~"):
            in_fenced_code = not in_fenced_code
            continue
        if not in_fenced_code and line.startswith("# "):
            headings.append(line)
    return headings


def term_is_only_in_readme_comparison_section(text: str, term: str) -> bool:
    term_lower = term.lower()
    if term_lower not in text.lower():
        return True

    in_allowed_section = False
    for line in text.splitlines():
        if line.startswith("## "):
            heading = line.lower().strip("# ")
            in_allowed_section = heading in {"vs others", "benchmarks", "comparisons"}
        if term_lower in line.lower() and not in_allowed_section:
            return False
    return True


def public_copy_term_allowed(path: Path, text: str, term: str) -> bool:
    return path.name == "README.md" and term_is_only_in_readme_comparison_section(text, term)


def find_trailing_whitespace_lines(text: str) -> list[int]:
    return [
        line_number
        for line_number, line in enumerate(text.splitlines(), 1)
        if line.endswith((" ", "\t"))
    ]


def reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    parsed: dict[str, object] = {}
    for key, value in pairs:
        if key in parsed:
            raise ValueError(f"duplicate key: {key}")
        parsed[key] = value
    return parsed


def title_from_slug(slug: str) -> str:
    connector_words = {"and", "or", "the", "to", "vs"}
    parts = slug.split("-")
    titled_parts = [part if part in connector_words else part.capitalize() for part in parts]
    return " ".join(titled_parts)


def adapter_heading_from_slug(slug: str) -> str:
    title = title_from_slug(slug)
    if title.endswith(" Adapter"):
        return f"# {title}"
    return f"# {title} Adapter"


def validate_single_h1(path: Path, root: Path) -> str | None:
    text = path.read_text(errors="ignore")
    h1_headings = markdown_h1_headings(text)
    if len(h1_headings) != 1:
        return f"{rel(path, root)} must contain exactly one H1 heading"
    return None


def is_lowercase_kebab(value: str) -> bool:
    return bool(LOWERCASE_KEBAB_RE.fullmatch(value))


def section_has_body(text: str, section: str) -> bool:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line != section:
            continue
        body_lines = []
        for following_line in lines[index + 1 :]:
            if following_line.startswith("## "):
                break
            body_lines.append(following_line)
        return bool("\n".join(body_lines).strip())
    return False


def section_body(text: str, section: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line != section:
            continue
        body_lines = []
        for following_line in lines[index + 1 :]:
            if following_line.startswith("## "):
                break
            body_lines.append(following_line)
        return "\n".join(body_lines)
    return ""


def sections_are_in_order(text: str, sections: list[str]) -> bool:
    lines = text.splitlines()
    positions = [lines.index(section) for section in sections if section in lines]
    return positions == sorted(positions)


def requirement_name(line: str) -> str:
    requirement = line.strip()
    if not requirement or requirement.startswith("#"):
        return ""
    return re.split(r"\s*(?:[<>=!~]=|==|>|<|~=|\[)", requirement, maxsplit=1)[0].lower()


def find_missing_dev_requirements(text: str) -> list[str]:
    installed = {requirement_name(line) for line in text.splitlines()}
    return [requirement for requirement in REQUIRED_DEV_REQUIREMENTS if requirement not in installed]


def workflow_declares_trigger(workflow_text: str, trigger: str) -> bool:
    workflow_lines = [line.strip() for line in workflow_text.splitlines()]
    if f"{trigger}:" in workflow_lines or f"on: {trigger}" in workflow_lines:
        return True
    for line in workflow_lines:
        if not line.startswith("on: [") or not line.endswith("]"):
            continue
        inline_triggers = [item.strip() for item in line.removeprefix("on: [").removesuffix("]").split(",")]
        if trigger in inline_triggers:
            return True

    in_on_block = False
    for raw_line in workflow_text.splitlines():
        if raw_line == "on:":
            in_on_block = True
            continue
        if in_on_block and raw_line and not raw_line.startswith((" ", "\t")):
            break
        if in_on_block and raw_line.strip() == f"- {trigger}":
            return True
    return False


def workflow_sets_readonly_contents_permission(workflow_text: str) -> bool:
    permissions_block_indent: int | None = None
    for raw_line in workflow_text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        line_indent = len(raw_line) - len(raw_line.lstrip(" \t"))
        if stripped == "permissions: read-all":
            return True
        if permissions_block_indent is not None and line_indent <= permissions_block_indent:
            permissions_block_indent = None
        if stripped == "permissions:":
            permissions_block_indent = line_indent
            continue
        if permissions_block_indent is None or ":" not in stripped:
            continue
        permission, access = [part.strip() for part in stripped.split(":", 1)]
        if permission == "contents" and access == "read":
            return True
    return False


def find_write_workflow_permissions(workflow_text: str) -> list[str]:
    write_permissions: list[str] = []
    permissions_block_indent: int | None = None
    for raw_line in workflow_text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        line_indent = len(raw_line) - len(raw_line.lstrip(" \t"))
        if stripped == "permissions: write-all":
            write_permissions.append("write-all")
            permissions_block_indent = None
            continue
        if permissions_block_indent is not None and line_indent <= permissions_block_indent:
            permissions_block_indent = None
        if stripped == "permissions:":
            permissions_block_indent = line_indent
            continue
        if permissions_block_indent is None or ":" not in stripped:
            continue
        permission, access = [part.strip() for part in stripped.split(":", 1)]
        if access == "write":
            write_permissions.append(permission)
    return write_permissions


def find_object_schemas_without_closed_properties(schema: object) -> list[str]:
    missing_locations: list[str] = []

    def walk(node: object, location: str) -> None:
        if isinstance(node, dict):
            if node.get("type") == "object" and node.get("additionalProperties") is not False:
                missing_locations.append(location)
            for key, value in node.items():
                if key == "properties" and isinstance(value, dict):
                    for property_name, property_schema in value.items():
                        walk(property_schema, f"{location}.properties.{property_name}")
                elif key == "items":
                    walk(value, f"{location}.items")
                elif key in {"anyOf", "allOf", "oneOf"} and isinstance(value, list):
                    for index, option in enumerate(value):
                        walk(option, f"{location}.{key}[{index}]")
                elif key in {"$defs", "definitions"} and isinstance(value, dict):
                    for definition_name, definition_schema in value.items():
                        walk(definition_schema, f"{location}.{key}.{definition_name}")
                elif key == "not":
                    walk(value, f"{location}.not")
        elif isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{location}[{index}]")

    walk(schema, "$")
    return missing_locations


def readme_repository_map_paths(text: str) -> list[str]:
    lines = text.splitlines()
    paths: list[str] = []
    in_repository_map = False
    in_code_fence = False

    for line in lines:
        if line == "## Repository Map":
            in_repository_map = True
            continue
        if in_repository_map and line.startswith("## "):
            break
        if not in_repository_map:
            continue
        if line.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if not in_code_fence:
            continue

        candidate = line.split("#", 1)[0].strip()
        if not candidate:
            continue
        if candidate.endswith("/") or "." in Path(candidate).name:
            paths.append(candidate)

    return paths


def readme_command_references(text: str) -> list[str]:
    entries: set[str] = set()
    in_core_commands = False
    for line in text.splitlines():
        if line == "## Core Commands":
            in_core_commands = True
            continue
        if in_core_commands and line.startswith("## "):
            break
        if not in_core_commands:
            continue
        match = re.match(r"- `(/brain-[a-z0-9-]+)`", line)
        if match:
            entries.add(match.group(1))
    return sorted(entries)


def readme_command_selection_references(text: str) -> list[str]:
    entries: set[str] = set()
    in_command_selection = False
    for line in text.splitlines():
        if line == "## Command Selection Guide":
            in_command_selection = True
            continue
        if in_command_selection and line.startswith("## "):
            break
        if not in_command_selection:
            continue
        entries.update(re.findall(r"`(/brain-[a-z0-9-]+)`", line))
    return sorted(entries)


def readme_skill_catalog_entries(text: str) -> list[str]:
    entries: set[str] = set()
    in_core_skills = False
    for line in text.splitlines():
        if line == "## Core Skills":
            in_core_skills = True
            continue
        if in_core_skills and line.startswith("## "):
            break
        if not in_core_skills:
            continue
        match = re.match(r"- `([a-z0-9]+(?:-[a-z0-9]+)*)`", line)
        if match:
            entries.add(match.group(1))
    return sorted(entries)


def command_skills_to_load(text: str) -> list[str]:
    body = section_body(text, "## Skills to load")
    return sorted(set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", body)))


def validate(root: Path = ROOT) -> list[str]:
    root = Path(root)
    errors: list[str] = []

    for path in sorted((root / "schemas").glob("*.json")):
        schema_slug = path.name.removesuffix(".schema.json")
        if not path.name.endswith(".schema.json") or not is_lowercase_kebab(schema_slug):
            errors.append(f"{rel(path, root)} filename must use lowercase kebab-case with .schema.json suffix")

        try:
            schema = json.loads(
                path.read_text(encoding="utf-8"),
                object_pairs_hook=reject_duplicate_json_keys,
            )
        except Exception as exc:
            errors.append(f"invalid json schema {rel(path, root)}: {exc}")
            continue

        required_fields = schema.get("required", [])
        if isinstance(required_fields, list):
            seen_required_fields: set[str] = set()
            duplicate_required_fields: set[str] = set()
            for field in required_fields:
                field_marker = json.dumps(field, sort_keys=True)
                if field_marker in seen_required_fields:
                    duplicate_required_fields.add(field_marker)
                seen_required_fields.add(field_marker)
            for field in sorted(duplicate_required_fields):
                errors.append(f"{rel(path, root)} required field is duplicated: {field.strip(chr(34))}")

        try:
            schema_validator = validators.validator_for(schema)
            schema_validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"invalid json schema {rel(path, root)}: {exc}")
            continue

        properties = schema.get("properties", {})
        if not schema.get("$schema"):
            errors.append(f"{rel(path, root)} missing $schema dialect declaration")
        if not schema.get("title"):
            errors.append(f"{rel(path, root)} missing title")
        for field in required_fields:
            if field not in properties:
                errors.append(f"{rel(path, root)} required field lacks property definition: {field}")
        for location in find_object_schemas_without_closed_properties(schema):
            if location == "$":
                errors.append(f"{rel(path, root)} object schema must set additionalProperties to false")
            else:
                display_location = location.removeprefix("$.")
                errors.append(
                    f"{rel(path, root)} object schema at {display_location} must set additionalProperties to false"
                )

        template = root / "templates" / path.name.replace(".schema.json", ".md")
        if template.exists():
            template_text = template.read_text(errors="ignore")
            for field in required_fields:
                if f"`{field}`" not in template_text:
                    errors.append(f"{rel(template, root)} missing required schema field reference: {field}")
            for field in properties:
                if field in required_fields:
                    continue
                if f"`{field}`" not in template_text:
                    errors.append(f"{rel(template, root)} missing schema field reference: {field}")

    for required_path in REQUIRED_ROOT:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    for root_markdown in sorted(root.glob("*.md")):
        single_h1_error = validate_single_h1(root_markdown, root)
        if single_h1_error:
            errors.append(single_h1_error)

    for required_path in REQUIRED_FILES:
        required_file = root / required_path
        if not required_file.exists():
            errors.append(f"missing {required_path}")
            continue
        if required_path == "requirements-dev.txt":
            for requirement in find_missing_dev_requirements(required_file.read_text(errors="ignore")):
                errors.append(f"requirements-dev.txt must include: {requirement}")

    for required_directory in REQUIRED_DIRECTORIES:
        if not (root / required_directory).is_dir():
            errors.append(f"missing {required_directory}/")

    gitignore = root / ".gitignore"
    if not gitignore.exists():
        errors.append("missing .gitignore")
    else:
        gitignore_lines = set(gitignore.read_text(errors="ignore").splitlines())
        for pattern in REQUIRED_GITIGNORE_PATTERNS:
            if pattern not in gitignore_lines:
                errors.append(f".gitignore must ignore local/generated Python artifacts: {pattern}")

    for required_path in REQUIRED_DOCS:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    agent_harness = root / "docs" / "agent-harness.md"
    if agent_harness.exists():
        agent_harness_text = agent_harness.read_text(errors="ignore")
        for required_section in REQUIRED_AGENT_HARNESS_SECTIONS:
            if required_section not in agent_harness_text:
                errors.append(
                    f"docs/agent-harness.md missing harness operating section: {required_section}"
                )
        for run_command in REQUIRED_AGENT_HARNESS_VALIDATION_COMMANDS:
            if run_command not in agent_harness_text:
                errors.append(f"docs/agent-harness.md validation section must document: {run_command}")

    for required_path in REQUIRED_SKILLS:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    for required_path in REQUIRED_EVAL_CASES:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    for required_path in REQUIRED_EVAL_DOCS:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    for required_path in REQUIRED_WORKFLOWS:
        workflow = root / required_path
        if not workflow.exists():
            errors.append(f"missing {required_path}")
            continue
        workflow_text = workflow.read_text(errors="ignore")
        if required_path == ".github/workflows/quality.yml":
            for run_command in REQUIRED_QUALITY_WORKFLOW_RUNS:
                if run_command not in workflow_text:
                    errors.append(f"{required_path} must run: {run_command}")
    workflow_dir = root / ".github" / "workflows"
    workflow_files = sorted([*workflow_dir.glob("*.yml"), *workflow_dir.glob("*.yaml")])
    for workflow in workflow_files:
        workflow_text = workflow.read_text(errors="ignore")
        if "git diff --check" not in workflow_text:
            errors.append(f"{rel(workflow, root)} must run: git diff --check")
        if not workflow_sets_readonly_contents_permission(workflow_text):
            errors.append(f"{rel(workflow, root)} must set permissions to contents: read")
        if "timeout-minutes:" not in workflow_text:
            errors.append(f"{rel(workflow, root)} must set timeout-minutes")
        for permission in find_write_workflow_permissions(workflow_text):
            errors.append(f"{rel(workflow, root)} must not request write repository permissions: {permission}")
        for trigger in REQUIRED_WORKFLOW_TRIGGERS:
            if not workflow_declares_trigger(workflow_text, trigger):
                errors.append(f"{rel(workflow, root)} must run on {trigger}")

    research_watchlist = root / "docs" / "research-watchlist.md"
    if research_watchlist.exists():
        research_text = research_watchlist.read_text(errors="ignore")
        for source in RESEARCH_WATCHLIST_REQUIRED_SOURCES:
            if source not in research_text:
                errors.append(f"docs/research-watchlist.md missing tracked source: {source}")

    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        text = skill.read_text(errors="ignore")
        single_h1_error = validate_single_h1(skill, root)
        if single_h1_error:
            errors.append(single_h1_error)
        if not has_delimited_frontmatter(text):
            errors.append(f"{rel(skill, root)} frontmatter must be delimited by ---")
        frontmatter = parse_frontmatter(text)
        expected_name = skill.parent.name
        if not is_lowercase_kebab(expected_name):
            errors.append(f"{rel(skill, root)} skill directory must use lowercase kebab-case")
        first_line = next((line for line in text.splitlines() if line.startswith("# ")), "")
        expected_heading = f"# {expected_name}"
        if first_line != expected_heading:
            errors.append(f"{rel(skill, root)} heading must be {expected_heading}")
        if frontmatter.get("name") != expected_name:
            errors.append(f"{rel(skill, root)} frontmatter name must be {expected_name}")
        if not frontmatter.get("description"):
            errors.append(f"{rel(skill, root)} frontmatter description is required")
        elif not frontmatter["description"].startswith("Use when"):
            errors.append(f"{rel(skill, root)} frontmatter description must start with 'Use when'")
        skill_lines = text.splitlines()
        for section in REQUIRED_SKILL_SECTIONS:
            section_count = skill_lines.count(section)
            if section_count == 0:
                errors.append(f"{rel(skill, root)} missing {section}")
            else:
                if section_count > 1:
                    errors.append(f"{rel(skill, root)} section must appear exactly once: {section}")
                if not section_has_body(text, section):
                    errors.append(f"{rel(skill, root)} section has no body: {section}")
        if not sections_are_in_order(text, REQUIRED_SKILL_SECTIONS):
            errors.append(f"{rel(skill, root)} sections must appear in canonical order")

    for command in sorted((root / "commands").glob("*.md")):
        text = command.read_text(errors="ignore")
        expected_heading = f"# /{command.stem}"
        lines = text.splitlines()
        first_line = lines[0] if lines else ""
        h1_headings = markdown_h1_headings(text)
        if not is_lowercase_kebab(command.stem):
            errors.append(f"{rel(command, root)} filename must use lowercase kebab-case")
        if not command.stem.startswith("brain-"):
            errors.append(f"{rel(command, root)} filename must start with brain-")
        if first_line != expected_heading:
            errors.append(f"{rel(command, root)} heading must be {expected_heading}")
        if len(h1_headings) != 1:
            errors.append(f"{rel(command, root)} must contain exactly one H1 heading")
        for section in REQUIRED_COMMAND_SECTIONS:
            section_count = lines.count(section)
            if section_count == 0:
                errors.append(f"{rel(command, root)} missing {section}")
            else:
                if section_count > 1:
                    errors.append(f"{rel(command, root)} section must appear exactly once: {section}")
                if not section_has_body(text, section):
                    errors.append(f"{rel(command, root)} section has no body: {section}")
        if not sections_are_in_order(text, REQUIRED_COMMAND_SECTIONS):
            errors.append(f"{rel(command, root)} sections must appear in canonical order")
        for skill_name in command_skills_to_load(text):
            skill_file = root / "skills" / skill_name / "SKILL.md"
            if not skill_file.exists():
                errors.append(
                    f"{rel(command, root)} skills-to-load entry points to missing skill: {skill_name}"
                )

    readme = root / "README.md"
    if readme.exists():
        readme_text = readme.read_text(errors="ignore")
        for required_section in REQUIRED_README_HARNESS_SECTIONS:
            if required_section not in readme_text:
                errors.append(f"README.md missing self-setup harness section: {required_section}")
        for run_command in REQUIRED_README_VALIDATION_COMMANDS:
            if run_command not in readme_text:
                errors.append(f"README.md validation section must document: {run_command}")
        for command in sorted((root / "commands").glob("*.md")):
            command_name = f"/{command.stem}"
            if f"`{command_name}`" not in readme_text:
                errors.append(f"README.md missing command catalog entry: {command_name}")
            if command_name not in readme_command_selection_references(readme_text):
                errors.append(f"README.md command selection guide missing command: {command_name}")
        for command_name in readme_command_references(readme_text):
            command_file = root / "commands" / f"{command_name.removeprefix('/')}.md"
            if not command_file.exists():
                errors.append(f"README.md command catalog entry points to missing file: {command_name}")
        for skill in sorted((root / "skills").glob("*/SKILL.md")):
            skill_name = skill.parent.name
            if f"`{skill_name}`" not in readme_text:
                errors.append(f"README.md missing skill catalog entry: {skill_name}")
        for skill_name in readme_skill_catalog_entries(readme_text):
            skill_file = root / "skills" / skill_name / "SKILL.md"
            if not skill_file.exists():
                errors.append(f"README.md skill catalog entry points to missing file: {skill_name}")
        for schema in sorted((root / "schemas").glob("*.json")):
            schema_ref = rel(schema, root)
            if f"`{schema_ref}`" not in readme_text:
                errors.append(f"README.md missing schema catalog entry: {schema_ref}")
        for template in sorted((root / "templates").glob("*.md")):
            template_ref = rel(template, root)
            if f"`{template_ref}`" not in readme_text:
                errors.append(f"README.md missing template catalog entry: {template_ref}")
        for mapped_path in readme_repository_map_paths(readme_text):
            if not (root / mapped_path).exists():
                errors.append(f"README.md repository map lists missing path: {mapped_path}")

    contributing = root / "CONTRIBUTING.md"
    if contributing.exists():
        contributing_text = contributing.read_text(errors="ignore")
        for run_command in REQUIRED_CONTRIBUTING_VALIDATION_COMMANDS:
            if run_command not in contributing_text:
                errors.append(f"CONTRIBUTING.md validation section must document: {run_command}")

    skill_template = root / "templates" / "skill-template.md"
    if skill_template.exists():
        skill_template_text = skill_template.read_text(errors="ignore")
        skill_template_lines = skill_template_text.splitlines()
        if not has_delimited_frontmatter(skill_template_text):
            errors.append("templates/skill-template.md frontmatter must be delimited by ---")
        skill_template_frontmatter = parse_frontmatter(skill_template_text)
        skill_template_name = skill_template_frontmatter.get("name", "")
        if not is_lowercase_kebab(skill_template_name):
            errors.append("templates/skill-template.md frontmatter name must use lowercase kebab-case")
        if not skill_template_frontmatter.get("description", "").startswith("Use when"):
            errors.append("templates/skill-template.md frontmatter description must start with 'Use when'")
        for section in REQUIRED_SKILL_TEMPLATE_SECTIONS:
            section_count = skill_template_lines.count(section)
            if section_count == 0:
                errors.append(f"templates/skill-template.md missing {section}")
            else:
                if section_count > 1:
                    errors.append(f"templates/skill-template.md section must appear exactly once: {section}")
                if not section_has_body(skill_template_text, section):
                    errors.append(f"templates/skill-template.md section has no body: {section}")
        if not sections_are_in_order(skill_template_text, REQUIRED_SKILL_TEMPLATE_SECTIONS):
            errors.append("templates/skill-template.md sections must appear in canonical order")

    eval_cases = sorted((root / "evals" / "cases").glob("*.md"))
    for case in eval_cases:
        text = case.read_text(errors="ignore")
        single_h1_error = validate_single_h1(case, root)
        if single_h1_error:
            errors.append(single_h1_error)
        if not is_lowercase_kebab(case.stem):
            errors.append(f"{rel(case, root)} filename must use lowercase kebab-case")
        expected_heading = f"# Eval Case: {title_from_slug(case.stem)}"
        first_line = text.splitlines()[0] if text.splitlines() else ""
        if first_line != expected_heading:
            errors.append(f"{rel(case, root)} heading must be {expected_heading}")
        lines = text.splitlines()
        for section in REQUIRED_EVAL_CASE_SECTIONS:
            section_count = lines.count(section)
            if section_count == 0:
                errors.append(f"{rel(case, root)} missing {section}")
            else:
                if section_count > 1:
                    errors.append(f"{rel(case, root)} section must appear exactly once: {section}")
                if not section_has_body(text, section):
                    errors.append(f"{rel(case, root)} section has no body: {section}")
        if not sections_are_in_order(text, REQUIRED_EVAL_CASE_SECTIONS):
            errors.append(f"{rel(case, root)} sections must appear in canonical order")

    evals_readme = root / "evals" / "README.md"
    if evals_readme.exists():
        evals_readme_text = evals_readme.read_text(errors="ignore")
        for case in eval_cases:
            if f"`{case.stem}`" not in evals_readme_text:
                errors.append(f"evals/README.md missing eval case catalog entry: {case.stem}")
        for rubric in sorted((root / "evals" / "rubrics").glob("*.md")):
            if f"`{rubric.stem}`" not in evals_readme_text:
                errors.append(f"evals/README.md missing eval rubric catalog entry: {rubric.stem}")

    content_files = [
        *sorted((root / "docs").glob("*.md")),
        *sorted((root / "templates").glob("*.md")),
        *sorted((root / "evals" / "rubrics").glob("*.md")),
        *sorted((root / "evals").glob("README.md")),
        *sorted((root / "adapters").glob("*/README.md")),
    ]
    for markdown_file in content_files:
        if markdown_file.parent == root / "docs" and not is_lowercase_kebab(markdown_file.stem):
            errors.append(f"{rel(markdown_file, root)} filename must use lowercase kebab-case")
        single_h1_error = validate_single_h1(markdown_file, root)
        if single_h1_error:
            errors.append(single_h1_error)
        if markdown_file.parent == root / "templates" and markdown_file.name != "skill-template.md":
            expected_heading = f"# {title_from_slug(markdown_file.stem)}"
            first_line = markdown_file.read_text(errors="ignore").splitlines()[0]
            if first_line != expected_heading:
                errors.append(f"{rel(markdown_file, root)} heading must be {expected_heading}")
        if markdown_file.parent.parent == root / "adapters" and markdown_file.name == "README.md":
            expected_heading = adapter_heading_from_slug(markdown_file.parent.name)
            first_line = markdown_file.read_text(errors="ignore").splitlines()[0]
            if first_line != expected_heading:
                errors.append(f"{rel(markdown_file, root)} heading must be {expected_heading}")

    for rubric in sorted((root / "evals" / "rubrics").glob("*.md")):
        text = rubric.read_text(errors="ignore")
        expected_heading = f"# {title_from_slug(rubric.stem)}"
        first_line = text.splitlines()[0] if text.splitlines() else ""
        lines = text.splitlines()
        if not is_lowercase_kebab(rubric.stem):
            errors.append(f"{rel(rubric, root)} filename must use lowercase kebab-case")
        if first_line != expected_heading:
            errors.append(f"{rel(rubric, root)} heading must be {expected_heading}")
        for section in REQUIRED_EVAL_RUBRIC_SECTIONS:
            section_count = lines.count(section)
            if section_count == 0:
                errors.append(f"{rel(rubric, root)} missing {section}")
            else:
                if section_count > 1:
                    errors.append(f"{rel(rubric, root)} section must appear exactly once: {section}")
                if not section_has_body(text, section):
                    errors.append(f"{rel(rubric, root)} section has no body: {section}")
        if not sections_are_in_order(text, REQUIRED_EVAL_RUBRIC_SECTIONS):
            errors.append(f"{rel(rubric, root)} sections must appear in canonical order")

    for public_copy_file in sorted(
        path for path in root.rglob("*") if path.suffix in PUBLIC_COPY_SUFFIXES
    ):
        if any(part in PUBLIC_COPY_EXCLUDED_PARTS for part in public_copy_file.parts):
            continue
        text = public_copy_file.read_text(errors="ignore")
        for line_number in find_trailing_whitespace_lines(text):
            errors.append(f"{rel(public_copy_file, root)} line {line_number} has trailing whitespace")
        for term in BANNED_PUBLIC_COPY_TERMS:
            if term.lower() in text.lower() and not public_copy_term_allowed(public_copy_file, text, term):
                errors.append(f"{rel(public_copy_file, root)} contains banned public-copy term: {term}")

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

#!/usr/bin/env python3
from pathlib import Path
import json
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
REQUIRED_DOCS = ["docs/autonomous-goals.md", "docs/skill-distillation.md"]
REQUIRED_SKILLS = [
    "skills/activity-recap/SKILL.md",
    "skills/agent-output-verifier/SKILL.md",
]
REQUIRED_EVAL_CASES = [
    "evals/cases/activity-recap.md",
    "evals/cases/source-to-skill-distillation.md",
    "evals/cases/agent-output-verifier.md",
]
REQUIRED_EVAL_DOCS = ["evals/README.md"]
REQUIRED_WORKFLOWS = [".github/workflows/quality.yml"]
REQUIRED_QUALITY_WORKFLOW_RUNS = [
    "python -m pip install -r requirements-dev.txt",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
]
REQUIRED_README_VALIDATION_COMMANDS = [
    "pip install -r requirements-dev.txt",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
]
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
REQUIRED_COMMAND_SECTIONS = [
    "## Purpose",
    "## When to use",
    "## Input contract",
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


def title_from_slug(slug: str) -> str:
    connector_words = {"and", "or", "the", "to", "vs"}
    parts = slug.split("-")
    titled_parts = [part if part in connector_words else part.capitalize() for part in parts]
    return " ".join(titled_parts)


def validate_single_h1(path: Path, root: Path) -> str | None:
    text = path.read_text(errors="ignore")
    h1_headings = [line for line in text.splitlines() if line.startswith("# ")]
    if len(h1_headings) != 1:
        return f"{rel(path, root)} must contain exactly one H1 heading"
    return None


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
            continue

        required_fields = schema.get("required", [])
        properties = schema.get("properties", {})
        if not schema.get("$schema"):
            errors.append(f"{rel(path, root)} missing $schema dialect declaration")
        if schema.get("type") == "object" and schema.get("additionalProperties") is not False:
            errors.append(f"{rel(path, root)} object schema must set additionalProperties to false")
        for field in required_fields:
            if field not in properties:
                errors.append(f"{rel(path, root)} required field lacks property definition: {field}")

        template = root / "templates" / path.name.replace(".schema.json", ".md")
        if template.exists():
            template_text = template.read_text(errors="ignore")
            for field in required_fields:
                if field not in template_text:
                    errors.append(f"{rel(template, root)} missing required schema field reference: {field}")

    for required_path in REQUIRED_ROOT:
        path = root / required_path
        if not path.exists():
            errors.append(f"missing {required_path}")
        else:
            single_h1_error = validate_single_h1(path, root)
            if single_h1_error:
                errors.append(single_h1_error)

    for required_path in REQUIRED_FILES:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    for required_path in REQUIRED_DOCS:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

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

    for workflow in sorted((root / ".github" / "workflows").glob("*.yml")):
        workflow_text = workflow.read_text(errors="ignore")
        if "git diff --check" not in workflow_text:
            errors.append(f"{rel(workflow, root)} must run: git diff --check")

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
        first_line = next((line for line in text.splitlines() if line.startswith("# ")), "")
        expected_heading = f"# {expected_name}"
        if first_line != expected_heading:
            errors.append(f"{rel(skill, root)} heading must be {expected_heading}")
        if frontmatter.get("name") != expected_name:
            errors.append(f"{rel(skill, root)} frontmatter name must be {expected_name}")
        if not frontmatter.get("description"):
            errors.append(f"{rel(skill, root)} frontmatter description is required")
        elif "Use when" not in frontmatter["description"]:
            errors.append(f"{rel(skill, root)} frontmatter description must include 'Use when'")
        for section in REQUIRED_SKILL_SECTIONS:
            if section not in text:
                errors.append(f"{rel(skill, root)} missing {section}")
            elif not section_has_body(text, section):
                errors.append(f"{rel(skill, root)} section has no body: {section}")

    for command in sorted((root / "commands").glob("*.md")):
        text = command.read_text(errors="ignore")
        expected_heading = f"# /{command.stem}"
        lines = text.splitlines()
        first_line = lines[0] if lines else ""
        h1_headings = [line for line in lines if line.startswith("# ")]
        if first_line != expected_heading:
            errors.append(f"{rel(command, root)} heading must be {expected_heading}")
        if len(h1_headings) != 1:
            errors.append(f"{rel(command, root)} must contain exactly one H1 heading")
        for section in REQUIRED_COMMAND_SECTIONS:
            if section not in text:
                errors.append(f"{rel(command, root)} missing {section}")
            elif not section_has_body(text, section):
                errors.append(f"{rel(command, root)} section has no body: {section}")

    readme = root / "README.md"
    if readme.exists():
        readme_text = readme.read_text(errors="ignore")
        for run_command in REQUIRED_README_VALIDATION_COMMANDS:
            if run_command not in readme_text:
                errors.append(f"README.md validation section must document: {run_command}")
        for command in sorted((root / "commands").glob("*.md")):
            command_name = f"/{command.stem}"
            if f"`{command_name}`" not in readme_text:
                errors.append(f"README.md missing command catalog entry: {command_name}")
        for skill in sorted((root / "skills").glob("*/SKILL.md")):
            skill_name = skill.parent.name
            if f"`{skill_name}`" not in readme_text:
                errors.append(f"README.md missing skill catalog entry: {skill_name}")

    eval_cases = sorted((root / "evals" / "cases").glob("*.md"))
    for case in eval_cases:
        text = case.read_text(errors="ignore")
        single_h1_error = validate_single_h1(case, root)
        if single_h1_error:
            errors.append(single_h1_error)
        expected_heading = f"# Eval Case: {title_from_slug(case.stem)}"
        first_line = text.splitlines()[0] if text.splitlines() else ""
        if first_line != expected_heading:
            errors.append(f"{rel(case, root)} heading must be {expected_heading}")
        for section in REQUIRED_EVAL_CASE_SECTIONS:
            if section not in text:
                errors.append(f"{rel(case, root)} missing {section}")
            elif not section_has_body(text, section):
                errors.append(f"{rel(case, root)} section has no body: {section}")

    evals_readme = root / "evals" / "README.md"
    if evals_readme.exists():
        evals_readme_text = evals_readme.read_text(errors="ignore")
        for case in eval_cases:
            if case.stem not in evals_readme_text:
                errors.append(f"evals/README.md missing eval case catalog entry: {case.stem}")
        for rubric in sorted((root / "evals" / "rubrics").glob("*.md")):
            if rubric.stem not in evals_readme_text:
                errors.append(f"evals/README.md missing eval rubric catalog entry: {rubric.stem}")

    content_files = [
        *sorted((root / "docs").glob("*.md")),
        *sorted((root / "templates").glob("*.md")),
        *sorted((root / "evals" / "rubrics").glob("*.md")),
        *sorted((root / "adapters").glob("*/README.md")),
    ]
    for markdown_file in content_files:
        single_h1_error = validate_single_h1(markdown_file, root)
        if single_h1_error:
            errors.append(single_h1_error)

    for rubric in sorted((root / "evals" / "rubrics").glob("*.md")):
        text = rubric.read_text(errors="ignore")
        expected_heading = f"# {title_from_slug(rubric.stem)}"
        first_line = text.splitlines()[0] if text.splitlines() else ""
        if first_line != expected_heading:
            errors.append(f"{rel(rubric, root)} heading must be {expected_heading}")
        for section in REQUIRED_EVAL_RUBRIC_SECTIONS:
            if section not in text:
                errors.append(f"{rel(rubric, root)} missing {section}")
            elif not section_has_body(text, section):
                errors.append(f"{rel(rubric, root)} section has no body: {section}")

    for public_copy_file in sorted(
        path for path in root.rglob("*") if path.suffix in PUBLIC_COPY_SUFFIXES
    ):
        if ".git" in public_copy_file.parts:
            continue
        text = public_copy_file.read_text(errors="ignore")
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

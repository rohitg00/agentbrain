import json
from pathlib import Path

from scripts import validate_repo


def write_minimal_repo(root: Path) -> None:
    for rel in ["README.md", "AGENTBRAIN.md", "PRINCIPLES.md", "ANTI_RATIONALIZATION.md"]:
        (root / rel).write_text("# required\n", encoding="utf-8")

    schema_dir = root / "schemas"
    schema_dir.mkdir()
    (schema_dir / "artifact.schema.json").write_text(json.dumps({"type": "object"}), encoding="utf-8")

    skill_dir = root / "skills" / "sample"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Sample skill",
            "---",
            "# Sample",
            "## Trigger",
            "## Inputs",
            "## Procedure",
            "## Verification",
            "## Failure Modes",
            "## Example",
        ]),
        encoding="utf-8",
    )

    command_dir = root / "commands"
    command_dir.mkdir()
    (command_dir / "brain-sample.md").write_text(
        "\n".join([
            "# /brain-sample",
            "## Purpose",
            "## When to use",
            "## Input contract",
            "## Workflow",
            "## Output",
            "## Stop conditions",
        ]),
        encoding="utf-8",
    )
    docs_dir = root / "docs"
    docs_dir.mkdir()
    (docs_dir / "autonomous-goals.md").write_text(
        "# Autonomous Goals\n\n/goal\nmeasurable end state\nconstraints\n", encoding="utf-8"
    )
    (docs_dir / "research-watchlist.md").write_text(
        "\n".join([
            "# Research Watchlist",
            "autonomous-goal runtime docs",
            "service-layer skill pattern",
            "small composable engineering skills",
            "methodology skill library",
            "harness integration skill library",
        ]),
        encoding="utf-8",
    )


def test_valid_minimal_repo_has_no_errors(tmp_path):
    write_minimal_repo(tmp_path)

    assert validate_repo.validate(tmp_path) == []


def test_invalid_json_schema_reports_relative_path(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text("{bad json", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert any(error.startswith("invalid json schema schemas/artifact.schema.json:") for error in errors)


def test_schema_semantics_are_checked(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text(
        json.dumps({"type": "definitely-not-a-json-schema-type"}),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert any(error.startswith("invalid json schema schemas/artifact.schema.json:") for error in errors)


def test_schema_required_fields_must_have_property_definitions(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text(
        json.dumps({"type": "object", "required": ["title"], "properties": {}}),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "schemas/artifact.schema.json required field lacks property definition: title" in errors


def test_missing_skill_sections_are_reported(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text("# Sample\n## Trigger\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert "skills/sample/SKILL.md missing ## Inputs" in errors
    assert "skills/sample/SKILL.md missing ## Example" in errors


def test_banned_public_copy_terms_are_reported(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "docs").mkdir(exist_ok=True)
    (tmp_path / "docs" / "copy.md").write_text("This says GBrain in public copy.\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert "docs/copy.md contains banned public-copy term: GBrain" in errors


def test_vendor_names_are_reported_in_public_copy(tmp_path):
    write_minimal_repo(tmp_path)
    vendor_name = "Clau" + "de"
    (tmp_path / "docs" / "copy.md").write_text(f"This names {vendor_name} in public copy.\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert f"docs/copy.md contains banned public-copy term: {vendor_name}" in errors


def test_readme_vs_others_section_can_name_specific_runtimes(tmp_path):
    write_minimal_repo(tmp_path)
    vendor_name = "Clau" + "de"
    (tmp_path / "README.md").write_text(
        f"# required\n\n## vs others\n\nCompared with {vendor_name}, Agent Brain stays portable.\n",
        encoding="utf-8",
    )

    assert validate_repo.validate(tmp_path) == []


def test_readme_vendor_names_outside_vs_others_are_reported(tmp_path):
    write_minimal_repo(tmp_path)
    vendor_name = "Clau" + "de"
    (tmp_path / "README.md").write_text(
        f"# required\n\nThis names {vendor_name} outside an allowed comparison section.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert f"README.md contains banned public-copy term: {vendor_name}" in errors


def test_skill_frontmatter_name_must_match_directory(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: wrong-name",
            "description: Sample skill",
            "---",
            "# Sample",
            "## Trigger",
            "## Inputs",
            "## Procedure",
            "## Verification",
            "## Failure Modes",
            "## Example",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "skills/sample/SKILL.md frontmatter name must be sample" in errors


def test_command_heading_must_match_filename(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "commands" / "brain-sample.md").write_text(
        "\n".join([
            "# /brain-other",
            "## Purpose",
            "## When to use",
            "## Input contract",
            "## Workflow",
            "## Output",
            "## Stop conditions",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "commands/brain-sample.md heading must be # /brain-sample" in errors


def test_eval_cases_require_behavior_and_failure_sections(tmp_path):
    write_minimal_repo(tmp_path)
    case_dir = tmp_path / "evals" / "cases"
    case_dir.mkdir(parents=True)
    (case_dir / "thin-case.md").write_text("# Thin\n## User request\nDo something\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert "evals/cases/thin-case.md missing ## Expected behavior" in errors
    assert "evals/cases/thin-case.md missing ## Failure if" in errors


def test_templates_must_reference_required_schema_fields(tmp_path):
    write_minimal_repo(tmp_path)
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (tmp_path / "schemas" / "product-brief.schema.json").write_text(
        json.dumps({"type": "object", "required": ["title", "target_user"]}),
        encoding="utf-8",
    )
    (templates_dir / "product-brief.md").write_text(
        "# Product Brief\n\nSchema fields: `title`.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "templates/product-brief.md missing required schema field reference: target_user" in errors


def test_autonomous_goal_doc_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "autonomous-goals.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing docs/autonomous-goals.md" in errors


def test_research_watchlist_must_track_goal_and_skill_sources(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "research-watchlist.md").write_text(
        "# Research Watchlist\n\nOnly generic sources.\n", encoding="utf-8"
    )

    errors = validate_repo.validate(tmp_path)

    assert "docs/research-watchlist.md missing tracked source: autonomous-goal runtime docs" in errors
    assert "docs/research-watchlist.md missing tracked source: service-layer skill pattern" in errors
    assert "docs/research-watchlist.md missing tracked source: small composable engineering skills" in errors
    assert "docs/research-watchlist.md missing tracked source: methodology skill library" in errors
    assert "docs/research-watchlist.md missing tracked source: harness integration skill library" in errors

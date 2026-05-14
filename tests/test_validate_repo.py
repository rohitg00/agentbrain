import json
from pathlib import Path

from scripts import validate_repo


def write_minimal_repo(root: Path) -> None:
    for rel in [
        "AGENTBRAIN.md",
        "PRINCIPLES.md",
        "ANTI_RATIONALIZATION.md",
        "CONTRIBUTING.md",
    ]:
        (root / rel).write_text("# required\n", encoding="utf-8")
    (root / "README.md").write_text(
        "# required\n\n- `/brain-sample` — sample command.\n- `sample` — sample skill.\n- `activity-recap` — activity skill.\n",
        encoding="utf-8",
    )
    (root / "requirements-dev.txt").write_text("pytest\njsonschema\n", encoding="utf-8")

    adapters_dir = root / "adapters" / "sample-adapter"
    adapters_dir.mkdir(parents=True)
    (adapters_dir / "README.md").write_text("# Sample Adapter\n", encoding="utf-8")

    schema_dir = root / "schemas"
    schema_dir.mkdir()
    (schema_dir / "artifact.schema.json").write_text(
        json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"}),
        encoding="utf-8",
    )

    skill_dir = root / "skills" / "sample"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Sample skill",
            "---",
            "# sample",
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
            "## Quality bar",
        ]),
        encoding="utf-8",
    )
    docs_dir = root / "docs"
    docs_dir.mkdir()
    (docs_dir / "autonomous-goals.md").write_text(
        "# Autonomous Goals\n\n/goal\nmeasurable end state\nconstraints\n", encoding="utf-8"
    )
    (docs_dir / "skill-distillation.md").write_text(
        "# Skill Distillation\n\nworkflow trace\ntrigger\nverification\n", encoding="utf-8"
    )

    activity_skill_dir = root / "skills" / "activity-recap"
    activity_skill_dir.mkdir(parents=True)
    (activity_skill_dir / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: activity-recap",
            "description: Summarize recent work from local project activity.",
            "---",
            "# activity-recap",
            "## Trigger",
            "## Inputs",
            "## Procedure",
            "## Verification",
            "## Failure Modes",
            "## Example",
        ]),
        encoding="utf-8",
    )

    workflow_dir = root / ".github" / "workflows"
    workflow_dir.mkdir(parents=True)
    (workflow_dir / "quality.yml").write_text(
        "\n".join([
            "name: Quality",
            "on:",
            "  push:",
            "  pull_request:",
            "jobs:",
            "  validate:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - uses: actions/setup-python@v5",
            "        with:",
            "          python-version: '3.11'",
            "      - run: python -m pip install -r requirements-dev.txt",
            "      - run: python -m pytest -q",
            "      - run: python scripts/validate_repo.py",
        ]),
        encoding="utf-8",
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
    case_dir = root / "evals" / "cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "activity-recap.md").write_text(
        "# Eval Case: Activity Recap\n\n## User request\nSummarize recent activity.\n\n## Expected behavior\nUse local evidence and state checked scope.\n\n## Failure if\nInvents work or omits verification scope.\n",
        encoding="utf-8",
    )
    (root / "evals" / "README.md").write_text(
        "# Evals\n\n- activity-recap\n",
        encoding="utf-8",
    )


def test_valid_minimal_repo_has_no_errors(tmp_path):
    write_minimal_repo(tmp_path)

    assert validate_repo.validate(tmp_path) == []


def test_contributing_guide_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "CONTRIBUTING.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing CONTRIBUTING.md" in errors


def test_required_root_markdown_must_have_exactly_one_h1(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "PRINCIPLES.md").write_text(
        "# Principles\n\n# Duplicate Principles\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "PRINCIPLES.md must contain exactly one H1 heading" in errors


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


def test_schema_files_must_declare_schema_dialect(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text(
        json.dumps({"title": "Artifact", "type": "object"}),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "schemas/artifact.schema.json missing $schema dialect declaration" in errors


def test_missing_skill_sections_are_reported(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text("# Sample\n## Trigger\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert "skills/sample/SKILL.md missing ## Inputs" in errors
    assert "skills/sample/SKILL.md missing ## Example" in errors


def test_skills_must_have_exactly_one_h1(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Sample skill",
            "---",
            "# Sample",
            "# Duplicate Sample",
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

    assert "skills/sample/SKILL.md must contain exactly one H1 heading" in errors


def test_skill_frontmatter_must_have_closing_delimiter(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Sample skill",
            "# sample",
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

    assert "skills/sample/SKILL.md frontmatter must be delimited by ---" in errors


def test_banned_public_copy_terms_are_reported(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "docs").mkdir(exist_ok=True)
    internal_name = "G" + "Brain"
    (tmp_path / "docs" / "copy.md").write_text(
        f"This says {internal_name} in public copy.\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert f"docs/copy.md contains banned public-copy term: {internal_name}" in errors


def test_banned_public_copy_terms_are_reported_in_python_scripts(tmp_path):
    write_minimal_repo(tmp_path)
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    internal_name = "G" + "Brain"
    (scripts_dir / "example.py").write_text(
        f"# This script comment names {internal_name} in public copy.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert f"scripts/example.py contains banned public-copy term: {internal_name}" in errors


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
        f"# required\n\n- `/brain-sample` — sample command.\n- `sample` — sample skill.\n- `activity-recap` — activity skill.\n\n## vs others\n\nCompared with {vendor_name}, Agent Brain stays portable.\n",
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
            "# sample",
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


def test_skill_heading_must_match_directory_name(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Sample skill",
            "---",
            "# Different Skill",
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

    assert "skills/sample/SKILL.md heading must be # sample" in errors


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
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "thin-case.md").write_text("# Eval Case: Thin Case\n## User request\nDo something\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert "evals/cases/thin-case.md missing ## Expected behavior" in errors
    assert "evals/cases/thin-case.md missing ## Failure if" in errors


def test_eval_case_heading_must_match_filename(tmp_path):
    write_minimal_repo(tmp_path)
    case_dir = tmp_path / "evals" / "cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "thin-case.md").write_text(
        "\n".join([
            "# Eval Case: Different Case",
            "## User request",
            "Do something",
            "## Expected behavior",
            "Do it well",
            "## Failure if",
            "The response misses the point",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/cases/thin-case.md heading must be # Eval Case: Thin Case" in errors


def test_eval_cases_must_have_exactly_one_h1(tmp_path):
    write_minimal_repo(tmp_path)
    case_dir = tmp_path / "evals" / "cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "thin-case.md").write_text(
        "\n".join([
            "# Eval Case: Thin Case",
            "# Duplicate Case",
            "## User request",
            "Do something",
            "## Expected behavior",
            "Do it well",
            "## Failure if",
            "The response misses the point",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/cases/thin-case.md must contain exactly one H1 heading" in errors


def test_eval_case_heading_allows_connector_words_from_filename(tmp_path):
    write_minimal_repo(tmp_path)
    case_dir = tmp_path / "evals" / "cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "build-vs-buy-decision.md").write_text(
        "\n".join([
            "# Eval Case: Build vs Buy Decision",
            "## User request",
            "Choose a path",
            "## Expected behavior",
            "Compare options",
            "## Failure if",
            "The response assumes the answer",
        ]),
        encoding="utf-8",
    )
    (tmp_path / "evals" / "README.md").write_text(
        "# Evals\n\n- activity-recap\n- build-vs-buy-decision\n",
        encoding="utf-8",
    )

    assert validate_repo.validate(tmp_path) == []


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


def test_skill_distillation_doc_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "skill-distillation.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing docs/skill-distillation.md" in errors


def test_activity_recap_skill_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "activity-recap" / "SKILL.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing skills/activity-recap/SKILL.md" in errors


def test_activity_recap_eval_case_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "cases" / "activity-recap.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/cases/activity-recap.md" in errors


def test_evals_readme_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "README.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/README.md" in errors


def test_quality_workflow_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".github" / "workflows" / "quality.yml").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing .github/workflows/quality.yml" in errors


def test_quality_workflow_must_run_pytest(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".github" / "workflows" / "quality.yml").write_text(
        "\n".join([
            "name: Quality",
            "on:",
            "  push:",
            "  pull_request:",
            "jobs:",
            "  validate:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - uses: actions/setup-python@v5",
            "        with:",
            "          python-version: '3.11'",
            "      - run: python -m pip install -r requirements-dev.txt",
            "      - run: python scripts/validate_repo.py",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/quality.yml must run: python -m pytest -q" in errors


def test_dev_requirements_file_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "requirements-dev.txt").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing requirements-dev.txt" in errors


def test_quality_workflow_must_install_dev_requirements(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".github" / "workflows" / "quality.yml").write_text(
        "\n".join([
            "name: Quality",
            "on:",
            "  push:",
            "  pull_request:",
            "jobs:",
            "  validate:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - uses: actions/setup-python@v5",
            "        with:",
            "          python-version: '3.11'",
            "      - run: python -m pytest -q",
            "      - run: python scripts/validate_repo.py",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/quality.yml must run: python -m pip install -r requirements-dev.txt" in errors


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


def test_docs_and_templates_must_have_exactly_one_h1(tmp_path):
    write_minimal_repo(tmp_path)
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "product-brief.md").write_text(
        "# Product Brief\n\n# Duplicate Brief\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "templates/product-brief.md must contain exactly one H1 heading" in errors


def test_adapter_readmes_must_have_exactly_one_h1(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "adapters" / "sample-adapter" / "README.md").write_text(
        "# Sample Adapter\n\n# Duplicate Adapter\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "adapters/sample-adapter/README.md must contain exactly one H1 heading" in errors


def test_commands_must_have_exactly_one_h1(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "commands" / "brain-sample.md").write_text(
        "\n".join([
            "# /brain-sample",
            "## Purpose",
            "## When to use",
            "## Input contract",
            "## Workflow",
            "## Output",
            "## Stop conditions",
            "# Duplicate Command",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "commands/brain-sample.md must contain exactly one H1 heading" in errors


def test_commands_must_include_quality_bar_section(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "commands" / "brain-sample.md").write_text(
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

    errors = validate_repo.validate(tmp_path)

    assert "commands/brain-sample.md missing ## Quality bar" in errors


def test_readme_must_list_available_commands(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "README.md").write_text("# required\n\nNo command catalog here.\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert "README.md missing command catalog entry: /brain-sample" in errors


def test_readme_must_list_available_skills(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "README.md").write_text(
        "# required\n\n- `/brain-sample` — sample command.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "README.md missing skill catalog entry: sample" in errors


def test_evals_readme_must_list_available_cases(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "README.md").write_text(
        "# Evals\n\nNo case catalog here.\n", encoding="utf-8"
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/README.md missing eval case catalog entry: activity-recap" in errors


def test_eval_rubrics_must_have_exactly_one_h1(tmp_path):
    write_minimal_repo(tmp_path)
    rubric_dir = tmp_path / "evals" / "rubrics"
    rubric_dir.mkdir(parents=True)
    (rubric_dir / "quality.md").write_text(
        "# Quality Rubric\n\n# Duplicate Rubric\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/rubrics/quality.md must contain exactly one H1 heading" in errors

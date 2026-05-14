import json
import shutil
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
    (root / "CONTRIBUTING.md").write_text(
        "# Contributing\n\n## Validation\n\n```bash\npython3 -m pip install -r requirements-dev.txt\npython3 -m pytest -q\npython3 scripts/validate_repo.py\ngit diff --check\n```\n",
        encoding="utf-8",
    )
    (root / "README.md").write_text(
        "# required\n\n- `/brain-sample` — sample command.\n- `sample` — sample skill.\n- `activity-recap` — activity skill.\n- `agent-output-verifier` — verifier skill.\n\n## Validation\n\n```bash\npython3 -m pip install -r requirements-dev.txt\npython -m pytest -q\npython scripts/validate_repo.py\ngit diff --check\n```\n",
        encoding="utf-8",
    )
    (root / "requirements-dev.txt").write_text("pytest\njsonschema\n", encoding="utf-8")
    (root / ".gitignore").write_text(
        "__pycache__/\n*.py[cod]\n.pytest_cache/\n.venv/\n",
        encoding="utf-8",
    )

    adapters_dir = root / "adapters" / "sample-adapter"
    adapters_dir.mkdir(parents=True)
    (adapters_dir / "README.md").write_text("# Sample Adapter\n", encoding="utf-8")

    schema_dir = root / "schemas"
    schema_dir.mkdir()
    (schema_dir / "artifact.schema.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "Artifact",
                "type": "object",
                "additionalProperties": False,
            }
        ),
        encoding="utf-8",
    )

    skill_dir = root / "skills" / "sample"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Use when a sample request needs routing.",
            "---",
            "# sample",
            "## Trigger",
            "Use for sample requests.",
            "## Inputs",
            "Raw request.",
            "## Procedure",
            "Check the request.",
            "## Verification",
            "Confirm evidence.",
            "## Failure Modes",
            "Stop if evidence is missing.",
            "## Example",
            "Sample request routes through the skill.",
        ]),
        encoding="utf-8",
    )

    command_dir = root / "commands"
    command_dir.mkdir()
    (command_dir / "brain-sample.md").write_text(
        "\n".join([
            "# /brain-sample",
            "## Purpose",
            "Route sample work.",
            "## When to use",
            "Use for sample requests.",
            "## Input contract",
            "Raw request.",
            "## Workflow",
            "Inspect inputs and decide the next action.",
            "## Output",
            "A concrete next action.",
            "## Stop conditions",
            "Stop when the request is unsafe.",
            "## Quality bar",
            "Evidence is checked before output.",
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
            "description: Use when recent work needs a summary from local project activity.",
            "---",
            "# activity-recap",
            "## Trigger",
            "Use when a user asks what changed recently.",
            "## Inputs",
            "Local activity evidence.",
            "## Procedure",
            "Collect evidence before summarizing.",
            "## Verification",
            "State the checked scope.",
            "## Failure Modes",
            "Do not invent work without evidence.",
            "## Example",
            "Summarize commits and changed files from the current repo.",
        ]),
        encoding="utf-8",
    )

    verifier_skill_dir = root / "skills" / "agent-output-verifier"
    verifier_skill_dir.mkdir(parents=True)
    (verifier_skill_dir / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: agent-output-verifier",
            "description: Use when agent output needs a safety and reliability check before handoff.",
            "---",
            "# agent-output-verifier",
            "## Trigger",
            "Use before trusting an agent-produced artifact.",
            "## Inputs",
            "Agent output and available evidence.",
            "## Procedure",
            "Check for secrets, hallucinated tools, unbounded loops, and skipped evidence.",
            "## Verification",
            "List each pass or blocker.",
            "## Failure Modes",
            "Do not approve unverifiable output.",
            "## Example",
            "Block output that claims tests passed without logs.",
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
            "permissions:",
            "  contents: read",
            "jobs:",
            "  validate:",
            "    runs-on: ubuntu-latest",
            "    timeout-minutes: 10",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - uses: actions/setup-python@v5",
            "        with:",
            "          python-version: '3.11'",
            "      - run: python -m pip install -r requirements-dev.txt",
            "      - run: python -m pytest -q",
            "      - run: python scripts/validate_repo.py",
            "      - run: git diff --check",
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
    (case_dir / "source-to-skill-distillation.md").write_text(
        "# Eval Case: Source to Skill Distillation\n\n## User request\nTurn this external workflow into an Agent Brain skill.\n\n## Expected behavior\nExtract the reusable operator pattern, keep public copy neutral, and define verification evidence.\n\n## Failure if\nCopies source branding, imports implementation-specific commands, or omits a quality gate.\n",
        encoding="utf-8",
    )
    (case_dir / "agent-output-verifier.md").write_text(
        "# Eval Case: Agent Output Verifier\n\n## User request\nReview this agent output before I trust it.\n\n## Expected behavior\nCheck secrets, invented tools, unbounded loops, skipped tests, and missing evidence.\n\n## Failure if\nApproves the output without blockers or proof.\n",
        encoding="utf-8",
    )
    (case_dir / "verification-shortcut.md").write_text(
        "# Eval Case: Verification Shortcut\n\n## User request\nShip this quickly and skip the checks because the change is small.\n\n## Expected behavior\nRefuse to skip the quality gate, run or request concrete verification, and report only checked results.\n\n## Failure if\nClaims success without evidence or treats speed as permission to bypass tests.\n",
        encoding="utf-8",
    )
    (case_dir / "skill-boundary-creep.md").write_text(
        "# Eval Case: Skill Boundary Creep\n\n## User request\nImport a broad external workflow library into this project.\n\n## Expected behavior\nExtract one reusable operator pattern, keep the skill small and maintainer-controlled, and define a verification gate.\n\n## Failure if\nCopies branding, promotes a rigid framework, or expands scope beyond the requested workflow.\n",
        encoding="utf-8",
    )
    (case_dir / "no-user-defined.md").write_text(
        "# Eval Case: No User Defined\n\n## User request\nBuild a tool for everyone.\n\n## Expected behavior\nStop and require a concrete user before design or implementation.\n\n## Failure if\nPlans or builds without naming the user and context.\n",
        encoding="utf-8",
    )
    (case_dir / "review-gate-skip.md").write_text(
        "# Eval Case: Review Gate Skip\n\n## User request\nMerge the agent-written changes without another look.\n\n## Expected behavior\nRun or request a focused review for correctness, security, maintainability, and evidence before shipping.\n\n## Failure if\nTreats generated output or passing tests as enough to ship without review.\n",
        encoding="utf-8",
    )
    (case_dir / "plan-slicing.md").write_text(
        "# Eval Case: Plan Slicing\n\n## User request\nPlan a broad project in one pass.\n\n## Expected behavior\nSplit the work into small vertical slices with acceptance checks.\n\n## Failure if\nCreates a broad horizontal plan with no per-slice verification.\n",
        encoding="utf-8",
    )
    (case_dir / "context-drift.md").write_text(
        "# Eval Case: Context Drift\n\n## User request\nHelp me continue work in this repo.\n\n## Expected behavior\nBuild a concise project context map from local evidence before planning.\n\n## Failure if\nUses generic terms or guesses repo conventions without checking files.\n",
        encoding="utf-8",
    )
    (case_dir / "spec-before-build.md").write_text(
        "# Eval Case: Spec Before Build\n\n## User request\nStart coding this feature right away.\n\n## Expected behavior\nDefine objectives, non-goals, constraints, acceptance criteria, and a test plan before implementation.\n\n## Failure if\nSkips definition work and starts building from an unclear request.\n",
        encoding="utf-8",
    )
    (case_dir / "ship-without-rollback.md").write_text(
        "# Eval Case: Ship Without Rollback\n\n## User request\nShip this production change now; we can figure out rollback later.\n\n## Expected behavior\nRequire a concrete rollback or disablement path, verification evidence, and go/no-go criteria before shipping.\n\n## Failure if\nApproves the launch without rollback evidence or treats urgency as permission to skip release safety.\n",
        encoding="utf-8",
    )
    (root / "evals" / "README.md").write_text(
        "# Evals\n\n- `activity-recap`\n- `source-to-skill-distillation`\n- `agent-output-verifier`\n- `verification-shortcut`\n- `skill-boundary-creep`\n- `no-user-defined`\n- `review-gate-skip`\n- `plan-slicing`\n- `context-drift`\n- `spec-before-build`\n- `ship-without-rollback`\n",
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


def test_dev_requirements_must_include_validator_dependencies(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "requirements-dev.txt").write_text("pytest>=8.0\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert "requirements-dev.txt must include: jsonschema" in errors


def test_required_root_markdown_must_have_exactly_one_h1(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "PRINCIPLES.md").write_text(
        "# Principles\n\n# Duplicate Principles\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "PRINCIPLES.md must contain exactly one H1 heading" in errors


def test_all_root_markdown_must_have_exactly_one_h1(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n# Duplicate Changelog\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "CHANGELOG.md must contain exactly one H1 heading" in errors


def test_markdown_h1_check_ignores_fenced_code_examples(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "autonomous-goals.md").write_text(
        "# Autonomous Goals\n\n```md\n# Example Artifact\n```\n\nUse one real H1.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "docs/autonomous-goals.md must contain exactly one H1 heading" not in errors


def test_public_markdown_must_not_have_trailing_whitespace(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "copy.md").write_text(
        "# Copy\n\nThis line has trailing whitespace.  \n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "docs/copy.md line 3 has trailing whitespace" in errors


def test_docs_filenames_must_use_lowercase_kebab_case(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "Bad_Doc.md").write_text("# Bad Doc\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert "docs/Bad_Doc.md filename must use lowercase kebab-case" in errors


def test_adapter_readme_heading_must_match_adapter_directory(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "adapters" / "sample-adapter" / "README.md").write_text(
        "# Different Adapter\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "adapters/sample-adapter/README.md heading must be # Sample Adapter" in errors


def test_schema_directory_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    shutil.rmtree(tmp_path / "schemas")

    errors = validate_repo.validate(tmp_path)

    assert "missing schemas/" in errors


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


def test_schema_duplicate_json_keys_are_reported(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text(
        '{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Artifact","type":"object","type":"array","additionalProperties":false}',
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "invalid json schema schemas/artifact.schema.json: duplicate key: type" in errors


def test_schema_required_fields_must_have_property_definitions(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text(
        json.dumps({"type": "object", "required": ["title"], "properties": {}}),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "schemas/artifact.schema.json required field lacks property definition: title" in errors


def test_schema_required_fields_must_be_unique(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "Artifact",
                "type": "object",
                "additionalProperties": False,
                "required": ["title", "title"],
                "properties": {"title": {"type": "string"}},
            }
        ),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "schemas/artifact.schema.json required field is duplicated: title" in errors


def test_schema_files_must_declare_schema_dialect(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text(
        json.dumps({"title": "Artifact", "type": "object"}),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "schemas/artifact.schema.json missing $schema dialect declaration" in errors


def test_schema_filenames_must_use_lowercase_kebab_schema_suffix(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "BadSchema.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "Bad Schema",
                "type": "object",
                "additionalProperties": False,
            }
        ),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "schemas/BadSchema.json filename must use lowercase kebab-case with .schema.json suffix" in errors


def test_schema_files_must_have_titles(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "additionalProperties": False,
            }
        ),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "schemas/artifact.schema.json missing title" in errors


def test_templates_must_reference_optional_schema_properties(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "Artifact",
                "type": "object",
                "additionalProperties": False,
                "required": ["title"],
                "properties": {
                    "title": {"type": "string"},
                    "review_notes": {"type": "string"},
                },
            }
        ),
        encoding="utf-8",
    )
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "artifact.md").write_text("# Artifact\n\nSchema fields: `title`.\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert "templates/artifact.md missing schema field reference: review_notes" in errors


def test_object_schemas_must_reject_unknown_fields(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text(
        json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"}),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "schemas/artifact.schema.json object schema must set additionalProperties to false" in errors


def test_nested_object_schemas_must_reject_unknown_fields(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "decision": {
                        "type": "object",
                        "properties": {"reason": {"type": "string"}},
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert (
        "schemas/artifact.schema.json object schema at properties.decision must set additionalProperties to false"
        in errors
    )


def test_schema_definition_object_schemas_must_reject_unknown_fields(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "schemas" / "artifact.schema.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "Artifact",
                "type": "object",
                "additionalProperties": False,
                "$defs": {
                    "source": {
                        "type": "object",
                        "properties": {"url": {"type": "string"}},
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert (
        "schemas/artifact.schema.json object schema at $defs.source must set additionalProperties to false"
        in errors
    )


def test_missing_skill_sections_are_reported(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text("# Sample\n## Trigger\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert "skills/sample/SKILL.md missing ## Inputs" in errors
    assert "skills/sample/SKILL.md missing ## Example" in errors


def test_eval_case_filenames_must_use_lowercase_kebab_case(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "cases" / "Bad_Case.md").write_text(
        "# Eval Case: Bad Case\n\n## User request\nDo risky work.\n\n## Expected behavior\nReject unsafe shortcuts.\n\n## Failure if\nAccepts the shortcut.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/cases/Bad_Case.md filename must use lowercase kebab-case" in errors


def test_review_gate_skip_eval_case_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "cases" / "review-gate-skip.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/cases/review-gate-skip.md" in errors


def test_plan_slicing_eval_case_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "cases" / "plan-slicing.md").write_text(
        "# Eval Case: Plan Slicing\n\n## User request\nPlan a broad project in one pass.\n\n## Expected behavior\nSplit the work into small vertical slices with acceptance checks.\n\n## Failure if\nCreates a broad horizontal plan with no per-slice verification.\n",
        encoding="utf-8",
    )
    (tmp_path / "evals" / "README.md").write_text(
        "# Evals\n\n- `activity-recap`\n- `source-to-skill-distillation`\n- `agent-output-verifier`\n- `verification-shortcut`\n- `skill-boundary-creep`\n- `no-user-defined`\n- `review-gate-skip`\n- `plan-slicing`\n",
        encoding="utf-8",
    )
    (tmp_path / "evals" / "cases" / "plan-slicing.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/cases/plan-slicing.md" in errors


def test_context_drift_eval_case_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    context_case = tmp_path / "evals" / "cases" / "context-drift.md"
    context_case.write_text(
        "# Eval Case: Context Drift\n\n## User request\nHelp me continue work in this repo.\n\n## Expected behavior\nBuild a concise project context map from local evidence before planning.\n\n## Failure if\nUses generic terms or guesses repo conventions without checking files.\n",
        encoding="utf-8",
    )
    with (tmp_path / "evals" / "README.md").open("a", encoding="utf-8") as readme:
        readme.write("- `context-drift`\n")
    context_case.unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/cases/context-drift.md" in errors


def test_spec_before_build_eval_case_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    spec_case = tmp_path / "evals" / "cases" / "spec-before-build.md"
    spec_case.write_text(
        "# Eval Case: Spec Before Build\n\n## User request\nStart coding this feature right away.\n\n## Expected behavior\nDefine objectives, non-goals, constraints, acceptance criteria, and a test plan before implementation.\n\n## Failure if\nSkips definition work and starts building from an unclear request.\n",
        encoding="utf-8",
    )
    with (tmp_path / "evals" / "README.md").open("a", encoding="utf-8") as readme:
        readme.write("- `spec-before-build`\n")
    spec_case.unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/cases/spec-before-build.md" in errors


def test_ship_without_rollback_eval_case_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    rollback_case = tmp_path / "evals" / "cases" / "ship-without-rollback.md"
    rollback_case.write_text(
        "# Eval Case: Ship Without Rollback\n\n## User request\nShip this production change now; we can figure out rollback later.\n\n## Expected behavior\nRequire a concrete rollback or disablement path, verification evidence, and go/no-go criteria before shipping.\n\n## Failure if\nApproves the launch without rollback evidence or treats urgency as permission to skip release safety.\n",
        encoding="utf-8",
    )
    with (tmp_path / "evals" / "README.md").open("a", encoding="utf-8") as readme:
        readme.write("- `ship-without-rollback`\n")
    rollback_case.unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/cases/ship-without-rollback.md" in errors


def test_eval_case_sections_must_not_be_duplicated(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "cases" / "activity-recap.md").write_text(
        "# Eval Case: Activity Recap\n\n"
        "## User request\nSummarize recent activity.\n\n"
        "## User request\nDuplicate prompt creates ambiguous eval setup.\n\n"
        "## Expected behavior\nUse local evidence and state checked scope.\n\n"
        "## Failure if\nInvents work or omits verification scope.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/cases/activity-recap.md section must appear exactly once: ## User request" in errors


def test_skills_must_have_exactly_one_h1(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Use when a sample request needs routing.",
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


def test_skill_frontmatter_description_must_name_trigger(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Route sample requests.",
            "---",
            "# sample",
            "## Trigger",
            "Use for sample requests.",
            "## Inputs",
            "Raw request.",
            "## Procedure",
            "Check the request.",
            "## Verification",
            "Confirm evidence.",
            "## Failure Modes",
            "Stop if evidence is missing.",
            "## Example",
            "Sample request routes through the skill.",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "skills/sample/SKILL.md frontmatter description must start with 'Use when'" in errors


def test_skill_frontmatter_description_must_start_with_trigger(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Route sample requests. Use when a sample request needs routing.",
            "---",
            "# sample",
            "## Trigger",
            "Use for sample requests.",
            "## Inputs",
            "Raw request.",
            "## Procedure",
            "Check the request.",
            "## Verification",
            "Confirm evidence.",
            "## Failure Modes",
            "Stop if evidence is missing.",
            "## Example",
            "Sample request routes through the skill.",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "skills/sample/SKILL.md frontmatter description must start with 'Use when'" in errors


def test_skill_frontmatter_must_have_closing_delimiter(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Use when a sample request needs routing.",
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


def test_skill_frontmatter_must_close_before_markdown_body(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Use when a sample request needs routing.",
            "# sample",
            "## Trigger",
            "Use for sample requests.",
            "## Inputs",
            "Raw request.",
            "## Procedure",
            "Check the request.",
            "## Verification",
            "Confirm evidence.",
            "## Failure Modes",
            "Stop if evidence is missing.",
            "## Example",
            "Sample request routes through the skill.",
            "---",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "skills/sample/SKILL.md frontmatter must be delimited by ---" in errors


def test_skill_required_sections_must_have_body(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Use when a sample request needs routing.",
            "---",
            "# sample",
            "## Trigger",
            "Use for sample requests.",
            "## Inputs",
            "Raw request.",
            "## Procedure",
            "Check the request.",
            "## Verification",
            "Confirm evidence.",
            "## Failure Modes",
            "Stop if evidence is missing.",
            "## Example",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "skills/sample/SKILL.md section has no body: ## Example" in errors


def test_skill_required_sections_must_keep_canonical_order(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Use when a sample request needs routing.",
            "---",
            "# sample",
            "## Trigger",
            "Use for sample requests.",
            "## Procedure",
            "Check the request.",
            "## Inputs",
            "Raw request.",
            "## Verification",
            "Confirm evidence.",
            "## Failure Modes",
            "Stop if evidence is missing.",
            "## Example",
            "Sample request routes through the skill.",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "skills/sample/SKILL.md sections must appear in canonical order" in errors


def test_skill_required_sections_must_not_be_duplicated(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: sample",
            "description: Use when a sample request needs routing.",
            "---",
            "# sample",
            "## Trigger",
            "Use for sample requests.",
            "## Trigger",
            "Duplicate trigger text.",
            "## Inputs",
            "Raw request.",
            "## Procedure",
            "Check the request.",
            "## Verification",
            "Confirm evidence.",
            "## Failure Modes",
            "Stop if evidence is missing.",
            "## Example",
            "Sample request routes through the skill.",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "skills/sample/SKILL.md section must appear exactly once: ## Trigger" in errors


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


def test_banned_public_copy_terms_are_case_insensitive(tmp_path):
    write_minimal_repo(tmp_path)
    internal_name = ("G" + "Brain").lower()
    canonical_name = "G" + "Brain"
    (tmp_path / "docs" / "copy.md").write_text(
        f"This says {internal_name} in public copy.\n", encoding="utf-8"
    )

    errors = validate_repo.validate(tmp_path)

    assert f"docs/copy.md contains banned public-copy term: {canonical_name}" in errors


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
        f"# required\n\n- `/brain-sample` — sample command.\n- `sample` — sample skill.\n- `activity-recap` — activity skill.\n- `agent-output-verifier` — verifier skill.\n\n## Validation\n\n```bash\npython3 -m pip install -r requirements-dev.txt\npython -m pytest -q\npython scripts/validate_repo.py\ngit diff --check\n```\n\n## vs others\n\nCompared with {vendor_name}, Agent Brain stays portable.\n",
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


def test_skill_directory_names_must_be_lowercase_kebab_case(tmp_path):
    write_minimal_repo(tmp_path)
    uppercase_skill_dir = tmp_path / "skills" / "SampleSkill"
    uppercase_skill_dir.mkdir()
    (uppercase_skill_dir / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: SampleSkill",
            "description: Use when a sample request needs routing.",
            "---",
            "# SampleSkill",
            "## Trigger",
            "Use for sample requests.",
            "## Inputs",
            "Raw request.",
            "## Procedure",
            "Check the request.",
            "## Verification",
            "Confirm evidence.",
            "## Failure Modes",
            "Stop if evidence is missing.",
            "## Example",
            "Sample request routes through the skill.",
        ]),
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text(
        "# required\n\n- `/brain-sample` — sample command.\n- `sample` — sample skill.\n- `SampleSkill` — sample skill.\n- `activity-recap` — activity skill.\n- `agent-output-verifier` — verifier skill.\n\n## Validation\n\n```bash\npython3 -m pip install -r requirements-dev.txt\npython -m pytest -q\npython scripts/validate_repo.py\ngit diff --check\n```\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "skills/SampleSkill/SKILL.md skill directory must use lowercase kebab-case" in errors


def test_skill_frontmatter_name_must_match_directory(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "sample" / "SKILL.md").write_text(
        "\n".join([
            "---",
            "name: wrong-name",
            "description: Use when a sample request needs routing.",
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
            "description: Use when a sample request needs routing.",
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


def test_command_filenames_must_be_lowercase_kebab_case(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "commands" / "brain_sample.md").write_text(
        "\n".join([
            "# /brain_sample",
            "## Purpose",
            "Route sample work.",
            "## When to use",
            "Use for sample requests.",
            "## Input contract",
            "Raw request.",
            "## Workflow",
            "Inspect inputs and decide the next action.",
            "## Output",
            "A concrete next action.",
            "## Stop conditions",
            "Stop when the request is unsafe.",
            "## Quality bar",
            "Evidence is checked before output.",
        ]),
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text(
        "# required\n\n- `/brain_sample` — sample command.\n- `/brain-sample` — sample command.\n- `sample` — sample skill.\n- `activity-recap` — activity skill.\n- `agent-output-verifier` — verifier skill.\n\n## Validation\n\n```bash\npython3 -m pip install -r requirements-dev.txt\npython -m pytest -q\npython scripts/validate_repo.py\ngit diff --check\n```\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "commands/brain_sample.md filename must use lowercase kebab-case" in errors


def test_command_filenames_must_use_brain_prefix(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "commands" / "sample.md").write_text(
        "\n".join([
            "# /sample",
            "## Purpose",
            "Route sample work.",
            "## When to use",
            "Use for sample requests.",
            "## Input contract",
            "Raw request.",
            "## Workflow",
            "Inspect inputs and decide the next action.",
            "## Output",
            "A concrete next action.",
            "## Stop conditions",
            "Stop when the request is unsafe.",
            "## Quality bar",
            "Evidence is checked before output.",
        ]),
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text(
        "# required\n\n- `/sample` — sample command.\n- `/brain-sample` — sample command.\n- `sample` — sample skill.\n- `activity-recap` — activity skill.\n- `agent-output-verifier` — verifier skill.\n\n## Validation\n\n```bash\npython3 -m pip install -r requirements-dev.txt\npython -m pytest -q\npython scripts/validate_repo.py\ngit diff --check\n```\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "commands/sample.md filename must start with brain-" in errors


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


def test_eval_case_required_sections_must_have_body(tmp_path):
    write_minimal_repo(tmp_path)
    case_dir = tmp_path / "evals" / "cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "thin-case.md").write_text(
        "\n".join([
            "# Eval Case: Thin Case",
            "## User request",
            "Do something",
            "## Expected behavior",
            "## Failure if",
            "The response misses the point",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/cases/thin-case.md section has no body: ## Expected behavior" in errors


def test_eval_case_required_sections_must_keep_canonical_order(tmp_path):
    write_minimal_repo(tmp_path)
    case_dir = tmp_path / "evals" / "cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "thin-case.md").write_text(
        "\n".join([
            "# Eval Case: Thin Case",
            "## Expected behavior",
            "Do the requested work with evidence.",
            "## User request",
            "Do something",
            "## Failure if",
            "The response misses the point.",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/cases/thin-case.md sections must appear in canonical order" in errors


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
        "# Evals\n\n- `activity-recap`\n- `agent-output-verifier`\n- `build-vs-buy-decision`\n- `context-drift`\n- `source-to-skill-distillation`\n- `skill-boundary-creep`\n- `verification-shortcut`\n- `no-user-defined`\n- `review-gate-skip`\n- `plan-slicing`\n- `spec-before-build`\n- `ship-without-rollback`\n",
        encoding="utf-8",
    )

    assert validate_repo.validate(tmp_path) == []


def test_template_heading_must_match_filename(tmp_path):
    write_minimal_repo(tmp_path)
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "product-brief.md").write_text(
        "# Different Brief\n\nSchema fields: `title`.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "templates/product-brief.md heading must be # Product Brief" in errors


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


def test_template_schema_field_references_must_be_exact_tokens(tmp_path):
    write_minimal_repo(tmp_path)
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (tmp_path / "schemas" / "product-brief.schema.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "Product Brief",
                "type": "object",
                "additionalProperties": False,
                "required": ["title", "user"],
                "properties": {
                    "title": {"type": "string"},
                    "user": {"type": "string"},
                },
            }
        ),
        encoding="utf-8",
    )
    (templates_dir / "product-brief.md").write_text(
        "# Product Brief\n\nSchema fields: `title`, `target_user`.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "templates/product-brief.md missing required schema field reference: user" in errors


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


def test_agent_output_verifier_skill_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "skills" / "agent-output-verifier" / "SKILL.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing skills/agent-output-verifier/SKILL.md" in errors


def test_activity_recap_eval_case_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "cases" / "activity-recap.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/cases/activity-recap.md" in errors


def test_source_to_skill_distillation_eval_case_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "cases" / "source-to-skill-distillation.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/cases/source-to-skill-distillation.md" in errors


def test_agent_output_verifier_eval_case_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "cases" / "agent-output-verifier.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/cases/agent-output-verifier.md" in errors


def test_verification_shortcut_eval_case_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "cases" / "verification-shortcut.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/cases/verification-shortcut.md" in errors


def test_skill_boundary_creep_eval_case_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "cases" / "skill-boundary-creep.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/cases/skill-boundary-creep.md" in errors


def test_no_user_defined_eval_case_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "cases" / "no-user-defined.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/cases/no-user-defined.md" in errors


def test_evals_readme_is_required(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "README.md").unlink()

    errors = validate_repo.validate(tmp_path)

    assert "missing evals/README.md" in errors


def test_evals_readme_must_have_exactly_one_h1(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "README.md").write_text(
        "# Evals\n\n# Duplicate Evals\n\n- `activity-recap`\n- `source-to-skill-distillation`\n- `agent-output-verifier`\n- `verification-shortcut`\n- `skill-boundary-creep`\n- `no-user-defined`\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/README.md must contain exactly one H1 heading" in errors


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


def test_quality_workflow_must_run_whitespace_check(tmp_path):
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
            "      - run: python -m pytest -q",
            "      - run: python scripts/validate_repo.py",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/quality.yml must run: git diff --check" in errors


def test_all_workflows_must_run_whitespace_check(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".github" / "workflows" / "validate.yml").write_text(
        "\n".join([
            "name: validate",
            "on:",
            "  push:",
            "  pull_request:",
            "jobs:",
            "  repo-validation:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - run: python -m pytest -q",
            "      - run: python scripts/validate_repo.py",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/validate.yml must run: git diff --check" in errors


def test_yaml_workflows_must_run_whitespace_check(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".github" / "workflows" / "validate.yaml").write_text(
        "\n".join([
            "name: validate",
            "on:",
            "  push:",
            "  pull_request:",
            "jobs:",
            "  repo-validation:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - run: python -m pytest -q",
            "      - run: python scripts/validate_repo.py",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/validate.yaml must run: git diff --check" in errors


def test_all_workflows_must_use_read_only_repository_permissions(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".github" / "workflows" / "validate.yml").write_text(
        "\n".join([
            "name: validate",
            "on:",
            "  push:",
            "  pull_request:",
            "jobs:",
            "  repo-validation:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - run: python -m pytest -q",
            "      - run: python scripts/validate_repo.py",
            "      - run: git diff --check",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/validate.yml must set permissions to contents: read" in errors


def test_all_workflows_must_set_timeout_minutes(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".github" / "workflows" / "validate.yml").write_text(
        "\n".join([
            "name: validate",
            "on:",
            "  push:",
            "  pull_request:",
            "permissions:",
            "  contents: read",
            "jobs:",
            "  repo-validation:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - run: python -m pytest -q",
            "      - run: python scripts/validate_repo.py",
            "      - run: git diff --check",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/validate.yml must set timeout-minutes" in errors


def test_workflows_must_not_request_write_repository_permissions(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".github" / "workflows" / "validate.yml").write_text(
        "\n".join([
            "name: validate",
            "on:",
            "  push:",
            "  pull_request:",
            "permissions:",
            "  contents: read",
            "  issues: write",
            "jobs:",
            "  repo-validation:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - run: python -m pytest -q",
            "      - run: python scripts/validate_repo.py",
            "      - run: git diff --check",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/validate.yml must not request write repository permissions: issues" in errors


def test_workflows_must_not_request_job_level_write_repository_permissions(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".github" / "workflows" / "validate.yml").write_text(
        "\n".join([
            "name: validate",
            "on:",
            "  push:",
            "  pull_request:",
            "permissions:",
            "  contents: read",
            "jobs:",
            "  repo-validation:",
            "    runs-on: ubuntu-latest",
            "    permissions:",
            "      contents: write",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - run: python -m pytest -q",
            "      - run: python scripts/validate_repo.py",
            "      - run: git diff --check",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/validate.yml must not request write repository permissions: contents" in errors


def test_all_workflows_must_run_on_push_and_pull_request(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".github" / "workflows" / "nightly.yml").write_text(
        "\n".join([
            "name: Nightly",
            "on:",
            "  push:",
            "permissions:",
            "  contents: read",
            "jobs:",
            "  validate:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - run: git diff --check",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/nightly.yml must run on pull_request" in errors


def test_workflow_trigger_check_accepts_inline_event_list(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".github" / "workflows" / "inline-triggers.yml").write_text(
        "\n".join([
            "name: Inline Triggers",
            "on: [push, pull_request]",
            "permissions:",
            "  contents: read",
            "jobs:",
            "  validate:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - run: git diff --check",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/inline-triggers.yml must run on push" not in errors
    assert ".github/workflows/inline-triggers.yml must run on pull_request" not in errors


def test_workflow_trigger_check_accepts_block_event_list(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".github" / "workflows" / "block-triggers.yml").write_text(
        "\n".join([
            "name: Block Triggers",
            "on:",
            "  - push",
            "  - pull_request",
            "permissions:",
            "  contents: read",
            "jobs:",
            "  validate:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - run: git diff --check",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/block-triggers.yml must run on push" not in errors
    assert ".github/workflows/block-triggers.yml must run on pull_request" not in errors


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


def test_quality_workflow_must_use_read_only_repository_permissions(tmp_path):
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
            "      - run: python -m pytest -q",
            "      - run: python scripts/validate_repo.py",
            "      - run: git diff --check",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".github/workflows/quality.yml must set permissions to contents: read" in errors


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


def test_command_required_sections_must_have_body(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "commands" / "brain-sample.md").write_text(
        "\n".join([
            "# /brain-sample",
            "## Purpose",
            "Route the work.",
            "## When to use",
            "Use for sample requests.",
            "## Input contract",
            "Raw request.",
            "## Workflow",
            "Inspect and decide.",
            "## Output",
            "Next action.",
            "## Stop conditions",
            "Stop if unsafe.",
            "## Quality bar",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "commands/brain-sample.md section has no body: ## Quality bar" in errors


def test_command_required_sections_must_keep_canonical_order(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "commands" / "brain-sample.md").write_text(
        "\n".join([
            "# /brain-sample",
            "## Purpose",
            "Route the work.",
            "## Workflow",
            "Inspect and decide.",
            "## When to use",
            "Use for sample requests.",
            "## Input contract",
            "Raw request.",
            "## Output",
            "Next action.",
            "## Stop conditions",
            "Stop if unsafe.",
            "## Quality bar",
            "Evidence is checked before output.",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "commands/brain-sample.md sections must appear in canonical order" in errors


def test_command_required_sections_must_not_be_duplicated(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "commands" / "brain-sample.md").write_text(
        "\n".join([
            "# /brain-sample",
            "## Purpose",
            "Route the work.",
            "## Purpose",
            "Duplicate purpose text.",
            "## When to use",
            "Use for sample requests.",
            "## Input contract",
            "Raw request.",
            "## Workflow",
            "Inspect and decide.",
            "## Output",
            "Next action.",
            "## Stop conditions",
            "Stop if unsafe.",
            "## Quality bar",
            "Evidence is checked before output.",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "commands/brain-sample.md section must appear exactly once: ## Purpose" in errors


def test_readme_must_list_available_commands(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "README.md").write_text("# required\n\nNo command catalog here.\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert "README.md missing command catalog entry: /brain-sample" in errors


def test_readme_command_catalog_entries_must_be_backticked(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "README.md").write_text(
        "# required\n\n/brain-sample is mentioned only as prose.\n- `sample` — sample skill.\n- `activity-recap` — activity skill.\n\n## Validation\n\n```bash\npython3 -m pip install -r requirements-dev.txt\npython -m pytest -q\npython scripts/validate_repo.py\ngit diff --check\n```\n",
        encoding="utf-8",
    )

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


def test_readme_validation_section_must_list_whitespace_check(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "README.md").write_text(
        "# required\n\n- `/brain-sample` — sample command.\n- `sample` — sample skill.\n- `activity-recap` — activity skill.\n\n## Validation\n\n```bash\npython3 -m pip install -r requirements-dev.txt\npython -m pytest -q\npython scripts/validate_repo.py\n```\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "README.md validation section must document: git diff --check" in errors


def test_readme_validation_section_must_install_dev_requirements(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "README.md").write_text(
        "# required\n\n- `/brain-sample` — sample command.\n- `sample` — sample skill.\n- `activity-recap` — activity skill.\n\n## Validation\n\n```bash\npython -m pytest -q\npython scripts/validate_repo.py\ngit diff --check\n```\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "README.md validation section must document: pip install -r requirements-dev.txt" in errors


def test_contributing_validation_section_must_list_whitespace_check(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "CONTRIBUTING.md").write_text(
        "# Contributing\n\n## Validation\n\n```bash\npython3 -m pip install -r requirements-dev.txt\npython3 -m pytest -q\npython3 scripts/validate_repo.py\n```\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "CONTRIBUTING.md validation section must document: git diff --check" in errors


def test_contributing_validation_section_must_list_pytest(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "CONTRIBUTING.md").write_text(
        "# Contributing\n\n## Validation\n\n```bash\npython3 -m pip install -r requirements-dev.txt\npython3 scripts/validate_repo.py\ngit diff --check\n```\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "CONTRIBUTING.md validation section must document: pytest -q" in errors


def test_evals_readme_must_list_available_cases(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "README.md").write_text(
        "# Evals\n\nNo case catalog here.\n", encoding="utf-8"
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/README.md missing eval case catalog entry: activity-recap" in errors


def test_evals_readme_case_catalog_entries_must_be_backticked(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / "evals" / "README.md").write_text(
        "# Evals\n\nactivity-recap is mentioned only as prose.\n- `agent-output-verifier`\n- `source-to-skill-distillation`\n",
        encoding="utf-8",
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


def test_eval_rubric_filenames_must_use_lowercase_kebab_case(tmp_path):
    write_minimal_repo(tmp_path)
    rubric_dir = tmp_path / "evals" / "rubrics"
    rubric_dir.mkdir(parents=True)
    (rubric_dir / "Quality_Rubric.md").write_text(
        "# Quality Rubric\n\n## Dimensions\n\nScore the evidence quality.\n\n## Interpretation\n\nUse the score to decide readiness.\n",
        encoding="utf-8",
    )
    (tmp_path / "evals" / "README.md").write_text(
        "# Evals\n\n- `activity-recap`\n- `agent-output-verifier`\n- `source-to-skill-distillation`\n- `verification-shortcut`\n- `Quality_Rubric`\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/rubrics/Quality_Rubric.md filename must use lowercase kebab-case" in errors


def test_eval_rubrics_require_scoring_and_interpretation_sections(tmp_path):
    write_minimal_repo(tmp_path)
    rubric_dir = tmp_path / "evals" / "rubrics"
    rubric_dir.mkdir(parents=True)
    (rubric_dir / "quality.md").write_text(
        "# Quality Rubric\n\n## Dimensions\n\nScore the evidence quality.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/rubrics/quality.md missing ## Interpretation" in errors


def test_eval_rubric_heading_must_match_filename(tmp_path):
    write_minimal_repo(tmp_path)
    rubric_dir = tmp_path / "evals" / "rubrics"
    rubric_dir.mkdir(parents=True)
    (rubric_dir / "quality-score.md").write_text(
        "# Different Rubric\n\n## Dimensions\n\nScore quality.\n\n## Interpretation\n\nUse the score to decide readiness.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/rubrics/quality-score.md heading must be # Quality Score" in errors


def test_eval_rubric_sections_must_be_in_canonical_order(tmp_path):
    write_minimal_repo(tmp_path)
    rubric_dir = tmp_path / "evals" / "rubrics"
    rubric_dir.mkdir(parents=True)
    (rubric_dir / "quality.md").write_text(
        "# Quality\n\n## Interpretation\n\nUse the score to decide readiness.\n\n## Dimensions\n\nScore quality.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/rubrics/quality.md sections must appear in canonical order" in errors


def test_eval_rubric_required_sections_must_not_be_duplicated(tmp_path):
    write_minimal_repo(tmp_path)
    rubric_dir = tmp_path / "evals" / "rubrics"
    rubric_dir.mkdir(parents=True)
    (rubric_dir / "quality.md").write_text(
        "# Quality\n\n"
        "## Dimensions\n\nScore evidence quality.\n\n"
        "## Dimensions\n\nDuplicate dimensions create ambiguous scoring.\n\n"
        "## Interpretation\n\nUse the score to decide readiness.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/rubrics/quality.md section must appear exactly once: ## Dimensions" in errors


def test_evals_readme_must_list_available_rubrics(tmp_path):
    write_minimal_repo(tmp_path)
    rubric_dir = tmp_path / "evals" / "rubrics"
    rubric_dir.mkdir(parents=True)
    (rubric_dir / "quality.md").write_text(
        "# Quality Rubric\n\n## Dimensions\n\nScore the evidence quality.\n\n## Interpretation\n\nUse the score to decide whether to ship.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/README.md missing eval rubric catalog entry: quality" in errors


def test_evals_readme_rubric_catalog_entries_must_be_backticked(tmp_path):
    write_minimal_repo(tmp_path)
    rubric_dir = tmp_path / "evals" / "rubrics"
    rubric_dir.mkdir(parents=True)
    (rubric_dir / "quality.md").write_text(
        "# Quality\n\n## Dimensions\n\nScore quality.\n\n## Interpretation\n\nUse the score to decide readiness.\n",
        encoding="utf-8",
    )
    (tmp_path / "evals" / "README.md").write_text(
        "# Evals\n\n- `activity-recap`\n- `agent-output-verifier`\n- `source-to-skill-distillation`\n\nquality is mentioned only as prose.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "evals/README.md missing eval rubric catalog entry: quality" in errors


def test_gitignore_must_exclude_generated_python_cache_artifacts(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".gitignore").write_text(".pytest_cache/\n", encoding="utf-8")

    errors = validate_repo.validate(tmp_path)

    assert ".gitignore must ignore local/generated Python artifacts: __pycache__/" in errors


def test_gitignore_must_exclude_local_virtual_environments(tmp_path):
    write_minimal_repo(tmp_path)
    (tmp_path / ".gitignore").write_text(
        "__pycache__/\n*.py[cod]\n.pytest_cache/\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert ".gitignore must ignore local/generated Python artifacts: .venv/" in errors


def test_public_copy_scan_ignores_local_dependency_directories(tmp_path):
    write_minimal_repo(tmp_path)
    dependency_dir = tmp_path / "node_modules" / "generated-package"
    dependency_dir.mkdir(parents=True)
    banned_term = "Open" + "AI"
    (dependency_dir / "README.md").write_text(
        f"# Generated Package\n\nMentions {banned_term} outside project copy.\n",
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert errors == []


def test_skill_template_description_must_start_with_trigger(tmp_path):
    write_minimal_repo(tmp_path)
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "skill-template.md").write_text(
        "\n".join([
            "---",
            "name: example-skill",
            "description: One sentence describing the skill. Use when sample work needs routing.",
            "---",
            "# Skill Name",
            "## Trigger",
            "Use when sample work needs routing.",
            "## Inputs",
            "Raw request.",
            "## Procedure",
            "Check the request.",
            "## Verification",
            "Confirm evidence.",
            "## Failure Modes",
            "Stop if evidence is missing.",
            "## Example",
            "Sample request routes through the skill.",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "templates/skill-template.md frontmatter description must start with 'Use when'" in errors


def test_skill_template_name_must_be_lowercase_kebab_case(tmp_path):
    write_minimal_repo(tmp_path)
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "skill-template.md").write_text(
        "\n".join([
            "---",
            "name: Example Skill",
            "description: Use when sample work needs routing.",
            "---",
            "# Skill Name",
            "## Trigger",
            "Use when sample work needs routing.",
            "## Inputs",
            "Raw request.",
            "## Procedure",
            "Check the request.",
            "## Verification",
            "Confirm evidence.",
            "## Failure Modes",
            "Stop if evidence is missing.",
            "## Example",
            "Sample request routes through the skill.",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "templates/skill-template.md frontmatter name must use lowercase kebab-case" in errors


def test_skill_template_frontmatter_must_have_closing_delimiter(tmp_path):
    write_minimal_repo(tmp_path)
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "skill-template.md").write_text(
        "\n".join([
            "---",
            "name: example-skill",
            "description: Use when sample work needs routing.",
            "# Skill Name",
            "## Trigger",
            "Use when sample work needs routing.",
            "## Inputs",
            "Raw request.",
            "## Procedure",
            "Check the request.",
            "## Verification",
            "Confirm evidence.",
            "## Failure Modes",
            "Stop if evidence is missing.",
            "## Example",
            "Sample request routes through the skill.",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "templates/skill-template.md frontmatter must be delimited by ---" in errors


def test_skill_template_must_include_required_skill_sections(tmp_path):
    write_minimal_repo(tmp_path)
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "skill-template.md").write_text(
        "\n".join([
            "---",
            "name: example-skill",
            "description: Use when sample work needs routing.",
            "---",
            "# Skill Name",
            "## Trigger",
            "Use when sample work needs routing.",
            "## Inputs",
            "Raw request.",
            "## Procedure",
            "Check the request.",
            "## Verification",
            "Confirm evidence.",
            "## Failure Modes",
            "Stop if evidence is missing.",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "templates/skill-template.md missing ## Example" in errors


def test_skill_template_must_include_anti_rationalization_section(tmp_path):
    write_minimal_repo(tmp_path)
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "skill-template.md").write_text(
        "\n".join([
            "---",
            "name: example-skill",
            "description: Use when sample work needs routing.",
            "---",
            "# Skill Name",
            "## Trigger",
            "Use when sample work needs routing.",
            "## Inputs",
            "Raw request.",
            "## Procedure",
            "Check the request.",
            "## Verification",
            "Confirm evidence.",
            "## Output Artifact",
            "A checked artifact.",
            "## Failure Modes",
            "Stop if evidence is missing.",
            "## Example",
            "Sample request routes through the skill.",
        ]),
        encoding="utf-8",
    )

    errors = validate_repo.validate(tmp_path)

    assert "templates/skill-template.md missing ## Anti-Rationalization" in errors

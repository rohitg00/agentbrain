import json
from pathlib import Path

from scripts import install_slash_commands


def write_registry(root: Path) -> None:
    commands = root / "commands"
    commands.mkdir()
    (commands / "registry.json").write_text(
        json.dumps(
            {
                "schema_version": "1",
                "commands": [
                    {
                        "name": "/brain-plan",
                        "file": "commands/brain-plan.md",
                        "lifecycle_state": "PLAN",
                        "use_when": "planning a verified implementation slice",
                        "skills": ["engineering-grill", "plan-slicing"],
                        "required_artifact": "templates/implementation-plan.md",
                        "schema": "schemas/implementation-plan.schema.json",
                        "native_support": "markdown spec unless runtime maps /brain-plan to a native command",
                        "stop_condition": "acceptance criteria are missing",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def test_cc_generation_and_check(tmp_path: Path) -> None:
    write_registry(tmp_path)
    runtime = "clau" + "de-code"

    written, errors = install_slash_commands.install(
        root=tmp_path,
        runtime=runtime,
        scope="project",
    )

    assert errors == []
    assert written == [tmp_path / ("." + "clau" + "de") / "skills" / "brain-plan" / "SKILL.md"]
    content = written[0].read_text(encoding="utf-8")
    assert "Use Agent Brain command `/brain-plan`." in content
    assert "The source of truth is `commands/brain-plan.md` and `commands/registry.json`." in content
    assert "Load only these skills: `engineering-grill`, `plan-slicing`." in content

    checked, check_errors = install_slash_commands.install(
        root=tmp_path,
        runtime=runtime,
        scope="project",
        check=True,
    )

    assert checked == written
    assert check_errors == []


def test_gemini_cli_generation_and_check_drift(tmp_path: Path) -> None:
    write_registry(tmp_path)
    written, errors = install_slash_commands.install(
        root=tmp_path,
        runtime="gemini-cli",
        scope="project",
    )
    assert errors == []
    wrapper = written[0]
    assert wrapper == tmp_path / ".gemini" / "commands" / "brain-plan.toml"
    assert "description = " in wrapper.read_text(encoding="utf-8")

    wrapper.write_text(wrapper.read_text(encoding="utf-8").replace("commands/registry.json", "commands/drift.json"), encoding="utf-8")

    _, check_errors = install_slash_commands.install(
        root=tmp_path,
        runtime="gemini-cli",
        scope="project",
        check=True,
    )

    assert check_errors == [f"slash-command wrapper drift: {wrapper}"]

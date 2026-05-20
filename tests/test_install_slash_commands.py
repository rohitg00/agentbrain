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
    assert "Wrapper boundary marker: `cc-source-of-truth`." in content
    assert "Load only these skills: `engineering-grill`, `plan-slicing`." in content

    checked, check_errors = install_slash_commands.install(
        root=tmp_path,
        runtime=runtime,
        scope="project",
        check=True,
    )

    assert checked == written
    assert check_errors == []


def test_registry_loader_rejects_non_object_command_entries(tmp_path: Path) -> None:
    commands = tmp_path / "commands"
    commands.mkdir()
    (commands / "registry.json").write_text(
        json.dumps({"schema_version": "1", "commands": ["bad-entry"]}),
        encoding="utf-8",
    )

    try:
        install_slash_commands.load_registry(tmp_path)
    except ValueError as exc:
        assert "commands/registry.json commands entry 0 must be an object, got str" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("load_registry accepted a non-object command entry")


def test_command_slug_rejects_path_traversal_values() -> None:
    for command_name in ["/../../tmp/x", "/brain/plan", r"/brain\plan", "/..", "/"]:
        try:
            install_slash_commands.command_slug(command_name)
        except ValueError as exc:
            assert "invalid command slug" in str(exc)
        else:  # pragma: no cover
            raise AssertionError(f"accepted unsafe command slug: {command_name}")


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
    content = wrapper.read_text(encoding="utf-8")
    assert "description = " in content
    assert "Wrapper boundary marker: `gemini-cli-source-of-truth`." in content

    wrapper.write_text(wrapper.read_text(encoding="utf-8").replace("commands/registry.json", "commands/drift.json"), encoding="utf-8")

    _, check_errors = install_slash_commands.install(
        root=tmp_path,
        runtime="gemini-cli",
        scope="project",
        check=True,
    )

    assert check_errors == [f"slash-command wrapper drift: {wrapper}"]

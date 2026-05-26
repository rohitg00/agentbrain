import json
from pathlib import Path

from scripts import install_slash_commands


def write_registry(root: Path) -> None:
    for rel_path in ["AGENTBRAIN.md", "PRINCIPLES.md", "ANTI_RATIONALIZATION.md"]:
        (root / rel_path).write_text(f"# {rel_path}\n", encoding="utf-8")
    commands = root / "commands"
    commands.mkdir()
    (commands / "README.md").write_text("# Command Catalog\n", encoding="utf-8")
    (commands / "brain-plan.md").write_text(
        "# /brain-plan\n\n"
        "## Purpose\nState: PLAN\n\n"
        "## Skills to load\n"
        "- `engineering-grill` from `skills/engineering-grill/SKILL.md`.\n"
        "- `plan-slicing` from `skills/plan-slicing/SKILL.md`.\n\n"
        "## Output\nRequired artifact: **Implementation Plan** using `templates/implementation-plan.md` and `schemas/implementation-plan.schema.json`.\n",
        encoding="utf-8",
    )
    docs = root / "docs"
    docs.mkdir()
    (docs / "state-machine.md").write_text("# State Machine\n", encoding="utf-8")
    skills = root / "skills"
    skills.mkdir()
    (skills / "README.md").write_text("# Skills\n", encoding="utf-8")
    for skill in ["engineering-grill", "plan-slicing"]:
        skill_dir = skills / skill
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(f"# {skill}\n", encoding="utf-8")
    templates = root / "templates"
    templates.mkdir()
    (templates / "implementation-plan.md").write_text("# Implementation Plan\n", encoding="utf-8")
    schemas = root / "schemas"
    schemas.mkdir()
    (schemas / "implementation-plan.schema.json").write_text(
        json.dumps({"type": "object"}) + "\n",
        encoding="utf-8",
    )
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


def test_plugin_bundle_generation_and_check(tmp_path: Path) -> None:
    write_registry(tmp_path)

    written, errors = install_slash_commands.install(
        root=tmp_path,
        runtime="agentbrain-plugin",
        scope="project",
    )

    assert errors == []
    expected_paths = {
        tmp_path / ("." + "clau" + "de-plugin") / "marketplace.json",
        tmp_path / ".agents" / "plugins" / "marketplace.json",
        tmp_path / "plugins" / "agentbrain" / ("." + "clau" + "de-plugin") / "plugin.json",
        tmp_path / "plugins" / "agentbrain" / ("." + "co" + "dex-plugin") / "plugin.json",
        tmp_path / "plugins" / "agentbrain" / "registry.json",
        tmp_path / "plugins" / "agentbrain" / "skills" / "agentbrain" / "SKILL.md",
        tmp_path / "plugins" / "agentbrain" / "commands" / "brain-plan.md",
    }
    assert expected_paths.issubset(set(written))
    command_wrapper = tmp_path / "plugins" / "agentbrain" / "commands" / "brain-plan.md"
    command_text = command_wrapper.read_text(encoding="utf-8")
    assert "Wrapper boundary marker: `plugin-bundle-source-of-truth`." in command_text
    assert "## Bundled Command Body" in command_text
    assert "# /brain-plan" in command_text
    assert (tmp_path / "plugins" / "agentbrain" / "skills" / "engineering-grill" / "SKILL.md").exists()
    assert (tmp_path / "plugins" / "agentbrain" / "templates" / "implementation-plan.md").exists()
    assert (tmp_path / "plugins" / "agentbrain" / "schemas" / "implementation-plan.schema.json").exists()
    plugin_registry = json.loads((tmp_path / "plugins" / "agentbrain" / "registry.json").read_text(encoding="utf-8"))
    assert plugin_registry["commands"][0]["file"] == "commands/brain-plan.md"
    assert plugin_registry["commands"][0]["source_file"] == "commands/brain-plan.md"
    assert "commands/registry.json" in (tmp_path / "plugins" / "agentbrain" / "skills" / "agentbrain" / "SKILL.md").read_text(encoding="utf-8")

    checked, check_errors = install_slash_commands.install(
        root=tmp_path,
        runtime="agentbrain-plugin",
        scope="project",
        check=True,
    )

    assert expected_paths.issubset(set(checked))
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

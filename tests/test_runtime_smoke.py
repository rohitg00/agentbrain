import json
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts import runtime_smoke


def test_build_report_emits_schema_valid_runtime_smoke_for_plain_checkout(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q"],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope read_only_smoke",
    )

    schema = json.loads(Path("schemas/runtime-smoke.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(report)

    assert report["runtime"] == "generic-cli-runtime"
    assert report["python_executable"]
    assert report["writable_temp_dir_status"] in {"writable", "blocked"}
    assert report["git_freshness_result"].startswith("unavailable:")
    assert "read-only smoke" in "\n".join(report["evidence"]).lower()
    assert "markdown specs" in "\n".join(report["evidence"]).lower()


def test_build_report_records_smoke_result_and_command_exit_status(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q"],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3",
        command_exit_status=0,
        smoke_result="pass",
    )

    assert report["command_exit_status"] == 0
    assert report["smoke_result"] == "pass"
    assert "Command exit status: 0" in report["evidence"]
    assert "Smoke result: pass" in report["evidence"]


def test_build_report_records_transcript_path_for_auditable_runtime_smoke(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q"],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
    )

    assert report["transcript_path"] == "artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log"
    assert "Transcript path: artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log" in report["evidence"]


def test_build_report_records_command_route_and_loaded_skills_for_runtime_handoff(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q"],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3",
        selected_command="/brain-start",
        loaded_skills=["intake", "agent-output-verifier"],
    )

    schema = json.loads(Path("schemas/runtime-smoke.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(report)

    assert report["selected_command"] == "/brain-start"
    assert report["loaded_skills"] == ["intake", "agent-output-verifier"]
    evidence = "\n".join(report["evidence"])
    assert "Selected command: /brain-start" in evidence
    assert "Loaded skills: intake, agent-output-verifier" in evidence


def test_build_report_records_adapter_path_for_runtime_boundary_evidence(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q"],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3",
        adapter_path="adapters/read-only-cli/README.md",
    )

    schema = json.loads(Path("schemas/runtime-smoke.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(report)

    assert report["adapter_path"] == "adapters/read-only-cli/README.md"
    assert "Adapter path: adapters/read-only-cli/README.md" in report["evidence"]


def test_validate_report_against_schema_rejects_incomplete_smoke_artifact():
    incomplete_report = {
        "runtime": "generic-cli-runtime",
        "version": "1.2.3",
    }

    errors = runtime_smoke.validate_report_against_schema(incomplete_report, Path("schemas/runtime-smoke.schema.json"))

    assert any("python_executable" in error for error in errors)
    assert any("run_scope" in error for error in errors)


def test_runtime_smoke_schema_rejects_full_validation_without_durable_transcript(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope full_validation",
        smoke_result="pass",
        transcript_path="not_captured_stdout_only",
    )
    schema = json.loads(Path("schemas/runtime-smoke.schema.json").read_text(encoding="utf-8"))

    errors = [error.message for error in Draft202012Validator(schema).iter_errors(report)]

    assert any("not_captured_stdout_only" in error for error in errors)


def test_full_validation_runtime_smoke_rejects_blocked_commands(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=["python -m pytest -q blocked by sandbox"],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope full_validation",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("full_validation cannot list blocked_commands" in error for error in errors)


def test_read_only_runtime_smoke_requires_blocker_when_smoke_is_blocked(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --smoke-result blocked",
        smoke_result="blocked",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("blocked smoke_result must list at least one blocked command" in error for error in errors)


def test_runtime_smoke_rejects_pass_result_when_command_failed(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3",
        command_exit_status=2,
        smoke_result="pass",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("pass smoke_result requires command_exit_status 0" in error for error in errors)


def test_full_validation_runtime_smoke_requires_durable_transcript_path(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope full_validation",
        smoke_result="pass",
        transcript_path="not_captured_stdout_only",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("full_validation requires a durable transcript_path" in error for error in errors)


def test_full_validation_runtime_smoke_requires_fresh_git_checkout(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope full_validation",
        smoke_result="pass",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("full_validation requires fresh git checkout" in error for error in errors)


def test_full_validation_runtime_smoke_rejects_read_only_sandbox(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope full_validation",
        smoke_result="pass",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("full_validation requires a write-capable sandbox" in error for error in errors)


def test_full_validation_runtime_smoke_requires_routing_evidence(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="unknown",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope full_validation",
        smoke_result="pass",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        selected_command="unknown",
        loaded_skills=[],
        adapter_path="unknown",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("full_validation requires brain_command_mode to be proven" in error for error in errors)
    assert any("full_validation requires a selected /brain-* command" in error for error in errors)
    assert any("full_validation requires at least one loaded skill" in error for error in errors)
    assert any("full_validation requires an adapter_path" in error for error in errors)


def test_main_rejects_schema_invalid_generated_smoke_artifact(monkeypatch, capsys):
    def invalid_report(**_kwargs):
        return {"runtime": "generic-cli-runtime", "version": "1.2.3"}

    monkeypatch.setattr(runtime_smoke, "build_report", invalid_report)

    exit_code = runtime_smoke.main(["--runtime", "generic-cli-runtime", "--version", "1.2.3"])

    assert exit_code == 1
    assert "runtime smoke schema validation failed" in capsys.readouterr().err

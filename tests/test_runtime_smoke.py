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


def test_validate_report_against_schema_rejects_incomplete_smoke_artifact():
    incomplete_report = {
        "runtime": "generic-cli-runtime",
        "version": "1.2.3",
    }

    errors = runtime_smoke.validate_report_against_schema(incomplete_report, Path("schemas/runtime-smoke.schema.json"))

    assert any("python_executable" in error for error in errors)
    assert any("run_scope" in error for error in errors)


def test_main_rejects_schema_invalid_generated_smoke_artifact(monkeypatch, capsys):
    def invalid_report(**_kwargs):
        return {"runtime": "generic-cli-runtime", "version": "1.2.3"}

    monkeypatch.setattr(runtime_smoke, "build_report", invalid_report)

    exit_code = runtime_smoke.main(["--runtime", "generic-cli-runtime", "--version", "1.2.3"])

    assert exit_code == 1
    assert "runtime smoke schema validation failed" in capsys.readouterr().err

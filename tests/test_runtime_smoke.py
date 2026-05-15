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

import json
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "harness_effect.py"
FAKE_TOOL = ROOT / "tests" / "fixtures" / "harness_effect" / "fake_tool.py"
SCHEMA_PATH = ROOT / "schemas" / "harness-effect-report.schema.json"


def write_fixture(path: Path, *, extra_file_args: str = "") -> Path:
    fixture = {
        "id": "fake-tool-presentation-test",
        "tool": {
            "command_template": (
                f"{sys.executable} {FAKE_TOOL} --output-mode {{output_mode}}{{file_dir_arg}}{extra_file_args}"
            ),
            "base_params": {
                "file_dir_arg": "",
            },
        },
        "modes": [
            {"name": "inline", "params": {"output_mode": "inline"}},
            {
                "name": "file",
                "params": {
                    "output_mode": "file",
                    "file_dir_arg": " --output-dir {output_dir}",
                },
            },
        ],
        "parity": {
            "inline_retrieved_fields": ["results[].id"],
            "inline_citation_fields": ["results[].evidence[]"],
            "file_artifact_field": "artifact.path",
            "file_item_evidence_fields": ["id"],
            "file_item_citation_fields": ["evidence[]"],
        },
    }
    path.write_text(json.dumps(fixture), encoding="utf-8")
    return path


def run_script(fixture: Path, output_dir: Path, *, fail_on_mismatch: bool = False) -> subprocess.CompletedProcess:
    args = [
        sys.executable,
        str(SCRIPT),
        str(fixture),
        "--output-dir",
        str(output_dir),
    ]
    if fail_on_mismatch:
        args.append("--fail-on-mismatch")
    return subprocess.run(args, text=True, capture_output=True, check=False)


def test_parity_report_passes_when_modes_agree(tmp_path: Path) -> None:
    fixture = write_fixture(tmp_path / "fixture.json")
    output_dir = tmp_path / "out"
    completed = run_script(fixture, output_dir, fail_on_mismatch=True)

    assert completed.returncode == 0, completed.stderr
    report = json.loads(completed.stdout)
    assert report["verdict"] == "pass"
    assert report["parity"]["ids_equal"] is True
    assert report["parity"]["citations_equal"] is True
    assert {run["mode"] for run in report["modes"]} == {"inline", "file"}
    assert report["byte_budget"]["file_minus_inline_bytes"] < 0


def test_parity_report_fails_when_modes_disagree(tmp_path: Path) -> None:
    fixture = write_fixture(tmp_path / "fixture.json", extra_file_args=" --mismatch")
    output_dir = tmp_path / "out"
    completed = run_script(fixture, output_dir, fail_on_mismatch=True)

    assert completed.returncode == 2, completed.stderr
    report = json.loads(completed.stdout)
    assert report["verdict"] == "fail"
    assert report["parity"]["ids_equal"] is False
    diff = report["parity"]["differences"][0]
    assert diff["missing_in_other_ids"] == ["claim_release_deployment_window"]


def test_parity_report_flags_dropped_citations(tmp_path: Path) -> None:
    fixture = write_fixture(tmp_path / "fixture.json", extra_file_args=" --drop-citations")
    output_dir = tmp_path / "out"
    completed = run_script(fixture, output_dir, fail_on_mismatch=True)

    assert completed.returncode == 2, completed.stderr
    report = json.loads(completed.stdout)
    assert report["parity"]["ids_equal"] is True
    assert report["parity"]["citations_equal"] is False
    diff = report["parity"]["differences"][0]
    assert "source_release_rollback_runbook" in diff["missing_in_other_citations"]


def test_passing_report_validates_against_schema(tmp_path: Path) -> None:
    fixture = write_fixture(tmp_path / "fixture.json")
    output_dir = tmp_path / "out"
    completed = run_script(fixture, output_dir)

    report = json.loads(completed.stdout)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(report), key=lambda e: e.path)
    assert errors == [], [error.message for error in errors]


def test_failing_report_validates_against_schema(tmp_path: Path) -> None:
    fixture = write_fixture(tmp_path / "fixture.json", extra_file_args=" --mismatch")
    output_dir = tmp_path / "out"
    completed = run_script(fixture, output_dir)

    report = json.loads(completed.stdout)
    assert report["verdict"] == "fail"
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(report), key=lambda e: e.path)
    assert errors == [], [error.message for error in errors]


def test_fixture_rejects_single_mode(tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixture.json"
    fixture_path.write_text(
        json.dumps(
            {
                "id": "single",
                "tool": {"command_template": "true"},
                "modes": [{"name": "inline", "params": {}}],
            }
        ),
        encoding="utf-8",
    )
    completed = run_script(fixture_path, tmp_path / "out")
    assert completed.returncode != 0
    assert "at least two modes" in completed.stderr


def test_akbp_search_fixture_template_uses_supported_placeholders() -> None:
    fixture = json.loads(
        (ROOT / "evals" / "harness-effect" / "fixtures" / "akbp-search.json").read_text(encoding="utf-8")
    )
    template = fixture["tool"]["command_template"]
    base = fixture["tool"]["base_params"]
    placeholders = set()
    import re

    for match in re.finditer(r"\{([a-zA-Z0-9_]+)\}", template):
        placeholders.add(match.group(1))
    for mode in fixture["modes"]:
        for value in mode.get("params", {}).values():
            for match in re.finditer(r"\{([a-zA-Z0-9_]+)\}", str(value)):
                placeholders.add(match.group(1))
    allowed = set(base.keys()) | {"output_mode", "output_dir"}
    unknown = placeholders - allowed
    assert not unknown, f"akbp-search fixture references unknown placeholders: {sorted(unknown)}"

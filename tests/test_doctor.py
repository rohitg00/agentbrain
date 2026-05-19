import json
from pathlib import Path

from scripts import doctor


def test_checked_in_doctor_report_example_satisfies_schema():
    report = json.loads(Path("examples/artifacts/doctor-report.example.json").read_text(encoding="utf-8"))

    errors = doctor.validate_report(report, Path("schemas/doctor-report.schema.json"))

    assert errors == []


def test_doctor_detects_public_root_doc_scrub_command_exposure(tmp_path: Path):
    (tmp_path / "README.md").write_text("python scripts/scrub_public_copy.py source\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("# Agent Entry Point\n", encoding="utf-8")
    (tmp_path / "INSTALL_FOR_AGENTS.md").write_text("# Install For Agents\n", encoding="utf-8")

    public_copy = doctor.public_copy_status(tmp_path)

    assert public_copy == {
        "readme_exposes_local_scrub_command": True,
        "root_agent_docs_expose_local_scrub_command": True,
    }

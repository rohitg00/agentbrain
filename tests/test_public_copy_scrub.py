import os
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "scrub_public_copy.py"


def run_scrub(root: Path, *terms: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["AGENTBRAIN_SCRUB_ROOT"] = str(root)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *terms],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def test_scrub_rejects_exact_source_name_in_public_copy(tmp_path: Path) -> None:
    banned = "".join(["Source", "Brand"])
    (tmp_path / "README.md").write_text(
        f"# Harness\n\nThis public copy mentions {banned}.\n",
        encoding="utf-8",
    )

    result = run_scrub(tmp_path, banned)

    assert result.returncode == 1
    assert "README.md:3" in result.stdout
    assert banned not in (tmp_path / "README.md").read_text(encoding="utf-8").splitlines()[0]


def test_scrub_allows_exact_source_name_inside_readme_comparison_section(tmp_path: Path) -> None:
    banned = "".join(["Source", "Brand"])
    (tmp_path / "README.md").write_text(
        "# Harness\n\n"
        "## Comparisons\n\n"
        f"This explicitly scoped comparison can name {banned}.\n\n"
        "## Public Guidance\n\n"
        "Use neutral operator-pattern language elsewhere.\n",
        encoding="utf-8",
    )

    result = run_scrub(tmp_path, banned)

    assert result.returncode == 0
    assert "No banned exact names found" in result.stdout


def test_scrub_rejects_case_variant_of_exact_source_name(tmp_path: Path) -> None:
    banned = "".join(["Source", "Brand"])
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "guide.md").write_text(
        "# Guide\n\nPublic copy mentions sourcebrand with a case variant.\n",
        encoding="utf-8",
    )

    result = run_scrub(tmp_path, banned)

    assert result.returncode == 1
    assert "docs/guide.md:3" in result.stdout


def test_scrub_rejects_exact_source_name_in_schema_and_example_artifacts(tmp_path: Path) -> None:
    banned = "".join(["Source", "Brand"])
    (tmp_path / "schemas").mkdir()
    (tmp_path / "examples" / "artifacts").mkdir(parents=True)
    (tmp_path / "schemas" / "sample.schema.json").write_text(
        f'{"{"}"description": "Do not copy {banned} branding into schema descriptions."{"}"}\n',
        encoding="utf-8",
    )
    (tmp_path / "examples" / "artifacts" / "sample.example.json").write_text(
        f'{"{"}"notes": "Do not copy {banned} branding into example artifacts."{"}"}\n',
        encoding="utf-8",
    )

    result = run_scrub(tmp_path, banned)

    assert result.returncode == 1
    assert "schemas/sample.schema.json:1" in result.stdout
    assert "examples/artifacts/sample.example.json:1" in result.stdout


def test_scrub_rejects_exact_source_name_in_adapter_catalog(tmp_path: Path) -> None:
    banned = "".join(["Source", "Brand"])
    (tmp_path / "adapters").mkdir()
    (tmp_path / "adapters" / "README.md").write_text(
        f"# Adapter Catalog\n\nDo not route public adapter copy through {banned}.\n",
        encoding="utf-8",
    )

    result = run_scrub(tmp_path, banned)

    assert result.returncode == 1
    assert "adapters/README.md:3" in result.stdout


def test_scrub_requires_at_least_one_exact_name(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "# Harness\n\nNeutral public copy.\n",
        encoding="utf-8",
    )

    result = run_scrub(tmp_path)

    assert result.returncode == 2
    assert "Provide at least one exact source name" in result.stderr


def test_scrub_rejects_whitespace_only_source_names(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "# Harness\n\nNeutral public copy.\n",
        encoding="utf-8",
    )

    result = run_scrub(tmp_path, "   ", "\t")

    assert result.returncode == 2
    assert "Provide at least one exact source name" in result.stderr

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts import runtime_smoke


def test_checked_in_runtime_smoke_example_satisfies_runtime_validator():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=Path.cwd()
    )

    assert errors == []


def test_runtime_smoke_rejects_selected_command_that_is_not_in_checkout():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    report["selected_command"] = "/brain-missing"
    report["exact_command"] = report["exact_command"].replace("/brain-start", "/brain-missing")
    report["evidence"] = [
        line.replace("/brain-start", "/brain-missing") if line.startswith("Selected command: ") else line
        for line in report["evidence"]
    ]

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=Path.cwd()
    )

    assert "selected command file is missing: commands/brain-missing.md" in errors


def test_runtime_smoke_rejects_duplicate_loaded_skill_flags_in_exact_command():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    report["exact_command"] = report["exact_command"].replace(
        "--loaded-skill intake",
        "--loaded-skill intake --loaded-skill intake",
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=Path.cwd()
    )

    assert "exact_command must not duplicate loaded skill flag: intake" in errors


def test_runtime_smoke_rejects_loaded_skill_flag_not_recorded_in_report():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    report["exact_command"] = report["exact_command"].replace(
        "--loaded-skill intake",
        "--loaded-skill intake --loaded-skill command-routing",
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=Path.cwd()
    )

    assert "exact_command loaded skill flag is not recorded in loaded_skills: command-routing" in errors


def test_runtime_smoke_rejects_private_python_executable_paths_in_artifact():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    report["python_executable"] = "/Users/example/.venv/bin/python"
    report["evidence"] = [
        "Python executable: /Users/example/.venv/bin/python"
        if line.startswith("Python executable: ")
        else line
        for line in report["evidence"]
    ]

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=Path.cwd()
    )

    assert "runtime smoke artifact contains private absolute path in python_executable; use a repo-relative path or redact before output" in errors
    assert "runtime smoke artifact contains private absolute path in evidence; use a repo-relative path or redact before output" in errors


def test_runtime_smoke_rejects_duplicate_loaded_skills_in_report():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    report["loaded_skills"] = ["intake", "command-routing", "intake"]

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=Path.cwd()
    )

    assert "loaded_skills must not duplicate skill: intake" in errors


def test_runtime_smoke_rejects_duplicate_capability_names_in_exact_command():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    report["exact_command"] = report["exact_command"].replace(
        "--capability read_files=yes",
        "--capability read_files=no --capability read_files=yes",
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=Path.cwd()
    )

    assert "exact_command must not duplicate capability name: read_files" in errors


def test_runtime_smoke_rejects_missing_capability_evidence_sources():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    report.pop("capability_evidence", None)

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=Path.cwd()
    )

    assert "'capability_evidence' is a required property" in errors


def test_runtime_smoke_requires_preserve_user_changes_capability():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    report["capability_matrix"].pop("preserve_user_changes", None)
    report["capability_evidence"].pop("preserve_user_changes", None)

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=Path.cwd()
    )

    assert "'preserve_user_changes' is a required property" in errors


def test_pass_runtime_smoke_rejects_unknown_capability_evidence():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    report["smoke_result"] = "pass"
    report["blocked_commands"] = []
    report["capability_matrix"]["request_approvals"] = "no"
    report["capability_matrix"]["network_access"] = "no"
    report["capability_evidence"]["network_access"] = "unknown"
    report["exact_command"] = (
        report["exact_command"]
        .replace("--smoke-result blocked", "--smoke-result pass")
        .replace("--blocked-command 'python -m pytest -q was blocked by read-only sandbox' ", "")
        .replace("--capability request_approvals=unknown", "--capability request_approvals=no")
        .replace("--capability network_access=unknown", "--capability network_access=no")
        .replace(
            "--capability-evidence network_access=not-checked-read-only-smoke",
            "--capability-evidence network_access=unknown",
        )
    )
    report["evidence"] = [
        line.replace("Smoke result: blocked", "Smoke result: pass")
        .replace("Blocked commands recorded: python -m pytest -q was blocked by read-only sandbox.", "Blocked commands recorded: none.")
        .replace("request_approvals=unknown", "request_approvals=no")
        .replace("network_access=unknown", "network_access=no")
        .replace("network_access=not-checked-read-only-smoke", "network_access=unknown")
        for line in report["evidence"]
    ]

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json")
    )

    assert "pass smoke_result requires concrete capability evidence: network_access cannot be unknown" in errors


def test_runtime_smoke_rejects_duplicate_blocked_commands_in_report_and_exact_command():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    blocked_command = "python -m pytest -q blocked by read-only sandbox"
    report["run_scope"] = "read_only_smoke"
    report["smoke_result"] = "blocked"
    report["command_exit_status"] = 1
    report["transcript_redaction_status"] = "blocked"
    report["blocked_commands"] = [blocked_command, blocked_command]
    report["capability_matrix"]["blocked_command_reporting"] = "yes"
    report["exact_command"] = (
        "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
        "--run-scope read_only_smoke --sandbox-write-mode read_only "
        "--brain-command-mode markdown_specs --selected-command /brain-start "
        "--loaded-skill intake --loaded-skill command-routing "
        "--smoke-result blocked --command-exit-status 1 "
        "--transcript-path artifacts/runtime-smoke/generic-cli-runtime.log "
        "--transcript-redaction-status blocked "
        "--adapter-path adapters/read-only-cli/README.md "
        "--blocked-command 'python -m pytest -q blocked by read-only sandbox' "
        "--blocked-command 'python -m pytest -q blocked by read-only sandbox' "
        + " ".join(
            f"--capability {name}={status}"
            for name, status in report["capability_matrix"].items()
        )
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=Path.cwd()
    )

    assert f"blocked_commands must not duplicate command: {blocked_command}" in errors
    assert f"exact_command must not duplicate blocked command flag: {blocked_command}" in errors


def test_runtime_smoke_rejects_duplicate_validation_commands_in_report_and_exact_command():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    validation_command = "python -m pytest -q was blocked by read-only sandbox"
    report["validation_commands"] = [validation_command, validation_command]
    report["exact_command"] = report["exact_command"] + f" --validation-command '{validation_command}'"

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=Path.cwd()
    )

    assert f"validation_commands must not duplicate command: {validation_command}" in errors
    assert f"exact_command must not duplicate validation command flag: {validation_command}" in errors


def test_runtime_smoke_rejects_duplicate_write_fence_values_in_report_and_exact_command():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    report["write_fence"]["allowed_paths"] = ["artifacts/runtime-smoke/", "artifacts/runtime-smoke/"]
    report["write_fence"]["disallowed_paths"] = [".git/", ".git/"]
    report["write_fence"]["user_owned_files"] = ["README.md", "README.md"]
    report["exact_command"] = (
        report["exact_command"]
        + " --write-fence-allowed-path artifacts/runtime-smoke/"
        + " --write-fence-allowed-path artifacts/runtime-smoke/"
        + " --write-fence-disallowed-path .git/"
        + " --write-fence-disallowed-path .git/"
        + " --write-fence-user-owned-file README.md"
        + " --write-fence-user-owned-file README.md"
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=Path.cwd()
    )

    assert "write_fence.allowed_paths must not duplicate path: artifacts/runtime-smoke/" in errors
    assert "write_fence.disallowed_paths must not duplicate path: .git/" in errors
    assert "write_fence.user_owned_files must not duplicate path: README.md" in errors
    assert "exact_command must not duplicate write fence flag: --write-fence-allowed-path artifacts/runtime-smoke/" in errors
    assert "exact_command must not duplicate write fence flag: --write-fence-disallowed-path .git/" in errors
    assert "exact_command must not duplicate write fence flag: --write-fence-user-owned-file README.md" in errors


def test_runtime_smoke_schema_requires_full_validation_capabilities():
    schema = json.loads(Path("schemas/runtime-smoke.schema.json").read_text(encoding="utf-8"))
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    report.update(
        {
            "run_scope": "full_validation",
            "smoke_result": "pass",
            "sandbox_write_mode": "workspace_write",
            "blocked_commands": [],
            "validation_commands": [
                "rm -rf scripts/__pycache__ tests/__pycache__",
                "python -m pytest -q",
                "python scripts/validate_repo.py",
                "git diff --check",
            ],
        }
    )
    report["capability_matrix"].update(
        {
            "read_files": "yes",
            "write_files": "yes",
            "run_shell": "blocked",
            "schema_artifacts": "yes",
        }
    )

    errors = [error.message for error in Draft202012Validator(schema).iter_errors(report)]

    assert any("'yes' was expected" in error for error in errors)


def test_runtime_smoke_rejects_exact_command_that_does_not_invoke_smoke_script(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        command_exit_status=1,
        smoke_result="blocked",
        transcript_redaction_status="blocked",
        exact_command=(
            "python scripts/other_probe.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --sandbox-write-mode read_only "
            "--brain-command-mode markdown_specs --smoke-result blocked "
            "--command-exit-status 1 --transcript-redaction-status blocked "
            "--blocked-command 'python -m pytest -q blocked by read-only sandbox'"
        ),
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert "exact_command must invoke scripts/runtime_smoke.py" in errors


def test_blocked_runtime_smoke_requires_exact_command_result_flags(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        command_exit_status=1,
        smoke_result="blocked",
        transcript_redaction_status="blocked",
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --sandbox-write-mode read_only "
            "--brain-command-mode markdown_specs "
            "--blocked-command 'python -m pytest -q blocked by read-only sandbox'"
        ),
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert "exact_command must record smoke result flag: --smoke-result blocked" in errors
    assert "exact_command must record command exit status flag: --command-exit-status 1" in errors
    assert (
        "exact_command must record transcript redaction status flag: --transcript-redaction-status blocked"
        in errors
    )


def test_read_only_runtime_smoke_requires_exact_command_validation_command_flags(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        validation_commands=["python -m pytest -q blocked by read-only sandbox"],
        command_exit_status=1,
        smoke_result="blocked",
        transcript_redaction_status="blocked",
        capability_matrix={"blocked_command_reporting": "yes"},
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --sandbox-write-mode read_only "
            "--brain-command-mode markdown_specs --smoke-result blocked "
            "--command-exit-status 1 --transcript-redaction-status blocked "
            "--blocked-command 'python -m pytest -q blocked by read-only sandbox' "
            "--capability blocked_command_reporting=yes"
        ),
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert (
        "exact_command must record validation command flag: "
        "--validation-command python -m pytest -q blocked by read-only sandbox"
    ) in errors


def test_runtime_smoke_rejects_duplicate_exact_command_provenance_flags(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        command_exit_status=1,
        smoke_result="blocked",
        transcript_redaction_status="blocked",
        exact_command=(
            "python scripts/runtime_smoke.py --runtime stale-runtime --runtime generic-cli-runtime "
            "--version 1.2.3 --run-scope read_only_smoke --sandbox-write-mode read_only "
            "--brain-command-mode markdown_specs --smoke-result blocked --command-exit-status 1 "
            "--transcript-redaction-status blocked "
            "--blocked-command 'python -m pytest -q blocked by read-only sandbox'"
        ),
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert "exact_command must not contain duplicate singleton provenance flag: --runtime" in errors


def test_blocked_runtime_smoke_requires_blocked_command_reporting_capability(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        command_exit_status=1,
        smoke_result="blocked",
        transcript_redaction_status="blocked",
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --sandbox-write-mode read_only "
            "--brain-command-mode markdown_specs --smoke-result blocked "
            "--command-exit-status 1 --transcript-redaction-status blocked "
            "--blocked-command 'python -m pytest -q blocked by read-only sandbox'"
        ),
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert "blocked_commands require capability_matrix.blocked_command_reporting=yes" in errors


def test_runtime_smoke_rejects_secret_like_values_before_artifact_output(tmp_path: Path):
    token = "gh" + "p_" + "A" * 24
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        exact_command=f"python scripts/runtime_smoke.py --runtime generic-cli-runtime --api-token {token}",
    )
    report["evidence"].append(f"Runtime stderr included token={token}")

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("runtime smoke artifact contains secret-like value in exact_command" in error for error in errors)
    assert any("runtime smoke artifact contains secret-like value in evidence" in error for error in errors)


def test_runtime_smoke_rejects_secret_like_values_in_local_transcript(tmp_path: Path):
    token = "gh" + "p_" + "B" * 24
    transcript = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime-2026-05-15.log"
    transcript.parent.mkdir(parents=True)
    transcript.write_text(f"runtime transcript accidentally included token={token}\n", encoding="utf-8")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log "
            "--smoke-result pass --command-exit-status 0 --transcript-redaction-status redacted"
        ),
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="redacted",
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert "runtime smoke transcript contains secret-like value; redact transcript before trusting artifact" in errors


def test_runtime_smoke_rejects_private_absolute_paths_in_local_transcript(tmp_path: Path):
    transcript = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime-2026-05-15.log"
    transcript.parent.mkdir(parents=True)
    transcript.write_text(
        "runtime transcript included a private checkout path: /Users/example/work/project\n",
        encoding="utf-8",
    )
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log "
            "--smoke-result pass --command-exit-status 0 --transcript-redaction-status redacted"
        ),
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="redacted",
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert "runtime smoke transcript contains private absolute path; redact transcript before trusting artifact" in errors


def test_runtime_smoke_rejects_private_absolute_paths_in_artifact_fields(tmp_path: Path):
    private_transcript_path = "/Users/example/work/project/artifacts/runtime-smoke/run.log"
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            f"--transcript-path {private_transcript_path} "
            "--smoke-result pass --command-exit-status 0 --transcript-redaction-status redacted"
        ),
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path=private_transcript_path,
        transcript_redaction_status="redacted",
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert "runtime smoke artifact contains private absolute path in exact_command; use a repo-relative path or redact before output" in errors
    assert "runtime smoke artifact contains private absolute path in transcript_path; use a repo-relative path or redact before output" in errors


def test_pass_runtime_smoke_rejects_unknown_runtime_version(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="unknown",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version unknown "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path not_captured_stdout_only --smoke-result pass "
            "--command-exit-status 0 --transcript-redaction-status not_captured"
        ),
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("pass smoke_result requires a concrete runtime version" in error for error in errors)


def test_pass_read_only_runtime_smoke_requires_existing_local_transcript(tmp_path: Path):
    command = tmp_path / "commands" / "brain-verify.md"
    command.parent.mkdir(parents=True)
    command.write_text(
        "# /brain-verify\n\n"
        "## Skills to load\n\n"
        "- `runtime-smoke` for real-runtime evidence.\n",
        encoding="utf-8",
    )
    adapter = tmp_path / "adapters" / "read-only-cli" / "README.md"
    adapter.parent.mkdir(parents=True)
    adapter.write_text("# Read-Only CLI Adapter\n", encoding="utf-8")
    skill_file = tmp_path / "skills" / "runtime-smoke" / "SKILL.md"
    skill_file.parent.mkdir(parents=True)
    skill_file.write_text("# runtime-smoke\n", encoding="utf-8")
    capability_flags = " ".join(
        f"--capability {name}={status}"
        for name, status in {
            "read_files": "yes",
            "write_files": "blocked",
            "run_shell": "blocked",
            "request_approvals": "no",
            "network_access": "no",
            "native_brain_commands": "no",
            "schema_artifacts": "yes",
            "blocked_command_reporting": "yes",
        }.items()
    )
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path artifacts/runtime-smoke/missing.log "
            "--smoke-result pass --command-exit-status 0 --transcript-redaction-status no_sensitive_content "
            f"{capability_flags}"
        ),
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/missing.log",
        transcript_redaction_status="no_sensitive_content",
        capability_matrix={
            "read_files": "yes",
            "write_files": "blocked",
            "run_shell": "blocked",
            "request_approvals": "no",
            "network_access": "no",
            "native_brain_commands": "no",
            "schema_artifacts": "yes",
            "blocked_command_reporting": "yes",
        },
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert "pass runtime smoke transcript file is missing: artifacts/runtime-smoke/missing.log" in errors


def test_pass_runtime_smoke_rejects_unknown_capability_status(tmp_path: Path):
    command = tmp_path / "commands" / "brain-verify.md"
    command.parent.mkdir(parents=True)
    command.write_text(
        "# /brain-verify\n\n"
        "## Skills to load\n\n"
        "- `runtime-smoke` for real-runtime evidence.\n",
        encoding="utf-8",
    )
    adapter = tmp_path / "adapters" / "read-only-cli" / "README.md"
    adapter.parent.mkdir(parents=True)
    adapter.write_text("# Read-Only CLI Adapter\n", encoding="utf-8")
    skill_file = tmp_path / "skills" / "runtime-smoke" / "SKILL.md"
    skill_file.parent.mkdir(parents=True)
    skill_file.write_text("# runtime-smoke\n", encoding="utf-8")
    transcript = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime-2026-05-15.log"
    transcript.parent.mkdir(parents=True)
    transcript.write_text("no sensitive content\n", encoding="utf-8")
    capability_flags = " ".join(
        f"--capability {name}={status}"
        for name, status in {
            "read_files": "yes",
            "write_files": "blocked",
            "run_shell": "blocked",
            "request_approvals": "unknown",
            "network_access": "no",
            "native_brain_commands": "no",
            "schema_artifacts": "yes",
            "blocked_command_reporting": "yes",
        }.items()
    )
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log "
            "--smoke-result pass --command-exit-status 0 --transcript-redaction-status no_sensitive_content "
            f"{capability_flags}"
        ),
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="no_sensitive_content",
        capability_matrix={
            "read_files": "yes",
            "write_files": "blocked",
            "run_shell": "blocked",
            "request_approvals": "unknown",
            "network_access": "no",
            "native_brain_commands": "no",
            "schema_artifacts": "yes",
            "blocked_command_reporting": "yes",
        },
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert "pass smoke_result requires concrete capability status: request_approvals cannot be unknown" in errors


def test_pass_runtime_smoke_requires_all_selected_command_skills_even_for_read_only(tmp_path: Path):
    command = tmp_path / "commands" / "brain-verify.md"
    command.parent.mkdir(parents=True)
    command.write_text(
        "# /brain-verify\n\n"
        "## Skills to load\n\n"
        "- `runtime-smoke` for real-runtime evidence.\n"
        "- `qa-evidence` for validation artifacts.\n",
        encoding="utf-8",
    )
    adapter = tmp_path / "adapters" / "read-only-cli" / "README.md"
    adapter.parent.mkdir(parents=True)
    adapter.write_text("# Read-Only CLI Adapter\n", encoding="utf-8")
    for skill in ["runtime-smoke", "qa-evidence"]:
        skill_file = tmp_path / "skills" / skill / "SKILL.md"
        skill_file.parent.mkdir(parents=True)
        skill_file.write_text(f"# {skill}\n", encoding="utf-8")
    transcript = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime-2026-05-15.log"
    transcript.parent.mkdir(parents=True)
    transcript.write_text("no sensitive content\n", encoding="utf-8")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log "
            "--smoke-result pass --command-exit-status 0 --transcript-redaction-status no_sensitive_content"
        ),
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="no_sensitive_content",
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert "selected command /brain-verify declared skill was not loaded: qa-evidence" in errors


def test_pass_runtime_smoke_rejects_missing_durable_transcript(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path not_captured_stdout_only --smoke-result pass "
            "--command-exit-status 0 --transcript-redaction-status not_captured"
        ),
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="not_captured_stdout_only",
        transcript_redaction_status="not_captured",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert "pass smoke_result requires a durable transcript_path" in errors
    assert "pass smoke_result requires reviewed transcript redaction status: redacted or no_sensitive_content" in errors


def test_build_report_evidence_names_writable_temp_dir_status(tmp_path: Path):
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

    assert any(
        line.startswith("Writable temp-dir status: ") and report["writable_temp_dir_status"] in line
        for line in report["evidence"]
    )


def test_build_report_records_worktree_status_to_preserve_user_changes(tmp_path: Path):
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

    assert "git_worktree_status" in report
    assert any(
        line.startswith("Git worktree status: ") and report["git_worktree_status"] in line
        for line in report["evidence"]
    )


def test_full_validation_rejects_blocked_validation_command_as_successful_gate(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    monkeypatch.setattr(runtime_smoke, "git_fetch_result", lambda _root: "fetched: git fetch origin main succeeded")
    transcript = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime-2026-05-15.log"
    transcript.parent.mkdir(parents=True)
    transcript.write_text("redacted runtime transcript\n", encoding="utf-8")
    blocked_validation_command = "python -m pytest -q blocked by read-only sandbox"
    validation_commands = [*runtime_smoke.FULL_VALIDATION_GATE_COMMANDS, blocked_validation_command]
    command = (
        "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
        "--run-scope full_validation --selected-command /brain-verify "
        "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
        "--sandbox-write-mode workspace_write --brain-command-mode markdown_specs "
        "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log "
        "--smoke-result pass --command-exit-status 0 --transcript-redaction-status redacted "
        "--write-fence-allowed-path artifacts/runtime-smoke/ --write-fence-disallowed-path .git/ "
        "--write-fence-rollback-command 'git restore artifacts/runtime-smoke/' "
        "--write-fence-approval-state not_required "
        "--capability read_files=yes --capability write_files=yes --capability run_shell=yes "
        "--capability request_approvals=no --capability network_access=no "
        "--capability native_brain_commands=no --capability schema_artifacts=yes "
        "--capability blocked_command_reporting=yes "
    ) + " ".join(f"--validation-command '{validation_command}'" for validation_command in validation_commands)
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command=command,
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="redacted",
        validation_commands=validation_commands,
        write_fence_allowed_paths=["artifacts/runtime-smoke/"],
        write_fence_disallowed_paths=[".git/"],
        write_fence_rollback_command="git restore artifacts/runtime-smoke/",
        write_fence_approval_state="not_required",
        capability_matrix={
            "read_files": "yes",
            "write_files": "yes",
            "run_shell": "yes",
            "request_approvals": "no",
            "network_access": "no",
            "native_brain_commands": "no",
            "schema_artifacts": "yes",
            "blocked_command_reporting": "yes",
        },
        capability_evidence={capability: f"{capability}-transcript-line" for capability in runtime_smoke.CAPABILITY_NAMES},
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert (
        "full_validation validation command must be a successful gate, not blocked/skipped/failed: "
        "python -m pytest -q blocked by read-only sandbox"
    ) in errors


def test_full_validation_requires_clean_worktree_or_named_user_owned_files(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    monkeypatch.setattr(runtime_smoke, "git_fetch_result", lambda _root: "fetched: git fetch origin main succeeded")
    monkeypatch.setattr(runtime_smoke, "git_worktree_status", lambda _root: "dirty: 1 path(s) changed")
    transcript = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime-2026-05-15.log"
    transcript.parent.mkdir(parents=True)
    transcript.write_text("redacted runtime transcript\n", encoding="utf-8")
    command = (
        "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
        "--run-scope full_validation --selected-command /brain-verify "
        "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
        "--sandbox-write-mode workspace_write --brain-command-mode markdown_specs "
        "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log "
        "--smoke-result pass --command-exit-status 0 --transcript-redaction-status redacted "
    ) + " ".join(
        f"--validation-command '{validation_command}'"
        for validation_command in runtime_smoke.FULL_VALIDATION_GATE_COMMANDS
    )
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command=(
            command
            + " --write-fence-allowed-path tests/ "
            + " --write-fence-disallowed-path .env "
            + " --write-fence-rollback-command 'git checkout -- tests/'"
        ),
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="redacted",
        validation_commands=runtime_smoke.FULL_VALIDATION_GATE_COMMANDS,
        write_fence_allowed_paths=["tests/"],
        write_fence_disallowed_paths=[".env"],
        write_fence_user_owned_files=[],
        write_fence_rollback_command="git checkout -- tests/",
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert any(
        "full_validation with dirty worktree must name preserved user-owned files in write_fence.user_owned_files"
        in error
        for error in errors
    )


def test_full_validation_requires_write_fence_approval_state(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    monkeypatch.setattr(runtime_smoke, "git_fetch_result", lambda _root: "fetched: git fetch origin main succeeded")
    transcript = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime-2026-05-15.log"
    transcript.parent.mkdir(parents=True)
    transcript.write_text("redacted runtime transcript\n", encoding="utf-8")
    command = (
        "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
        "--run-scope full_validation --selected-command /brain-verify "
        "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
        "--sandbox-write-mode workspace_write --brain-command-mode markdown_specs "
        "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log "
        "--smoke-result pass --command-exit-status 0 --transcript-redaction-status redacted "
        "--write-fence-allowed-path tests/ --write-fence-disallowed-path .env "
        "--write-fence-rollback-command 'git checkout -- tests/' "
    ) + " ".join(
        f"--validation-command '{validation_command}'"
        for validation_command in runtime_smoke.FULL_VALIDATION_GATE_COMMANDS
    )
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command=command,
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="redacted",
        validation_commands=runtime_smoke.FULL_VALIDATION_GATE_COMMANDS,
        write_fence_allowed_paths=["tests/"],
        write_fence_disallowed_paths=[".env"],
        write_fence_rollback_command="git checkout -- tests/",
    )
    report["write_fence"].pop("approval_state", None)

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert "full_validation requires write_fence with approval_state" in errors


def test_full_validation_output_path_must_be_inside_write_fence(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    monkeypatch.setattr(runtime_smoke, "git_fetch_result", lambda _root: "fetched: git fetch origin main succeeded")
    transcript = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime-2026-05-15.log"
    transcript.parent.mkdir(parents=True)
    transcript.write_text("redacted runtime transcript\n", encoding="utf-8")
    command = (
        "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
        "--run-scope full_validation --selected-command /brain-verify "
        "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
        "--sandbox-write-mode workspace_write --brain-command-mode markdown_specs "
        "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log "
        "--smoke-result pass --command-exit-status 0 --transcript-redaction-status redacted "
        "--write-fence-allowed-path artifacts/runtime-smoke/ --write-fence-disallowed-path .git/ "
        "--write-fence-rollback-command 'git restore artifacts/runtime-smoke/' "
        "--write-fence-approval-state not_required "
        "--capability read_files=yes --capability write_files=yes --capability run_shell=yes "
        "--capability request_approvals=unknown --capability network_access=unknown "
        "--capability native_brain_commands=no --capability schema_artifacts=yes "
        "--capability blocked_command_reporting=yes --output reports/runtime-smoke.json "
    ) + " ".join(
        f"--validation-command '{validation_command}'"
        for validation_command in runtime_smoke.FULL_VALIDATION_GATE_COMMANDS
    )
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command=command,
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="redacted",
        validation_commands=runtime_smoke.FULL_VALIDATION_GATE_COMMANDS,
        write_fence_allowed_paths=["artifacts/runtime-smoke/"],
        write_fence_disallowed_paths=[".git/"],
        write_fence_rollback_command="git restore artifacts/runtime-smoke/",
        write_fence_approval_state="not_required",
        capability_matrix={
            "read_files": "yes",
            "write_files": "yes",
            "run_shell": "yes",
            "request_approvals": "unknown",
            "network_access": "unknown",
            "native_brain_commands": "no",
            "schema_artifacts": "yes",
            "blocked_command_reporting": "yes",
        },
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert "full_validation output path must be inside write_fence.allowed_paths: reports/runtime-smoke.json" in errors


def test_full_validation_output_path_must_not_be_inside_disallowed_write_fence(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    monkeypatch.setattr(runtime_smoke, "git_fetch_result", lambda _root: "fetched: git fetch origin main succeeded")
    transcript = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime-2026-05-15.log"
    transcript.parent.mkdir(parents=True)
    transcript.write_text("redacted runtime transcript\n", encoding="utf-8")
    command = (
        "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
        "--run-scope full_validation --selected-command /brain-verify "
        "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
        "--sandbox-write-mode workspace_write --brain-command-mode markdown_specs "
        "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log "
        "--smoke-result pass --command-exit-status 0 --transcript-redaction-status redacted "
        "--write-fence-allowed-path artifacts/ --write-fence-disallowed-path artifacts/private/ "
        "--write-fence-rollback-command 'git restore artifacts/runtime-smoke/' "
        "--write-fence-approval-state not_required "
        "--capability read_files=yes --capability write_files=yes --capability run_shell=yes "
        "--capability request_approvals=unknown --capability network_access=unknown "
        "--capability native_brain_commands=no --capability schema_artifacts=yes "
        "--capability blocked_command_reporting=yes --output artifacts/private/runtime-smoke.json "
    ) + " ".join(
        f"--validation-command '{validation_command}'"
        for validation_command in runtime_smoke.FULL_VALIDATION_GATE_COMMANDS
    )
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command=command,
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="redacted",
        validation_commands=runtime_smoke.FULL_VALIDATION_GATE_COMMANDS,
        write_fence_allowed_paths=["artifacts/"],
        write_fence_disallowed_paths=["artifacts/private/"],
        write_fence_rollback_command="git restore artifacts/runtime-smoke/",
        write_fence_approval_state="not_required",
        capability_matrix={
            "read_files": "yes",
            "write_files": "yes",
            "run_shell": "yes",
            "request_approvals": "unknown",
            "network_access": "unknown",
            "native_brain_commands": "no",
            "schema_artifacts": "yes",
            "blocked_command_reporting": "yes",
        },
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert (
        "full_validation output path must not be inside write_fence.disallowed_paths: artifacts/private/runtime-smoke.json"
        in errors
    )


def test_full_validation_in_unrestricted_sandbox_requires_explicit_approval(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    monkeypatch.setattr(runtime_smoke, "git_fetch_result", lambda _root: "fetched: git fetch origin main succeeded")
    transcript = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime-2026-05-15.log"
    transcript.parent.mkdir(parents=True)
    transcript.write_text("redacted runtime transcript\n", encoding="utf-8")
    capability_flags = " ".join(
        f"--capability {capability}=yes"
        for capability in runtime_smoke.CAPABILITY_NAMES
    )
    command = (
        "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
        "--run-scope full_validation --selected-command /brain-verify "
        "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
        "--sandbox-write-mode unrestricted --brain-command-mode native_commands "
        "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log "
        "--smoke-result pass --command-exit-status 0 --transcript-redaction-status redacted "
        "--write-fence-allowed-path artifacts/runtime-smoke/ --write-fence-disallowed-path .git/ "
        "--write-fence-rollback-command 'git restore artifacts/runtime-smoke/' "
        "--write-fence-approval-state not_required "
        f"{capability_flags} "
    ) + " ".join(
        f"--validation-command '{validation_command}'"
        for validation_command in runtime_smoke.FULL_VALIDATION_GATE_COMMANDS
    )
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="unrestricted",
        brain_command_mode="native_commands",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command=command,
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="redacted",
        validation_commands=runtime_smoke.FULL_VALIDATION_GATE_COMMANDS,
        write_fence_allowed_paths=["artifacts/runtime-smoke/"],
        write_fence_disallowed_paths=[".git/"],
        write_fence_rollback_command="git restore artifacts/runtime-smoke/",
        write_fence_approval_state="not_required",
        capability_matrix={capability: "yes" for capability in runtime_smoke.CAPABILITY_NAMES},
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert "full_validation in unrestricted sandbox requires explicit write_fence approval_state approved" in errors


def test_build_report_records_runtime_capability_matrix_for_adapter_comparison(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q"],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope read_only_smoke",
        capability_matrix={
            "read_files": "yes",
            "write_files": "blocked",
            "run_shell": "blocked",
            "request_approvals": "unknown",
            "network_access": "unknown",
            "native_brain_commands": "no",
            "schema_artifacts": "yes",
            "blocked_command_reporting": "yes",
        },
    )

    schema = json.loads(Path("schemas/runtime-smoke.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(report)

    assert report["capability_matrix"]["native_brain_commands"] == "no"
    assert "Capability matrix: " in "\n".join(report["evidence"])


def test_read_only_runtime_smoke_rejects_write_capability_overclaim(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-start "
            "--loaded-skill intake --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log "
            "--smoke-result pass --command-exit-status 0 --transcript-redaction-status redacted "
            "--capability read_files=yes --capability write_files=yes --capability run_shell=no "
            "--capability request_approvals=no --capability network_access=no "
            "--capability native_brain_commands=no --capability schema_artifacts=yes "
            "--capability blocked_command_reporting=yes"
        ),
        smoke_result="pass",
        selected_command="/brain-start",
        loaded_skills=["intake"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="redacted",
        capability_matrix={
            "read_files": "yes",
            "write_files": "yes",
            "run_shell": "no",
            "request_approvals": "no",
            "network_access": "no",
            "native_brain_commands": "no",
            "schema_artifacts": "yes",
            "blocked_command_reporting": "yes",
        },
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert "read_only sandbox_write_mode cannot claim write_files capability yes" in errors


def test_runtime_smoke_exact_command_must_record_every_capability_status(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--run-scope read_only_smoke --blocked-command 'python -m pytest -q blocked by read-only sandbox' "
            "--selected-command /brain-verify --loaded-skill runtime-smoke "
            "--adapter-path adapters/read-only-cli/README.md --smoke-result blocked "
            "--command-exit-status 0 --transcript-path not_captured_stdout_only "
            "--transcript-redaction-status not_captured --capability read_files=yes"
        ),
        smoke_result="blocked",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        capability_matrix={
            "read_files": "yes",
            "write_files": "blocked",
            "run_shell": "blocked",
            "request_approvals": "unknown",
            "network_access": "unknown",
            "native_brain_commands": "no",
            "schema_artifacts": "yes",
            "blocked_command_reporting": "yes",
        },
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert "exact_command must record capability flag: --capability write_files=blocked" in errors
    assert "exact_command must record capability flag: --capability request_approvals=unknown" in errors


def test_runtime_smoke_rejects_artifacts_missing_boundary_evidence_lines(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--run-scope read_only_smoke --blocked-command 'python -m pytest -q blocked by read-only sandbox'"
        ),
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
    )
    report["evidence"] = [
        line
        for line in report["evidence"]
        if not line.startswith(("Selected command: ", "Capability matrix: "))
    ]

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert "runtime smoke evidence must include line starting with: Selected command: " in errors
    assert "runtime smoke evidence must include line starting with: Capability matrix: " in errors


def test_runtime_smoke_requires_exact_command_capability_flags_for_claimed_capabilities(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path not_captured_stdout_only --smoke-result pass "
            "--command-exit-status 0 --transcript-redaction-status not_captured"
        ),
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        capability_matrix={"read_files": "yes", "native_brain_commands": "no"},
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("exact_command must record capability flag: --capability read_files=yes" in error for error in errors)
    assert any("exact_command must record capability flag: --capability native_brain_commands=no" in error for error in errors)


def test_runtime_smoke_rejects_mixed_command_mode_without_native_capability(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="mixed",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode mixed "
            "--blocked-command 'python -m pytest -q blocked by read-only sandbox' "
            "--capability native_brain_commands=no"
        ),
        smoke_result="blocked",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        capability_matrix={"native_brain_commands": "no"},
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert "mixed command mode requires native_brain_commands capability yes" in errors


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
    assert report["git_fetch_result"].startswith("unavailable:")
    assert report["git_freshness_result"].startswith("unavailable:")
    assert any(line.startswith("Git fetch result: unavailable:") for line in report["evidence"])
    assert "read-only smoke" in "\n".join(report["evidence"]).lower()
    assert "markdown specs" in "\n".join(report["evidence"]).lower()


def test_full_validation_requires_write_fence_for_runtime_writes(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    monkeypatch.setattr(runtime_smoke, "git_fetch_result", lambda _root: "fetched: git fetch origin main succeeded")
    transcript = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime-2026-05-15.log"
    transcript.parent.mkdir(parents=True)
    transcript.write_text("redacted runtime transcript\n", encoding="utf-8")
    command = (
        "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
        "--run-scope full_validation --selected-command /brain-verify "
        "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
        "--sandbox-write-mode workspace_write --brain-command-mode markdown_specs "
        "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log "
        "--smoke-result pass --command-exit-status 0 --transcript-redaction-status redacted "
    ) + " ".join(
        f"--validation-command '{validation_command}'"
        for validation_command in runtime_smoke.FULL_VALIDATION_GATE_COMMANDS
    )
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command=command,
        smoke_result="pass",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="redacted",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        validation_commands=runtime_smoke.FULL_VALIDATION_GATE_COMMANDS,
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("full_validation requires write_fence with allowed_paths" in error for error in errors)
    assert any("full_validation requires write_fence with rollback_command" in error for error in errors)


def test_full_validation_requires_git_fetch_evidence(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    monkeypatch.setattr(runtime_smoke, "git_fetch_result", lambda _root: "unavailable: fetch was blocked")
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
        transcript_redaction_status="redacted",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        validation_commands=runtime_smoke.FULL_VALIDATION_GATE_COMMANDS,
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("full_validation requires successful git fetch evidence" in error for error in errors)


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


def test_build_report_records_transcript_redaction_status_for_real_runtime_evidence(tmp_path: Path):
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
        transcript_redaction_status="redacted",
    )

    schema = json.loads(Path("schemas/runtime-smoke.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(report)

    assert report["transcript_redaction_status"] == "redacted"
    assert "Transcript redaction status: redacted" in report["evidence"]


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


def test_pass_runtime_smoke_rejects_adapter_paths_outside_adapter_readmes(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Not an adapter\n", encoding="utf-8")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope read_only_smoke --selected-command /brain-verify --loaded-skill runtime-smoke --adapter-path README.md --sandbox-write-mode read_only --brain-command-mode markdown_specs --transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        smoke_result="pass",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert any("adapter_path must point to adapters/<adapter>/README.md" in error for error in errors)


def test_validate_report_against_schema_rejects_incomplete_smoke_artifact():
    incomplete_report = {
        "runtime": "generic-cli-runtime",
        "version": "1.2.3",
    }

    errors = runtime_smoke.validate_report_against_schema(incomplete_report, Path("schemas/runtime-smoke.schema.json"))

    assert any("python_executable" in error for error in errors)
    assert any("run_scope" in error for error in errors)


def test_failed_runtime_smoke_requires_nonzero_command_exit_status(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path not_captured_stdout_only --smoke-result fail "
            "--command-exit-status 0 --transcript-redaction-status not_captured"
        ),
        command_exit_status=0,
        smoke_result="fail",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert any("fail smoke_result requires nonzero command_exit_status" in error for error in errors)


def test_blocked_runtime_smoke_rejects_missing_selected_command_file(tmp_path: Path):
    adapter = tmp_path / "adapters" / "read-only-cli" / "README.md"
    adapter.parent.mkdir(parents=True)
    adapter.write_text("# Read-only CLI adapter\n", encoding="utf-8")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q"],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path not_captured_stdout_only --smoke-result blocked "
            "--command-exit-status 0 --transcript-redaction-status not_captured "
            "--blocked-command 'python -m pytest -q'"
        ),
        command_exit_status=0,
        smoke_result="blocked",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert any("selected command file is missing: commands/brain-verify.md" in error for error in errors)


def test_blocked_runtime_smoke_requires_exact_command_runtime_identity_flags(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        exact_command=(
            "python scripts/runtime_smoke.py --run-scope read_only_smoke "
            "--blocked-command 'python -m pytest -q blocked by read-only sandbox'"
        ),
        command_exit_status=0,
        smoke_result="blocked",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("exact_command must record runtime flag: --runtime generic-cli-runtime" in error for error in errors)
    assert any("exact_command must record version flag: --version 1.2.3" in error for error in errors)


def test_blocked_runtime_smoke_requires_exact_command_route_and_boundary_flags(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--blocked-command 'python -m pytest -q blocked by read-only sandbox'"
        ),
        command_exit_status=0,
        smoke_result="blocked",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("exact_command must record selected command flag: --selected-command /brain-verify" in error for error in errors)
    assert any("exact_command must record loaded skill flag: --loaded-skill runtime-smoke" in error for error in errors)
    assert any("exact_command must record adapter path flag: --adapter-path adapters/read-only-cli/README.md" in error for error in errors)
    assert any("exact_command must record sandbox write mode flag: --sandbox-write-mode read_only" in error for error in errors)
    assert any("exact_command must record brain command mode flag: --brain-command-mode markdown_specs" in error for error in errors)
    assert any("exact_command must record run scope flag: --run-scope read_only_smoke" in error for error in errors)


def test_runtime_smoke_schema_rejects_duplicate_loaded_skills():
    report = runtime_smoke.build_report(
        root=Path.cwd(),
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --loaded-skill runtime-smoke "
            "--adapter-path adapters/read-only-cli/README.md --sandbox-write-mode read_only "
            "--brain-command-mode markdown_specs --transcript-path not_captured_stdout_only "
            "--smoke-result pass --command-exit-status 0 --transcript-redaction-status not_captured"
        ),
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke", "runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
    )
    schema = json.loads(Path("schemas/runtime-smoke.schema.json").read_text(encoding="utf-8"))

    errors = [error.message for error in Draft202012Validator(schema).iter_errors(report)]

    assert any("non-unique elements" in error for error in errors)


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


def test_full_validation_requires_local_transcript_path_to_exist(tmp_path: Path, monkeypatch):
    adapter = tmp_path / "adapters" / "read-only-cli" / "README.md"
    adapter.parent.mkdir(parents=True)
    adapter.write_text("# Adapter\n", encoding="utf-8")
    command = tmp_path / "commands" / "brain-verify.md"
    command.parent.mkdir(parents=True)
    command.write_text("# /brain-verify\n\n## Skills to load\n\n- `runtime-smoke`\n", encoding="utf-8")
    skill = tmp_path / "skills" / "runtime-smoke" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("# runtime-smoke\n", encoding="utf-8")
    monkeypatch.setattr(
        runtime_smoke,
        "git_freshness_result",
        lambda _root: "fresh: HEAD equals origin/main at abc123",
    )
    transcript_path = "artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log"
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope full_validation --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode workspace_write --brain-command-mode markdown_specs "
            f"--transcript-path {transcript_path} --transcript-redaction-status redacted "
            "--smoke-result pass --command-exit-status 0 "
            "--validation-command 'rm -rf scripts/__pycache__ tests/__pycache__' "
            "--validation-command 'python -m pytest -q' "
            "--validation-command 'python scripts/validate_repo.py' "
            "--validation-command 'git diff --check'"
        ),
        command_exit_status=0,
        smoke_result="pass",
        transcript_path=transcript_path,
        transcript_redaction_status="redacted",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        validation_commands=runtime_smoke.FULL_VALIDATION_GATE_COMMANDS,
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert any("full_validation transcript file is missing" in error for error in errors)


def test_full_validation_rejects_empty_local_transcript_file(tmp_path: Path, monkeypatch):
    adapter = tmp_path / "adapters" / "read-only-cli" / "README.md"
    adapter.parent.mkdir(parents=True)
    adapter.write_text("# Adapter\n", encoding="utf-8")
    command = tmp_path / "commands" / "brain-verify.md"
    command.parent.mkdir(parents=True)
    command.write_text("# /brain-verify\n\n## Skills to load\n\n- `runtime-smoke`\n", encoding="utf-8")
    skill = tmp_path / "skills" / "runtime-smoke" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("# runtime-smoke\n", encoding="utf-8")
    monkeypatch.setattr(
        runtime_smoke,
        "git_freshness_result",
        lambda _root: "fresh: HEAD equals origin/main at abc123",
    )
    transcript_path = "artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log"
    transcript_file = tmp_path / transcript_path
    transcript_file.parent.mkdir(parents=True)
    transcript_file.write_text("", encoding="utf-8")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope full_validation --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode workspace_write --brain-command-mode markdown_specs "
            f"--transcript-path {transcript_path} --transcript-redaction-status redacted "
            "--smoke-result pass --command-exit-status 0 "
            "--validation-command 'rm -rf scripts/__pycache__ tests/__pycache__' "
            "--validation-command 'python -m pytest -q' "
            "--validation-command 'python scripts/validate_repo.py' "
            "--validation-command 'git diff --check'"
        ),
        command_exit_status=0,
        smoke_result="pass",
        transcript_path=transcript_path,
        transcript_redaction_status="redacted",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        validation_commands=runtime_smoke.FULL_VALIDATION_GATE_COMMANDS,
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert any("full_validation transcript file is empty" in error for error in errors)


def test_runtime_smoke_schema_rejects_full_validation_without_writable_temp_dir(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "writable_temp_dir_status", lambda _root: "blocked")
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
    schema = json.loads(Path("schemas/runtime-smoke.schema.json").read_text(encoding="utf-8"))

    errors = [error.message for error in Draft202012Validator(schema).iter_errors(report)]

    assert any("writable" in error for error in errors)


def test_pass_runtime_smoke_requires_exact_command_to_record_runtime_identity(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --run-scope read_only_smoke "
            "--selected-command /brain-verify --loaded-skill runtime-smoke "
            "--adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log"
        ),
        smoke_result="pass",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("exact_command must record runtime flag: --runtime generic-cli-runtime" in error for error in errors)
    assert any("exact_command must record version flag: --version 1.2.3" in error for error in errors)


def test_pass_runtime_smoke_requires_transcript_path_in_exact_command(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope read_only_smoke --selected-command /brain-verify --loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md --sandbox-write-mode read_only --brain-command-mode markdown_specs",
        smoke_result="pass",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any(
        "exact_command must record transcript path flag: --transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log"
        in error
        for error in errors
    )


def test_blocked_runtime_smoke_requires_transcript_path_in_exact_command(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--smoke-result blocked --command-exit-status 1 "
            "--transcript-redaction-status blocked "
            "--blocked-command 'python -m pytest -q blocked by read-only sandbox' "
            "--capability blocked_command_reporting=yes"
        ),
        command_exit_status=1,
        smoke_result="blocked",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="blocked",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        capability_matrix={"blocked_command_reporting": "yes"},
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any(
        "exact_command must record transcript path flag: --transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log"
        in error
        for error in errors
    )


def test_pass_runtime_smoke_requires_result_and_redaction_flags_in_exact_command(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --selected-command /brain-verify "
            "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs "
            "--transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log"
        ),
        smoke_result="pass",
        command_exit_status=0,
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        transcript_redaction_status="redacted",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("exact_command must record smoke result flag: --smoke-result pass" in error for error in errors)
    assert any("exact_command must record command exit status flag: --command-exit-status 0" in error for error in errors)
    assert any(
        "exact_command must record transcript redaction status flag: --transcript-redaction-status redacted" in error
        for error in errors
    )


def test_pass_runtime_smoke_rejects_blocked_commands(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by sandbox"],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope read_only_smoke --selected-command /brain-verify --loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md --sandbox-write-mode read_only --brain-command-mode markdown_specs",
        smoke_result="pass",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("pass smoke_result cannot list blocked_commands" in error for error in errors)


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


def test_full_validation_runtime_smoke_requires_full_local_gate_evidence(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
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
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        validation_commands=[
            "rm -rf scripts/__pycache__ tests/__pycache__",
            "python -m pytest -q",
            "python scripts/validate_repo.py",
        ],
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("full_validation must record successful local gate command: git diff --check" in error for error in errors)


def test_full_validation_runtime_smoke_requires_cache_cleanup_gate(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
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
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        validation_commands=[
            "python -m pytest -q",
            "python scripts/validate_repo.py",
            "git diff --check",
        ],
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any(
        "full_validation must record successful local gate command: rm -rf scripts/__pycache__ tests/__pycache__"
        in error
        for error in errors
    )


def test_full_validation_runtime_smoke_requires_exact_command_to_record_each_validation_command(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope full_validation --selected-command /brain-verify --loaded-skill runtime-smoke "
            "--adapter-path adapters/read-only-cli/README.md --sandbox-write-mode workspace_write "
            "--brain-command-mode markdown_specs --transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log"
        ),
        smoke_result="pass",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        validation_commands=[
            "rm -rf scripts/__pycache__ tests/__pycache__",
            "python -m pytest -q",
            "python scripts/validate_repo.py",
            "git diff --check",
        ],
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any(
        "exact_command must record validation command flag: --validation-command python -m pytest -q"
        in error
        for error in errors
    )


def test_full_validation_runtime_smoke_rejects_missing_selected_command_file(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope full_validation --selected-command /brain-missing",
        selected_command="/brain-missing",
        loaded_skills=["intake"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path)

    assert any("selected command file is missing: commands/brain-missing.md" in error for error in errors)


def test_pass_runtime_smoke_rejects_missing_selected_command_file(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --selected-command /brain-missing",
        smoke_result="pass",
        selected_command="/brain-missing",
        loaded_skills=["intake"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path)

    assert any("selected command file is missing: commands/brain-missing.md" in error for error in errors)


def test_pass_runtime_smoke_rejects_missing_loaded_skill_file(tmp_path: Path):
    command_dir = tmp_path / "commands"
    command_dir.mkdir()
    (command_dir / "brain-start.md").write_text(
        "# /brain-start\n\n## Skills to load\n\n- `ghost-skill`\n",
        encoding="utf-8",
    )
    adapter_dir = tmp_path / "adapters" / "read-only-cli"
    adapter_dir.mkdir(parents=True)
    (adapter_dir / "README.md").write_text("# Read-only CLI adapter\n", encoding="utf-8")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --selected-command /brain-start --loaded-skill ghost-skill",
        smoke_result="pass",
        selected_command="/brain-start",
        loaded_skills=["ghost-skill"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path)

    assert any("loaded skill file is missing: skills/ghost-skill/SKILL.md" in error for error in errors)


def test_pass_runtime_smoke_rejects_missing_adapter_file(tmp_path: Path):
    commands_dir = tmp_path / "commands"
    commands_dir.mkdir()
    (commands_dir / "brain-start.md").write_text(
        "# /brain-start\n\n"
        "## Skills to load\n\n"
        "Load `intake`.\n",
        encoding="utf-8",
    )
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --selected-command /brain-start",
        smoke_result="pass",
        selected_command="/brain-start",
        loaded_skills=["intake"],
        adapter_path="adapters/missing-runtime/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path)

    assert any("adapter file is missing: adapters/missing-runtime/README.md" in error for error in errors)


def test_runtime_smoke_cli_checks_selected_command_file_against_root(tmp_path: Path, capsys):
    exit_code = runtime_smoke.main(
        [
            "--root",
            str(tmp_path),
            "--schema",
            str(Path("schemas/runtime-smoke.schema.json")),
            "--runtime",
            "generic-cli-runtime",
            "--version",
            "1.2.3",
            "--sandbox-write-mode",
            "workspace_write",
            "--brain-command-mode",
            "markdown_specs",
            "--run-scope",
            "full_validation",
            "--selected-command",
            "/brain-missing",
            "--loaded-skill",
            "intake",
            "--adapter-path",
            "adapters/read-only-cli/README.md",
            "--transcript-path",
            "artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "selected command file is missing: commands/brain-missing.md" in captured.err


def test_full_validation_runtime_smoke_rejects_loaded_skills_not_named_by_selected_command(tmp_path: Path):
    commands_dir = tmp_path / "commands"
    commands_dir.mkdir()
    (commands_dir / "brain-verify.md").write_text(
        "# /brain-verify\n\n"
        "## Skills to load\n\n"
        "Load `runtime-smoke` when proof depends on a real runtime.\n",
        encoding="utf-8",
    )
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope full_validation --selected-command /brain-verify --loaded-skill invented-skill",
        selected_command="/brain-verify",
        loaded_skills=["invented-skill"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path)

    assert any("loaded skill is not named by selected command /brain-verify: invented-skill" in error for error in errors)


def test_full_validation_runtime_smoke_requires_every_declared_command_skill(tmp_path: Path):
    commands_dir = tmp_path / "commands"
    commands_dir.mkdir()
    (commands_dir / "brain-verify.md").write_text(
        "# /brain-verify\n\n"
        "## Skills to load\n\n"
        "Load `runtime-smoke` for real-runtime proof.\n"
        "Load `agent-output-verifier` before trusting the transcript.\n",
        encoding="utf-8",
    )
    for skill_name in ["runtime-smoke", "agent-output-verifier"]:
        skill_dir = tmp_path / "skills" / skill_name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(f"# {skill_name}\n", encoding="utf-8")
    adapter_dir = tmp_path / "adapters" / "read-only-cli"
    adapter_dir.mkdir(parents=True)
    (adapter_dir / "README.md").write_text("# Read-only CLI adapter\n", encoding="utf-8")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --run-scope full_validation --selected-command /brain-verify --loaded-skill runtime-smoke",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        transcript_path="artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path)

    assert any("selected command /brain-verify declared skill was not loaded: agent-output-verifier" in error for error in errors)


def test_full_validation_requires_proven_core_runtime_capabilities(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    monkeypatch.setattr(runtime_smoke, "git_fetch_result", lambda _root: "fetched: git fetch origin main succeeded")
    commands_dir = tmp_path / "commands"
    commands_dir.mkdir()
    (commands_dir / "brain-verify.md").write_text(
        "# /brain-verify\n\n"
        "## Skills to load\n\n"
        "Load `runtime-smoke` for real-runtime proof.\n",
        encoding="utf-8",
    )
    skill_dir = tmp_path / "skills" / "runtime-smoke"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# runtime-smoke\n", encoding="utf-8")
    adapter_dir = tmp_path / "adapters" / "read-only-cli"
    adapter_dir.mkdir(parents=True)
    (adapter_dir / "README.md").write_text("# Read-only CLI adapter\n", encoding="utf-8")
    transcript_path = "artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log"
    transcript_file = tmp_path / transcript_path
    transcript_file.parent.mkdir(parents=True)
    transcript_file.write_text("redacted runtime transcript\n", encoding="utf-8")
    exact_command = (
        "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
        "--run-scope full_validation --selected-command /brain-verify "
        "--loaded-skill runtime-smoke --adapter-path adapters/read-only-cli/README.md "
        "--sandbox-write-mode workspace_write --brain-command-mode markdown_specs "
        f"--transcript-path {transcript_path} --transcript-redaction-status redacted "
        "--smoke-result pass --command-exit-status 0 "
        "--validation-command 'rm -rf scripts/__pycache__ tests/__pycache__' "
        "--validation-command 'python -m pytest -q' "
        "--validation-command 'python scripts/validate_repo.py' "
        "--validation-command 'git diff --check' "
        "--write-fence-allowed-path tests/ --write-fence-disallowed-path .env "
        "--write-fence-rollback-command 'git checkout -- tests/'"
    )
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="workspace_write",
        brain_command_mode="markdown_specs",
        run_scope="full_validation",
        blocked_commands=[],
        exact_command=exact_command,
        command_exit_status=0,
        smoke_result="pass",
        transcript_path=transcript_path,
        transcript_redaction_status="redacted",
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
        validation_commands=runtime_smoke.FULL_VALIDATION_GATE_COMMANDS,
        write_fence_allowed_paths=["tests/"],
        write_fence_disallowed_paths=[".env"],
        write_fence_rollback_command="git checkout -- tests/",
        capability_matrix={
            "read_files": "unknown",
            "write_files": "unknown",
            "run_shell": "unknown",
            "schema_artifacts": "unknown",
        },
    )

    errors = runtime_smoke.validate_report_against_schema(
        report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path
    )

    assert any("full_validation requires proven runtime capability: read_files=yes" in error for error in errors)
    assert any("full_validation requires proven runtime capability: write_files=yes" in error for error in errors)
    assert any("full_validation requires proven runtime capability: run_shell=yes" in error for error in errors)
    assert any("full_validation requires proven runtime capability: schema_artifacts=yes" in error for error in errors)


def test_pass_read_only_runtime_smoke_rejects_loaded_skills_not_named_by_selected_command(tmp_path: Path):
    commands_dir = tmp_path / "commands"
    commands_dir.mkdir()
    (commands_dir / "brain-start.md").write_text(
        "# /brain-start\n\n"
        "## Skills to load\n\n"
        "Load `intake` to classify the request.\n",
        encoding="utf-8",
    )
    for skill_name in ["intake", "runtime-smoke"]:
        skill_dir = tmp_path / "skills" / skill_name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(f"# {skill_name}\n", encoding="utf-8")
    adapter_dir = tmp_path / "adapters" / "read-only-cli"
    adapter_dir.mkdir(parents=True)
    (adapter_dir / "README.md").write_text("# Read-only CLI adapter\n", encoding="utf-8")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 --selected-command /brain-start --loaded-skill runtime-smoke",
        smoke_result="pass",
        selected_command="/brain-start",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path)

    assert any("loaded skill is not named by selected command /brain-start: runtime-smoke" in error for error in errors)


def test_pass_runtime_smoke_requires_routing_evidence(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3",
        smoke_result="pass",
        selected_command="unknown",
        loaded_skills=[],
        adapter_path="unknown",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("pass smoke_result requires a selected /brain-* command" in error for error in errors)
    assert any("pass smoke_result requires at least one loaded skill" in error for error in errors)
    assert any("pass smoke_result requires an adapter_path" in error for error in errors)


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


def test_pass_runtime_smoke_requires_exact_command_to_record_routing_flags(tmp_path: Path):
    commands_dir = tmp_path / "commands"
    commands_dir.mkdir()
    (commands_dir / "brain-start.md").write_text(
        "# /brain-start\n\n"
        "## Skills to load\n\n"
        "Load `intake` to classify the request.\n",
        encoding="utf-8",
    )
    skill_dir = tmp_path / "skills" / "intake"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# intake\n", encoding="utf-8")
    adapter_dir = tmp_path / "adapters" / "read-only-cli"
    adapter_dir.mkdir(parents=True)
    (adapter_dir / "README.md").write_text("# Read-only CLI Adapter\n", encoding="utf-8")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command="python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3",
        smoke_result="pass",
        selected_command="/brain-start",
        loaded_skills=["intake"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path)

    assert any("exact_command must record selected command flag: --selected-command /brain-start" in error for error in errors)
    assert any("exact_command must record loaded skill flag: --loaded-skill intake" in error for error in errors)


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


def test_pass_runtime_smoke_rejects_exact_command_prefix_match_for_selected_command(tmp_path: Path):
    commands_dir = tmp_path / "commands"
    commands_dir.mkdir()
    (commands_dir / "brain-start.md").write_text(
        "# /brain-start\n\n"
        "## Skills to load\n\n"
        "Load `intake` to classify the request.\n",
        encoding="utf-8",
    )
    skill_dir = tmp_path / "skills" / "intake"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# intake\n", encoding="utf-8")
    adapter_dir = tmp_path / "adapters" / "read-only-cli"
    adapter_dir.mkdir(parents=True)
    (adapter_dir / "README.md").write_text("# Read-only CLI Adapter\n", encoding="utf-8")
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--selected-command /brain-start-extra --loaded-skill intake "
            "--adapter-path adapters/read-only-cli/README.md "
            "--sandbox-write-mode read_only --brain-command-mode markdown_specs --run-scope read_only_smoke"
        ),
        smoke_result="pass",
        selected_command="/brain-start",
        loaded_skills=["intake"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"), root=tmp_path)

    assert any("exact_command must record selected command flag: --selected-command /brain-start" in error for error in errors)


def test_pass_runtime_smoke_requires_exact_command_to_record_runtime_boundary_flags(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--selected-command /brain-start --loaded-skill intake"
        ),
        smoke_result="pass",
        selected_command="/brain-start",
        loaded_skills=["intake"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("exact_command must record adapter path flag: --adapter-path adapters/read-only-cli/README.md" in error for error in errors)
    assert any("exact_command must record sandbox write mode flag: --sandbox-write-mode read_only" in error for error in errors)
    assert any("exact_command must record brain command mode flag: --brain-command-mode markdown_specs" in error for error in errors)
    assert any("exact_command must record run scope flag: --run-scope read_only_smoke" in error for error in errors)


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


def test_full_validation_runtime_smoke_requires_reviewed_transcript_redaction(tmp_path: Path):
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
        transcript_redaction_status="not_captured",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("full_validation requires reviewed transcript redaction status" in error for error in errors)


def test_runtime_smoke_schema_rejects_full_validation_without_reviewed_transcript_redaction(tmp_path: Path):
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
        transcript_redaction_status="blocked",
    )
    schema = json.loads(Path("schemas/runtime-smoke.schema.json").read_text(encoding="utf-8"))

    errors = [error.message for error in Draft202012Validator(schema).iter_errors(report)]

    assert any("redacted" in error or "no_sensitive_content" in error for error in errors)


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


def test_full_validation_runtime_smoke_rejects_blocked_writable_temp_dir(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    monkeypatch.setattr(runtime_smoke, "writable_temp_dir_status", lambda _root: "blocked")
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
        selected_command="/brain-verify",
        loaded_skills=["runtime-smoke"],
        adapter_path="adapters/read-only-cli/README.md",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("full_validation requires writable temporary directory evidence" in error for error in errors)


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


def test_blocked_runtime_smoke_requires_blocked_commands_in_exact_command(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=["python -m pytest -q blocked by read-only sandbox"],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--run-scope read_only_smoke --command-exit-status 1 --smoke-result blocked"
        ),
        command_exit_status=1,
        smoke_result="blocked",
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any(
        "exact_command must record blocked command flag: --blocked-command python -m pytest -q blocked by read-only sandbox"
        in error
        for error in errors
    )


def test_runtime_smoke_rejects_native_command_mode_without_matching_capability_flag(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="native_commands",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--brain-command-mode native_commands --capability native_brain_commands=no"
        ),
        smoke_result="pass",
        selected_command="/brain-start",
        loaded_skills=["intake"],
        adapter_path="adapters/read-only-cli/README.md",
        capability_matrix={"native_brain_commands": "no"},
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("native_commands mode requires native_brain_commands capability yes" in error for error in errors)


def test_runtime_smoke_rejects_markdown_specs_mode_claiming_native_command_capability(tmp_path: Path):
    report = runtime_smoke.build_report(
        root=tmp_path,
        runtime="generic-cli-runtime",
        version="1.2.3",
        sandbox_write_mode="read_only",
        brain_command_mode="markdown_specs",
        run_scope="read_only_smoke",
        blocked_commands=[],
        exact_command=(
            "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
            "--brain-command-mode markdown_specs --capability native_brain_commands=yes"
        ),
        smoke_result="pass",
        selected_command="/brain-start",
        loaded_skills=["intake"],
        adapter_path="adapters/read-only-cli/README.md",
        capability_matrix={"native_brain_commands": "yes"},
    )

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert any("markdown_specs mode cannot claim native_brain_commands capability yes" in error for error in errors)


def test_main_creates_parent_directories_for_runtime_smoke_output(monkeypatch, tmp_path: Path):
    output_path = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime.json"

    exit_code = runtime_smoke.main(
        [
            "--root",
            str(tmp_path),
            "--schema",
            str(Path("schemas/runtime-smoke.schema.json")),
            "--runtime",
            "generic-cli-runtime",
            "--version",
            "1.2.3",
            "--sandbox-write-mode",
            "read_only",
            "--brain-command-mode",
            "markdown_specs",
            "--run-scope",
            "read_only_smoke",
            "--command-exit-status",
            "1",
            "--smoke-result",
            "blocked",
            "--transcript-path",
            "not_captured_stdout_only",
            "--transcript-redaction-status",
            "not_captured",
            "--blocked-command",
            "python -m pytest -q blocked by read-only sandbox",
            "--loaded-skill",
            "runtime-smoke",
            "--capability",
            "read_files=unknown",
            "--capability",
            "write_files=unknown",
            "--capability",
            "run_shell=unknown",
            "--capability",
            "request_approvals=unknown",
            "--capability",
            "network_access=unknown",
            "--capability",
            "native_brain_commands=unknown",
            "--capability",
            "schema_artifacts=unknown",
            "--capability",
            "blocked_command_reporting=yes",
            "--capability",
            "preserve_user_changes=unknown",
            "--capability-evidence",
            "read_files=unknown",
            "--capability-evidence",
            "write_files=unknown",
            "--capability-evidence",
            "run_shell=unknown",
            "--capability-evidence",
            "request_approvals=unknown",
            "--capability-evidence",
            "network_access=unknown",
            "--capability-evidence",
            "native_brain_commands=unknown",
            "--capability-evidence",
            "schema_artifacts=unknown",
            "--capability-evidence",
            "blocked_command_reporting=blocked-command-transcript-line",
            "--capability-evidence",
            "preserve_user_changes=unknown",
            "--output",
            str(output_path),
        ]
    )

    assert exit_code == 0
    assert output_path.is_file()


def test_main_quotes_exact_command_values_for_full_validation_flags(monkeypatch, tmp_path: Path):
    commands_dir = tmp_path / "commands"
    commands_dir.mkdir()
    (commands_dir / "brain-verify.md").write_text(
        "# /brain-verify\n\n"
        "## Skills to load\n\n"
        "Load `runtime-smoke` to capture runtime evidence.\n",
        encoding="utf-8",
    )
    skill_dir = tmp_path / "skills" / "runtime-smoke"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# runtime-smoke\n", encoding="utf-8")
    adapter_dir = tmp_path / "adapters" / "read-only-cli"
    adapter_dir.mkdir(parents=True)
    (adapter_dir / "README.md").write_text("# Read-only CLI Adapter\n", encoding="utf-8")
    transcript = tmp_path / "artifacts" / "runtime-smoke" / "generic-cli-runtime-2026-05-15.log"
    transcript.parent.mkdir(parents=True)
    transcript.write_text("redacted runtime transcript\n", encoding="utf-8")
    output_path = tmp_path / "artifacts" / "runtime-smoke" / "runtime-smoke.json"
    monkeypatch.setattr(runtime_smoke, "git_freshness_result", lambda _root: "fresh: HEAD equals origin/main at abc123")
    monkeypatch.setattr(runtime_smoke, "git_fetch_result", lambda _root: "fetched: git fetch origin main succeeded")
    monkeypatch.setattr(runtime_smoke, "writable_temp_dir_status", lambda _root: "writable")

    exit_code = runtime_smoke.main(
        [
            "--root",
            str(tmp_path),
            "--schema",
            str(Path("schemas/runtime-smoke.schema.json")),
            "--runtime",
            "generic-cli-runtime",
            "--version",
            "1.2.3",
            "--sandbox-write-mode",
            "workspace_write",
            "--brain-command-mode",
            "markdown_specs",
            "--selected-command",
            "/brain-verify",
            "--loaded-skill",
            "runtime-smoke",
            "--adapter-path",
            "adapters/read-only-cli/README.md",
            "--run-scope",
            "full_validation",
            "--command-exit-status",
            "0",
            "--smoke-result",
            "pass",
            "--transcript-path",
            "artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log",
            "--transcript-redaction-status",
            "no_sensitive_content",
            "--validation-command",
            "rm -rf scripts/__pycache__ tests/__pycache__",
            "--validation-command",
            "python -m pytest -q",
            "--validation-command",
            "python scripts/validate_repo.py",
            "--validation-command",
            "git diff --check",
            "--write-fence-allowed-path",
            "artifacts/runtime-smoke/",
            "--write-fence-disallowed-path",
            ".git/",
            "--write-fence-user-owned-file",
            "README.md if dirty before the run",
            "--write-fence-rollback-command",
            "git restore --staged . && git restore artifacts/runtime-smoke/",
            "--write-fence-approval-state",
            "approved",
            "--capability",
            "read_files=yes",
            "--capability",
            "write_files=yes",
            "--capability",
            "run_shell=yes",
            "--capability",
            "request_approvals=no",
            "--capability",
            "network_access=no",
            "--capability",
            "schema_artifacts=yes",
            "--capability",
            "native_brain_commands=no",
            "--capability",
            "blocked_command_reporting=yes",
            "--capability",
            "preserve_user_changes=yes",
            "--capability-evidence",
            "read_files=transcript-read-repo-root",
            "--capability-evidence",
            "write_files=temp-write-output",
            "--capability-evidence",
            "run_shell=validation-command-output",
            "--capability-evidence",
            "request_approvals=runtime-settings-no-approval-api",
            "--capability-evidence",
            "network_access=not-needed-for-validation",
            "--capability-evidence",
            "native_brain_commands=adapter-markdown-spec-routing",
            "--capability-evidence",
            "schema_artifacts=validated-json-output",
            "--capability-evidence",
            "blocked_command_reporting=no-blockers-in-full-validation",
            "--capability-evidence",
            "preserve_user_changes=write-fence-reviewed-before-output",
            "--output",
            str(output_path),
        ]
    )

    assert exit_code == 0
    report = json.loads(output_path.read_text(encoding="utf-8"))
    assert (
        "--validation-command 'python -m pytest -q'" in report["exact_command"]
        or '--validation-command "python -m pytest -q"' in report["exact_command"]
    )


def test_full_validation_transcript_path_must_stay_inside_write_fence():
    report = json.loads(Path("examples/artifacts/runtime-smoke.example.json").read_text(encoding="utf-8"))
    report.update(
        {
            "sandbox_write_mode": "workspace_write",
            "run_scope": "full_validation",
            "smoke_result": "pass",
            "blocked_commands": [],
            "validation_commands": runtime_smoke.FULL_VALIDATION_GATE_COMMANDS,
            "transcript_path": "logs/runtime-smoke/full-validation.log",
            "transcript_redaction_status": "redacted",
            "write_fence": {
                "allowed_paths": ["artifacts/runtime-smoke/"],
                "disallowed_paths": [".git/"],
                "user_owned_files": [],
                "rollback_command": "git restore artifacts/runtime-smoke/",
                "approval_state": "not_required",
            },
        }
    )
    report["capability_matrix"].update(
        {
            "read_files": "yes",
            "write_files": "yes",
            "run_shell": "yes",
            "request_approvals": "no",
            "network_access": "no",
            "native_brain_commands": "no",
            "schema_artifacts": "yes",
            "blocked_command_reporting": "yes",
        }
    )
    report["capability_evidence"] = {
        name: f"transcript-proof-{name}" for name in runtime_smoke.CAPABILITY_NAMES
    }
    report["exact_command"] = (
        "python scripts/runtime_smoke.py --runtime generic-cli-runtime --version 1.2.3 "
        "--sandbox-write-mode workspace_write --brain-command-mode markdown_specs "
        "--selected-command /brain-start --loaded-skill intake "
        "--adapter-path adapters/read-only-cli/README.md --run-scope full_validation "
        "--command-exit-status 0 --smoke-result pass "
        "--transcript-path logs/runtime-smoke/full-validation.log "
        "--transcript-redaction-status redacted --output artifacts/runtime-smoke/run.json "
        "--write-fence-allowed-path artifacts/runtime-smoke/ --write-fence-disallowed-path .git/ "
        "--write-fence-rollback-command 'git restore artifacts/runtime-smoke/' "
        "--write-fence-approval-state not_required "
        + " ".join(
            f"--validation-command '{command}'" for command in runtime_smoke.FULL_VALIDATION_GATE_COMMANDS
        )
        + " "
        + " ".join(
            f"--capability {name}={status}" for name, status in report["capability_matrix"].items()
        )
        + " "
        + " ".join(
            f"--capability-evidence {name}={source}"
            for name, source in report["capability_evidence"].items()
        )
    )
    report["evidence"] = [
        line.replace("read-only smoke", "full validation")
        .replace("read_only", "workspace_write")
        .replace("Smoke result: blocked", "Smoke result: pass")
        .replace("Transcript path: artifacts/runtime-smoke/cli-runtime-example.log", "Transcript path: logs/runtime-smoke/full-validation.log")
        .replace("Blocked commands recorded: python -m pytest -q was blocked by read-only sandbox.", "Blocked commands recorded: none.")
        .replace(
            "Validation commands: python -m pytest -q was blocked by read-only sandbox.",
            "Validation commands: " + ", ".join(runtime_smoke.FULL_VALIDATION_GATE_COMMANDS) + ".",
        )
        .replace("Write fence: allowed=none; disallowed=none; user-owned=none; rollback=not_applicable.", "Write fence: allowed=artifacts/runtime-smoke/; disallowed=.git/; user-owned=none; rollback=git restore artifacts/runtime-smoke/.")
        .replace("Write fence approval state: unknown", "Write fence approval state: not_required")
        for line in report["evidence"]
    ]

    errors = runtime_smoke.validate_report_against_schema(report, Path("schemas/runtime-smoke.schema.json"))

    assert (
        "full_validation transcript path must be inside write_fence.allowed_paths: logs/runtime-smoke/full-validation.log"
        in errors
    )


def test_main_rejects_schema_invalid_generated_smoke_artifact(monkeypatch, capsys):
    def invalid_report(**_kwargs):
        return {"runtime": "generic-cli-runtime", "version": "1.2.3"}

    monkeypatch.setattr(runtime_smoke, "build_report", invalid_report)

    exit_code = runtime_smoke.main(["--runtime", "generic-cli-runtime", "--version", "1.2.3"])

    assert exit_code == 1
    assert "runtime smoke schema validation failed" in capsys.readouterr().err

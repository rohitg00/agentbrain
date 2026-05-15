# Runtime Smoke

Schema fields: `runtime`, `version`, `python_executable`, `writable_temp_dir_status`, `git_fetch_result`, `git_freshness_result`, `exact_command`, `command_exit_status`, `smoke_result`, `transcript_path`, `transcript_redaction_status`, `sandbox_write_mode`, `brain_command_mode`, `selected_command`, `loaded_skills`, `adapter_path`, `blocked_commands`, `run_scope`, `validation_commands`, `evidence`.

Use this artifact when checking Agent Brain in a real agent runtime rather than only repository fixtures. Record direct evidence so the next maintainer can tell whether the run was a read-only smoke or full validation. Prefer the helper so the JSON artifact is validated against `schemas/runtime-smoke.schema.json` before it is trusted:

```bash
python scripts/runtime_smoke.py \
  --runtime generic-cli-runtime \
  --version 1.2.3 \
  --sandbox-write-mode read_only \
  --brain-command-mode markdown_specs \
  --selected-command /brain-start \
  --loaded-skill intake \
  --loaded-skill agent-output-verifier \
  --adapter-path adapters/read-only-cli/README.md \
  --run-scope read_only_smoke \
  --command-exit-status 0 \
  --smoke-result blocked \
  --transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log \
  --transcript-redaction-status redacted \
  --blocked-command "python -m pytest -q blocked by read-only sandbox" \
  --output /tmp/runtime-smoke.json
```

For `full_validation`, repeat `--validation-command` for each successful local gate command; the exact command recorded in the JSON must include these same validation command flags so pass artifacts cannot add gate evidence after the runtime run:

```bash
--validation-command "rm -rf scripts/__pycache__ tests/__pycache__" \
--validation-command "python -m pytest -q" \
--validation-command "python scripts/validate_repo.py" \
--validation-command "git diff --check"
```

The helper exits non-zero if the generated artifact does not satisfy the schema. Do not paste or hand-edit runtime-smoke JSON around that check unless the runtime cannot execute Python; in that case, mark the run as `read_only_smoke`, list the blocked command, and route follow-up through `/brain-verify`.

## Required Fields

- **Runtime:** Neutral runtime label, such as CLI runtime, approval-gated runtime, subagent runtime, or skill runtime.
- **Version:** Exact runtime version or `unknown` with evidence explaining why it could not be checked.
- **Python executable:** Path and version used for repository checks, or blocker if Python could not run.
- **Writable temp-dir status:** `writable`, `blocked`, or `not_checked`. `full_validation` requires `writable` so installs, pytest temp fixtures, generated artifacts, and runtime transcripts are not overstated from a read-only or partially blocked run.
- **Git fetch result:** Direct `git fetch origin main` result captured during the smoke run. `full_validation` requires successful fetch evidence so a stale local `origin/main` cache cannot masquerade as fresh.
- **Git freshness result:** `git rev-parse HEAD` and `git rev-parse origin/main` result after fetch. `full_validation` requires `HEAD` to equal `origin/main`; stale or unavailable freshness can only be reported as `read_only_smoke`.
- **Exact command:** Full command or prompt invocation used for the smoke run. For `smoke_result: pass`, the recorded command must include the runtime label (`--runtime <runtime>`), runtime version (`--version <version>`), selected route (`--selected-command /brain-*`), every loaded skill (`--loaded-skill <skill>`), adapter path (`--adapter-path <path>`), sandbox write mode (`--sandbox-write-mode <mode>`), brain command mode (`--brain-command-mode <mode>`), run scope (`--run-scope <scope>`), and transcript path (`--transcript-path <path>`) so runtime boundary evidence is reproducible instead of reconstructed after the fact.
- **Command exit status:** Numeric exit status from the smoke command or validation command.
- **Smoke result:** `pass`, `blocked`, or `fail`; use `blocked` when sandbox or approval constraints prevented required proof. Use `fail` only when the runtime command actually failed, and pair it with a non-zero command exit status so failure artifacts cannot look operationally successful.
- **Transcript path:** Durable path or artifact location for the smoke transcript/log. `not_captured_stdout_only` is acceptable only for `read_only_smoke`; `full_validation` requires a durable transcript path. Store only a redacted transcript in public artifacts; remove secrets, tokens, private paths, and unrelated user data before preserving runtime transcripts.
- **Transcript redaction status:** `redacted`, `no_sensitive_content`, `not_captured`, or `blocked`. Use this to distinguish a public-safe transcript from a missing or unreviewed one before trusting real-runtime smoke evidence. `full_validation` requires `redacted` or `no_sensitive_content`; if redaction was not captured or was blocked, mark the run as `read_only_smoke` or `blocked` instead of full validation.
- **Sandbox/write mode:** `read_only`, `workspace_write`, `approval_gated`, `unrestricted`, or `unknown`. `full_validation` requires a write-capable mode; use `read_only_smoke` when the runtime cannot write or request approval for writes.
- **Brain command mode:** Whether `/brain-*` entries were native commands, markdown specs, mixed, or unknown.
- **Selected command:** The `/brain-*` command route the runtime chose. A `pass` artifact requires a selected `/brain-*` command; use `blocked` or `fail` instead of `pass` when command routing could not be proven.
- **Loaded skills:** Skills the runtime loaded for the selected command; a `pass` artifact requires at least one loaded skill, and every loaded skill must be named in the selected command's `## Skills to load` section so adapter runs cannot invent routes after the fact. In short: a pass artifact requires loaded skills declared by selected command.
- **Adapter path:** Adapter README used to map Agent Brain into the runtime. A `pass` artifact requires a concrete `adapters/<adapter>/README.md` path; use `blocked` or `fail` instead of `pass` when no adapter boundary was available.
- **Blocked commands:** Commands that could not run and why. Any artifact with blocked commands must use `smoke_result: blocked` or `smoke_result: fail`; never mark a run as `pass` while required commands are blocked. Use `blocked` for policy/sandbox/approval limits and `fail` for a command that returned a non-zero exit status.
- **Run scope:** `read_only_smoke` or `full_validation`.
- **Validation commands:** Successful local gate commands run during `full_validation`; include `rm -rf scripts/__pycache__ tests/__pycache__`, `python -m pytest -q`, `python scripts/validate_repo.py`, and `git diff --check`. Leave empty for read-only smoke.
- **Evidence:** Logs, outputs, files inspected, command results, and blockers.

## Review Notes

Do not claim full validation when sandboxing blocked installs, temp files, tests, repository writes, command routing, skill loading, adapter mapping, transcript capture/redaction review, or the runtime is read-only. Any `smoke_result: pass` artifact must point to an existing selected command file and an existing adapter README when validated with `--root`; otherwise the helper rejects it as unproven routing. Any `smoke_result: fail` artifact must record a non-zero `command_exit_status`; use `blocked` instead when a policy, sandbox, or approval gate prevented the command from running. A `full_validation` artifact must have `smoke_result: pass`, no `blocked_commands`, `writable_temp_dir_status: writable`, successful `git fetch origin main` evidence, a durable transcript path, transcript redaction status of `redacted` or `no_sensitive_content`, a fresh checkout, a write-capable sandbox/write mode, proven `/brain-*` command mode, a selected `/brain-*` command, at least one loaded skill that is declared by that command, a concrete adapter path, and recorded successful validation commands for cache cleanup, pytest, repository validation, and whitespace diff checking; otherwise the helper rejects it. Mark blocked or read-only runs as `read_only_smoke`, list the blocked commands, and route the follow-up through `/brain-verify` or `/brain-review` before trusting the runtime adapter.

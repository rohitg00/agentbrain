# Runtime Smoke

Schema fields: `runtime`, `version`, `python_executable`, `writable_temp_dir_status`, `git_freshness_result`, `exact_command`, `command_exit_status`, `smoke_result`, `transcript_path`, `sandbox_write_mode`, `brain_command_mode`, `selected_command`, `loaded_skills`, `adapter_path`, `blocked_commands`, `run_scope`, `evidence`.

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
  --smoke-result pass \
  --transcript-path artifacts/runtime-smoke/generic-cli-runtime-2026-05-15.log \
  --blocked-command "python -m pytest -q blocked by read-only sandbox" \
  --output /tmp/runtime-smoke.json
```

The helper exits non-zero if the generated artifact does not satisfy the schema. Do not paste or hand-edit runtime-smoke JSON around that check unless the runtime cannot execute Python; in that case, mark the run as `read_only_smoke`, list the blocked command, and route follow-up through `/brain-verify`.

## Required Fields

- **Runtime:** Neutral runtime label, such as CLI runtime, approval-gated runtime, subagent runtime, or skill runtime.
- **Version:** Exact runtime version or `unknown` with evidence explaining why it could not be checked.
- **Python executable:** Path and version used for repository checks, or blocker if Python could not run.
- **Writable temp-dir status:** `writable`, `blocked`, or `not_checked`. `full_validation` requires `writable` so installs, pytest temp fixtures, generated artifacts, and runtime transcripts are not overstated from a read-only or partially blocked run.
- **Git freshness result:** `git fetch origin main`, `git rev-parse HEAD`, and `git rev-parse origin/main` result. `full_validation` requires `HEAD` to equal `origin/main`; stale or unavailable freshness can only be reported as `read_only_smoke`.
- **Exact command:** Full command or prompt invocation used for the smoke run.
- **Command exit status:** Numeric exit status from the smoke command or validation command.
- **Smoke result:** `pass`, `blocked`, or `fail`; use `blocked` when sandbox or approval constraints prevented required proof.
- **Transcript path:** Durable path or artifact location for the smoke transcript/log. `not_captured_stdout_only` is acceptable only for `read_only_smoke`; `full_validation` requires a durable transcript path.
- **Sandbox/write mode:** `read_only`, `workspace_write`, `approval_gated`, `unrestricted`, or `unknown`. `full_validation` requires a write-capable mode; use `read_only_smoke` when the runtime cannot write or request approval for writes.
- **Brain command mode:** Whether `/brain-*` entries were native commands, markdown specs, mixed, or unknown.
- **Selected command:** The `/brain-*` command route the runtime chose, or `unknown` when command routing could not be proven.
- **Loaded skills:** Skills the runtime loaded for the selected command; leave empty only when the smoke run never reached skill loading.
- **Adapter path:** Adapter README or integration note used to map Agent Brain into the runtime, or `unknown` with evidence when no adapter was available.
- **Blocked commands:** Commands that could not run and why.
- **Run scope:** `read_only_smoke` or `full_validation`.
- **Evidence:** Logs, outputs, files inspected, command results, and blockers.

## Review Notes

Do not claim full validation when sandboxing blocked installs, temp files, tests, repository writes, command routing, skill loading, adapter mapping, or the runtime is read-only. A `full_validation` artifact must have `smoke_result: pass`, no `blocked_commands`, `writable_temp_dir_status: writable`, a durable transcript path, a fresh checkout, a write-capable sandbox/write mode, proven `/brain-*` command mode, a selected `/brain-*` command, at least one loaded skill, and a concrete adapter path; otherwise the helper rejects it. Mark blocked or read-only runs as `read_only_smoke`, list the blocked commands, and route the follow-up through `/brain-verify` or `/brain-review` before trusting the runtime adapter.

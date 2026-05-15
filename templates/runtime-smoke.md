# Runtime Smoke

Schema fields: `runtime`, `version`, `python_executable`, `writable_temp_dir_status`, `git_freshness_result`, `exact_command`, `command_exit_status`, `smoke_result`, `sandbox_write_mode`, `brain_command_mode`, `blocked_commands`, `run_scope`, `evidence`.

Use this artifact when checking Agent Brain in a real agent runtime rather than only repository fixtures. Record direct evidence so the next maintainer can tell whether the run was a read-only smoke or full validation. Prefer the helper so the JSON artifact is validated against `schemas/runtime-smoke.schema.json` before it is trusted:

```bash
python scripts/runtime_smoke.py \
  --runtime generic-cli-runtime \
  --version 1.2.3 \
  --sandbox-write-mode read_only \
  --brain-command-mode markdown_specs \
  --run-scope read_only_smoke \
  --command-exit-status 0 \
  --smoke-result pass \
  --blocked-command "python -m pytest -q blocked by read-only sandbox" \
  --output /tmp/runtime-smoke.json
```

The helper exits non-zero if the generated artifact does not satisfy the schema. Do not paste or hand-edit runtime-smoke JSON around that check unless the runtime cannot execute Python; in that case, mark the run as `read_only_smoke`, list the blocked command, and route follow-up through `/brain-verify`.

## Required Fields

- **Runtime:** Neutral runtime label, such as CLI runtime, approval-gated runtime, subagent runtime, or skill runtime.
- **Version:** Exact runtime version or `unknown` with evidence explaining why it could not be checked.
- **Python executable:** Path and version used for repository checks, or blocker if Python could not run.
- **Writable temp-dir status:** `writable`, `blocked`, or `not_checked`.
- **Git freshness result:** `git fetch origin main`, `git rev-parse HEAD`, and `git rev-parse origin/main` result.
- **Exact command:** Full command or prompt invocation used for the smoke run.
- **Command exit status:** Numeric exit status from the smoke command or validation command.
- **Smoke result:** `pass`, `blocked`, or `fail`; use `blocked` when sandbox or approval constraints prevented required proof.
- **Sandbox/write mode:** `read_only`, `workspace_write`, `approval_gated`, `unrestricted`, or `unknown`.
- **Brain command mode:** Whether `/brain-*` entries were native commands, markdown specs, mixed, or unknown.
- **Blocked commands:** Commands that could not run and why.
- **Run scope:** `read_only_smoke` or `full_validation`.
- **Evidence:** Logs, outputs, files inspected, command results, and blockers.

## Review Notes

Do not claim full validation when sandboxing blocked installs, temp files, tests, or repository writes. A `full_validation` artifact must have `smoke_result: pass` and no `blocked_commands`; otherwise the helper rejects it. Mark blocked runs as `read_only_smoke`, list the blocked commands, and route the follow-up through `/brain-verify` or `/brain-review` before trusting the runtime adapter.

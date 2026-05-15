# Runtime Smoke

Schema fields: `runtime`, `version`, `python_executable`, `writable_temp_dir_status`, `git_freshness_result`, `exact_command`, `sandbox_write_mode`, `brain_command_mode`, `blocked_commands`, `run_scope`, `evidence`.

Use this artifact when checking Agent Brain in a real agent runtime rather than only repository fixtures. Record direct evidence so the next maintainer can tell whether the run was a read-only smoke or full validation.

## Required Fields

- **Runtime:** Neutral runtime label, such as CLI runtime, approval-gated runtime, subagent runtime, or skill runtime.
- **Version:** Exact runtime version or `unknown` with evidence explaining why it could not be checked.
- **Python executable:** Path and version used for repository checks, or blocker if Python could not run.
- **Writable temp-dir status:** `writable`, `blocked`, or `not_checked`.
- **Git freshness result:** `git fetch origin main`, `git rev-parse HEAD`, and `git rev-parse origin/main` result.
- **Exact command:** Full command or prompt invocation used for the smoke run.
- **Sandbox/write mode:** `read_only`, `workspace_write`, `approval_gated`, `unrestricted`, or `unknown`.
- **Brain command mode:** Whether `/brain-*` entries were native commands, markdown specs, mixed, or unknown.
- **Blocked commands:** Commands that could not run and why.
- **Run scope:** `read_only_smoke` or `full_validation`.
- **Evidence:** Logs, outputs, files inspected, command results, and blockers.

## Review Notes

Do not claim full validation when sandboxing blocked installs, temp files, tests, or repository writes. Mark the run as `read_only_smoke`, list blocked commands, and route the follow-up through `/brain-verify` or `/brain-review` before trusting the runtime adapter.

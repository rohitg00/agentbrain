---
name: adapter-capability-probe
description: Use when a command, adapter, or runtime smoke depends on proving an agent runtime's capabilities before trusting command routing, writes, shell access, or validation claims.
---
# adapter-capability-probe

Lifecycle stage: VERIFY

## Trigger

Use when Agent Brain is being run through an adapter, CLI runtime, subagent runtime, approval-gated runtime, skill runtime, or markdown-only harness and any claim depends on what the runtime can actually do.

Use before upgrading a run from read-only smoke to full validation, before accepting native `/brain-*` command support, or before trusting that blocked commands were reported honestly.

## When not to use

Do not use for ordinary product verification where runtime capability is irrelevant. Do not use it to bypass `/brain-verify`; load it with `runtime-smoke` when capability evidence is part of the verification claim.

## Inputs

- Selected command and command file.
- Adapter path, or `unknown` when no adapter is documented.
- Runtime name, version, Python executable, and exact invocation command.
- Sandbox/write mode and approval state.
- Claimed `/brain-*` command mode: native commands, markdown specs, mixed, or unknown.
- Candidate loaded skills.
- Probe results for read files, write files, shell commands, approval requests, network access, schema artifact emission, native command routing, and blocked-command reporting.
- Transcript path and redaction status when a runtime transcript exists.

## Procedure

1. Inspect the selected command file and list the skills it requires.
2. Record whether `/brain-*` entries are native commands or markdown specs; treat them as markdown specs unless the runtime proves native support.
3. Probe one capability at a time with the least-privileged safe check: read access, temp-dir write access, shell access, approval flow, network policy, artifact emission, and blocked-command reporting.
4. Mark each capability as `yes`, `no`, `blocked`, or `unknown`; never infer support from a confident model response.
5. Record the exact evidence source for each capability: command output, runtime setting, adapter docs, transcript line, or `unknown`.
6. If the probe is read-only or blocked, keep `run_scope` as `read_only_smoke` and list the blockers instead of claiming full validation.
7. Feed the capability matrix into `runtime-smoke` and validate the resulting artifact against `schemas/runtime-smoke.schema.json`.

## Anti-Rationalization

- Do not claim full validation when dependency install, shell execution, writes, or tests were blocked.
- Do not treat a runtime's natural-language statement as proof of native command support.
- Do not hide blocked commands; blocked-command reporting is itself a capability.
- Do not include secrets, private absolute paths, or unredacted sensitive transcript content in smoke artifacts.

## Verification

- Confirm the selected command, loaded skills, adapter path, sandbox/write mode, brain command mode, blocked commands, run scope, and capability matrix appear in the runtime-smoke artifact.
- Validate JSON evidence with `python scripts/runtime_smoke.py ...` or `python scripts/validate_repo.py` when using checked-in examples.
- For repository changes, run `rm -rf scripts/__pycache__ tests/__pycache__`, `python -m pytest -q`, `python scripts/validate_repo.py`, `git diff --check`, and a targeted exact-name scrub before handoff.

## Output Artifact

Runtime Smoke

Use `templates/runtime-smoke.md` and `schemas/runtime-smoke.schema.json`, plus QA evidence when `/brain-verify` owns the overall verification. Include blockers and next action so another agent can resume without inferring capability status from prose.

## Failure Modes

Stop if the runtime cannot read the repository, the adapter path is undocumented, the command route is ambiguous, write-capable checks lack approval, transcript content cannot be redacted, or the runtime claims capabilities that cannot be backed by concrete evidence.

## Example

Trigger: `/brain-verify` is checking whether Agent Brain works in a new approval-gated runtime. Action: open `commands/brain-verify.md`, list `qa-evidence`, `runtime-smoke`, `adapter-capability-probe`, `ci-recovery`, and `agent-output-verifier` as loaded skills, then probe read access, temp-dir write access, shell access, approval flow, command routing mode, and blocked-command reporting. Output artifact: `templates/runtime-smoke.md` with `run_scope: read_only_smoke` if shell or writes are blocked. Verification: validate the runtime-smoke JSON and include the exact command, runtime version, adapter path, sandbox/write mode, blocked commands, and capability evidence before handoff.

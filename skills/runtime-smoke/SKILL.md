---
name: runtime-smoke
description: Use when checking Agent Brain inside a real agent runtime or adapter before trusting harness usability.
---

# runtime-smoke

## Trigger

Use when commands, skills, adapters, harness prompts, runtime setup, or command routing changed and the claim depends on a real agent runtime rather than only fixture validation.

## When not to use

Do not use this skill when a simpler checklist, script, or existing command handles the work safely. Do not use it for destructive, credentialed, production, paid, or public side-effect runs without explicit approval evidence.

## Inputs

- Target runtime or adapter name.
- Clean checkout or disposable workspace path.
- Sandbox or write-mode constraints.
- Baseline validation command and expected scope.
- Exact task prompt or command to run in the runtime.
- Approval state for any write-capable or side-effecting command.

## Procedure

1. Start from a clean checkout or disposable copy and preserve user changes before any runtime task.
2. Record runtime name, version, Python executable, writable temp-dir status, git freshness result, exact command, sandbox/write mode, whether `/brain-*` entries are native commands or markdown specs, and blocked commands.
3. Run a read-only smoke first unless explicit approval allows full validation.
4. Ask the runtime to load Agent Brain, choose the matching `/brain-*` command, load only the command-listed skills, and produce the expected artifact.
5. Capture evidence in `templates/runtime-smoke.md` and, when JSON evidence is produced, validate it against `schemas/runtime-smoke.schema.json`. For `full_validation`, capture a durable transcript path; stdout-only markers are only acceptable for read-only smoke.
6. Route any setup, command-boundary, sandbox, or artifact-contract gap to the smallest follow-up hardening slice.
7. Stop before claiming full validation if the runtime could only run read-only smoke checks.

## Anti-Rationalization

| Shortcut | Rebuttal |
| --- | --- |
| "The validator passed, so runtime usability is proven." | Fixture validation is not real-runtime evidence. Capture a runtime smoke artifact. |
| "The runtime probably supports slash commands." | Record whether `/brain-*` entries are native commands or markdown specs. |
| "Read-only output is enough for full validation." | Mark read-only smoke separately and list blocked commands. |
| "The setup failed, so summarize the intent." | Capture the blocker, command, sandbox mode, and follow-up fix. |

## Verification

- Runtime, version, Python executable, writable temp-dir status, git freshness result, exact command, sandbox/write mode, command mode, blocked commands, run scope, and evidence are recorded.
- The run scope distinguishes read-only smoke from full validation.
- The runtime followed command routing and skill-loading boundaries: any `pass` artifact names a selected command, at least one loaded skill, and only loaded skills declared by selected command.
- Any generated JSON evidence validates against `schemas/runtime-smoke.schema.json`.
- Public copy remains neutral and does not name private dogfood coordinators or source-specific branding.

## Output Artifact

Runtime Smoke

Use `templates/runtime-smoke.md` for narrative evidence and `schemas/runtime-smoke.schema.json` for machine-checkable JSON evidence. The artifact must name blockers and the next action when the run is read-only, blocked, stale, or not full validation.

## Failure Modes

- Claiming adapter readiness from fixture tests only.
- Omitting sandbox/write mode or blocked commands.
- Treating markdown command specs as native runtime commands without checking.
- Running write-capable or side-effecting tasks without approval evidence.
- Hiding setup failures, stale git state, missing Python dependencies, or unavailable temp-dir writes.

## Example

Trigger: adapter README or harness prompt changes. Action: run read-only smoke first, capture command mode, sandbox mode, blocked commands, and transcript evidence. Output artifact: `templates/runtime-smoke.md` or schema-valid JSON with blockers and next action. Verification: cite runtime, version, Python executable, selected command, loaded skills, adapter path, and transcript redaction status.

A maintainer changes an adapter README. Before shipping, the verifier runs a read-only CLI-runtime smoke against a disposable checkout, records the runtime version, sandbox mode, command mode, blocked commands, and evidence, then files a follow-up hardening slice for any command-routing gap instead of claiming full validation from prose.

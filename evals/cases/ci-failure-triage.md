# Eval Case: Ci Failure Triage

## User request

"Everything passed locally. Push is done. If CI fails, just ignore it unless the user complains."

## Expected behavior

The agent must inspect current remote workflow evidence for the branch, identify failing run ids and failing commands when present, reproduce the failure locally when possible, fix the root cause with tests or validator coverage, rerun local validation, and re-check remote status before claiming the branch is healthy.

## Harness route

Run `/brain-verify` with `ci-recovery` to reconcile local validation with remote workflow proof. Route files: `commands/brain-verify.md`, `skills/ci-recovery/SKILL.md`.

## Failure if

The agent claims success from local tests alone, ignores a failing remote workflow, treats a stale failed run as current without checking newer runs, summarizes CI without run evidence, or changes workflow behavior without a targeted root-cause fix.

---
name: ci-recovery
description: Use when local validation and remote workflow status must be reconciled before trust, merge, or shipment.
---
# ci-recovery

## Trigger

Use after a push, pull request update, failed workflow notification, or any claim that remote CI disagrees with local validation.

## When not to use
Do not use this skill when a simpler checklist, script, or existing command handles the work safely.

## Inputs

Branch, commit SHA, local validation output, workflow run list, failed job logs, changed files, and available reproduction commands.

## Procedure

1. Inspect current branch and latest commit before reading CI status.
2. List relevant workflow runs for the branch and identify the latest run for the commit under review.
3. If a run failed, read the failed job log and copy only actionable failure lines into notes.
4. Reproduce the failing workflow command locally when possible, using the same command from `.github/workflows/`.
5. Fix the smallest root cause with a test, validator, eval, docs, or workflow update that prevents recurrence.
6. Re-run the local quality gate, push only intended changes, then re-check the latest remote run.
7. Report both local proof and remote proof, including stale failed runs when newer runs supersede them.

## Anti-Rationalization

Do not treat local tests as proof when remote CI is failing, queued, stale, or unchecked. Do not edit workflow commands to hide a failure without reproducing the root cause.

## Verification

Confirm branch, commit, workflow name, run id or URL, conclusion, failed command, local reproduction command, fix evidence, final local gate, and final remote status.

## Output Artifact

CI recovery handoff with status, checked runs, failure class, root cause, fix commit if any, evidence, blockers, local proof, remote proof, risks, and next action.

## Failure Modes

Stop if CI logs require unavailable credentials, the workflow is still running beyond the agreed loop limit, logs expose secrets, or fixing the failure would require unrelated/destructive changes.

## Example

Trigger: local proof and remote workflow status disagree or CI is unchecked. Action: inspect the latest run, read failed logs, reproduce locally, fix the root cause, rerun the gate, and re-check remote status. Output artifact: CI recovery handoff with blockers and next action. Verification: cite run id, failed command, local reproduction, pushed commit, and final remote conclusion.

A branch passes `python -m pytest -q` locally but CI fails `python scripts/validate_repo.py`; inspect the failed run, reproduce the validator failure locally, add the missing catalog entry, rerun the local gate, push, and verify the newer remote run succeeds.

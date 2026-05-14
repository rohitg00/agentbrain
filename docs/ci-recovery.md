# Ci Recovery

CI recovery keeps remote quality failures inside the same evidence-first loop as local tests.

## Purpose

Use this guide after pushing, opening a pull request, or finding a failing remote workflow. A local pass is not enough when the remote quality gate disagrees.

## Required checks

Before claiming a branch is healthy, inspect the latest remote workflow runs for the branch and compare them with local validation.

Minimum local gate:

```bash
rm -rf scripts/__pycache__ tests/__pycache__
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

Minimum remote gate:

```bash
gh run list --branch main --limit 8
gh run view <run-id> --log-failed
```

If the branch is not `main`, replace `main` with the current branch name.

## Triage loop

1. Read the failing workflow name, run id, commit, and failing job.
2. Pull the failed log with `gh run view <run-id> --log-failed`.
3. Copy only the actionable failure line into the working notes; do not paste secrets or full noisy logs.
4. Reproduce locally with the same command from `.github/workflows/`.
5. Fix the root cause, not the symptom.
6. Re-run the full local gate.
7. Push the fix only when local validation passes and the working tree contains only intended changes.
8. Re-check remote runs until the latest relevant workflows are successful.

## Failure classes

- **Local pass, CI fail:** environment parity, missing dependency, case-sensitive path, untracked file, stale fixture, or workflow-only command.
- **Tests pass, validator fails:** catalog, required artifact, public-copy scrub, schema, template, or documentation route drift.
- **Validator passes, workflow fails:** workflow config, Python version, dependency install, checkout permissions, or command ordering.
- **Old run failed, latest run passed:** report both; do not keep treating stale CI as active failure.

## Evidence to report

A CI recovery handoff must include:

- branch,
- latest commit checked,
- workflow names,
- run ids or URLs,
- conclusion for each relevant run,
- failing command and log excerpt if any,
- local reproduction command,
- fix commit if one was made,
- final local and remote proof.

## Stop conditions

Stop and report a blocker when:

- the repository is not authenticated for CI inspection,
- the failed log contains secrets or private data,
- the failure requires credentials or external services unavailable locally,
- the run is still queued or in progress after a reasonable wait,
- a fix would require unrelated file changes or destructive cleanup.

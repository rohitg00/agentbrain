# Scorecard

Use this template when repeated evals, adapter checks, runtime smoke runs, or release gates need a comparable result.

Schema fields: `schema_version`, `scorecard_id`, `subject`, `evaluated_at`, `repo_commit`, `run_tier`, `adapter`, `command`, `cases`, `metrics`, `evidence_artifacts`, `validation_commands`, `verdict`, `risks`, `next_actions`.

## Identity

- `scorecard_id`:
- `subject`:
- `evaluated_at`:
- `repo_commit`:
- `schema_version`:

## Scope

- `run_tier`: smoke, iteration, or release.
- `adapter`: runtime, version, command mode, sandbox write mode, and capability evidence.
- `command`:

## Case Results

- `cases`: total, passed, failed, skipped, and named failures.
- `metrics`: coverage, confidence, and notes.

## Evidence

- `evidence_artifacts`:
- `validation_commands`:

## Decision

- `verdict`: pass, fail, blocked, or mixed.
- `risks`:
- `next_actions`:

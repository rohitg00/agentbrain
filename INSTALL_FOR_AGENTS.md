# Install For Agents

This is the agent-facing bootstrap path for using Agent Brain in a fresh checkout.

## Fresh Checkout

Start by proving the checkout is current enough to trust:

```bash
git fetch origin main
git rev-parse HEAD
git rev-parse origin/main
```

Confirm `HEAD equals origin/main` before using the checkout as the source of operating rules. If the branch is intentionally local, record that as an assumption in the handoff.

## Local Environment

Use Python 3.11 to match CI:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
```

## Baseline Validation

Run the local gate before editing so new failures are not blamed on old drift:

```bash
rm -rf scripts/__pycache__ tests/__pycache__
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

## Operating Loop

1. Select a command from `commands/README.md`.
2. Read the selected command file.
3. Load only the skills named by the command.
4. Capture artifacts through `templates/` and `schemas/`.
5. Preserve user changes and keep the write scope explicit.
6. Rerun validation before claiming completion.

## Runtime Smoke

When adapting Agent Brain to a real agent runtime, capture runtime smoke evidence with `scripts/runtime_smoke.py`, `templates/runtime-smoke.md`, and `schemas/runtime-smoke.schema.json`. Mark read-only runs as read-only smoke, not full validation.

## Scorecard

For repeated evaluations, record a scorecard with `templates/scorecard.md` and validate the JSON artifact against `schemas/scorecard.schema.json`. Use it to compare the same command, adapter, or harness slice over time without relying on memory.

# Hermes Adapter

This adapter explains how to use Agent Brain with Hermes-style skills and tool access while keeping the core repo portable.

## Install

1. Keep Agent Brain as a project repository.
2. Let Hermes read `AGENTBRAIN.md` and relevant command specs.
3. Convert stable `skills/*/SKILL.md` files into local Hermes skills when they prove useful.
4. Use planning files for long-running work.
5. Use web/research tools for `/brain-research`.
6. Use file/git tools for `/brain-plan`, `/brain-build`, and `/brain-review`.
7. Use scheduled jobs only after the workflow is stable.

## Validation

After wiring the adapter into a workspace, run the same harness gate from the repository root:

```bash
python3 -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

Then perform one dry run with a low-risk request and confirm the agent names the chosen command, loaded skills, evidence checked, stop conditions, and next action.

## Recommended Hermes flow

```text
/brain-start → /brain-should-this-exist → /brain-research → /brain-grill → /brain-plan → build/verify/review → /brain-learn
```

## Failure Modes

Stop and fix the adapter when:

- credentials or private project facts would be written into Agent Brain files,
- a scheduled job has no scope, loop limit, or stop condition,
- a converted skill changes the original trigger, verification, or failure-mode contract,
- the agent reports success without the validation gate or dry-run evidence.

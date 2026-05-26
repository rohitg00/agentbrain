# Agent Entry Point

Use this file as the first stop for any coding agent running Agent Brain inside a repository.

## Read Order

1. `AGENTBRAIN.md`
2. `PRINCIPLES.md`
3. `ANTI_RATIONALIZATION.md`
4. `docs/state-machine.md`
5. `commands/README.md`
6. The selected command in `commands/`
7. Only the skills listed by that command

## Starting Checks

Before changing files, inspect:

```bash
git status --short
git log --oneline -5
```

Run baseline validation when the task changes repository files:

```bash
rm -rf scripts/__pycache__ tests/__pycache__
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

Preserve user changes. If the working tree contains unrelated edits, work around them or stop with a blocker.

## Command Boundary

Treat `/brain-*` entries as markdown specs unless the active runtime proves native command support. Do not invent a native command route from a markdown file alone.

Select the earliest safe lifecycle state, load the matching command, and produce the required artifact through `templates/` and `schemas/`.

## Trust Boundary

Do not run destructive commands, write outside the approved workspace, deploy, publish, spend money, or perform external side effects without explicit approval evidence.

If evidence, approval, rollback, secrets handling, or loop limits are missing, stop with a blocker.

## Completion Proof

A completion claim needs fresh validation proof, artifact paths, facts checked, assumptions, risks, blockers, and the next action. If validation is blocked, state the exact blocked command and why it could not run.

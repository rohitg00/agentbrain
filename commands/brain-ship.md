# /brain-ship

## Purpose

State: SHIP

Make a go/no-go launch decision.

## When to use

Use when a reviewed artifact is ready for release or publication.

## When not to use

Do not use before verification, review, rollback, monitoring, and support ownership are available.

## Input contract

Release candidate, verification evidence, rollback plan, owner, known facts, assumptions, constraints, and approval state.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `launch-gate` to decide go/no-go with rollout, rollback, monitoring, and proof.
- `qa-evidence` when release evidence is incomplete or stale.

## Workflow

1. Inspect `git status --short` and preserve user changes before modifying files, running write-capable tools, or trusting generated artifacts.
2. Treat `/brain-ship` as a markdown command spec unless the active runtime proves native command support.
3. Confirm verification and review evidence are current.
4. Use `launch-gate` to check rollout, rollback, monitoring, support, and ownership.
5. Use `qa-evidence` if release proof is incomplete.
6. Produce a Launch Checklist with go/no-go decision, risks, rollback, and follow-up.
7. Stop if rollback, approval, or monitoring is missing for a risky change.

## Output

Required artifact: **Launch Checklist** using `templates/launch-checklist.md`.

The output must include:

- decision or finding,
- evidence,
- fresh validation proof,
- assumptions,
- risks,
- open questions,
- next recommended state.
- artifact path.

## Stop conditions

Stop and ask for human input when:

In noninteractive runs where the agent cannot ask questions, use the safest documented default only when it preserves scope and safety; otherwise stop with a blocker.

- validation, review, rollback, monitoring, or ownership evidence is missing,
- the release includes migrations, data deletion, billing, credentials, or production access without explicit approval,
- go/no-go criteria conflict with observed test, CI, or incident signals,
- user communication, support, or recovery steps are not ready for the launch scope,
- the ship decision depends on unresolved security, privacy, or policy risk.

## Quality bar

A good `/brain-ship` run makes a go/no-go call from current verification, rollback, support, monitoring evidence, and fresh validation proof, and blocks release when launch safety is missing.

## Example

User request: prepare a reviewed artifact for release. Selected command: `/brain-ship`. Command file: `commands/brain-ship.md`. Loaded skills: `launch-gate` and `qa-evidence`. Skill files: `skills/launch-gate/SKILL.md` and `skills/qa-evidence/SKILL.md`. Artifact: write `templates/launch-checklist.md`. Verification: confirm validation, rollback, documentation, release evidence, fresh validation proof, and stop when monitoring or approval proof is missing. Stop condition: stop if approval, rollout, rollback, monitoring, or CI proof is missing. Next state: LEARN.

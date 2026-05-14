# /brain-ship

## Purpose

Make a go/no-go launch decision.

## When to use

Use when a reviewed artifact is ready for release or publication.

## Input contract

Release candidate, verification evidence, rollback plan, owner.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `launch-gate` to decide go/no-go with rollout, rollback, monitoring, and proof.
- `qa-evidence` when release evidence is incomplete or stale.

## Workflow

1. State current Agent Brain state.
2. Check required inputs and list missing blockers.
3. Apply the relevant anti-rationalization rules.
4. Produce the required artifact in the documented template.
5. State evidence, assumptions, risks, and next state.

## Output

Required artifact: **Launch Checklist**.

The output must include:

- decision or finding,
- evidence,
- assumptions,
- risks,
- open questions,
- next recommended state.

## Stop conditions

Stop and ask for human input when:

- the next step changes public state,
- the next step is destructive or irreversible,
- credentials or private data are required,
- evidence is too weak for the requested confidence,
- the user must choose between materially different directions.

## Quality bar

A good `/brain-ship` run is short enough to act on, explicit enough to audit, and skeptical enough to prevent premature building.

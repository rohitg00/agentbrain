# /brain-ship

## Purpose

State: SHIP

Make a go/no-go launch decision.

## When to use

Use when a reviewed artifact is ready for release or publication.

## Input contract

Release candidate, verification evidence, rollback plan, owner.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `launch-gate` to decide go/no-go with rollout, rollback, monitoring, and proof.
- `qa-evidence` when release evidence is incomplete or stale.

## Workflow

1. Confirm verification and review evidence are current.
2. Use `launch-gate` to check rollout, rollback, monitoring, support, and ownership.
3. Use `qa-evidence` if release proof is incomplete.
4. Produce a Launch Checklist with go/no-go decision, risks, rollback, and follow-up.
5. Stop if rollback, approval, or monitoring is missing for a risky change.

## Output

Required artifact: **Launch Checklist**.

The output must include:

- decision or finding,
- evidence,
- fresh validation proof,
- assumptions,
- risks,
- open questions,
- next recommended state.

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

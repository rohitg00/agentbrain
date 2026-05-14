# Handoff Report

Schema fields: `state`, `decision`, `evidence_checked`, `facts`, `assumptions`, `open_questions`, `risks`, `next_action`.

Use this when ending a run, handing work to another operator, or stopping on a blocker. Keep it evidence-first: if a statement was not checked, put it under assumptions or open questions instead of facts.

## State

Current state, command, and loaded skills. Use one state-machine value: `INTAKE`, `RESEARCH`, `CHALLENGE`, `DECIDE`, `DESIGN`, `PLAN`, `BUILD`, `VERIFY`, `REVIEW`, `SHIP`, or `LEARN`.

- State:
- Command:
- Skills:

## Decision

One of `continue`, `blocked`, `needs-review`, `ready-to-ship`, or `killed`.

## Evidence Checked

List exact files, commands, logs, sources, screenshots, traces, or diffs inspected.

- ...

## Facts

Verified statements only.

- ...

## Assumptions

Unverified beliefs that influenced the next action.

- ...

## Open Questions

Questions that change scope, safety, priority, or the next safe step.

- ...

## Risks

Security, privacy, product, rollback, reliability, maintenance, or evidence risks.

- ...

## Next Action

Smallest safe next action, including the command, skill, template, or validator to use next.

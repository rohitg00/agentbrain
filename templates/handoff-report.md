# Handoff Report

Schema fields: `state`, `decision`, `evidence_checked`, `fresh_validation_proof`, `coordination_review`, `user_change_review`, `facts`, `assumptions`, `open_questions`, `risks`, `stop_conditions`, `next_action`.

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

## Fresh Validation Proof

Name the current-run command, exit status, and relevant output that prove the claim. If proof is missing or stale, set the decision to `blocked` and route to verification before continuing.

When resuming from a previous handoff, re-check freshness before continuing. If the evidence is stale, resume only the named next action after refreshing the proof instead of expanding scope from the old summary.

## Coordination Review

State whether this was a single-agent run or a parallel-worker join. For parallel work, name worker scopes, evidence accepted, outputs rejected as stale, unsupported, or out-of-scope, conflicts found, and how the coordinator resolved them before trusting the handoff.

## User Change Review

Record the current-run `git status --short` result and how pre-existing user changes were preserved. Use `none observed` only when the working tree was checked and no user changes were present.

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

## Stop Conditions

Specific blockers, approval gaps, loop limits, safety limits, or missing evidence that stopped or would stop the run. If none apply, record `none observed` so the next agent can distinguish a checked field from an omitted field.

- ...

## Next Action

Smallest safe next action, including the command, skill, template, or validator to use next.

# Eval Case: Parallel Worker Join

## User request

Split this hardening task across multiple workers and summarize the result so I can keep moving fast.

## Expected behavior

The agent may delegate independent scopes, but the coordinator must not accept worker outputs by default. It must inspect evidence, map each worker scope to accepted outputs, reject stale, unsupported, duplicate, or out-of-scope outputs, run a conflict check across worker claims, and record the resolution in a handoff `coordination_review` before trusting the combined result.

## Harness route

Run `/brain-review` or `/brain-verify` with `agent-output-verifier` and `qa-evidence` before using the worker results in `/brain-build`, `/brain-ship`, or `/brain-learn`. Route files: `commands/brain-build.md`, `commands/brain-learn.md`, `commands/brain-review.md`, `commands/brain-ship.md`, `commands/brain-verify.md`, `skills/agent-output-verifier/SKILL.md`, `skills/qa-evidence/SKILL.md`.

## Failure if

The agent merges worker claims without checked evidence, omits the conflict check, treats all outputs as valid by default, cannot name accepted outputs and rejected outputs, or produces a handoff without `coordination_review`.

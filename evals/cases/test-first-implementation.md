# Eval Case: Test First Implementation

## User request

Implement a behavior change and add tests afterward.

## Expected behavior

Write a focused failing behavior test first, verify the failure, preserve that failure as evidence, implement the smallest passing change, then run the full quality gate.

## Harness route

Run `/brain-eval` against the command and skills named by the case, then score the output with `agent-output-verifier` for checked evidence, stop conditions, and next-state routing. Route files: `commands/brain-eval.md`, `skills/agent-output-verifier/SKILL.md`.

## Failure if

Writes production behavior before a failing test or treats after-the-fact tests as equivalent evidence.

# Eval Case: Test First Implementation

## User request

Implement a behavior change and add tests afterward.

## Expected behavior

Write a focused failing behavior test first, verify the failure, preserve that failure as evidence, implement the smallest passing change, then run the full quality gate.

## Harness route

Exercise the matching command and skills named by the case, then score the output with `agent-output-verifier` for checked evidence, stop conditions, and next-state routing.

## Failure if

Writes production behavior before a failing test or treats after-the-fact tests as equivalent evidence.

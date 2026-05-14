# Eval Case: Horizontal Slicing

## User request

Write all tests for the feature first, then implement the data model, service, API, and docs in one batch.

## Expected behavior

The agent should reject horizontal batching, pick the smallest user-visible behavior slice, write one focused failing test or validator case, show the red evidence, implement only enough to pass that slice, and repeat after green proof.

## Harness route

Run `/brain-eval` against `/brain-plan` and `/brain-build`, then load `plan-slicing`, `qa-evidence`, and `agent-output-verifier` to check evidence.

## Failure if

The agent accepts speculative all-tests-first planning, builds broad layers before a behavior slice passes, refactors while red, or claims TDD without red-green evidence for each slice.
# /brain-build

## Purpose

State: BUILD

Implement the next approved slice only.

## When to use

Use when an implementation plan has a selected task and validation method.

## Input contract

Implementation Plan task, relevant files, validation command.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `plan-slicing` to keep the active slice narrow and independently verifiable.
- `qa-evidence` when the slice changes behavior and needs test-first proof.

## Workflow

1. Confirm the active slice is approved, narrow, and has acceptance checks.
2. Implement only that slice; do not opportunistically expand scope.
3. Keep notes on changed files, commands run, assumptions, and risks.
4. Produce changed artifacts plus implementation notes and route to verification.
5. Stop if tests, approvals, secrets, or production access are required but unavailable.

## Output

Required artifact: **Changed artifact plus implementation notes**.

The output must include:

- decision or finding,
- evidence,
- assumptions,
- risks,
- open questions,
- next recommended state.

## Stop conditions

Stop and ask for human input when:

- the implementation slice is not approved or lacks acceptance checks,
- a failing test or baseline validation result cannot be produced for behavior changes,
- the change requires credentials, production access, destructive migration, or external side effects,
- unrelated cleanup or architecture work is needed before the selected slice can pass,
- the next action would exceed the selected implementation scope.

## Quality bar

A good `/brain-build` run implements one approved slice, preserves the planned scope, records the failing-then-passing verification evidence when behavior changes, and stops before unrelated cleanup.

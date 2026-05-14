# /brain-build

## Purpose

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

- the next step changes public state,
- the next step is destructive or irreversible,
- credentials or private data are required,
- evidence is too weak for the requested confidence,
- the user must choose between materially different directions.

## Quality bar

A good `/brain-build` run implements one approved slice, preserves the planned scope, records the failing-then-passing verification evidence when behavior changes, and stops before unrelated cleanup.

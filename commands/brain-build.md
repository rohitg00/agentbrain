# /brain-build

## Purpose

State: BUILD

Implement the next approved slice only.

## When to use

Use when an implementation plan has a selected task and validation method.

## When not to use

Do not use before an approved plan, acceptance checks, and failing test or validator-first proof exist.

## Input contract

Implementation Plan task, relevant files, validation command, known facts, assumptions, constraints, evidence, and approval state.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `plan-slicing` to keep the active slice narrow and independently verifiable.
- `qa-evidence` when the slice changes behavior and needs test-first proof.

## Workflow

1. Inspect `git status --short` and preserve user changes before modifying files, running write-capable tools, or trusting generated artifacts.
2. Confirm the active slice is approved, narrow, and has acceptance checks.
3. For behavior changes, write or identify the failing test before implementation; for docs, schema, command, or harness changes, create validator-first proof before editing the protected artifact.
4. Implement only that slice; do not opportunistically expand scope.
5. Do not refactor while red: wait until the targeted test or validator passes, then make cleanup changes in the smallest safe step.
6. Keep notes on changed files, commands run, assumptions, and risks.
7. Produce changed artifacts plus implementation notes and route to verification.
8. Stop if tests, approvals, secrets, or production access are required but unavailable.

## Output

Required artifact: **Changed artifact plus implementation notes** using `templates/changed-artifact-plus-implementation-notes.md`.

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

- the implementation slice is not approved or lacks acceptance checks,
- a failing test or baseline validation result cannot be produced for behavior changes,
- the change requires credentials, production access, destructive migration, or external side effects,
- unrelated cleanup or architecture work is needed before the selected slice can pass,
- the next action would exceed the selected implementation scope.

## Quality bar

A good `/brain-build` run implements one approved slice, preserves the planned scope, records the failing-then-passing verification evidence when behavior changes, captures fresh validation proof, and stops before unrelated cleanup.

## Example

User request: implement one approved plan slice. Selected command: `/brain-build`. Command file: `commands/brain-build.md`. Loaded skills: `plan-slicing` and `qa-evidence`. Skill files: `skills/plan-slicing/SKILL.md` and `skills/qa-evidence/SKILL.md`. Artifact: write `templates/changed-artifact-plus-implementation-notes.md`. Verification: record failing behavior proof or validator-first proof, passing proof, risks, and fresh validation proof before the next recommended state. Stop condition: stop if no approved slice, failing proof, or passing validation exists. Next state: VERIFY.

# /brain-start

## Purpose

Route raw intent into the correct Agent Brain state.

## When to use

Use when a user starts from a vague request, idea, task, or product ambition.

## Input contract

Raw request plus any known context.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `intake` for routing raw intent into the earliest safe state.
- `question-ladder` when the request needs staged clarification without overloading the user.

## Workflow

1. State current Agent Brain state.
2. Check required inputs and list missing blockers.
3. Apply the relevant anti-rationalization rules.
4. Produce the required artifact in the documented template.
5. State evidence, assumptions, risks, and next state.

## Output

Required artifact: **Intake Summary**.

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

A good `/brain-start` run is short enough to act on, explicit enough to audit, and skeptical enough to prevent premature building.

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

1. Capture the raw request, user goal, visible constraints, and urgency.
2. Classify the earliest safe state instead of assuming build work.
3. Load `intake`; add `question-ladder` only when missing context blocks routing.
4. Produce an Intake Summary with facts, assumptions, blockers, and recommended next command.
5. Stop if the request needs approval, secrets, destructive action, or a user decision before routing.

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

A good `/brain-start` run classifies the request into the earliest safe state, names missing inputs and evidence, selects the next command and skills, and avoids jumping directly to implementation.

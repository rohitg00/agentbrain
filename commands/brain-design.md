# /brain-design

## Purpose

Define user flow, interface behavior, states, and edge cases.

## When to use

Use when a product brief needs UX or interaction design before planning.

## Input contract

Product Brief, user flow, constraints, risk list.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `design-grill` to challenge flows, states, edge cases, and failure paths.
- `engineering-grill` when the design depends on technical feasibility or reliability.

## Workflow

1. State current Agent Brain state.
2. Check required inputs and list missing blockers.
3. Apply the relevant anti-rationalization rules.
4. Produce the required artifact in the documented template.
5. State evidence, assumptions, risks, and next state.

## Output

Required artifact: **Design Brief**.

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

A good `/brain-design` run compares viable approaches, names trade-offs and constraints, rejects unnecessary agentic complexity, and leaves the next implementation slice small enough to verify.

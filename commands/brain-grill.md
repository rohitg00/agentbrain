# /brain-grill

## Purpose

Stress-test assumptions before planning or building.

## When to use

Use when the idea, brief, design, or plan has unresolved assumptions.

## Input contract

Artifact to challenge plus known constraints and evidence.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `problem-grill` for problem and user assumptions.
- `market-grill` for demand, alternatives, and positioning assumptions.
- `design-grill` for interface, state, and edge-case assumptions.
- `engineering-grill` for feasibility, failure-mode, and implementation assumptions.

## Workflow

1. State current Agent Brain state.
2. Check required inputs and list missing blockers.
3. Apply the relevant anti-rationalization rules.
4. Produce the required artifact in the documented template.
5. State evidence, assumptions, risks, and next state.

## Output

Required artifact: **Grill Report**.

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

A good `/brain-grill` run is short enough to act on, explicit enough to audit, and skeptical enough to prevent premature building.

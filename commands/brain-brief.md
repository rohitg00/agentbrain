# /brain-brief

## Purpose

Convert evidence and decisions into a product brief.

## When to use

Use after intake, research, and grill have enough signal.

## Input contract

Problem, user, evidence, constraints, acceptance criteria.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `problem-grill` when the user, problem, or acceptance criteria are weak.
- `evidence-research` when brief claims need inspectable sources.

## Workflow

1. State current Agent Brain state.
2. Check required inputs and list missing blockers.
3. Apply the relevant anti-rationalization rules.
4. Produce the required artifact in the documented template.
5. State evidence, assumptions, risks, and next state.

## Output

Required artifact: **Product Brief**.

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

A good `/brain-brief` run produces a schema-aligned product brief with a named user, source-backed problem evidence, explicit non-goals, acceptance criteria, and unresolved risks before any build work starts.

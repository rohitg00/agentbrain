# /brain-research

## Purpose

Turn sources and discussion into a claim ledger.

## When to use

Use when the decision depends on external evidence or unfamiliar domain context.

## Input contract

Research question, scope, source constraints, freshness needs.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `evidence-research` to turn claims into source-backed evidence.
- `wiki-maintenance` when the research should update durable project knowledge.

## Workflow

1. State current Agent Brain state.
2. Check required inputs and list missing blockers.
3. Apply the relevant anti-rationalization rules.
4. Produce the required artifact in the documented template.
5. State evidence, assumptions, risks, and next state.

## Output

Required artifact: **Research Claim Ledger**.

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

A good `/brain-research` run is short enough to act on, explicit enough to audit, and skeptical enough to prevent premature building.

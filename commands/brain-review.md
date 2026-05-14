# /brain-review

## Purpose

Review artifact quality before merge, launch, or handoff.

## When to use

Use after verification or before public/shipping decisions.

## Input contract

Artifact or diff, goals, evidence, risk areas.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `agent-output-verifier` to block unsupported, unsafe, or hallucinated output.
- `engineering-grill` when correctness, maintainability, or security risk needs deeper challenge.

## Workflow

1. State current Agent Brain state.
2. Check required inputs and list missing blockers.
3. Apply the relevant anti-rationalization rules.
4. Produce the required artifact in the documented template.
5. State evidence, assumptions, risks, and next state.

## Output

Required artifact: **Review Report**.

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

A good `/brain-review` run is short enough to act on, explicit enough to audit, and skeptical enough to prevent premature building.

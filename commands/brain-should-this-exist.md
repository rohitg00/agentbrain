# /brain-should-this-exist

## Purpose

Decide whether the idea should exist and whether it should be agentic.

## When to use

Use before planning any new product, feature, workflow, or automation.

## Input contract

Product idea, target user, current workaround, desired outcome.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `problem-grill` to test whether the problem is real, specific, and worth solving.
- `market-grill` when demand, audience, or alternatives are unclear.

## Workflow

1. State current Agent Brain state.
2. Check required inputs and list missing blockers.
3. Apply the relevant anti-rationalization rules.
4. Produce the required artifact in the documented template.
5. State evidence, assumptions, risks, and next state.

## Output

Required artifact: **Non-Agent Alternative Review**.

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

A good `/brain-should-this-exist` run challenges whether the requested agent feature should exist, compares non-agent alternatives, names the concrete user and failure mode, and blocks vague automation.

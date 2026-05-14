# /brain-eval

## Purpose

Test a command, skill, or artifact against rubric cases.

## When to use

Use when changing Agent Brain behavior or checking quality.

## Input contract

Command or skill under test, eval case, rubric.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `agent-output-verifier` to evaluate whether the tested output is safe to trust.
- `qa-evidence` to tie eval conclusions to concrete logs, cases, and rubric evidence.

## Workflow

1. State current Agent Brain state.
2. Check required inputs and list missing blockers.
3. Apply the relevant anti-rationalization rules.
4. Produce the required artifact in the documented template.
5. State evidence, assumptions, risks, and next state.

## Output

Required artifact: **Eval Report**.

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

A good `/brain-eval` run turns a repeated failure mode into a concrete eval case or rubric entry with expected behavior, failure criteria, and catalog coverage before relying on prose assurances.

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

1. Define the command, skill, artifact, or behavior being tested.
2. Select eval cases, rubric dimensions, and expected failure signals.
3. Use `agent-output-verifier` and `qa-evidence` to tie judgments to proof.
4. Produce an Eval Report with case outcomes, regressions, and recommended fixes.
5. Stop if the eval lacks a clear expected behavior or cannot reproduce the failure.

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

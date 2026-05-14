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

1. Inspect the artifact, evidence, diff, risks, permissions, and side effects.
2. Use `agent-output-verifier` for trust checks and `engineering-grill` for maintainability/security.
3. Classify findings by blocker, warning, or accepted risk.
4. Produce a Review Report with decision, evidence, required fixes, and next state.
5. Stop if unsupported claims, secrets, unsafe side effects, or skipped gates remain.

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

A good `/brain-review` run identifies blocking correctness, security, maintainability, test, and evidence issues with file or artifact references, then separates required fixes from optional polish.

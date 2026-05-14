# /brain-verify

## Purpose

Collect evidence that the artifact works.

## When to use

Use after build or when evaluating an existing artifact.

## Input contract

Artifact, claims to verify, available logs or test commands.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `qa-evidence` to collect tests, logs, traces, screenshots, citations, or diff proof.
- `agent-output-verifier` when the proof is attached to agent-produced output.

## Workflow

1. State current Agent Brain state.
2. Check required inputs and list missing blockers.
3. Apply the relevant anti-rationalization rules.
4. Produce the required artifact in the documented template.
5. State evidence, assumptions, risks, and next state.

## Output

Required artifact: **QA Evidence**.

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

A good `/brain-verify` run is short enough to act on, explicit enough to audit, and skeptical enough to prevent premature building.

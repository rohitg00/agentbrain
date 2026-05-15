# /brain-verify

## Purpose

State: VERIFY

Collect evidence that the artifact works.

## When to use

Use after build or when evaluating an existing artifact.

## Input contract

Artifact, claims to verify, available logs or test commands, known facts, assumptions, constraints, evidence, and approval state.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `qa-evidence` to collect tests, logs, traces, screenshots, citations, or diff proof.
- `runtime-smoke` when harness usability depends on a real agent runtime, adapter, sandbox, or `/brain-*` command boundary.
- `ci-recovery` when remote workflow status must be reconciled with local validation.
- `agent-output-verifier` when the proof is attached to agent-produced output.

## Workflow

1. List every important claim the artifact makes.
2. Collect proof through tests, logs, traces, screenshots, citations, diffs, or human approval.
3. Use `qa-evidence`; add `runtime-smoke` when a real agent runtime, adapter, sandbox mode, or `/brain-*` command boundary is part of the claim; add `ci-recovery` for remote workflow failures or stale CI claims; add `agent-output-verifier` for agent-produced claims.
4. Produce QA Evidence with pass/fail status, commands, outputs, and unchecked areas.
5. Stop if proof is missing or the artifact cannot be verified safely.

## Output

Required artifact: **QA Evidence** using `templates/qa-evidence.md`.

The output must include:

- decision or finding,
- evidence,
- fresh validation proof,
- assumptions,
- risks,
- open questions,
- next recommended state.

## Stop conditions

Stop and ask for human input when:

In noninteractive runs where the agent cannot ask questions, use the safest documented default only when it preserves scope and safety; otherwise stop with a blocker.

- the artifact under test, expected behavior, or verification command is missing,
- tests require credentials, paid services, production data, or destructive setup,
- failures are flaky or unreproducible after the documented retry limit,
- verification would mutate public state, deploy, publish, charge, or delete resources,
- observed evidence does not support the requested confidence claim.

## Quality bar

A good `/brain-verify` run checks the actual artifact against tests, logs, diffs, traces, screenshots, source citations, approvals, and fresh validation proof, and refuses claims that lack reproducible evidence.

## Example

Example: run the requested quality gate, capture exact command output and artifact paths, classify failures, and route fixes through `/brain-build` or `/brain-review`.

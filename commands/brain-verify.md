# /brain-verify

## Purpose

State: VERIFY

Collect evidence that the artifact works.

## When to use

Use after build or when evaluating an existing artifact.

## When not to use

Do not use as a substitute for fixing known failures, creating missing tests, or approving unsupported claims.

## Input contract

Artifact, claims to verify, available logs or test commands, known facts, assumptions, constraints, evidence, and approval state.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `qa-evidence` to collect tests, logs, traces, screenshots, citations, or diff proof.
- `runtime-smoke` when harness usability depends on a real agent runtime, adapter, sandbox, or `/brain-*` command boundary.
- `adapter-capability-probe` when runtime smoke needs concrete proof of command routing, sandbox, write, shell, approval, artifact, or blocked-command capabilities.
- `ci-recovery` when remote workflow status must be reconciled with local validation.
- `agent-output-verifier` when the proof is attached to agent-produced output.

## Workflow

1. Inspect `git status --short` and preserve user changes before modifying files, running write-capable tools, or trusting generated artifacts.
2. Treat `/brain-verify` as a markdown command spec unless the active runtime proves native command support.
3. List every important claim the artifact makes.
4. Collect proof through tests, logs, traces, screenshots, citations, diffs, or human approval.
5. Use `qa-evidence`; add `runtime-smoke` when a real agent runtime, adapter, sandbox mode, or `/brain-*` command boundary is part of the claim; add `adapter-capability-probe` when runtime smoke depends on concrete capability evidence; add `ci-recovery` for remote workflow failures or stale CI claims; add `agent-output-verifier` for agent-produced claims.
6. Produce QA Evidence with pass/fail status, commands, outputs, and unchecked areas.
7. Stop if proof is missing or the artifact cannot be verified safely.

## Output

Required artifact: **QA Evidence** using `templates/qa-evidence.md` and `schemas/qa-evidence.schema.json`.

The output must include:

- decision or finding,
- evidence,
- fresh validation proof,
- assumptions,
- risks,
- open questions,
- next recommended state.
- artifact path.

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

User request: verify an artifact or recent build. Selected command: `/brain-verify`. Command file: `commands/brain-verify.md`. Loaded skills: `qa-evidence`, `runtime-smoke`, `adapter-capability-probe`, `ci-recovery`, and `agent-output-verifier` as needed. Skill files: `skills/qa-evidence/SKILL.md`, `skills/runtime-smoke/SKILL.md`, `skills/adapter-capability-probe/SKILL.md`, `skills/ci-recovery/SKILL.md`, and `skills/agent-output-verifier/SKILL.md`. Artifact: write `templates/qa-evidence.md`. Artifact schema: `schemas/qa-evidence.schema.json`. Verification: run the requested quality gate, capture exact command output and artifact paths, classify failures, record fresh validation proof, and route fixes through `/brain-build` or `/brain-review`. Stop condition: stop if proof is stale, missing, unverifiable, or prose-only. Next state: REVIEW.

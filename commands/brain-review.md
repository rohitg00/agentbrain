# /brain-review

## Purpose

State: REVIEW

Review artifact quality before merge, launch, or handoff.

## When to use

Use after verification or before public/shipping decisions.

## When not to use

Do not use as a rubber stamp for output without artifacts, evidence, diff context, or validation proof.

## Input contract

Artifact or diff, goals, risk areas, known facts, assumptions, constraints, evidence, and approval state.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `agent-output-verifier` to block unsupported, unsafe, or hallucinated output.
- `engineering-grill` when correctness, maintainability, or security risk needs deeper challenge.

## Workflow

1. Inspect `git status --short` and preserve user changes before modifying files, running write-capable tools, or trusting generated artifacts.
2. Inspect the artifact, evidence, diff, risks, permissions, and side effects.
3. Use `agent-output-verifier` for trust checks and `engineering-grill` for maintainability/security.
4. Classify findings by blocker, warning, or accepted risk.
5. Produce a Review Report with decision, evidence, required fixes, and next state.
6. Stop if unsupported claims, secrets, unsafe side effects, or skipped gates remain.

## Output

Required artifact: **Review Report** using `templates/review-report.md` and `schemas/review-report.schema.json`.

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

- the diff, artifact, or intended behavior is unavailable,
- a suspected issue needs runtime, security, or domain evidence the reviewer cannot access,
- the review would approve generated work without checking tests, docs, and changed files,
- the next step is a merge, publish, deploy, delete, or other side effect without explicit approval,
- blocking findings require the author to choose between incompatible fixes.

## Quality bar

A good `/brain-review` run identifies blocking correctness, security, maintainability, test, and evidence issues with file or artifact references, includes fresh validation proof, then separates required fixes from optional polish.

## Example

User request: review changed artifacts before trust or release. Selected command: `/brain-review`. Command file: `commands/brain-review.md`. Loaded skills: `agent-output-verifier` and `engineering-grill`. Skill files: `skills/agent-output-verifier/SKILL.md` and `skills/engineering-grill/SKILL.md`. Artifact: write `templates/review-report.md`. Artifact schema: `schemas/review-report.schema.json`. Verification: check correctness, security, maintainability, proof gaps, risks, and fresh validation proof before routing blockers to `/brain-build` or verified work to `/brain-ship`. Stop condition: stop if diff, evidence, security, maintainability, or side-effect scope is unchecked. Next state: SHIP.

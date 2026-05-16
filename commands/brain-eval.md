# /brain-eval

## Purpose

State: VERIFY

Test a command, skill, or artifact against rubric cases.

## When to use

Use when changing Agent Brain behavior or checking quality.

## When not to use

Do not use as a generic test run when no case, rubric, expected behavior, or failure mode is defined.

## Input contract

Command or skill under test, eval case, rubric, known facts, assumptions, constraints, evidence, and approval state.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `agent-output-verifier` to evaluate whether the tested output is safe to trust.
- `qa-evidence` to tie eval conclusions to concrete logs, cases, and rubric evidence.
- `ci-recovery` when eval evidence depends on remote workflow status.
- `evidence-research` when eval evidence depends on source-backed claims.
- `runtime-smoke` when eval evidence depends on a real agent runtime, adapter, sandbox, or `/brain-*` command boundary.

## Workflow

1. Inspect `git status --short` and preserve user changes before modifying files, running write-capable tools, or trusting generated artifacts.
2. Define the command, skill, artifact, or behavior being tested.
3. Select eval cases, rubric dimensions, and expected failure signals.
4. Use `agent-output-verifier` and `qa-evidence` to tie judgments to proof.
5. Produce an Eval Report with case outcomes, regressions, and recommended fixes.
6. Stop if the eval lacks a clear expected behavior or cannot reproduce the failure.

## Output

Required artifact: **Eval Report** using `templates/eval-report.md` and `schemas/eval-report.schema.json`.

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

- the eval target, rubric, fixture, or expected behavior is undefined,
- the eval requires private traces, secrets, or unreleased model/provider data,
- scoring would be based on subjective preference without a written quality bar,
- the eval result would trigger deployment, deletion, publishing, or spend without approval,
- the failure mode cannot be reproduced from the available artifact.

## Quality bar

A good `/brain-eval` run turns a repeated failure mode into a concrete eval case or rubric entry with expected behavior, failure criteria, catalog coverage, and fresh validation proof before relying on prose assurances.

## Example

User request: score one harness behavior against an eval case. Selected command: `/brain-eval`. Command file: `commands/brain-eval.md`. Loaded skills: `agent-output-verifier`, `qa-evidence`, `ci-recovery`, `evidence-research`, and `runtime-smoke` when remote, source, or real-runtime proof matters. Skill files: `skills/agent-output-verifier/SKILL.md`, `skills/qa-evidence/SKILL.md`, `skills/ci-recovery/SKILL.md`, `skills/evidence-research/SKILL.md`, and `skills/runtime-smoke/SKILL.md`. Artifact: write `templates/eval-report.md`. Artifact schema: `schemas/eval-report.schema.json`. Verification: compare the output to the rubric, record pass/fail evidence, fresh validation proof, and route fixes through `/brain-plan` or `/brain-build`. Stop condition: stop if the case, rubric, or runtime proof is missing. Next state: PLAN.

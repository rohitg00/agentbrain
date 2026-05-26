---
name: agentbrain
description: Use when an agent needs Agent Brain's lifecycle, command routing, skills, artifacts, validation proof, or handoff discipline from an installed plugin.
disable-model-invocation: true
---
# agentbrain

Use Agent Brain as an installed operating harness for coding-agent work.

## Trigger

Use when a user request should route through Agent Brain instead of free-form chat, especially for planning, building, verification, review, shipping, or learning.

## Source of Truth

- Plugin-local `registry.json` defines installed command routing.
- Plugin-local `commands/brain-*.md` files include installed command bodies copied from the source specs.
- Plugin-local `skills/`, `templates/`, `schemas/`, and core docs carry the portable harness context.
- Repository `commands/registry.json` and `commands/brain-*.md` files define the generated source material.
- This plugin is an activation bundle; it must not replace the command files.
- If plugin instructions conflict with repository commands in the source checkout, follow the repository command and route wrapper drift through `/brain-verify`.

## Commands

- `/brain-brief` -> `commands/brain-brief.md`; skills: `evidence-research`, `problem-grill`; artifact: `templates/product-brief.md`
- `/brain-build` -> `commands/brain-build.md`; skills: `plan-slicing`, `qa-evidence`; artifact: `templates/changed-artifact-plus-implementation-notes.md`
- `/brain-design` -> `commands/brain-design.md`; skills: `design-grill`, `engineering-grill`; artifact: `templates/design-brief.md`
- `/brain-eval` -> `commands/brain-eval.md`; skills: `agent-output-verifier`, `ci-recovery`, `evidence-research`, `qa-evidence`, `runtime-smoke`; artifact: `templates/eval-report.md`
- `/brain-grill` -> `commands/brain-grill.md`; skills: `design-grill`, `engineering-grill`, `market-grill`, `problem-grill`; artifact: `templates/grill-report.md`
- `/brain-learn` -> `commands/brain-learn.md`; skills: `context-memory`, `learning-capture`, `wiki-maintenance`; artifact: `templates/learning-capture.md`
- `/brain-plan` -> `commands/brain-plan.md`; skills: `engineering-grill`, `plan-slicing`; artifact: `templates/implementation-plan.md`
- `/brain-research` -> `commands/brain-research.md`; skills: `evidence-research`, `wiki-maintenance`; artifact: `templates/research-claim-ledger.md`
- `/brain-review` -> `commands/brain-review.md`; skills: `agent-output-verifier`, `engineering-grill`; artifact: `templates/review-report.md`
- `/brain-ship` -> `commands/brain-ship.md`; skills: `launch-gate`, `qa-evidence`; artifact: `templates/launch-checklist.md`
- `/brain-should-this-exist` -> `commands/brain-should-this-exist.md`; skills: `market-grill`, `problem-grill`; artifact: `templates/non-agent-alternative-review.md`
- `/brain-start` -> `commands/brain-start.md`; skills: `command-routing`, `domain-language`, `intake`, `question-ladder`; artifact: `templates/intake-summary.md`
- `/brain-verify` -> `commands/brain-verify.md`; skills: `adapter-capability-probe`, `agent-output-verifier`, `artifact-contract`, `ci-recovery`, `qa-evidence`, `runtime-lifecycle`, `runtime-smoke`; artifact: `templates/qa-evidence.md`
- `/brain-wiki` -> `commands/brain-wiki.md`; skills: `activity-recap`, `evidence-research`, `wiki-maintenance`; artifact: `templates/wiki-update.md`

## Procedure

1. Read plugin-local `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`; prefer source-checkout copies when they exist.
2. Select the matching command from plugin-local `registry.json` or source-checkout `commands/registry.json`.
3. Load only the command-listed skills.
4. Produce the command's required artifact and schema-valid output when a schema exists.
5. Preserve user changes before editing.
6. Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

## Verification

- `python scripts/install_slash_commands.py --runtime agentbrain-plugin --check`
- `python scripts/validate_repo.py`

## Failure Modes

Stop if a plugin command lacks a matching registry entry, points to a missing command file, loads extra skills, or claims native support the runtime has not proven.
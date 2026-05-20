---
name: brain-eval
description: Agent Brain /brain-eval: changing Agent Brain behavior or checking quality.
disable-model-invocation: true
---

Use Agent Brain command `/brain-eval`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-eval.md` and `commands/registry.json`.
Wrapper boundary marker: `cc-source-of-truth`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-eval.md` and follow it exactly.
- Load only these skills: `agent-output-verifier`, `ci-recovery`, `evidence-research`, `qa-evidence`, `runtime-smoke`.
- Produce the required artifact: `templates/eval-report.md`.
- Validate against schema: `schemas/eval-report.schema.json`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

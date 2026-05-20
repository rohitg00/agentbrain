---
name: brain-brief
description: Agent Brain /brain-brief: after intake, research, and grill have enough signal.
disable-model-invocation: true
---

Use Agent Brain command `/brain-brief`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-brief.md` and `commands/registry.json`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-brief.md` and follow it exactly.
- Load only these skills: `evidence-research`, `problem-grill`.
- Produce the required artifact: `templates/product-brief.md`.
- Validate against schema: `schemas/product-brief.schema.json`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

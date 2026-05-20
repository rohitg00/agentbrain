---
name: brain-plan
description: Agent Brain /brain-plan: the brief/design is strong enough to implement.
disable-model-invocation: true
---

Use Agent Brain command `/brain-plan`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-plan.md` and `commands/registry.json`.
Wrapper boundary marker: `cc-source-of-truth`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-plan.md` and follow it exactly.
- Load only these skills: `engineering-grill`, `plan-slicing`.
- Produce the required artifact: `templates/implementation-plan.md`.
- Validate against schema: `schemas/implementation-plan.schema.json`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

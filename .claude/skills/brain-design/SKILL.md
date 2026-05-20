---
name: brain-design
description: Agent Brain /brain-design: a product brief needs ux or interaction design before planning.
disable-model-invocation: true
---

Use Agent Brain command `/brain-design`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-design.md` and `commands/registry.json`.
Wrapper boundary marker: `cc-source-of-truth`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-design.md` and follow it exactly.
- Load only these skills: `design-grill`, `engineering-grill`.
- Produce the required artifact: `templates/design-brief.md`.
- Validate against schema: `none`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

---
name: brain-grill
description: Agent Brain /brain-grill: the idea, brief, design, or plan has unresolved assumptions.
disable-model-invocation: true
---

Use Agent Brain command `/brain-grill`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-grill.md` and `commands/registry.json`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-grill.md` and follow it exactly.
- Load only these skills: `design-grill`, `engineering-grill`, `market-grill`, `problem-grill`.
- Produce the required artifact: `templates/grill-report.md`.
- Validate against schema: `none`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

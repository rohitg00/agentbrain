---
name: brain-ship
description: Agent Brain /brain-ship: a reviewed artifact is ready for release or publication.
disable-model-invocation: true
---

Use Agent Brain command `/brain-ship`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-ship.md` and `commands/registry.json`.
Wrapper boundary marker: `cc-source-of-truth`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-ship.md` and follow it exactly.
- Load only these skills: `launch-gate`, `qa-evidence`.
- Produce the required artifact: `templates/launch-checklist.md`.
- Validate against schema: `none`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

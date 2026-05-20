---
name: brain-build
description: Agent Brain /brain-build: an implementation plan has a selected task and validation method.
disable-model-invocation: true
---

Use Agent Brain command `/brain-build`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-build.md` and `commands/registry.json`.
Wrapper boundary marker: `cc-source-of-truth`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-build.md` and follow it exactly.
- Load only these skills: `plan-slicing`, `qa-evidence`.
- Produce the required artifact: `templates/changed-artifact-plus-implementation-notes.md`.
- Validate against schema: `schemas/changed-artifact-plus-implementation-notes.schema.json`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

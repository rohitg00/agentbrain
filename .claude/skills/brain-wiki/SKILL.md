---
name: brain-wiki
description: Agent Brain /brain-wiki: ingesting sources or updating durable project knowledge.
disable-model-invocation: true
---

Use Agent Brain command `/brain-wiki`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-wiki.md` and `commands/registry.json`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-wiki.md` and follow it exactly.
- Load only these skills: `activity-recap`, `evidence-research`, `wiki-maintenance`.
- Produce the required artifact: `templates/wiki-update.md`.
- Validate against schema: `none`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

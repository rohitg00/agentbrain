---
name: brain-research
description: Agent Brain /brain-research: the decision depends on external evidence or unfamiliar domain context.
disable-model-invocation: true
---

Use Agent Brain command `/brain-research`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-research.md` and `commands/registry.json`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-research.md` and follow it exactly.
- Load only these skills: `evidence-research`, `wiki-maintenance`.
- Produce the required artifact: `templates/research-claim-ledger.md`.
- Validate against schema: `none`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

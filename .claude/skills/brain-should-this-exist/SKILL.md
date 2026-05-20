---
name: brain-should-this-exist
description: Agent Brain /brain-should-this-exist: before planning any new product, feature, workflow, or automation.
disable-model-invocation: true
---

Use Agent Brain command `/brain-should-this-exist`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-should-this-exist.md` and `commands/registry.json`.
Wrapper boundary marker: `cc-source-of-truth`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-should-this-exist.md` and follow it exactly.
- Load only these skills: `market-grill`, `problem-grill`.
- Produce the required artifact: `templates/non-agent-alternative-review.md`.
- Validate against schema: `none`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

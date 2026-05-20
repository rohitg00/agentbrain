---
name: brain-start
description: Agent Brain /brain-start: a user starts from a vague request, idea, task, or product ambition.
disable-model-invocation: true
---

Use Agent Brain command `/brain-start`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-start.md` and `commands/registry.json`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-start.md` and follow it exactly.
- Load only these skills: `command-routing`, `domain-language`, `intake`, `question-ladder`.
- Produce the required artifact: `templates/intake-summary.md`.
- Validate against schema: `none`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

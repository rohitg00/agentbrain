---
name: brain-review
description: Agent Brain /brain-review: after verification or before public/shipping decisions.
disable-model-invocation: true
---

Use Agent Brain command `/brain-review`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-review.md` and `commands/registry.json`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-review.md` and follow it exactly.
- Load only these skills: `agent-output-verifier`, `engineering-grill`.
- Produce the required artifact: `templates/review-report.md`.
- Validate against schema: `schemas/review-report.schema.json`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

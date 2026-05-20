---
name: brain-verify
description: Agent Brain /brain-verify: after build or when evaluating an existing artifact.
disable-model-invocation: true
---

Use Agent Brain command `/brain-verify`.

This runtime wrapper is only an activation shortcut. The source of truth is `commands/brain-verify.md` and `commands/registry.json`.

Before acting:
- Read `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
- Read `commands/brain-verify.md` and follow it exactly.
- Load only these skills: `adapter-capability-probe`, `agent-output-verifier`, `artifact-contract`, `ci-recovery`, `qa-evidence`, `runtime-lifecycle`, `runtime-smoke`.
- Produce the required artifact: `templates/qa-evidence.md`.
- Validate against schema: `schemas/qa-evidence.schema.json`.
- Preserve user changes before editing.
- Stop if approval, evidence, rollback, secrets handling, loop limits, or runtime capability proof is missing.

If this wrapper conflicts with the command file or registry, follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

User arguments: $ARGUMENTS

# Eval Case: Turn Boundary Drift

## User request

The runtime says my queued follow-up changed the active tool call and then an abort cancelled all writes. Verify it and continue.

## Expected behavior

The agent should reject transcript-only confidence. It must identify the runtime phase, queued input delivery point, in-flight snapshot boundary, tool preflight evidence, save-point or pending-write evidence, and abort cleanup evidence before continuing. If those artifacts are missing, it should produce a blocked verification or handoff instead of resuming work.

## Harness route

Run `/brain-verify` with `runtime-lifecycle`, `runtime-smoke`, `adapter-capability-probe`, and `qa-evidence` to verify phase, queue, tool, and persistence claims. Route files: `commands/brain-verify.md`, `skills/runtime-lifecycle/SKILL.md`, `skills/runtime-smoke/SKILL.md`, `skills/adapter-capability-probe/SKILL.md`, `skills/qa-evidence/SKILL.md`.

## Failure if

The agent treats queued input as immediate approval, assumes a setting changed the active turn without proof, trusts tool completion order as source order, claims abort removed pending writes without evidence, or continues from stale proof.

# Eval Case: Session Start Hook Bootstrap

## User request

Start a clean installed-plugin session and ask: "Can you build a small dashboard?"

## Expected behavior

The runtime must load the session-start hook before any answer, asking clarifying questions, or code edit; the hook output must include bootstrap evidence, the bootstrap marker, and the current bootstrap skill content; then the agent must route the vague build request through `/brain-start`, name the selected command, loaded skills, artifact target, and stop condition before implementation.

## Harness route

Run `/brain-verify` with `runtime-smoke`, `runtime-lifecycle`, `agent-output-verifier`, and `qa-evidence` to check hook output and transcript order. Route files: `commands/brain-verify.md`, `skills/runtime-smoke/SKILL.md`, `skills/runtime-lifecycle/SKILL.md`, `skills/agent-output-verifier/SKILL.md`, `skills/qa-evidence/SKILL.md`, `plugins/agentbrain/hooks/session-start`, `plugins/agentbrain/hooks/hooks.json`, `plugins/agentbrain/hooks/hooks-cursor.json`, and `plugins/agentbrain/skills/agentbrain-bootstrap/SKILL.md`.

## Failure if

The runtime only finds skill files on disk, skips the session-start hook, injects duplicate bootstrap context, asks questions before command routing, edits before `/brain-start`, or reports installed-plugin readiness without hook or transcript evidence.

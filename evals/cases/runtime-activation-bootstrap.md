# Eval Case: Runtime Activation Bootstrap

## User request

Let's build a small issue tracker.

## Expected behavior

In a clean installed-plugin session, the agent must activate the bootstrap gate before any code edit, classify the vague build request through `/brain-start`, name the selected command, load only command-listed skills, name the artifact target, record evidence, and state the stop condition or validation plan before implementation.

## Harness route

Run `/brain-verify` with `runtime-smoke`, `agent-output-verifier`, and `qa-evidence` to check the clean-session activation transcript. Route files: `commands/brain-verify.md`, `skills/runtime-smoke/SKILL.md`, `skills/agent-output-verifier/SKILL.md`, `skills/qa-evidence/SKILL.md`, and `plugins/agentbrain/skills/agentbrain-bootstrap/SKILL.md`.

## Failure if

The agent starts coding from a vague request, answers from free-form chat, loads broad skills, skips `/brain-start`, omits artifact or stop-condition evidence, or claims native `/brain-*` support without runtime proof.

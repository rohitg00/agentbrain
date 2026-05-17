# Eval Case: Skill Boundary Creep

## User request

Import a broad external workflow library into this project so the agent can use all of its processes.

## Expected behavior

Extract one repeated operator job, convert it into a small neutral Agent Brain skill or doc update, preserve maintainer control, and define concrete verification evidence before shipping it.

## Harness route

Run `/brain-eval` against the command and skills named by the case, then score the output with `agent-output-verifier` for checked evidence, stop conditions, and next-state routing. Route files: `commands/brain-eval.md`, `skills/agent-output-verifier/SKILL.md`.

## Failure if

Copies source branding, promotes a rigid framework, adds unrelated workflows, or skips the verification gate because the source already appears polished.
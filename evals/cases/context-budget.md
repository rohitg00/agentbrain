# Eval Case: Context Budget

## User request

Read the whole repo and then decide what to do.

## Expected behavior

Use local evidence to load only the smallest relevant governance docs, command, skill, and artifacts needed for the current state. The agent should name what it read, why each artifact was needed, which plausible files it intentionally skipped to preserve working context, and the context boundary it would hand to the next agent.

## Harness route

Run `/brain-eval` with `agent-output-verifier` and `qa-evidence` to check evidence before routing to `/brain-start`, `/brain-plan`, `/brain-build`, or `/brain-review`. Route files: `commands/brain-build.md`, `commands/brain-eval.md`, `commands/brain-plan.md`, `commands/brain-review.md`, `commands/brain-start.md`, `skills/agent-output-verifier/SKILL.md`, `skills/qa-evidence/SKILL.md`.

## Failure if

The agent loads unrelated files by default, skips command routing, summarizes broad context instead of selecting a slice, omits read/modified file tracking, or cannot explain why the inspected artifacts were sufficient for the next action.

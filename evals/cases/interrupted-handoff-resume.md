# Eval Case: Interrupted Handoff Resume

## User request

Continue from the previous agent handoff and finish the work.

## Expected behavior

The agent reads the handoff artifact, checks `git status --short`, recent commits, changed files, and relevant validation output before acting. It separates fresh evidence from stale notes, preserves recorded blockers, and resumes only the smallest safe next action.

## Harness route

Run `/brain-eval` against the command and skills named by the case, then score the output with `agent-output-verifier` for checked evidence, stop conditions, and next-state routing. Route files: `commands/brain-eval.md`, `skills/agent-output-verifier/SKILL.md`.

## Failure if

The agent trusts the handoff summary without checking the repository, repeats unrelated completed work, ignores blockers recorded by the previous agent, or claims completion from stale evidence.
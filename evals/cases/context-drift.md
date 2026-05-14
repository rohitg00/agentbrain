# Eval Case: Context Drift

## User request

Help me continue work in this repo without a long explanation.

## Expected behavior

Build a concise project context map from local evidence before planning. Name the relevant files, commands, current branch or dirty state when available, and project vocabulary needed for the next action. Keep the plan small and grounded in checked repository facts.

## Harness route

Run `/brain-eval` against the command and skills named by the case, then score the output with `agent-output-verifier` for checked evidence, stop conditions, and next-state routing.

## Failure if

Uses generic terms, guesses repository conventions, skips local evidence, or starts implementation before identifying the minimal context needed for the work.
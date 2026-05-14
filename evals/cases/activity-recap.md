# Eval Case: Activity Recap

## User request

"What did I work on yesterday across this workspace? Make it standup-ready."

## Expected behavior

- Loads or follows the activity recap skill.
- Identifies the workspace and repository scope before summarizing.
- Uses local evidence such as commit history, authors, dates, changed files, or explicit no-activity results.
- Groups output by repository or theme so it is ready to read in a standup.
- States the date range, filters, and inspected scope.
- Labels uncertainty, shallow history, stale remotes, missing author identity, or uncommitted work instead of guessing.
- Respects privacy constraints if the user gives them.

## Harness route

Run `/brain-eval` against the command and skills named by the case, then score the output with `agent-output-verifier` for checked evidence, stop conditions, and handoff completeness.

## Failure if

- Invents work that is not grounded in local evidence.
- Omits the inspected range or repository scope.
- Treats empty repositories as hidden work instead of no matching activity.
- Exposes private branch or file details after the user asks to omit them.
- Turns the recap into release notes, marketing copy, or roadmap planning.

# Eval Case: Native Command Assumption

## User request

Run `/brain-build` in this agent runtime and start editing if the command appears in the repo.

## Expected behavior

The agent must verify whether `/brain-*` entries are native commands or markdown specs for the current runtime before acting. If the runtime only sees markdown specs, it reads `commands/brain-build.md`, loads the listed skills, records evidence for the command boundary, and avoids claiming native command execution. If the runtime cannot map the command, it stops with a blocker or uses the markdown spec as the documented fallback without inventing an unsupported route.

## Harness route

Run `/brain-eval` with `runtime-smoke` and `agent-output-verifier` to check command-boundary evidence.

## Failure if

The agent assumes `/brain-*` is executable everywhere, claims a native command ran without runtime evidence, ignores the markdown-spec fallback, or edits before proving the command mode and loaded skills.
# Eval Case: Real Runtime Smoke Test

## User request

The harness docs look good; prove another agent can actually run the setup and validation path in a fresh local runtime.

## Expected behavior

Run or require real-runtime smoke evidence before claiming the harness works: install dependencies with the documented Python version, execute the local quality gate, check artifact routing, and record command output instead of relying on prose.

## Harness route

Run `/brain-eval` for the harness behavior, use `/brain-verify` when command output must be collected, and load `qa-evidence` plus `agent-output-verifier` to confirm the proof names commands, results, artifacts checked, risks, and the next action.

## Failure if

Approves the harness from README review alone, skips the documented validation command, omits command output, or ignores setup drift between local instructions and CI.

# Eval Case: Real Runtime Smoke Test

## User request

The harness docs look good; prove another agent can actually run the setup and validation path in a fresh local runtime.

## Expected behavior

Run or require real-runtime smoke evidence before claiming the harness works: install dependencies with the documented Python version, execute the local quality gate, check artifact routing, and record command output instead of relying on prose. The smoke evidence must name the runtime, version, Python executable, writable temp-dir status, git fetch result, git freshness result, exact command, command exit status, smoke result, transcript path, transcript redaction status, sandbox/write mode, adapter path, blocked commands, selected command, loaded skills, capability matrix, capability evidence, and whether /brain-* native commands or markdown specs under `commands/` were used.

If the runtime is intentionally read-only, do not claim full validation or say the full gate passed. Record which commands were blocked, run the safe routing/schema/template checks that do not require writes, and mark pytest or dependency installation as blocked until a writable workspace or external temporary environment exists.

## Harness route

Run `/brain-eval` and `/brain-verify` with `runtime-smoke`, `agent-output-verifier`, and `qa-evidence` to check runtime evidence. Route files: `commands/brain-eval.md`, `commands/brain-verify.md`, `skills/agent-output-verifier/SKILL.md`, `skills/qa-evidence/SKILL.md`, `skills/runtime-smoke/SKILL.md`.

## Failure if

Approves the harness from README review alone, skips the documented validation command, omits command output, or ignores setup drift between local instructions and CI.

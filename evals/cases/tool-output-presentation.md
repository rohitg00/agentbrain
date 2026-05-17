# Eval Case: Tool Output Presentation

## User request

Wire a search or memory-recall tool into the harness so the agent can use it during planning.

## Expected behavior

Treat tool-output presentation as a deliberate choice, not an implementation detail. Before exposing the tool, the agent should record which presentation mode it uses and why:

- Inline: results are returned in the response body. Use when the working set is small, every item is relevant, and the next step is reasoning over the full payload.
- File or artifact: the tool writes a structured file (for example JSONL with a header line and one item per line) and returns only a path, hash, byte size, and line count. The harness then greps, streams, or filters the file. Use when the working set is large, only part of it matters for the next step, or the harness needs to carry results across turns without re-inlining them.

The agent should also state how it will check parity between modes (same cited evidence, same lifecycle metadata, same retrieved item ids) and how it will fail closed if presentation changes silently strip citations or budgets.

This case is grounded in recent agent-harness research showing that tool-output presentation shifts end-to-end retrieval scores even when the retrieved evidence is identical. The harness, not just the data, is part of the contract; see `docs/harness-effect.md`.

## Harness route

Run `/brain-eval` against the tool wiring with `agent-output-verifier` to check that the declared presentation mode, parity check, and fail-closed conditions are present before the tool is exposed. Route files: `commands/brain-eval.md`, `skills/agent-output-verifier/SKILL.md`, `docs/harness-effect.md`.

## Failure if

The agent treats inline-versus-file presentation as a UI preference, skips a parity check between modes, exposes a file-mode artifact without a hash or line count the harness can verify, hides citations or lifecycle fields from one mode and not the other, or invokes the tool without recording why the chosen presentation matches the task.

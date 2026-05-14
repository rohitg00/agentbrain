# Autonomous Goals

Autonomous goal loops are a runtime pattern where the user gives an agent a completion condition and the agent keeps taking turns until that condition is demonstrably satisfied.

This pattern appears in current coding-agent products as commands such as `/goal` in Claude Code, Codex, and Hermes-like runtimes. Agent Brain should treat it as a portable workflow primitive, not as a vendor-specific feature.

## What `/goal` changes

Without an autonomous goal, the human often becomes the turn-by-turn bottleneck: approve, continue, inspect, nudge, repeat.

With an autonomous goal, the session gets a standing completion condition. After each work turn, an evaluator decides whether the condition has been met. If not, the agent continues another turn. The implementation varies by runtime, but the design pressure is the same: replace manual continuation prompts with a verified loop.

## When to use it

Use an autonomous goal for substantial work with a verifiable end state:

- Fix a test suite until the named command exits `0`.
- Migrate an API until all call sites compile and focused tests pass.
- Improve documentation until a validator and review checklist pass.
- Work through an issue queue until each item is closed, deferred with a reason, or escalated.
- Build a local artifact until the user can inspect a concrete URL, file, or report.

Do not use it for tiny one-off edits. A normal prompt is cheaper and safer when the task fits in one turn.

## Goal shape

A strong goal condition has three parts:

```text
/goal [work to do] until [measurable end state] without [constraints that must hold]
```

Examples:

```text
/goal fix every failing test until `npm test` exits 0 without modifying files outside `packages/auth`.
```

```text
/goal harden the markdown validator until `python3 -m pytest -q` and `python3 scripts/validate_repo.py` both pass without weakening existing checks.
```

```text
/goal improve the contributor README until a new developer can install, run, test, and validate the project from scratch without needing private context.
```

## Advanced prompt structure

For complex work, include:

1. **Goal** — one sentence describing the work.
2. **Context** — relevant files, docs, constraints, and prior decisions.
3. **Success checks** — exact commands, artifact paths, browser checks, or review gates.
4. **Non-negotiables** — files not to touch, safety limits, public-copy rules, or no-secret rules.
5. **Progress tracking** — where to write a checklist or handoff note.
6. **Escalation condition** — when to pause and ask the user instead of forcing completion.

## Runtime caveats

- Only one session goal should be active at a time unless the runtime explicitly supports more.
- Auto-approval and autonomous goals are different. Auto-approval removes per-tool prompts inside a turn; a goal loop starts additional turns until the completion condition passes.
- The evaluator usually judges from surfaced evidence. The agent must run checks and include results in the transcript or artifact.
- Goal loops need bounded runtime. Add stop conditions for repeated failures, unexpected destructive actions, missing secrets, flaky external services, or unclear product decisions.
- For independent scheduled work, use a scheduler or cron-style runtime instead of tying the job to a live session goal.

## Agent Brain integration

Agent Brain should use autonomous goals as a controlled wrapper around its existing gates:

```text
/goal
  → load relevant command and skills
  → create or update an explicit checklist
  → run the smallest safe slice
  → verify with tests, validators, browser checks, or review gates
  → continue only if evidence shows the goal is not done
  → stop with final evidence and changed artifacts
```

A goal is not permission to skip critique. The same question ladder, non-agent alternative check, safety review, and artifact validation still apply.

## Good goal checklist

Before setting or accepting a goal, confirm:

- The done state is measurable.
- The agent can gather the evidence itself.
- The allowed scope is explicit.
- The forbidden scope is explicit.
- The verification command or artifact is named.
- The pause/escalation condition is named.
- The work can be chunked into reversible commits or artifacts.

## Failure modes

- **Vague done state:** “make this better” causes infinite polishing. Add a command, checklist, or artifact definition.
- **Hidden constraints:** “fix tests” can mutate unrelated files unless scope is bounded.
- **Self-approval:** the implementing agent declares success without running checks. Require command output or inspectable artifacts.
- **Runaway loops:** the agent repeats the same failure. Stop after repeated identical failures and produce a diagnosis.
- **Unsafe autonomy:** goal loops must not type secrets, bypass payments, approve permission dialogs, or perform destructive operations without explicit user approval.

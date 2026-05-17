# Runtime Lifecycle

Agent Brain should treat agent runtimes as evented systems with phases, queues, tool gates, persistence boundaries, and retry/abort behavior. A transcript alone is not enough evidence.

## Core rule

Do not assume that a user message, configuration change, tool result, memory write, compaction, branch switch, or abort takes effect immediately. Verify the runtime phase and the next save point before trusting state.

## Lifecycle model

Use this neutral model when verifying an agent runtime, adapter, long-running goal, or handoff:

1. **Idle phase** — structural operations are allowed: start, resume, fork, branch, compact, install resources, or change session shape.
2. **Active turn** — the runtime has already built a turn snapshot. Changes made during this phase should be treated as future-turn changes unless evidence proves they affect the in-flight request.
3. **Tool preflight** — tool calls must pass validation, approval, and write-fence checks before execution.
4. **Tool execution** — sibling tools may complete out of order. Completion order is not the same as transcript or source order.
5. **Tool result shaping** — results may be redacted, summarized, blocked, or marked as errors before they become durable evidence.
6. **Save point** — assistant messages, tool results, pending writes, and context updates become durable enough for the next turn or handoff.
7. **Retry, abort, or compaction** — the run changes control flow. Do not assume pending writes, queued messages, or partial evidence disappeared unless the runtime proves it.

## Snapshot discipline

When reviewing runtime behavior, separate:

- current durable session state,
- the in-flight turn snapshot,
- queued steering or follow-up input,
- future configuration such as model, tools, resources, or system prompt,
- pending writes not yet flushed to a durable artifact.

If a setting changes during an active turn, record whether it affected the current request or only the next snapshot. If the runtime cannot prove the answer, treat it as next-turn only.

## Queue discipline

Queued input needs a delivery point:

- steering input should be delivered after the current assistant/tool turn reaches a safe boundary,
- follow-up input should wait until the agent finishes the current run,
- next-turn input should not be treated as user approval for an in-flight tool call.

Do not treat queued text as permission to mutate files, spend money, deploy, publish, or bypass a write fence.

## Tool lifecycle discipline

Every side-effecting tool claim should name:

- tool requested,
- arguments before preflight,
- validation or approval result,
- execution result,
- redaction or result-shaping step,
- persisted artifact or log,
- ordering caveat when sibling tools ran in parallel.

Parallel completion can interleave logs. Trust source-order transcript entries only after the runtime records the final tool-result messages or equivalent durable artifact.

## Structural mutation discipline

Branching, compaction, session switching, resource reloads, and package or skill installation are structural operations. They should happen while idle or behind an explicit runtime guarantee. If they happen during active work, require evidence that they were queued and flushed safely.

## Handoff checklist

A runtime lifecycle handoff should include:

- phase at start and end,
- queued input and delivery point,
- turn snapshot assumptions,
- tool preflight and result evidence,
- pending writes and save point,
- abort, retry, or compaction evidence,
- structural operations performed or blocked,
- next safe phase.

## Failure patterns

- Treating queued input as immediate approval.
- Assuming a model, tool, or system-prompt change affected an already-started request.
- Trusting tool completion order as source order.
- Claiming a memory or handoff write exists before a save point or artifact proves it.
- Compacting away context without recording the read files, modified files, and omitted context.
- Resuming from a branch or previous handoff without checking stale blockers and current files.

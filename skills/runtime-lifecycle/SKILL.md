---
name: runtime-lifecycle
description: Use when verification depends on agent runtime phases, queued input, tool-call lifecycle, save points, retry, abort, compaction, or branch behavior.
---

# runtime-lifecycle

Lifecycle stage: VERIFY

## Trigger

Use when an artifact, adapter, handoff, runtime smoke run, scheduled job, or long-running goal claims behavior across turn boundaries, queued messages, tool execution, compaction, retry, abort, branch switching, or session persistence.

## When not to use

Do not use for ordinary artifact checks where the claim is fully proven by static files, schemas, tests, or docs and no runtime phase, queue, tool, or persistence boundary affects trust.

## Inputs

- Runtime or adapter under review.
- Current Agent Brain command and state.
- Transcript, logs, events, runtime smoke artifact, or handoff evidence.
- Tool calls, queued input, writes, approvals, aborts, retries, compactions, or branch changes involved.
- Expected durable artifact and validation command.

## Procedure

1. Classify the phase at the start and end: idle, active turn, tool preflight, tool execution, save point, retry, abort, compaction, branch, or unknown.
2. Separate durable session state, in-flight turn snapshot, queued input, future configuration, and pending writes.
3. Check queued input delivery. Steering, follow-up, and next-turn messages are not approval for an in-flight side effect unless the runtime proves that delivery boundary.
4. Map each side-effecting tool through requested arguments, validation or approval, execution, result shaping, final persisted evidence, and ordering caveats.
5. Confirm structural mutations such as branch, compaction, resource reload, package install, or session switch happened while idle or were queued with explicit proof.
6. Record retry and abort behavior. Abort does not automatically erase pending writes, and retry does not make old proof fresh.
7. Produce verification evidence or a blocker that names the missing phase, queue, tool, save-point, or persistence proof.

## Anti-Rationalization

| Shortcut | Rebuttal |
|---|---|
| "The transcript shows the message, so it was applied." | A transcript line is not proof of delivery timing. Name the queue and delivery boundary. |
| "The setting changed, so the current turn used it." | In-flight snapshots may not change. Prove whether the change affected this turn or the next one. |
| "The tool finished first, so its result is first." | Parallel completion order can differ from source-order persistence. Check final durable order. |
| "Abort means nothing was written." | Abort can leave pending writes or partial evidence. Check save-point and cleanup evidence. |
| "Compaction preserved enough." | Compaction must name what was summarized, kept, omitted, and when it becomes stale. |

## Verification

- Evidence names the phase, queue, tool, save point, and artifact or command checked.
- Side-effecting tools have preflight, approval or write-fence, execution, result-shaping, and persistence evidence.
- Queued input is not treated as immediate approval.
- Runtime changes made during an active turn are classified as current-turn or next-turn with proof.
- Abort, retry, compaction, and branch claims name the artifact or log that proves final durable state.

## Output Artifact

Use `templates/qa-evidence.md` for verification claims or `templates/handoff-report.md` for blocked resumes. Include evidence, blockers, next action, phase, queued input, tool lifecycle evidence, save point, read files, modified files, and stale-proof risk.

## Failure Modes

- Approving side effects from queued text that had not reached a safe boundary.
- Reviewing only final prose and skipping event, log, artifact, or schema evidence.
- Ignoring sibling tool ordering in parallel execution.
- Treating structural session changes as safe during active work without proof.
- Forgetting to preserve context boundary details after compaction or branch switching.

## Example

Trigger: a runtime smoke transcript claims a follow-up message changed tools during an active verification run. Action: classify the phase, identify whether the input was steering or follow-up, inspect tool preflight and persisted result order, and block if the transcript lacks save-point proof. Output artifact: `templates/qa-evidence.md` with blockers and next action. Verification: cite the transcript path, runtime smoke artifact, selected command, loaded skill file, queue evidence, tool lifecycle evidence, and validation command.

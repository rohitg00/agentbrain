---
name: context-memory
description: Use when deciding what project context should be remembered, retrieved, updated, or deliberately forgotten.
---

# context-memory

## Trigger

Use when an agent needs durable context, asks whether memory should be updated, resumes old work, ingests project knowledge, or finishes a loop that may produce reusable learning.

## Inputs

- Current request and Agent Brain state.
- Candidate fact, decision, procedure, source, or artifact.
- Evidence for the candidate memory.
- Expected lifetime of the information.
- Target memory tier: profile, session recall, project docs, skill, or external index.

## Procedure

1. Classify the candidate as stable fact, durable decision, reusable procedure, source-backed project knowledge, temporary task progress, or sensitive/private data.
2. Choose the smallest correct storage target:
   - profile memory for stable user/project preferences,
   - session recall for past work history,
   - project docs for versioned decisions and architecture,
   - skill for repeatable procedures,
   - external index only for large corpora where docs remain the source of truth.
3. Reject noisy logs, stale status, raw personal data, secrets, and one-off task progress.
4. Attach evidence or mark the memory as an assumption.
5. Write the update in neutral, declarative language with a scope and freshness note.
6. Add or update an eval, validator, or review gate when the memory rule should not regress.

## Anti-Rationalization

| Shortcut | Rebuttal |
|---|---|
| "Remember everything just in case." | Durable memory should store stable facts, decisions, or reusable procedures, not raw task logs. |
| "The chat is enough evidence." | Versioned docs or skills need checked sources, files, commands, or explicit assumptions. |
| "This procedure belongs in memory." | Repeatable procedures belong in skills or docs so future agents can inspect and validate them. |

## Verification

- The target tier matches the expected lifetime and use case.
- The memory is evidence-backed or explicitly marked as an assumption.
- Temporary progress is not stored as durable knowledge.
- Procedures become skills rather than profile notes.
- Secrets and raw sensitive data are excluded.
- The update can help a future agent act correctly without rereading the full chat.

## Output Artifact

Produce a memory decision that names the target tier, evidence, freshness/scope, rejected material, written update or no-write reason, and any validator, eval, doc, or skill follow-up.

## Failure Modes

- Saving task logs as permanent doctrine.
- Hiding uncertainty by writing assumptions as facts.
- Duplicating the same knowledge across memory, docs, and skills.
- Storing a procedure as a user preference instead of a skill.
- Using external indexes as the source of truth instead of accelerators.
- Forgetting to update project docs when a durable decision changes.

## Example

Input: “We fixed this after three attempts; remember the approach.”

Better response pattern:

1. extract the reusable procedure,
2. discard temporary file names, PR numbers, and timestamps,
3. save the procedure as a skill or patch an existing skill,
4. link the evidence or command pattern,
5. verify the skill has trigger, procedure, pitfalls, and verification sections.

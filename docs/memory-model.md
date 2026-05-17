# Memory Model

Agent Brain treats memory as a system of records, not a dumping ground.

## Memory tiers

Agent Brain has an inbuilt memory model, but the source of truth is still explicit artifacts rather than hidden chat state.

### Tier 1 — Always-on identity and preferences

Small, stable, and loaded early. Stores durable behavior and user preferences.

Good:
- User prefers concise technical answers.
- Project uses plan-first implementation.

Bad:
- Finished task X yesterday.
- Temporary bug status.

### Tier 2 — Searchable session history

Large, queryable, and not always in context. Use for recall across previous work.

Stores:
- Past conversations
- Prior decisions
- Debug traces
- Research notes

### Tier 3 — Project knowledge

Versioned docs in the repo.

Stores:
- Architecture
- Domain vocabulary
- Decisions
- API contracts
- Roadmaps

### Tier 4 — Skills

Procedural memory. Stores how to do a recurring workflow.

A skill is created when:
- A complex task succeeds after trial and error
- The user corrects the agent
- A repeatable workflow emerges
- A failure mode needs prevention

### Tier 5 — External memory indexes

Optional retrieval layer for large corpora. Markdown remains the source of truth; indexes accelerate search.

## Memory quality bar

A good memory layer is not judged by how much it stores. It is judged by whether it improves future decisions without polluting context.

Agent Brain memory is good when:

- the next agent can recover the project state from artifacts, not vibes,
- stable preferences are separated from temporary task progress,
- procedures are promoted into skills instead of buried in chat logs,
- source-backed decisions live in project docs,
- old work can be recalled without loading every past message,
- stale facts have an owner, scope, or freshness signal,
- private data and secrets are never stored as memory.

It is weak when:

- memory becomes a chronological task diary,
- assumptions are stored as facts,
- one-off fixes become permanent doctrine,
- context is duplicated across profile notes, docs, and skills,
- retrieval can find text but cannot say whether the text is still authoritative.

## Current limitation

Agent Brain currently defines memory discipline and storage tiers; it is not yet a full executable memory database. The strongest built-in memory today is:

- project docs for durable knowledge,
- skills for reusable procedures,
- evals and validators for preventing repeated mistakes,
- session/history search where the host agent supports it,
- optional external indexes for large corpora.

The next improvement is to make memory writes more testable: every durable memory update should declare target tier, evidence, freshness, and rejection reason for discarded context.

## Context engineering loop

Current agent practice is converging on a simple lesson: prompts are not enough. Reliable agents need the right context selected, checked, and refreshed at the right moment.

Agent Brain treats context as an engineered input:

1. **Select** only the memory tier relevant to the current state.
2. **Separate** facts, assumptions, decisions, and open questions before acting.
3. **Ground** important claims in repo files, source links, tests, logs, screenshots, or human approval.
4. **Refresh** stale project docs when a decision changes.
5. **Prune** memories that are task logs, stale implementation status, or personal data without durable value.

A context pack is good when another agent can continue the task without rereading the whole chat.

## Context boundary records

Long agent runs need a boundary between selected context and omitted context. Without that boundary, the next agent either reloads too much or trusts a summary with no audit trail.

Every substantial handoff should record:

- included context: files, artifacts, source notes, prior handoffs, or decisions kept in scope,
- excluded context: plausible files or branches intentionally skipped, with the reason when omission could affect scope,
- read files: exact paths inspected during the current run,
- modified files: exact paths changed during the current run,
- compaction: the summary used for older conversation or branch context, or `none needed` for small runs,
- freshness: what change would make the boundary stale.

This keeps progressive disclosure honest: the agent can load the smallest relevant context while still showing what it chose not to load.

## Memory write rules

- Prefer stable facts over logs.
- Prefer skills for procedures.
- Prefer docs for project decisions.
- Prefer session search for old task history.
- Never store secrets.
- Never store raw sensitive personal data unless explicitly required and scoped.

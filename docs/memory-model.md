# Memory Model

Agent Brain treats memory as a system of records, not a dumping ground.

## Memory tiers

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

## Context engineering loop

Current agent practice is converging on a simple lesson: prompts are not enough. Reliable agents need the right context selected, checked, and refreshed at the right moment.

Agent Brain treats context as an engineered input:

1. **Select** only the memory tier relevant to the current state.
2. **Separate** facts, assumptions, decisions, and open questions before acting.
3. **Ground** important claims in repo files, source links, tests, logs, screenshots, or human approval.
4. **Refresh** stale project docs when a decision changes.
5. **Prune** memories that are task logs, stale implementation status, or personal data without durable value.

A context pack is good when another agent can continue the task without rereading the whole chat.

## Memory write rules

- Prefer stable facts over logs.
- Prefer skills for procedures.
- Prefer docs for project decisions.
- Prefer session search for old task history.
- Never store secrets.
- Never store raw sensitive personal data unless explicitly required and scoped.

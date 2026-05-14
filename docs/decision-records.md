# Decision Records

Decision records preserve hard-to-reconstruct reasoning so future agents do not re-litigate settled choices or repeat rejected paths.

## Purpose

Use decision records for durable trade-offs. They are not meeting notes, task logs, or a place to store every small preference.

## When to create one

Create a decision record only when all three are true:

1. **Hard to reverse** — changing the decision later has meaningful cost.
2. **Surprising without context** — a future maintainer would reasonably ask why this path was chosen.
3. **Real trade-off** — there were plausible alternatives and the chosen option has consequences.

If any condition is missing, use a lighter artifact such as a handoff, memory decision, issue note, or glossary entry.

## Minimal format

```text
# ADR-0001: Short decision title

## Status
Accepted | Superseded | Rejected | Proposed

## Context
Facts and constraints that made the decision necessary.

## Decision
The chosen path in one or two paragraphs.

## Alternatives considered
- Option A — why rejected.
- Option B — why rejected.

## Consequences
Expected benefits, costs, risks, and follow-up checks.

## Evidence
Links, files, commands, tests, incidents, user decisions, or artifacts checked.
```

## Operating rules

1. Read relevant decision records before proposing architecture or process changes.
2. If a new recommendation conflicts with an accepted record, name the conflict and explain what evidence changed.
3. Do not reopen a decision just because a different pattern is fashionable.
4. Supersede rather than silently editing history when the decision materially changes.
5. Keep decision records neutral and evidence-backed; do not name research sources unless the record is explicitly a comparison artifact.

## Rejection examples

Do not create a decision record for:

- "We will do this later."
- "This was too much work today."
- "The current implementation happened accidentally."
- "A transient bug was fixed."
- "A one-off preference applied to a single session."

## Good candidates

Create or update a decision record for:

- Choosing the memory source of truth.
- Selecting a validation or eval strategy.
- Defining a public-copy naming policy.
- Changing the command/skill lifecycle.
- Rejecting a recurring architecture option for a load-bearing reason.

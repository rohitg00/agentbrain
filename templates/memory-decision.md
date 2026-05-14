# Memory Decision

Use this artifact before writing, updating, retrieving, or rejecting durable context.

Schema: `schemas/memory-decision.schema.json`

Required fields: `candidate`, `decision`, `target_tier`, `evidence`, `freshness`, `privacy_review`, `rejected_material`, `next_use`.

Optional fields: `written_update`, `no_write_reason`, `follow_up`.

## Candidate

What fact, decision, procedure, source, artifact, or reminder is being considered?

## Decision

Choose one:

- `write`
- `update`
- `reject`
- `retrieve`
- `defer`

## Target Tier

Choose one:

- `profile` — stable user/project preference.
- `session-recall` — prior work history that should stay searchable, not always loaded.
- `project-doc` — versioned architecture, decisions, contracts, or roadmap.
- `skill` — reusable procedure or repeated failure prevention.
- `external-index` — large corpus retrieval where docs remain source of truth.
- `none` — rejected or deferred.

## Evidence

List checked files, commands, source links, tests, logs, user statements, or explicit assumptions.

## Freshness

- Scope:
- Expires or review after:

## Privacy Review

- Contains secret: yes/no
- Contains sensitive personal data: yes/no
- Action taken:

## Rejected Material

List noisy logs, temporary task progress, stale status, raw private data, secrets, or one-off details that should not become durable memory.

## Written Update or No-Write Reason

If writing/updating, include the exact neutral memory/doc/skill update.

If rejecting, explain why no durable write is appropriate.

## Next Use

Describe the future retrieval/use case. If there is no plausible future use, reject the memory.

## Follow-up

List any doc, skill, eval, validator, or index work required to keep the memory useful.

# Shared Language

Shared language keeps agents concise, consistent, and aligned with the codebase's domain model.

## Purpose

Use shared language to reduce ambiguity before planning or implementation. It is a glossary, not a requirements document, scratchpad, or architecture spec.

A good shared language file helps an agent know that two phrases refer to the same concept, or that one overloaded phrase actually names different concepts.

## Files

Use the simplest layout that fits the project:

```text
CONTEXT.md                  # single project glossary
CONTEXT-MAP.md              # optional map when multiple contexts exist
docs/adr/                   # decision records, not glossary entries
```

For multi-domain projects, `CONTEXT-MAP.md` should point to the glossary for each bounded area. Do not make every repository start with a map; create it only when one glossary becomes confusing.

## Entry format

Each entry should be short and operational:

```text
## Term

Definition: precise meaning in this project.

Use when: where this term applies.

Do not confuse with: nearby terms that are different.

Evidence: file, doc, issue, or decision that supports the definition.
```

## Operating rules

1. Read existing shared language before naming plans, modules, commands, templates, schemas, or skills.
2. If a user or artifact uses a term that conflicts with the glossary, stop and resolve the conflict before proceeding.
3. If a fuzzy phrase appears repeatedly, propose a canonical term and capture it after it is accepted.
4. Keep implementation details out of shared language. Put implementation decisions in a decision record.
5. Update shared language inline when a term is resolved; do not leave durable terminology only in chat.
6. Use the glossary vocabulary in artifacts so future agents can retrieve and reason with the same names.

## What belongs here

- Domain nouns and verbs.
- User-visible states and transitions.
- Short distinctions between similar concepts.
- Canonical names for recurring work products.
- Evidence-backed vocabulary that reduces repeated explanation.

## What does not belong here

- Temporary task status.
- Debug logs.
- Implementation trade-offs.
- Release notes.
- Personal preferences.
- Secrets, credentials, or private raw data.

## Failure modes

- Treating the glossary as a spec and hiding acceptance criteria in it.
- Creating a term without evidence or user confirmation.
- Letting two names drift for the same concept.
- Naming code from local implementation trivia instead of the domain concept.
- Forgetting to update shared language after a grilling or review session resolves a fuzzy term.

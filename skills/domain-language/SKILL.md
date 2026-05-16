---
name: domain-language
description: Use when project vocabulary is fuzzy, overloaded, disputed, or needed before naming docs, schemas, commands, skills, code, plans, or memory.
---
# domain-language

Lifecycle stage: INTAKE

Resolve project vocabulary before it leaks into durable artifacts.

## Trigger

Use when a request, plan, review, or artifact depends on a term that is ambiguous, overloaded, newly introduced, or likely to become durable project language.

Common triggers:

- Two names appear to describe the same concept.
- One word describes multiple concepts in different files or teams.
- A command, skill, schema, template, state, or document needs a durable name.
- A user corrects terminology or positioning.
- A glossary entry, memory note, or decision record might be needed.

Do not use this skill for temporary task status, private notes, logs, or implementation trivia that will not affect future understanding.

## When not to use
Do not use when this trigger is absent; choose the command or skill that owns the requested state, artifact, and verification gate.

## Inputs

Collect only evidence that can resolve the term:

- the user request or correction;
- existing glossary or shared-language docs;
- nearby docs, schemas, commands, templates, and tests;
- accepted decision records when terminology follows a trade-off;
- examples of the term in current repository artifacts.

If repo evidence answers the question, inspect it instead of asking. Ask only when the term changes user-facing meaning or the evidence is genuinely missing.

## Procedure

1. Locate existing uses of the term and likely aliases.
2. Decide whether the issue is vocabulary, a product requirement, or a durable trade-off.
3. Route vocabulary to shared language, requirements to the relevant brief or plan, and hard-to-reverse trade-offs to decision records.
4. Propose one canonical term with a short definition and rejected aliases.
5. Update only the smallest durable artifact needed.
6. Use the canonical term consistently in the current command, skill, schema, template, or doc slice.
7. Add or update validator/eval coverage when the terminology rule should not regress.

## Anti-Rationalization

- Do not treat the current implementation name as the domain term by default.
- Do not create a decision record just because a term changed; use one only for durable trade-offs.
- Do not hide acceptance criteria in a glossary entry.
- Do not preserve source-specific or vendor branding when the user asked for a neutral operator pattern.
- Do not add private raw data, secrets, temporary progress, or chat-only context to shared language.

## Verification

Before finishing, confirm:

- the canonical term has evidence or explicit user acceptance;
- rejected aliases are named when they are likely to recur;
- the term was routed to the right artifact type;
- affected docs, templates, schemas, or skills use the same term;
- validation or eval coverage exists when drift would be costly.

## Output Artifact

Return or update a concise domain-language decision:

```text
Term: <canonical term>
Definition: <project-specific meaning>
Use when: <scope>
Do not confuse with: <aliases or neighboring terms>
Evidence: <files, commands, user decision, or sources checked>
Blockers: <missing evidence, unresolved owner decision, or none>
Routed to: shared language | brief | plan | decision record | no durable write
Next action: <validator/eval/doc/code update if needed>
```

## Failure Modes

- Inventing project vocabulary without inspecting existing artifacts.
- Letting two aliases persist for the same concept.
- Using a glossary to store implementation decisions.
- Creating decision records for trivial or reversible naming choices.
- Copying external source branding into public repo copy.
- Leaving the resolved term only in chat, making the next agent rediscover it.

## Example

Trigger: overloaded or source-specific vocabulary could leak into durable artifacts. Action: inspect shared language, resolve canonical terms, and route trade-offs to decision records only when justified. Output artifact: domain language decision with blockers and next action. Verification: cite accepted term, rejected aliases, evidence, and target artifact.

A user says, "Add memory guidance," but the repo already separates session recall, durable project knowledge, and reusable skills.

Correct response:

1. Inspect existing memory docs and schemas.
2. Define the intended concept as "durable project knowledge" or "memory decision" rather than generic "memory."
3. Route recurring procedure into a skill, project facts into shared language or docs, and trade-offs into a decision record only if they are hard to reverse.
4. Add an eval or validator if future agents might store temporary task chatter as durable memory.

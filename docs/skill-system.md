# Skill System

A skill is a reusable operating procedure for an agent.

## Skill lifecycle

```text
Failure or repeated workflow
  ↓
Skill candidate
  ↓
Skill draft
  ↓
Evaluation against scenarios
  ↓
Install
  ↓
Use in real tasks
  ↓
Patch / consolidate / archive
```

## Skill quality bar

A good skill is:

- Triggerable by a clear situation
- Short enough to load into context
- Specific enough to prevent mistakes
- Opinionated about what not to do
- Verifiable through tests, examples, or checklists
- Maintained when reality changes

## Anti-patterns

- Giant prompt dumps
- Generic advice
- No trigger condition
- No verification
- No failure modes
- Naming tied to one model, vendor, or platform
- Skills that silently do writes without review

## Skill evaluation

Before installing a skill, test it against:

- Happy path
- Ambiguous input
- Missing context
- Hostile or unsafe request
- Edge-case constraints
- Output format requirements

## Skill consolidation

If three skills overlap, consolidate around the user intent, not the implementation detail.

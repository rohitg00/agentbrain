# Devex Engineering

Agent Brain treats developer experience as a reliability surface, not polish. A future agent should be able to install, validate, edit, review, and recover the repository without hidden chat context.

## Use When

Use this guidance when a change touches setup, validation, command routing, templates, schemas, CI, or maintainer workflows.

## Quality Bar

A devex change is acceptable only when it makes the next agent's safest path more obvious and more verifiable:

- install commands match CI;
- validation commands are copyable and current;
- generated files are ignored or rejected before commit;
- command outputs route to concrete templates or schemas;
- failures name the broken artifact and recovery command;
- public copy stays neutral and source names are scrubbed when required;
- handoffs include evidence, blockers, risks, and the smallest next action.

## Procedure

1. Start with the current failing or weak operator path.
2. Add or update a validator, test, or eval before relying on prose.
3. Update the smallest doc, command, template, schema, or skill that closes the gap.
4. Run the targeted test first, then the full quality gate.
5. Record the change as a small conventional commit.

## Anti-Patterns

- Adding a new command without a template-backed output artifact.
- Writing setup prose that does not match CI.
- Hiding recovery steps in chat instead of versioned docs.
- Treating docs-only changes as exempt from validation.
- Letting external source branding leak into public harness copy.

## Recovery Checklist

When developer experience breaks, inspect in this order:

1. `git status --short` and recent commits.
2. The failing test or validator message.
3. The affected command, template, schema, README entry, and harness doc.
4. The CI workflow for command drift.
5. The exact-name scrub target list for public-copy leakage.

Stop with a handoff if the recovery requires credentials, destructive cleanup, or approval that is not present.

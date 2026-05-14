# Skill Distillation

Skill distillation turns repeated agent work into a small, reusable operating procedure.

## When to distill

Create or update a skill when at least one of these is true:

- The same workflow has been repeated across multiple tasks.
- A failure would have been prevented by a written procedure.
- A command, template, or validator needs companion judgment rules.
- A reviewer keeps giving the same correction.

Do not distill one-off preferences, private context, or vague advice that cannot be verified.

## Source material

Use durable evidence, not memory alone:

- Completed task traces or review notes.
- Existing docs, commands, schemas, and templates.
- Validation failures and fixes.
- Explicit user constraints.

Remove private details, internal tool names, credentials, and vendor-specific instructions unless the repository section is explicitly scoped for comparison.

## Distillation loop

1. Name the repeated situation in one sentence.
2. Write the trigger before writing the procedure.
3. List the minimum inputs needed to act safely.
4. Convert the workflow into numbered steps.
5. Add verification checks that can catch regressions.
6. Add failure modes that describe how the skill can be misused.
7. Add one compact example.
8. Run repository validation before committing.

## Quality bar

A distilled skill is ready when it is:

- Triggerable from a real task.
- Short enough to load without crowding out task context.
- Specific enough to prevent the repeated mistake.
- Neutral in public copy.
- Covered by the repository validator structure checks.

## Maintenance

Update a skill when new evidence changes the workflow. Archive or merge skills that overlap rather than growing a parallel set of near-duplicates.

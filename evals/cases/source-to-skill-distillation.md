# Eval Case: Source to Skill Distillation

## User request

"This external workflow looks useful. Add the underlying idea to Agent Brain as a reusable skill."

## Expected behavior

- Reads the source as evidence, not as public copy to paste.
- Extracts the repeatable operator job: trigger, inputs, procedure, output artifact, verification, and failure modes.
- Names the result by the job-to-be-done instead of the source, vendor, or runtime.
- Keeps public docs, tests, commands, and commit messages neutral unless the user explicitly asks for a benchmark or comparison section.
- Adds or updates the smallest relevant skill, doc, template, schema, or eval case.
- Defines a quality gate that prevents regression, such as a validator rule, eval expectation, or checklist item.

## Harness route

Run `/brain-eval` against the command and skills named by the case, then score the output with `agent-output-verifier` for checked evidence, stop conditions, and next-state routing. Route files: `commands/brain-eval.md`, `skills/agent-output-verifier/SKILL.md`.

## Failure if

- Copies source branding or implementation-specific commands into public copy.
- Creates a broad framework instead of a small composable skill.
- Omits verification evidence or a regression guard.
- Adds the source as a dependency when only the workflow pattern was requested.
- Asks the user for information that can be gathered from the provided source or repository.

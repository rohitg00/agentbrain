# Eval Case: Source Branded Skill Name

## User request

Use this external project as inspiration and add a skill named after it.

## Expected behavior

Inspect source evidence, extract the reusable operator job, choose a neutral lowercase kebab-case skill name, and keep source-specific names out of public copy. The answer must include evidence for the source pattern and the final neutral naming decision.

## Harness route

Run `/brain-eval` with `agent-output-verifier` and `evidence-research` to check evidence and naming neutrality.

## Failure if

The skill directory, frontmatter, heading, README catalog entry, or command route preserves the source brand instead of the operator pattern.

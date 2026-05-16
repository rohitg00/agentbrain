# Eval Case: Skill Trigger Drift

## User request

Add this new reusable skill to the harness and make it easy for any runtime to choose it.

## Expected behavior

Compare the skill frontmatter description, Trigger section, skills catalog entry, command-loaded skill list, and Example evidence before accepting the skill. The agent should repair any mismatch so the same neutral trigger, runtime boundary, output artifact, and verification evidence are visible from every route.

## Harness route

Run `/brain-eval` with `qa-evidence` and `agent-output-verifier` to check trigger, catalog, artifact, and loaded-skill evidence.

## Failure if

The agent adds or edits a skill whose frontmatter says one trigger, Trigger section says another, catalog omits the trigger, examples cite a different route, or commands cannot load the skill that the docs tell the runtime to use.
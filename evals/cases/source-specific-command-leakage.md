# Eval Case: Source Specific Command Leakage

## User request

Learn from this external repo, thread, talk, or tool and add its workflow to Agent Brain.

## Expected behavior

The agent uses source evidence to identify the repeated operator job, then renames the workflow in neutral project language. It should preserve triggers, inputs, procedure, output artifact, verification evidence, and failure modes without copying source-specific commands, branding, or vendor-style positioning into public commands, skills, docs, templates, schemas, or evals.

## Harness route

Run `/brain-eval` with `agent-output-verifier` and `evidence-research` to check the evidence trail, artifact diff, and public-copy neutrality before accepting the distillation.

## Failure if

The agent copies source command names, source-branded headings, vendor-specific positioning, or one-off tool instructions into public harness artifacts instead of converting them into portable operator patterns.
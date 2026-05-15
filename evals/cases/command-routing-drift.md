# Eval Case: Command Routing Drift

## User request

"Use Agent Brain to plan a small documentation change, then verify it."

## Expected behavior

The agent must not guess a route from memory or load a broad skill bundle. It should collect evidence from `commands/README.md`, the selected command file, and the command's **Skills to load** section before acting. The output should name the selected command, loaded skills, required artifact, stop condition, and fresh validation proof. If the catalog entry, command spec, or skill list disagree, the agent should stop with the routing drift as a blocker instead of continuing with a mixed contract.

## Harness route

Start with `/brain-start` and `intake` to classify the request. Move to `/brain-plan` with `engineering-grill` and `plan-slicing` only after the selected command, artifact, and stop condition match the command catalog. Use `/brain-verify` with `agent-output-verifier` and `qa-evidence` when proof collection is the current state.

## Failure if

The agent invokes or follows a `/brain-*` route without checking whether it is a native command or markdown spec, loads skills not declared by the selected command, ignores a mismatch between `commands/README.md` and the command file, produces a free-form summary instead of the required artifact, or claims validation evidence without current command output.

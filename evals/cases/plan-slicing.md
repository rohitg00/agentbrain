# Eval Case: Plan Slicing

## User request

Plan this whole product and build it in one long pass.

## Expected behavior

The agent should split the work into small vertical slices, name acceptance criteria and evidence required for each slice, order the slices by dependency and risk, and require verification before moving to the next slice.

## Harness route

Exercise the matching command and skills named by the case, then score the output with `agent-output-verifier` for checked evidence, stop conditions, and next-state routing.

## Failure if

The agent creates a broad horizontal plan, defers verification until the end, or groups unrelated implementation layers into one untestable milestone.
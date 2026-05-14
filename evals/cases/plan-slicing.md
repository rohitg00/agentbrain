# Eval Case: Plan Slicing

## User request

Plan this whole product and build it in one long pass.

## Expected behavior

The agent should split the work into small vertical slices, name acceptance criteria and evidence required for each slice, order the slices by dependency and risk, and require verification before moving to the next slice.

## Failure if

The agent creates a broad horizontal plan, defers verification until the end, or groups unrelated implementation layers into one untestable milestone.
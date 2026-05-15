# /brain-plan

## Purpose

State: PLAN

Break approved work into small verifiable implementation slices.

## When to use

Use when the brief/design is strong enough to implement.

## Input contract

Product Brief, Design Brief, constraints, repo context.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `plan-slicing` to split work into small vertical slices with acceptance checks.
- `engineering-grill` when implementation risk or feasibility is still uncertain.

## Workflow

1. Start from an approved brief/design and list all constraints.
2. Use `plan-slicing` to split work into the smallest independently verifiable slices.
3. Attach acceptance checks, rollback notes, and dependencies to each slice.
4. Produce an Implementation Plan that a builder can execute without guessing.
5. Stop if the work is too broad, untestable, or missing a first reversible slice.

## Output

Required artifact: **Implementation Plan**.

The output must include:

- decision or finding,
- evidence,
- fresh validation proof,
- assumptions,
- risks,
- open questions,
- next recommended state.

## Stop conditions

Stop and ask for human input when:

- objectives, constraints, owner, or acceptance criteria are not defined,
- the plan cannot be sliced into independently verifiable steps,
- the first slice needs approvals, credentials, production access, or irreversible migration,
- risk ordering depends on a stakeholder priority trade-off,
- verification commands or rollback paths are unknown for the proposed work.

## Quality bar

A good `/brain-plan` run decomposes approved work into ordered vertical slices, gives each slice acceptance checks and rollback notes, and keeps unverified assumptions out of the build queue.

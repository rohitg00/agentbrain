# /brain-design

## Purpose

Define user flow, interface behavior, states, and edge cases.

## When to use

Use when a product brief needs UX or interaction design before planning.

## Input contract

Product Brief, user flow, constraints, risk list.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `design-grill` to challenge flows, states, edge cases, and failure paths.
- `engineering-grill` when the design depends on technical feasibility or reliability.

## Workflow

1. Define the user journey, interface states, empty states, errors, permissions, and edge cases.
2. Use `design-grill` to challenge flows and `engineering-grill` for feasibility risks.
3. Specify behavior before implementation details.
4. Produce a Design Brief with state transitions, acceptance checks, and unresolved risks.
5. Stop if critical states, accessibility, or failure paths are missing.

## Output

Required artifact: **Design Brief**.

The output must include:

- decision or finding,
- evidence,
- assumptions,
- risks,
- open questions,
- next recommended state.

## Stop conditions

Stop and ask for human input when:

- the user, scenario, constraints, or non-goals are missing,
- research evidence conflicts and a product/design trade-off needs owner judgment,
- the design would commit to public claims, brand direction, pricing, or irreversible IA,
- sensitive user data, accessibility risk, or policy risk needs specialist review,
- the requested artifact cannot be validated with available examples or acceptance criteria.

## Quality bar

A good `/brain-design` run compares viable approaches, names trade-offs and constraints, rejects unnecessary agentic complexity, and leaves the next implementation slice small enough to verify.

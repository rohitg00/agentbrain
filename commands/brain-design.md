# /brain-design

## Purpose

State: DESIGN

Define user flow, interface behavior, states, and edge cases.

## When to use

Use when a product brief needs UX or interaction design before planning.

## When not to use

Do not use when the interface, workflow, and failure paths are already specified well enough for implementation planning.

## Input contract

Product Brief, user flow, constraints, risk list, known facts, assumptions, evidence, and approval state.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `design-grill` to challenge flows, states, edge cases, and failure paths.
- `engineering-grill` when the design depends on technical feasibility or reliability.

## Workflow

1. Inspect `git status --short` and preserve user changes before modifying files, running write-capable tools, or trusting generated artifacts.
2. Treat `/brain-design` as a markdown command spec unless the active runtime proves native command support.
3. Define the user journey, interface states, empty states, errors, permissions, and edge cases.
4. Use `design-grill` to challenge flows and `engineering-grill` for feasibility risks.
5. Specify behavior before implementation details.
6. Produce a Design Brief with state transitions, acceptance checks, and unresolved risks.
7. Stop if critical states, accessibility, or failure paths are missing.

## Output

Required artifact: **Design Brief** using `templates/design-brief.md`.

The output must include:

- decision or finding,
- evidence,
- fresh validation proof,
- assumptions,
- risks,
- open questions,
- next recommended state.
- artifact path.

## Stop conditions

Stop and ask for human input when:

In noninteractive runs where the agent cannot ask questions, use the safest documented default only when it preserves scope and safety; otherwise stop with a blocker.

- the user, scenario, constraints, or non-goals are missing,
- research evidence conflicts and a product/design trade-off needs owner judgment,
- the design would commit to public claims, brand direction, pricing, or irreversible IA,
- sensitive user data, accessibility risk, or policy risk needs specialist review,
- the requested artifact cannot be validated with available examples or acceptance criteria.

## Quality bar

A good `/brain-design` run compares viable approaches, names trade-offs and constraints, rejects unnecessary agentic complexity, captures fresh validation proof, and leaves the next implementation slice small enough to verify.

## Example

User request: convert a scoped brief into interaction design. Selected command: `/brain-design`. Command file: `commands/brain-design.md`. Loaded skills: `design-grill` and `engineering-grill`. Skill files: `skills/design-grill/SKILL.md` and `skills/engineering-grill/SKILL.md`. Artifact: write `templates/design-brief.md`. Verification: capture flows, constraints, failure modes, evidence, risks, and fresh validation proof before routing to `/brain-plan`. Stop condition: stop if state, flow, edge-case, accessibility, or risk evidence is missing. Next state: PLAN.

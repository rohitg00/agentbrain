# /brain-brief

## Purpose

State: DESIGN

Convert evidence and decisions into a product brief.

## When to use

Use after intake, research, and grill have enough signal.

## When not to use

Do not use when the request still needs challenge, research, or a non-agent alternative review before scope is safe.

## Input contract

Problem, user, evidence, constraints, acceptance criteria, known facts, assumptions, and approval state.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `problem-grill` when the user, problem, or acceptance criteria are weak.
- `evidence-research` when brief claims need inspectable sources.

## Workflow

1. Start from checked evidence, decisions, constraints, and open questions.
2. Resolve or label missing user, problem, scope, and success criteria.
3. Use `problem-grill` for weak scope and `evidence-research` for claims.
4. Produce a Product Brief that names facts, assumptions, risks, non-goals, and next state.
5. Stop if the brief would hide uncertainty or convert guesses into requirements.

## Output

Required artifact: **Product Brief** using `templates/product-brief.md`.

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

In noninteractive runs where the agent cannot ask questions, use the safest documented default only when it preserves scope and safety; otherwise stop with a blocker.

- the target user, decision owner, or success metric for the brief is unnamed,
- the brief would depend on private customer, revenue, or analytics data that is not available,
- evidence is too weak to choose a product direction,
- the next step commits the team to roadmap, pricing, launch, or public positioning,
- the user must choose between materially different product bets.

## Quality bar

A good `/brain-brief` run produces a schema-aligned product brief with a named user, source-backed problem evidence, explicit non-goals, acceptance criteria, unresolved risks, and fresh validation proof before any build work starts.

## Example

User request: turn accepted intake facts into product scope. Selected command: `/brain-brief`. Loaded skills: `problem-grill` and `evidence-research`. Artifact: write `templates/product-brief.md`. Verification: cite checked evidence, assumptions, risks, and fresh validation proof before routing to `/brain-design` or stopping with a blocker. Stop condition: stop if user/problem evidence or acceptance criteria are missing. Next state: DESIGN.

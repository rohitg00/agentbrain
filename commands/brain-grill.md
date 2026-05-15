# /brain-grill

## Purpose

State: CHALLENGE

Stress-test assumptions before planning or building.

## When to use

Use when the idea, brief, design, or plan has unresolved assumptions.

## Input contract

Artifact to challenge plus known constraints and evidence.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `problem-grill` for problem and user assumptions.
- `market-grill` for demand, alternatives, and positioning assumptions.
- `design-grill` for interface, state, and edge-case assumptions.
- `engineering-grill` for feasibility, failure-mode, and implementation assumptions.

## Workflow

1. Identify which assumptions are product, market, design, engineering, safety, or launch risks.
2. Load the relevant grill skills and challenge the strongest weak points first.
3. Write rebuttals, failure modes, counterexamples, and kill criteria.
4. Produce a Grill Report with must-fix blockers and the safest next state.
5. Stop if the idea should be killed, narrowed, or rerouted before planning.

## Output

Required artifact: **Grill Report**.

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

- code/docs cannot answer a blocking question and the user is unavailable,
- the problem owner, target user, constraints, or decision deadline are unknown,
- continuing would turn questioning into implementation without an approved spec,
- the request involves secrets, legal/compliance, medical, financial, or safety-sensitive facts,
- the next question would ask for information already retrievable from repository evidence.

## Quality bar

A good `/brain-grill` run asks only the few blocking questions that change the decision, gives recommended answers where useful, captures verified decisions, and records fresh validation proof instead of drifting into generic discovery.

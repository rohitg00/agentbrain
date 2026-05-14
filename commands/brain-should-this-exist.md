# /brain-should-this-exist

## Purpose

State: DECIDE

Decide whether the idea should exist and whether it should be agentic.

## When to use

Use before planning any new product, feature, workflow, or automation.

## Input contract

Product idea, target user, current workaround, desired outcome.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `problem-grill` to test whether the problem is real, specific, and worth solving.
- `market-grill` when demand, audience, or alternatives are unclear.

## Workflow

1. Name the target user, job, pain, current alternative, and success metric.
2. Test simpler non-agent options before proposing an agent.
3. Use `problem-grill` and `market-grill` to find kill criteria, demand gaps, and risk.
4. Produce a Non-Agent Alternative Review with decision, evidence, risks, and next state.
5. Stop if the user/problem is undefined or the idea lacks measurable value.

## Output

Required artifact: **Non-Agent Alternative Review**.

The output must include:

- decision or finding,
- evidence,
- assumptions,
- risks,
- open questions,
- next recommended state.

## Stop conditions

Stop and ask for human input when:

- the target user, repeated job, or non-agent baseline is not concrete,
- a simple checklist, script, form, dashboard, or process change may solve the need with less risk,
- the agent would need broad autonomy, hidden memory, credentials, or policy-sensitive access,
- expected value depends on unsupported adoption, accuracy, or cost claims,
- the decision requires stakeholder appetite for complexity, maintenance, or operational risk.

## Quality bar

A good `/brain-should-this-exist` run challenges whether the requested agent feature should exist, compares non-agent alternatives, names the concrete user and failure mode, and blocks vague automation.

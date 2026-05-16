# /brain-should-this-exist

## Purpose

State: DECIDE

Decide whether the idea should exist and whether it should be agentic.

## When to use

Use before planning any new product, feature, workflow, or automation.

## When not to use

Do not use when the user has already provided source-backed problem evidence, a non-agent alternative review, and explicit approval to proceed.

## Input contract

Product idea, target user, current workaround, desired outcome, known facts, assumptions, constraints, evidence, and approval state.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `problem-grill` to test whether the problem is real, specific, and worth solving.
- `market-grill` when demand, audience, or alternatives are unclear.

## Workflow

1. Inspect `git status --short` and preserve user changes before modifying files, running write-capable tools, or trusting generated artifacts.
2. Treat `/brain-should-this-exist` as a markdown command spec unless the active runtime proves native command support.
3. Name the target user, job, pain, current alternative, and success metric.
4. Test simpler non-agent options before proposing an agent.
5. Use `problem-grill` and `market-grill` to find kill criteria, demand gaps, and risk.
6. Produce a Non-Agent Alternative Review with decision, evidence, risks, and next state.
7. Stop if the user/problem is undefined or the idea lacks measurable value.

## Output

Required artifact: **Non-Agent Alternative Review** using `templates/non-agent-alternative-review.md`.

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

- the target user, repeated job, or non-agent baseline is not concrete,
- a simple checklist, script, form, dashboard, or process change may solve the need with less risk,
- the agent would need broad autonomy, hidden memory, credentials, or policy-sensitive access,
- expected value depends on unsupported adoption, accuracy, or cost claims,
- the decision requires stakeholder appetite for complexity, maintenance, or operational risk.

## Quality bar

A good `/brain-should-this-exist` run challenges whether the requested agent feature should exist, compares non-agent alternatives, names the concrete user and failure mode, records fresh validation proof, and blocks vague automation.

## Example

User request: decide whether a requested agent workflow should exist. Selected command: `/brain-should-this-exist`. Command file: `commands/brain-should-this-exist.md`. Loaded skills: `problem-grill` and `market-grill`. Skill files: `skills/problem-grill/SKILL.md` and `skills/market-grill/SKILL.md`. Artifact: write `templates/non-agent-alternative-review.md`. Verification: compare user evidence, non-agent alternatives, costs, risks, and fresh validation proof before continuing to `/brain-research` or stopping. Stop condition: stop if non-agent alternatives, user evidence, risk, or success criteria are missing. Next state: RESEARCH.

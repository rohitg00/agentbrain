---
name: market-grill
description: Use when a product idea needs pressure-testing against alternatives, category, urgency, and distribution.
---

# market-grill

## Trigger

Use when a product direction depends on adoption or positioning.

## When not to use
Do not use when this trigger is absent; choose the command or skill that owns the requested state, artifact, and verification gate.

## Inputs

- User request or current artifact.
- Known constraints and context.
- Relevant evidence or source links, if available.
- Current Agent Brain state.

## Procedure

1. State the current state and target artifact.
2. Identify missing blockers and ask at most three blocking questions.
3. Separate facts, assumptions, hypotheses, and open questions.
4. Apply the anti-rationalization table below.
5. Produce the required artifact: **Market Grill Report**.
6. Add evidence, risks, decision, and next state.

## Anti-Rationalization

| Shortcut | Rebuttal |
|---|---|
| "This is obvious." | Write the assumption and evidence. If you cannot, it is not obvious. |
| "We can do this later." | If the missing step changes the decision, do it now or state the risk. |
| "The user wants speed." | Reduce scope; do not skip the quality bar. |
| "This does not need verification." | Every important claim or behavior needs proof. |

## Verification

- Required artifact exists and is named.
- Facts, assumptions, and open questions are separated.
- Evidence or evidence gaps are explicit.
- Next state is stated.
- Stop conditions are honored.

## Output Artifact

Market Grill Report

The artifact should be concise, auditable, and include evidence, blockers, and next action so another agent can resume.

## Failure Modes

- Producing advice instead of an artifact.
- Accepting user assumptions without challenge.
- Skipping evidence because the task feels simple.
- Recommending an agent when a simpler system is enough.
- Hiding risks or open questions.

## Example

Trigger: market or positioning claim lacks evidence. Action: identify buyer, user, alternatives, proof needed, and neutral messaging boundaries. Output artifact: `templates/grill-report.md` with blockers and next action. Verification: cite category evidence, rejected claims, and open market questions.

A request says, "Position this as the default harness for teams." The skill should identify the buyer/user, alternative non-agent workflows, proof needed for adoption claims, and neutral messaging boundaries, then produce a market grill report that separates evidence from aspiration.

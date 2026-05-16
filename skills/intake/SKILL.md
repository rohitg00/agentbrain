---
name: intake
description: Use when raw intent must be captured and routed to the right next state.
---

# intake

Lifecycle stage: INTAKE

## Trigger

Use when a request is vague, new, or missing context.

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
5. Produce the required artifact: **Intake Summary**.
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

Intake Summary

Use `templates/intake-summary.md`. The artifact should be concise, auditable, and include evidence, blockers, and next action so another agent can resume.

## Failure Modes

- Producing advice instead of an artifact.
- Accepting user assumptions without challenge.
- Skipping evidence because the task feels simple.
- Recommending an agent when a simpler system is enough.
- Hiding risks or open questions.

## Example

Trigger: raw request enters the harness. Action: capture facts, assumptions, constraints, missing evidence, approval state, and likely next command before deeper work. Output artifact: `templates/intake-summary.md` with blockers and next action. Verification: cite routing evidence and the safest noninteractive default when follow-up is impossible.

A user says, "Make the harness better." Intake should capture known facts, assumptions, constraints, missing evidence, approval state, and likely next command; in a scheduled run, choose the safest documented default and create an intake summary rather than asking a broad follow-up.

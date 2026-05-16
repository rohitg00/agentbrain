---
name: design-grill
description: Use when a design needs pressure-testing for UX, information architecture, states, and accessibility.
---

# design-grill

## Trigger

Use before implementing user-facing flows.

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
5. Produce the required artifact: **Design Grill Report**.
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

Design Grill Report

Use `templates/grill-report.md` for a concise, auditable artifact with evidence, blockers, and next action so another agent can resume.

## Failure Modes

- Producing advice instead of an artifact.
- Accepting user assumptions without challenge.
- Skipping evidence because the task feels simple.
- Recommending an agent when a simpler system is enough.
- Hiding risks or open questions.

## Example

Trigger: workflow or interface design has unclear states, users, or failure paths. Action: pressure-test UX, information architecture, accessibility, edge states, and safer non-agent alternatives. Output artifact: `templates/grill-report.md` with blockers and next action. Verification: cite flows reviewed, rejected assumptions, accessibility checks, and remaining risks.

Input: "Build an assistant that handles customer refunds."

Better response pattern:

1. identify this as high-risk automation,
2. ask who approves refunds and what policies apply,
3. consider non-agent alternatives like form plus approval queue,
4. require human-in-loop gate,
5. produce the relevant artifact and next state instead of building immediately.

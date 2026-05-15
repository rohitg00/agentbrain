---
name: question-ladder
description: Use when uncertainty remains and the minimum useful sequence of questions should be asked.
---

# question-ladder

## Trigger

Use when missing answers block product, design, or engineering decisions.

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
5. Produce the required artifact: **Open Questions plus assumptions**.
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

Open Questions plus assumptions

The artifact should be concise, auditable, and include evidence, blockers, and next action so another agent can resume.

## Failure Modes

- Producing advice instead of an artifact.
- Accepting user assumptions without challenge.
- Skipping evidence because the task feels simple.
- Recommending an agent when a simpler system is enough.
- Hiding risks or open questions.

## Example

Trigger: uncertainty remains after retrievable evidence has been checked. Action: ask the smallest useful next question or choose the safest documented default in noninteractive mode. Output artifact: intake or grill artifact with blockers and next action. Verification: cite evidence checked, why the question changes action, and stop condition if no answer is available.

A plan is blocked by "needs approval." The ladder should ask the smallest next question first: what side effect is approval-gated, what safe read-only alternative exists, what assumption can unblock planning, and what evidence would change the route.

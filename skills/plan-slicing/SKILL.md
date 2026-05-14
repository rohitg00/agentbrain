---
name: plan-slicing
description: Use when broad work needs to be broken into small verifiable slices.
---

# plan-slicing

## Trigger

Use after a brief/design is accepted and before build.

## Inputs

- User request or current artifact.
- Known constraints and context.
- Relevant evidence or source links, if available.
- Current Agent Brain state.

## Procedure

1. State the current state and target artifact.
2. Identify missing blockers and ask at most three blocking questions.
3. Separate facts, assumptions, hypotheses, and open questions.
4. Split broad work into vertical slices small enough to verify independently.
5. For each slice, name the user-visible outcome, files likely touched, acceptance checks, and verification command.
6. Apply the anti-rationalization table below.
7. Produce the required artifact: **Implementation Plan**.
8. Add evidence, risks, decision, and next state.

## Anti-Rationalization

| Shortcut | Rebuttal |
|---|---|
| "This is obvious." | Write the assumption and evidence. If you cannot, it is not obvious. |
| "We can do this later." | If the missing step changes the decision, do it now or state the risk. |
| "The user wants speed." | Reduce scope; do not skip the quality bar. |
| "This does not need verification." | Every important claim or behavior needs proof. |

## Verification

- Required artifact exists and is named.
- Every slice has acceptance checks and a verification command.
- Facts, assumptions, and open questions are separated.
- Evidence or evidence gaps are explicit.
- Next state is stated.
- Stop conditions are honored.

## Output Artifact

Implementation Plan

The artifact should be concise, auditable, and ready for the next Agent Brain state. Each slice should be independently runnable by another agent without private context.

## Failure Modes

- Producing advice instead of an artifact.
- Accepting user assumptions without challenge.
- Skipping evidence because the task feels simple.
- Recommending an agent when a simpler system is enough.
- Hiding risks or open questions.
- Listing tasks without acceptance checks or a verification command.

## Example

Input: "Build an assistant that handles customer refunds."

Better response pattern:

1. identify this as high-risk automation,
2. ask who approves refunds and what policies apply,
3. consider non-agent alternatives like form plus approval queue,
4. require human-in-loop gate,
5. produce the relevant artifact and next state instead of building immediately.

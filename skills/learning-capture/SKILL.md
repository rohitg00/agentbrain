---
name: learning-capture
description: Use when repeated wins or failures should become durable memory, wiki, or skill updates.
---

# learning-capture

## Trigger

Use after completing, killing, or repeating a workflow.

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
5. Produce the required artifact: **Learning Capture**.
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

Learning Capture

Use `templates/learning-capture.md`. The artifact should be concise, auditable, and include evidence, blockers, and next action so another agent can resume.

## Failure Modes

- Producing advice instead of an artifact.
- Accepting user assumptions without challenge.
- Skipping evidence because the task feels simple.
- Recommending an agent when a simpler system is enough.
- Hiding risks or open questions.

## Example

Trigger: repeated success or failure should become durable guidance. Action: capture only reusable procedure, reject transient logs, and route the learning to docs, validator, eval, or skill updates. Output artifact: `templates/learning-capture.md` with blockers and next action. Verification: cite recurrence evidence, changed artifact, and validation command.

After a CI failure is fixed by adding a missing catalog rule, capture the reusable rule as validator guidance or a skill update, reject transient run IDs and timestamps, record the verification commands, and produce a learning capture only if the procedure will prevent a future repeat.

---
name: engineering-grill
description: Use when an engineering plan needs pressure-testing for architecture, complexity, data, risk, and operability.
---

# engineering-grill

Lifecycle stage: CHALLENGE

## Trigger

Use before committing to implementation approach.

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
5. Produce the required artifact: **Engineering Grill Report**.
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

Engineering Grill Report

Use `templates/grill-report.md` for a concise, auditable artifact with evidence, blockers, and next action so another agent can resume.

## Failure Modes

- Producing advice instead of an artifact.
- Accepting user assumptions without challenge.
- Skipping evidence because the task feels simple.
- Recommending an agent when a simpler system is enough.
- Hiding risks or open questions.

## Example

Trigger: an engineering plan needs pressure-testing before implementation. Action: compare scripts, checklists, human review, and agent workflows; require file scope, rollback, and validation proof. Output artifact: `templates/grill-report.md` with blockers and next action. Verification: cite architecture risks, data risks, operability checks, and smallest safe path.

A request says, "Add recurring workspace cleanup." The skill should compare a scheduled script, manual checklist, and agent-run cleanup; require file-scope, dry-run, rollback, and validation proof; then produce an engineering grill report that recommends the smallest safe implementation path instead of jumping straight to code.

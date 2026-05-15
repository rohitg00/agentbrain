---
name: qa-evidence
description: Use when behavior needs concrete proof before review, merge, or shipment.
---

# qa-evidence

## Trigger

Use after build or before review/ship.

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
5. Produce the required artifact: **QA Evidence**.
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

QA Evidence

Use `templates/qa-evidence.md`. The artifact should be concise, auditable, and include evidence, blockers, and next action so another agent can resume.

## Failure Modes

- Producing advice instead of an artifact.
- Accepting user assumptions without challenge.
- Skipping evidence because the task feels simple.
- Recommending an agent when a simpler system is enough.
- Hiding risks or open questions.

## Example

Trigger: a build claims a route or behavior works. Action: tie the claim to exact commands, checked artifacts, schema validation, diff checks, scrub results, and blocked runtime commands. Output artifact: `templates/qa-evidence.md` with blockers and next action. Verification: cite command output, artifact path, expected result, and unresolved gaps.

A build claims, "The command router works." QA evidence should name the exact command, fixture or runtime checked, expected artifact, schema validation, git diff check, public-copy scrub, and any blocked runtime commands before accepting the claim.

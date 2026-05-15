---
name: wiki-maintenance
description: Use when source-backed project knowledge needs to be created, refreshed, or corrected.
---

# wiki-maintenance

## Trigger

Use when ingesting sources, resolving contradictions, or preserving synthesis.

## When not to use
Do not use this skill when a simpler checklist, script, or existing command handles the work safely.

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
5. Produce the required artifact: **Wiki Update**.
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

Wiki Update

The artifact should be concise, auditable, and ready for the next Agent Brain state.

## Failure Modes

- Producing advice instead of an artifact.
- Accepting user assumptions without challenge.
- Skipping evidence because the task feels simple.
- Recommending an agent when a simpler system is enough.
- Hiding risks or open questions.

## Example

A new source contradicts an existing project note. The skill should preserve both claims with provenance, mark freshness and confidence, update only the relevant wiki section, and record a recheck trigger instead of overwriting durable knowledge with unverified synthesis.

---
name: wiki-maintenance
description: Use when source-backed project knowledge needs to be created, refreshed, or corrected.
---

# wiki-maintenance

## Trigger

Use when ingesting sources, resolving contradictions, or preserving synthesis.

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

Use `templates/wiki-update.md`. The artifact should be concise, auditable, and include evidence, blockers, and next action so another agent can resume.

## Failure Modes

- Producing advice instead of an artifact.
- Accepting user assumptions without challenge.
- Skipping evidence because the task feels simple.
- Recommending an agent when a simpler system is enough.
- Hiding risks or open questions.

## Example

Trigger: source-backed project knowledge needs a durable update. Action: preserve provenance, confidence, freshness, and recheck triggers while updating only the relevant wiki section. Output artifact: `templates/wiki-update.md` with blockers and next action. Verification: cite changed paths, sources checked, stale claims rejected, and validation evidence.

A new source contradicts an existing project note. The skill should preserve both claims with provenance, mark freshness and confidence, update only the relevant wiki section, and record a recheck trigger instead of overwriting durable knowledge with unverified synthesis.

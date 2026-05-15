# /brain-research

## Purpose

State: RESEARCH

Turn sources and discussion into a claim ledger.

## When to use

Use when the decision depends on external evidence or unfamiliar domain context.

## When not to use

Do not use when authoritative sources are unavailable and the next safe action is to stop with a blocker instead of speculating.

## Input contract

Research question, scope, source constraints, freshness needs, known facts, assumptions, evidence, and approval state.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `evidence-research` to turn claims into source-backed evidence.
- `wiki-maintenance` when the research should update durable project knowledge.

## Workflow

1. Convert the question into explicit claims to verify.
2. Gather source-backed evidence and separate facts from assumptions.
3. Use `evidence-research`; add `wiki-maintenance` only for durable project knowledge.
4. Produce a Research Claim Ledger with citations, confidence, contradictions, and gaps.
5. Stop if sources are stale, unavailable, or insufficient for the requested confidence.

## Output

Required artifact: **Research Claim Ledger** using `templates/research-claim-ledger.md`.

The output must include:

- decision or finding,
- evidence,
- fresh validation proof,
- assumptions,
- risks,
- open questions,
- next recommended state.

## Stop conditions

Stop and ask for human input when:

In noninteractive runs where the agent cannot ask questions, use the safest documented default only when it preserves scope and safety; otherwise stop with a blocker.

- the claim cannot be grounded in primary or authoritative evidence,
- the source requires login, paywalled/private context, or unverifiable social proof,
- the research would introduce source branding or vendor names into public copy without an approved comparison section,
- the answer depends on current facts that cannot be checked from available sources,
- conflicting evidence changes the recommended next state or risk level.

## Quality bar

A good `/brain-research` run produces a claim ledger with inspectable sources, separates leads from verified facts, flags weak evidence, records fresh validation proof, and keeps public copy in neutral pattern language.

## Example

User request: resolve a claim that depends on evidence. Selected command: `/brain-research`. Loaded skills: `evidence-research` and `wiki-maintenance`. Artifact: write `templates/research-claim-ledger.md`. Verification: inspect local files and source-backed references, separate facts from assumptions, record provenance, and route findings to `/brain-grill` or `/brain-brief` with fresh validation proof.

# /brain-research

## Purpose

Turn sources and discussion into a claim ledger.

## When to use

Use when the decision depends on external evidence or unfamiliar domain context.

## Input contract

Research question, scope, source constraints, freshness needs.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

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

Required artifact: **Research Claim Ledger**.

The output must include:

- decision or finding,
- evidence,
- assumptions,
- risks,
- open questions,
- next recommended state.

## Stop conditions

Stop and ask for human input when:

- the next step changes public state,
- the next step is destructive or irreversible,
- credentials or private data are required,
- evidence is too weak for the requested confidence,
- the user must choose between materially different directions.

## Quality bar

A good `/brain-research` run produces a claim ledger with inspectable sources, separates leads from verified facts, flags weak evidence, and keeps public copy in neutral pattern language.

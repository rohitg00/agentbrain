# /brain-wiki

## Purpose

Maintain source-backed project knowledge.

## When to use

Use when ingesting sources or updating durable project knowledge.

## Input contract

Source material, target knowledge area, staleness or ownership notes.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk.

## Skills to load

- `wiki-maintenance` to update project knowledge from checked sources.
- `evidence-research` when the update depends on external claims or freshness.

## Workflow

1. Check the source material, target knowledge area, owner, and staleness risk.
2. Use `wiki-maintenance` and `evidence-research` to ground each durable statement.
3. Update project knowledge with citations, decisions, and open questions.
4. Produce a Wiki Update summarizing changed pages, evidence, and follow-up.
5. Stop if sources are missing, conflicting, or too weak for a durable knowledge update.

## Output

Required artifact: **Wiki Update**.

The output must include:

- decision or finding,
- evidence,
- assumptions,
- risks,
- open questions,
- next recommended state.

## Stop conditions

Stop and ask for human input when:

- the proposed wiki fact lacks a stable source, owner, or freshness date,
- the update would expose private project context, secrets, customer data, or internal-only notes,
- existing docs conflict and the durable source of truth is unclear,
- the change would replace maintained guidance instead of linking or reconciling it,
- no validator, review, or freshness check can keep the wiki entry from going stale.

## Quality bar

A good `/brain-wiki` run updates durable project knowledge only after evidence is checked, links it to the relevant command or skill, and avoids turning temporary session context into permanent doctrine.

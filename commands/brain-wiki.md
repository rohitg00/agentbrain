# /brain-wiki

## Purpose

State: LEARN

Maintain source-backed project knowledge.

## When to use

Use when ingesting sources or updating durable project knowledge.

## Input contract

Source material, target knowledge area, staleness or ownership notes, known facts, assumptions, constraints, evidence, and approval state.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `wiki-maintenance` to update project knowledge from checked sources.
- `activity-recap` when local repository history or recent changes must be summarized before updating knowledge.
- `evidence-research` when the update depends on external claims or freshness.

## Workflow

1. Check the source material, target knowledge area, owner, and staleness risk.
2. Use `wiki-maintenance`; add `activity-recap` for recent local repo evidence and `evidence-research` for external claims or freshness.
3. Update project knowledge with citations, decisions, and open questions.
4. Produce a Wiki Update summarizing changed pages, evidence, and follow-up.
5. Stop if sources are missing, conflicting, or too weak for a durable knowledge update.

## Output

Required artifact: **Wiki Update** using `templates/wiki-update.md`.

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

- the proposed wiki fact lacks a stable source, owner, or freshness date,
- the update would expose private project context, secrets, customer data, or internal-only notes,
- existing docs conflict and the durable source of truth is unclear,
- the change would replace maintained guidance instead of linking or reconciling it,
- no validator, review, or freshness check can keep the wiki entry from going stale.

## Quality bar

A good `/brain-wiki` run updates durable project knowledge only after evidence and fresh validation proof are checked, links it to the relevant command or skill, and avoids turning temporary session context into permanent doctrine.

## Example

User request: update durable project guidance from checked evidence. Selected command: `/brain-wiki`. Loaded skills: `wiki-maintenance`, `activity-recap`, and `evidence-research`. Artifact: write `templates/wiki-update.md`. Verification: preserve neutral copy, cite source-backed evidence, validate changed docs, and record fresh validation proof before handoff.

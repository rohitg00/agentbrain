# /brain-learn

## Purpose

State: LEARN

Capture reusable learning from a completed or failed loop.

## When to use

Use after repeated success/failure, a tricky fix, or a shipped workflow.

## When not to use

Do not use for one-off session notes, stale status summaries, secrets, or raw private data that should not become durable memory.

## Input contract

Repeated outcome, trace, decision, proposed durable update, known facts, assumptions, constraints, evidence, and approval state.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `learning-capture` from `skills/learning-capture/SKILL.md` to convert repeated outcomes into durable knowledge.
- `context-memory` from `skills/context-memory/SKILL.md` to decide whether the lesson belongs in memory, a skill, a doc, a template, an eval, or nowhere.
- `wiki-maintenance` from `skills/wiki-maintenance/SKILL.md` when the update belongs in source-backed project context.

## Workflow

1. Inspect `git status --short` and preserve user changes before modifying files, running write-capable tools, or trusting generated artifacts.
2. Treat `/brain-learn` as a markdown command spec unless the active runtime proves native command support.
3. Identify the repeated outcome, failure mode, correction, or durable decision.
4. Decide whether it belongs in memory, wiki, skill, template, eval, or nowhere.
5. Use `learning-capture` and `context-memory`; add `wiki-maintenance` for source-backed project knowledge.
6. Produce Learning Capture with evidence, scope, update target, and next state.
7. Stop if the lesson is temporary task progress, private data, or stale implementation status.

## Output

Required artifact: **Learning Capture** using `templates/learning-capture.md`.

The output must include:

- decision or finding,
- evidence,
- fresh validation proof,
- assumptions,
- risks,
- open questions,
- next recommended state.
- artifact path.

## Stop conditions

Stop and ask for human input when:

In noninteractive runs where the agent cannot ask questions, use the safest documented default only when it preserves scope and safety; otherwise stop with a blocker.

- the lesson is temporary task state rather than durable project behavior,
- the source contains private data, secrets, credentials, or raw conversation content,
- the pattern is too source-specific to become a neutral command, skill, template, or validator,
- the capture would overwrite existing guidance without evidence that it is stale,
- no regression test, eval, or validator can protect the learned behavior.

## Quality bar

A good `/brain-learn` run distills a durable operator lesson into neutral guidance, updates the smallest relevant skill, doc, template, or eval, includes fresh validation proof, and avoids storing source-specific branding as project doctrine.

## Example

User request: preserve a repeated failure as reusable guidance. Selected command: `/brain-learn`. Command file: `commands/brain-learn.md`. Loaded skills: `learning-capture`, `context-memory`, and `wiki-maintenance`. Skill files: `skills/learning-capture/SKILL.md`, `skills/context-memory/SKILL.md`, and `skills/wiki-maintenance/SKILL.md`. Artifact: write `templates/learning-capture.md`. Verification: update the matching skill, validator, or memory guidance with neutral copy and fresh validation proof before handoff. Stop condition: stop if the lesson is temporary chatter, private data, or not reusable. Next state: LEARN.

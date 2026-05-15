# /brain-learn

## Purpose

State: LEARN

Capture reusable learning from a completed or failed loop.

## When to use

Use after repeated success/failure, a tricky fix, or a shipped workflow.

## Input contract

Repeated outcome, trace, decision, and proposed durable update.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `learning-capture` to convert repeated outcomes into durable knowledge.
- `context-memory` to decide whether the lesson belongs in memory, a skill, a doc, a template, an eval, or nowhere.
- `wiki-maintenance` when the update belongs in source-backed project context.

## Workflow

1. Identify the repeated outcome, failure mode, correction, or durable decision.
2. Decide whether it belongs in memory, wiki, skill, template, eval, or nowhere.
3. Use `learning-capture` and `context-memory`; add `wiki-maintenance` for source-backed project knowledge.
4. Produce Learning Capture with evidence, scope, update target, and next state.
5. Stop if the lesson is temporary task progress, private data, or stale implementation status.

## Output

Required artifact: **Learning Capture**.

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

- the lesson is temporary task state rather than durable project behavior,
- the source contains private data, secrets, credentials, or raw conversation content,
- the pattern is too source-specific to become a neutral command, skill, template, or validator,
- the capture would overwrite existing guidance without evidence that it is stale,
- no regression test, eval, or validator can protect the learned behavior.

## Quality bar

A good `/brain-learn` run distills a durable operator lesson into neutral guidance, updates the smallest relevant skill, doc, template, or eval, includes fresh validation proof, and avoids storing source-specific branding as project doctrine.

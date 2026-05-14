---
name: brain-learn
description: Convert repeated failures and successful workflows into durable skills.
version: 0.1.0
---

# Brain Learn

## Trigger

Use when a task required trial and error, the user corrected the agent, a workflow repeated, or a failure mode should not recur.

## Procedure

1. Summarize what happened.
2. Decide whether the learning is a fact, project doc, session note, or skill.
3. If it is procedural, write a skill with trigger, procedure, pitfalls, and verification.
4. Add examples.
5. Add an evaluation scenario.
6. Keep it short enough to load.

## Pitfalls

- Do not save temporary progress as durable memory.
- Do not create a skill for a one-off.
- Do not store secrets.
- Do not overwrite a human-written skill without review.

## Verification

The next agent facing the same situation should avoid the previous mistake.

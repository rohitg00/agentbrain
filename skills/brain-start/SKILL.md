---
name: brain-start
description: Turn a raw idea into a questioned, grilled, and scoped product brief.
version: 0.1.0
---

# Brain Start

## Trigger

Use when the user has an idea, feature request, product concept, repo concept, or vague “build this” prompt.

## Procedure

1. Restate the idea in one sentence.
2. Identify missing context.
3. Ask up to 5 high-leverage questions. If the user wants speed, ask 3.
4. Run the grilling protocol.
5. Produce a product brief using `templates/product-brief.md`.
6. Recommend one next step: `/brain-plan`, `/brain-design`, `/brain-eng`, or `/brain-grill`.

## Pitfalls

- Do not start implementation from a vague prompt.
- Do not ask a long questionnaire when 3 questions unblock progress.
- Do not flatter weak ideas; improve them.
- Do not bury assumptions.

## Verification

A successful output has a named user, clear job, v0 scope, success metric, risks, and next step.

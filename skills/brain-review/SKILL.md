---
name: brain-review
description: Review product, design, engineering, security, QA, and launch readiness.
version: 0.1.0
---

# Brain Review

## Trigger

Use before merging, shipping, publishing, or declaring a task done.

## Procedure

1. Identify artifact under review.
2. Check against `docs/review-gates.md`.
3. Find correctness, UX, security, maintainability, and scope issues.
4. Classify findings: must-fix, should-fix, nice-to-have.
5. Require evidence for “done”.
6. Approve only if must-fix findings are resolved.

## Pitfalls

- Do not say “looks good” without evidence.
- Do not focus only on code style.
- Do not approve missing tests for risky logic.

## Verification

The review includes actionable findings with severity and exact remediation.

# Qa Evidence

Schema fields: `checks`. Each check records a name, method, result, and evidence.

Use this when collecting verification proof for review, shipping, or an agent-output trust decision. Keep every check tied to an inspectable artifact rather than a summary.

## Checks

Repeat this block for each verification check.

### Check: <name>

- **Name:** Short label for the check.
- **Method:** Exact command, manual journey, source lookup, trace, screenshot, log, or file inspection used.
- **Result:** `pass`, `fail`, `blocked`, or `not_applicable`.
- **Evidence:** Specific output, path, log excerpt, screenshot reference, source URL, commit, or blocker that supports the result.

## Notes

- Prefer direct proof over paraphrase.
- Mark unchecked claims as `blocked` instead of filling them with assumptions.
- Re-run stale checks when code, docs, schemas, templates, commands, skills, evals, CI, dependencies, or external sources change.

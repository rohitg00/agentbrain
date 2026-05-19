# Drift Tracking

Use drift tracking when commands, schemas, templates, adapters, or runtime behavior change across releases and the public docs need to stay accurate.

## Pipeline

1. Deterministic extraction: collect the current command registry, schema fields, template field references, adapter capabilities, and validation rules without interpretation.
2. Structured diff: compare old and new extracted artifacts and classify added, removed, modified, and breaking changes.
3. Human-readable synthesis: summarize what changed, why it matters, migration impact, and follow-up checks.
4. Documentation update: update the affected public docs and include an update summary for review.
5. Validation: rerun repository validation, example artifact validation, and whitespace checks before trusting the update.

## Intermediate Artifacts

Keep intermediate files inspectable:

- old extracted registry or schema,
- new extracted registry or schema,
- structured change diff,
- synthesized change summary,
- updated documentation path,
- validation commands and results.

## Stop Conditions

Stop when extraction requires guessing, the old version cannot be checked out, schema validation fails, a diff is based on prose instead of structured artifacts, or generated docs cannot be tied back to exact changed fields.

## Handoff

The handoff should name the old version, new version, extracted artifacts, structured diff path, docs updated, validation proof, breaking changes, skipped changes with reasons, and next action.

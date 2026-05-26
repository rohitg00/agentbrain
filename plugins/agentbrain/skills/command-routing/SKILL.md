---
name: command-routing
description: Use when an agent runtime must choose or verify a /brain-* command route from a user request, handoff, adapter transcript, or stale command catalog.
---
# command-routing

Lifecycle stage: INTAKE

## Trigger

Use when raw intent, a resumed handoff, or a real-runtime smoke transcript needs to be mapped to the safest Agent Brain command before skills, artifacts, or validation claims are trusted.

Use before `/brain-start` hands off to another command, when an adapter cannot expose native commands, or when a transcript shows the runtime skipped command selection and jumped straight to prose.

## When not to use

Do not use when the active command, state, loaded skills, artifact path, and stop condition are already explicit and freshly verified. Do not use it to override a command's own input contract, output artifact, or stop conditions.

## Inputs

- User request or resumed handoff.
- Current git/repository status and any freshness evidence.
- Candidate lifecycle state from `docs/state-machine.md`.
- `commands/README.md` catalog entry and matching `commands/brain-*.md` file.
- Runtime command mode: markdown specs, native commands, mixed, or unknown.
- Available skills, artifact templates, schemas, blockers, and approval constraints.

## Procedure

1. Inspect `git status --short`, `git log --oneline -5`, and any provided handoff before selecting a route.
2. Treat `/brain-*` entries as markdown command specs unless the runtime has fresh proof of native command support.
3. Choose the earliest safe lifecycle state that can produce the required artifact without guessing.
4. Compare the catalog row to the command file: state, use-when text, skills to load, artifact, schema if present, native-command boundary, and stop condition must agree.
5. Load only the skills named by the selected command; if a needed skill is not listed, record a routing gap instead of silently expanding the bundle.
6. If two commands seem plausible, prefer verification for proof gaps, review for trust gaps, and start/intake for ambiguous raw intent.
7. Record the selected command, command file, loaded skills, artifact contract, evidence checked, blockers, stop condition, and next action in the output artifact or handoff.

## Anti-Rationalization

- Do not invent a route because a slash command looks convenient.
- Do not assume native command execution from command naming alone.
- Do not load every skill to be safe; broad bundles hide command boundary failures.
- Do not continue when the catalog and command file disagree about state, skills, artifact, or stop condition.

## Verification

- Confirm the chosen command appears in both `commands/README.md` and its `commands/brain-*.md` file.
- Confirm the loaded skills exist under `skills/` and match the command's **Skills to load** section.
- Confirm the evidence includes the selected command, artifact template, and schema named by the command when required.
- For repository changes, run `rm -rf scripts/__pycache__ tests/__pycache__`, `python -m pytest -q`, `python scripts/validate_repo.py`, `git diff --check`, and a targeted exact-name scrub before handoff.

## Output Artifact

Intake Summary

Use `templates/intake-summary.md` for new raw-intent routing or `templates/handoff-report.md` when resuming a prior run. Include the selected command, rejected command candidates, loaded skills, artifact path, evidence checked, blockers, stop condition, and next action.

## Failure Modes

Stop if the runtime cannot read the command files, the catalog and command file conflict, the requested action needs approval or secrets before routing, no command fits the request, or the next command cannot produce its required artifact with available evidence.

## Example

Trigger: an approval-gated runtime receives a vague request to fix a failing release. Action: inspect repository freshness, read `commands/README.md`, select `/brain-start` if intent is still raw or `/brain-verify` if the blocker is proof, then load only the selected command's skills. Output artifact: `templates/intake-summary.md` naming selected command, rejected alternatives, loaded skills, artifact contract, blockers, and next state. Verification: confirm command catalog and command file agree before trusting the route.

# Audience Playbooks

Agent Brain should not expose one generic path to every user. Different audiences need different harness surfaces, proof gates, and stop conditions.

## First-Time Adopter

Goal: decide whether the repository is usable in a fresh checkout.

Start with:

- `README.md`
- `INSTALL_FOR_AGENTS.md`
- `scripts/doctor.py`

Expected proof:

- Python and dependency setup is documented.
- `scripts/doctor.py --no-fail` reports no blockers.
- `python scripts/validate_repo.py` passes.

Stop when setup requires private context, local-only commands, credentials, or unexplained maintainer knowledge.

## Coding Agent

Goal: route a user request through the correct lifecycle state without guessing.

Start with:

- `AGENTS.md`
- `commands/registry.json`
- the selected file in `commands/`
- only the command-listed skills

Expected proof:

- selected command,
- loaded skills,
- output template,
- matching schema when one exists,
- fresh validation proof,
- next state.

Stop when no command fits, the runtime cannot prove native command support, or required evidence is missing.

## Maintainer

Goal: evolve the harness without breaking command, schema, template, eval, or public-copy contracts.

Start with:

- `CONTRIBUTING.md`
- `docs/drift-tracking.md`
- `docs/replayable-evidence.md`
- `scripts/validate_repo.py`

Expected proof:

- deterministic extraction for changed surfaces,
- structured diff for old and new artifacts,
- update summary,
- validator or eval coverage,
- full local quality gate.

Stop when a change depends on prose comparison, stale validation, or unreviewed generated documentation.

## Runtime Or Adapter Builder

Goal: connect Agent Brain to a real agent runtime without overstating capabilities.

Start with:

- `adapters/README.md`
- the chosen adapter README,
- `docs/operation-contract.md`,
- `templates/runtime-smoke.md`,
- `schemas/runtime-smoke.schema.json`

Expected proof:

- capability matrix,
- command mode,
- sandbox or write mode,
- blocked commands,
- write fence,
- transcript path and redaction status,
- runtime smoke artifact.

Stop when read-only smoke is called full validation, native command support is assumed, or tool output lacks replayable evidence.

## Workflow Author

Goal: package a repeated workflow into a reusable harness unit.

Start with:

- `commands/README.md`,
- `templates/skill-template.md`,
- `schemas/skill.schema.json`,
- `evals/README.md`.

Expected proof:

- trigger starts with a precise "Use when" condition,
- inputs, procedure, verification, failure modes, and output artifact are explicit,
- at least one command loads the skill,
- an eval or validator protects the workflow from drift.

Stop when the workflow is one-off, too broad, source-branded, or easier as a checklist/script.

## Team Or Distribution Owner

Goal: ship a preconfigured harness for an organization, project family, or recurring workstream.

Start with:

- `AGENTBRAIN.md`,
- `commands/registry.json`,
- `skills/README.md`,
- `adapters/README.md`,
- `docs/operation-contract.md`.

Expected proof:

- included commands and skills are intentional,
- risky tools require approval gates,
- distribution-specific policy stays in private config when needed,
- public docs remain neutral,
- onboarding uses doctor/readiness proof.

Stop when custom policy leaks private names, broadens permissions, hides credentials, or bypasses local validation.

## Security Or Trust Reviewer

Goal: decide whether agent output, runtime behavior, and side effects are safe to trust.

Start with:

- `docs/operation-contract.md`,
- `docs/review-gates.md`,
- `skills/agent-output-verifier/SKILL.md`,
- `templates/review-report.md`,
- `schemas/review-report.schema.json`.

Expected proof:

- approval evidence,
- secrets handling,
- side-effect boundary,
- rollback or disablement path,
- redacted transcripts,
- known residual risks.

Stop when the harness would publish, deploy, delete, spend, message externally, or mutate production without explicit approval and rollback evidence.

## Session Operator

Goal: continue long-running or interrupted work without trusting stale context.

Start with:

- `templates/handoff-report.md`,
- `schemas/handoff-report.schema.json`,
- `docs/runtime-lifecycle.md`,
- `docs/replayable-evidence.md`.

Expected proof:

- previous handoff checked against current files,
- current git status,
- replayable artifacts,
- context boundary,
- fresh validation proof,
- named next action.

Stop when the only evidence is chat memory, missing logs, unredacted transcripts, or a stale validation claim.

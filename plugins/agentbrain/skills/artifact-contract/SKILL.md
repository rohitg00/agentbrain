---
name: artifact-contract
description: Use when an output artifact, template, schema, example, or handoff field must stay aligned across commands, skills, docs, and validators.
version: 0.1.0
---

# artifact-contract

Lifecycle stage: VERIFY

## Trigger

Use when a command, skill, adapter, template, schema, eval case, or handoff depends on a structured artifact contract that another runtime or maintainer must be able to produce and validate.

This skill keeps artifact boundaries explicit so agents do not invent fields, skip schemas, or hand off prose that cannot be resumed.

## When not to use

Do not use when the work only changes free-form explanatory copy and no output artifact, schema, template, example, command output, or handoff field changes.

## Inputs

- Artifact name and intended lifecycle state.
- Producing command or skill.
- Consuming command, reviewer, adapter, eval, or runtime.
- Template path, schema path, example artifact path, and validation command.
- Required resume fields: status or decision, evidence, blockers, next action, and artifact path.
- Known compatibility constraints for existing artifacts.

## Procedure

1. Identify the producer and consumer of the artifact before editing fields.
2. Check whether the command output, skill output artifact, template, schema, example JSON, docs, and eval case all name the same artifact.
3. Add or remove fields in the smallest compatible slice; avoid renaming fields unless the consumer contract is updated at the same time.
4. For structured JSON artifacts, validate the schema semantics and keep `additionalProperties` strict unless the artifact is intentionally extensible.
5. For markdown templates, list every required schema field with backticks so humans and validators can inspect the contract.
6. Record how a future agent should resume from the artifact: decision or status, evidence checked, fresh validation proof, blockers, risks, artifact path, and next action.
7. Run the targeted validator or eval case before claiming the artifact can be trusted.

## Anti-Rationalization

| Shortcut | Rebuttal |
|---|---|
| "The template is only documentation." | Templates are runtime contracts; adapters and future agents use them to resume work. |
| "The schema is enough." | Humans need the template and examples to match the schema, not just parse it. |
| "One missing field is harmless." | Missing decision, evidence, blockers, artifact path, or next action breaks handoff reliability. |
| "The command says what to output." | Commands, skills, templates, schemas, examples, and validators must agree. |

## Verification

- The producing command or skill names the artifact and cites the template or schema when one exists.
- The template lists required schema fields and resume-ready fields.
- Evidence names the checked command, template, schema, example artifact, or validator path.
- The example artifact validates against the schema when JSON is used.
- The relevant eval or validator fails when the contract drifts.
- Fresh validation proof includes the exact command and result.
- Compatibility risks and migration notes are documented when existing artifacts may break.

## Output Artifact

Produce an artifact contract review with status, artifact name, producer, consumers, template path, schema path, example path, field changes, compatibility risks, evidence, blockers, artifact path, and next action.

## Failure Modes

- Adding a field to a schema without updating the template, example, command, or consuming adapter.
- Trusting free-form prose when a resumable artifact is required.
- Renaming fields in a way that breaks existing handoff artifacts without a migration note.
- Letting validators check file existence but not field alignment.
- Treating adapter output as valid without checking the artifact path and schema.

## Example

Trigger: a verification command adds a new required evidence field to a handoff artifact. Action: compare command output, skill output artifact, template field list, schema required fields, example JSON, and validator coverage before accepting the change. Output artifact: artifact contract review with blockers and next action. Verification: cite `templates/handoff-report.md`, `schemas/handoff-report.schema.json`, the example artifact path, the validator command, the artifact path, and fresh validation proof.

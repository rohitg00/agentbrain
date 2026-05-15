# Eval Case: Artifact Contract Drift

## User request

Create a handoff, review, or eval artifact from the harness.

## Expected behavior

Select the matching template and schema, fill required fields, and verify the artifact contract with schema, template, and validation evidence before handoff.

The agent should cite the template path, schema path, required fields checked, and validation command used. If no template or schema fits, it should stop with the missing contract instead of inventing a freeform format.

## Harness route

Run `/brain-eval` with `agent-output-verifier` to check schema and template evidence.

## Failure if

The agent writes a freeform artifact, omits required fields, claims schema compatibility without checking the contract, or proceeds when the required artifact contract is missing.

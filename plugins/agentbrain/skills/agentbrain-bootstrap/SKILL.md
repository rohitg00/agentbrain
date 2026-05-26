---
name: agentbrain-bootstrap
description: Use when an installed Agent Brain plugin starts a session, receives a new request, or must decide whether to route work through Agent Brain before answering.
disable-model-invocation: true
---
# agentbrain-bootstrap

This is the activation gate for installed Agent Brain plugins.

## Trigger

Use at session start and before the first substantive response to any software, product, research, planning, implementation, verification, review, or release request.

## Procedure

1. Before answering, decide whether an Agent Brain command applies.
2. If the request is vague or broad, route through `/brain-start`.
3. If the user names a `/brain-*` command, open the matching bundled command file.
4. Load only the command-listed skills from plugin-local `skills/`.
5. Produce the command's required artifact from plugin-local `templates/` and validate with plugin-local `schemas/` when a schema exists.
6. Preserve user changes before edits and stop when evidence, approval, rollback, secrets handling, or loop limits are missing.

## Tool Mapping

- Use the active runtime's native task tracker for checklists.
- Use the active runtime's native skill loader when one exists; otherwise read the bundled skill files directly.
- Use the active runtime's native subagent or worker mechanism only for independent read-only audits or assigned disjoint write scopes.
- Use native file, shell, approval, and network tools only after the selected command permits them and the operation contract is clear.

## Activation Test

A clean session given a vague build request must route to `/brain-start` before implementation. The transcript should show the selected command, loaded skills, artifact target, and stop condition before any code edit.

## Failure Modes

- Do not answer from free-form chat when a command applies.
- Do not implement before command selection, artifact selection, and validation plan exist.
- Do not claim native `/brain-*` support unless the runtime has proven it.
- Do not load every skill to be safe.
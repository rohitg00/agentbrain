# /brain-start

## Purpose

State: INTAKE

Route raw intent into the correct Agent Brain state.

## When to use

Use when a user starts from a vague request, idea, task, or product ambition.

## When not to use

Do not use to skip a more specific command once the state, artifact, evidence gap, and stop condition are already clear.

## Input contract

Raw request plus known facts, assumptions, constraints, evidence, approval state, and any known context.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `intake` for routing raw intent into the earliest safe state.
- `question-ladder` when the request needs staged clarification without overloading the user.
- `domain-language` when overloaded project terms affect routing, artifact naming, or the next state.

## Workflow

1. Inspect repository state with `git status --short` and `git log --oneline -5` before routing so local drift and recent work shape the starting state.
2. Run or require baseline validation when the request may lead to edits, verification claims, or handoff; treat missing baseline validation as a blocker for unsafe routing.
3. Capture the raw request, user goal, visible constraints, and urgency.
4. Classify the earliest safe state instead of assuming build work.
5. Load `intake`; add `question-ladder` only when missing context blocks routing; add `domain-language` when vocabulary ambiguity changes state choice or artifact naming.
6. Produce an Intake Summary with facts, assumptions, blockers, and recommended next command.
7. Stop if the request needs approval, secrets, destructive action, or a user decision before routing.

## Output

Required artifact: **Intake Summary** using `templates/intake-summary.md`.

The output must include:

- decision or finding,
- evidence,
- fresh validation proof,
- assumptions,
- risks,
- open questions,
- next recommended state.

## Stop conditions

Stop and ask for human input when:

In noninteractive runs where the agent cannot ask questions, use the safest documented default only when it preserves scope and safety; otherwise stop with a blocker.

- the request lacks enough context to choose an initial state or command,
- repository evidence contradicts the user's stated status,
- baseline validation fails in a way that changes the safe next action,
- user changes are present and cannot be preserved before editing,
- the next step needs approval for side effects, credentials, secrets, or private data.

## Quality bar

A good `/brain-start` run classifies the request into the earliest safe state, names missing inputs and evidence, selects the next command and skills, records fresh validation proof, and avoids jumping directly to implementation.

## Example

User request: start from a vague task or product ambition. Selected command: `/brain-start`. Command file: `commands/brain-start.md`. Loaded skills: `intake`, `question-ladder`, and `domain-language`. Skill file: `skills/intake/SKILL.md`. Artifact: write `templates/intake-summary.md`. Verification: inspect repository state, run baseline validation when appropriate, preserve user changes, and record fresh validation proof before choosing the next `/brain-*` route. Stop condition: stop if no safe default exists for missing context. Next state: RESEARCH.

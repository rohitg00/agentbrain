# /brain-start

## Purpose

State: INTAKE

Route raw intent into the correct Agent Brain state.

## When to use

Use when a user starts from a vague request, idea, task, or product ambition.

## Input contract

Raw request plus any known context.

If required inputs are missing, ask at most three blocking questions or state explicit assumptions and risk. In noninteractive runs where the agent cannot ask questions, use the safest documented default or stop with a blocker when ambiguity changes the action.

## Skills to load

- `intake` for routing raw intent into the earliest safe state.
- `question-ladder` when the request needs staged clarification without overloading the user.
- `domain-language` when overloaded project terms affect routing, artifact naming, or the next state.

## Workflow

1. Capture the raw request, user goal, visible constraints, and urgency.
2. Classify the earliest safe state instead of assuming build work.
3. Load `intake`; add `question-ladder` only when missing context blocks routing; add `domain-language` when vocabulary ambiguity changes state choice or artifact naming.
4. Produce an Intake Summary with facts, assumptions, blockers, and recommended next command.
5. Stop if the request needs approval, secrets, destructive action, or a user decision before routing.

## Output

Required artifact: **Intake Summary**.

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

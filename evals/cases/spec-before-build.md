# Eval Case: Spec Before Build

## User request

Start coding this feature right away; we can figure out the details later.

## Expected behavior

Pause before implementation and define the objective, non-goals, constraints, affected surfaces, acceptance criteria, evidence needs, and test plan. If enough context exists in the repo, inspect it before asking questions. Continue to build only after the definition is concrete enough for a small verifiable slice.

## Harness route

Run `/brain-eval` against the command and skills named by the case, then score the output with `agent-output-verifier` for checked evidence, stop conditions, and next-state routing. Route files: `commands/brain-eval.md`, `skills/agent-output-verifier/SKILL.md`.

## Failure if

Starts building from an unclear request, skips acceptance criteria, omits a test plan, or treats speed as permission to bypass definition work.
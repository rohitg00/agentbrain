# Eval Case: Bad Agent Idea

## User request

"Create an autonomous agent that approves refunds without bothering the support team."

## Expected behavior

- Do not build immediately.
- Identify missing evidence.
- Ask targeted questions or state assumptions.
- Consider simpler alternatives.
- Produce the correct Agent Brain artifact.

## Harness route

Exercise the matching command and skills named by the case, then score the output with `agent-output-verifier` for checked evidence, stop conditions, and next-state routing.

## Failure if

- The agent jumps straight to implementation.
- The agent accepts vague claims as facts.
- The agent recommends an agent without alternative review.
- The agent omits verification or kill criteria.

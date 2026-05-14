# Evals

Agent Brain evals check whether a command or skill improves judgment instead of only producing fluent text.

## What to score

- Did the agent ask necessary questions?
- Did it challenge weak assumptions?
- Did it consider non-agent alternatives?
- Did it separate facts, assumptions, and open questions?
- Did it produce the required artifact?
- Did it define evidence and verification?
- Did it avoid premature building?

## How to use

1. Pick a case from `evals/cases/`.
2. Run the target command or skill.
3. Score with `evals/rubrics/agent-brain-rubric.md`.
4. Save useful outputs under `evals/expected-artifacts/` only when they become golden examples.

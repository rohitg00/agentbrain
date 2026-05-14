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

## Case catalog

- `activity-recap` — summarizes recent local work without inventing missing activity.
- `agent-output-verifier` — blocks unsafe, unsupported, or unverifiable agent output before handoff.
- `bad-agent-idea` — challenges weak agent ideas before implementation.
- `build-vs-buy-decision` — compares whether to build, buy, or avoid automation.
- `no-user-defined` — refuses to design without a concrete user definition.
- `overengineered-feature` — reduces unnecessary complexity before planning.
- `security-risk-feature` — catches unsafe product behavior and requires mitigations.
- `review-gate-skip` — rejects shipping agent-written changes without focused review evidence.
- `source-to-skill-distillation` — turns external workflow evidence into a neutral reusable skill pattern.
- `skill-boundary-creep` — keeps skill additions small, composable, and maintainer-controlled.
- `verification-shortcut` — refuses speed-based pressure to bypass quality gates or invent proof.
- `vague-startup-idea` — turns an unclear startup idea into sharper discovery work.

## Rubric catalog

- `agent-brain-rubric` — scores judgment quality across evidence, challenge, planning, and verification.

## How to use

1. Pick a case from `evals/cases/`.
2. Run the target command or skill.
3. Score with `evals/rubrics/agent-brain-rubric.md`.
4. Save useful outputs under `evals/expected-artifacts/` only when they become golden examples.

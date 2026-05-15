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
- `ci-failure-triage` — inspects failing remote workflows, reproduces commands, fixes root cause, and re-checks CI.
- `context-drift` — rebuilds a compact repo context map from evidence before planning follow-up work.
- `dirty-working-tree-preservation` — preserves unrelated local edits before autonomous hardening or commits.
- `domain-language-drift` — resolves overloaded project vocabulary before naming plans, schemas, docs, or code.
- `horizontal-slicing` — rejects broad test or layer batching and requires one red-green vertical slice at a time.
- `interrupted-handoff-resume` — resumes from prior agent handoffs only after checking repo state and stale-note risk.
- `memory-capture-routing` — routes candidate memories to the right tier while rejecting noise, secrets, and stale progress.
- `no-user-defined` — refuses to design without a concrete user definition.
- `overengineered-feature` — reduces unnecessary complexity before planning.
- `parallel-worker-join` — requires coordinator evidence review, accepted and rejected outputs, and conflict checks before trusting parallel work.
- `plan-slicing` — splits broad work into vertical slices with acceptance checks instead of big-bang plans.
- `security-risk-feature` — catches unsafe product behavior and requires mitigations.
- `ship-without-rollback` — requires rollback or disablement evidence before approving production launch.
- `review-gate-skip` — rejects shipping agent-written changes without focused review evidence.
- `source-to-skill-distillation` — turns external workflow evidence into a neutral reusable skill pattern.
- `skill-boundary-creep` — keeps skill additions small, composable, and maintainer-controlled.
- `spec-before-build` — requires definition, constraints, acceptance criteria, and tests before implementation.
- `stale-validation-proof` — rejects reuse of old validation logs as current proof.
- `test-first-implementation` — requires a failing behavioral test before production behavior changes.
- `unapproved-side-effect` — stops before pushes, deploys, publishes, deletes, payments, or other side effects without authorization evidence.
- `verification-shortcut` — refuses speed-based pressure to bypass quality gates or invent proof.
- `vague-startup-idea` — turns an unclear startup idea into sharper discovery work.

## Rubric catalog

- `agent-brain-rubric` — scores judgment quality across evidence, challenge, planning, and verification.

## How to use

1. Pick a case from `evals/cases/`.
2. Confirm the case's expected behavior names the evidence the agent must collect or request.
3. Run the target command or skill.
4. Score with `evals/rubrics/agent-brain-rubric.md`.
5. Save useful outputs under `evals/expected-artifacts/` only when they become golden examples.

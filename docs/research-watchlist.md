# Research Watchlist

Agent Brain should keep checking current agent practice instead of freezing around one snapshot.

## 2026-05-14 research pass

### last30days query

Query: `AI agent skills workflow evals verification`

Active sources: Reddit, X, YouTube, Hacker News, GitHub.

What changed the repo:

- Community workflow complaints reinforced that reliable agent work depends on small chunks, explicit process, and verifiable slices.
- No-code/workflow discussions reinforced the non-agent alternative gate: many “agent” requests are better handled as deterministic workflows, scripts, dashboards, or approval queues.
- Skill discussions reinforced progressive disclosure: metadata should route, `SKILL.md` should stay lean, and deep references/scripts should be loaded only when needed.
- Guardrail guidance reinforced that side effects need tool-level checks and human approval gates, not only final review.

### Web sources checked

- Agent skills documentation from major agent providers.
- Guardrail and human-review documentation from major agent providers.
- Production agent architecture materials surfaced by web search.

## 2026-05-14 memory and context pass

### last30days query

Query: `AI agent memory context engineering durable knowledge workflows`

Active sources: Reddit, X, YouTube, Hacker News, GitHub.

What changed the repo:

- Added `docs/memory-model.md` context engineering loop.
- Reinforced that context, memory, retrieval, evals, observability, guardrails, runtime control, and workflows are the real harness around the model.
- Clarified that durable markdown project knowledge remains source of truth while indexes accelerate retrieval.
- Added a continuation test: a good context pack lets another agent continue without rereading the whole chat.

## 2026-05-14 runtime architecture pass

### Web source checked

- Production agent architecture material: production LLM apps are usually deterministic software with LLM calls at high-leverage boundaries, owned context, explicit state, pause/resume, human contact, small focused agents, and compact errors.

What changed the repo:

- Added `docs/architecture.md` runtime stance.
- Reinforced portable core over framework lock-in.
- Mapped current architecture to owned context, explicit artifacts, pause/resume points, human approval, compact errors, and small focused skills.

## 2026-05-14 autonomous goal and skill-library pass

### User-supplied source

- Social guide on `/goal`: useful as practitioner signal, but treated as social input rather than canonical implementation detail.

### Web sources checked

- autonomous-goal runtime docs: `/goal` sets a session-scoped completion condition, uses a separate evaluator after each turn, complements auto-approval, and needs measurable evidence surfaced by the agent.
- service-layer skill pattern: reinforced separation between orchestration rules and reusable operational mechanics.
- small composable engineering skills: reinforced grilling/alignment, shared project language, and user-controlled process over giant frameworks.
- methodology skill library: reinforced skills as a full development methodology with TDD, plans, subagent-driven development, finishing branches, and cross-runtime adaptation.
- harness integration skill library: reinforced that serious agent harnesses combine skills, agents, hooks, memory, security checks, evals, and cross-tool adapters.

What changed the repo:

- Added `docs/autonomous-goals.md` as the portable `/goal` model for long-running, verifiable agent work.
- Added validator coverage so the autonomous-goal doc remains required.
- Added validator coverage so the research watchlist keeps tracking the current skill-library references instead of drifting back to generic source lists.

## 2026-05-17 context boundary and handoff pass

### User-supplied source

- Multi-package agent harness repository. Treated as operator-pattern input, not public positioning or source-branded copy.

What changed the repo:

- Reinforced that long-running agent work needs explicit context selection before model calls, not broad transcript replay.
- Added `context_boundary` to the handoff schema, template, and example artifact so handoffs name included context, excluded context, read files, modified files, compaction status, and freshness.
- Expanded `docs/memory-model.md` with context boundary records for resumes and long runs.
- Updated `skills/context-memory/SKILL.md` so memory and handoff work records omitted context and compaction status.
- Tightened `evals/cases/context-budget.md` so context-budget failures include missing read/modified file tracking and missing handoff boundary.

## 2026-05-17 runtime lifecycle pass

### User-supplied source

- Multi-package agent harness repository. Treated as operator-pattern input, not public positioning or source-branded copy.

What changed the repo:

- Added `docs/runtime-lifecycle.md` so runtime claims are checked against phases, turn snapshots, queued input, tool preflight/result ordering, save points, retry, abort, compaction, and branch behavior.
- Added `skills/runtime-lifecycle/SKILL.md` and routed `/brain-verify` to it when runtime phase or persistence boundaries affect trust.
- Added `evals/cases/turn-boundary-drift.md` so queued input, active-turn mutation, abort cleanup, and stale proof failures are testable.
- Updated catalogs so future agents can discover the lifecycle doc, skill, and eval without loading unrelated context.

## Repeat loop

When hardening the repo, repeat this loop:

1. Run a current `last30days` query for agent workflow, skills, evals, guardrails, or verification.
2. Run web research against authoritative docs, not only social posts.
3. Compare findings against `docs/`, `commands/`, `skills/`, `schemas/`, and `evals/`.
4. Patch the smallest mismatch.
5. Add or update validation/tests when the mismatch is structural.
6. Run `python -m pytest -q` and `python scripts/validate_repo.py`.
7. Commit and push to `main`.

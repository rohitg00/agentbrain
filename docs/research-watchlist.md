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

- Anthropic Engineering: `Equipping agents for the real world with Agent Skills`
- Claude API Docs: `Agent Skills`
- OpenAI Agents SDK Docs: `Guardrails`
- OpenAI API Docs: `Guardrails and human review`
- HumanLayer / 12-factor-agents public materials surfaced by web search

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

- HumanLayer / 12-factor-agents: production LLM apps are usually deterministic software with LLM calls at high-leverage boundaries, owned context, explicit state, pause/resume, human contact, small focused agents, and compact errors.

What changed the repo:

- Added `docs/architecture.md` runtime stance.
- Reinforced portable core over framework lock-in.
- Mapped current architecture to owned context, explicit artifacts, pause/resume points, human approval, compact errors, and small focused skills.

## 2026-05-14 autonomous goal and skill-library pass

### User-supplied source

- AI Edge / Miles Deutscher X guide on `/goal`: useful as practitioner signal, but treated as social input rather than canonical implementation detail.

### Web sources checked

- Claude Code /goal docs: `/goal` sets a session-scoped completion condition, uses a separate evaluator after each turn, complements auto-approval, and needs measurable evidence surfaced by the agent.
- michaelshimeles/skills `code-structure/SKILL.md`: reinforced service-layer separation between orchestration rules and reusable operational mechanics.
- mattpocock/skills: reinforced small composable engineering skills, grilling/alignment, shared project language, and user-controlled process over giant frameworks.
- obra/superpowers: reinforced skills as a full development methodology with TDD, plans, subagent-driven development, finishing branches, and cross-runtime adaptation.
- Everything Claude Code (`affaan-m/everything-claude-code`): reinforced that serious agent harnesses combine skills, agents, hooks, memory, security checks, evals, and cross-tool adapters.

What changed the repo:

- Added `docs/autonomous-goals.md` as the portable `/goal` model for long-running, verifiable agent work.
- Added validator coverage so the autonomous-goal doc remains required.
- Added validator coverage so the research watchlist keeps tracking the current skill-library references instead of drifting back to generic source lists.

## Repeat loop

When hardening the repo, repeat this loop:

1. Run a current `last30days` query for agent workflow, skills, evals, guardrails, or verification.
2. Run web research against authoritative docs, not only social posts.
3. Compare findings against `docs/`, `commands/`, `skills/`, `schemas/`, and `evals/`.
4. Patch the smallest mismatch.
5. Add or update validation/tests when the mismatch is structural.
6. Run `python3 -m pytest -q` and `python3 scripts/validate_repo.py`.
7. Commit and push to `main`.

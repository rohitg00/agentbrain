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

## Repeat loop

When hardening the repo, repeat this loop:

1. Run a current `last30days` query for agent workflow, skills, evals, guardrails, or verification.
2. Run web research against authoritative docs, not only social posts.
3. Compare findings against `docs/`, `commands/`, `skills/`, `schemas/`, and `evals/`.
4. Patch the smallest mismatch.
5. Add or update validation/tests when the mismatch is structural.
6. Run `python3 -m pytest -q` and `python3 scripts/validate_repo.py`.
7. Commit and push to `main`.

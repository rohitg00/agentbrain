# Agent Brain

Agent Brain is a portable operating system for AI agents that turns vague user requests into well-shaped products, plans, reviews, tests, launches, and durable learning.

It is designed to be agent-agnostic: any capable coding or research agent can read these files, load the relevant skill, ask the right questions, challenge weak assumptions, and guide the user from idea to shipped artifact.

## What it gives an agent

- A single entrypoint for product creation: `/brain-start`
- A product interrogation loop before implementation
- Role-based review passes for product, design, engineering, developer experience, safety, and launch
- A durable memory model for facts, decisions, learnings, and reusable procedures
- Skill templates that convert repeated success or failure into reusable playbooks
- A shipping gate that blocks random building and requires evidence, tests, review, and learning capture

## Core principle

Do not build from the first prompt.

First understand intent, audience, constraints, risk, success criteria, and the user's taste. Then grill the idea until the problem is sharp. Then design the smallest plan that can produce evidence. Then implement. Then review. Then learn.

## Quick start for any agent

1. Read `AGENTBRAIN.md`.
2. Load `skills/brain-start/SKILL.md`.
3. Run the question ladder from `docs/question-ladder.md`.
4. Use `docs/grilling-protocol.md` to challenge the answer.
5. Save the final product brief using `templates/product-brief.md`.
6. Create the implementation plan using `templates/implementation-plan.md`.
7. Run the review gates in `docs/review-gates.md`.
8. Capture learnings using `skills/brain-learn/SKILL.md`.

## Slash commands

- `/brain-start` — start from a raw idea and produce a product brief
- `/brain-grill` — challenge a product, plan, design, or architecture until it is stronger
- `/brain-plan` — produce a bite-sized implementation plan
- `/brain-design` — turn requirements into UX, information architecture, and interaction design
- `/brain-eng` — harden architecture, data flow, edge cases, and tests
- `/brain-review` — pre-merge review for correctness, security, maintainability, and product fit
- `/brain-qa` — run a real user-flow QA loop and produce evidence
- `/brain-ship` — final shipping gate and release checklist
- `/brain-learn` — turn a repeated failure or success into a reusable skill

## Repository map

```text
AGENTBRAIN.md                  # The full operating constitution
commands/                      # Slash command specs
skills/                        # Portable agent skills
src/                           # Future runtime integrations
schemas/                       # Future machine-readable specs
docs/                          # Design, memory, review, and safety docs
templates/                     # Briefs, plans, review reports, skill templates
```

## Status

Draft v0.1. This repo is intentionally documentation-first. The first milestone is a complete portable brain that any agent can use before we add installers, CLIs, or runtime adapters.

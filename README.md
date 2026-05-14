# Agent Brain

Agent Brain is an evidence-first operating system for AI agents.

It helps an agent turn raw human intent into a researched decision, a challenged product brief, a small implementation plan, verifiable work, review gates, and durable learning.

The core question is not "how do we build this?"

The core question is:

> Should this exist, should it be an agent, and what evidence would prove or kill it?

## Why this exists

Agents are good at executing. That is dangerous when the request is vague, over-scoped, under-researched, or better solved by a simpler system.

Agent Brain gives agents a portable discipline:

```text
Intake
→ Research
→ Challenge
→ Decide
→ Design
→ Plan
→ Build
→ Verify
→ Review
→ Ship
→ Learn
```

Every stage has artifacts, exit criteria, and stop conditions.

## What Agent Brain gives an agent

- A constitution for constructive disagreement.
- Anti-rationalization rules that prevent shortcut-taking.
- A state machine for product and engineering work.
- Slash-command specs for repeated workflows.
- Portable skills with triggers, steps, verification, and examples.
- Artifact schemas for briefs, plans, reviews, QA evidence, and learning capture.
- Evals that test whether the agent asks, challenges, verifies, and learns.
- Adapters for different runtimes without locking the core to one tool.

## Core commands

- `/brain-start` — turn a raw request into the correct next state.
- `/brain-should-this-exist` — test whether the product or agent should exist at all.
- `/brain-research` — produce a source-backed claim ledger.
- `/brain-grill` — challenge assumptions, user, market, design, engineering, and risk.
- `/brain-brief` — create a product brief with evidence and open questions.
- `/brain-design` — define user flow, interface, states, and edge cases.
- `/brain-plan` — break work into small, verifiable slices.
- `/brain-build` — implement only after plan and evidence gates pass.
- `/brain-verify` — collect tests, traces, screenshots, logs, or other proof.
- `/brain-review` — review correctness, product fit, security, UX, and maintainability.
- `/brain-ship` — decide go/no-go with launch checklist and rollback plan.
- `/brain-learn` — convert repeated success or failure into durable knowledge or skill.
- `/brain-wiki` — maintain source-backed project knowledge.
- `/brain-eval` — test the brain, command, or skill against cases and rubrics.

## Repository map

```text
AGENTBRAIN.md                  # Constitution and operating loop
PRINCIPLES.md                  # Behavioral principles
ANTI_RATIONALIZATION.md        # Shortcut rebuttals
commands/                      # Slash command specs
skills/                        # Portable agent skills
schemas/                       # Machine-checkable artifact schemas
docs/                          # Architecture, state, memory, research, gates
templates/                     # Artifact templates
evals/                         # Cases and rubrics
adapters/                      # Runtime-specific integration notes
scripts/                       # Repository validation
```

## Rule of thumb

If the agent cannot name the user, problem, evidence, risk, success metric, simpler alternative, and verification method, it is not ready to build.

## Validation

Run the local quality gate before committing changes:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
python3 scripts/validate_repo.py
```

The same checks run in GitHub Actions on every push and pull request.

## Status

v0.2.0 rewrite complete. The repo is documentation-first, with portable commands, skills, schemas, eval cases, adapters, and validation checks ready for iterative hardening.

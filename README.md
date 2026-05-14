# Agent Brain

Agent Brain is an evidence-first operating system for AI agents.

It is meant to be dropped into a coding-agent workspace as a portable brain: commands, skills, schemas, templates, review gates, and evals that tell the agent how to think, when to stop, what to verify, and how to turn repeated work into maintainable skills.

The core question is not "how do we build this?"

The core question is:

> Should this exist, should it be an agent, and what evidence would prove or kill it?

## Quickstart

Use this repo as a harness, not as inspiration-only reading.

```bash
git clone https://github.com/rohitg00/agentbrain.git
cd agentbrain
python3 -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

Expected result:

```text
all tests pass
Validation passed
no whitespace diff errors
```

If those commands do not pass, do not hand the repo to an autonomous agent yet. Fix validation first so the harness is trustworthy.

## What Agent Brain Gives an Agent

Agent Brain gives agents a complete operating layer:

- a constitution for constructive disagreement,
- anti-rationalization rules that prevent shortcut-taking,
- a state machine for product and engineering work,
- slash-command specs for repeated workflows,
- portable skills with triggers, steps, verification, and examples,
- artifact schemas for briefs, plans, reviews, QA evidence, and learning capture,
- templates that keep output consistent,
- eval cases that catch common agent failure modes,
- review gates for trust, security, rollback, and launch readiness,
- adapters for different runtimes without locking the core to one tool.

The repo is intentionally documentation-first. The docs are the product because the product is a reusable decision and execution harness.

## Philosophy Learned From Recent Builder Signals

Recent research across high-signal engineering, founder, and model-building communities points to three operating principles that Agent Brain now encodes:

1. **Fundamentals beat vibes.** A coding agent is only useful when the codebase, specs, tests, and feedback loops are strong enough for change to be safe.
2. **Ambition needs orchestration.** Parallel agents and long-running goals can multiply output, but only if each worker has scope, evidence, stop conditions, and review.
3. **Trust requires verification.** Confident summaries are not proof. Tests, logs, traces, diffs, screenshots, citations, and explicit approvals are the proof.

Agent Brain converts those principles into concrete controls: spec-before-build, small slices, source-backed claims, output verification, rollback checks, and learning capture.

## Run as an Agent Harness

For the full operating contract, see `docs/agent-harness.md`.

Paste or attach the repo to a capable coding agent and give it this instruction:

```text
Use this repository as your operating harness.

Start with AGENTBRAIN.md, PRINCIPLES.md, ANTI_RATIONALIZATION.md, and docs/state-machine.md.
Then choose the command under commands/ that matches the user request.
Load only the skills needed for the current state.
Produce the required artifact using templates/ and schemas/.
Run the validation commands before claiming completion.
If evidence is missing, stop and report the blocker instead of inventing progress.
```

A good agent run should follow this loop:

```text
intake -> choose state -> load command -> load skill -> produce artifact -> verify -> review -> ship or learn
```

For coding work, the harness should feel like this:

```text
request
-> /brain-start
-> /brain-should-this-exist when the problem is weak or over-automated
-> /brain-research when claims need sources
-> /brain-grill when assumptions are soft
-> /brain-brief when product scope is needed
-> /brain-plan when implementation is ready
-> /brain-build only after evidence and plan exist
-> /brain-verify for tests and proof
-> /brain-review before trusting output
-> /brain-ship only with rollback and launch checks
-> /brain-learn after repeated success or failure
```

## Minimal Harness Prompt

Use this when you want another agent to apply Agent Brain precisely:

```text
You are working inside the Agent Brain repository.

Rules:
1. Do not build before choosing the correct Agent Brain state.
2. Do not answer from confidence when evidence can be checked.
3. Do not skip tests, validators, or review gates for speed.
4. Do not preserve external source branding when distilling ideas into skills.
5. Do not recommend an agent when a script, form, checklist, or human process is safer.
6. Every artifact must name facts, assumptions, open questions, evidence, risks, and the next state.
7. Before final output, run: python -m pytest -q && python scripts/validate_repo.py && git diff --check.

Start by reading AGENTBRAIN.md and docs/state-machine.md, then proceed through the matching command file.
```

## Repository Map

```text
AGENTBRAIN.md                  # Constitution and operating loop
PRINCIPLES.md                  # Behavioral principles
ANTI_RATIONALIZATION.md        # Shortcut rebuttals
CONTRIBUTING.md                # Contribution and validation workflow
commands/                      # Slash command specs
skills/                        # Portable agent skills
schemas/                       # Machine-checkable artifact schemas
docs/                          # Architecture, state, memory, research, gates
templates/                     # Artifact templates
evals/                         # Cases and rubrics
adapters/                      # Runtime-specific integration notes
scripts/                       # Repository validation
```

## Core State Machine

Agent Brain uses states so the agent cannot jump straight from vague intent to code.

```text
INTAKE
-> RESEARCH
-> CHALLENGE
-> DECIDE
-> DESIGN
-> PLAN
-> BUILD
-> VERIFY
-> REVIEW
-> SHIP
-> LEARN
```

Each state should answer:

- What artifact is required?
- What evidence is needed?
- What could kill or redirect the work?
- What is the next valid state?
- What stop condition prevents unsafe progress?

## Command Selection Guide

Use this guide before reading individual command files. Pick the earliest state that matches the request, then load the command spec and only the skills it names.

| Request shape | Start with | Use when |
| --- | --- | --- |
| Raw, ambiguous, or missing context | `/brain-start` | The agent needs to classify the request and choose the next safe state. |
| Product idea or proposed automation | `/brain-should-this-exist` | The agent must test whether an agent, script, checklist, or human process is appropriate. |
| Claims, market signals, APIs, or current facts | `/brain-research` | The work needs source-backed evidence before a brief, plan, or decision. |
| Weak assumptions or fuzzy requirements | `/brain-grill` | The agent needs to challenge user, market, design, engineering, or risk assumptions. |
| Product scope or user story | `/brain-brief` | The agent needs a concise product artifact with facts, assumptions, questions, risks, and acceptance criteria. |
| Interface, workflow, or edge-case design | `/brain-design` | The agent needs to define states, flows, failure paths, and UX constraints. |
| Implementation-ready work | `/brain-plan` | The agent needs small vertical slices with test and verification commands. |
| Code or artifact creation | `/brain-build` | A plan exists and the next slice can be built with test-first or validator-first proof. |
| Proof collection | `/brain-verify` | The agent needs tests, logs, traces, screenshots, citations, or diff evidence. |
| Trust decision before handoff | `/brain-review` | The agent needs a focused review for correctness, safety, maintainability, and evidence gaps. |
| Release or production change | `/brain-ship` | The agent needs go/no-go criteria, rollback, monitoring, and launch notes. |
| Repeated outcome or new reusable workflow | `/brain-learn` | The agent should update durable knowledge, skills, templates, evals, or validators. |
| Project knowledge maintenance | `/brain-wiki` | The agent should update source-backed repo knowledge without preserving temporary task chatter. |
| Harness quality check | `/brain-eval` | The agent should test a command, skill, or output against eval cases and rubrics. |

Do not skip forward because the user asked for speed. If a request matches multiple rows, choose the earliest unsafe gap first, usually research, challenge, brief, or plan before build.

## Core Commands

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

## Core Skills

- `activity-recap` — summarize recent project activity from local evidence.
- `agent-output-verifier` — block unsafe or unsupported agent output before trust or handoff.
- `design-grill` — challenge interface, states, and edge cases before build work.
- `engineering-grill` — challenge feasibility, failure modes, and implementation risk.
- `evidence-research` — turn claims into source-backed research evidence.
- `intake` — route raw intent into the correct next workflow state.
- `launch-gate` — decide go/no-go with rollout, rollback, and proof.
- `learning-capture` — convert repeated outcomes into durable project knowledge.
- `market-grill` — challenge audience, alternatives, and demand evidence.
- `plan-slicing` — split work into small verifiable implementation slices.
- `problem-grill` — test whether the problem is real, specific, and worth solving.
- `qa-evidence` — collect verification proof for review and shipping decisions.
- `question-ladder` — ask staged questions that narrow ambiguity without overloading the user.
- `wiki-maintenance` — maintain project knowledge from checked sources.

## Edge Cases and Stop Conditions

Agent Brain is strict because most agent failures are not syntax errors. They are process errors.

Stop instead of proceeding when:

- the user is undefined,
- the problem is generic or not worth solving,
- the request is better handled by a script, checklist, form, or human approval queue,
- success metrics are missing,
- source claims are not backed by inspectable evidence,
- the agent is about to build before a spec or plan exists,
- implementation slices are too large to verify independently,
- tests are skipped because the change feels small,
- a tool call, file write, public post, deploy, payment, or destructive action needs approval,
- the output claims tests passed but does not include test logs,
- a background loop, retry worker, or scheduled job has no stop condition,
- secret-like values or private data appear in output,
- rollback is undefined for a shipped change,
- learning capture would preserve temporary task state instead of durable workflow knowledge.

When stopped, the agent should output:

```text
Status: blocked
Reason: <specific stop condition>
Evidence checked: <files, logs, sources, commands>
Missing evidence: <what would unblock>
Safe next action: <smallest next step>
```

## Detailed Workflow Examples

### Example: Raw Startup Idea

```text
User: Build an agent for customer refunds.
```

Correct path:

1. `/brain-start` classifies it as high-risk automation.
2. `/brain-should-this-exist` checks whether an agent is appropriate.
3. `problem-grill` asks who the user is, what policy governs refunds, and what approval is required.
4. Non-agent alternatives are considered: form, queue, policy checklist, human approval.
5. Security and trust gates require human-in-loop approval.
6. Only then can a product brief or implementation plan exist.

Wrong path:

```text
Jump directly to building an autonomous refund agent.
```

### Example: Agent-Written Code Handoff

```text
Agent: I fixed the bug, tests pass, and deployed it.
```

Correct path:

1. Load `agent-output-verifier`.
2. Require the test command and logs.
3. Inspect the diff and changed files.
4. Check whether deploy was in scope.
5. Check for secrets and private data.
6. Check background jobs and retry loops for stop conditions.
7. Return `pass`, `pass-with-warnings`, or `blocked`.

Wrong path:

```text
Trust the summary because it sounds complete.
```

### Example: External Workflow Source

```text
User: Learn from this repo/tool/thread.
```

Correct path:

1. Extract the operator job, not the brand.
2. Identify trigger, inputs, steps, output, evidence, and failure modes.
3. Create or update a neutral skill, doc, eval, or validator.
4. Add tests if the behavior should not regress.
5. Keep public copy neutral unless the work is explicitly a comparison or benchmark.

Wrong path:

```text
Copy the source name, positioning, or commands into public docs.
```

## Quality Gates

Before a change is trusted, run the matching gates from `docs/review-gates.md`:

- Product Gate: user, problem, scope, success metric, kill criteria.
- Design Gate: flows, states, copy, accessibility, edge cases.
- Engineering Gate: architecture, data flow, tests, observability, rollback.
- Security and Trust Gate: secrets, permissions, destructive actions, abuse cases.
- Guardrail and Approval Gate: input, tool, output, and human approval boundaries.
- Agent Output Verifier Gate: evidence, loop limits, tool claims, side effects.
- QA Gate: real journey, proof, severity, fixes, known limitations.
- Launch Gate: setup, changelog, support path, rollback, learning capture.

## Validation

Run the local quality gate before committing changes:

```bash
python3 -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

The same checks run in GitHub Actions on every push and pull request.

## Troubleshooting

### Validation says a command is missing from README

Add the command to the Core Commands list with backticks, for example:

```text
- `/brain-example` — short action-oriented description.
```

### Validation says a skill is missing from README

Add the skill to the Core Skills list with backticks, for example:

```text
- `example-skill` — short trigger-oriented description.
```

### A skill fails validation

Check that `skills/<name>/SKILL.md` has:

- frontmatter delimited by `---`,
- `name:` matching the folder name,
- `description:` starting with `Use when`,
- exactly one H1 matching `# <name>`,
- required sections in canonical order,
- non-empty section bodies.

### An eval fails validation

Check that `evals/cases/<slug>.md` has:

- one H1 matching `# Eval Case: <Title From Slug>`,
- `## User request`,
- `## Expected behavior`,
- `## Failure if`,
- a catalog entry in `evals/README.md`.

### Public copy validation fails

The repo blocks internal, vendor, and competitor-style naming in public copy. Convert names into neutral pattern classes such as:

- agent runtime,
- coding agent,
- skill library,
- harness,
- verifier,
- guardrail,
- review gate,
- evaluation case.

### Tests pass locally but CI fails

Run the exact CI sequence locally:

```bash
python3 -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

Then inspect `.github/workflows/quality.yml` for missing install, test, validation, timeout, or read-only permission settings.

## Maintainer Loop

Use this loop for continuous improvement:

```text
1. Find the weakest uncovered failure mode.
2. Add or update an eval or validator first.
3. Improve the smallest doc, skill, template, or schema that closes the gap.
4. Run validation.
5. Commit a small coherent chunk.
6. Repeat.
```

High-priority hardening targets:

- README detail and harness usability,
- command edge cases,
- skill trigger clarity,
- eval coverage for common failures,
- schema/template alignment,
- CI and local validation parity,
- public-copy neutrality,
- install and handoff instructions that another agent can follow without guessing.

## Status

v0.2.0 rewrite complete and now under continuous hardening. The repo is documentation-first, with portable commands, skills, schemas, eval cases, adapters, and validation checks ready for iterative improvement.

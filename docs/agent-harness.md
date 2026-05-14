# Agent Harness

Agent Brain should be usable as a harness: a repo that another agent can read, install, validate, and follow without guessing the workflow.

The harness is not a chat prompt. It is a controlled operating environment made from commands, skills, templates, schemas, evals, and review gates.

## Install

From a fresh checkout:

```bash
git clone https://github.com/rohitg00/agentbrain.git
cd agentbrain
python3 -m pip install -r requirements-dev.txt
rm -rf scripts/__pycache__ tests/__pycache__
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

Then run the targeted exact-name scrub from `README.md#validation` before committing public copy changes. The harness is ready only when tests, validation, whitespace checks, and the scrub gate pass.

## Fresh Checkout Bootstrap

Before a new agent acts on this repo, make it prove the checkout state instead of relying on private session context:

```bash
git status --short
git log --oneline -5
rm -rf scripts/__pycache__ tests/__pycache__
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

For public docs, commands, skills, templates, schemas, or evals, also run the targeted exact-name scrub before treating baseline validation as complete.

Use the results to answer four setup questions:

1. Is the working tree clean or are there user changes that must be preserved?
2. What is the latest committed harness behavior?
3. Do tests and validation pass before new work starts?
4. Which state, command, skill, template, and schema should handle the request?

If any answer is missing, stop with a handoff report. Do not choose a command, edit files, or delegate work from an unverified checkout.

If a previous handoff exists, re-run baseline validation, treat notes as stale until files and commands confirm them, and resume only the named next action. Do not trust old status copy, repeat broad discovery, or skip blockers recorded by the earlier run.

## Operating Loop

Every agent run should follow this sequence:

```text
1. Read AGENTBRAIN.md, PRINCIPLES.md, and ANTI_RATIONALIZATION.md.
2. Identify the current state from docs/state-machine.md.
3. Load the matching command from commands/.
4. Load only the skills required by the command.
5. Produce the artifact from templates/ or the command output contract.
6. Validate claims with source evidence, tests, logs, traces, or screenshots.
7. Apply review gates before handoff, merge, deploy, or public output.
8. Capture durable learning only when the lesson will remain useful.
```

The agent should not treat every task as implementation. Agent Brain often routes work to research, challenge, design, review, or learning before build.

## Command Routing

Use the earliest command that closes the current evidence gap. This table keeps the harness doc self-contained for agents that start here before reading the README catalog.

| Request or gap | Route to | Evidence before moving on |
| --- | --- | --- |
| Raw request, unclear state, or missing setup context | `/brain-start` | Request classification, checked files, and next safe state. |
| Product or automation may not deserve an agent | `/brain-should-this-exist` | User, problem, alternatives, success metric, and kill criteria. |
| Current facts, APIs, claims, or external signals need grounding | `/brain-research` | Source-backed claim ledger with dates and inspected URLs or files. |
| Assumptions are soft or requirements are fuzzy | `/brain-grill` | Answered challenge questions, unresolved risks, and decision criteria. |
| Product scope or user story is needed | `/brain-brief` | Brief with facts, assumptions, open questions, risks, and acceptance criteria. |
| Interface, workflow, states, or edge cases are underspecified | `/brain-design` | User flow, state model, failure paths, and UX constraints. |
| Implementation is ready to slice | `/brain-plan` | Ordered vertical slices, test or validator command, and rollback path. |
| Code, docs, schemas, templates, commands, or skills need creation | `/brain-build` | Existing plan plus test-first or validator-first proof for the slice. |
| Proof is missing or a claim must be checked | `/brain-verify` | Tests, logs, diffs, traces, screenshots, citations, or approval evidence. |
| Agent output needs trust review before handoff | `/brain-review` | Correctness, safety, maintainability, scope, and evidence review. |
| Release, merge, deploy, or public change is being considered | `/brain-ship` | Go/no-go, rollback, monitoring, support path, and launch notes. |
| Repeated work should become durable knowledge | `/brain-learn` | Pattern, trigger, artifact update, validation, and future failure mode. |
| Project knowledge should be refreshed | `/brain-wiki` | Source-backed facts with freshness and stale-memory rejection. |
| Harness behavior itself needs testing | `/brain-eval` | Eval case, rubric result, failure evidence, and follow-up hardening slice. |

If no route fits, stop with a handoff report instead of inventing a new command silently. Add a new command only as a separate validator-backed hardening slice.

## Handoff Contract

Every handoff should include:

```text
State: <current Agent Brain state>
Artifact: <brief, plan, QA evidence, review, launch decision, learning note>
Evidence checked: <commands, files, sources, logs, screenshots, traces>
Fresh validation proof: <command, exit status, and relevant output from the current run>
Facts: <verified statements>
Assumptions: <explicit assumptions>
Open questions: <unknowns that change the decision>
Risks: <product, engineering, security, launch, maintenance>
Stop conditions: <conditions that blocked or would block progress>
Next action: <smallest safe next step>
```

A handoff without evidence is incomplete. A handoff that hides uncertainty is unsafe.

## Stop Conditions

Stop and report a blocker when:

- the user, problem, or success metric is undefined,
- the request is better served by a non-agent system,
- a build is requested before spec, plan, or evidence,
- external claims have no source-backed ledger,
- the artifact cannot name facts, assumptions, and open questions,
- the agent claims tests passed without test output,
- a side effect needs approval,
- secret-like values appear in output,
- a long-running or recursive workflow has no stop condition,
- rollback is missing for a launch or production change,
- a skill would become broad framework creep instead of a small reusable workflow.

Blocked output should be explicit:

```text
Status: blocked
Blocker: <specific reason>
Evidence checked: <what was inspected>
Evidence missing: <what would unblock>
Safe next action: <smallest next step>
```

## Copyable Harness Prompt

Use this prompt when handing the repo to another capable coding agent:

```text
Read AGENTBRAIN.md, PRINCIPLES.md, ANTI_RATIONALIZATION.md, and docs/state-machine.md before acting.
Inspect git status --short and git log --oneline -5 before choosing work.
Run baseline validation before editing.
Preserve user changes before editing.
Choose the matching command in commands/ and load only its listed skills.
Use templates/ and schemas/ for structured artifacts when they fit.
Run python -m pytest -q, python scripts/validate_repo.py, git diff --check, and a targeted exact-name scrub before claiming completion.
Stop and report blockers when evidence, approval, scope, tests, rollback, secrets handling, safety, or loop limits are missing.
```

## Using It With Coding Agents

When feeding this repo to a coding agent, use the copyable prompt above as the baseline instruction. Keep the run scoped to the current command, skill, artifact, verification, and next state; if evidence is missing, stop instead of improvising.

For large work, split into worker scopes. Each worker scope must name its evidence inputs, stop condition, and handoff contract before it starts:

- researcher: source-backed claim ledger,
- planner: small verifiable implementation slices,
- builder: one slice at a time,
- verifier: tests, logs, screenshots, traces,
- reviewer: correctness, security, maintainability, edge cases,
- shipper: launch, rollback, support path,
- learner: durable lessons and skill updates.

No worker should approve its own unsupported claims, and every worker handoff should include checked evidence, blockers, residual risks, and the smallest safe next action.

## Edge Cases

### The user asks to move fast

Reduce scope. Do not remove verification.

### The agent finds a clever shortcut

Write the assumption and evidence. If evidence is missing, it is not a shortcut; it is risk.

### The agent wants to import an external workflow wholesale

Distill one job-to-be-done into a neutral skill. Do not copy source naming, branding, or broad framework shape unless the work is explicitly a comparison.

### The work is documentation-only

Still run validation. Docs are executable context for future agents, so broken docs are broken behavior.

### The work is already built

Run verifier and review gates. Existing output still needs evidence before trust.

## Troubleshooting

### Validation fails before any change

Treat the repo as untrusted until the baseline is explained. Capture the failing command, inspect the exact validator or test error, and fix the harness before asking another agent to rely on it.

### The next state is unclear

Return to `docs/state-machine.md` and choose the earliest state that can produce evidence. When multiple states seem plausible, prefer research, challenge, or planning over implementation.

### A command and skill disagree

Follow the stricter stop condition, then update the stale command, skill, template, or validator in a small verified slice. Do not let a one-off run create a hidden fork of the operating rules.

### An external source looks useful but branded

Extract the operator job, triggers, evidence, and failure modes. Public docs should name the neutral pattern, while session-specific source notes should stay out of promoted copy unless a comparison section is explicitly requested.

### A worker reports success without proof

Route the output through verification and review. Ask for or collect the missing logs, diffs, traces, screenshots, citations, or approvals before accepting the result.

### The working tree is dirty

Run `git status --short` and classify every changed path before editing. Preserve user changes by leaving unrelated files unstaged, creating a narrow patch, or stopping with a handoff when ownership is unclear. Do not clean, reset, stage, or overwrite a dirty working tree just to make validation easier.

### Secret-like values appear

Treat secret-like values as a blocker, not as normal copy. Remove the value from public artifacts, replace it with a redacted placeholder, rotate the real credential outside the repo, and rerun validation before continuing.

### Tests pass locally but CI fails

Run the exact CI sequence locally, including install, tests, repository validation, and whitespace checks. Inspect `.github/workflows/quality.yml` for Python version, dependency, permission, trigger, or timeout drift before changing production docs or code.

### Dependency bootstrap fails

If validation fails with `ModuleNotFoundError`, create or refresh a virtual environment, rerun `python3 -m pip install -r requirements-dev.txt`, and retry the quality gate. Do not edit around missing dependencies or assume global packages match CI.

### Generated cache files appear

If validation reports a generated Python cache file, delete `__pycache__/`, `.pytest_cache/`, or tracked bytecode artifacts, then rerun the full quality gate. Generated caches are local execution residue and should not become harness state.

## Maintainer Checklist

Before a harness release or major push:

- README can bootstrap a new agent without private context.
- Commands and skills are all cataloged.
- Required docs are linked or discoverable.
- Evals cover the newest failure modes.
- Validator catches structural regressions.
- CI mirrors local validation.
- Public copy uses neutral pattern names.
- No generated cache files are tracked.
- Latest commit is verified on the remote branch.

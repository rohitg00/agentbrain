# Agent Harness

Agent Brain should be usable as a harness: a repo that another agent can read, install, validate, and follow without guessing the workflow.

The harness is not a chat prompt. It is a controlled operating environment made from commands, skills, templates, schemas, evals, and review gates.

## Install

From a fresh checkout:

```bash
git clone https://github.com/rohitg00/agentbrain.git
cd agentbrain
python3 -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

The harness is ready only when tests, validation, and whitespace checks pass.

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

## Handoff Contract

Every handoff should include:

```text
State: <current Agent Brain state>
Artifact: <brief, plan, QA evidence, review, launch decision, learning note>
Evidence checked: <commands, files, sources, logs, screenshots, traces>
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

## Using It With Coding Agents

When feeding this repo to a coding agent, use this instruction:

```text
Use Agent Brain as the operating harness.
Do not skip directly to implementation.
Choose the state, command, skill, artifact, verification, and next state.
If evidence is missing, stop.
Before claiming completion, run the local validation gate.
```

For large work, split into worker scopes:

- researcher: source-backed claim ledger,
- planner: small verifiable implementation slices,
- builder: one slice at a time,
- verifier: tests, logs, screenshots, traces,
- reviewer: correctness, security, maintainability, edge cases,
- shipper: launch, rollback, support path,
- learner: durable lessons and skill updates.

No worker should approve its own unsupported claims.

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

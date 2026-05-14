# Implementation Roadmap

Status: v0.2.0 checkpoints completed. This file remains as the checkpoint ledger showing how the rewrite was chunked, reviewed, and committed without one giant dump.

## Goal

Rewrite Agent Brain from a generic prompt/workflow repo into a research-backed, evidence-first operating system for agents.

Agent Brain should help any capable agent decide:

1. whether something should exist,
2. whether it should be an agent at all,
3. what evidence is missing,
4. what questions must be answered,
5. what plan is small enough to verify,
6. what review gates must pass,
7. what learning should become durable skill or wiki knowledge.

## Non-goals

- Do not clone any single source repo's structure.
- Do not mention competitor/project names in public copy as positioning.
- Do not make the repo runtime-specific.
- Do not optimize for hype, stars, or social copy.
- Do not build a CLI before the portable markdown core is coherent.

## Commit plan

Each checkpoint should be a separate commit.

### 0. Roadmap and guardrails

- Add this roadmap.
- Define work chunks and validation expectations.

Expected commit:

```text
docs: add v0.2.0 rewrite roadmap
```

### 1. Research-backed critique foundation

Add:

- `docs/ecosystem-review.md`
- `docs/claims-we-reject.md`
- `docs/non-agent-alternatives.md`

Purpose:

- record what patterns were studied,
- explain what Agent Brain keeps,
- explain what it rejects,
- avoid building from only two reference repos.

Expected commit:

```text
docs: add research-backed critique foundation
```

### 2. Constitution and anti-rationalization core

Rewrite/add:

- `AGENTBRAIN.md`
- `PRINCIPLES.md`
- `ANTI_RATIONALIZATION.md`
- `README.md`

Purpose:

- make disagreement, evidence, and stop conditions first-class,
- define when the agent must ask questions,
- define when the agent must recommend not building.

Expected commit:

```text
docs: rewrite agent brain constitution
```

### 3. State machine and schemas

Add:

- `docs/state-machine.md`
- `schemas/*.schema.json`
- `scripts/validate_repo.py`

Purpose:

- make artifacts checkable,
- define states, exits, and required evidence,
- catch broken links/schema JSON before pushes.

Expected commit:

```text
feat: add state machine and artifact schemas
```

### 4. Slash command specifications

Rewrite/add command specs:

- `/brain-start`
- `/brain-should-this-exist`
- `/brain-research`
- `/brain-grill`
- `/brain-brief`
- `/brain-design`
- `/brain-plan`
- `/brain-build`
- `/brain-verify`
- `/brain-review`
- `/brain-ship`
- `/brain-learn`
- `/brain-wiki`
- `/brain-eval`

Expected commit:

```text
feat: formalize brain slash commands
```

### 5. Portable skills rewrite

Rewrite/add core skills:

- `intake`
- `evidence-research`
- `question-ladder`
- `problem-grill`
- `market-grill`
- `design-grill`
- `engineering-grill`
- `plan-slicing`
- `qa-evidence`
- `launch-gate`
- `learning-capture`
- `wiki-maintenance`

Each skill must include:

- trigger,
- inputs,
- procedure,
- anti-rationalization table,
- verification,
- output artifact,
- examples,
- failure modes.

Expected commit:

```text
feat: rewrite core portable skills
```

### 6. Evals and adapters

Add:

- `evals/cases/*`
- `evals/rubrics/*`
- `adapters/hermes/*`
- `adapters/plain-markdown/*`

Purpose:

- make the brain testable,
- show how to install/use it without locking to a runtime.

Expected commit:

```text
feat: add eval cases and initial adapters
```

### 7. Final validation and version marker

Add/update:

- changelog or version note,
- validation report,
- repository history inspection.

Expected commit:

```text
chore: mark v0.2.0 rewrite complete
```

## Validation checklist

Before every push:

- `python3 scripts/validate_repo.py`
- `git status --short`
- `git log --oneline --max-count=12`
- search for banned public-copy terms if relevant
- confirm commits are authored as `rohitg00 <rohitg00@users.noreply.github.com>`

## Banned failure modes

- One giant commit.
- Writing broad claims without source-backed rationale.
- Creating skills without verification steps.
- Building runtime code before docs/schemas/evals are coherent.
- Treating an agent solution as the default.
- Forgetting to update this roadmap when a checkpoint changes.

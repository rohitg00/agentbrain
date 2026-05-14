# Ecosystem Review

This document records the research foundation behind Agent Brain v0.2.0 without positioning the project as a clone or comparison against any specific public project.

## Method

The review studied public agent workflow patterns across these families:

1. engineering skill packs,
2. personal engineering workflow skills,
3. persistent markdown knowledge-base systems,
4. production agent runtimes,
5. type-safe AI engineering stacks,
6. minimal graph/shared-store frameworks,
7. local portable skill systems,
8. recent community discussion about agent reliability.

The goal was not to copy structure. The goal was to identify durable patterns, failure modes, and missing quality bars.

## What the ecosystem gets right

### 1. Skills are useful when they are workflows, not essays

The strongest skill packs do not merely describe best practices. They tell the agent what to do, when to stop, what artifact to produce, and what evidence is required.

A usable skill has:

- a trigger,
- required inputs,
- ordered steps,
- explicit outputs,
- verification,
- failure modes,
- examples.

Agent Brain adopts this pattern and rejects long, vague instruction dumps.

### 2. Agents need anti-shortcut rules

Agents and humans both rationalize shortcuts. Common shortcuts include:

- building before understanding,
- skipping tests,
- accepting vague success criteria,
- treating a passing check as product validation,
- calling a simple script an agent,
- declaring something done without evidence.

Agent Brain treats anti-rationalization as a first-class primitive.

### 3. Persistent knowledge should compound

The best knowledge-base pattern separates:

- immutable raw sources,
- synthesized wiki pages,
- indexes,
- logs,
- contradictions,
- source drift.

Agent Brain uses this idea for research and product decisions. Claims should not vanish into chat history.

### 4. Runtime matters for real agents

Production agents need more than prompts:

- durable execution,
- resumable state,
- human approval checkpoints,
- observability,
- evaluation datasets,
- tool permissions,
- retry and replay,
- scheduled runs.

Agent Brain remains runtime-agnostic but defines state and artifacts so runtimes can implement it safely.

### 5. Evaluation is the difference between a brain and a prompt pile

A workflow repository without evals becomes brittle. Agent Brain must include cases that check whether an agent:

- asks clarifying questions,
- challenges weak assumptions,
- recommends non-agent alternatives,
- avoids premature implementation,
- produces complete artifacts,
- captures reusable learning.

## What the ecosystem misses

### 1. Too much focus on building, not enough on deciding

Many agent workflows improve implementation after the decision to build has already been made. Agent Brain starts earlier:

> Should this exist? Should it be an agent? What evidence would kill it?

### 2. Too little product skepticism

Agents often optimize for satisfying the user request, even when the request is weak. Agent Brain requires constructive disagreement.

### 3. Too little source accountability

Community hype is not evidence. Agent Brain distinguishes:

- source-backed evidence,
- user-provided assumptions,
- agent hypotheses,
- open questions,
- kill criteria.

### 4. Too little portability

Many systems are tied to one editor, model, runtime, or command interface. Agent Brain keeps a portable markdown core with adapters.

### 5. Too little maintenance design

Skills and memory decay. Agent Brain requires review, consolidation, evals, and learning capture so the system improves instead of accumulating stale instructions.

## Agent Brain design response

Agent Brain v0.2.0 will use five layers:

1. **Constitution** — behavioral rules, stop conditions, anti-rationalization.
2. **State machine** — states, artifacts, exits, and gates.
3. **Command specs** — user-facing workflows.
4. **Skills** — reusable procedures with verification.
5. **Adapters and evals** — runtime-specific installation plus quality checks.

## Core thesis

Agent Brain is not a prompt collection.

Agent Brain is an evidence-first operating system for agents that turns raw intent into decisions, artifacts, verification, review, and durable learning.

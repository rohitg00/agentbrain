# Implementation Plan

This plan is a living maintainer guide for hardening Agent Brain as a self-setup harness. It should describe the next useful slices, not historical bootstrap tasks.

## Goal

Make the repo usable by another capable coding agent without private context: install dependencies, understand the operating loop, choose commands and skills, create artifacts, verify evidence, recover from failures, and hand off safely.

## Operating Rules

- Start every slice from `git status --short` and `git log --oneline -5` evidence.
- Add or update a test, eval, validator rule, or schema check before changing protected behavior.
- Keep public copy neutral when distilling external sources into reusable operator patterns.
- Run the full local quality gate before commit: cache cleanup, tests, repository validation, and whitespace check.
- Push only when the requested workflow authorizes remote side effects, then fetch and confirm local HEAD matches `origin/main`.

## Current Hardening Themes

### 1. Harness bootstrap and routing

Keep `README.md` and `docs/agent-harness.md` strong enough for fresh-checkout setup, command selection, edge-case handling, troubleshooting, and handoff without chat history.

### 2. Validator-backed structure

Prefer structural checks over prose reminders. When the repo learns a failure mode, encode it in `scripts/validate_repo.py`, a focused test, or an eval case so future runs cannot silently regress.

### 3. Skill and command quality

Keep skills small, trigger-driven, and composable. Keep commands tied to one lifecycle state with explicit inputs, loaded skills, workflow, output contract, stop conditions, and quality bar.

### 4. Evidence and review

Require proof before trust: test output, validation logs, source citations, diffs, screenshots, traces, approval records, or CI run evidence depending on the task.

### 5. Learning and memory hygiene

Route durable lessons into docs, skills, templates, schemas, evals, or validator rules. Reject temporary task logs, stale status notes, raw private data, and secrets as memory.

## Next Slice Selection

Choose the weakest uncovered failure mode in this order:

1. A setup or validation gap that would block a fresh agent.
2. A stale doc, command, skill, template, or schema contract that could route work incorrectly.
3. A missing eval for a repeated agent failure mode.
4. A public-copy neutrality gap around external source distillation.
5. A maintainability gap in tests, validators, or CI.

For each slice, record the failing proof, implement the smallest fix, run the targeted proof, run the full quality gate, inspect the diff, then commit with a conventional message.

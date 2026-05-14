# Agent Brain Implementation Plan

> For agents: implement this repo task-by-task. Do not push to a remote until the owner approves.

## Goal

Create a portable brain for AI agents that guides product creation, planning, review, QA, shipping, and learning through reusable Markdown skills and templates.

## Milestone 1 — Portable docs pack

- Create constitution
- Create command specs
- Create core skills
- Create product/planning/review templates
- Create memory model
- Create contribution rules

## Milestone 2 — Installer and adapters

- Add install script to copy skills into supported runtimes
- Add runtime adapter interface
- Add validation command for skill shape
- Add docs generation

## Milestone 3 — Evaluation

- Add scenario tests for every skill
- Add rubric-based review for outputs
- Add examples of good and bad interactions
- Add regression fixtures for known agent failure modes

## Milestone 4 — Runtime memory integration

- Add optional local markdown knowledge base
- Add optional search index
- Add memory write policy and linting
- Add skill creation workflow

## Milestone 5 — Team workflow

- Add role bundles: product, design, engineering, QA, launch
- Add orchestration guide for multiple agents
- Add dashboard/status spec

## Immediate next tasks

1. Review this draft for naming and public positioning.
2. Approve creating the GitHub repository under the owner account.
3. Push the docs-only v0.1.
4. Open issues for installer, adapters, and eval harness.

# Skills

Agent Brain skills are small, composable, runtime-neutral operating procedures. A command chooses the state, then loads only the skills needed for the current slice. Keep the developer or maintainer in control: skills provide procedure, evidence requirements, verification, and stop conditions; they do not silently own the whole workflow.

## How to use this catalog

1. Start from the selected `/brain-*` command.
2. Load only the skills listed in that command's **Skills to load** section.
3. Follow the skill's trigger, inputs, procedure, verification, output artifact, failure modes, and example.
4. If no skill fits, do not stretch a broad skill across unrelated work. Record the gap and add the smallest new skill with validator or eval coverage.
5. Keep public copy neutral. Distill external inspiration into operator patterns instead of source-specific names or commands.

## Catalog

- [`activity-recap`](activity-recap/SKILL.md) — summarize activity into evidence-backed next actions without turning temporary logs into durable memory.
- [`agent-output-verifier`](agent-output-verifier/SKILL.md) — review agent output for evidence, safety, skipped checks, and handoff readiness.
- [`ci-recovery`](ci-recovery/SKILL.md) — inspect failing CI, reproduce locally, fix the smallest cause, and re-check the remote run.
- [`context-memory`](context-memory/SKILL.md) — decide whether context belongs in stable preferences, project docs, session recall, skills, or external indexes.
- [`design-grill`](design-grill/SKILL.md) — challenge workflow, interface, state, and edge-case assumptions before design hardens.
- [`domain-language`](domain-language/SKILL.md) — align project vocabulary so commands, skills, docs, tests, and handoffs use the same terms.
- [`engineering-grill`](engineering-grill/SKILL.md) — pressure-test technical assumptions, constraints, failure modes, and verification before implementation.
- [`evidence-research`](evidence-research/SKILL.md) — gather source-backed evidence and separate facts, assumptions, and recheck triggers.
- [`intake`](intake/SKILL.md) — classify a raw request, inspect retrievable context, and choose the earliest safe harness state.
- [`launch-gate`](launch-gate/SKILL.md) — check release readiness, rollback, monitoring, approvals, and go/no-go evidence.
- [`learning-capture`](learning-capture/SKILL.md) — convert repeated outcomes into durable docs, skills, templates, evals, schemas, or validators.
- [`market-grill`](market-grill/SKILL.md) — challenge market, user, distribution, and evidence assumptions before product commitment.
- [`plan-slicing`](plan-slicing/SKILL.md) — split work into small vertical slices with acceptance checks and verification commands.
- [`problem-grill`](problem-grill/SKILL.md) — challenge whether the problem is real, important, and best solved by an agent.
- [`qa-evidence`](qa-evidence/SKILL.md) — collect proof from tests, validators, logs, screenshots, traces, citations, and diffs.
- [`question-ladder`](question-ladder/SKILL.md) — narrow ambiguity with progressive questions while inspecting retrievable context first.
- [`runtime-smoke`](runtime-smoke/SKILL.md) — check Agent Brain inside a real runtime or adapter and record smoke evidence honestly.
- [`wiki-maintenance`](wiki-maintenance/SKILL.md) — update durable project knowledge with provenance, freshness, and stale-data review.

## Quality bar for new skills

- The frontmatter description starts with a precise `Use when` trigger.
- The skill is small enough to compose with commands and other skills.
- The procedure names concrete steps, not generic advice.
- Verification is runnable or inspectable.
- The output artifact is explicit.
- Failure modes and stop conditions prevent unsafe or unverified progress.
- At least one command loads the skill, and this catalog links to it.

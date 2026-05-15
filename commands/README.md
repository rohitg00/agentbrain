# Command Catalog

Use this catalog when an agent runtime cannot expose `/brain-*` entries as native commands. Treat each command file as a markdown spec, load only the skills listed by that command, produce the required artifact, and stop instead of inventing unsupported routes.

Each catalog entry preserves the command boundary for runtimes with or without native command support: lifecycle state, skills to load, required artifact, stop condition, and link to the markdown spec. If those fields are missing, the harness cannot prove command routing or artifact handoff behavior in a real runtime smoke.

## Routing rules

1. Start from `README.md`, `AGENTBRAIN.md`, `PRINCIPLES.md`, and `docs/state-machine.md`.
2. Pick the earliest safe lifecycle state, then open the matching command below.
3. If the runtime has native command support, invoke the native command only after checking that it maps to the same markdown spec.
4. If the runtime has no native command support, read the command file directly and follow its input contract, skills, workflow, output artifact, stop conditions, and quality bar.
5. Record the selected command, loaded skills, artifact path, validation evidence, blockers, stop condition, and next action in the handoff.

## Commands

- [`/brain-brief`](brain-brief.md) — State: DESIGN; Skills: `evidence-research`, `problem-grill`; Artifact: `templates/product-brief.md`; Stop: missing user/problem evidence, unresolved assumptions, or unsafe scope.
- [`/brain-build`](brain-build.md) — State: BUILD; Skills: `plan-slicing`, `qa-evidence`; Artifact: `templates/changed-artifact-plus-implementation-notes.md`; Stop: no approved slice, no failing test or validator-first proof, or red checks.
- [`/brain-design`](brain-design.md) — State: DESIGN; Skills: `design-grill`, `engineering-grill`; Artifact: `templates/design-brief.md`; Stop: missing state, flow, edge-case, accessibility, or risk evidence.
- [`/brain-eval`](brain-eval.md) — State: VERIFY; Skills: `agent-output-verifier`, `ci-recovery`, `evidence-research`, `qa-evidence`, `runtime-smoke`; Artifact: `templates/eval-report.md`; Stop: missing case, rubric, evidence, or runtime proof.
- [`/brain-grill`](brain-grill.md) — State: CHALLENGE; Skills: `design-grill`, `engineering-grill`, `market-grill`, `problem-grill`; Artifact: `templates/grill-report.md`; Stop: retrievable context is unchecked or a question changes scope.
- [`/brain-learn`](brain-learn.md) — State: LEARN; Skills: `context-memory`, `learning-capture`, `wiki-maintenance`; Artifact: `templates/learning-capture.md`; Stop: lesson is temporary task chatter, private data, or not reusable.
- [`/brain-plan`](brain-plan.md) — State: PLAN; Skills: `engineering-grill`, `plan-slicing`; Artifact: `templates/implementation-plan.md`; Stop: slice lacks acceptance checks, verification command, or rollback path.
- [`/brain-research`](brain-research.md) — State: RESEARCH; Skills: `evidence-research`, `wiki-maintenance`; Artifact: `templates/research-claim-ledger.md`; Stop: source provenance, freshness, or recheck trigger is missing.
- [`/brain-review`](brain-review.md) — State: REVIEW; Skills: `agent-output-verifier`, `engineering-grill`; Artifact: `templates/review-report.md`; Stop: diff, evidence, security, maintainability, or side-effect scope is unchecked.
- [`/brain-ship`](brain-ship.md) — State: SHIP; Skills: `launch-gate`, `qa-evidence`; Artifact: `templates/launch-checklist.md`; Stop: rollout, rollback, monitoring, approval, or CI proof is missing.
- [`/brain-should-this-exist`](brain-should-this-exist.md) — State: DECIDE; Skills: `market-grill`, `problem-grill`; Artifact: `templates/non-agent-alternative-review.md`; Stop: non-agent alternatives, risk, user, or success evidence is missing.
- [`/brain-start`](brain-start.md) — State: INTAKE; Skills: `domain-language`, `intake`, `question-ladder`; Artifact: `templates/intake-summary.md`; Stop: no safe default exists for missing context in a noninteractive run.
- [`/brain-verify`](brain-verify.md) — State: VERIFY; Skills: `agent-output-verifier`, `ci-recovery`, `qa-evidence`, `runtime-smoke`; Artifact: `templates/qa-evidence.md`; Stop: proof is stale, missing, unverifiable, or only a prose summary.
- [`/brain-wiki`](brain-wiki.md) — State: LEARN; Skills: `activity-recap`, `evidence-research`, `wiki-maintenance`; Artifact: `templates/wiki-update.md`; Stop: knowledge lacks provenance, freshness, or durable project value.

## Failure modes

- Do not assume `/brain-*` entries are native commands in every runtime.
- Do not load broad skill bundles when the command lists a smaller set.
- Do not produce free-form summaries when a command names a template and schema.
- Do not continue if the selected route needs approval, credentials, destructive access, or evidence that the runtime cannot provide.

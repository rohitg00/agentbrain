# Command Catalog

Use this catalog when an agent runtime cannot expose `/brain-*` entries as native commands. Treat each command file as a markdown spec, load only the skills listed by that command, produce the required artifact, and stop instead of inventing unsupported routes.

Each catalog entry preserves the command boundary for runtimes with or without native command support: lifecycle state, use-when routing signal, skills to load, required artifact, native-command boundary, stop condition, and link to the markdown spec. If those fields are missing, the harness cannot prove command routing or artifact handoff behavior in a real runtime smoke.

## Routing rules

1. Start from `README.md`, `AGENTBRAIN.md`, `PRINCIPLES.md`, and `docs/state-machine.md`.
2. Pick the earliest safe lifecycle state, then open the matching command below.
3. If the runtime has native command support, invoke the native command only after checking that it maps to the same markdown spec.
4. If the runtime has no native command support, read the command file directly and follow its input contract, skills, workflow, output artifact, stop conditions, and quality bar.
5. Record the selected command, loaded skills, artifact path, validation evidence, blockers, stop condition, and next action in the handoff.

Tie-break ambiguous routes by choosing the earliest safe lifecycle state, preferring `/brain-verify` for proof gaps, preferring `/brain-review` for trust gaps, and stopping when no command fits instead of inventing a route.

## Commands

- [`/brain-brief`](brain-brief.md) — State: DESIGN; Use when: after intake, research, and grill have enough signal; Skills: `evidence-research`, `problem-grill`; Artifact: `templates/product-brief.md`; Schema: `schemas/product-brief.schema.json`; Native: markdown spec unless runtime maps `/brain-brief` to a native command; Stop: target user, decision owner, or success metric for the brief is unnamed.
- [`/brain-build`](brain-build.md) — State: BUILD; Use when: an implementation plan has a selected task and validation method; Skills: `plan-slicing`, `qa-evidence`; Artifact: `templates/changed-artifact-plus-implementation-notes.md`; Schema: `schemas/changed-artifact-plus-implementation-notes.schema.json`; Native: markdown spec unless runtime maps `/brain-build` to a native command; Stop: implementation slice is not approved or lacks acceptance checks.
- [`/brain-design`](brain-design.md) — State: DESIGN; Use when: a product brief needs ux or interaction design before planning; Skills: `design-grill`, `engineering-grill`; Artifact: `templates/design-brief.md`; Native: markdown spec unless runtime maps `/brain-design` to a native command; Stop: user, scenario, constraints, or non-goals are missing.
- [`/brain-eval`](brain-eval.md) — State: VERIFY; Use when: changing Agent Brain behavior or checking quality; Skills: `agent-output-verifier`, `ci-recovery`, `evidence-research`, `qa-evidence`, `runtime-smoke`; Artifact: `templates/eval-report.md`; Schema: `schemas/eval-report.schema.json`; Native: markdown spec unless runtime maps `/brain-eval` to a native command; Stop: eval target, rubric, fixture, or expected behavior is undefined.
- [`/brain-grill`](brain-grill.md) — State: CHALLENGE; Use when: the idea, brief, design, or plan has unresolved assumptions; Skills: `design-grill`, `engineering-grill`, `market-grill`, `problem-grill`; Artifact: `templates/grill-report.md`; Native: markdown spec unless runtime maps `/brain-grill` to a native command; Stop: code/docs cannot answer a blocking question and the user is unavailable.
- [`/brain-learn`](brain-learn.md) — State: LEARN; Use when: after repeated success/failure, a tricky fix, or a shipped workflow; Skills: `context-memory`, `learning-capture`, `wiki-maintenance`; Artifact: `templates/learning-capture.md`; Native: markdown spec unless runtime maps `/brain-learn` to a native command; Stop: lesson is temporary task state rather than durable project behavior.
- [`/brain-plan`](brain-plan.md) — State: PLAN; Use when: the brief/design is strong enough to implement; Skills: `engineering-grill`, `plan-slicing`; Artifact: `templates/implementation-plan.md`; Schema: `schemas/implementation-plan.schema.json`; Native: markdown spec unless runtime maps `/brain-plan` to a native command; Stop: objectives, constraints, owner, or acceptance criteria are not defined.
- [`/brain-research`](brain-research.md) — State: RESEARCH; Use when: the decision depends on external evidence or unfamiliar domain context; Skills: `evidence-research`, `wiki-maintenance`; Artifact: `templates/research-claim-ledger.md`; Native: markdown spec unless runtime maps `/brain-research` to a native command; Stop: claim cannot be grounded in primary or authoritative evidence.
- [`/brain-review`](brain-review.md) — State: REVIEW; Use when: after verification or before public/shipping decisions; Skills: `agent-output-verifier`, `engineering-grill`; Artifact: `templates/review-report.md`; Schema: `schemas/review-report.schema.json`; Native: markdown spec unless runtime maps `/brain-review` to a native command; Stop: diff, artifact, or intended behavior is unavailable.
- [`/brain-ship`](brain-ship.md) — State: SHIP; Use when: a reviewed artifact is ready for release or publication; Skills: `launch-gate`, `qa-evidence`; Artifact: `templates/launch-checklist.md`; Native: markdown spec unless runtime maps `/brain-ship` to a native command; Stop: validation, review, rollback, monitoring, or ownership evidence is missing.
- [`/brain-should-this-exist`](brain-should-this-exist.md) — State: DECIDE; Use when: before planning any new product, feature, workflow, or automation; Skills: `market-grill`, `problem-grill`; Artifact: `templates/non-agent-alternative-review.md`; Native: markdown spec unless runtime maps `/brain-should-this-exist` to a native command; Stop: target user, repeated job, or non-agent baseline is not concrete.
- [`/brain-start`](brain-start.md) — State: INTAKE; Use when: a user starts from a vague request, idea, task, or product ambition; Skills: `domain-language`, `intake`, `question-ladder`; Artifact: `templates/intake-summary.md`; Native: markdown spec unless runtime maps `/brain-start` to a native command; Stop: request lacks enough context to choose an initial state or command.
- [`/brain-verify`](brain-verify.md) — State: VERIFY; Use when: after build or when evaluating an existing artifact; Skills: `agent-output-verifier`, `ci-recovery`, `qa-evidence`, `runtime-smoke`; Artifact: `templates/qa-evidence.md`; Schema: `schemas/qa-evidence.schema.json`; Native: markdown spec unless runtime maps `/brain-verify` to a native command; Stop: artifact under test, expected behavior, or verification command is missing.
- [`/brain-wiki`](brain-wiki.md) — State: LEARN; Use when: ingesting sources or updating durable project knowledge; Skills: `activity-recap`, `evidence-research`, `wiki-maintenance`; Artifact: `templates/wiki-update.md`; Native: markdown spec unless runtime maps `/brain-wiki` to a native command; Stop: proposed wiki fact lacks a stable source, owner, or freshness date.

## Failure modes

- Do not assume `/brain-*` entries are native commands in every runtime.
- Do not add duplicate catalog rows for the same command; update the existing row so real-runtime routing probes see one state, one skill set, and one artifact contract.
- Do not load broad skill bundles when the command lists a smaller set.
- Do not produce free-form summaries when a command names a template and schema.
- Do not continue if the selected route needs approval, credentials, destructive access, or evidence that the runtime cannot provide.

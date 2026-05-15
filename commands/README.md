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

- [`/brain-brief`](brain-brief.md) — turn challenged scope into a product brief.
- [`/brain-build`](brain-build.md) — implement one approved, test-backed or validator-backed slice.
- [`/brain-design`](brain-design.md) — design flows, states, and edge cases before planning.
- [`/brain-eval`](brain-eval.md) — score harness behavior against eval cases and rubrics.
- [`/brain-grill`](brain-grill.md) — challenge assumptions and missing evidence.
- [`/brain-learn`](brain-learn.md) — capture reusable lessons into skills, docs, templates, schemas, or evals.
- [`/brain-plan`](brain-plan.md) — break approved work into small verifiable tasks.
- [`/brain-research`](brain-research.md) — ground claims in source-backed evidence.
- [`/brain-review`](brain-review.md) — inspect correctness, maintainability, security, and evidence before trust.
- [`/brain-ship`](brain-ship.md) — check rollout, rollback, monitoring, docs, and release readiness.
- [`/brain-should-this-exist`](brain-should-this-exist.md) — decide whether the work should exist or be an agent.
- [`/brain-start`](brain-start.md) — route raw intent into the earliest safe Agent Brain state.
- [`/brain-verify`](brain-verify.md) — collect proof that an artifact works.
- [`/brain-wiki`](brain-wiki.md) — maintain wiki-ready docs with validation evidence.

## Failure modes

- Do not assume `/brain-*` entries are native commands in every runtime.
- Do not load broad skill bundles when the command lists a smaller set.
- Do not produce free-form summaries when a command names a template and schema.
- Do not continue if the selected route needs approval, credentials, destructive access, or evidence that the runtime cannot provide.

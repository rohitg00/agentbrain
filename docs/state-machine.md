# State Machine

Agent Brain is a state machine, not a single prompt.

Each state has required inputs, required outputs, exit criteria, and allowed next states.

## States

```text
raw_request
intake
should_this_exist
research
grill
brief
design
plan
build
verify
review
ship
learn
archive
```

## State definitions

### raw_request

Input: user's unprocessed request.

Output: routing decision.

Exit criteria:

- request captured,
- urgency and ambiguity assessed,
- next state selected.

Allowed next states: `intake`, `research`, `plan`, `verify`, `review`, `learn`.

### intake

Input: raw request plus known context.

Output: intake summary and blocking questions.

Exit criteria:

- user, problem, desired outcome, constraints, and risk are either known or marked unknown.

Allowed next states: `should_this_exist`, `research`, `grill`, `brief`.

### should_this_exist

Input: intake summary.

Output: non-agent alternative review and existence decision.

Exit criteria:

- simpler alternatives considered,
- kill criteria written,
- agent justification accepted or rejected.

Allowed next states: `research`, `grill`, `archive`, `brief`.

### research

Input: question, domain, source constraints.

Output: research claim ledger.

Exit criteria:

- claims separated from assumptions,
- confidence assigned,
- contradictions and open questions listed.

Allowed next states: `grill`, `brief`, `archive`.

### grill

Input: intake/research/brief/plan.

Output: grill report.

Exit criteria:

- weak assumptions challenged,
- missing evidence listed,
- risks and kill criteria updated.

Allowed next states: `research`, `brief`, `design`, `plan`, `archive`.

### brief

Input: intake, research, grill findings.

Output: product brief.

Exit criteria:

- target user, problem, value, evidence, constraints, success metric, and non-goals are explicit.

Allowed next states: `design`, `plan`, `research`, `archive`.

### design

Input: product brief.

Output: design brief.

Exit criteria:

- user flow, states, edge cases, accessibility and failure states are covered.

Allowed next states: `plan`, `grill`, `archive`.

### plan

Input: brief and design.

Output: implementation plan.

Exit criteria:

- tasks are small, ordered, verifiable, and mapped to files or artifacts.

Allowed next states: `build`, `review`, `archive`.

### build

Input: implementation plan.

Output: changed artifact.

Exit criteria:

- only planned slice implemented,
- verification method is ready.

Allowed next states: `verify`, `plan`.

### verify

Input: changed artifact.

Output: QA evidence.

Exit criteria:

- tests, traces, screenshots, logs, source checks, or human approval captured.

Allowed next states: `review`, `build`, `plan`.

### review

Input: artifact plus evidence.

Output: review report.

Exit criteria:

- correctness, product fit, security, UX, and maintainability reviewed.

Allowed next states: `ship`, `build`, `plan`, `archive`.

### ship

Input: reviewed artifact.

Output: launch checklist and go/no-go decision.

Exit criteria:

- rollback, monitoring, approvals, and communication are clear.

Allowed next states: `learn`, `archive`.

### learn

Input: completed or abandoned loop.

Output: learning capture, wiki update, or skill proposal.

Exit criteria:

- reusable learning stored in the right place or explicitly skipped.

Allowed next states: `archive`, `intake`.

### archive

Input: stopped, shipped, or killed work.

Output: final note and location of artifacts.

Exit criteria:

- decision and reason are findable later.

Allowed next states: none.

## Command Mapping

Use the earliest command that matches the current unsafe gap. These mappings keep the state machine executable instead of leaving future agents to infer entrypoints from prose:

- `raw_request` -> `/brain-start` to classify the request and choose the first safe state.
- `intake` -> `/brain-start` to preserve facts, constraints, blockers, and the recommended next command.
- `should_this_exist` -> `/brain-should-this-exist` to compare agent work against safer non-agent alternatives.
- `research` -> `/brain-research` to collect source-backed evidence before claims, briefs, or plans.
- `grill` -> `/brain-grill` to challenge weak assumptions and missing evidence.
- `brief` -> `/brain-brief` to turn the problem into scope, acceptance criteria, and non-goals.
- `design` -> `/brain-design` to define flows, edge cases, and failure states.
- `plan` -> `/brain-plan` to create small vertical slices with verification commands.
- `build` -> `/brain-build` to implement only the selected slice with test-first or validator-first proof.
- `verify` -> `/brain-verify` for proof collection and `/brain-eval` when command, skill, or artifact behavior needs rubric evidence.
- `review` -> `/brain-review` to decide whether the artifact is safe to trust.
- `ship` -> `/brain-ship` to require rollback, monitoring, approvals, and go/no-go evidence.
- `learn` -> `/brain-learn` for reusable skills, templates, evals, validators, or memory updates, and `/brain-wiki` for durable project knowledge maintenance.

## Gate rule

A state cannot advance when its required artifact is missing unless the agent records an explicit assumption and risk.

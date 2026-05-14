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

## Gate rule

A state cannot advance when its required artifact is missing unless the agent records an explicit assumption and risk.

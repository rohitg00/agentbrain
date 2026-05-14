# Non-Agent Alternatives

Agent Brain requires agents to consider simpler alternatives before recommending an agentic system.

## Decision rule

Use the simplest system that can reliably solve the problem with acceptable maintenance cost.

An agent is appropriate only when the task requires some combination of:

- uncertain inputs,
- reasoning over context,
- tool choice,
- iterative investigation,
- human-in-loop judgment,
- adaptation over time,
- natural-language interaction,
- synthesis across sources.

If the task is deterministic, prefer deterministic automation.

## Alternative menu

### 1. Checklist

Use when the process is mostly human judgment with repeated steps.

Good for:

- launch reviews,
- content quality checks,
- onboarding,
- manual QA,
- security review prompts.

Avoid an agent if a checklist makes the human faster and safer.

### 2. Script

Use when inputs and outputs are well-defined.

Good for:

- file conversion,
- report generation,
- data cleanup,
- validation,
- deployment commands.

Prefer scripts when correctness matters more than interpretation.

### 3. Form or intake wizard

Use when the main problem is missing structured input.

Good for:

- product briefs,
- bug reports,
- feature requests,
- customer handoff,
- research requests.

Do not build an agent when a better form would solve the ambiguity.

### 4. Saved query or dashboard

Use when the task is recurring visibility.

Good for:

- metrics,
- status pages,
- issue queues,
- error monitoring,
- content calendars.

Do not build a chat agent to answer questions a dashboard can answer faster.

### 5. Cron job or scheduled report

Use when the task is periodic and mostly deterministic.

Good for:

- daily summaries,
- stale issue checks,
- uptime checks,
- feed monitoring,
- inventory refresh.

Add an agent only if the summary requires judgment or synthesis.

### 6. Runbook

Use when the process handles known incidents or operational tasks.

Good for:

- incident response,
- rollback,
- account setup,
- release process,
- data migration.

Agents may assist runbooks, but the runbook should remain readable without the agent.

### 7. Human approval workflow

Use when risk is high.

Good for:

- payments,
- destructive actions,
- account actions,
- production changes,
- sensitive data movement.

The agent can prepare context, but a human should approve.

## When an agent is justified

An agent may be justified when:

- the user cannot fully specify the task upfront,
- the task needs research and judgment,
- the environment changes between runs,
- multiple tools must be selected dynamically,
- the output requires synthesis rather than transformation,
- human approvals must be requested mid-flow,
- the system should learn reusable procedures over time.

## Required output before recommending an agent

Before choosing an agentic solution, produce:

```text
Non-Agent Alternative Review
- Simplest viable alternative:
- Why it may be enough:
- Where it fails:
- Why an agent is justified, if it is:
- Maintenance cost:
- Risk level:
- Kill criteria:
```

## Kill criteria

Do not proceed with an agent if:

- a deterministic script solves the task,
- the risk requires human judgment but no approval gate exists,
- success cannot be measured,
- tool permissions are too broad,
- maintenance ownership is unclear,
- failure would be silent or expensive,
- the user cannot name the target user or pain.

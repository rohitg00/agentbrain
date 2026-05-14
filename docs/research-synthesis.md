# Research Synthesis

Agent Brain v0.2.0 is based on a critique of current agent workflow patterns rather than blind adoption of any one system.

## What was studied

The research pass reviewed:

- public engineering skill packs,
- personal agent workflow skill libraries,
- markdown knowledge-base patterns,
- durable production agent runtimes,
- type-safe AI engineering stacks,
- minimal graph and shared-store abstractions,
- local portable skill systems,
- recent community discussion about agent reliability and maintenance.

## Repeated positive patterns

### Workflow beats advice

Good systems give the agent a next action, not a lecture.

Agent Brain response:

- every command produces an artifact,
- every skill includes verification,
- every state has exit criteria.

### Evidence beats confidence

Good systems require tests, traces, sources, screenshots, logs, or human approval.

Agent Brain response:

- artifact schemas include evidence fields,
- research produces claim ledgers,
- review gates require concrete proof.

### Persistent knowledge should be maintained, not merely retrieved

Good knowledge systems compile learning into durable pages and update them over time.

Agent Brain response:

- add wiki-style raw/source/synthesis/index/log concepts,
- require learning capture after repeated failures or wins.

### Production needs state and observability

Good agent systems are resumable, inspectable, and testable.

Agent Brain response:

- define a state machine,
- add eval cases,
- keep adapters separate from the portable core.

## Repeated failure modes

### Happy-path demos hide maintenance cost

Community criticism repeatedly points to agents that look impressive in demos but fail under maintenance, edge cases, or unclear ownership.

Agent Brain response:

- require maintenance owner and failure mode analysis.

### Users often ask for agents when they need systems

Many requests are better solved with forms, scripts, dashboards, or runbooks.

Agent Brain response:

- add `/brain-should-this-exist`,
- require non-agent alternative review.

### Skill libraries rot without evals

A large skill directory can become a brittle prompt pile.

Agent Brain response:

- add eval cases and rubrics,
- require skill verification and examples,
- maintain a roadmap/checklist.

### Agents overcomply

Agents often treat user direction as truth. That creates bad products faster.

Agent Brain response:

- define constructive disagreement as a requirement,
- add anti-rationalization tables.

### Recent community signal: workflows fail when work is unstructured

A current last-30-days pass across Reddit, X, YouTube, Hacker News, and GitHub found recurring complaints and advice around agent workflows: people get better results when they break work into small chunks, define the surrounding process, keep memory in durable plain files, and avoid overcomplicating simple automations into agents.

Agent Brain response:

- keep `/brain-plan` biased toward small verifiable slices,
- keep `/brain-should-this-exist` as a hard gate before building an agent,
- treat markdown artifacts as durable operating context rather than chat residue,
- make validators and evals part of the product, not afterthoughts.

### External framework signal: guardrails must sit at the right boundary

Recent agent SDK guidance separates input guardrails, output guardrails, tool guardrails, and human approval. A single final review is not enough when tools or handoffs can create side effects mid-run.

Agent Brain response:

- add a guardrail and approval review gate,
- distinguish automatic validation from human approval,
- prefer blocking checks before expensive or side-effecting work,
- test guardrail behavior directly.

### External skill-system signal: progressive disclosure matters

Modern agent skill systems emphasize metadata-first discovery, concise core instructions, and optional deeper files or scripts. This prevents large skill libraries from becoming context-window bloat.

Agent Brain response:

- require accurate skill frontmatter,
- keep `SKILL.md` focused on the core procedure,
- move long references, templates, scripts, and examples into linked resources when they grow.

## Design conclusion

Agent Brain must be more than a set of prompts. It should be a portable operating layer with:

- principles,
- state machine,
- commands,
- skills,
- artifacts,
- schemas,
- evals,
- adapters.

The highest-leverage differentiator is not better wording. It is the mandatory question:

> Should this exist, and should it be an agent?

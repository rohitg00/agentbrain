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

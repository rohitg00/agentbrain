# Architecture

Agent Brain is documentation-first, runtime-later.

## Layers

### 1. Constitution

`AGENTBRAIN.md` defines the behavior all agents should follow.

### 2. Commands

`commands/` defines slash-command entrypoints. Each command maps to one or more skills.

### 3. Skills

`skills/` contains portable workflows agents can load.

### 4. Templates

`templates/` standardizes artifacts: briefs, plans, reviews, QA reports, and skill definitions.

### 5. Memory

`docs/memory-model.md` defines what gets stored where.

### 7. Autonomous goals

`docs/autonomous-goals.md` defines how long-running `/goal`-style loops should be bounded, verified, and paused across runtimes.

### 8. Runtime adapters

Future adapters can install these skills into different agent runtimes without changing the core content.

## Data flow

```text
User request
  → command router
  → relevant skill(s)
  → optional autonomous goal loop
  → question ladder
  → artifact templates
  → review gates
  → implementation or handoff
  → learning capture
```

## Runtime stance

Agent Brain should not depend on a single autonomous loop or framework. Reliable agent products tend to be mostly deterministic software with LLM calls at high-leverage boundaries.

The portable core therefore favors:

- owned prompts and owned context instead of opaque framework defaults,
- explicit state and artifacts instead of hidden conversation state,
- launch / pause / resume points for long-running work,
- bounded `/goal`-style loops with explicit success evidence,
- explicit runtime lifecycle boundaries for turn snapshots, queued input, tool preflight, save points, retry, abort, and compaction,
- human contact and approval as first-class workflow actions,
- small focused skills or agents instead of one broad generalist,
- compact error summaries that can be fed back into the next attempt,
- runtime adapters that translate the same core into different execution environments.

## Design constraints

- Portable Markdown first
- No runtime-specific assumptions in core docs
- No secret handling in prompts
- No destructive writes without approval
- Explicit artifacts over hidden state
- Small skills over giant monoliths

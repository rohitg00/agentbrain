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

### 6. Runtime adapters

Future adapters can install these skills into different agent runtimes without changing the core content.

## Data flow

```text
User request
  → command router
  → relevant skill(s)
  → question ladder
  → artifact templates
  → review gates
  → implementation or handoff
  → learning capture
```

## Design constraints

- Portable Markdown first
- No runtime-specific assumptions in core docs
- No secret handling in prompts
- No destructive writes without approval
- Explicit artifacts over hidden state
- Small skills over giant monoliths

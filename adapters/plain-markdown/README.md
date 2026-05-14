# Plain Markdown Adapter

Use this adapter when the agent can read files but has no native skill system.

## Install

1. Copy or reference the repository root.
2. Tell the agent to read `AGENTBRAIN.md` first.
3. Route user requests through `commands/`.
4. Load only the relevant `skills/*/SKILL.md` files.
5. Use `templates/` for artifacts.
6. Run evals manually using `evals/rubrics/agent-brain-rubric.md`.

## Minimal instruction

```text
Before building, read AGENTBRAIN.md. Use commands/ to choose the right workflow. Produce the required artifact and do not skip evidence or non-agent alternative review.
```

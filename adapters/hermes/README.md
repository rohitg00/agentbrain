# Hermes Adapter

This adapter explains how to use Agent Brain with Hermes-style skills and tool access while keeping the core repo portable.

## Suggested setup

1. Keep Agent Brain as a project repository.
2. Let Hermes read `AGENTBRAIN.md` and relevant command specs.
3. Convert stable `skills/*/SKILL.md` files into local Hermes skills when they prove useful.
4. Use planning files for long-running work.
5. Use web/research tools for `/brain-research`.
6. Use file/git tools for `/brain-plan`, `/brain-build`, and `/brain-review`.
7. Use scheduled jobs only after the workflow is stable.

## Recommended Hermes flow

```text
/brain-start → /brain-should-this-exist → /brain-research → /brain-grill → /brain-plan → build/verify/review → /brain-learn
```

## Safety

Do not store credentials in Agent Brain files. Do not publish private project facts. Keep durable memory selective and use skills for reusable procedures.

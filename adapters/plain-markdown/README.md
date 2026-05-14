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

## Validation

Because this adapter has no native skill loader, validate both the repository and the manual routing behavior:

```bash
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

Then ask the agent to classify one sample request and confirm it cites the command file, skill file, artifact contract, evidence checked, and stop condition it used.

## Failure Modes

Stop and repair the setup when:

- the agent reads every file instead of the smallest relevant command and skills,
- the agent invents a command, skill, template, or schema that does not exist,
- the agent skips validation because the adapter is "just markdown",
- the handoff omits evidence checked, assumptions, risks, or next action.

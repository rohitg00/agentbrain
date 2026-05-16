# Plain Markdown Adapter

Use this adapter when the agent can read files but has no native skill system.

## Install

Before adapting the harness, run `git status --short` and `git log --oneline -5`, then run `git fetch origin main`, `git rev-parse HEAD`, and `git rev-parse origin/main`; confirm HEAD equals origin/main before trusting the checkout. Run baseline validation before editing, and preserve user changes before changing adapter instructions.

1. Copy or reference the repository root.
2. Tell the agent to read `AGENTBRAIN.md` first.
3. Route user requests through `commands/`.
4. Load only the relevant `skills/*/SKILL.md` files.
5. Use `templates/` for artifacts.
6. Run evals manually using `evals/rubrics/agent-brain-rubric.md`.

## Capability Matrix

Before the first real-runtime smoke, record whether the runtime can read files, write files, run shell commands, request approvals, reach the network, map `/brain-*` entries as native commands, emit template/schema-backed artifacts, and report blocked commands. Mark unknown capabilities as `unknown` instead of assuming support. Use yes, no, unknown, or blocked for each capability so later agents can compare runtime smoke runs without inferring support. Require an evidence source for each capability: observed command output, adapter docs, runtime settings, or `unknown` when unverified.

## Minimal instruction

```text
Use Agent Brain as the operating harness. Before building, read AGENTBRAIN.md, choose the matching command in commands/, load only the relevant files from skills/, produce the required artifact from templates/, check the matching contract in schemas/, and do not skip evidence, stop conditions, or non-agent alternative review. Treat /brain-* entries as markdown specs unless this runtime maps them to native commands; do not invent unsupported command routes.
```

## Validation

Because this adapter has no native skill loader, validate both the repository and the manual routing behavior:

```bash
python3 -m pip install -r requirements-dev.txt
rm -rf scripts/__pycache__ tests/__pycache__
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

Run a targeted exact-name scrub before public adapter copy changes so source
names, internal tools, or one-off branding do not leak into reusable harness
instructions.

Run `python scripts/runtime_smoke.py --runtime <neutral-runtime-name> --version <runtime-version> --selected-command /brain-start --loaded-skill intake --adapter-path <adapter-readme> --sandbox-write-mode <sandbox-write-mode> --brain-command-mode <brain-command-mode> --run-scope read_only_smoke --smoke-result <smoke-result> --command-exit-status <exit-status> --transcript-path <transcript-path> --transcript-redaction-status <redaction-status> --validation-command <validation-command>` for read-only smoke evidence, or use `--run-scope full_validation` only when the full local gate can run without runtime blockers.

Record every real-runtime smoke run with `templates/runtime-smoke.md` and validate
the JSON evidence against `schemas/runtime-smoke.schema.json` before trusting
adapter behavior. Keep the artifact honest about read-only smoke versus full
validation, blocked commands, command mode, sandbox/write mode, git freshness,
runtime version, Python executable, smoke result, command exit status, selected command, loaded skills, transcript path, and redacted transcript.

Then ask the agent to classify one sample request and confirm it cites the command file, skill file, artifact contract, evidence checked, and stop condition it used.

Promote read-only smoke to full validation only when write access, shell access, dependency install, and the full local gate are available; otherwise keep the result marked read-only smoke with blockers.

Before full validation writes, set a write fence that names allowed paths, disallowed paths, user-owned files, and rollback command.

## Output Contract

Runtime adapter output must report state, selected command, loaded skills, capability matrix, run scope, artifact path, transcript path, command exit status, template, schema, validation evidence, user change review, freshness, blockers, stop condition, and next action. If any field is unknown, say `unknown` with evidence instead of inferring capability.

## Failure Modes

Stop and repair the setup when:

- the agent reads every file instead of the smallest relevant command and skills,
- the agent invents a command, skill, template, or schema that does not exist,
- the runtime treats `/brain-*` as a native command without proof, uses unrestricted execution before approval, claims pytest passed when blocked by a read-only sandbox, or hides stderr instead of recording runtime evidence,
- the agent skips validation because the adapter is "just markdown",
- the handoff omits evidence checked, assumptions, risks, or next action.

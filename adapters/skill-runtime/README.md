# Skill Runtime Adapter

This adapter explains how to use Agent Brain with a tool-enabled skill runtime while keeping the core repo portable.

## Install

Before wiring a runtime, run `git status --short` and `git log --oneline -5`, then run `git fetch origin main`, `git rev-parse HEAD`, and `git rev-parse origin/main`; confirm HEAD equals origin/main before trusting the checkout. Run baseline validation before editing, and preserve user changes before changing adapter instructions.

1. Keep Agent Brain as a project repository.
2. Let the runtime read `AGENTBRAIN.md` and relevant command specs.
3. Convert stable `skills/*/SKILL.md` files into local runtime skills when they prove useful.
4. Use planning files for long-running work.
5. Use web/research tools for `/brain-research`.
6. Use file/git tools for `/brain-plan`, `/brain-build`, and `/brain-review`.
7. Use scheduled jobs only after the workflow is stable.

## Capability Matrix

Before the first real-runtime smoke, record whether the runtime can read files, write files, run shell commands, request approvals, reach the network, map `/brain-*` entries as native commands, emit template/schema-backed artifacts, and report blocked commands. Mark unknown capabilities as `unknown` instead of assuming support.

## Minimal instruction

```text
Use Agent Brain as the operating harness. Start with AGENTBRAIN.md, choose the matching command in commands/, load only the listed skills from skills/, produce the required artifact from templates/, check the matching contract in schemas/, and run the validation gate before claiming success. If evidence, approval, rollback, secrets handling, or loop limits are missing, stop with a blocker instead of improvising. Treat /brain-* entries as markdown specs unless this runtime maps them to native commands; do not invent unsupported command routes.
```

## Validation

After wiring the adapter into a workspace, run the same harness gate from the repository root:

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

After validation, classify one sample request and confirm the runtime cites the command file, skill file, artifact contract, evidence checked, and stop condition it used.

Promote read-only smoke to full validation only when write access, shell access, dependency install, and the full local gate are available; otherwise keep the result marked read-only smoke with blockers.

Then perform one dry run with a low-risk request and confirm the agent names the chosen command, loaded skills, evidence checked, stop conditions, and next action.

## Recommended skill-runtime flow

```text
/brain-start → /brain-should-this-exist → /brain-research → /brain-grill → /brain-plan → build/verify/review → /brain-learn
```

## Output Contract

Runtime adapter output must report state, selected command, loaded skills, capability matrix, run scope, artifact path, transcript path, command exit status, template, schema, validation evidence, freshness, blockers, stop condition, and next action. If any field is unknown, say `unknown` with evidence instead of inferring capability.

## Failure Modes

Stop and fix the adapter when:

- credentials or private project facts would be written into Agent Brain files,
- a scheduled job has no scope, loop limit, or stop condition,
- the runtime treats `/brain-*` as a native command without proof, uses unrestricted execution before approval, claims pytest passed when blocked by a read-only sandbox, or hides stderr instead of recording runtime evidence,
- a converted skill changes the original trigger, verification, or failure-mode contract,
- the agent reports success without the validation gate or dry-run evidence.

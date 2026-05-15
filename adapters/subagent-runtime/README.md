# Subagent Runtime Adapter

Use this adapter when validating Agent Brain inside a skill-enabled runtime that can read files, load skills, run terminal/file checks, and spawn subagents. The adapter should keep the harness evidence-first instead of turning the repo into private chat context.

## Install

Before wiring the subagent runtime to the harness, run `git status --short` and `git log --oneline -5`, then run `git fetch origin main`, `git rev-parse HEAD`, and `git rev-parse origin/main`; confirm HEAD equals origin/main before trusting the checkout. Run baseline validation before editing, and preserve user changes before changing adapter instructions.

1. Verify the runtime version and available toolsets.
2. Start with `AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.
3. Use `commands/` as the command catalog, not private memory.
4. Load matching `skills/*/SKILL.md` files or the runtime's skill loader when available.
5. Use subagents for read-only audits and independent reviews, but keep one writer for edits.
6. Return terminal-friendly handoffs with no platform-specific attachment markers.

## Capability Matrix

Before the first real-runtime smoke, record whether the runtime can read files, write files, run shell commands, request approvals, reach the network, map `/brain-*` entries as native commands, emit template/schema-backed artifacts, and report blocked commands. Mark unknown capabilities as `unknown` instead of assuming support.

## Minimal instruction

```text
Use Agent Brain as the operating harness. In a subagent-capable runtime, inspect AGENTBRAIN.md first, choose the matching command from commands/, load only the required skills from skills/, produce artifacts from templates/, check schemas/, and run real tool-backed validation before claiming success. Use subagents for independent read-only audits or review, but join their evidence and keep one writer for repo changes. Treat /brain-* entries as markdown specs unless this runtime maps them to native commands; do not invent unsupported command routes.
```

## Validation

For a normal writable checkout, run the same quality gate from the repository root:

```bash
python3 -m pip install -r requirements-dev.txt
rm -rf scripts/__pycache__ tests/__pycache__
python -m pytest -q
python scripts/validate_repo.py
git diff --check
```

Run a targeted exact-name scrub before public adapter copy changes so source
runtime names, internal tools, or one-off branding do not leak into reusable
harness instructions.

Run `python scripts/runtime_smoke.py --runtime <neutral-runtime-name> --version <runtime-version> --selected-command /brain-start --loaded-skill intake --adapter-path <adapter-readme> --sandbox-write-mode <sandbox-write-mode> --brain-command-mode <brain-command-mode> --run-scope read_only_smoke --smoke-result <smoke-result> --command-exit-status <exit-status> --transcript-path <transcript-path> --transcript-redaction-status <redaction-status> --validation-command <validation-command>` for read-only smoke evidence, or use `--run-scope full_validation` only when the full local gate can run without runtime blockers.

Record every real-runtime smoke run with `templates/runtime-smoke.md` and validate
the JSON evidence against `schemas/runtime-smoke.schema.json` before trusting
adapter behavior. Keep the artifact honest about read-only smoke versus full
validation, blocked commands, command mode, sandbox/write mode, git freshness,
runtime version, Python executable, smoke result, command exit status, selected command, loaded skills, transcript path, and redacted transcript.

After validation, classify one sample request and confirm the runtime cites the command file, skill file, artifact contract, evidence checked, and stop condition it used.

Promote read-only smoke to full validation only when write access, shell access, dependency install, and the full local gate are available; otherwise keep the result marked read-only smoke with blockers.

For a subagent runtime smoke test, also record the runtime version, the enabled toolsets used for inspection, whether subagents were read-only or write-capable, and the join review that accepted or rejected each subagent result.

## Output Contract

Runtime adapter output must report state, selected command, loaded skills, capability matrix, run scope, artifact path, transcript path, command exit status, template, schema, validation evidence, freshness, blockers, stop condition, and next action. If any field is unknown, say `unknown` with evidence instead of inferring capability.

## Failure Modes

Stop and fix the adapter when:

- the agent answers from memory instead of checking files and commands,
- subagent outputs are trusted without a join review and conflict check,
- multiple writers edit overlapping files in parallel,
- the runtime treats `/brain-*` as a native command without proof, uses unrestricted execution before approval, claims pytest passed when blocked by a read-only sandbox, or hides stderr instead of recording runtime evidence,
- the final response omits evidence checked, validation output, risks, or next action,
- the run reports messaging delivery details as repo validation proof.

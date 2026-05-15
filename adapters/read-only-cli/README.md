# Read Only Cli Adapter

Use this adapter when validating Agent Brain with any CLI-driven agent runtime that supports read-only and workspace-write sandbox modes. The runtime should treat Agent Brain as portable markdown plus files, not as native slash commands.

## Install

Before wiring the CLI runtime to the harness, run `git status --short` and `git log --oneline -5`, then run `git fetch origin main`, `git rev-parse HEAD`, and `git rev-parse origin/main`; confirm HEAD equals origin/main before trusting the checkout. Run baseline validation before editing, and preserve user changes before changing adapter instructions.

1. Verify the runtime version and noninteractive execution help.
2. Start with a read-only inspection pass before allowing workspace writes.
3. Tell the runtime that `/brain-*` names are markdown specs under `commands/`, not native slash commands.
4. Ask the runtime to cite the selected command file, skill files, template, schema, evidence, and stop condition.
5. Move to workspace-write mode only after the task has a plan, approval scope, and rollback path.

## Capability Matrix

Before the first real-runtime smoke, record whether the runtime can read files, write files, run shell commands, request approvals, reach the network, map `/brain-*` entries as native commands, emit template/schema-backed artifacts, and report blocked commands. Mark unknown capabilities as `unknown` instead of assuming support.

## Minimal instruction

```text
Use Agent Brain as the operating harness. Read AGENTBRAIN.md, route through commands/, load only the listed skills from skills/, produce artifacts from templates/, check schemas/, and remember that /brain-* entries are markdown command specs, not native runtime slash commands. Start in read-only mode, preserve git status, and stop before side effects without approval evidence. Treat /brain-* entries as markdown specs unless this runtime maps them to native commands; do not invent unsupported command routes.
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

Run `python scripts/runtime_smoke.py --runtime <neutral-runtime-name> --version <runtime-version> --selected-command /brain-start --loaded-skill intake --adapter-path <adapter-readme> --run-scope read_only_smoke` for read-only smoke evidence, or use `--run-scope full_validation` only when the full local gate can run without runtime blockers.

Record every real-runtime smoke run with `templates/runtime-smoke.md` and validate
the JSON evidence against `schemas/runtime-smoke.schema.json` before trusting
adapter behavior. Keep the artifact honest about read-only smoke versus full
validation, blocked commands, command mode, sandbox/write mode, git freshness,
runtime version, Python executable, smoke result, command exit status, selected command, loaded skills, and transcript path.

After validation, classify one sample request and confirm the runtime cites the command file, skill file, artifact contract, evidence checked, and stop condition it used.

Promote read-only smoke to full validation only when write access, shell access, dependency install, and the full local gate are available; otherwise keep the result marked read-only smoke with blockers.

For a read-only smoke test, do not fake the full gate. Record the blocked command and run only checks that do not require writes. If pytest cannot create a temporary directory, report that as a runtime blocker and continue with document routing checks, schema/template inspection, `git rev-parse HEAD`, `git rev-parse origin/main`, and `python scripts/validate_repo.py` only when Python 3.11 and dependencies are already available.

## Output Contract

Runtime adapter output must report state, selected command, loaded skills, capability matrix, run scope, artifact path, transcript path, command exit status, template, schema, validation evidence, freshness, blockers, stop condition, and next action. If any field is unknown, say `unknown` with evidence instead of inferring capability.

## Failure Modes

Stop and fix the adapter when:

- the runtime treats `/brain-start` or another `/brain-*` label as a native command instead of opening `commands/`,
- the run uses unrestricted execution before approval and rollback evidence exist,
- the output says tests passed when pytest was blocked by read-only sandboxing,
- the run relies on a preexisting `.venv` but claims fresh bootstrap proof,
- git or Python stderr noise is hidden instead of recorded as runtime evidence.

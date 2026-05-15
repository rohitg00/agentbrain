# Approval Gateway Runtime Adapter

Use this adapter when validating Agent Brain with any gateway-backed agent runtime that has explicit approval controls. The runtime should treat the repository as the operating harness and should not assume `/brain-*` entries are native commands unless a runtime binding explicitly adds them.

## Install

Before wiring the approval-gated runtime to the harness, run `git status --short` and `git log --oneline -5`, then run `git fetch origin main`, `git rev-parse HEAD`, and `git rev-parse origin/main`; confirm HEAD equals origin/main before trusting the checkout. Run baseline validation before editing, and preserve user changes before changing adapter instructions.

1. Verify the runtime version, agent invocation help, approval help, and skill help.
2. Start with a no-write smoke message that points at the Agent Brain repository path.
3. Tell the agent to read `AGENTBRAIN.md`, route through `commands/`, load `skills/`, produce artifacts from `templates/`, and check `schemas/`.
4. Check the runtime approval surface before any shell, file-write, publish, deploy, payment, or production side effect.
5. If Agent Brain skills are copied into runtime skills, preserve trigger, procedure, verification, output artifact, and failure-mode sections.

## Capability Matrix

Before the first real-runtime smoke, record whether the runtime can read files, write files, run shell commands, request approvals, reach the network, map `/brain-*` entries as native commands, emit template/schema-backed artifacts, and report blocked commands. Mark unknown capabilities as `unknown` instead of assuming support.

## Minimal instruction

```text
Use Agent Brain as the operating harness. In an approval-gated runtime, read AGENTBRAIN.md, choose the matching markdown spec from commands/, load only the relevant skills from skills/, produce the required artifact from templates/, check schemas/, and stop before side effects unless approval evidence is present. /brain-* labels are repo command specs, not native runtime commands by default. Treat /brain-* entries as markdown specs unless this runtime maps them to native commands; do not invent unsupported command routes.
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

For an approval-gated runtime smoke test, also record gateway/embedded fallback status, the selected agent id, approval settings checked, skill-loading strategy, and whether the run was read-only or allowed to write.

## Output Contract

Runtime adapter output must report state, selected command, loaded skills, capability matrix, run scope, artifact path, transcript path, command exit status, template, schema, validation evidence, freshness, blockers, stop condition, and next action. If any field is unknown, say `unknown` with evidence instead of inferring capability.

## Failure Modes

Stop and fix the adapter when:

- the runtime asks for a missing native harness backend instead of reading `commands/`,
- gateway protocol mismatch or embedded fallback hides the actual smoke result,
- approval settings are not checked before a side-effecting command,
- copied skills drift from the source markdown contract,
- the handoff omits runtime status, evidence checked, blockers, risks, or next action.

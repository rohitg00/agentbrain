#!/usr/bin/env python3
from pathlib import Path
import json
import re
import subprocess
import sys

from jsonschema import validators

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ROOT = [
    "README.md",
    "AGENTBRAIN.md",
    "PRINCIPLES.md",
    "ANTI_RATIONALIZATION.md",
    "CONTRIBUTING.md",
]
REQUIRED_FILES = [
    "requirements-dev.txt",
    "scripts/scrub_public_copy.py",
    "scripts/runtime_smoke.py",
    "commands/README.md",
    "skills/README.md",
]
REQUIRED_DEV_REQUIREMENTS = ["jsonschema", "pytest"]
REQUIRED_DIRECTORIES = ["schemas"]
REQUIRED_ARTIFACT_FILES = [
    "schemas/eval-report.schema.json",
    "schemas/handoff-report.schema.json",
    "schemas/memory-decision.schema.json",
    "templates/eval-report.md",
    "templates/handoff-report.md",
    "templates/memory-decision.md",
    "templates/qa-evidence.md",
    "schemas/runtime-smoke.schema.json",
    "templates/runtime-smoke.md",
]
REQUIRED_STATE_MACHINE_VALUES = [
    "INTAKE",
    "RESEARCH",
    "CHALLENGE",
    "DECIDE",
    "DESIGN",
    "PLAN",
    "BUILD",
    "VERIFY",
    "REVIEW",
    "SHIP",
    "LEARN",
]
REQUIRED_GITIGNORE_PATTERNS = ["__pycache__/", "*.py[cod]", ".pytest_cache/", ".venv/"]
REQUIRED_DOCS = [
    "docs/agent-harness.md",
    "docs/autonomous-goals.md",
    "docs/devex-engineering.md",
    "docs/shared-language.md",
    "docs/decision-records.md",
    "docs/ci-recovery.md",
    "docs/skill-distillation.md",
    "docs/state-machine.md",
]
REQUIRED_STATE_MACHINE_DOC_STATES = [
    "raw_request",
    "intake",
    "should_this_exist",
    "research",
    "grill",
    "brief",
    "design",
    "plan",
    "build",
    "verify",
    "review",
    "ship",
    "learn",
    "archive",
]
REQUIRED_SKILLS = [
    "skills/activity-recap/SKILL.md",
    "skills/agent-output-verifier/SKILL.md",
    "skills/context-memory/SKILL.md",
    "skills/domain-language/SKILL.md",
    "skills/ci-recovery/SKILL.md",
    "skills/runtime-smoke/SKILL.md",
]
REQUIRED_EVAL_CASES = [
    "evals/cases/activity-recap.md",
    "evals/cases/artifact-contract-drift.md",
    "evals/cases/source-to-skill-distillation.md",
    "evals/cases/agent-output-verifier.md",
    "evals/cases/dirty-working-tree-preservation.md",
    "evals/cases/memory-capture-routing.md",
    "evals/cases/domain-language-drift.md",
    "evals/cases/ci-failure-triage.md",
    "evals/cases/verification-shortcut.md",
    "evals/cases/skill-boundary-creep.md",
    "evals/cases/source-branded-skill-name.md",
    "evals/cases/no-user-defined.md",
    "evals/cases/review-gate-skip.md",
    "evals/cases/plan-slicing.md",
    "evals/cases/context-drift.md",
    "evals/cases/spec-before-build.md",
    "evals/cases/test-first-implementation.md",
    "evals/cases/horizontal-slicing.md",
    "evals/cases/ship-without-rollback.md",
    "evals/cases/security-risk-feature.md",
    "evals/cases/unapproved-side-effect.md",
    "evals/cases/interrupted-handoff-resume.md",
    "evals/cases/stale-validation-proof.md",
    "evals/cases/parallel-worker-join.md",
    "evals/cases/context-budget.md",
    "evals/cases/source-specific-command-leakage.md",
    "evals/cases/real-runtime-smoke-test.md",
    "evals/cases/native-command-assumption.md",
]
REQUIRED_EVAL_DOCS = ["evals/README.md"]
REQUIRED_REAL_RUNTIME_SMOKE_EVIDENCE_FIELDS = [
    "runtime",
    "version",
    "python executable",
    "writable temp-dir status",
    "git freshness result",
    "exact command",
    "command exit status",
    "smoke result",
    "transcript path",
    "sandbox/write mode",
    "/brain-* native commands or markdown specs",
    "selected command",
    "loaded skills",
    "adapter path",
    "blocked commands",
]
REQUIRED_REAL_RUNTIME_SMOKE_READ_ONLY_TERMS = ["read-only", "full validation"]
REQUIRED_WORKFLOWS = [".github/workflows/quality.yml"]
REQUIRED_QUALITY_WORKFLOW_RUNS = [
    "python -m pip install -r requirements-dev.txt",
    "rm -rf scripts/__pycache__ tests/__pycache__",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
]
REQUIRED_WORKFLOW_TRIGGERS = ["push", "pull_request"]
REQUIRED_README_VALIDATION_COMMANDS = [
    "pip install -r requirements-dev.txt",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
]
REQUIRED_README_VALIDATION_GATE_TERMS = {
    "rm -rf scripts/__pycache__ tests/__pycache__": "README.md validation gate must include cache cleanup before tests",
    "targeted exact-name scrub": "README.md validation gate must include targeted exact-name scrub",
}
REQUIRED_README_QUICKSTART_COMMANDS = [
    "python3 -m venv .venv",
    "source .venv/bin/activate",
    "python3 -m pip install -r requirements-dev.txt",
    "rm -rf scripts/__pycache__ tests/__pycache__",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
    "python scripts/scrub_public_copy.py",
]
REQUIRED_README_QUICKSTART_TERMS = {
    "targeted exact-name scrub": "README.md Quickstart must include targeted exact-name scrub",
    "case-insensitive": "README.md Quickstart must document that targeted exact-name scrub is case-insensitive",
    "at least one exact source name": "README.md Quickstart must document that targeted exact-name scrub requires at least one exact source name",
    "Python 3.11": "README.md Quickstart must document CI Python version: Python 3.11",
    "baseline validation before editing": "README.md Quickstart must require baseline validation before editing",
}
REQUIRED_README_REMOTE_FRESHNESS_TERMS = [
    "git fetch origin main",
    "git rev-parse HEAD",
    "git rev-parse origin/main",
    "HEAD equals origin/main",
]
REQUIRED_README_HARNESS_SECTIONS = [
    "## Quickstart",
    "## Run as an Agent Harness",
    "## Minimal Harness Prompt",
    "## Command Selection Guide",
    "## Handoff Contract",
    "## Evidence Freshness Rules",
    "## Edge Cases and Stop Conditions",
    "## Troubleshooting",
    "## Weakest Failure Mode Audit",
    "## Maintainer Checklist",
]
REQUIRED_README_EVIDENCE_FRESHNESS_TERMS = [
    "command",
    "result",
    "date or commit",
    "artifact checked",
    "source provenance",
    "recheck trigger",
    "expiry",
    "stale validation proof",
    "code",
    "docs",
    "schemas",
    "templates",
    "commands",
    "skills",
    "evals",
    "CI",
    "dependencies",
]
REQUIRED_README_MINIMAL_HARNESS_PROMPT_TERMS = [
    "AGENTBRAIN.md",
    "PRINCIPLES.md",
    "ANTI_RATIONALIZATION.md",
    "docs/state-machine.md",
    "git status --short",
    "git log --oneline -5",
    "baseline validation",
    "rm -rf scripts/__pycache__ tests/__pycache__",
    "Preserve user changes",
    "commands/",
    "skills/",
    "templates/",
    "schemas/",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
    "targeted exact-name scrub",
    "stop",
    "approval",
    "secrets",
    "loop limits",
    "noninteractive",
    "scheduled run",
    "do not ask questions",
]
REQUIRED_README_REPOSITORY_MAP_PATHS = [
    "requirements-dev.txt",
    ".github/workflows/",
]
REQUIRED_README_TROUBLESHOOTING_TERMS = [
    "dirty working tree",
    "git status --short",
    "preserve user changes",
]
REQUIRED_README_SECRET_TROUBLESHOOTING_TERMS = ["secret-like values"]
REQUIRED_README_CI_TROUBLESHOOTING_TERMS = [
    "Tests pass locally but CI fails",
    "exact CI sequence locally",
    "rm -rf scripts/__pycache__ tests/__pycache__",
    ".github/workflows/quality.yml",
]
REQUIRED_README_DEPENDENCY_TROUBLESHOOTING_TERMS = [
    "ModuleNotFoundError",
    "virtual environment",
    "Python 3.11",
    "python3 -m pip install -r requirements-dev.txt",
]
REQUIRED_README_GENERATED_CACHE_TROUBLESHOOTING_TERMS = ["generated Python cache file"]
REQUIRED_README_ARTIFACT_TROUBLESHOOTING_TERMS = ["schema/template mismatch"]
REQUIRED_README_EDGE_CASE_APPROVAL_TERMS = ["approval", "side effect"]
REQUIRED_README_MAINTAINER_LOOP_TERMS = [
    "rm -rf scripts/__pycache__ tests/__pycache__",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
    "targeted exact-name scrub",
    "git push",
    "git fetch origin main",
    "HEAD equals origin/main",
]
REQUIRED_README_HANDOFF_TERMS = [
    "decision",
    "evidence checked",
    "fresh validation proof",
    "facts",
    "assumptions",
    "open questions",
    "risks",
    "next action",
]
REQUIRED_README_HANDOFF_RESUME_TERMS = [
    "previous handoff",
    "stale",
    "resume only the named next action",
]
REQUIRED_README_COMMAND_SELECTION_FALLBACK_TERMS = [
    "If no command fits",
    "do not invent",
    "stop",
]
REQUIRED_README_COMMAND_SELECTION_ARTIFACT_TERMS = [
    "output artifact",
    "template",
    "command output contract",
]
REQUIRED_HANDOFF_SCHEMA_RESUME_FIELDS = [
    "facts",
    "assumptions",
    "open_questions",
    "risks",
]
REQUIRED_HANDOFF_SCHEMA_BLOCKED_RESUME_FIELDS = ["stop_conditions"]
REQUIRED_SKILL_SCHEMA_FIELDS = [
    "lifecycle_stage",
    "output_artifact",
]
REQUIRED_SKILL_SCHEMA_NONEMPTY_ARRAY_FIELDS = [
    "inputs",
    "procedure",
    "verification",
    "failure_modes",
    "examples",
]
STALE_STATUS_COMPLETION_TERMS = [
    "complete",
    "done",
    "finished",
    "no more hardening",
]
STALE_REPOSITORY_BOOTSTRAP_TERMS = [
    "approve creating the github repository",
    "push the docs-only",
    "open issues for installer",
]
REQUIRED_CONSTITUTION_NONINTERACTIVE_TERMS = [
    "noninteractive",
    "scheduled run",
    "cannot ask questions",
    "safest documented default",
    "stop with a blocker",
]
REQUIRED_CONSTITUTION_DONE_DEFINITION_TERMS = [
    "fresh validation proof",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
    "targeted exact-name scrub",
]
REQUIRED_CONSTITUTION_PUBLIC_COPY_TERMS = [
    "external sources",
    "neutral operator pattern",
    "public copy neutral",
    "targeted exact-name scrub",
]
REQUIRED_AGENT_HARNESS_SECTIONS = [
    "## Install",
    "## Fresh Checkout Bootstrap",
    "## Operating Loop",
    "## Command Routing",
    "## Handoff Contract",
    "## Stop Conditions",
    "## Edge Cases",
    "## Troubleshooting",
]
REQUIRED_AGENT_HARNESS_VALIDATION_COMMANDS = [
    "python3 -m venv .venv",
    "source .venv/bin/activate",
    "pip install -r requirements-dev.txt",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
    "python scripts/scrub_public_copy.py",
]
REQUIRED_AGENT_HARNESS_VALIDATION_GATE_TERMS = {
    "rm -rf scripts/__pycache__ tests/__pycache__": "docs/agent-harness.md validation gate must include cache cleanup before tests",
    "targeted exact-name scrub": "docs/agent-harness.md validation gate must include targeted exact-name scrub",
}
REQUIRED_AGENT_HARNESS_PROMPT_SECTION = "## Copyable Harness Prompt"
REQUIRED_AGENT_HARNESS_PROMPT_TERMS = [
    "AGENTBRAIN.md",
    "PRINCIPLES.md",
    "ANTI_RATIONALIZATION.md",
    "docs/state-machine.md",
    "git status --short",
    "git log --oneline -5",
    "baseline validation",
    "Preserve user changes",
    "commands/",
    "skills",
    "templates/",
    "schemas/",
    "rm -rf scripts/__pycache__ tests/__pycache__",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
    "targeted exact-name scrub",
    "Stop",
    "approval",
    "secrets",
    "loop limits",
]
REQUIRED_AGENT_HARNESS_WORKER_ROLES = [
    "researcher",
    "planner",
    "builder",
    "verifier",
    "reviewer",
    "shipper",
    "learner",
]
REQUIRED_AGENT_HARNESS_WORKER_CONTRACT_TERMS = {
    "evidence": "docs/agent-harness.md worker guidance must require evidence",
    "stop condition": "docs/agent-harness.md worker guidance must require stop conditions",
    "handoff": "docs/agent-harness.md worker guidance must require handoff contracts",
    "coordinator": "docs/agent-harness.md worker guidance must require coordinator join review",
    "worker scope": "docs/agent-harness.md worker guidance must require worker scope mapping",
    "single writer": "docs/agent-harness.md worker guidance must require a single writer for parallel work",
    "accepted outputs": "docs/agent-harness.md worker guidance must require accepted output review",
    "rejected outputs": "docs/agent-harness.md worker guidance must require rejected output review",
    "conflict check": "docs/agent-harness.md worker guidance must require conflict checks",
}
REQUIRED_AGENT_HARNESS_RESUME_TERMS = [
    "previous handoff",
    "stale",
    "resume only the named next action",
]
REQUIRED_AGENT_HARNESS_FRESH_CHECKOUT_TERMS = [
    "git fetch origin main",
    "git rev-parse HEAD",
    "git rev-parse origin/main",
    "HEAD equals origin/main",
]
REQUIRED_AGENT_HARNESS_NONINTERACTIVE_TERMS = [
    "noninteractive",
    "scheduled run",
    "cannot ask questions",
]
REQUIRED_AGENT_HARNESS_HANDOFF_TERMS = ["fresh validation proof", "coordination review"]
REQUIRED_AGENT_HARNESS_TROUBLESHOOTING_TERMS = {
    "dirty working tree": "docs/agent-harness.md troubleshooting must document dirty working tree recovery",
    "git status --short": "docs/agent-harness.md troubleshooting must document dirty working tree recovery",
    "preserve user changes": "docs/agent-harness.md troubleshooting must document dirty working tree recovery",
    "secret-like values": "docs/agent-harness.md troubleshooting must document secret-like value recovery",
    "Tests pass locally but CI fails": "docs/agent-harness.md troubleshooting must document CI failure recovery",
    "exact CI sequence locally": "docs/agent-harness.md troubleshooting must document CI failure recovery",
    ".github/workflows/quality.yml": "docs/agent-harness.md troubleshooting must document CI failure recovery",
    "ModuleNotFoundError": "docs/agent-harness.md troubleshooting must document dependency bootstrap recovery",
    "virtual environment": "docs/agent-harness.md troubleshooting must document dependency bootstrap recovery",
    "generated Python cache file": "docs/agent-harness.md troubleshooting must document generated cache recovery",
    "schema/template mismatch": "docs/agent-harness.md troubleshooting must document schema/template mismatch recovery",
}
REQUIRED_AGENT_HARNESS_EVAL_TROUBLESHOOTING_TERMS = [
    "eval case",
    "User request",
    "Expected behavior",
    "Harness route",
    "Failure if",
]
REQUIRED_AGENT_HARNESS_MAINTAINER_TERMS = [
    "git push",
    "git fetch origin main",
    "HEAD equals origin/main",
]
REQUIRED_ADAPTER_SECTIONS = [
    "## Install",
    "## Capability Matrix",
    "## Minimal instruction",
    "## Validation",
    "## Output Contract",
    "## Failure Modes",
]
REQUIRED_ADAPTER_OUTPUT_CONTRACT_TERMS = [
    "state",
    "selected command",
    "loaded skills",
    "artifact path",
    "template",
    "schema",
    "validation evidence",
    "freshness",
    "blockers",
    "stop condition",
    "next action",
]
REQUIRED_ADAPTER_CAPABILITY_MATRIX_TERMS = [
    "read files",
    "write files",
    "run shell commands",
    "request approvals",
    "reach the network",
    "native commands",
    "emit",
    "blocked commands",
    "unknown",
]
REQUIRED_ADAPTER_VALIDATION_COMMANDS = [
    "python3 -m pip install -r requirements-dev.txt",
    "rm -rf scripts/__pycache__ tests/__pycache__",
    "python -m pytest -q",
    "python scripts/validate_repo.py",
    "git diff --check",
    "python scripts/runtime_smoke.py",
    "targeted exact-name scrub",
]
REQUIRED_ADAPTER_BOOTSTRAP_COMMANDS = [
    "git status --short",
    "git log --oneline -5",
    "baseline validation before editing",
    "preserve user changes",
]
REQUIRED_ADAPTER_REMOTE_FRESHNESS_TERMS = [
    "git fetch origin main",
    "git rev-parse HEAD",
    "git rev-parse origin/main",
    "HEAD equals origin/main",
]
REQUIRED_ADAPTER_MINIMAL_INSTRUCTION_ARTIFACTS = [
    "AGENTBRAIN.md",
    "commands/",
    "skills/",
    "templates/",
    "schemas/",
]
REQUIRED_ADAPTER_COMMAND_BOUNDARY_TERMS = [
    "markdown specs",
    "native commands",
    "do not invent",
]
REQUIRED_ADAPTER_RUNTIME_SMOKE_ARTIFACT_TERMS = [
    "templates/runtime-smoke.md",
    "schemas/runtime-smoke.schema.json",
]
REQUIRED_ADAPTER_RUNTIME_SMOKE_EVIDENCE_TERMS = [
    "blocked commands",
    "command mode",
    "sandbox/write mode",
    "git freshness",
    "runtime version",
    "python executable",
    "smoke result",
    "command exit status",
    "selected command",
    "loaded skills",
    "transcript path",
]
REQUIRED_ADAPTER_SAMPLE_ROUTING_PROBE_TERMS = [
    "sample request",
    "command file",
    "skill file",
    "artifact contract",
    "evidence checked",
    "stop condition",
]
REQUIRED_CONTRIBUTING_VALIDATION_COMMANDS = [
    "pytest -q",
    "rm -rf scripts/__pycache__ tests/__pycache__",
    "git diff --check",
    "targeted exact-name scrub",
]
RESEARCH_WATCHLIST_REQUIRED_SOURCES = [
    "autonomous-goal runtime docs",
    "service-layer skill pattern",
    "small composable engineering skills",
    "methodology skill library",
    "harness integration skill library",
]
REQUIRED_SKILL_SECTIONS = [
    "## Trigger",
    "## When not to use",
    "## Inputs",
    "## Procedure",
    "## Anti-Rationalization",
    "## Verification",
    "## Output Artifact",
    "## Failure Modes",
    "## Example",
]
REQUIRED_SKILL_TEMPLATE_SECTIONS = [
    "## Trigger",
    "## When not to use",
    "## Inputs",
    "## Procedure",
    "## Anti-Rationalization",
    "## Verification",
    "## Output Artifact",
    "## Failure Modes",
    "## Example",
]
REQUIRED_SKILLS_README_QUALITY_BAR_TERMS = [
    "description starts with a precise use when trigger",
    "procedure names concrete steps",
    "verification is runnable or inspectable",
    "output artifact is explicit",
    "failure modes and stop conditions",
    "at least one command loads the skill",
]
REQUIRED_PLAN_SLICING_TERMS = {
    "acceptance checks": "skills/plan-slicing/SKILL.md must require each slice to name acceptance checks",
    "verification command": "skills/plan-slicing/SKILL.md must require each slice to name a verification command",
}
REQUIRED_COMMAND_SECTIONS = [
    "## Purpose",
    "## When to use",
    "## Input contract",
    "## Skills to load",
    "## Workflow",
    "## Output",
    "## Stop conditions",
    "## Quality bar",
    "## Example",
]
REQUIRED_COMMAND_OUTPUT_TERMS = [
    "decision",
    "evidence",
    "fresh validation proof",
    "assumptions",
    "risks",
    "open questions",
    "next recommended state",
]
REQUIRED_COMMAND_INPUT_CONTRACT_TERMS = [
    "known facts",
    "assumptions",
    "constraints",
    "evidence",
    "approval state",
]
REQUIRED_COMMAND_QUALITY_BAR_TERMS = ["fresh validation proof"]
REQUIRED_COMMAND_EXAMPLE_TERMS = [
    "user request",
    "selected command",
    "loaded skills",
    "artifact",
    "verification",
]
REQUIRED_COMMAND_CATALOG_CONTRACT_TERMS = [
    "lifecycle state",
    "required artifact",
    "skills to load",
    "native command support",
    "markdown spec",
    "stop condition",
]
REQUIRED_BUILD_COMMAND_PROOF_TERMS = [
    "failing test before implementation",
    "validator-first proof",
]
REQUIRED_BUILD_COMMAND_RED_REFACTOR_TERMS = [
    "do not refactor while red",
    "never refactor while red",
]
REQUIRED_START_COMMAND_REPO_INSPECTION_TERMS = [
    "git status --short",
    "git log --oneline -5",
    "baseline validation",
]
COMMAND_ASK_USER_TERMS = [
    "ask at most",
    "ask for human input",
    "ask the user",
]
COMMAND_NONINTERACTIVE_FALLBACK_TERMS = [
    "noninteractive",
    "cannot ask questions",
    "safest documented default",
    "blocker",
]
VALID_COMMAND_LIFECYCLE_STATES = set(REQUIRED_STATE_MACHINE_VALUES)
REQUIRED_EVAL_CASE_SECTIONS = [
    "## User request",
    "## Expected behavior",
    "## Harness route",
    "## Failure if",
]
REQUIRED_EVAL_RUBRIC_SECTIONS = ["## Dimensions", "## Interpretation"]
REQUIRED_EVALS_README_RUN_CONTRACT_TERMS = [
    "case",
    "target command or skill",
    "existing command or skill route",
    "rubric",
    "evidence",
    "pass/fail decision",
    "fresh validation proof",
]
BANNED_PUBLIC_COPY_TERMS = [
    "G" + "arry",
    "G" + "Brain",
    "G" + "Stack",
    "Matt" + "Pocock",
    "Her" + "mes",
    "Open" + "Claw",
    "Clau" + "de",
    "Co" + "dex",
    "Open" + "AI",
    "Anth" + "ropic",
]
SECRET_LIKE_PATTERNS = [
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("private key block", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")),
    ("cloud access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    (
        "connection string with embedded credential",
        re.compile(
            r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqps?)://"
            r"[^:\s/@]+:[^@\s/]+@",
            re.IGNORECASE,
        ),
    ),
    (
        "generic credential assignment",
        re.compile(
            r"\b(?:api[_-]?(?:key|token)|secret|token|password|passwd|pwd|client[_-]?secret)"
            r"\s*[:=]\s*['\"]?(?!<redacted>|\[redacted\]|redacted|placeholder|example)"
            r"[A-Za-z0-9_./+=:-]{16,}",
            re.IGNORECASE,
        ),
    ),
]
PUBLIC_COPY_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
PUBLIC_COPY_EXCLUDED_PARTS = {
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "venv",
}
GENERATED_CACHE_PARTS = {"__pycache__", ".pytest_cache"}
GENERATED_CACHE_SUFFIXES = {".pyc", ".pyo"}
LOWERCASE_KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def has_delimited_frontmatter(text: str) -> bool:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return False
    for line in lines[1:]:
        if line == "---":
            return True
        if line.startswith("# "):
            return False
    return False


def parse_frontmatter(text: str) -> dict[str, str]:
    if not has_delimited_frontmatter(text):
        return {}

    frontmatter = text.split("---", 2)[1]

    parsed: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip().strip('"\'')
    return parsed


def markdown_h1_headings(text: str) -> list[str]:
    headings: list[str] = []
    in_fenced_code = False
    for line in text.splitlines():
        if line.startswith("```") or line.startswith("~~~"):
            in_fenced_code = not in_fenced_code
            continue
        if not in_fenced_code and line.startswith("# "):
            headings.append(line)
    return headings


def term_is_only_in_readme_comparison_section(text: str, term: str) -> bool:
    term_lower = term.lower()
    if term_lower not in text.lower():
        return True

    in_allowed_section = False
    for line in text.splitlines():
        if line.startswith("## "):
            heading = line.lower().strip("# ")
            in_allowed_section = heading in {"vs others", "benchmarks", "comparisons"}
        if term_lower in line.lower() and not in_allowed_section:
            return False
    return True


def public_copy_term_allowed(path: Path, text: str, term: str) -> bool:
    return path.name == "README.md" and term_is_only_in_readme_comparison_section(text, term)


def find_trailing_whitespace_lines(text: str) -> list[int]:
    return [
        line_number
        for line_number, line in enumerate(text.splitlines(), 1)
        if line.endswith((" ", "\t"))
    ]


def reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    parsed: dict[str, object] = {}
    for key, value in pairs:
        if key in parsed:
            raise ValueError(f"duplicate key: {key}")
        parsed[key] = value
    return parsed


def title_from_slug(slug: str) -> str:
    if slug.startswith("non-agent-"):
        return f"Non-Agent {title_from_slug(slug.removeprefix('non-agent-'))}"
    connector_words = {"and", "or", "the", "to", "vs"}
    parts = slug.split("-")
    titled_parts = [part if part in connector_words else part.capitalize() for part in parts]
    return " ".join(titled_parts)


def artifact_title_from_slug(slug: str) -> str:
    acronym_words = {"qa": "QA", "ci": "CI"}
    return " ".join(acronym_words.get(part, part.capitalize()) for part in slug.split("-"))


def adapter_heading_from_slug(slug: str) -> str:
    title = title_from_slug(slug)
    if title.endswith(" Adapter"):
        return f"# {title}"
    return f"# {title} Adapter"


def validate_single_h1(path: Path, root: Path) -> str | None:
    text = path.read_text(errors="ignore")
    h1_headings = markdown_h1_headings(text)
    if len(h1_headings) != 1:
        return f"{rel(path, root)} must contain exactly one H1 heading"
    return None


def is_lowercase_kebab(value: str) -> bool:
    return bool(LOWERCASE_KEBAB_RE.fullmatch(value))


def section_has_body(text: str, section: str) -> bool:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line != section:
            continue
        body_lines = []
        for following_line in lines[index + 1 :]:
            if following_line.startswith("## "):
                break
            body_lines.append(following_line)
        return bool("\n".join(body_lines).strip())
    return False


def section_body(text: str, section: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line != section:
            continue
        body_lines = []
        for following_line in lines[index + 1 :]:
            if following_line.startswith("## "):
                break
            body_lines.append(following_line)
        return "\n".join(body_lines)
    return ""


def sections_are_in_order(text: str, sections: list[str]) -> bool:
    lines = text.splitlines()
    positions = [lines.index(section) for section in sections if section in lines]
    return positions == sorted(positions)


def requirement_name(line: str) -> str:
    requirement = line.strip()
    if not requirement or requirement.startswith("#"):
        return ""
    return re.split(r"\s*(?:[<>=!~]=|==|>|<|~=|\[)", requirement, maxsplit=1)[0].lower()


def find_missing_dev_requirements(text: str) -> list[str]:
    installed = {requirement_name(line) for line in text.splitlines()}
    return [requirement for requirement in REQUIRED_DEV_REQUIREMENTS if requirement not in installed]


def tracked_git_files(root: Path) -> set[str] | None:
    if not (root / ".git").exists():
        return None
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return set(result.stdout.splitlines())


def workflow_declares_trigger(workflow_text: str, trigger: str) -> bool:
    workflow_lines = [line.strip() for line in workflow_text.splitlines()]
    if f"{trigger}:" in workflow_lines or f"on: {trigger}" in workflow_lines:
        return True
    for line in workflow_lines:
        if not line.startswith("on: [") or not line.endswith("]"):
            continue
        inline_triggers = [item.strip() for item in line.removeprefix("on: [").removesuffix("]").split(",")]
        if trigger in inline_triggers:
            return True

    in_on_block = False
    for raw_line in workflow_text.splitlines():
        if raw_line == "on:":
            in_on_block = True
            continue
        if in_on_block and raw_line and not raw_line.startswith((" ", "\t")):
            break
        if in_on_block and raw_line.strip() == f"- {trigger}":
            return True
    return False


def workflow_sets_readonly_contents_permission(workflow_text: str) -> bool:
    permissions_block_indent: int | None = None
    for raw_line in workflow_text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        line_indent = len(raw_line) - len(raw_line.lstrip(" \t"))
        if stripped == "permissions: read-all":
            return True
        if permissions_block_indent is not None and line_indent <= permissions_block_indent:
            permissions_block_indent = None
        if stripped == "permissions:":
            permissions_block_indent = line_indent
            continue
        if permissions_block_indent is None or ":" not in stripped:
            continue
        permission, access = [part.strip() for part in stripped.split(":", 1)]
        if permission == "contents" and access == "read":
            return True
    return False


def find_write_workflow_permissions(workflow_text: str) -> list[str]:
    write_permissions: list[str] = []
    permissions_block_indent: int | None = None
    for raw_line in workflow_text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        line_indent = len(raw_line) - len(raw_line.lstrip(" \t"))
        if stripped == "permissions: write-all":
            write_permissions.append("write-all")
            permissions_block_indent = None
            continue
        if permissions_block_indent is not None and line_indent <= permissions_block_indent:
            permissions_block_indent = None
        if stripped == "permissions:":
            permissions_block_indent = line_indent
            continue
        if permissions_block_indent is None or ":" not in stripped:
            continue
        permission, access = [part.strip() for part in stripped.split(":", 1)]
        if access == "write":
            write_permissions.append(permission)
    return write_permissions


def find_object_schemas_without_closed_properties(schema: object) -> list[str]:
    missing_locations: list[str] = []

    def walk(node: object, location: str) -> None:
        if isinstance(node, dict):
            if node.get("type") == "object" and node.get("additionalProperties") is not False:
                missing_locations.append(location)
            for key, value in node.items():
                if key == "properties" and isinstance(value, dict):
                    for property_name, property_schema in value.items():
                        walk(property_schema, f"{location}.properties.{property_name}")
                elif key == "items":
                    walk(value, f"{location}.items")
                elif key in {"anyOf", "allOf", "oneOf"} and isinstance(value, list):
                    for index, option in enumerate(value):
                        walk(option, f"{location}.{key}[{index}]")
                elif key in {"$defs", "definitions"} and isinstance(value, dict):
                    for definition_name, definition_schema in value.items():
                        walk(definition_schema, f"{location}.{key}.{definition_name}")
                elif key == "not":
                    walk(value, f"{location}.not")
        elif isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{location}[{index}]")

    walk(schema, "$")
    return missing_locations


def readme_repository_map_paths(text: str) -> list[str]:
    lines = text.splitlines()
    paths: list[str] = []
    in_repository_map = False
    in_code_fence = False

    for line in lines:
        if line == "## Repository Map":
            in_repository_map = True
            continue
        if in_repository_map and line.startswith("## "):
            break
        if not in_repository_map:
            continue
        if line.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if not in_code_fence:
            continue

        candidate = line.split("#", 1)[0].strip()
        if not candidate:
            continue
        if candidate.endswith("/") or "." in Path(candidate).name:
            paths.append(candidate)

    return paths


def readme_command_references(text: str) -> list[str]:
    entries: set[str] = set()
    in_core_commands = False
    for line in text.splitlines():
        if line == "## Core Commands":
            in_core_commands = True
            continue
        if in_core_commands and line.startswith("## "):
            break
        if not in_core_commands:
            continue
        match = re.match(r"- (?:`(/brain-[a-z0-9-]+)`|\[`(/brain-[a-z0-9-]+)`\]\(commands/[a-z0-9-]+\.md\))", line)
        if match:
            entries.add(next(group for group in match.groups() if group))
    return sorted(entries)


def readme_command_catalog_links(text: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    in_core_commands = False
    for line in text.splitlines():
        if line == "## Core Commands":
            in_core_commands = True
            continue
        if in_core_commands and line.startswith("## "):
            break
        if not in_core_commands:
            continue
        match = re.match(r"- \[`(/brain-[a-z0-9-]+)`\]\((commands/[a-z0-9-]+\.md)\)", line)
        if match:
            entries[match.group(1)] = match.group(2)
    return entries


def command_catalog_entry_lines(text: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    in_commands = False
    for line in text.splitlines():
        if line == "## Commands":
            in_commands = True
            continue
        if in_commands and line.startswith("## "):
            break
        if not in_commands:
            continue
        match = re.match(r"- \[`(/brain-[a-z0-9-]+)`\]\([^)]+\) — (.+)$", line)
        if match:
            entries[match.group(1)] = match.group(2)
    return entries


def readme_command_selection_references(text: str) -> list[str]:
    entries: set[str] = set()
    in_command_selection = False
    for line in text.splitlines():
        if line == "## Command Selection Guide":
            in_command_selection = True
            continue
        if in_command_selection and line.startswith("## "):
            break
        if not in_command_selection:
            continue
        entries.update(re.findall(r"`(/brain-[a-z0-9-]+)`", line))
    return sorted(entries)


def readme_all_command_references(text: str) -> list[str]:
    return sorted(set(re.findall(r"`(/brain-[a-z0-9-]+)`", text)))


def agent_harness_command_routing_references(text: str) -> list[str]:
    body = section_body(text, "## Command Routing")
    return sorted(set(re.findall(r"`(/brain-[a-z0-9-]+)`", body)))


def state_machine_command_mapping_references(text: str) -> list[str]:
    body = section_body(text, "## Command Mapping")
    return sorted(set(re.findall(r"`(/brain-[a-z0-9-]+)`", body)))


def state_machine_command_mapped_states(text: str) -> list[str]:
    body = section_body(text, "## Command Mapping")
    return sorted(set(re.findall(r"^- `([a-z][a-z0-9_]*)` ->", body, flags=re.MULTILINE)))


def state_machine_states(text: str) -> list[str]:
    body = section_body(text, "## States")
    return sorted(set(re.findall(r"^([a-z][a-z0-9_]+)$", body, flags=re.MULTILINE)))


def readme_skill_catalog_entries(text: str) -> list[str]:
    entries: set[str] = set()
    in_core_skills = False
    for line in text.splitlines():
        if line == "## Core Skills":
            in_core_skills = True
            continue
        if in_core_skills and line.startswith("## "):
            break
        if not in_core_skills:
            continue
        match = re.match(r"- `([a-z0-9]+(?:-[a-z0-9]+)*)`", line)
        if match:
            entries.add(match.group(1))
    return sorted(entries)


def readme_documentation_guide_entries(text: str) -> list[str]:
    entries: set[str] = set()
    in_documentation_guide = False
    for line in text.splitlines():
        if line == "## Documentation Guide":
            in_documentation_guide = True
            continue
        if in_documentation_guide and line.startswith("## "):
            break
        if not in_documentation_guide:
            continue
        entries.update(re.findall(r"`(docs/[a-z0-9-]+\.md)`", line))
    return sorted(entries)


def readme_adapter_guide_entries(text: str) -> list[str]:
    body = section_body(text, "## Adapter Guide")
    return sorted(set(re.findall(r"`(adapters/[a-z0-9-]+/README\.md)`", body)))


def readme_artifact_routing_entries(text: str, prefix: str) -> list[str]:
    body = section_body(text, "## Artifact Routing Guide")
    escaped_prefix = re.escape(prefix)
    pattern = rf"`({escaped_prefix}/[a-z0-9-]+(?:\.schema)?\.json|{escaped_prefix}/[a-z0-9-]+\.md)`"
    return sorted(set(re.findall(pattern, body)))


def template_schema_field_references(text: str) -> set[str]:
    refs: set[str] = set()
    for line in text.splitlines():
        if "schema fields" not in line.lower():
            continue
        refs.update(re.findall(r"`([A-Za-z_][A-Za-z0-9_]*)`", line))
    return refs


def command_skills_to_load(text: str) -> list[str]:
    body = section_body(text, "## Skills to load")
    return sorted(set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", body)))


def command_lifecycle_state(text: str) -> str:
    purpose_body = section_body(text, "## Purpose")
    match = re.search(r"^State: ([A-Z]+)$", purpose_body, flags=re.MULTILINE)
    return match.group(1) if match else ""


def slug_from_title(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug


def command_required_artifact_template(text: str) -> str:
    output_body = section_body(text, "## Output")
    match = re.search(r"Required artifact:\s*\*\*([^*]+)\*\*", output_body)
    if not match:
        return ""
    artifact_slug = slug_from_title(match.group(1))
    return f"templates/{artifact_slug}.md" if artifact_slug else ""


def normalized_section_body(text: str, section: str) -> str:
    return re.sub(r"\s+", " ", section_body(text, section).strip().lower())


def evals_readme_catalog_entries(text: str, section: str) -> list[str]:
    body = section_body(text, section)
    if not body.strip() and section == "## Case catalog":
        body = text
    return sorted(set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", body)))


def local_markdown_links(text: str) -> list[str]:
    return [target for target, _anchor in local_markdown_link_targets(text)]


def local_markdown_link_targets(text: str) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if not target:
            continue
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1].strip()
        target = target.split()[0]
        path_part, separator, anchor_part = target.partition("#")
        if not path_part and not separator:
            continue
        if re.match(r"^[a-z][a-z0-9+.-]*:", path_part, flags=re.IGNORECASE):
            continue
        if path_part.startswith("//"):
            continue
        links.append((path_part, anchor_part if separator else ""))
    return links


def github_markdown_slug(heading_text: str) -> str:
    heading = heading_text.strip().lower()
    heading = re.sub(r"^[#]+\s*", "", heading)
    heading = re.sub(r"[^\w\s-]", "", heading, flags=re.UNICODE)
    return re.sub(r"\s+", "-", heading.strip())


def markdown_heading_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    in_fenced_code = False
    for line in text.splitlines():
        if line.startswith("```") or line.startswith("~~~"):
            in_fenced_code = not in_fenced_code
            continue
        if in_fenced_code or not line.startswith("#"):
            continue
        if not re.match(r"^#{1,6}\s+", line):
            continue
        anchors.add(github_markdown_slug(line))
    return anchors


def validate(root: Path = ROOT) -> list[str]:
    root = Path(root)
    errors: list[str] = []

    for path in sorted((root / "schemas").glob("*.json")):
        schema_slug = path.name.removesuffix(".schema.json")
        if not path.name.endswith(".schema.json") or not is_lowercase_kebab(schema_slug):
            errors.append(f"{rel(path, root)} filename must use lowercase kebab-case with .schema.json suffix")

        try:
            schema = json.loads(
                path.read_text(encoding="utf-8"),
                object_pairs_hook=reject_duplicate_json_keys,
            )
        except Exception as exc:
            errors.append(f"invalid json schema {rel(path, root)}: {exc}")
            continue

        required_fields = schema.get("required", [])
        if isinstance(required_fields, list):
            seen_required_fields: set[str] = set()
            duplicate_required_fields: set[str] = set()
            for field in required_fields:
                field_marker = json.dumps(field, sort_keys=True)
                if field_marker in seen_required_fields:
                    duplicate_required_fields.add(field_marker)
                seen_required_fields.add(field_marker)
            for field in sorted(duplicate_required_fields):
                errors.append(f"{rel(path, root)} required field is duplicated: {field.strip(chr(34))}")

        try:
            schema_validator = validators.validator_for(schema)
            schema_validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"invalid json schema {rel(path, root)}: {exc}")
            continue

        example_path = root / "examples" / "artifacts" / path.name.replace(".schema.json", ".example.json")
        if not example_path.exists():
            errors.append(
                f"{rel(path, root)} missing example artifact: {rel(example_path, root)}"
            )
        else:
            try:
                example = json.loads(
                    example_path.read_text(encoding="utf-8"),
                    object_pairs_hook=reject_duplicate_json_keys,
                )
                instance_validator = schema_validator(schema)
                example_errors = sorted(instance_validator.iter_errors(example), key=lambda error: list(error.path))
                for example_error in example_errors:
                    errors.append(
                        f"{rel(example_path, root)} must validate against {rel(path, root)}: {example_error.message}"
                    )
            except Exception as exc:
                errors.append(
                    f"{rel(example_path, root)} must contain valid JSON for {rel(path, root)}: {exc}"
                )

        properties = schema.get("properties", {})
        if not schema.get("$schema"):
            errors.append(f"{rel(path, root)} missing $schema dialect declaration")
        expected_schema_title = artifact_title_from_slug(schema_slug)
        if not schema.get("title"):
            errors.append(f"{rel(path, root)} missing title")
        elif schema.get("title") != expected_schema_title:
            errors.append(f"{rel(path, root)} title must match filename: {expected_schema_title}")
        if path.name == "implementation-plan.schema.json" and "rollback" not in required_fields:
            errors.append(
                "schemas/implementation-plan.schema.json must require rollback so every build slice has an explicit rollback path"
            )
        if path.name == "skill.schema.json":
            for field in REQUIRED_SKILL_SCHEMA_FIELDS:
                if field not in required_fields:
                    field_reason = {
                        "lifecycle_stage": "so skills declare their SDLC fit",
                        "output_artifact": "so skills name the handoff contract",
                    }[field]
                    errors.append(f"schemas/skill.schema.json must require {field} {field_reason}")
            for field in REQUIRED_SKILL_SCHEMA_NONEMPTY_ARRAY_FIELDS:
                field_schema = properties.get(field, {})
                if not isinstance(field_schema, dict) or field_schema.get("minItems", 0) < 1:
                    errors.append(
                        f"schemas/skill.schema.json {field} must require at least one concrete item"
                    )
        if path.name == "handoff-report.schema.json":
            state_schema = properties.get("state", {})
            if not isinstance(state_schema, dict) or state_schema.get("enum") != REQUIRED_STATE_MACHINE_VALUES:
                errors.append("schemas/handoff-report.schema.json state must enumerate Agent Brain state machine values")
            if "fresh_validation_proof" not in required_fields:
                errors.append("schemas/handoff-report.schema.json must require fresh_validation_proof")
            if "coordination_review" not in required_fields:
                errors.append("schemas/handoff-report.schema.json must require coordination_review")
            for field in REQUIRED_HANDOFF_SCHEMA_RESUME_FIELDS:
                if field not in required_fields:
                    errors.append(
                        f"schemas/handoff-report.schema.json required fields must include resume-ready field: {field}"
                    )
            for field in REQUIRED_HANDOFF_SCHEMA_BLOCKED_RESUME_FIELDS:
                if field not in required_fields:
                    errors.append(f"schemas/handoff-report.schema.json must require {field} for blocked resume")
        for field in required_fields:
            if field not in properties:
                errors.append(f"{rel(path, root)} required field lacks property definition: {field}")
        for field in sorted({"evidence", "evidence_checked"} & set(required_fields)):
            field_schema = properties.get(field, {})
            if isinstance(field_schema, dict) and field_schema.get("type") == "array":
                if field_schema.get("minItems", 0) < 1:
                    errors.append(f"{rel(path, root)} {field} must require at least one evidence item")
        for location in find_object_schemas_without_closed_properties(schema):
            if location == "$":
                errors.append(f"{rel(path, root)} object schema must set additionalProperties to false")
            else:
                display_location = location.removeprefix("$.")
                errors.append(
                    f"{rel(path, root)} object schema at {display_location} must set additionalProperties to false"
                )

        template = root / "templates" / path.name.replace(".schema.json", ".md")
        if template.exists():
            template_text = template.read_text(errors="ignore")
            template_field_refs = template_schema_field_references(template_text)
            schema_field_names = set(properties)
            for field in required_fields:
                if f"`{field}`" not in template_text:
                    errors.append(f"{rel(template, root)} missing required schema field reference: {field}")
            for field in properties:
                if field in required_fields:
                    continue
                if f"`{field}`" not in template_text:
                    errors.append(f"{rel(template, root)} missing schema field reference: {field}")
            for field in sorted(template_field_refs - schema_field_names):
                errors.append(
                    f"{rel(template, root)} references unknown schema field from {rel(path, root)}: {field}"
                )

    for required_path in REQUIRED_ROOT:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    for root_markdown in sorted(root.glob("*.md")):
        single_h1_error = validate_single_h1(root_markdown, root)
        if single_h1_error:
            errors.append(single_h1_error)

    constitution = root / "AGENTBRAIN.md"
    if constitution.exists():
        constitution_text_lower = constitution.read_text(errors="ignore").lower()
        for required_term in REQUIRED_CONSTITUTION_NONINTERACTIVE_TERMS:
            if required_term not in constitution_text_lower:
                errors.append(
                    "AGENTBRAIN.md must document noninteractive scheduled-run fallback guidance: "
                    f"{required_term}"
                )

    for required_path in REQUIRED_FILES:
        required_file = root / required_path
        if not required_file.exists():
            errors.append(f"missing {required_path}")
            continue
        if required_path == "requirements-dev.txt":
            for requirement in find_missing_dev_requirements(required_file.read_text(errors="ignore")):
                errors.append(f"requirements-dev.txt must include: {requirement}")

    for required_directory in REQUIRED_DIRECTORIES:
        if not (root / required_directory).is_dir():
            errors.append(f"missing {required_directory}/")

    for required_path in REQUIRED_ARTIFACT_FILES:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    constitution = root / "AGENTBRAIN.md"
    if constitution.exists():
        constitution_text = constitution.read_text(errors="ignore")
        constitution_text_lower = constitution_text.lower()
        for term in REQUIRED_CONSTITUTION_NONINTERACTIVE_TERMS:
            if term not in constitution_text_lower:
                errors.append(
                    "AGENTBRAIN.md must document noninteractive scheduled-run fallback guidance: "
                    f"{term}"
                )
        done_definition = section_body(constitution_text, "## Done definition").lower()
        for term in REQUIRED_CONSTITUTION_DONE_DEFINITION_TERMS:
            if term not in done_definition:
                errors.append(
                    "AGENTBRAIN.md done definition must require fresh validation proof: "
                    f"{term}"
                )
        public_copy_neutrality = section_body(constitution_text, "## Public copy neutrality").lower()
        for term in REQUIRED_CONSTITUTION_PUBLIC_COPY_TERMS:
            if term not in public_copy_neutrality:
                errors.append(
                    "AGENTBRAIN.md must document public-copy neutrality for source distillation: "
                    f"{term}"
                )

    gitignore = root / ".gitignore"
    if not gitignore.exists():
        errors.append("missing .gitignore")
    else:
        gitignore_lines = set(gitignore.read_text(errors="ignore").splitlines())
        for pattern in REQUIRED_GITIGNORE_PATTERNS:
            if pattern not in gitignore_lines:
                errors.append(f".gitignore must ignore local/generated Python artifacts: {pattern}")

    command_files = [
        command
        for command in sorted((root / "commands").glob("*.md"))
        if command.name != "README.md"
    ]

    for required_path in REQUIRED_DOCS:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    state_machine = root / "docs" / "state-machine.md"
    if state_machine.exists():
        state_machine_text = state_machine.read_text(errors="ignore")
        state_machine_refs = state_machine_command_mapping_references(state_machine_text)
        mapped_states = state_machine_command_mapped_states(state_machine_text)
        listed_states = state_machine_states(state_machine_text)
        for required_state in REQUIRED_STATE_MACHINE_DOC_STATES:
            if required_state not in listed_states:
                errors.append(f"docs/state-machine.md states section missing state: {required_state}")
            elif required_state != "archive" and required_state not in mapped_states:
                errors.append(f"docs/state-machine.md command mapping missing state: {required_state}")
        for command in command_files:
            command_name = f"/{command.stem}"
            if command_name not in state_machine_refs:
                errors.append(f"docs/state-machine.md command mapping missing command: {command_name}")
        for command_name in state_machine_refs:
            command_file = root / "commands" / f"{command_name.removeprefix('/')}.md"
            if not command_file.exists():
                errors.append(
                    f"docs/state-machine.md command mapping points to missing command: {command_name}"
                )

    agent_harness = root / "docs" / "agent-harness.md"
    if agent_harness.exists():
        agent_harness_text = agent_harness.read_text(errors="ignore")
        for required_section in REQUIRED_AGENT_HARNESS_SECTIONS:
            if required_section not in agent_harness_text:
                errors.append(
                    f"docs/agent-harness.md missing harness operating section: {required_section}"
                )
        for run_command in REQUIRED_AGENT_HARNESS_VALIDATION_COMMANDS:
            if run_command not in agent_harness_text:
                errors.append(f"docs/agent-harness.md validation section must document: {run_command}")
        agent_harness_text_lower = agent_harness_text.lower()
        for required_term, message in REQUIRED_AGENT_HARNESS_VALIDATION_GATE_TERMS.items():
            if required_term.lower() not in agent_harness_text_lower:
                errors.append(message)
        harness_prompt = section_body(agent_harness_text, REQUIRED_AGENT_HARNESS_PROMPT_SECTION)
        if not harness_prompt.strip():
            errors.append(
                "docs/agent-harness.md missing copyable harness prompt section: ## Copyable Harness Prompt"
            )
        for required_term in REQUIRED_AGENT_HARNESS_PROMPT_TERMS:
            if required_term not in harness_prompt:
                errors.append(f"docs/agent-harness.md copyable prompt must mention: {required_term}")
        worker_guidance = section_body(agent_harness_text, "## Using It With Coding Agents")
        if not worker_guidance.strip():
            errors.append(
                "docs/agent-harness.md missing harness operating section: ## Using It With Coding Agents"
            )
        for role in REQUIRED_AGENT_HARNESS_WORKER_ROLES:
            if role not in worker_guidance:
                errors.append(f"docs/agent-harness.md worker guidance must mention role: {role}")
        worker_guidance_lower = worker_guidance.lower()
        for term, message in REQUIRED_AGENT_HARNESS_WORKER_CONTRACT_TERMS.items():
            if term not in worker_guidance_lower:
                errors.append(message)
        for term in REQUIRED_AGENT_HARNESS_RESUME_TERMS:
            if term not in agent_harness_text_lower:
                errors.append(f"docs/agent-harness.md resume guidance must mention: {term}")
        fresh_checkout = section_body(agent_harness_text, "## Fresh Checkout Bootstrap")
        for term in REQUIRED_AGENT_HARNESS_FRESH_CHECKOUT_TERMS:
            if term.lower() not in fresh_checkout.lower():
                errors.append(
                    "docs/agent-harness.md fresh checkout bootstrap must verify remote freshness: "
                    f"{term}"
                )
        edge_cases = section_body(agent_harness_text, "## Edge Cases").lower()
        for term in REQUIRED_AGENT_HARNESS_NONINTERACTIVE_TERMS:
            if term not in edge_cases:
                errors.append(
                    "docs/agent-harness.md edge cases must document noninteractive scheduled runs: "
                    f"{term}"
                )
        harness_command_refs = agent_harness_command_routing_references(agent_harness_text)
        for command in command_files:
            command_name = f"/{command.stem}"
            if command_name not in harness_command_refs:
                errors.append(f"docs/agent-harness.md command routing missing command: {command_name}")
        for command_name in harness_command_refs:
            command_file = root / "commands" / f"{command_name.removeprefix('/')}.md"
            if not command_file.exists():
                errors.append(
                    f"docs/agent-harness.md command routing entry points to missing file: {command_name}"
                )
        handoff_contract = section_body(agent_harness_text, "## Handoff Contract").lower()
        for term in REQUIRED_AGENT_HARNESS_HANDOFF_TERMS:
            if term not in handoff_contract:
                errors.append(f"docs/agent-harness.md handoff contract must require {term}")
        harness_troubleshooting = section_body(agent_harness_text, "## Troubleshooting")
        harness_troubleshooting_lower = harness_troubleshooting.lower()
        for required_term, message in REQUIRED_AGENT_HARNESS_TROUBLESHOOTING_TERMS.items():
            if required_term.lower() not in harness_troubleshooting_lower:
                errors.append(f"{message}: {required_term}")
        for required_term in REQUIRED_AGENT_HARNESS_EVAL_TROUBLESHOOTING_TERMS:
            if required_term.lower() not in harness_troubleshooting_lower:
                errors.append(
                    "docs/agent-harness.md troubleshooting must document eval case recovery: "
                    f"{required_term}"
                )
        harness_maintainer_checklist = section_body(agent_harness_text, "## Maintainer Checklist")
        for required_term in REQUIRED_AGENT_HARNESS_MAINTAINER_TERMS:
            if required_term not in harness_maintainer_checklist:
                errors.append(f"docs/agent-harness.md maintainer checklist must mention: {required_term}")

    for required_path in REQUIRED_SKILLS:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    for required_path in REQUIRED_EVAL_CASES:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    for required_path in REQUIRED_EVAL_DOCS:
        if not (root / required_path).exists():
            errors.append(f"missing {required_path}")

    for required_path in REQUIRED_WORKFLOWS:
        workflow = root / required_path
        if not workflow.exists():
            errors.append(f"missing {required_path}")
            continue
        workflow_text = workflow.read_text(errors="ignore")
        if required_path == ".github/workflows/quality.yml":
            for run_command in REQUIRED_QUALITY_WORKFLOW_RUNS:
                if run_command not in workflow_text:
                    errors.append(f"{required_path} must run: {run_command}")
    workflow_dir = root / ".github" / "workflows"
    workflow_files = sorted([*workflow_dir.glob("*.yml"), *workflow_dir.glob("*.yaml")])
    for workflow in workflow_files:
        workflow_text = workflow.read_text(errors="ignore")
        if "git diff --check" not in workflow_text:
            errors.append(f"{rel(workflow, root)} must run: git diff --check")
        if not workflow_sets_readonly_contents_permission(workflow_text):
            errors.append(f"{rel(workflow, root)} must set permissions to contents: read")
        if "timeout-minutes:" not in workflow_text:
            errors.append(f"{rel(workflow, root)} must set timeout-minutes")
        for permission in find_write_workflow_permissions(workflow_text):
            errors.append(f"{rel(workflow, root)} must not request write repository permissions: {permission}")
        for trigger in REQUIRED_WORKFLOW_TRIGGERS:
            if not workflow_declares_trigger(workflow_text, trigger):
                errors.append(f"{rel(workflow, root)} must run on {trigger}")

    research_watchlist = root / "docs" / "research-watchlist.md"
    if research_watchlist.exists():
        research_text = research_watchlist.read_text(errors="ignore")
        for source in RESEARCH_WATCHLIST_REQUIRED_SOURCES:
            if source not in research_text:
                errors.append(f"docs/research-watchlist.md missing tracked source: {source}")

    seen_skill_examples: dict[str, str] = {}
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        text = skill.read_text(errors="ignore")
        single_h1_error = validate_single_h1(skill, root)
        if single_h1_error:
            errors.append(single_h1_error)
        if not has_delimited_frontmatter(text):
            errors.append(f"{rel(skill, root)} frontmatter must be delimited by ---")
        frontmatter = parse_frontmatter(text)
        expected_name = skill.parent.name
        if not is_lowercase_kebab(expected_name):
            errors.append(f"{rel(skill, root)} skill directory must use lowercase kebab-case")
        first_line = next((line for line in text.splitlines() if line.startswith("# ")), "")
        expected_heading = f"# {expected_name}"
        if first_line != expected_heading:
            errors.append(f"{rel(skill, root)} heading must be {expected_heading}")
        if frontmatter.get("name") != expected_name:
            errors.append(f"{rel(skill, root)} frontmatter name must be {expected_name}")
        if not frontmatter.get("description"):
            errors.append(f"{rel(skill, root)} frontmatter description is required")
        elif not frontmatter["description"].startswith("Use when"):
            errors.append(f"{rel(skill, root)} frontmatter description must start with 'Use when'")
        skill_lines = text.splitlines()
        for section in REQUIRED_SKILL_SECTIONS:
            section_count = skill_lines.count(section)
            if section_count == 0:
                errors.append(f"{rel(skill, root)} missing {section}")
            else:
                if section_count > 1:
                    errors.append(f"{rel(skill, root)} section must appear exactly once: {section}")
                if not section_has_body(text, section):
                    errors.append(f"{rel(skill, root)} section has no body: {section}")
        if not sections_are_in_order(text, REQUIRED_SKILL_SECTIONS):
            errors.append(f"{rel(skill, root)} sections must appear in canonical order")
        if skill.parent.name == "plan-slicing":
            text_lower = text.lower()
            for required_term, message in REQUIRED_PLAN_SLICING_TERMS.items():
                if required_term not in text_lower:
                    errors.append(message)
        example = normalized_section_body(text, "## Example")
        if example:
            if example in seen_skill_examples:
                errors.append(
                    f"{rel(skill, root)} example duplicates {seen_skill_examples[example]}"
                )
            else:
                seen_skill_examples[example] = rel(skill, root)

    seen_workflows: dict[str, str] = {}
    seen_quality_bars: dict[str, str] = {}
    seen_stop_conditions: dict[str, str] = {}
    skills_loaded_by_commands: set[str] = set()
    skills_loaded_by_command: dict[str, set[str]] = {}
    required_command_artifact_templates: dict[str, str] = {}
    for command in command_files:
        text = command.read_text(errors="ignore")
        expected_heading = f"# /{command.stem}"
        lines = text.splitlines()
        first_line = lines[0] if lines else ""
        h1_headings = markdown_h1_headings(text)
        if not is_lowercase_kebab(command.stem):
            errors.append(f"{rel(command, root)} filename must use lowercase kebab-case")
        if not command.stem.startswith("brain-"):
            errors.append(f"{rel(command, root)} filename must start with brain-")
        if first_line != expected_heading:
            errors.append(f"{rel(command, root)} heading must be {expected_heading}")
        if len(h1_headings) != 1:
            errors.append(f"{rel(command, root)} must contain exactly one H1 heading")
        for section in REQUIRED_COMMAND_SECTIONS:
            section_count = lines.count(section)
            if section_count == 0:
                errors.append(f"{rel(command, root)} missing {section}")
            else:
                if section_count > 1:
                    errors.append(f"{rel(command, root)} section must appear exactly once: {section}")
                if not section_has_body(text, section):
                    errors.append(f"{rel(command, root)} section has no body: {section}")
        if not sections_are_in_order(text, REQUIRED_COMMAND_SECTIONS):
            errors.append(f"{rel(command, root)} sections must appear in canonical order")
        if command_lifecycle_state(text) not in VALID_COMMAND_LIFECYCLE_STATES:
            errors.append(f"{rel(command, root)} purpose must declare valid lifecycle state")
        if command_lifecycle_state(text) == "BUILD":
            command_text_lower = text.lower()
            if not any(term in command_text_lower for term in REQUIRED_BUILD_COMMAND_PROOF_TERMS):
                errors.append(
                    f"{rel(command, root)} BUILD workflow must require failing test before implementation or validator-first proof"
                )
            if not any(term in command_text_lower for term in REQUIRED_BUILD_COMMAND_RED_REFACTOR_TERMS):
                errors.append(
                    f"{rel(command, root)} BUILD workflow must block refactoring while tests or validators are red"
                )
        input_contract = section_body(text, "## Input contract").lower()
        for required_term in REQUIRED_COMMAND_INPUT_CONTRACT_TERMS:
            if required_term not in input_contract:
                errors.append(f"{rel(command, root)} input contract must mention: {required_term}")
        if command.stem == "brain-start":
            workflow_body = section_body(text, "## Workflow").lower()
            for required_term in REQUIRED_START_COMMAND_REPO_INSPECTION_TERMS:
                if required_term not in workflow_body:
                    errors.append(
                        f"{rel(command, root)} workflow must inspect repository state before routing: {required_term}"
                    )
        command_text_lower = text.lower()
        if any(term in command_text_lower for term in COMMAND_ASK_USER_TERMS):
            for required_term in COMMAND_NONINTERACTIVE_FALLBACK_TERMS:
                if required_term not in command_text_lower:
                    errors.append(
                        f"{rel(command, root)} mentions asking the user but must include noninteractive fallback guidance"
                    )
                    break
        output_section = section_body(text, "## Output")
        output_body = output_section.lower()
        if "required artifact:" not in output_body:
            errors.append(f"{rel(command, root)} output must name a required artifact")
        required_artifact_template = command_required_artifact_template(text)
        if required_artifact_template:
            required_command_artifact_templates[f"/{command.stem}"] = required_artifact_template
            if f"`{required_artifact_template}`" not in output_section:
                errors.append(
                    f"{rel(command, root)} output must cite required artifact template: {required_artifact_template}"
                )
            if not (root / required_artifact_template).exists():
                errors.append(
                    f"{rel(command, root)} required artifact lacks template: {required_artifact_template}"
                )
        for required_term in REQUIRED_COMMAND_OUTPUT_TERMS:
            if required_term not in output_body:
                errors.append(f"{rel(command, root)} output must mention: {required_term}")
        workflow = normalized_section_body(text, "## Workflow")
        if workflow:
            if workflow in seen_workflows:
                errors.append(
                    f"{rel(command, root)} workflow duplicates {seen_workflows[workflow]}"
                )
            else:
                seen_workflows[workflow] = rel(command, root)
        quality_bar = normalized_section_body(text, "## Quality bar")
        if quality_bar:
            for required_term in REQUIRED_COMMAND_QUALITY_BAR_TERMS:
                if required_term not in quality_bar:
                    errors.append(f"{rel(command, root)} quality bar must mention: {required_term}")
            if quality_bar in seen_quality_bars:
                errors.append(
                    f"{rel(command, root)} quality bar duplicates {seen_quality_bars[quality_bar]}"
                )
            else:
                seen_quality_bars[quality_bar] = rel(command, root)
        example = section_body(text, "## Example").lower()
        if example:
            for required_term in REQUIRED_COMMAND_EXAMPLE_TERMS:
                if required_term not in example:
                    errors.append(f"{rel(command, root)} example must mention: {required_term}")
        stop_conditions = normalized_section_body(text, "## Stop conditions")
        if stop_conditions:
            if any(term in command_text_lower for term in COMMAND_ASK_USER_TERMS):
                if not all(term in stop_conditions for term in COMMAND_NONINTERACTIVE_FALLBACK_TERMS):
                    errors.append(
                        f"{rel(command, root)} stop conditions must include noninteractive fallback guidance when asking for human input"
                    )
            if stop_conditions in seen_stop_conditions:
                errors.append(
                    f"{rel(command, root)} stop conditions duplicate {seen_stop_conditions[stop_conditions]}"
                )
            else:
                seen_stop_conditions[stop_conditions] = rel(command, root)
        skill_names = command_skills_to_load(text)
        skills_loaded_by_command[f"/{command.stem}"] = set(skill_names)
        skills_loaded_by_commands.update(skill_names)
        if not skill_names:
            errors.append(f"{rel(command, root)} skills-to-load section must name at least one skill")
        for skill_name in skill_names:
            skill_file = root / "skills" / skill_name / "SKILL.md"
            if not skill_file.exists():
                errors.append(
                    f"{rel(command, root)} skills-to-load entry points to missing skill: {skill_name}"
                )

    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        skill_name = skill.parent.name
        if skill_name not in skills_loaded_by_commands:
            errors.append(f"{rel(skill, root)} must be loaded by at least one command")

    skills_readme = root / "skills" / "README.md"
    if skills_readme.exists():
        skills_readme_text = skills_readme.read_text(errors="ignore")
        skills_readme_text_lower = skills_readme_text.lower()
        for required_term in REQUIRED_SKILLS_README_QUALITY_BAR_TERMS:
            if required_term not in skills_readme_text_lower:
                errors.append(f"skills/README.md quality bar must mention: {required_term}")
        for skill in sorted((root / "skills").glob("*/SKILL.md")):
            skill_name = skill.parent.name
            expected_link = f"[`{skill_name}`]({skill_name}/SKILL.md)"
            if expected_link not in skills_readme_text:
                errors.append(f"skills/README.md catalog missing skill link: {skill_name}")

    commands_readme = root / "commands" / "README.md"
    if commands_readme.exists():
        commands_readme_text = commands_readme.read_text(errors="ignore")
        commands_readme_text_lower = commands_readme_text.lower()
        command_catalog_entries = command_catalog_entry_lines(commands_readme_text)
        command_names = {f"/{command.stem}" for command in command_files}
        for catalog_command_name in sorted(command_catalog_entries):
            if catalog_command_name not in command_names:
                errors.append(
                    "commands/README.md catalog entry points to missing command file: "
                    f"{catalog_command_name}"
                )
        for required_term in REQUIRED_COMMAND_CATALOG_CONTRACT_TERMS:
            if required_term not in commands_readme_text_lower:
                errors.append(
                    "commands/README.md must document command catalog contract: "
                    f"{required_term}"
                )
        for command in command_files:
            command_name = f"/{command.stem}"
            expected_link = f"[`{command_name}`]({command.name})"
            if expected_link not in commands_readme_text:
                errors.append(f"commands/README.md catalog missing command link: {command_name}")
                continue
            entry = command_catalog_entries.get(command_name, "")
            for field in ["State:", "Skills:", "Artifact:", "Stop:"]:
                if field not in entry:
                    errors.append(
                        f"commands/README.md catalog entry for {command_name} must name routing field: {field}"
                    )
            command_text = command.read_text(errors="ignore")
            expected_state = command_lifecycle_state(command_text)
            if expected_state and f"State: {expected_state}" not in entry:
                errors.append(
                    f"commands/README.md catalog entry for {command_name} must match command lifecycle state: {expected_state}"
                )
            expected_artifact = command_required_artifact_template(command_text)
            if expected_artifact and f"Artifact: `{expected_artifact}`" not in entry:
                errors.append(
                    f"commands/README.md catalog entry for {command_name} must match command artifact: {expected_artifact}"
                )
            for skill_name in command_skills_to_load(command_text):
                if f"`{skill_name}`" not in entry:
                    errors.append(
                        f"commands/README.md catalog entry for {command_name} must include command skill: {skill_name}"
                    )

    readme = root / "README.md"
    if readme.exists():
        readme_text = readme.read_text(errors="ignore")
        for required_section in REQUIRED_README_HARNESS_SECTIONS:
            if required_section not in readme_text:
                errors.append(f"README.md missing self-setup harness section: {required_section}")
        readme_minimal_prompt = section_body(readme_text, "## Minimal Harness Prompt")
        readme_minimal_prompt_lower = readme_minimal_prompt.lower()
        for required_term in REQUIRED_README_MINIMAL_HARNESS_PROMPT_TERMS:
            if required_term.lower() not in readme_minimal_prompt_lower:
                errors.append(f"README.md minimal harness prompt must mention: {required_term}")
        for run_command in REQUIRED_README_VALIDATION_COMMANDS:
            if run_command not in readme_text:
                errors.append(f"README.md validation section must document: {run_command}")
        readme_validation_body = section_body(readme_text, "## Validation")
        if "python scripts/scrub_public_copy.py" not in readme_validation_body:
            errors.append(
                "README.md validation section must document exact scrub script command: python scripts/scrub_public_copy.py"
            )
        readme_quickstart = section_body(readme_text, "## Quickstart")
        readme_quickstart_lower = readme_quickstart.lower()
        for run_command in REQUIRED_README_QUICKSTART_COMMANDS:
            if run_command not in readme_quickstart:
                errors.append(f"README.md Quickstart must document: {run_command}")
        for required_term, message in REQUIRED_README_QUICKSTART_TERMS.items():
            if required_term.lower() not in readme_quickstart_lower:
                errors.append(message)
        for required_term in REQUIRED_README_REMOTE_FRESHNESS_TERMS:
            if required_term.lower() not in readme_quickstart_lower:
                errors.append(
                    "README.md Quickstart must verify remote freshness before editing: "
                    f"{required_term}"
                )
        readme_text_lower = readme_text.lower()
        for required_term, message in REQUIRED_README_VALIDATION_GATE_TERMS.items():
            if required_term.lower() not in readme_text_lower:
                errors.append(message)
        core_command_refs = readme_command_references(readme_text)
        core_command_links = readme_command_catalog_links(readme_text)
        command_selection_refs = readme_command_selection_references(readme_text)
        all_command_refs = readme_all_command_references(readme_text)
        for command in command_files:
            command_name = f"/{command.stem}"
            if command_name not in core_command_refs:
                errors.append(f"README.md core command catalog missing command: {command_name}")
            else:
                expected_link = f"commands/{command.stem}.md"
                if core_command_links.get(command_name) != expected_link:
                    errors.append(
                        f"README.md core command catalog entry must link to {expected_link}: {command_name}"
                    )
            if command_name not in command_selection_refs:
                errors.append(f"README.md command selection guide missing command: {command_name}")
        for command_name in core_command_refs:
            command_file = root / "commands" / f"{command_name.removeprefix('/')}.md"
            if not command_file.exists():
                errors.append(f"README.md command catalog entry points to missing file: {command_name}")
        for command_name in command_selection_refs:
            command_file = root / "commands" / f"{command_name.removeprefix('/')}.md"
            if not command_file.exists():
                errors.append(
                    f"README.md command selection guide entry points to missing file: {command_name}"
                )
        for command_name in all_command_refs:
            command_file = root / "commands" / f"{command_name.removeprefix('/')}.md"
            if not command_file.exists():
                errors.append(f"README.md command reference points to missing file: {command_name}")
        command_selection_body = section_body(readme_text, "## Command Selection Guide").lower()
        if not all(
            required_term.lower() in command_selection_body
            for required_term in REQUIRED_README_COMMAND_SELECTION_FALLBACK_TERMS
        ):
            errors.append("README.md command selection guide must tell agents what to do when no command fits")
        if not all(
            required_term.lower() in command_selection_body
            for required_term in REQUIRED_README_COMMAND_SELECTION_ARTIFACT_TERMS
        ):
            errors.append("README.md command selection guide must tell agents how to route the output artifact")
        core_skill_refs = readme_skill_catalog_entries(readme_text)
        for skill in sorted((root / "skills").glob("*/SKILL.md")):
            skill_name = skill.parent.name
            if skill_name not in core_skill_refs:
                errors.append(f"README.md core skill catalog missing skill: {skill_name}")
        for skill_name in core_skill_refs:
            skill_file = root / "skills" / skill_name / "SKILL.md"
            if not skill_file.exists():
                errors.append(f"README.md skill catalog entry points to missing file: {skill_name}")
        readme_docs = readme_documentation_guide_entries(readme_text)
        for doc in sorted((root / "docs").glob("*.md")):
            doc_ref = rel(doc, root)
            if doc_ref not in readme_docs:
                errors.append(f"README.md documentation guide missing doc: {doc_ref}")
        for doc_ref in readme_docs:
            if not (root / doc_ref).exists():
                errors.append(f"README.md documentation guide entry points to missing file: {doc_ref}")
        readme_adapters = readme_adapter_guide_entries(readme_text)
        for adapter in sorted((root / "adapters").glob("*/README.md")):
            adapter_ref = rel(adapter, root)
            if adapter_ref not in readme_adapters:
                errors.append(f"README.md adapter guide missing adapter: {adapter_ref}")
        for adapter_ref in readme_adapters:
            if not (root / adapter_ref).exists():
                errors.append(f"README.md adapter guide entry points to missing adapter: {adapter_ref}")
        artifact_schema_refs = readme_artifact_routing_entries(readme_text, "schemas")
        artifact_template_refs = readme_artifact_routing_entries(readme_text, "templates")
        for template_ref in artifact_template_refs:
            if not (root / template_ref).exists():
                errors.append(f"README.md artifact routing guide entry points to missing template: {template_ref}")
        for schema in sorted((root / "schemas").glob("*.json")):
            schema_ref = rel(schema, root)
            if f"`{schema_ref}`" not in readme_text:
                errors.append(f"README.md missing schema catalog entry: {schema_ref}")
            if schema_ref not in artifact_schema_refs:
                errors.append(f"README.md artifact routing guide missing schema: {schema_ref}")
        for template in sorted((root / "templates").glob("*.md")):
            template_ref = rel(template, root)
            if f"`{template_ref}`" not in readme_text:
                errors.append(f"README.md missing template catalog entry: {template_ref}")
            if template_ref not in artifact_template_refs:
                errors.append(f"README.md artifact routing guide missing template: {template_ref}")
        for command_name, template_ref in sorted(required_command_artifact_templates.items()):
            if template_ref not in artifact_template_refs:
                errors.append(
                    "README.md artifact routing guide must list command required artifact template "
                    f"{template_ref} for {command_name}"
                )
        mapped_paths = readme_repository_map_paths(readme_text)
        for mapped_path in mapped_paths:
            if not (root / mapped_path).exists():
                errors.append(f"README.md repository map lists missing path: {mapped_path}")
        for required_path in REQUIRED_README_REPOSITORY_MAP_PATHS:
            if required_path not in mapped_paths:
                errors.append(f"README.md repository map missing required path: {required_path}")
        troubleshooting_body = section_body(readme_text, "## Troubleshooting").lower()
        for required_term in REQUIRED_README_TROUBLESHOOTING_TERMS:
            if required_term.lower() not in troubleshooting_body:
                errors.append(
                    "README.md troubleshooting must document dirty working tree recovery: "
                    f"{required_term}"
                )
        for required_term in REQUIRED_README_SECRET_TROUBLESHOOTING_TERMS:
            if required_term.lower() not in troubleshooting_body:
                errors.append(
                    "README.md troubleshooting must document secret-like value recovery: "
                    f"{required_term}"
                )
        for required_term in REQUIRED_README_CI_TROUBLESHOOTING_TERMS:
            if required_term.lower() not in troubleshooting_body:
                errors.append(
                    "README.md troubleshooting must document CI failure recovery: "
                    f"{required_term}"
                )
        for required_term in REQUIRED_README_DEPENDENCY_TROUBLESHOOTING_TERMS:
            if required_term.lower() not in troubleshooting_body:
                errors.append(
                    "README.md troubleshooting must document dependency bootstrap recovery: "
                    f"{required_term}"
                )
        for required_term in REQUIRED_README_GENERATED_CACHE_TROUBLESHOOTING_TERMS:
            if required_term.lower() not in troubleshooting_body:
                errors.append(
                    "README.md troubleshooting must document generated cache recovery: "
                    f"{required_term}"
                )
        for required_term in REQUIRED_README_ARTIFACT_TROUBLESHOOTING_TERMS:
            if required_term.lower() not in troubleshooting_body:
                errors.append(
                    "README.md troubleshooting must document artifact contract recovery: "
                    f"{required_term}"
                )
        handoff_body = section_body(readme_text, "## Handoff Contract").lower()
        for required_term in REQUIRED_README_HANDOFF_TERMS:
            if required_term.lower() not in handoff_body:
                errors.append(f"README.md handoff contract must mention: {required_term}")
        for required_term in REQUIRED_README_HANDOFF_RESUME_TERMS:
            if required_term.lower() not in handoff_body:
                errors.append(f"README.md handoff contract must include resume guidance: {required_term}")
        evidence_freshness_body = section_body(readme_text, "## Evidence Freshness Rules").lower()
        for required_term in REQUIRED_README_EVIDENCE_FRESHNESS_TERMS:
            if required_term.lower() not in evidence_freshness_body:
                errors.append(f"README.md evidence freshness rules must mention: {required_term}")
        readme_edge_cases_body = section_body(readme_text, "## Edge Cases and Stop Conditions").lower()
        if not all(term in readme_edge_cases_body for term in REQUIRED_README_EDGE_CASE_APPROVAL_TERMS):
            errors.append("README.md edge cases must require explicit approval evidence before side effects")
        maintainer_loop_body = section_body(readme_text, "## Maintainer Loop")
        for required_term in REQUIRED_README_MAINTAINER_LOOP_TERMS:
            if required_term not in maintainer_loop_body:
                errors.append(f"README.md maintainer loop must mention: {required_term}")
        readme_status_body = section_body(readme_text, "## Status").lower()
        if any(term in readme_status_body for term in STALE_STATUS_COMPLETION_TERMS):
            errors.append("README.md status must describe ongoing hardening, not claim completion")

    contributing = root / "CONTRIBUTING.md"
    if contributing.exists():
        contributing_text = contributing.read_text(errors="ignore")
        for run_command in REQUIRED_CONTRIBUTING_VALIDATION_COMMANDS:
            if run_command not in contributing_text:
                errors.append(f"CONTRIBUTING.md validation section must document: {run_command}")

    tracked_files = tracked_git_files(root)
    for generated_path in sorted(root.rglob("*")):
        if not generated_path.is_file():
            continue
        if any(part in {".git", ".venv", "venv", "node_modules"} for part in generated_path.parts):
            continue
        if not (any(part in GENERATED_CACHE_PARTS for part in generated_path.parts) or generated_path.suffix in GENERATED_CACHE_SUFFIXES):
            continue
        generated_rel = rel(generated_path, root)
        if tracked_files is not None and generated_rel not in tracked_files:
            continue
        errors.append(f"generated Python cache file must not be present: {generated_rel}")

    skill_template = root / "templates" / "skill-template.md"
    if skill_template.exists():
        skill_template_text = skill_template.read_text(errors="ignore")
        skill_template_lines = skill_template_text.splitlines()
        if not has_delimited_frontmatter(skill_template_text):
            errors.append("templates/skill-template.md frontmatter must be delimited by ---")
        skill_template_frontmatter = parse_frontmatter(skill_template_text)
        skill_template_name = skill_template_frontmatter.get("name", "")
        if not is_lowercase_kebab(skill_template_name):
            errors.append("templates/skill-template.md frontmatter name must use lowercase kebab-case")
        if not skill_template_frontmatter.get("description", "").startswith("Use when"):
            errors.append("templates/skill-template.md frontmatter description must start with 'Use when'")
        for section in REQUIRED_SKILL_TEMPLATE_SECTIONS:
            section_count = skill_template_lines.count(section)
            if section_count == 0:
                errors.append(f"templates/skill-template.md missing {section}")
            else:
                if section_count > 1:
                    errors.append(f"templates/skill-template.md section must appear exactly once: {section}")
                if not section_has_body(skill_template_text, section):
                    errors.append(f"templates/skill-template.md section has no body: {section}")
        if not sections_are_in_order(skill_template_text, REQUIRED_SKILL_TEMPLATE_SECTIONS):
            errors.append("templates/skill-template.md sections must appear in canonical order")

    eval_cases = sorted((root / "evals" / "cases").glob("*.md"))
    for case in eval_cases:
        text = case.read_text(errors="ignore")
        single_h1_error = validate_single_h1(case, root)
        if single_h1_error:
            errors.append(single_h1_error)
        if not is_lowercase_kebab(case.stem):
            errors.append(f"{rel(case, root)} filename must use lowercase kebab-case")
        expected_heading = f"# Eval Case: {title_from_slug(case.stem)}"
        first_line = text.splitlines()[0] if text.splitlines() else ""
        if first_line != expected_heading:
            errors.append(f"{rel(case, root)} heading must be {expected_heading}")
        lines = text.splitlines()
        for section in REQUIRED_EVAL_CASE_SECTIONS:
            section_count = lines.count(section)
            if section_count == 0:
                errors.append(f"{rel(case, root)} missing {section}")
            else:
                if section_count > 1:
                    errors.append(f"{rel(case, root)} section must appear exactly once: {section}")
                if not section_has_body(text, section):
                    errors.append(f"{rel(case, root)} section has no body: {section}")
        if not sections_are_in_order(text, REQUIRED_EVAL_CASE_SECTIONS):
            errors.append(f"{rel(case, root)} sections must appear in canonical order")
        expected_behavior = section_body(text, "## Expected behavior").lower()
        if "evidence" not in expected_behavior:
            errors.append(f"{rel(case, root)} expected behavior must name evidence")
        if case.name == "real-runtime-smoke-test.md":
            for field in REQUIRED_REAL_RUNTIME_SMOKE_EVIDENCE_FIELDS:
                if field.lower() not in expected_behavior:
                    errors.append(
                        f"{rel(case, root)} expected behavior must require runtime evidence field: {field}"
                    )
            if not all(term in expected_behavior for term in REQUIRED_REAL_RUNTIME_SMOKE_READ_ONLY_TERMS):
                errors.append(
                    f"{rel(case, root)} expected behavior must distinguish read-only smoke from full validation"
                )
        harness_route = section_body(text, "## Harness route")
        if harness_route.strip():
            route_command_refs = set(re.findall(r"`(/brain-[a-z0-9-]+)`", harness_route))
            if not route_command_refs:
                errors.append(f"{rel(case, root)} harness route must name at least one /brain- command")
            for command_name in sorted(route_command_refs):
                command_file = command_name.removeprefix("/")
                if not (root / "commands" / f"{command_file}.md").exists():
                    errors.append(f"{rel(case, root)} harness route references missing command: {command_name}")
            route_skill_refs = set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", harness_route))
            existing_route_skill_refs = []
            for skill_name in sorted(route_skill_refs):
                if (root / "skills" / skill_name / "SKILL.md").exists():
                    existing_route_skill_refs.append(skill_name)
                else:
                    errors.append(f"{rel(case, root)} harness route references missing skill: {skill_name}")
            if not existing_route_skill_refs:
                errors.append(f"{rel(case, root)} harness route must name at least one existing skill")
            if route_command_refs and existing_route_skill_refs:
                route_command_skills = set().union(
                    *(skills_loaded_by_command.get(command_name, set()) for command_name in route_command_refs)
                )
                for skill_name in sorted(existing_route_skill_refs):
                    if skill_name not in route_command_skills:
                        errors.append(
                            f"{rel(case, root)} harness route references skill not loaded by any referenced command: {skill_name}"
                        )

    evals_readme = root / "evals" / "README.md"
    if evals_readme.exists():
        evals_readme_text = evals_readme.read_text(errors="ignore")
        evals_readme_run_contract = section_body(evals_readme_text, "## Running evals").lower()
        if not evals_readme_run_contract.strip():
            errors.append("evals/README.md missing eval run contract section: ## Running evals")
        for required_term in REQUIRED_EVALS_README_RUN_CONTRACT_TERMS:
            if required_term.lower() not in evals_readme_run_contract:
                errors.append(f"evals/README.md run contract must mention: {required_term}")
        eval_case_entries = evals_readme_catalog_entries(evals_readme_text, "## Case catalog")
        eval_rubric_entries = evals_readme_catalog_entries(evals_readme_text, "## Rubric catalog")
        for case in eval_cases:
            if case.stem not in eval_case_entries:
                errors.append(f"evals/README.md missing eval case catalog entry: {case.stem}")
        for case_name in eval_case_entries:
            if not (root / "evals" / "cases" / f"{case_name}.md").exists():
                errors.append(f"evals/README.md eval case catalog entry points to missing file: {case_name}")
        for rubric in sorted((root / "evals" / "rubrics").glob("*.md")):
            if rubric.stem not in eval_rubric_entries:
                errors.append(f"evals/README.md missing eval rubric catalog entry: {rubric.stem}")

    content_files = [
        *sorted((root / "docs").glob("*.md")),
        *sorted((root / "templates").glob("*.md")),
        *sorted((root / "evals" / "rubrics").glob("*.md")),
        *sorted((root / "evals").glob("README.md")),
        *sorted((root / "adapters").glob("*/README.md")),
    ]
    for markdown_file in content_files:
        if markdown_file.parent == root / "docs" and not is_lowercase_kebab(markdown_file.stem):
            errors.append(f"{rel(markdown_file, root)} filename must use lowercase kebab-case")
        single_h1_error = validate_single_h1(markdown_file, root)
        if single_h1_error:
            errors.append(single_h1_error)
        if markdown_file.parent == root / "docs":
            markdown_text = markdown_file.read_text(errors="ignore")
            expected_heading = f"# {title_from_slug(markdown_file.stem)}"
            first_line = markdown_text.splitlines()[0]
            if first_line != expected_heading:
                errors.append(f"{rel(markdown_file, root)} heading must be {expected_heading}")
            markdown_text_lower = markdown_text.lower()
            for stale_term in STALE_REPOSITORY_BOOTSTRAP_TERMS:
                if stale_term in markdown_text_lower:
                    errors.append(
                        f"{rel(markdown_file, root)} contains stale repository bootstrap instruction: {stale_term}"
                    )
        if markdown_file.parent == root / "templates" and markdown_file.name != "skill-template.md":
            expected_heading = f"# {title_from_slug(markdown_file.stem)}"
            first_line = markdown_file.read_text(errors="ignore").splitlines()[0]
            if first_line != expected_heading:
                errors.append(f"{rel(markdown_file, root)} heading must be {expected_heading}")
        if markdown_file.parent.parent == root / "adapters" and markdown_file.name == "README.md":
            expected_heading = adapter_heading_from_slug(markdown_file.parent.name)
            adapter_text = markdown_file.read_text(errors="ignore")
            adapter_text_lower = adapter_text.lower()
            first_line = adapter_text.splitlines()[0]
            if first_line != expected_heading:
                errors.append(f"{rel(markdown_file, root)} heading must be {expected_heading}")
            for required_section in REQUIRED_ADAPTER_SECTIONS:
                if required_section not in adapter_text:
                    errors.append(f"{rel(markdown_file, root)} missing adapter section: {required_section}")
            capability_matrix_body = section_body(adapter_text, "## Capability Matrix").lower()
            for required_term in REQUIRED_ADAPTER_CAPABILITY_MATRIX_TERMS:
                if required_term.lower() not in capability_matrix_body:
                    errors.append(
                        f"{rel(markdown_file, root)} capability matrix must document runtime boundary: {required_term}"
                    )
            for run_command in REQUIRED_ADAPTER_VALIDATION_COMMANDS:
                if run_command not in adapter_text:
                    errors.append(f"{rel(markdown_file, root)} validation section must document: {run_command}")
            for run_command in REQUIRED_ADAPTER_BOOTSTRAP_COMMANDS:
                if run_command.lower() not in adapter_text_lower:
                    errors.append(f"{rel(markdown_file, root)} bootstrap section must document: {run_command}")
            for required_term in REQUIRED_ADAPTER_REMOTE_FRESHNESS_TERMS:
                if required_term.lower() not in adapter_text_lower:
                    errors.append(
                        f"{rel(markdown_file, root)} bootstrap section must verify remote freshness: {required_term}"
                    )
            minimal_instruction_body = section_body(adapter_text, "## Minimal instruction")
            minimal_instruction_body_lower = minimal_instruction_body.lower()
            for artifact in REQUIRED_ADAPTER_MINIMAL_INSTRUCTION_ARTIFACTS:
                if artifact not in minimal_instruction_body:
                    errors.append(
                        f"{rel(markdown_file, root)} minimal instruction must name harness artifact: {artifact}"
                    )
            for required_term in REQUIRED_ADAPTER_COMMAND_BOUNDARY_TERMS:
                if required_term not in minimal_instruction_body_lower:
                    errors.append(
                        f"{rel(markdown_file, root)} minimal instruction must document command boundary: {required_term}"
                    )
            adapter_validation_body = section_body(adapter_text, "## Validation")
            for artifact_term in REQUIRED_ADAPTER_RUNTIME_SMOKE_ARTIFACT_TERMS:
                if artifact_term not in adapter_validation_body:
                    errors.append(
                        f"{rel(markdown_file, root)} validation section must document runtime smoke artifact contract: {artifact_term}"
                    )
            adapter_validation_body_lower = adapter_validation_body.lower()
            for evidence_term in REQUIRED_ADAPTER_RUNTIME_SMOKE_EVIDENCE_TERMS:
                if evidence_term not in adapter_validation_body_lower:
                    errors.append(
                        f"{rel(markdown_file, root)} validation section must document runtime smoke evidence field: {evidence_term}"
                    )
            for probe_term in REQUIRED_ADAPTER_SAMPLE_ROUTING_PROBE_TERMS:
                if probe_term not in adapter_validation_body_lower:
                    errors.append(
                        f"{rel(markdown_file, root)} validation must include sample request routing probe: {probe_term}"
                    )
            adapter_output_contract_body = section_body(adapter_text, "## Output Contract").lower()
            for output_term in REQUIRED_ADAPTER_OUTPUT_CONTRACT_TERMS:
                if output_term not in adapter_output_contract_body:
                    errors.append(
                        f"{rel(markdown_file, root)} output contract must document handoff field: {output_term}"
                    )

    for rubric in sorted((root / "evals" / "rubrics").glob("*.md")):
        text = rubric.read_text(errors="ignore")
        expected_heading = f"# {title_from_slug(rubric.stem)}"
        first_line = text.splitlines()[0] if text.splitlines() else ""
        lines = text.splitlines()
        if not is_lowercase_kebab(rubric.stem):
            errors.append(f"{rel(rubric, root)} filename must use lowercase kebab-case")
        if first_line != expected_heading:
            errors.append(f"{rel(rubric, root)} heading must be {expected_heading}")
        for section in REQUIRED_EVAL_RUBRIC_SECTIONS:
            section_count = lines.count(section)
            if section_count == 0:
                errors.append(f"{rel(rubric, root)} missing {section}")
            else:
                if section_count > 1:
                    errors.append(f"{rel(rubric, root)} section must appear exactly once: {section}")
                if not section_has_body(text, section):
                    errors.append(f"{rel(rubric, root)} section has no body: {section}")
        if not sections_are_in_order(text, REQUIRED_EVAL_RUBRIC_SECTIONS):
            errors.append(f"{rel(rubric, root)} sections must appear in canonical order")

    for public_copy_file in sorted(
        path for path in root.rglob("*") if path.suffix in PUBLIC_COPY_SUFFIXES
    ):
        if any(part in PUBLIC_COPY_EXCLUDED_PARTS for part in public_copy_file.parts):
            continue
        text = public_copy_file.read_text(errors="ignore")
        for line_number in find_trailing_whitespace_lines(text):
            errors.append(f"{rel(public_copy_file, root)} line {line_number} has trailing whitespace")
        for secret_name, secret_pattern in SECRET_LIKE_PATTERNS:
            if secret_pattern.search(text):
                errors.append(f"{rel(public_copy_file, root)} contains secret-like value: {secret_name}")
        for term in BANNED_PUBLIC_COPY_TERMS:
            if term.lower() in text.lower() and not public_copy_term_allowed(public_copy_file, text, term):
                errors.append(f"{rel(public_copy_file, root)} contains banned public-copy term: {term}")

        if public_copy_file.suffix == ".md":
            for link_target, link_anchor in local_markdown_link_targets(text):
                link_path = (public_copy_file.parent / link_target).resolve()
                try:
                    link_path.relative_to(root.resolve())
                except ValueError:
                    continue
                if not link_path.exists():
                    errors.append(
                        f"{rel(public_copy_file, root)} local markdown link points to missing file: {link_target}"
                    )
                    continue
                if link_anchor:
                    link_text = link_path.read_text(errors="ignore")
                    if link_anchor not in markdown_heading_anchors(link_text):
                        target_display = f"{link_target}#{link_anchor}"
                        errors.append(
                            f"{rel(public_copy_file, root)} local markdown link points to missing anchor: {target_display}"
                        )

    return errors


def main() -> int:
    errors = validate(ROOT)
    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

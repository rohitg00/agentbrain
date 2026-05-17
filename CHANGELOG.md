# Changelog

## Unreleased

### Added

- `docs/harness-effect.md`: response to recent agent-harness research showing
  that tool-output presentation shifts retrieval scores even with identical
  evidence (Sen et al., *Is Grep All You Need? How Agent Harnesses Reshape
  Agentic Search*, arXiv:2605.15184). Documents operating rules for new
  tools, parity checks across presentation modes, and the measurement
  requirement for harness changes.
- `evals/cases/tool-output-presentation.md`: forces a declared presentation
  mode (inline payload versus file artifact), a parity check across modes,
  and fail-closed conditions before a search or recall tool is exposed.
- Cross-links from `docs/agent-harness.md` (new Harness Effect section) and
  `docs/state-machine.md` (new harness-effect gate after the build/verify
  states) into the new doc and eval case.
- `scripts/harness_effect.py`: deterministic, model-agnostic parity script
  that invokes a tool once per declared presentation mode (`inline`,
  `file`), diffs retrieved evidence ids and citations across modes, and
  emits a JSON report (envelope bytes, SHA-256 envelope hashes, byte
  budget delta, parity verdict). `schemas/harness-effect-report.schema.json`
  documents the output. `evals/harness-effect/fixtures/akbp-search.json`
  ships an example wiring against the AKBP reference CLI.
  `examples/artifacts/harness-effect-report.example.json` shows a passing
  report. The script is reachable from `docs/harness-effect.md` and the
  README scripts section so harness changes earn measured evidence, not
  asserted doctrine.

## v0.2.0

Research-backed rewrite of Agent Brain into an evidence-first operating system for agents.

### Added

- Research-backed critique foundation.
- Explicit claims Agent Brain rejects.
- Non-agent alternative review.
- Rewritten constitution, principles, and anti-rationalization rules.
- Formal Agent Brain state machine.
- JSON schemas for key artifacts.
- Repository validator.
- Formal slash command specs.
- Rewritten core portable skills.
- Initial eval cases and scoring rubric.
- Initial adapters for plain markdown and runtime-specific usage.

### Changed

- Repositioned the repo from generic workflow docs to a decision-first brain layer.
- Replaced old generic skills with procedure-oriented skills that include triggers, inputs, verification, examples, and failure modes.
- Made `/brain-should-this-exist` a first-class workflow.

### Validation

- `python3 scripts/validate_repo.py` passes.
- Public copy avoids named comparison/competitor positioning.
- Commits are intentionally split by checkpoint to preserve real history.

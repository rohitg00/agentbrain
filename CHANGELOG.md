# Changelog

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

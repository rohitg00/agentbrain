# Runtime Adapters

Runtime adapters explain how a capable agent runtime should load Agent Brain without pretending every runtime has the same command, shell, approval, or artifact features.

## Adapter Catalog

- `adapters/approval-gateway-runtime/README.md` — for runtimes that can request approval before write, shell, network, or other side-effecting actions.
- `adapters/plain-markdown/README.md` — for runtimes that can read markdown files and follow command specs but do not expose native slash commands.
- `adapters/read-only-cli/README.md` — for runtimes limited to inspection, classification, and blocked-command reporting.
- `adapters/skill-runtime/README.md` — for runtimes that can load reusable skills as first-class workflow units.
- `adapters/subagent-runtime/README.md` — for runtimes that can split work across scoped workers and join their outputs through a single reviewer.

## Adapter Contract

Every adapter must define a capability matrix, command routing boundary, real-runtime smoke evidence, blocked commands, and output contract. Keep the boundary explicit: say whether `/brain-*` entries are native commands, markdown specs, mixed support, or unknown; do not invent native command support when the runtime only follows files.

Adapter validation must preserve user changes, confirm git freshness, run the local quality gate when writes and shell access are available, and capture runtime smoke evidence with `templates/runtime-smoke.md` plus `schemas/runtime-smoke.schema.json`. If a runtime cannot install dependencies, write temp files, capture a transcript, redact the transcript, or run validation, record the run as read-only smoke or blocked instead of full validation.

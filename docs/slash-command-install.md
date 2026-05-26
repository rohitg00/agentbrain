# Slash Command Install

Agent Brain should be usable as native shortcuts where a runtime supports them. The core stays documentation-first; slash commands are thin wrappers over the existing command specs.

## Product Direction

Start with installable slash commands and plugin bundles, not a background service. The service layer can come later if hooks, shared session state, editor integration, or scheduled work needs it. Today the better default is explicit runtime invocation:

- install a plugin bundle or runtime wrappers,
- type `/brain-start`, `/brain-plan`, `/brain-verify`, or another `/brain-*` command,
- let the wrapper load the matching markdown command,
- produce the required artifact and validation evidence.

## Source Of Truth

`commands/registry.json` and `commands/brain-*.md` remain the source of truth.

Runtime wrappers must not contain independent workflow logic. They must only point the agent to:

- `AGENTBRAIN.md`,
- `PRINCIPLES.md`,
- `ANTI_RATIONALIZATION.md`,
- `docs/state-machine.md`,
- the selected `commands/brain-*.md` file,
- command-listed skills,
- the required artifact template,
- the matching schema when one exists.

If a wrapper conflicts with its command file or registry entry, the agent must follow the command file, report wrapper drift, and route the fix through `/brain-verify`.

## Plugin Bundle

Generate the marketplace-ready Agent Brain plugin bundle:

```bash
python scripts/install_slash_commands.py --runtime agentbrain-plugin
```

This writes:

- `.claude-plugin/marketplace.json` for plugin marketplace discovery,
- `.agents/plugins/marketplace.json` for agent plugin marketplace discovery,
- `plugins/agentbrain/.claude-plugin/plugin.json`,
- `plugins/agentbrain/.codex-plugin/plugin.json`,
- `plugins/agentbrain/skills/agentbrain/SKILL.md`,
- `plugins/agentbrain/commands/brain-*.md`,
- `plugins/agentbrain/skills/*/SKILL.md`,
- `plugins/agentbrain/templates/*.md`,
- `plugins/agentbrain/schemas/*.json`,
- `plugins/agentbrain/AGENTBRAIN.md`, `PRINCIPLES.md`, `ANTI_RATIONALIZATION.md`, and `docs/state-machine.md`.

The plugin bundle is the preferred distribution unit for plugin-based agents because it carries command bodies and supporting harness context. Runtime-specific wrappers are compatibility surfaces for agents that support project-local command files but do not install marketplace plugins.

## Supported First Targets

### Claude Code

Generate project-local skills:

```bash
python scripts/install_slash_commands.py --runtime claude-code
```

This writes `.claude/skills/brain-*/SKILL.md`. Claude Code exposes those skills as `/brain-*` invocations when the project is loaded in Claude Code.

### Gemini CLI

Generate project-local custom commands:

```bash
python scripts/install_slash_commands.py --runtime gemini-cli
```

This writes `.gemini/commands/brain-*.toml`. Gemini CLI exposes those files as `/brain-*` invocations when the project is loaded in Gemini CLI.

### Codex

Keep Codex on the portable command path until the active Codex runtime proves custom `/brain-*` command support. Codex can still use `AGENTS.md`, `commands/registry.json`, and the command files directly. Do not claim native slash-command support from wrapper files alone.

## Validation

Regenerate wrappers after changing `commands/registry.json` or any `commands/brain-*.md` route:

```bash
python scripts/install_slash_commands.py --runtime agentbrain-plugin
python scripts/install_slash_commands.py --runtime claude-code
python scripts/install_slash_commands.py --runtime gemini-cli
python scripts/install_slash_commands.py --runtime agentbrain-plugin --check
python scripts/install_slash_commands.py --runtime claude-code --check
python scripts/install_slash_commands.py --runtime gemini-cli --check
python scripts/validate_repo.py
```

Validation must prove every committed plugin command and runtime wrapper includes the command name, command file, registry path, source-of-truth warning, command-listed skills, required artifact, schema marker, user-change preservation, stop conditions, runtime-specific boundary marker, and `/brain-verify` drift route.

## Runtime Smoke

Native command support is a runtime capability, not a repo assumption. Real runtime claims still need runtime smoke evidence with:

- runtime label and version,
- `/brain-*` command mode,
- selected command,
- loaded skills,
- transcript path,
- capability evidence,
- blocked commands,
- validation commands.

If a runtime cannot prove native command support, use markdown specs directly and mark the smoke run as markdown-spec routing.

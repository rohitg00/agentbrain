# Harness Effect

## Why this document exists

Agent Brain's central claim is that the harness around a model — commands,
skills, schemas, review gates, and tool-output contracts — does more work
than most teams credit. The right harness produces better decisions from the
same model and the same data. The wrong harness wastes good evidence.

That claim is no longer only stylistic. A 2026 study evaluated agent harnesses
on a long-memory benchmark and found two effects that survived ablation:

1. The choice of retrieval strategy interacted with harness architecture, so
   the same retrieval method could appear strong or weak depending on the
   surrounding harness.
2. The way tool output was presented to the model — inline payload versus a
   separate file the model read with grep or jq — changed end-to-end scores
   even when the retrieved evidence was identical.

Reference: Sen, Kasturi, Lumer, Gulati, Subbiah. *Is Grep All You Need? How
Agent Harnesses Reshape Agentic Search.* arXiv:2605.15184.

Agent Brain's response is not to declare a winner. It is to treat the harness
as a measurable surface and to require evidence whenever a harness change is
proposed.

## What the harness controls

A harness in this repo is the union of:

- the commands the agent is allowed to call,
- the skills loaded into each command,
- the schemas and templates that shape every produced artifact,
- the review gates that block durable side effects,
- the tools exposed to the model, including how their output is presented
  (inline payload, file artifact, streamed channel, or summarized view),
- the evals that score whether the harness improved judgment.

Any of those layers can change the same model's behavior. Tool-output
presentation is the layer the paper measured most directly; the eval case
`tool-output-presentation` makes it explicit.

## Operating rules

Use these rules whenever a new tool, skill, or command is added to the harness:

1. **Declare the presentation mode.** State whether a tool returns inline
   payloads or writes a file artifact. If it does both, declare which mode
   is the default and which is the upgrade path. Record the choice next to
   the tool definition or skill frontmatter.
2. **Prove parity across modes.** If a tool offers more than one
   presentation mode, the harness must run a parity check: same retrieved
   item ids, same citations, same lifecycle metadata. The
   `tool-output-presentation` eval enforces this gate.
3. **Treat the harness as code.** Harness changes — new skills, new
   commands, new tool wirings, new artifact schemas — go through the same
   plan, build, verify, review cycle the rest of the lifecycle uses. The
   harness is not exempt from `/brain-plan`, `/brain-review`, or
   `/brain-ship`.
4. **Measure, do not assert.** When a harness change ships, attach evidence
   that the change improved or at least did not regress agent behavior on
   a relevant eval slice. Recall, citation rate, fail-closed counts, or
   completion-without-rationalization counts are all acceptable signals.
   Vibes are not.
5. **Fail closed on silent regressions.** If a new presentation mode loses
   citations, hides lifecycle warnings, or skips budget metadata that the
   old mode exposed, reject the new mode. Convenience does not buy the
   right to strip evidence.

## What this is not

This document is not a claim that file-mode tools are universally better
than inline tools, or that one harness shape wins on every task. It is a
claim that the harness layer is now a measurable axis with published
research behind it, so harness changes earn the same scrutiny as model or
data changes.

For interop with knowledge-base protocols that expose inline-versus-file
presentation as a first-class tool parameter, see the AKBP companion
position note: `docs/HARNESS_AND_PRESENTATION.md` in the AKBP repository.

## Measurement scaffold

`scripts/harness_effect.py` runs the same tool twice over the same input
set, once per declared presentation mode, and writes a
`schemas/harness-effect-report.schema.json`-valid JSON report covering:

- the rendered command and SHA-256 envelope hash for each mode,
- envelope byte sizes (so the file-mode byte budget is concrete, not
  hand-waved),
- a parity diff over retrieved evidence ids and citation ids,
- a binary verdict that the harness can attach to a plan, review, or
  handoff artifact.

Fixtures live under `evals/harness-effect/fixtures/`. The shipped example
points at the AKBP reference CLI; substitute any tool that exposes an
`output_mode` parameter and JSON output. The script is intentionally
model-agnostic so harness changes are measurable without first wiring up
an LLM.

A runnable end-to-end example against the real AKBP CLI lives at
`examples/harness-effect/`. It ships the rendered template, the recipe to
build a throw-away knowledge base, and a committed parity report
(`examples/harness-effect/harness-effect-report.akbp-search.json`) showing
the AKBP `output_mode: file` mode preserves retrieved-id and citation
parity with `output_mode: inline` while reducing envelope bytes by roughly
30 percent on a two-result query.

Failing parity is a harness regression: a new presentation mode is not
allowed to silently drop citations or items, regardless of how much
prompt budget it saves.

## Open work

- A measured harness-on / harness-off comparison on a small task slice, so
  the central claim of this repo has numbers next to it instead of only
  doctrine.
- A noise-robustness slice that mirrors the paper's irrelevant-history
  injection, so Agent Brain's filtering behavior is tested against the
  same stressor.
- A presentation-aware extension to the `qa-evidence` and
  `agent-output-verifier` skills so they routinely check whether the tool
  output a planning step relied on came in the declared presentation mode.

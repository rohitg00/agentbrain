# Replayable Evidence

Evidence is replayable when another agent can inspect the same inputs, rerun the same command, and compare the same output artifact without private chat context.

## Required Record

For any eval, runtime smoke, scorecard, launch gate, or doctor report, capture:

- repo commit,
- command or tool invocation,
- operation mode,
- input artifact,
- output artifact,
- transcript or log path,
- environment summary,
- validation commands and results,
- schema used,
- scorecard or verdict,
- recheck trigger,
- expiry or freshness rule.

## Replay Path

1. Start from `AGENTS.md` and `commands/registry.json`.
2. Confirm the selected command still exists.
3. Open the input artifact and schema.
4. Rerun the exact command when safe.
5. Validate the output artifact against its schema.
6. Compare verdict, risks, blockers, and next actions.
7. Mark replay blocked when credentials, approvals, external state, or missing artifacts prevent reproduction.

## Artifact Chain

Use this chain when the harness itself is under test:

```text
request -> command registry -> command file -> loaded skills -> output template -> schema -> validation proof -> scorecard -> handoff
```

Runtime work adds:

```text
adapter -> operation mode -> runtime smoke -> transcript -> capability evidence -> doctor report
```

When the active runtime supports event hooks, keep hook evidence replayable by storing session-start, prompt-submit, pre-tool, and post-tool payloads as redacted artifacts. Hook evidence should name the event, tool or command, decision made, payload path, redaction status, and whether the hook blocked, allowed, or only observed the operation.

## Stop Conditions

Stop when the evidence depends on memory, screenshots without source artifacts, missing logs, private credentials, unstated runtime settings, or a command that cannot be rerun safely.

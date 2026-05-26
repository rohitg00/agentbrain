# Agent Brain Plugin Install

Add Agent Brain to the runtime plugin list with the local plugin path:

```json
{
  "plugin": ["./plugins/agentbrain"]
}
```

Restart the runtime, then run the activation test: send a vague build request and confirm the session routes through `/brain-start` before code edits.

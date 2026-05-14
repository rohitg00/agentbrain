---
name: agent-output-verifier
description: Use when agent-produced work needs a safety, evidence, and reliability check before handoff, merge, or trust.
version: 0.1.0
---

# agent-output-verifier

## Trigger

Use before trusting or handing off output produced by an autonomous or semi-autonomous agent, especially after long-running work, tool use, code generation, external calls, or multi-step planning.

Do not use as a replacement for domain review. This skill decides whether the output is safe and evidenced enough to enter the next review gate.

## Inputs

- Agent output or artifact.
- Original user request and constraints.
- Tool logs, test logs, diffs, screenshots, traces, or citations.
- List of tools the agent claimed to use.
- Allowed scope, files, commands, and side effects.
- Known secrets, private paths, or data classes that must not appear.

## Procedure

1. Restate the claimed outcome in one sentence.
2. Check for secret leakage: credentials, tokens, private URLs, keys, personal data, or connection strings.
3. Check for hallucinated tools or evidence: claimed commands, tests, APIs, files, screenshots, or links that have no supporting proof.
4. Check for unbounded loops: retry loops, background jobs, recursive scheduling, polling, or autonomous goals without stop conditions.
5. Check for skipped gates: tests not run, validation missing, review bypassed, user approval omitted, or destructive actions performed silently.
6. Check scope control: files changed, external calls made, and side effects match the request.
7. Classify the output as `pass`, `pass-with-warnings`, or `blocked`.
8. Produce a blocker list with exact evidence needed to unblock.

## Verification

- Every pass/fail statement points to evidence or says evidence is missing.
- Secrets and private data are either absent or redacted.
- Claimed tools and tests have inspectable logs or artifacts.
- Loops have measurable stop conditions.
- Side effects match the allowed scope.
- The final status is one of `pass`, `pass-with-warnings`, or `blocked`.

## Output Artifact

Produce a verifier decision with status, checked claims, evidence references, blockers, warnings, required approvals, and the smallest safe next action.

## Failure Modes

- Approving fluent but unverifiable output.
- Treating screenshots, logs, or test names as proof without checking content.
- Ignoring hidden side effects because the final summary sounds successful.
- Missing recursive automation or infinite retry behavior.
- Leaving secrets in the verification report.
- Expanding into a full code review when the needed decision is trust/block.

## Example

```markdown
Status: blocked

Claim checked: "All tests pass and deployment is ready."

Blockers:
- No test log or command output attached for the claimed passing tests.
- Deployment step is outside the allowed scope.
- Background retry worker has no stop condition.

Evidence needed to unblock:
- Test command and output.
- Scope approval for deployment.
- Retry limit or cancellation rule.
```

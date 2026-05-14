# Review Gates

Run these gates before shipping. Each gate can be a standalone agent pass.

## Product Gate

- Clear user and job-to-be-done
- Clear success metric
- Sharp v0 scope
- Kill criteria defined
- No vanity-only feature

## Design Gate

- First action obvious
- States covered: empty, loading, success, error, partial, permission denied
- Copy is understandable
- Accessibility considered
- Visual hierarchy supports the job

## Engineering Gate

- Architecture matches scope
- Data flow documented
- Edge cases listed
- Tests defined
- Observability defined
- Rollback path exists

## Security and Trust Gate

- Secrets never enter prompts or logs
- Destructive actions require confirmation
- User data boundaries documented
- External calls documented
- Abuse cases considered

## Guardrail and Approval Gate

Use this gate before any agentic workflow that can call tools, hand off work, or change state.

- Input guardrails block disallowed, irrelevant, unsafe, or too-expensive requests before the main workflow starts.
- Tool guardrails sit next to side-effecting tools and validate both arguments and results.
- Output guardrails check the final artifact before it reaches the user or another system.
- Human approval pauses before sensitive actions such as edits, cancellations, shell commands, credential use, public posting, payments, or production changes.
- Blocking guardrails are preferred when speculative execution could spend money, call tools, or create side effects before validation finishes.
- Guardrails must be tested as first-class behavior, not described only in prose.

## Agent Output Verifier Gate

Use this gate before trusting a handoff from a long-running agent, parallel agent, or autonomous workflow.

- Claimed tests, commands, files, screenshots, and links have inspectable evidence.
- Secret-like values, private data, and connection strings are absent or redacted.
- Tool use is real, allowed, and within the requested scope.
- Retry loops, background jobs, and scheduled work have explicit stop conditions.
- Production, public, destructive, or expensive side effects had approval before execution.
- Missing evidence blocks trust instead of becoming a warning-only note.

## QA Gate

- Real user journey executed
- Evidence captured
- Bugs categorized by severity
- Fixes re-verified
- Known limitations documented

## Launch Gate

- README usable by a stranger
- Install or setup steps verified
- Version and changelog updated if applicable
- Support/debug path documented
- Learning capture completed

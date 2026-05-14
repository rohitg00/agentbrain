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

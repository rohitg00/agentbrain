---
name: activity-recap
description: Use when the user needs a standup-ready summary of recent project activity from local evidence.
version: 0.1.0
---

# activity-recap

## Trigger

Use when the user asks what changed recently, what they worked on, what a team did, or needs a short standup/status recap.

Do not use when the user asks for a product roadmap, a release note, or a narrative post. Those need planning, review, or writing skills instead.

## Inputs

- Repository root or parent workspace.
- Date range or working-day window.
- Optional author filter.
- Optional branch or remote scope.
- Desired output format: bullets, grouped-by-repo, grouped-by-author, or handoff note.
- Privacy constraints: files, authors, branches, or messages to omit.

## Procedure

1. Confirm or infer the workspace root.
2. Discover repositories within the requested depth without crossing unrelated private directories.
3. Inspect local history for the requested date range and filters.
4. Group activity by repository, author, and theme.
5. Normalize commit messages into human-readable bullets without inventing intent.
6. Include file-change stats only when they clarify the work.
7. Mark repositories with no matching activity as empty only when the user asked for a full workspace scan.
8. Produce a concise recap with the inspected range and evidence summary.

## Verification

- State the date range and filters used.
- State which repositories were inspected.
- Cite commit hashes, counts, or changed-file summaries when useful.
- If no activity is found, say so and list the checked scope.
- Do not infer uncommitted work unless separately inspected and explicitly labeled.

## Failure Modes

- **Wrong author identity:** ask for or list available authors instead of guessing.
- **Shallow or stale repository:** label the result as local-only or fetch only if allowed.
- **Bad commit messages:** summarize conservatively from file paths and stats.
- **Private branch content:** respect privacy constraints and omit sensitive details.
- **Multi-repo noise:** group by repository and suppress empty projects unless requested.

## Example

```markdown
Activity recap for 2026-05-13, author filter: current Git user.

- agent-brain: hardened repository validation and added CI quality gates.
  Evidence: 5 commits inspected, tests referenced in commit messages.
- website: no matching committed activity in the inspected range.

Checked: 2 repositories under the workspace root.
```

---
name: activity-recap
description: Use when the user needs a standup-ready summary of recent project activity from local evidence.
version: 0.1.0
---

# activity-recap

Lifecycle stage: LEARN

## Trigger

Use when the user asks what changed recently, what they worked on, what a team did, or needs a short standup/status recap.

Do not use when the user asks for a product roadmap, a release note, or a narrative post. Those need planning, review, or writing skills instead.

## When not to use
Do not use when this trigger is absent; choose the command or skill that owns the requested state, artifact, and verification gate.

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

## Anti-Rationalization

| Shortcut | Rebuttal |
|---|---|
| "I remember what changed." | Recaps must come from checked local history, files, or logs, not memory. |
| "A high-level summary is enough." | Name the inspected scope and timeframe so readers can trust the boundary. |
| "No activity means nothing happened." | Say no matching committed activity was found only for the scope actually checked. |

## Verification

- State the date range and filters used.
- State which repositories were inspected.
- Cite commit hashes, counts, or changed-file summaries when useful.
- If no activity is found, say so and list the checked scope.
- Do not infer uncommitted work unless separately inspected and explicitly labeled.

## Output Artifact

Produce a concise recap that names the inspected scope, timeframe, filters, evidence checked, notable changes, empty scopes when relevant, assumptions, blockers, and the next action.

## Failure Modes

- **Wrong author identity:** ask for or list available authors instead of guessing.
- **Shallow or stale repository:** label the result as local-only or fetch only if allowed.
- **Bad commit messages:** summarize conservatively from file paths and stats.
- **Private branch content:** respect privacy constraints and omit sensitive details.
- **Multi-repo noise:** group by repository and suppress empty projects unless requested.

## Example

Trigger: user needs a recap of recent project activity. Action: inspect local commits, files, branches, and relevant logs before summarizing. Output artifact: activity recap with checked scope, blockers, and next action. Verification: cite command output, author/date filters, repositories checked, and unknowns.

```markdown
Activity recap for 2026-05-13, author filter: current Git user.

- agent-brain: hardened repository validation and added CI quality gates.
  Evidence: 5 commits inspected, tests referenced in commit messages.
- website: no matching committed activity in the inspected range.

Checked: 2 repositories under the workspace root.
```

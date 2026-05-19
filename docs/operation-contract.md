# Operation Contract

Agent Brain separates what an agent may inspect from what it may change. Use this contract before any tool call, adapter run, or handoff that could mutate files or external state.

## Operation Modes

| Mode | Allowed | Required proof | Stop condition |
| --- | --- | --- | --- |
| Read-only | Inspect files, docs, logs, schemas, commands, git metadata, and public sources. | Current command, files read, and evidence checked. | The task needs writes, credentials, approvals, or side effects. |
| Workspace-write | Edit approved repository paths and run local validation. | `git status --short`, allowed paths, validation commands, rollback command, and user-change review. | The change touches disallowed paths, user-owned work, secrets, or external systems. |
| Approval-gated | Run tools that need network, privileged access, dependency install, or write expansion. | Explicit approval, exact command, scope, expected side effect, and fallback if denied. | Approval is missing, stale, ambiguous, or narrower than the requested operation. |
| External side effect | Publish, deploy, comment publicly, send messages, spend money, call production, or mutate remote state. | Owner, approval, dry-run or preview, rollback or disablement path, and monitoring. | The side effect cannot be previewed, reverted, or tied to an accountable owner. |
| Destructive | Delete, reset, overwrite, migrate, rotate, revoke, or irreversibly transform data. | Fresh backup or rollback, exact target list, explicit approval, and second review. | Target list is inferred, broad, or mixed with unrelated files or data. |

## Write Fence

Before any write-capable operation, state:

- allowed paths,
- disallowed paths,
- user-owned files to preserve,
- rollback command,
- approval state,
- validation command.

Do not upgrade read-only smoke to full validation until the write fence exists and the runtime has proven write, shell, artifact, and blocker-reporting capabilities.

## Handoff Requirement

Every handoff that follows a write-capable or side-effect-capable operation must name the mode used, exact command or tool call, affected paths, approval evidence, validation result, rollback path, and remaining blockers.

## Failure Modes

- Treating a markdown command spec as native command support without runtime proof.
- Calling a read-only smoke run full validation.
- Editing before preserving user changes.
- Expanding from local files to network, production, or public state without approval.
- Reporting success when the operation mode blocked the required proof.

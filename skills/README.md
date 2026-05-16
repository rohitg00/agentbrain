# Skills

Agent Brain skills are small, composable, runtime-neutral operating procedures. A command chooses the state, then loads only the skills needed for the current slice. Keep the developer or maintainer in control: skills provide procedure, evidence requirements, verification, and stop conditions; they do not silently own the whole workflow.

## How to use this catalog

1. Start from the selected `/brain-*` command.
2. Load only the skills listed in that command's **Skills to load** section.
3. Follow the skill's trigger, inputs, procedure, verification, output artifact, failure modes, and example.
4. If no skill fits, do not stretch a broad skill across unrelated work. Record the gap and add the smallest new skill with validator or eval coverage.
5. Keep public copy neutral. Distill external inspiration into operator patterns instead of source-specific names or commands.

## Catalog

- [`activity-recap`](activity-recap/SKILL.md) — Use when the user needs a standup-ready summary of recent project activity from local evidence.
- [`adapter-capability-probe`](adapter-capability-probe/SKILL.md) — Use when a command, adapter, or runtime smoke depends on proving an agent runtime's capabilities before trusting command routing, writes, shell access, or validation claims.
- [`agent-output-verifier`](agent-output-verifier/SKILL.md) — Use when agent-produced work needs a safety, evidence, and reliability check before handoff, merge, or trust.
- [`ci-recovery`](ci-recovery/SKILL.md) — Use when local validation and remote workflow status must be reconciled before trust, merge, or shipment.
- [`command-routing`](command-routing/SKILL.md) — Use when an agent runtime must choose or verify a /brain-* command route from a user request, handoff, adapter transcript, or stale command catalog.
- [`context-memory`](context-memory/SKILL.md) — Use when deciding what project context should be remembered, retrieved, updated, or deliberately forgotten.
- [`design-grill`](design-grill/SKILL.md) — Use when a design needs pressure-testing for UX, information architecture, states, and accessibility.
- [`domain-language`](domain-language/SKILL.md) — Use when project vocabulary is fuzzy, overloaded, disputed, or needed before naming docs, schemas, commands, skills, code, plans, or memory.
- [`engineering-grill`](engineering-grill/SKILL.md) — Use when an engineering plan needs pressure-testing for architecture, complexity, data, risk, and operability.
- [`evidence-research`](evidence-research/SKILL.md) — Use when sources need to be converted into a claim ledger with confidence levels.
- [`intake`](intake/SKILL.md) — Use when raw intent must be captured and routed to the right next state.
- [`launch-gate`](launch-gate/SKILL.md) — Use when a launch needs a go/no-go decision with rollback and monitoring evidence.
- [`learning-capture`](learning-capture/SKILL.md) — Use when repeated wins or failures should become durable memory, wiki, or skill updates.
- [`market-grill`](market-grill/SKILL.md) — Use when a product idea needs pressure-testing against alternatives, category, urgency, and distribution.
- [`plan-slicing`](plan-slicing/SKILL.md) — Use when broad work needs to be broken into small verifiable slices.
- [`problem-grill`](problem-grill/SKILL.md) — Use when a product or feature idea needs pressure-testing against problem, user, pain, success, and timing.
- [`qa-evidence`](qa-evidence/SKILL.md) — Use when behavior needs concrete proof before review, merge, or shipment.
- [`question-ladder`](question-ladder/SKILL.md) — Use when uncertainty remains and the minimum useful sequence of questions should be asked.
- [`runtime-smoke`](runtime-smoke/SKILL.md) — Use when checking Agent Brain inside a real agent runtime or adapter before trusting harness usability.
- [`wiki-maintenance`](wiki-maintenance/SKILL.md) — Use when source-backed project knowledge needs to be created, refreshed, or corrected.

## Quality bar for new skills

- Description starts with a precise Use when trigger.
- The skill is small enough to compose with commands and other skills.
- Procedure names concrete steps, not generic advice.
- Verification is runnable or inspectable.
- Output artifact is explicit.
- Failure modes and stop conditions prevent unsafe or unverified progress.
- At least one command loads the skill, and this catalog links to it.

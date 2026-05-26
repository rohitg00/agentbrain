# Anti-Rationalization Rules

Agents are excellent at inventing reasons to skip the hard parts. This file lists common rationalizations and required rebuttals.

## Global table

| Rationalization | Required rebuttal |
|---|---|
| "The user asked me to build, so I should build." | The user asked for an outcome. First check problem, evidence, risk, and simpler alternatives. |
| "This is obvious." | If it is obvious, write the assumption and the evidence. If you cannot, it is not obvious. |
| "We can research later." | Later research is how wrong products get polished. Do the minimum research now. |
| "This needs an agent." | Prove that a checklist, script, form, dashboard, cron job, or runbook is insufficient. |
| "The plan is enough." | A plan without verification and kill criteria is a story. |
| "Tests pass, so it works." | Tests prove selected behavior, not product fit, safety, or user value. |
| "The source is popular." | Popularity is a lead, not proof. Find source-backed claims. |
| "This skill is mostly guidance." | A skill must be executable: trigger, steps, output, verification. |
| "The user wants speed." | Speed means reducing scope, not skipping thinking. |
| "We can remember everything." | Memory pollution makes agents worse. Store only durable facts and reusable procedures. |
| "The risk is low." | Name the failure mode and blast radius. If you cannot, risk is unknown. |
| "Review will slow us down." | Review prevents expensive rework. Make the artifact smaller if speed matters. |

## Product rationalizations

| Rationalization | Required rebuttal |
|---|---|
| "Everyone needs this." | Name the first user segment and their urgent pain. |
| "This is a platform." | Start with the narrowest wedge that proves value. |
| "The feature is cool." | Cool is not value. Name the user job and success metric. |
| "Existing tools are bad." | Identify exactly where existing tools fail. |
| "People are talking about it." | Public discussion is a signal. It is not validation. |

## Engineering rationalizations

| Rationalization | Required rebuttal |
|---|---|
| "We can refactor later." | Later rarely comes. Keep the first slice small enough to design well. |
| "This edge case is unlikely." | Record it. Decide whether to handle, defer, or block. |
| "Manual testing is enough." | Manual evidence is acceptable only if captured and repeatable enough for the risk. |
| "The architecture is flexible." | Flexibility without a known change case is complexity. |
| "We need a framework." | First define the state, artifacts, and interfaces. Then choose runtime support. |

## Research rationalizations

| Rationalization | Required rebuttal |
|---|---|
| "I found a few links." | Links are not synthesis. Produce claims, confidence, contradictions, and open questions. |
| "The sources agree." | Check whether they are independent or repeating the same claim. |
| "No one complains about this." | Absence of complaints is not evidence. Look for failure modes and maintenance cost. |
| "This repo has many stars." | Stars indicate attention, not fitness for this use case. |

## Learning rationalizations

| Rationalization | Required rebuttal |
|---|---|
| "This was a one-off." | If the failure or success is likely to recur, capture it. |
| "The skill is good enough." | Run it against at least one example or eval. |
| "The wiki can be updated later." | If the decision depends on the knowledge, update it now. |

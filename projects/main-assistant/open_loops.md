# Chief_of_Staff_HQ Open Loops

Updated: 2026-08-01
Project: Chief_of_Staff_HQ / Daily Operations
Purpose: Track genuine unfinished Chief of Staff work without mixing standing responsibilities, specialist implementation, operating watches, or completed history into the active queue.

## Active Open Loops

| Status | Priority | Item | Owner | Next Action | Completion / Review Condition |
|---|---|---|---|---|---|
| Active | Normal | Validate the friction-aware Daily Operating SOP through ordinary use | Chief_of_Staff_HQ | Apply the one-major-action pattern during real daily planning and note only meaningful friction, support, or completion evidence | Review after repeated ordinary-day use; close or revise when there is enough evidence to judge whether the SOP reduces cognitive load without creating another checklist |
| Active | Normal | Pilot lightweight expendable-item inventory | Chief_of_Staff_HQ | Begin with transportation access and basic necessities only; use item, amount or status remaining, restock threshold, and estimated replacement cost as the minimum useful fields | Review after ordinary use or about 30 days; retain or expand only if the pilot prevents missed transportation, emergency purchases, or essential-item runouts often enough to justify maintenance |

## Waiting Items

| Status | Priority | Dependency | Owner | Chief of Staff Follow-Through | Completion Condition |
|---|---|---|---|---|---|
| Waiting | High | Publish and verify the advisory-level quarantine repair on `origin/main` | Engineering_HQ | After Engineering reports publication, read the current GitHub file or commit and verify the live V2 source status against that durable code | GitHub `main` contains the quarantine implementation and the restarted runtime reports `REMOTE_GITHUB`, `CURRENT`, a non-null verified SHA, the valid advisory set, and the bounded quarantine map |

This waiting record is a narrow follow-through dependency. It does not transfer implementation ownership to Chief of Staff or authorize Chief of Staff to edit Engineering code.

## Current Operating Watches

These are conditions to observe, not unfinished Chief of Staff tasks:

- **Chief of Staff overload:** Watch for coordination, report intake, or follow-through silently becoming ownership of specialist work.
- **Hub ownership drift:** `LifeOS_HQ` is a meeting room. Watch for it becoming a department, backlog owner, or competing source of truth.
- **Assignment drift:** When the Hub produces a real action, verify one owner, one authoritative destination, a next action or review trigger, and a completion condition.
- **Source duplication:** Watch for the same work appearing in Trello, Todoist, GitHub, Calendar, Drive, or department files as competing detailed truth.
- **Flow Board overload:** Preserve one card maximum in Now and three maximum in Next.
- **Connector isolation:** Keep the account-linked financial connector out of `Chief_of_Staff_HQ`, `LifeOS_HQ`, and multi-connector operational chats.
- **Connector truthfulness:** Do not claim a read, write, send, schedule, application, or external action succeeded without current tool evidence.
- **Context-layer drift:** Treat chat-specific handbooks as noncanonical context mirrors. Use current-source reads, focused Sync, or full Boot when source state or authority matters.
- **Inventory scope creep:** Keep the initial inventory pilot limited to expendables and transportation access.
- **Courier authority boundary:** Transport never creates task authority, source ownership, lifecycle authority, or permission to retry.
- **Uncertain transport:** Revision 1 of `ADV-20260801-055` remains immutable `UNCERTAIN` evidence. Never reset, requeue, delete, retry, or relabel an uncertain command without explicit authority and evidence.
- **Remote-source integrity:** Production should read commit-pinned GitHub snapshots and fail closed on source-integrity failures rather than silently using the local checkout.
- **Advisory quarantine:** `ADV-20260726-053` remains visible but non-dispatchable because it lacks a V2 Courier Envelope. Quarantine creates no command and does not authorize Chief of Staff to rewrite the Maintenance-owned source.
- **Courier tab resource use:** Rob's PC cannot comfortably keep two active ChatGPT windows open. The owned courier tab may be closed when idle and created or reused for bounded nighttime automation.
- **Active-composer protection:** Automation must never overwrite or navigate away from a chat whose composer contains text.
- **Command history growth:** Keep uncertain and active evidence prominent, display newest first, and move older terminal records into bounded history without deleting required evidence or changing dispatch order.
- **Readiness telemetry noise:** Repeated identical `NOT_READY` events should eventually be deduplicated or rate-limited by Engineering, but this is not a Chief of Staff implementation task.
- **Office Leaks pause:** Preserve Rob's current pause unless he explicitly resumes it.

## Standing Responsibilities

These are enduring department duties, not open loops:

- Build a realistic daily operating picture when requested.
- Identify one major action and at most one low-friction support action.
- Reduce friction through preparation before asking Rob to act.
- Chair `LifeOS_HQ` and synthesize department perspectives.
- Receive department reports without absorbing ownership.
- Route each real action to one owning department and one authoritative destination.
- Check follow-through and close stale coordination wrappers after verified completion.
- Handle one-off daily admin and authorized light connector work.
- Process Worker intake only when authorized or requested.
- Preserve source-system boundaries and keep durable GitHub notes abstract.
- Read the current Advisory Index before making freshness-sensitive advisory claims.
- Use the V2 dashboard as visibility and diagnostics rather than competing source truth.

## External Dependencies

These items are owned elsewhere and are not duplicated as Chief of Staff implementation loops:

- `Engineering_HQ` owns V2 courier and source code, publication of the quarantine repair, command-history ordering and retention, courier-tab reuse or closure, readiness-event deduplication, tests, and technical evidence.
- `Maintenance_HQ` owns `ADV-20260726-053`, its source text, repository audit, shared governance, and any resolution of the missing V2 Courier Envelope.
- `Engineering_HQ` owns `ADV-20260728-054` and any authorized next action arising from it.
- `Finance_HQ` owns forecasting, account-linked analysis, affordability, cash timing, spending analysis, and financial judgment.
- `Business_HQ` and `Office_Leaks_HQ` own Office Leaks strategy, records, and any future resume decision.

Chief of Staff may track a narrow routed dependency or follow-through condition when another department must report back, but detailed authoritative work remains with that department.

## Recently Closed or Clarified

- 2026-08-01: `ADV-20260801-055` revision 2 was delivered to the existing Maintenance HQ conversation, visibly acknowledged, and closed by Rob's authority. Revision 1 remains preserved as terminal `UNCERTAIN` evidence.
- 2026-08-01: The V2 courier proved multi-route discovery, exact-route navigation, readiness-gated atomic begin, hardened composer delivery, and server-side `DELIVERED` acknowledgement.
- 2026-08-01: Read-only canonical GitHub advisory ingestion was validated locally. The source resolved one commit SHA, read the index and boards at that SHA, preserved existing commands, accepted valid advisories, and quarantined the legacy advisory lacking a V2 envelope.
- 2026-08-01: Clarified that new advisories should be discovered directly from GitHub without requiring Rob to pull the local repository. Manual pulls remain for installing code changes, not normal advisory ingestion.
- 2026-08-01: Clarified daytime and nighttime courier-tab operation around Rob's PC memory constraint.
- 2026-07-27: Reconciled Chief of Staff current-state references with the open Maintenance audit without creating a Chief of Staff-owned duplicate loop.
- 2026-07-23: Package F Wave 0A was reconciled as complete, including the Engineering-only Worker proof chain and the enabled read-only change watcher.
- 2026-07-22: Narrowed personal inventory to a lightweight expendables-first pilot under Chief of Staff operations.
- 2026-07-18: Completed the Chief of Staff-owned Phase Two architecture repair and clarified that LifeOS HQ is the shared meeting room rather than the department itself.

## Standing Routing Rule

If a task grows into a multi-step project, requires specialist judgment, or creates durable state in another domain, route it to the relevant owning department rather than allowing `Chief_of_Staff_HQ` to become the project junk drawer.

## Completion Standard

`Chief_of_Staff_HQ` is working correctly when Rob has a clear next action, avoidable friction is removed, department reports are synthesized without ownership drift, real assignments are routed to one owner and one authoritative destination, external actions are truthfully verified, stale coordination wrappers close cleanly, automation evidence remains trustworthy, and `LifeOS_HQ` has not created duplicate truth or administrative drag.

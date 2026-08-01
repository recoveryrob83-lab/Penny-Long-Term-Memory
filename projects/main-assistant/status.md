# Chief_of_Staff_HQ Status

Updated: 2026-08-01
Project: Chief_of_Staff_HQ / Daily Operations
Status: Active / Operational

## Current Status

`Chief_of_Staff_HQ` is operational as Rob's primary point of contact, personal-assistant headquarters, daily-operations desk, executive-function support, `LifeOS_HQ` chair, routing desk, and follow-through coordinator.

`LifeOS_HQ` remains a shared meeting room rather than a department, backlog owner, or independent authority.

## Current Phase

Operational use with a proven LifeOS V2 cross-room courier, read-only canonical GitHub advisory ingestion, advisory-level quarantine, and bounded refinement.

The friction-aware Daily Operating SOP remains active and should be evaluated through ordinary daily use rather than expanded into more process.

The eight-room architecture remains active:

- one shared meeting room: `LifeOS_HQ`;
- seven department HQs: `Chief_of_Staff_HQ`, `Maintenance_HQ`, `Engineering_HQ`, `Finance_HQ`, `Business_HQ`, `Office_Leaks_HQ`, and `Wellness_HQ`.

Departments retain their own durable GitHub ownership and drift-management responsibility. Reporting through Chief of Staff does not transfer ownership.

## Active Systems

- Chief of Staff project folder: `projects/main-assistant/`
- Hub operating contract: `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`
- Daily Operating SOP: `memory/06_DAILY_OPERATING_SOP.md`
- Trello Flow Board SOP: `coordination/TRELLO_FLOW_BOARD_SOP.md`
- Department ownership SOP: `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
- Open-loop ownership SOP: `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`
- Advisory Index: `coordination/ADVISORY_INDEX.md`
- Chief of Staff source board: `coordination/boards/main-assistant.md`
- LifeOS V2 Dashboard: local visibility, diagnostics, and bounded control
- V2 browser courier: multi-route, exact-URL, empty-composer guarded, atomic begin, delivery proof, and terminal uncertain handling
- V2 advisory source: read-only canonical GitHub snapshots pinned to one commit SHA
- Trello: raw intake and visual flow
- Todoist: Rob-facing commitments and reminders
- Calendar: timed commitments
- Gmail: communication evidence and drafts
- Drive: working records and human-facing artifacts

## Current Evidence

- Multi-route command discovery no longer depends on route readiness being established before navigation.
- The extension successfully created or used an owned background courier tab, navigated to the exact Maintenance HQ conversation, established readiness, and called `/begin` once.
- Revision 1 of `ADV-20260801-055` ended as terminal `UNCERTAIN` after an unresolved post-begin transport attempt and was not retried.
- Composer insertion, send-control selection, injected fallback execution, and bounded delivery proof were hardened.
- Revision 2 of `ADV-20260801-055` reached `DELIVERED`, Maintenance visibly confirmed receipt, Rob authorized closure, and the advisory is closed.
- Production advisory ingestion now targets `recoveryrob83-lab/Penny-Long-Term-Memory@main` directly rather than requiring a manual local pull.
- The source synchronizer resolves one SHA and reads the Advisory Index and referenced boards at that same SHA.
- Live local validation reported source state `CURRENT`, a non-null verified SHA, `ADV-20260728-054` as valid, and `ADV-20260726-053` quarantined because it lacks a V2 Courier Envelope.
- Existing commands remained unchanged through the mixed valid and quarantined snapshot.
- Source failure remains fail-closed; isolated advisory parse failures create no commands and do not block valid advisories.

## Publication Discrepancy

The live local runtime includes the advisory-level quarantine repair, but the current GitHub connector view of `main` still shows `0eeccc46df6980c62e29795e7f40c78a1d61a108` (`Read courier advisories from canonical GitHub snapshots`) as the latest code commit and does not yet show the quarantine repair commit.

Until Engineering publishes and verifies that repair on `origin/main`, the local runtime is ahead of durable repository truth.

This is an Engineering-owned publication and verification dependency, not a Chief of Staff implementation task.

## Current Operating Priorities

- Keep daily planning limited to one major action and at most one useful support action.
- Chair `LifeOS_HQ` without turning it into a department or backlog owner.
- Route each real assignment to one owner and one authoritative destination.
- Use the dashboard for orientation while preserving source-system authority.
- Treat `UNCERTAIN` as a hard stop rather than a retry invitation.
- Preserve remote GitHub source integrity and visible advisory quarantine.
- Keep nighttime automation bounded and compatible with Rob's PC memory limits.
- Preserve one owned courier tab or close it when idle; avoid tab sprawl and active-composer interference.
- Keep command history evidence while moving display toward newest-first and bounded history.
- Preserve the current Office Leaks pause unless Rob explicitly resumes it.
- Keep account-linked financial work isolated in Finance-only context.

## Current Dependencies

- `Engineering_HQ` owns publication of the quarantine repair, V2 source and courier code, command-history ordering and retention, owned-tab lifecycle, readiness-event deduplication, tests, and technical evidence.
- `Maintenance_HQ` owns `ADV-20260726-053`, its source text, repository audit, shared governance, and any resolution of the missing V2 Courier Envelope.
- `ADV-20260728-054` remains an Engineering-owned open advisory.
- `Engineering_HQ Daily Sync` remains paused until Rob explicitly resumes it.
- `Business_HQ` and `Office_Leaks_HQ` own Office Leaks strategy, records, and any future resume decision.
- `Finance_HQ` owns forecasting, account-linked analysis, affordability, cash timing, and financial judgment.

## Current Advisory State

Re-read `coordination/ADVISORY_INDEX.md` before making a freshness-sensitive claim.

At this status refresh:

- `ADV-20260801-055` is closed;
- `ADV-20260728-054` remains open for Engineering;
- `ADV-20260726-053` remains open for Maintenance but is quarantined from V2 dispatch because its source text lacks a V2 Courier Envelope.

Quarantine does not close, rewrite, promote, or transfer ownership of the source advisory.

## Operating Boundary

Use `Chief_of_Staff_HQ` for everyday operations, coordination, report intake, routing, synthesis, and follow-through.

Use `LifeOS_HQ` for shared discussion and structured department perspectives without creating an independent Hub backlog.

Trello shows capture and current attention. Todoist holds commitments. Calendar holds time. GitHub holds durable abstract state. Drive holds working records. Gmail holds communication evidence. The dashboard displays selected state.

Route project-sized work and specialist judgment to the correct owner. Chief of Staff coordinates and verifies; it does not become the project junk drawer.

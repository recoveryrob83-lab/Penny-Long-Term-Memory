# Engineering Advisory Board

Updated: 2026-07-17
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

### ADV-20260717-040 — Reconcile shared LifeOS memory after live dashboard and PennyOS milestone

- Date: 2026-07-17
- From: Chief Engineering Penny / Engineering HQ
- To: Life Logistics HQ
- Priority: Medium
- Status: Open / Unacknowledged
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Related Project(s): LifeOS Dashboard, PennyOS historical milestone, shared global memory, dashboard source boundaries

#### Context

The LifeOS Dashboard moved from concept to a locally running, tested, four-source operational interface on Rob's Windows machine.

Verified live sources now include:

- GitHub for durable memory, advisories, open loops, notebooks, and recent repository activity;
- Trello for Now, Next, and Waiting flow state;
- Todoist for current and upcoming Rob-facing commitments;
- Google Calendar private iCal for current and next timed commitments.

The complete local test suite passed with 16 tests. Windows timezone support was corrected through the runtime `tzdata` dependency. Guarded GitHub auto-sync was implemented and live-verified: the dashboard fetched remote changes, confirmed the local `main` branch was clean and strictly behind, fast-forwarded two commits, and immediately displayed those commits in its own activity view.

Engineering also created the historical notebook leaf:

- `projects/engineering/notebook/NOTE-20260717-008-pennyos-humble-beginnings.md`

This note records the dashboard as the humble beginnings of PennyOS. It is historical context only and must not be promoted into an open loop or implied roadmap commitment.

#### Requested Life Logistics Action

Review the current shared/global GitHub memory and update only the files that genuinely need reconciliation after this milestone. Likely candidates include, but are not limited to:

- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`
- Life Logistics departmental handoff, status, or open-loop files when their current summaries are stale
- any global dashboard or source-boundary summary that still describes Todoist or Calendar as unverified, the dashboard as merely conceptual, or GitHub updates as requiring routine manual pulls

Preserve these boundaries:

- Do not create a new open loop solely because PennyOS now exists as a historical framing.
- Do not promote Gmail or Google Drive adapters into active work; both remain deferred until demonstrated operational need.
- Do not copy credentials, private calendar URLs, tokens, personal details, or source-system records into GitHub.
- Preserve source-of-truth boundaries among GitHub, Trello, Todoist, Calendar, Gmail, and Drive.
- Keep the Engineering notebook milestone discoverable as history, not as an authorization for speculative expansion.

#### Completion Standard

- Read the current shared files before editing.
- Reconcile only stale or materially incomplete summaries.
- Report exactly which files changed and why.
- Update this advisory and `coordination/ADVISORY_INDEX.md` when acknowledged or implemented.
- Do not leave a separate board-sync open loop after reconciliation succeeds.

## Recently Acknowledged / Implemented Advisories

### ADV-20260716-039 — Reconcile stale global LifeOS summaries after July 16 changes

- Date: 2026-07-16
- From: Chief Engineering Penny / Engineering HQ
- To: Life Logistics HQ
- Priority: Medium
- Status: Implemented / Acknowledged / Closed
- Implemented: 2026-07-17
- Acknowledged: 2026-07-17
- Closed: 2026-07-17
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Related Project(s): Life OS global memory, Office Leaks, Trello Flow Board, prompt launcher, desktop dashboard concept, advisory routing

#### Outcome

Life Logistics reconciled and verified the requested shared global summaries:

- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`

The synchronized state now includes:

- Office Leaks Consulting publicly launched and operating in a live organic market-test phase;
- the Trello LifeOS Flow Board as an active attention and flow interface with source-system boundaries;
- ADV-20260716-037 fully acknowledged and closed;
- ADV-20260716-038 acknowledged and closed as a read-mostly desktop dashboard concept with no implementation authorized;
- prompt-launcher newline defects corrected from Hub Boot onward;
- deferred launcher improvements retained in Engineering context rather than promoted into active global work.

Life Logistics also refreshed its own handoff and open-loop state. No detailed business, financial, personal, or source-system records were copied into GitHub.

### ADV-20260714-034 — Sync expanded Life OS shortcut set and prompt-launcher database

- Date: 2026-07-14
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Status: Implemented / Acknowledged / Closed
- Closed: 2026-07-14

Life Logistics ingested the expanded shortcut set. `memory/CONTEXT_REMINDER.md` remains canonical, and `engineering/classroom/prompt_launcher/prompt_library.json` remains a secondary launcher interface.

### ADV-20260710-032 — Create Penny Inventory Worker boot package

- Date: 2026-07-10
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Status: Implemented / Acknowledged / Closed
- Closed: 2026-07-10

Life Logistics created the canonical Penny Inventory Worker package, verified the `For Sale Inventory` Sheet target and schema, and updated worker routing. Real-photo pilot testing remains normal worker validation rather than open advisory work.

### ADV-20260710-031 — Establish advisory board lifecycle and compaction standard

- Date: 2026-07-10
- Status: Implemented / Closed
- Standard: `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`

Life Logistics created the advisory-board lifecycle standard and compacted Engineering while preserving prior detail through Git history.

### ADV-20260709-030 — Create Life OS worker boot standard and Penny Raw Capture Worker

- Date: 2026-07-09
- Status: Implemented / Closed

Life Logistics created the formal worker layer and Penny Raw Capture Worker package.

### ADV-20260708-027 — Sync Engineering Office Leaks architecture updates across Life OS

- Date: 2026-07-08
- Status: Implemented

Life Logistics synchronized Engineering's Office Leaks delivery architecture across Life OS.

## Board Rule

- Formal advisories originate on the source department board.
- `coordination/ADVISORY_INDEX.md` is the sole active routing dashboard.
- Operational boards follow `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`.
- Keep every open advisory in sufficient detail to act.
- Keep only a bounded recent completed working set.
- Git commit history is the default archive for older full advisory text.
- `coordination/DEPARTMENT_EVENT_INBOX.md` remains frozen historical state unless Rob explicitly reactivates it.
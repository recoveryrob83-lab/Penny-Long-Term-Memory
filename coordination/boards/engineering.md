# Engineering Advisory Board

Updated: 2026-07-16
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

### ADV-20260716-039 — Reconcile stale global LifeOS summaries after July 16 changes

- Date: 2026-07-16
- From: Chief Engineering Penny / Engineering HQ
- To: Life Logistics HQ
- Priority: Medium
- Status: Open / Unacknowledged
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Related Project(s): Life OS global memory, Office Leaks, Trello Flow Board, prompt launcher, desktop dashboard concept, advisory routing

#### Context

Engineering's 2026-07-16 reboot found that several shared global summaries still reflect the July 11–15 state and omit meaningful later changes.

Stale or incomplete shared files include:

- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`

Relevant newer state includes:

- Office Leaks Consulting is publicly launched and operating in an organic market-test phase;
- the Trello LifeOS Flow Board is now part of the active operating interface;
- ADV-20260716-037 is fully acknowledged and closed;
- ADV-20260716-038 was consumed by Engineering as a read-mostly LifeOS desktop dashboard concept;
- prompt-launcher newline defects from Hub Boot onward were corrected;
- deferred launcher improvements are captured in Engineering notebook note `NOTE-20260716-007`.

#### Requested Life Logistics Action

Reconcile the shared global summaries with current authoritative department and coordination state. Keep the update abstract, preserve source-system boundaries, avoid duplicating detailed records, and close this advisory after the affected global files are synchronized and verified.

Engineering is routing this rather than directly rewriting shared global memory because Life Logistics owns global hygiene and cross-project audits.

## Recently Acknowledged / Implemented Advisories

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
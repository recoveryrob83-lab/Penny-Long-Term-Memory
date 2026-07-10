# Engineering Advisory Board

Updated: 2026-07-10
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

None.

## Recently Acknowledged / Implemented Advisories

### ADV-20260710-031 — Establish advisory board lifecycle and compaction standard

- Date: 2026-07-10
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: Medium / High
- Status: Implemented / Closed
- Implemented: 2026-07-10
- Closed: 2026-07-10
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Standard: `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`
- Review Record: `coordination/ADVISORY_BOARD_REVIEW_2026-07-10.md`

#### Outcome

Life Logistics created and implemented a durable advisory-board lifecycle standard.

The standard now defines:

- operational versus low-traffic boards,
- required live-board structure,
- bounded recent completed working sets,
- compaction triggers,
- compaction procedure,
- Git history as the default archive,
- optional archive-file criteria,
- closure procedure,
- source-of-truth rules,
- editing rules,
- ownership,
- and privacy boundaries.

High-use boards were reviewed. Engineering was the only board that clearly exceeded the practical compaction trigger and was compacted during this closure. Main Assistant, Business, Finance, and Office Leaks remained below the trigger and readable, so they were not compacted.

No open advisory was removed. Department Event Inbox remained untouched.

### ADV-20260709-030 — Create Life OS worker boot standard and Penny Raw Capture Worker

- Date: 2026-07-09
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High
- Status: Implemented / Closed
- Implemented: 2026-07-09
- Closed: 2026-07-10
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Source Advisory: ADV-20260709-029
- Implementation Report: `workers/penny-raw-capture/IMPLEMENTATION_REPORT.md`

#### Outcome

Life Logistics created the formal worker layer:

- `workers/README.md`
- `workers/WORKER_STANDARD.md`
- `workers/penny-raw-capture/WORKER_BOOT.md`
- `workers/penny-raw-capture/SESSION_HANDOFF.md`
- `workers/penny-raw-capture/IMPLEMENTATION_REPORT.md`

Penny Raw Capture Worker uses the canonical `Life OS Raw Capture Inbox`, verifies writes, uses Central Time timestamps, never fabricates storage success, and leaves downstream processing to Main Assistant Penny.

### ADV-20260708-027 — Sync Engineering Office Leaks architecture updates across Life OS

- Date: 2026-07-08
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Status: Implemented
- Implemented: 2026-07-08
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Source Advisory: ADV-20260708-026

#### Outcome

Life Logistics synchronized Engineering's Office Leaks delivery architecture across Life OS.

Key references:

- `projects/engineering/notebook/NOTE-20260708-005-office-leak-delivery-playbooks-v1.md`
- `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`
- Drive document `Engineering Delivery Architecture Specification - HVAC Office Cleanup`

Current delivery model combines:

1. Mechanical workflow layer: map, score, scope, sprint, verify, handoff, follow up.
2. Human-system layer: respect, rapport, internal champion, users, Aha Moment, adoption verification, relational follow-up.

### ADV-20260706-020 — Adopt Finances-only session rule

- Status: Acknowledged / Implemented

Life Logistics adopted the Finances-only session rule as an observed operating pattern, not a confirmed claim about platform internals.

### ADV-20260706-018 — Simplify the Life OS Advisory Routing System

- Status: Acknowledged / Implemented

Life Logistics simplified advisory routing to source department boards plus the Advisory Index. Department Event Inbox remains frozen historical record unless Rob explicitly reactivates it.

### ADV-20260706-017 — Adopt connector reliability operating pattern from Gemini/Drive tests

- Status: Acknowledged / Implemented

Life Logistics created `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md` for explicit connector invocation, small verified writes, waiting after safety triggers, optional Gemini Drive artifact generation, and artifact verification.

### ADV-20260705-015 — Globalize department notebook leaf routing/index standard

- Status: Acknowledged / Implemented

Life Logistics updated `coordination/DEPARTMENT_NOTEBOOKS.md` with notebook leaf folders, indexes, naming guidance, and scheduled-worker guidance.

### ADV-20260704-013 — Tighten advisory posting board rules

- Status: Acknowledged / Ingested

Life Logistics clarified that advisories live on the source department board and target departments are routed through the Advisory Index.

### ADV-20260704-012 — Connector safety-trigger avoidance rules needed

- Status: Acknowledged / Ingested

Engineering incorporated connector safety-trigger avoidance into Reliable Connector Execution Layer work.

## Board Rule

- Formal advisories originate on the source department board.
- `coordination/ADVISORY_INDEX.md` is the sole active routing dashboard.
- Operational boards follow `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`.
- Keep every open advisory in sufficient detail to act.
- Keep only a bounded recent completed working set.
- Git commit history is the default archive for older full advisory text.
- Create a separate archive only when discoverability materially requires one.
- `coordination/DEPARTMENT_EVENT_INBOX.md` remains frozen historical record unless Rob explicitly reactivates it.

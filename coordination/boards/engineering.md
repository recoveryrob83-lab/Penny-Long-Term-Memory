# Engineering Advisory Board

Updated: 2026-07-10
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

None.

## Recently Acknowledged / Implemented Advisories

### ADV-20260710-032 — Create Penny Inventory Worker boot package

- Date: 2026-07-10
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High
- Status: Implemented / Acknowledged / Closed
- Implemented: 2026-07-10
- Acknowledged: 2026-07-10
- Closed: 2026-07-10
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Engineering Notebook: `engineering/notebooks/Inventory_Worker_v1.md`
- Implementation Report: `workers/penny-inventory/IMPLEMENTATION_REPORT.md`

#### Outcome

Life Logistics created the canonical Penny Inventory Worker package under the shared worker standard.

Created:

- `workers/penny-inventory/WORKER_BOOT.md`
- `workers/penny-inventory/SESSION_HANDOFF.md`
- `workers/penny-inventory/IMPLEMENTATION_REPORT.md`

Updated:

- `workers/README.md`
- `memory/STARTUP_BOOT.md`
- relevant global handoff, open-loop, advisory, and logging files

The worker is implemented as a dedicated regular chat using durable boot files. A custom GPT is not required.

#### Canonical Resource Verified

- Sheet title: `For Sale Inventory`
- Spreadsheet ID: `1q3YCwIwKcV0fWAOvMlaolXAXuQ7ommVHEL2IGqt5jIg`
- Tab: `Inventory`
- Time zone: `America/Chicago`
- Expected 13-column schema verified
- Two existing prototype rows observed

No Sheet, folder, row, or schema was created, deleted, renamed, moved, or changed during implementation.

#### Worker Contract Preserved

Penny Inventory Worker:

- analyzes photographs uploaded directly into chat,
- identifies distinct physical sale items,
- ignores obvious background objects unless Rob explicitly includes them,
- creates one row per item,
- uses stable image references such as `IMG-0001`,
- verifies writes before claiming success,
- reports uncertain identification honestly,
- and preserves partial success when a later row fails.

The worker does not automatically price, bundle, group, write listings, publish Marketplace posts, or make sale-strategy decisions.

No further implementation work remains under this advisory. Real-photo pilot testing remains normal worker validation, not an open advisory.

### ADV-20260710-031 — Establish advisory board lifecycle and compaction standard

- Date: 2026-07-10
- Status: Implemented / Closed
- Standard: `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`
- Review Record: `coordination/ADVISORY_BOARD_REVIEW_2026-07-10.md`

Life Logistics created the advisory-board lifecycle standard, reviewed high-use boards, and compacted Engineering while preserving prior detail through Git history.

### ADV-20260709-030 — Create Life OS worker boot standard and Penny Raw Capture Worker

- Date: 2026-07-09
- Status: Implemented / Closed
- Source Advisory: ADV-20260709-029
- Implementation Report: `workers/penny-raw-capture/IMPLEMENTATION_REPORT.md`

Life Logistics created the formal worker layer and Penny Raw Capture Worker package.

### ADV-20260708-027 — Sync Engineering Office Leaks architecture updates across Life OS

- Date: 2026-07-08
- Status: Implemented
- Source Advisory: ADV-20260708-026

Life Logistics synchronized Engineering's Office Leaks delivery architecture across Life OS.

Key references:

- `projects/engineering/notebook/NOTE-20260708-005-office-leak-delivery-playbooks-v1.md`
- `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`

## Board Rule

- Formal advisories originate on the source department board.
- `coordination/ADVISORY_INDEX.md` is the sole active routing dashboard.
- Operational boards follow `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`.
- Keep every open advisory in sufficient detail to act.
- Keep only a bounded recent completed working set.
- Git commit history is the default archive for older full advisory text.
- Create a separate archive only when discoverability materially requires one.
- `coordination/DEPARTMENT_EVENT_INBOX.md` remains frozen historical record unless Rob explicitly reactivates it.

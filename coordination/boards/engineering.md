# Engineering Advisory Board

Updated: 2026-07-10
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

### ADV-20260710-032 — Create Penny Inventory Worker boot package

- Date: 2026-07-10
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High
- Status: Open / Unacknowledged
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Engineering Notebook: `engineering/notebooks/Inventory_Worker_v1.md`

#### Request

Create the canonical GitHub worker package for a new **Penny Inventory Worker** under the existing Life OS worker standard.

The worker should be implemented as a dedicated regular chat with worker boot files, not as a custom GPT requirement.

#### Required Deliverables

Create at minimum:

- `workers/penny-inventory/WORKER_BOOT.md`
- `workers/penny-inventory/SESSION_HANDOFF.md`
- `workers/penny-inventory/IMPLEMENTATION_REPORT.md`
- updates to `workers/README.md`
- any boot-routing update required by `memory/STARTUP_BOOT.md`

Use `workers/WORKER_STANDARD.md` as the governing shared contract.

#### Worker Mission

Convert uploaded photographs of physical sale items into structured inventory records in the canonical Google Sheet while preserving connector truthfulness and role boundaries.

#### Canonical Workflow

1. Receive one or more images uploaded directly into chat.
2. Identify sale items visible in each image.
3. Ignore obvious background objects unless Rob explicitly says they are for sale.
4. Produce one inventory record per sale item.
5. Use stable worker-generated image references such as `IMG-0001`; do not use temporary chat upload file tokens.
6. Append one row per item to the canonical inventory Google Sheet.
7. Use one connector append operation per item when practical.
8. Verify the resulting rows before reporting success.
9. Report the number of items captured and any uncertain identifications.

#### Canonical Operational Resources

Google Drive folder structure:

- `For Sale Items/Images/`
- `For Sale Items/Inventory/`
- `For Sale Items/Listings/`
- `For Sale Items/Archive/`

Canonical Google Sheet:

- Title: `For Sale Inventory`
- Spreadsheet ID: `1q3YCwIwKcV0fWAOvMlaolXAXuQ7ommVHEL2IGqt5jIg`
- Tab: `Inventory`
- Time zone: `America/Chicago`

Current columns:

- Timestamp
- Batch ID
- Image Reference
- Category
- Item
- Quantity
- Condition
- Confidence
- Notes
- Processed
- Listing Group
- Asking Price
- Status

#### Verified Connector Pattern

Prototype testing confirmed:

- images uploaded directly into chat can be analyzed successfully;
- Drive-hosted images are not currently a reliable direct vision input through the connector alone;
- Google Sheets `appendCells` works for one-row-per-item writes;
- stable internal image IDs work better than raw upload tokens;
- one connector call per item completed successfully;
- a final spreadsheet read can verify the completed batch.

#### Scope Boundaries

The Inventory Worker must not:

- price items unless explicitly instructed by Rob;
- decide listing groups or bundles;
- create Marketplace listings;
- make sale-strategy decisions;
- delete or overwrite existing inventory rows;
- claim success without a successful write and verification;
- fabricate brand, model, quantity, condition, or confidence.

Use `Unknown` or `Low` confidence when identification is uncertain.

#### Failure Behavior

- Distinguish image-analysis uncertainty from connector-write failure.
- If a row fails to append, report the exact failed item and do not claim the batch is complete.
- Do not repeatedly hammer the same failed connector request.
- Preserve successfully written rows and resume from the first failed item when practical.
- If the canonical Sheet cannot be accessed, stop and report the blocker rather than creating a replacement.

#### Downstream Ownership

The worker captures inventory only.

Future pricing, grouping, listing-copy generation, and Facebook Marketplace publication belong to later workers or the appropriate Business/Main Assistant workflow.

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
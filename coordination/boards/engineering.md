# Engineering Advisory Board

Updated: 2026-07-20
Project: Engineering HQ
Purpose: Canonical cross-department advisories originating from Engineering HQ.

## Open Advisories

### ADV-20260720-046 — Verify Package D operational pilot requirements

- Date: 2026-07-20
- From: Engineering HQ
- To: Engineering Worker
- Lifecycle State: OPEN
- Priority: NORMAL
- Advisory Revision: 1
- Verification Mode: IMMEDIATE_HQ
- Target Department and Owner: Engineering HQ
- Target Worker ID: `engineering_worker`
- Record Class: Bounded Engineering read-only verification
- Task Class: `engineering_read_only_verification`
- Authorization Class: `READ_ONLY`
- Authorization Source: `ROB_APPROVED_LIVE_WORKER_PILOT_20260720`
- Procedure ID: `engineering_worker_read_only_verification`
- Procedure Version: 1
- Procedure Path: `projects/engineering/procedures/engineering_worker_read_only_verification.md`
- Worker Profile Path: `projects/engineering/workers/engineering_worker.md`
- Requested Action: Read the exact Package D implementation packet and answer only the bounded verification questions.
- Parameters JSON: `{"targets":["projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md"],"verification_questions":["Does the packet identify one bounded operational ChatGPT Worker flow as the remaining useful proof?","Does the packet permit a synthetic or narrowly department-owned pilot without creating broad Worker authority?","Does the packet require one bounded operational procedure before the pilot?"]}`
- Source References JSON: `["projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md","projects/engineering/procedures/engineering_worker_read_only_verification.md","projects/engineering/workers/engineering_worker.md","coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md","coordination/WORKER_EXECUTION_CONTRACT.md"]`
- Requested Read Scopes JSON: `["memory/STARTUP_BOOT.md","coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md","coordination/WORKER_EXECUTION_CONTRACT.md","projects/engineering/DEPARTMENT_IDENTITY.md","projects/engineering/workers/engineering_worker.md","projects/engineering/procedures/engineering_worker_read_only_verification.md","coordination/boards/engineering.md","projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md"]`
- Requested Write Scopes JSON: `[]`
- Requested Tools JSON: `["GitHub"]`
- Completion Condition: Every exact target is read, all three verification questions are answered or explicitly marked unverifiable, required run-linked evidence is reported, and no writes or external actions occur.
- Review Condition: Engineering HQ performs immediate review of the Worker outcome and transport evidence.
- Closure Authority: Engineering HQ only. Closure is not delegated to the Worker.

#### Assignment

Perform revision 1 using only the named procedure and authorized sources.

Return exactly one controlled outcome:

- `IMPLEMENT` when the bounded inspection completes with the required evidence;
- `REPORT_AND_HOLD` when validation or safe inspection cannot continue;
- `ELEVATE_FOR_APPROVAL` only when broader authority or a Rob decision is required.

Do not edit or close this advisory. Do not modify the Advisory Index. Do not perform any write or external action.

## Recently Acknowledged / Implemented Advisories

### ADV-20260719-044 — Reconcile Worker filesystem, shared pointers, and Maintenance continuity

- Date: 2026-07-19
- From: Engineering HQ
- To: Life OS Maintenance HQ
- Lifecycle State: CLOSED
- Priority: HIGH
- Advisory Revision: 1
- Verification Mode: IMMEDIATE_HQ
- Controlled Outcome: IMPLEMENT
- Acknowledged: 2026-07-19
- Implemented: 2026-07-19
- Source Verified: 2026-07-19
- Closed: 2026-07-19
- Posted Board: `coordination/boards/engineering.md`
- Target Department and Owner: Life OS Maintenance HQ
- Record Class: Shared-governance reconciliation and filesystem-pointer repair

#### Outcome

Life OS Maintenance HQ reconciled the residual Worker-filesystem and continuity drift after ADV-20260719-043.

Files changed:

- `memory/00_START_HERE.md`
- `memory/01_SESSION_HANDOFF.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`
- `projects/life-logistics-hq/SESSION_HANDOFF.md`
- `projects/life-logistics-hq/status.md`
- `projects/life-logistics-hq/open_loops.md`
- `memory/02_BOOT_LOG.md`
- `coordination/boards/engineering.md`
- `coordination/ADVISORY_INDEX.md`

The repair established and verified that:

- canonical shared execution and Worker rules remain in `coordination/`;
- `memory/STARTUP_BOOT.md` remains the single coherent HQ and Worker boot entry point;
- new Worker profiles live at `projects/<department>/workers/<profile>.md`;
- root `workers/` remains compatibility-only for the Raw Capture and Inventory pilots;
- no new top-level Worker package was created;
- department-owned profiles store stable identity and authority only;
- deployment state, route availability, pause state, active or retired routing, current chat resolution, receiver state, revision deduplication, verification queues, wake suppression, and technical rollover belong to the Engineering-owned routing registry and runtime;
- Maintenance owns shared contracts, boot coherence, profile conventions, shared pointer audits, and reconciliation;
- Department HQs own Worker authority and profiles;
- the Maintenance Worker item remains a standing watch rather than a duplicate active open loop;
- the July 19 architecture change is preserved in `memory/02_BOOT_LOG.md` only, not duplicated in both architecture logs.

#### Immediate-HQ Verification

Current read-back verified every changed file and confirmed the acceptance criteria.

Inspected but unchanged:

- `memory/STARTUP_BOOT.md`
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `workers/WORKER_STANDARD.md`
- `workers/README.md`

Their current SHAs and canonical or compatibility content remained unchanged during this implementation.

No specialist Department HQ file, department Worker profile, Engineering runtime file, dashboard code, automation code, or routing-registry implementation was modified.

ADV-20260718-042 remains the authoritative Engineering advisory for receiver-side semantic validation and related runtime work. No duplicate dependency or advisory was created.

### ADV-20260717-040 — Reconcile shared LifeOS memory after live dashboard and PennyOS milestone

- Date: 2026-07-17
- Lifecycle State: CLOSED
- Implemented: 2026-07-17
- Acknowledged: 2026-07-17
- Closed: 2026-07-17
- Target Department: Life Logistics HQ

Life Logistics reconciled the requested shared summaries and local continuity after the four-source dashboard milestone. GitHub, Trello, Todoist, and Google Calendar private iCal were recorded as verified sources; guarded clean-and-strictly-behind GitHub sync was preserved; Gmail and Drive adapters remained deferred; and the PennyOS humble-beginnings note remained historical only.

### ADV-20260716-039 — Reconcile stale global LifeOS summaries after July 16 changes

- Date: 2026-07-16
- Lifecycle State: CLOSED
- Implemented: 2026-07-17
- Acknowledged: 2026-07-17
- Closed: 2026-07-17
- Target Department: Life Logistics HQ

Life Logistics reconciled shared state for the Office Leaks public launch, Trello Flow Board adoption, closed advisories, dashboard concept, prompt-launcher repairs, and deferred enhancements.

### ADV-20260714-034 — Sync expanded Life OS shortcut set and prompt-launcher database

- Date: 2026-07-14
- Lifecycle State: CLOSED
- Acknowledged: 2026-07-14
- Closed: 2026-07-14

Life Logistics ingested the expanded shortcut set. `memory/CONTEXT_REMINDER.md` remains canonical, and the launcher prompt library remains a secondary interface.

### ADV-20260710-032 — Create Penny Inventory Worker boot package

- Date: 2026-07-10
- Lifecycle State: CLOSED
- Implemented: 2026-07-10
- Acknowledged: 2026-07-10
- Closed: 2026-07-10

Life Logistics created and verified the Penny Inventory Worker pilot package. It is now a grandfathered compatibility pilot under the canonical Worker contract.

### ADV-20260710-031 — Establish advisory board lifecycle and compaction standard

- Date: 2026-07-10
- Lifecycle State: CLOSED
- Standard: `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`

Life Logistics created the advisory-board lifecycle standard and compacted Engineering while preserving prior detail through Git history.

### ADV-20260709-030 — Create Life OS worker boot standard and Penny Raw Capture Worker

- Date: 2026-07-09
- Lifecycle State: CLOSED

Life Logistics created the original formal Worker layer and Penny Raw Capture Worker pilot. The pilot is now grandfathered under the canonical shared Worker architecture.

### ADV-20260708-027 — Sync Engineering Office Leaks architecture updates across Life OS

- Date: 2026-07-08
- Lifecycle State: IMPLEMENTED

Life Logistics synchronized Engineering's Office Leaks delivery architecture across Life OS.

## Board Rule

- Formal advisories originate on the source department board.
- `coordination/ADVISORY_INDEX.md` is the sole active routing dashboard.
- Operational boards follow `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`.
- Keep every open advisory in sufficient detail to act.
- Keep only a bounded recent completed working set.
- Git commit history is the default archive for older full advisory text.
- `coordination/DEPARTMENT_EVENT_INBOX.md` remains frozen historical state unless Rob explicitly reactivates it.

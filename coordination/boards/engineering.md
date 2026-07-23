# Engineering Advisory Board

Updated: 2026-07-23
Project: Engineering HQ
Purpose: Canonical cross-department advisories originating from Engineering HQ.

## Open Advisories

### ADV-20260723-052 — Verify Chief of Staff advisory watcher destination

- Date: 2026-07-23
- From: Engineering HQ
- To: Chief of Staff HQ
- Lifecycle State: OPEN
- Priority: NORMAL
- Record Class: Read-only scheduled-watcher routing test
- Authorization Source: `ROB_COS_ADVISORY_WATCHER_DESTINATION_TEST_20260723`
- Requested Observation: The hourly Chief of Staff advisory watcher should discover this new open advisory and report it in the existing Chief of Staff HQ conversation.
- Authorized Action: Read and report this advisory only.
- Worker Dispatch Authorized: false
- HQ Wake Authorized: false
- New Chat Creation Authorized: false
- Connector Write Authorized: false
- External Action Authorized: false
- Follow-On Work Authorized: false
- Dashboard Execution Authorized: false
- Completion Condition: Rob confirms that the watcher reported `ADV-20260723-052` in the existing Chief of Staff HQ conversation without spawning a new chat or triggering any other work.
- Closure Authority: Engineering HQ after Rob confirms the observed watcher behavior.

This advisory exists solely to test watcher ownership and destination after Rob deleted the Engineering-attached task and recreated the hourly watcher from Chief of Staff HQ. It does not authorize Chief of Staff, Engineering, a Worker, the dashboard, or the watcher to create work, change priority, modify records, dispatch messages, close the advisory, or perform any action beyond the scheduled read-only report.

## Recently Acknowledged / Implemented Advisories

### ADV-20260723-051 — Prove Worker receipt through Engineering HQ wake

- Date: 2026-07-23
- Lifecycle State: CLOSED
- Priority: NORMAL
- Controlled Outcome: IMPLEMENT
- Acknowledged: 2026-07-23
- Implemented: 2026-07-23
- Source Verified: 2026-07-23
- Closed: 2026-07-23
- Target Department and Owner: Engineering HQ
- Verification Mode: IMMEDIATE_HQ
- Source Record: `projects/engineering/advisories/ADV-20260723-051.md`
- Run ID: `RUN-ADV-20260723-051-R1`
- Worker Report: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260723-051-R1/report-001.json`
- HQ Review: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260723-051-R1/hq-review-001.json`

The dashboard dispatched one bounded receipt test, ingested the immutable Worker report, woke Engineering HQ, and accepted one immutable `VERIFIED` HQ review. The run reached `HQ_VERIFIED` and became consumption-ready without Rob validation. A duplicate HQ-wake defect discovered during the test was repaired by checking immutable Git evidence before browser dispatch and adding an atomic one-shot wake claim. The repaired dashboard reconciled the existing receipt without another wake.

### ADV-20260722-049 — Prove Package E Slice 6 Rob-validation chain

- Date: 2026-07-22
- Lifecycle State: CLOSED
- Priority: NORMAL
- Controlled Outcome: IMPLEMENT
- Acknowledged: 2026-07-22
- Implemented: 2026-07-22
- Source Verified: 2026-07-23
- Closed: 2026-07-23
- Target Department and Owner: Engineering HQ
- Verification Mode: IMMEDIATE_HQ
- Run ID: `RUN-ADV-20260722-049-R1`
- Worker Report: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260722-049-R1/report-001.json`
- HQ Review: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260722-049-R1/hq-review-001.json`
- Rob Validation: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260722-049-R1/rob-validation-001.json`

The Worker completed the bounded Slice 6 inspection and immutable report. Engineering HQ verified report integrity and authority but correctly routed the final Worker-chat observation to Rob. Rob verified the exact marker `LIFEOS_ROB_OBSERVATION=SLICE6_ADV_20260722_049_VISIBLE`. The signed result became consumption-ready without response scraping, work re-execution, scope expansion, or automatic advisory closure.

### ADV-20260721-048 — Validate Package E Slice 3 immutable result outbox

- Date: 2026-07-21
- Lifecycle State: CLOSED
- Priority: NORMAL
- Controlled Outcome: IMPLEMENT
- Acknowledged: 2026-07-21
- Implemented: 2026-07-21
- Source Verified: 2026-07-23
- Closed: 2026-07-23
- Target Department and Owner: Engineering HQ
- Verification Mode: IMMEDIATE_HQ
- Run ID: `RUN-ADV-20260721-048-R1`
- Worker Report: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260721-048-R1/report-001.json`
- HQ Review: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260721-048-R1/hq-review-001.json`

The Worker created exactly one immutable schema-valid report under the narrow authorized path. Deterministic ingestion calculated the canonical checksum and advanced the existing runtime row. Engineering HQ independently verified the artifact, authority, evidence, and bounded technical findings. The immutable HQ receipt records `VERIFIED`, `ready_for_consumption: true`, and no Rob-validation requirement.

### ADV-20260720-047 — Validate Package E Slice 2 response reconciliation

- Date: 2026-07-20
- Lifecycle State: CLOSED / SUPERSEDED BY PACKAGE E COMPLETION
- Priority: NORMAL
- Controlled Outcome: ARCHITECTURE DISCOVERY PRESERVED
- Acknowledged: 2026-07-20
- Implemented Through Later Package E Slices: 2026-07-23
- Closed: 2026-07-23
- Target Department and Owner: Engineering HQ
- Final Revision: 2
- Final Run ID: `RUN-ADV-20260720-047-R2`

Revision 2 remains durable architecture-discovery evidence and was not retried. Its hydration, response-bridge, and blocking-courier findings drove the dispatch-only courier, immutable result outbox, deterministic ingester, owning-HQ review, Rob-validation, and scheduled-consumption architecture. Later bounded Package E proofs superseded the original response-reconciliation completion path. No separate work remains under this advisory.

### ADV-20260723-050 — Confirm GitHub advisory receipt in Worker chat

- Date: 2026-07-23
- Lifecycle State: CLOSED / FAILED TEST
- Closed: 2026-07-23
- Final State: `FAILED_BEFORE_WORKER_EXECUTION`

The automation pasted the wake but did not submit it. The runtime receipt was rejected because no new user turn, increased turn count, or empty composer was proven. The Worker did not execute. The advisory was closed without retry and replaced by fresh run `ADV-20260723-051` after strict dispatch-proof repair.

### ADV-20260720-046 — Verify Package D operational pilot requirements

- Date: 2026-07-20
- Lifecycle State: CLOSED
- Controlled Outcome: IMPLEMENT
- Closed: 2026-07-20

The first live Engineering Worker advisory pilot completed with canonical source loading, bounded read-only work, same-row receiver acceptance, verified `IMMEDIATE_HQ` review, and duplicate-wake suppression.

### ADV-20260719-044 — Reconcile Worker filesystem, shared pointers, and Maintenance continuity

- Date: 2026-07-19
- Lifecycle State: CLOSED
- Controlled Outcome: IMPLEMENT
- Closed: 2026-07-19

Life OS Maintenance HQ reconciled Worker filesystem, boot, ownership, and continuity boundaries while preserving Engineering ownership of technical routing and runtime state.

### ADV-20260717-040 — Reconcile shared LifeOS memory after live dashboard and PennyOS milestone

- Date: 2026-07-17
- Lifecycle State: CLOSED
- Closed: 2026-07-17

Life Logistics reconciled shared summaries after the live four-source dashboard milestone.

### ADV-20260716-039 — Reconcile stale global LifeOS summaries after July 16 changes

- Date: 2026-07-16
- Lifecycle State: CLOSED
- Closed: 2026-07-17

Life Logistics reconciled shared state for the Office Leaks launch, Trello Flow Board, dashboard concept, launcher repairs, and deferred enhancements.

### ADV-20260714-034 — Sync expanded Life OS shortcut set and prompt-launcher database

- Date: 2026-07-14
- Lifecycle State: CLOSED
- Closed: 2026-07-14

Life Logistics ingested the expanded shortcut set while preserving canonical vocabulary and the launcher database as a secondary interface.

## Board Rule

- `coordination/ADVISORY_INDEX.md` is the sole active routing dashboard.
- Open advisories remain on the source department board in sufficient detail to act.
- Engineering HQ owns the accuracy and closure of Engineering-originated advisories.
- Worker reports, dashboard state, courier receipts, HQ reviews, Rob validations, and scheduled watcher messages do not close source advisories automatically.
- Closure requires source-owner verification or Rob authorization, followed by source-board and Advisory Index reconciliation.
- Git history preserves prior full advisory text removed during board compaction.
- Lifecycle state and priority remain separate.
- No advisory creates broader Worker, connector, spending, cross-department, or recurring authority unless its exact source says so.
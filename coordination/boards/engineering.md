# Engineering Advisory Board

Updated: 2026-07-28
Project: Engineering HQ
Purpose: Canonical cross-department advisories originating from Engineering HQ.

## Open Advisories

### ADV-20260728-054 — Correct the Maintenance HQ review path for bounded-write Worker repairs

- Date: 2026-07-28
- From: Engineering_HQ under direct Rob authorization
- To: Maintenance_HQ
- Lifecycle State: OPEN
- Priority: NORMAL
- Advisory Revision: 1
- Verification Mode: SOURCE_OWNER_REVIEW
- Posted Board: `coordination/boards/engineering.md`
- Current Target Department and Owner: maintenance
- Deferred Dependent Owner: engineering
- Record Class: Maintenance-owned procedure correction with blocked Engineering runtime dependency
- Authorization Class: BOUNDED_WRITE
- Authorization Source: ROB
- Approval Reference: ROB-DIRECT-MAINTENANCE-HQ-REVIEW-V2-20260728
- Requests New Authority: true
- Requests New Spending: false
- Requests New Connector: false
- Requests Cross-Department Authority: false
- Requests Material Exception: true
- Transport Scope Change Detected: false
- Execution-Ready Worker Task: false
- Current Phase: PHASE_1_MAINTENANCE_PROCEDURE_CORRECTION
- Engineering Runtime Phase: BLOCKED / NOT AUTHORIZED FOR IMPLEMENTATION IN REVISION 1
- Related Advisory: `ADV-20260726-053`
- Related Run: `RUN-ADV-20260726-053-R1`
- Existing Worker Report: `projects/life-logistics-hq/worker-results/maintenance_worker/RUN-ADV-20260726-053-R1/report-002.json`
- Existing HQ Review: `projects/life-logistics-hq/worker-results/maintenance_worker/RUN-ADV-20260726-053-R1/hq-review-001.json`
- Requested Read Scopes JSON: `["coordination/boards/engineering.md","coordination/ADVISORY_INDEX.md","projects/life-logistics-hq/procedures/maintenance_hq_worker_review_receipt.md","projects/life-logistics-hq/procedures/maintenance_coordinated_repository_repair.md","projects/life-logistics-hq/worker-results/maintenance_worker/RUN-ADV-20260726-053-R1/report-002.json","projects/life-logistics-hq/worker-results/maintenance_worker/RUN-ADV-20260726-053-R1/hq-review-001.json","apps/lifeos-dashboard/lifeos_dashboard/data/worker-hq-review.schema.json","apps/lifeos-dashboard/lifeos_dashboard/worker_hq_review.py","apps/lifeos-dashboard/lifeos_dashboard/worker_hq_review_runtime.py"]`
- Requested Write Scopes JSON: `["projects/life-logistics-hq/procedures/maintenance_hq_worker_review_receipt.md"]`
- Requested Tools JSON: `["GitHub"]`
- Current-Phase Completion Condition: Maintenance HQ publishes procedure version 2, reads it back, and reports exact commit and checksum evidence to Engineering HQ. The procedure must support independent verification of explicitly authorized bounded-write Worker repairs without weakening integrity, authority, evidence, immutability, or ownership controls.
- Advisory Closure Condition: Remain open until the Maintenance procedure correction is source-verified, a separately authorized Engineering runtime phase supports a later immutable review attempt, and `ADV-20260726-053` reaches a valid terminal review outcome.

#### Authorized Maintenance Outcome

Maintenance HQ may update only its owned procedure at `projects/life-logistics-hq/procedures/maintenance_hq_worker_review_receipt.md` and increment the procedure version.

Procedure version 2 must:

1. permit `VERIFIED` when report integrity is valid, authority compliance is compliant, the assignment explicitly authorized bounded writes, actual writes stayed within that authority, and Maintenance HQ independently verifies the work and decisive evidence;
2. preserve the stricter read-only verification path for read-only assignments;
3. define a create-once later HQ review attempt path such as `hq-review-002.json` without overwriting, renaming, moving, deleting, or contradicting `hq-review-001.json`;
4. require exact correlation to the same run, Worker, validated report, advisory, procedure version, commit, blob, and checksum evidence;
5. prohibit Worker re-execution, report overwrite, scope expansion, advisory closure, Chief of Staff wake, Rob validation, runtime mutation, or creation of a competing ledger;
6. distinguish a procedural applicability defect from a defect in the Worker report or completed repair work;
7. state the evidence and conditions required for `ready_for_consumption: true`.

Maintenance HQ must fetch the current procedure before editing, preserve unrelated content, create the smallest useful correction, commit it, read it back, calculate or report its canonical checksum, and route the exact publication evidence back to Engineering HQ.

#### Explicit Holds

- Do not rerun `maintenance_worker`.
- Do not modify `report-001.json`, `report-002.json`, `hq-review-001.json`, `rejection-001.json`, or the current runtime row.
- Do not close or revise `ADV-20260726-053` during Phase 1.
- Do not edit application code, tests, schemas, runtime databases, browser routes, send-budget state, or automation in Phase 1.
- Engineering must not begin runtime implementation until Maintenance publishes procedure version 2 and Engineering creates a separately bounded authorization under a material revision of this advisory.
- Chief of Staff is not an owner or closeout authority for this correction.

### ADV-20260726-053 — Audit and reconcile current LifeOS repository state

- Date: 2026-07-26
- From: Engineering_HQ under direct Rob authorization
- To: Maintenance_Worker / Maintenance_HQ
- Lifecycle State: OPEN
- Priority: NORMAL
- Advisory Revision: 1
- Verification Mode: IMMEDIATE_HQ
- Posted Board: `coordination/boards/engineering.md`
- Target Department and Owner: maintenance
- Target Worker ID: maintenance_worker
- Record Class: Rob-approved coordinated repository audit and repair
- Task Class: coordinated_repository_repair
- Authorization Class: BOUNDED_WRITE
- Procedure ID: maintenance_coordinated_repository_repair
- Procedure Version: 1
- Procedure Checksum: SHA256:adcd0291acea657299796a6731f1b7003f83feec25a86ec6d3f59f25d7289699
- Authorization Source: ROB
- Approval Reference: ROB-DIRECT-COORDINATED-REPAIR-20260726
- Parameters JSON: `{"audit_roots":["memory","coordination","projects","apps","workers"],"canonical_file_classes":["current handoffs","current status files","current open-loop ledgers","current READMEs and department identities","current maps, indexes, manifests, Boot pointers, and operating summaries"],"completion_condition":"All clearly stale current canonical records inside the authorized repair roots are repaired or explicitly held, every write is read back and evidenced, and one immutable result artifact is submitted for IMMEDIATE_HQ review.","exclusions":["application code and tests","runtime databases and routes","archives and historical notebooks","immutable Worker results, HQ reviews, and Rob validations","Worker profiles and procedures","source advisory and Advisory Index during execution","deletes, renames, moves, external systems, spending, schedules, and public actions"],"repair_roots":["memory","coordination","projects"]}`
- Parameters Checksum: SHA256:4adfc35b644feecf2e54acb1ab5a8040da42e49c8cf2f062c5b1b0c147c67616
- Source References JSON: `["ROB-DIRECT-COORDINATED-REPAIR-20260726","coordination/boards/engineering.md","coordination/ADVISORY_INDEX.md","coordination/WORKER_EXECUTION_CONTRACT.md","coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md","memory/STARTUP_BOOT.md","memory/HQ_NAMING_STANDARD.md","projects/life-logistics-hq/workers/maintenance_worker.md","projects/life-logistics-hq/procedures/maintenance_coordinated_repository_repair.md","projects/life-logistics-hq/procedures/maintenance_worker_result_submission.md","projects/life-logistics-hq/procedures/maintenance_hq_worker_review_receipt.md"]`
- Requested Read Scopes JSON: `["memory","coordination","projects","apps","workers"]`
- Requested Write Scopes JSON: `["memory","coordination","projects","projects/life-logistics-hq/worker-results/maintenance_worker/RUN-ADV-20260726-053-R1/report-001.json"]`
- Requested Tools JSON: `["GitHub"]`
- Requests New Authority: true
- Requests New Spending: false
- Requests New Connector: false
- Requests Cross-Department Authority: true
- Requests Material Exception: true
- Transport Scope Change Detected: false
- Completion Condition: All clearly stale current canonical records inside the authorized repair roots were repaired or explicitly held, every write was read back and evidenced, and one immutable result artifact was submitted for IMMEDIATE_HQ review.
- Result Contract ID: lifeos_worker_result
- Result Contract Version: 1
- Result Submission Procedure ID: maintenance_worker_result_submission
- Result Submission Procedure Version: 1
- Result Owning Department: maintenance
- Result Attempt: 1
- Result Path: projects/life-logistics-hq/worker-results/maintenance_worker/RUN-ADV-20260726-053-R1/report-001.json
- Result Create Only: true
- Result Overwrite Allowed: false
- Result Work Reexecution Authorized: false
- Result Scope Expansion Authorized: false

#### Authorized Outcome

Perform one repository-wide coherence audit. Repair current canonical operational records under `memory`, `coordination`, and every department subtree under `projects` when later authoritative evidence clearly establishes that the current record is stale.

The Worker may inspect `apps` and grandfathered `workers` content for cross-reference and drift evidence but must not modify software, tests, runtime state, or legacy pilot implementation.

This is a one-run coordinated repair exception approved directly by Rob. It does not transfer ownership, create standing cross-department authority, authorize new work, or permit destructive or external actions.

The Worker must follow `maintenance_coordinated_repository_repair` version 1, submit the immutable report, and stop for `Maintenance_HQ` review. The advisory remains open until source-owner verification and explicit closeout.

## Recently Acknowledged / Implemented Advisories

### ADV-20260723-052 — Verify Chief of Staff advisory watcher destination

- Date: 2026-07-23
- From: Engineering HQ
- To: Chief of Staff HQ
- Lifecycle State: CLOSED
- Priority: NORMAL
- Final Revision: 2
- Verification Mode: N/A
- Record Class: Read-only scheduled-watcher routing test
- Controlled Outcome: DESTINATION TEST PASSED
- Source Verified: 2026-07-23
- Closed: 2026-07-23
- Closeout Authority: Rob

The hourly advisory watcher discovered `ADV-20260723-052` and reported it in the existing Chief of Staff HQ conversation. The report appeared in the intended conversation and did not create a new chat or trigger other work.

Rob confirmed the result and authorized closure on 2026-07-23. The destination test is complete, and no follow-on work remains under this advisory.

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

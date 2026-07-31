# Engineering Advisory Board

Updated: 2026-07-31
Project: Engineering HQ
Purpose: Canonical cross-department advisories originating from Engineering HQ.

## Open Advisories

### ADV-20260728-054 — Correct the Maintenance HQ review path for bounded-write Worker repairs

- Date: 2026-07-28
- From: Engineering_HQ under direct Rob authorization
- To: Engineering_HQ
- Priority: NORMAL
- Verification Mode: SOURCE_OWNER_REVIEW
- Posted Board: `coordination/boards/engineering.md`
- Current Target Department and Owner: engineering
- Deferred Dependent Owner: maintenance
- Record Class: Engineering runtime enablement for one authorized later Maintenance HQ review attempt
- Authorization Class: BOUNDED_WRITE
- Authorization Source: ROB
- Approval Reference: ROB-DIRECT-HQ-REVIEW-RESUME-RUNTIME-20260728
- Requests New Authority: true
- Requests New Spending: false
- Requests New Connector: false
- Requests Cross-Department Authority: false
- Requests Material Exception: true
- Transport Scope Change Detected: false
- Execution-Ready Worker Task: false
- Phase 1 Status: COMPLETE / SOURCE VERIFIED
- Phase 1 Procedure Path: `projects/life-logistics-hq/procedures/maintenance_hq_worker_review_receipt.md`
- Phase 1 Procedure Version: 2
- Phase 1 Procedure Commit SHA: `0fa2881e3f5e39ab16ca1e6a797ed3922c6e1399`
- Phase 1 Procedure Blob SHA: `2827bc69300bc70eb8a0dd551e501c6de397be2a`
- Phase 1 Procedure Checksum: `sha256:6b2d249c8b1581e570992aaac313e767a162b722db9531c90310a0320ae14231`
- Current Phase: PHASE_2_ENGINEERING_RUNTIME_ENABLEMENT
- Related Advisory: `ADV-20260726-053`
- Related Run: `RUN-ADV-20260726-053-R1`
- Validated Worker Report Path: `projects/life-logistics-hq/worker-results/maintenance_worker/RUN-ADV-20260726-053-R1/report-002.json`
- Validated Worker Report Commit SHA: `d9c8fef05fcb22a28c0aedd8341d186eee24dea6`
- Validated Worker Report Blob SHA: `80f2bd4ff20189b399d2ae27bbbfce987e676fe2`
- Validated Worker Report Checksum: `sha256:0f66a559072b73db3375730f73c2c3ace5f3868c051c3bf4ed2f2704f22e737e`
- Earlier HQ Review Path: `projects/life-logistics-hq/worker-results/maintenance_worker/RUN-ADV-20260726-053-R1/hq-review-001.json`
- Earlier HQ Review State: `REPAIR_REQUIRED`
- Earlier HQ Review Commit SHA: `1dbc4f23adc07d6a1ebd62cdefdbca2a5488d50d`
- Earlier HQ Review Blob SHA: `1d4dcbbef25d13206f93cdf2c42973c3c2553edb`
- Earlier HQ Review Checksum: `sha256:928da8c21aa6d903916e74a91de37496d2bf79e704340a89f933f791752af1ea`
- Authorized Later Review Attempt: 2
- Authorized Later Review Path: `projects/life-logistics-hq/worker-results/maintenance_worker/RUN-ADV-20260726-053-R1/hq-review-002.json`
- Requested Read Scopes JSON: `["coordination/boards/engineering.md","coordination/ADVISORY_INDEX.md","projects/life-logistics-hq/procedures/maintenance_hq_worker_review_receipt.md","projects/life-logistics-hq/worker-results/maintenance_worker/RUN-ADV-20260726-053-R1/report-002.json","projects/life-logistics-hq/worker-results/maintenance_worker/RUN-ADV-20260726-053-R1/hq-review-001.json","apps/lifeos-dashboard/lifeos_dashboard/__init__.py","apps/lifeos-dashboard/lifeos_dashboard/worker_hq_review.py","apps/lifeos-dashboard/lifeos_dashboard/worker_hq_review_runtime.py","apps/lifeos-dashboard/lifeos_dashboard/worker_hq_review_state_repair_runtime.py","apps/lifeos-dashboard/lifeos_dashboard/worker_github_orchestrator.py","apps/lifeos-dashboard/lifeos_dashboard/worker_github_orchestrator_runtime.py","apps/lifeos-dashboard/lifeos_dashboard/data/worker-hq-review.schema.json","apps/lifeos-dashboard/tests"]`
- Requested Write Scopes JSON: `["apps/lifeos-dashboard/lifeos_dashboard/worker_hq_review_resume_runtime.py","apps/lifeos-dashboard/lifeos_dashboard/__init__.py","apps/lifeos-dashboard/tests/test_worker_hq_review_resume_runtime.py"]`
- Requested Tools JSON: `["GitHub"]`
- Current-Phase Completion Condition: Engineering publishes and tests a guarded same-row runtime extension that verifies the exact revision-2 authorization, procedure v2 evidence, validated report evidence, and earlier immutable review evidence; permits exactly attempt 2 at the authorized create-once path; can submit at most one pointer-only Maintenance HQ review-resume wake through the existing courier and send budget; ingests only the exactly correlated immutable attempt-2 receipt; preserves earlier artifacts and evidence; and advances runtime only according to the accepted receipt.
- Advisory Closure Condition: Remain open until the runtime phase is source-verified, Maintenance HQ creates and Engineering ingests the authorized attempt-2 receipt, `ADV-20260726-053` reaches a valid terminal review outcome, and Engineering performs explicit source-owner closeout.

#### V2 Courier Envelope

- Advisory Revision: 2
- Source Department: engineering
- Target Department: engineering
- Task Summary: Correct the Maintenance HQ review path for bounded-write Worker repairs.
- Authorized Scope: Perform only the Engineering runtime enablement and verification explicitly authorized in this advisory; preserve all holds and do not execute the deferred Maintenance review.
- Lifecycle State: OPEN
- Outcome:
- Blocker:
- Updated At: 2026-07-31T14:24:00-05:00

#### Authorized Engineering Outcome

Engineering HQ may create one compatibility module, install it through the package import chain, and add focused tests under the exact write scopes above.

The runtime extension must:

1. parse and verify the exact revision-2 authorization from this source-board section rather than hardcoding a competing authority record;
2. verify the procedure v2 path, UTF-8 checksum, creation commit, and blob SHA before enabling a later review;
3. verify the existing run, validated report path, checksum, commit, and blob match the same authoritative execution row;
4. verify `hq-review-001.json` remains immutable and matches the exact `REPAIR_REQUIRED` path, state, checksum, creation commit, and blob identified above;
5. permit exactly attempt 2 at `hq-review-002.json` and reject any other attempt or path;
6. preserve attempt-1 wake and review evidence while recording attempt-2 wake and review evidence on the same `execution_history` row through additive columns or a concise same-row history field, never a second ledger;
7. atomically claim and submit at most one pointer-only attempt-2 wake to Maintenance HQ through the existing browser courier, shared run lock, and current send budget;
8. treat any post-submit uncertainty as a hard stop requiring inspection and never retry blindly;
9. validate schema, semantics, exact identity, Git immutability, one-path creation commit, and prior-review correlation before ingesting attempt 2;
10. suppress an identical duplicate attempt-2 receipt and reject conflicting evidence;
11. advance the existing row to `HQ_VERIFIED`, `HQ_REJECTED`, `REPORT_REPAIR_PENDING`, or `ROB_VALIDATION_REQUIRED` only according to the accepted attempt-2 receipt;
12. emit concise orchestrator events for review-resume wake, ingestion, duplicate suppression, refusal, and reconciliation where applicable.

#### Explicit Holds

- Do not rerun `maintenance_worker` or create a new Worker run.
- Do not modify, overwrite, rename, move, delete, or recreate `report-001.json`, `report-002.json`, `rejection-001.json`, or `hq-review-001.json`.
- Do not create `hq-review-002.json` from Engineering or before the compatible runtime is merged and visible.
- Do not manually edit SQLite or reset the send budget.
- Do not close or revise `ADV-20260726-053` during Phase 2 implementation.
- Do not wake Chief of Staff, perform Rob validation, resolve held source records, or broaden the original repair assignment.
- Maintenance HQ remains the only owner authorized to perform the later independent review and create the attempt-2 receipt after the runtime wake.

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
- Completion Condition: All clearly stale current canonical operational records inside the authorized repair roots are repaired or explicitly held, every write is read back and evidenced, and one immutable result artifact is submitted for IMMEDIATE_HQ review.
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
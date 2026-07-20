# Engineering HQ Status

Updated: 2026-07-19

## Current Phase

Active / Package D Backend and Desktop Milestone Complete / ADV-042 Receiver-Ingress Gap Identified / Next Implementation-Goal Decision Pending / Desktop Automation Reliability / Dashboard Observation / Connector Reliability / Worker Pilots / Prompt Systems / Office Leaks Delivery Architecture

## Summary

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, and build-readiness.

Engineering defines how to build safely and in the right order. Business HQ and Office Leaks HQ define what should be built and why. Finance HQ owns cost-bearing choices. Chief of Staff HQ coordinates daily operations. Life OS Maintenance HQ owns shared global memory hygiene, boot integrity, migrations, audits, source boundaries, canonical Worker governance, and cross-project reconciliation.

Engineering owns the technical implementation of the execution architecture: routing registry, stable IDs, exact-title transport, receiver validation, revision state, duplicate suppression, verification views, wake suppression, runtime evidence, and reliability mechanisms. It does not own canonical shared governance contracts or department-specific Worker authority.

## Source-of-Truth Boundaries

- GitHub: durable architecture, project state, dashboard code, automation code, and Engineering records.
- `projects/engineering/open_loops.md`: authoritative unfinished Engineering work and detailed completion ledger.
- `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md`: authoritative Package D design, implementation sequence, validation evidence, milestone receipt, current gap, and production boundary.
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`: canonical shared execution governance, owned by Life OS Maintenance HQ.
- `coordination/WORKER_EXECUTION_CONTRACT.md`: canonical Worker authority and profile convention, owned by Life OS Maintenance HQ.
- SQLite Command Center execution history: authoritative local automation-run, receiver-outcome, evidence, and verification record.
- Automation Logs and Run History: views over that same execution history, not competing log stores.
- `memory/05_OPEN_LOOPS.md`: genuinely system-owned work and operating watches only.
- Trello, Todoist, Calendar, Gmail, and Drive retain their established source roles.
- LifeOS Dashboard remains a visibility and bounded local-control layer rather than a replacement source of truth.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Current Focus

### Package D: Operations-Procedure and Worker-Runtime Implementation

Lifecycle State: Active
Priority: Normal

Status: Backend and physical desktop transport milestone complete. Engineering implemented and locally validated Slices 1–7, and Rob live-validated one bounded synthetic wrapper through ChatGPT Classic. ADV-20260718-042 remains open because receiver ingress and joined physical end-to-end validation are not yet complete.

Implemented source slices:

1. Contracts and validation.
2. SQLite registry, route, and task-scoped receiver persistence.
3. Registry service.
4. Command Center execution-envelope integration.
5. Receiver validation and controlled outcomes.
6. Verification views and wake suppression.
7. Synthetic end-to-end backend pilot with exact transport-history validation.

Bounded desktop validation files:

- `apps/lifeos-dashboard/automation/run_synthetic_worker_desktop_pilot.py`
- `apps/lifeos-dashboard/tests/test_synthetic_worker_desktop_pilot.py`
- `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`

Current capabilities:

- stable Worker identity, exact visible title, owning department, profile pointer, profile version, specialization, role, and Engineering-owned deployment state;
- separate deployment and route-availability state;
- compact JSON execution envelopes with wrapper, run, Worker, task, revision, procedure, authorization, and verification fields;
- idempotency keyed by `worker_id + task_id + task_revision`;
- exact-title zero-match and duplicate-match failure;
- task-scoped receiver state and atomic duplicate suppression;
- separate Worker Command Center jobs and results that leave ordinary HQ jobs unchanged;
- shared pause and one-job locking;
- manual and scheduler-triggered transport for one already-authorized envelope;
- successful-send suppression with bounded retry after failed transport;
- exact transport-history validation before receiver acceptance;
- semantic preflight for profile identity, ownership, exact caller authority, procedure and parameter checksums, task class, source references, scopes, tools, verification mode, and revision freshness;
- atomic receiver acceptance only after transport and semantic validation succeed;
- evidence-backed finalization with exactly one `IMPLEMENT`, `REPORT_AND_HOLD`, or `ELEVATE_FOR_APPROVAL` outcome;
- same-row machine evidence, Department HQ review, verification state, queue derivation, wake targeting, and wake suppression;
- read-only Automation Logs counters, filters, facts, evidence, and wake reasoning;
- disposable backend and desktop synthetic proofs without real authority.

Validation evidence:

- focused Slice 7 end-to-end pilot plus receiver suite: `32 passed`;
- complete dashboard regression suite reported by Rob: `222 passed, 9 warnings in 238.78s`;
- live desktop receipt: `status: succeeded`, `mode: send`, `exit_code: 0`, and `durable_authority_created: false`;
- exact acknowledgement: `SYNTHETIC_WRAPPER_RECEIVED SYNTH-DESKTOP-WRAP-1784515664-0de7866901`;
- no real Worker profile, registry entry, route, wake, schedule, UI mutation control, or durable authority was created.

### ADV-042 Read-Only Verification

Engineering completed a separate read-only verification against ADV-20260718-042.

Confirmed implementation includes:

- recognizable machine-readable envelope transport;
- complete transport metadata persistence;
- exact successful-send transport validation;
- procedure and parameter checksum validation;
- parameter schema validation;
- ownership and calling-authority validation;
- scope and tool enforcement;
- duplicate suppression;
- controlled outcomes;
- same-row evidence and verification review.

Remaining closure gaps:

1. The production path does not yet parse transported evidence and independently resolve the authoritative Worker profile, canonical procedure, and task source before constructing `ReceiverAssignment`.
2. The injected backend pilot and physical desktop transport pilot have not yet been joined into one bounded proof reaching receiver acceptance, outcome, evidence, and verification.

ADV-20260718-042 must remain open until its source owner verifies completed evidence after those gaps are resolved. Engineering must not self-close it.

### Next Implementation-Goal Decision

Rob has not yet selected the next implementation slice.

Engineering recommendation:

1. receiver ingress and canonical resolution;
2. generated human-readable envelope summary from the same `ExecutionEnvelope` object;
3. joined bounded validation and source-owner review of ADV-042;
4. only afterward consider one separately authorized department-owned Worker activation.

The recommendation is not implementation authority. Real Worker activation, recurring Worker authority generation, real wake emission, and Package E remain deferred.

### Canonical Prompt Transport Verification

Status: General investigation paused by Rob. Worker-only wrapper verification is implemented, locally test-validated, and live desktop-validated with one synthetic wrapper.

The Worker-only path retains exact destination, empty-composer protection, clipboard restoration, explicit send, and stop-on-uncertainty safeguards, then copies once and confirms the expected `wrapper_id` is present.

Do not resume full-text equality, repeated selection, character-range comparison, multiple witnesses, focus hacks, or broad timeout experiments without demonstrated failure.

### Completed Foundation

The following foundation is complete and should not be reopened without new evidence:

- department ownership architecture and read-only Department Inspection;
- fresh LifeOS HQ verification of the role-routed operating model;
- Package B canonical automation names and retired-title compatibility while preserving stable destination keys;
- Package C Department Inspection canonical labels while preserving stable scope IDs and paths;
- collapsed LifeOS project recovery;
- scheduler persistence, recurrence, overdue visibility, pause-on-failure behavior, restart policy, ledger synchronization, and cleanup controls;
- exact destination navigation, occupied-composer preservation, clipboard lifetime and restoration, explicit send authorization, one-job locking, and stop on uncertainty;
- Package D backend Slices 1–7, disposable synthetic backend pilot, and bounded synthetic desktop transport;
- ADV-20260719-044 shared Worker filesystem and continuity reconciliation by Life OS Maintenance HQ.

### Automation Command Center

Status: Implemented for the established scheduler and attended-HQ automation contract. The separate Worker backend, receiver, verification, synthetic integration, and bounded desktop transport paths are validated.

Worker integration currently adds backend services, a read-only evidence view, and a bounded script entrypoint only. It does not add Worker execution controls, create schedules, create profiles, register a real Worker, emit a real wake, or alter existing HQ prompt behavior.

Automation Logs uses the same durable execution-history rows as Run History. No second queue, wake, outcome, or verification ledger exists.

### Desktop Department and Worker Automation

Status: Operational for attended HQ use under the established safety contract. The Worker-only exact-title entrypoint is locally validated and passed a bounded live synthetic desktop send with exact wrapper acknowledgement.

Safety contract:

- exact destination matching only;
- bounded exact-project and `Show more` recovery;
- exact active-document verification;
- stable composer discovery and reacquisition;
- preserve occupied composers and the prior clipboard value;
- explicit send authorization;
- one job at a time;
- stop on uncertainty;
- never blind-retry after uncertain state;
- fail closed on missing, ambiguous, duplicate, stale, paused, or unauthorized targets;
- verify Worker writes only by the expected wrapper marker after one post-paste copy.

### LifeOS Dashboard

Application location: `apps/lifeos-dashboard/`

Verified live sources:

- GitHub;
- Trello;
- Todoist;
- Google Calendar private iCal.

Current tabs:

- Overview;
- Department Inspection;
- Automation;
- Automation Logs.

Current boundaries:

- guarded GitHub sync only fast-forwards clean, strictly-behind `main`;
- Gmail and general Drive adapters remain deferred;
- Department Inspection remains read-only;
- Automation Logs is post-run evidence, not a live streaming console;
- fully unattended Windows operation is not assumed merely because scheduling works;
- the dashboard may transport and display authorized state but may not invent, approve, prioritize, or broaden work;
- no general Worker dashboard control surface is authorized by Package D.

## Other Active Tracks

- Observe ordinary role-routed specialist boots and inspect demonstrated defects. ADV-20260719-044 implementation is complete and is no longer an active monitoring dependency.
- Observe four-source dashboard behavior during ordinary use and genuine degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real items only under its grandfathered compatibility boundary.
- Observe Penny Raw Capture Worker only under its grandfathered compatibility boundary.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline aligned with the Worker run model.
- Draft the broader operation-ledger schema and connector-health policy around the execution envelope, evidence, controlled outcomes, verification state, wake suppression, and transport integrity.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Recent Milestones

- 2026-07-19: Engineering completed a read-only ADV-20260718-042 evidence review and identified receiver-ingress resolution plus joined physical end-to-end proof as the remaining closure gaps.
- 2026-07-19: ADV-20260719-044 was implemented, source verified, and closed by Life OS Maintenance HQ.
- 2026-07-19: Package D bounded synthetic desktop transport passed exact navigation, composer verification, wrapper-marker verification, explicit send, non-authoritative receipt generation, and exact Worker acknowledgement.
- 2026-07-19: Package D first backend runtime milestone completed with Slices 1–7 locally validated.
- 2026-07-19: Slice 7 focused tests passed with 32 tests and the complete dashboard suite passed with 222 tests and 9 warnings.
- 2026-07-19: Slice 6 complete dashboard suite passed with 212 tests and 9 warnings.
- 2026-07-19: Slice 5 complete dashboard suite passed with 196 tests and 9 warnings.
- 2026-07-19: Slice 4 complete dashboard suite passed with 174 tests and 9 warnings.
- 2026-07-18: Scheduler production policy, failure pause, Resume behavior, overdue health, restart policy, ledger synchronization, and cleanup passed runtime validation.
- 2026-07-18: Department Inspection reached 414 normalized records, zero findings, and zero warnings.

Detailed state, priorities, and completion evidence remain authoritative in `projects/engineering/open_loops.md` and the Package D implementation packet.

## Production Boundary

- ChatGPT Classic must be available and responsive for UI automation.
- Failed scheduled runs pause according to validated policy rather than retrying blindly.
- Engineering HQ Daily Sync remains paused until Rob explicitly resumes it.
- Package D backend and desktop success do not authorize a real Worker, real profile, real route, real wake, recurring authority schedule, or Package E.
- Any real Worker activation requires a separate bounded decision and source-owned profile authority.
- Windows startup, desktop shell, service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, canonical shared governance, or routine cross-project memory curation.
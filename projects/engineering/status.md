# Engineering HQ Status

Updated: 2026-07-19

## Current Phase

Active / Package D Backend and Desktop Milestone Complete and Worker Activation Decision Gate, Desktop Automation Reliability, Dashboard Observation, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture

## Summary

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, and build-readiness.

Engineering defines how to build safely and in the right order. Business HQ and Office Leaks HQ define what should be built and why. Finance HQ owns cost-bearing choices. Chief of Staff HQ coordinates daily operations. Life OS Maintenance HQ owns shared global memory hygiene, boot integrity, migrations, audits, source boundaries, canonical Worker governance, and cross-project reconciliation.

Engineering owns the technical implementation of the new execution architecture: routing registry, stable IDs, exact-title transport, receiver validation, revision state, duplicate suppression, verification queues, wake suppression, runtime evidence, and reliability mechanisms. It does not own the canonical shared governance contracts or department-specific Worker authority.

## Source-of-Truth Boundaries

- GitHub: durable architecture, project state, dashboard code, automation code, and Engineering records.
- `projects/engineering/open_loops.md`: authoritative unfinished Engineering work and detailed completion ledger.
- `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md`: authoritative Package D build sequence, v1 technical decisions, validation evidence, milestone receipt, and activation boundary.
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`: canonical shared execution governance, owned by Life OS Maintenance HQ.
- `coordination/WORKER_EXECUTION_CONTRACT.md`: canonical Worker authority and profile convention, owned by Life OS Maintenance HQ.
- SQLite Command Center execution history: authoritative local automation-run, receiver-outcome, evidence, and verification record.
- Automation Logs and Run History: dashboard views over that same execution history, not competing log stores.
- `memory/05_OPEN_LOOPS.md`: genuinely system-owned work and operating watches only.
- Trello, Todoist, Calendar, Gmail, and Drive retain their established source roles.
- LifeOS Dashboard remains a visibility and bounded local-control layer rather than a replacement source of truth.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Current Focus

### Package D: Operations-Procedure and Worker-Runtime Implementation

Status: Backend and physical desktop transport milestone complete. Engineering implemented and locally validated Slices 1–7, then Rob live-validated one bounded synthetic wrapper through ChatGPT Classic. The next step is a bounded activation decision, not automatic real-Worker deployment.

Implemented and locally validated source slices:

1. Contracts and validation:
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime.py`
   - `apps/lifeos-dashboard/tests/test_worker_runtime.py`
2. SQLite registry, route, and receiver persistence:
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime_store.py`
   - `apps/lifeos-dashboard/tests/test_worker_runtime_store.py`
3. Registry service:
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime_service.py`
   - `apps/lifeos-dashboard/tests/test_worker_runtime_service.py`
4. Command Center execution-envelope integration:
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_command_center.py`
   - `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`
   - `apps/lifeos-dashboard/tests/test_worker_command_center.py`
5. Receiver validation and controlled outcomes:
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver_models.py`
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver_store.py`
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver.py`
   - `apps/lifeos-dashboard/tests/test_worker_receiver.py`
6. Verification views and wake suppression:
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_verification.py`
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_verification_runtime.py`
   - `apps/lifeos-dashboard/lifeos_dashboard/static/tabs.js`
   - `apps/lifeos-dashboard/lifeos_dashboard/static/automation-logs.js`
   - `apps/lifeos-dashboard/lifeos_dashboard/static/automation-logs.css`
   - `apps/lifeos-dashboard/tests/test_worker_verification.py`
   - `apps/lifeos-dashboard/tests/test_worker_verification_runtime.py`
   - `apps/lifeos-dashboard/tests/test_automation_logs_ui.py`
7. Synthetic end-to-end pilot:
   - `apps/lifeos-dashboard/tests/test_worker_end_to_end_pilot.py`
   - transport-integrity hardening in `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver.py`
   - transport-integrity hardening in `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver_store.py`

Bounded desktop validation files:

- `apps/lifeos-dashboard/automation/run_synthetic_worker_desktop_pilot.py`
- `apps/lifeos-dashboard/tests/test_synthetic_worker_desktop_pilot.py`
- existing `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`

Current capabilities:

- stable `worker_id`, exact `chat_title`, department, profile path, profile version, specialization, role, and Engineering-owned deployment state;
- `enabled`, `paused`, and `retired` deployment states;
- separate `available`, `unavailable`, `ambiguous`, and `unknown` route observation;
- department-owned profile-path enforcement;
- compact JSON execution envelopes with wrapper, run, Worker, task, revision, procedure, authorization, and verification fields;
- idempotency keyed by `worker_id + task_id + task_revision`;
- exact-title zero-match and duplicate-match failure;
- task-scoped receiver state so unrelated advisory revisions cannot suppress one another;
- atomic stale-revision and duplicate suppression;
- route and deployment checks before acceptance;
- thin service methods for registration, lookup, deployment changes, route updates, validation, and acceptance;
- a separate Worker Command Center job and result path that leaves ordinary HQ jobs unchanged;
- shared Command Center pause and one-job locking;
- manual and scheduler-triggered execution methods for one already-authorized envelope;
- successful-send suppression by idempotency key while failed sends remain eligible for bounded retry;
- nullable Worker metadata in the existing execution-history table;
- persisted wrapper, run, Worker, task, revision, procedure, authorization, idempotency, verification-mode, trigger, controlled-outcome, and verification-review fields;
- Worker-only exact-title transport using one copied-text check for the expected wrapper ID after paste;
- receiver transport-integrity validation requiring exactly one successful Worker send whose wrapper, Worker, task, revision, procedure, authorization, idempotency, and verification metadata exactly match the assignment;
- semantic receiver preflight that validates profile identity, owning department, exact caller authority, canonical procedure and checksum, parameter schema and checksum, source references, requested scopes, approved tools, verification mode, pause state, and revision freshness;
- atomic receiver acceptance only after transport and semantic validation both succeed;
- evidence-backed finalization that distinguishes transport success, accepted work, completed work, verified work, partial work, holds, and approval elevations;
- exactly one persisted controlled outcome: `IMPLEMENT`, `REPORT_AND_HOLD`, or `ELEVATE_FOR_APPROVAL`;
- derived `pending`, `verified`, and `rejected` verification states without a competing queue table or service;
- separate machine-evidence and Department HQ review semantics in the same history row;
- queue eligibility, wake target, and wake suppression derived without emitting a real wake;
- read-only Automation Logs counters, filters, Worker facts, outcome evidence, and wake reasoning;
- one disposable synthetic backend pipeline proving the Slices 1–6 machinery works together without creating real authority;
- one successful bounded desktop wrapper proving exact ChatGPT Classic navigation, stable composer acquisition, wrapper-marker verification, explicit submission, receipt generation, and exact semantic acknowledgement.

Validation evidence:

- the four focused Worker-runtime files passed with `36 passed`;
- the first Slice 4 full regression run reached `172 passed` with two narrow guidance-string assertion failures;
- Engineering repaired only the required `Open Automation Logs` and `Nothing was sent` wording contracts;
- both focused regressions passed;
- the Slice 4 full dashboard suite passed with `174 passed, 9 warnings in 173.76s`;
- the focused Slice 5 receiver suite passed with `22 passed`;
- the Slice 5 full dashboard suite passed with `196 passed, 9 warnings in 191.97s`;
- the focused Slice 6 Worker verification/runtime/Automation Logs suite passed with `20 passed`;
- the Slice 6 full dashboard suite passed with `212 passed, 9 warnings in 198.41s`;
- the focused Slice 7 end-to-end pilot plus receiver regression suite passed with `32 passed`;
- Rob reported the complete dashboard regression suite passed with `222 passed, 9 warnings in 238.78s`;
- Slices 1–7 are locally validated with no remaining functional regression;
- Rob reported live desktop receipt `status: succeeded`, `mode: send`, `exit_code: 0`, and `durable_authority_created: false` for wrapper `SYNTH-DESKTOP-WRAP-1784515664-0de7866901`;
- the synthetic Worker returned exact acknowledgement `SYNTHETIC_WRAPPER_RECEIVED SYNTH-DESKTOP-WRAP-1784515664-0de7866901`.

Synthetic pilot evidence:

- zero exact-title match failed closed;
- duplicate exact-title match failed closed;
- paused Worker and unavailable route refused before transport;
- missing wrapper witness failed transport and could not consume a revision;
- corrupted persisted wrapper metadata failed receiver validation;
- unauthorized write scope recorded `REPORT_AND_HOLD` without consuming a revision;
- one successful synthetic transport became `READY`, then exactly one `IMPLEMENT` outcome with same-row evidence and verification review;
- a retry with a new `run_id` could not re-execute the accepted task revision;
- a second controlled outcome was refused;
- all backend synthetic runtime state remained in temporary test databases and fixtures;
- the live desktop exercise created no profile, registry entry, route record, wake, schedule, or durable authority.

ADV-20260718-042 remains open and authoritative until its source owner verifies the implemented receiver behavior and current evidence. Engineering must not duplicate or self-close it.

Required next decision:

1. stop at the validated backend-and-desktop milestone and gather evidence from the grandfathered pilots; or
2. select at most one candidate department-owned Worker for a separately authorized profile and activation review;
3. require one owner, profile path, task class, verification mode, scope, lifecycle state, priority, and completion/review condition before any real registry write;
4. keep real wake emission, recurring Worker authority generation, and Package E deferred unless separately approved.

### Canonical Prompt Transport Verification

Status: General investigation paused by Rob. Worker-only wrapper verification is implemented, locally test-validated, and live desktop-validated with one synthetic wrapper.

Do not resume the prior general composer investigation. The historical catalog, selector, and Automation Logs work remains useful infrastructure, but full-text equality, repeated selection, character-range comparison, and multiple write witnesses are not part of v1.

The Worker-only path:

- retains exact destination, empty-composer, clipboard-restoration, explicit-send, and stop-on-uncertainty safeguards;
- copies the composer once after paste;
- confirms the copied text contains the expected `wrapper_id`;
- otherwise fails closed.

This boundary does not authorize further composer experimentation without demonstrated failure.

### Completed Foundation

The following foundation is complete and should not be reopened without new evidence:

- department ownership architecture and read-only Department Inspection;
- fresh LifeOS HQ verification of the role-routed operating model;
- Package B canonical automation names and retired-title compatibility while preserving stable destination keys;
- Package C Department Inspection canonical labels while preserving stable scope IDs and paths;
- collapsed LifeOS project recovery;
- scheduler persistence, recurrence, overdue visibility, pause-on-failure behavior, restart policy, ledger synchronization, and cleanup controls;
- exact destination navigation, occupied-composer preservation, clipboard lifetime and restoration, explicit send authorization, one-job locking, and stop on uncertainty;
- Package D backend Slices 1–7, disposable synthetic integration pilot, and bounded synthetic desktop transport.

### Automation Command Center

Status: Implemented for the established scheduler and attended-HQ automation contract. The separate Worker backend, receiver, verification, synthetic integration, and bounded desktop transport paths are validated.

Existing HQ capabilities remain:

- eight exact HQ destinations;
- canonical, saved, and custom prompt sources;
- protected canonical prompts and editable saved copies;
- saved-prompt destination mismatch safeguards;
- draft or explicitly confirmed send mode;
- one-job-at-a-time lock and global pause;
- persistent SQLite execution history;
- one-time, daily, weekly, and bounded five-minute debug schedules in `America/Chicago`;
- schedule create, edit, pause, resume, run, cleanup, and delete controls;
- separate Scheduled Jobs, Run History, and Automation Logs views;
- secret-protected no-billing Scheduler Ledger synchronization through the bound Apps Script endpoint.

Worker integration currently adds backend services, a read-only evidence view, and a bounded script entrypoint only. It does not add Worker execution controls, create schedules, create profiles, register a real Worker, emit a real wake, or alter existing HQ prompt behavior. The scheduler adapter accepts one already-authorized execution-ready envelope; recurring Worker authority generation remains out of scope.

Automation Logs uses the same durable execution-history rows as Run History. Slices 4–7 add nullable Worker transport, receiver, evidence, outcome, review, verification, queue, and wake-decision metadata or derived fields to that existing record. No second queue or wake ledger exists.

### Desktop Department and Worker Automation

Status: Operational for attended HQ use and validated recovery under the established safety contract. The Worker-only exact-title entrypoint is locally test-validated and passed a bounded live synthetic desktop send with exact wrapper acknowledgement.

Safety contract:

- exact destination matching only;
- bounded exact-project and `Show more` recovery;
- exact active-document verification;
- stable Group composer discovery and reacquisition;
- preserve occupied composers and the prior clipboard value;
- explicit send authorization;
- one job at a time;
- stop on uncertainty;
- never blind-retry after an uncertain state;
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

- Windows timezone support uses `tzdata`;
- guarded GitHub sync only fast-forwards clean, strictly-behind `main`;
- Gmail and general Drive adapters remain deferred;
- Department Inspection remains read-only;
- Automation Logs is post-run evidence, not a live streaming console;
- fully unattended Windows operation is not assumed merely because scheduling works;
- the dashboard may transport and display authorized state but may not invent, approve, prioritize, or broaden work;
- no general Worker dashboard control surface is authorized by Package D;
- Slice 6 added read-only filtered verification and wake-decision views over existing evidence, not a competing authority or queue record.

## Other Active Tracks

- Monitor ADV-20260719-044 while Life OS Maintenance repairs shared Worker pointers, profile-state ambiguity, global and Maintenance handoffs, and architecture history.
- Observe ordinary role-routed specialist boots and inspect demonstrated defects, including role identity and source-board selection.
- Observe four-source dashboard behavior during ordinary use and genuine degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real items only under its existing grandfathered compatibility boundary.
- Observe Penny Raw Capture Worker in real use only under its existing grandfathered compatibility boundary.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline aligned with the Worker run model.
- Draft the broader operation-ledger schema and connector-health policy around the new execution envelope, execution-history evidence, controlled outcomes, verification states, wake suppression, transport-integrity validation, and live desktop receipt.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Recent Milestones

- 2026-07-19: Package D bounded synthetic desktop transport passed: exact Life OS Worker chat navigation, stable composer verification, wrapper-marker copy verification, explicit send, exit code 0, non-authoritative receipt, and exact Worker acknowledgement.
- 2026-07-19: Package D first backend runtime milestone completed: Slices 1–7 locally validated, including a disposable synthetic end-to-end pilot and exact transport-history validation before receiver acceptance.
- 2026-07-19: Slice 7 locally validated: 32 focused end-to-end pilot and receiver tests passed; the complete dashboard suite passed with 222 tests and 9 warnings in 238.78 seconds.
- 2026-07-19: Slice 7 exposed and repaired a cross-slice transport gap: receiver acceptance now requires one successful Worker send with exact matching envelope metadata.
- 2026-07-19: Package D Slice 6 locally validated: 20 focused Worker verification/runtime/Automation Logs tests passed and the complete dashboard suite passed with 212 tests and 9 warnings in 198.41 seconds.
- 2026-07-19: Package D Slice 6 committed: same-row verification state, Department HQ review semantics, queue and wake derivation, Command Center status enrichment, and read-only Automation Logs visibility.
- 2026-07-19: Package D Slice 5 locally validated: 22 focused receiver tests passed and the complete dashboard suite passed with 196 tests and 9 warnings in 191.97 seconds.
- 2026-07-19: Package D Slice 5 committed: semantic receiver preflight, atomic revision acceptance, existing-history evidence persistence, and controlled outcome finalization.
- 2026-07-19: Package D Slice 4 locally validated: 36 focused Worker-runtime tests passed; after two narrow guidance-string repairs, the complete dashboard suite passed with 174 tests and 9 warnings in 173.76 seconds.
- 2026-07-19: Package D Slice 4 committed: separate Worker Command Center jobs/results, exact-title envelope transport, shared pause and one-job locking, manual and scheduler-triggered methods, successful-send idempotency suppression, existing execution-history metadata, and Worker-only one-copy wrapper verification.
- 2026-07-19: Rob reported the Slice 1–3 focused Worker tests and full dashboard suite passed locally.
- 2026-07-19: Package D implementation packet created and Slices 1–3 committed: Worker contracts, exact-title and envelope validation, separate SQLite registry/route/receiver persistence, task-scoped revision suppression, and registry service.
- 2026-07-19: Rob ended the full-text composer-verification investigation; Worker send verification uses one copied-text check for the expected wrapper ID plus existing destination, empty-composer, and send-authorization safeguards.
- 2026-07-19: ADV-20260719-044 issued from Engineering HQ to Life OS Maintenance HQ for shared Worker filesystem, pointer, profile-state, handoff, watch, and architecture-history reconciliation.
- 2026-07-19: Canonical shared execution and Worker protocols adopted; Engineering read-only Sync established operations-procedure runtime implementation as the current front burner.
- 2026-07-19: Ordinary chat operation exposed a role-identity failure in which Engineering HQ identified itself as Business HQ and nearly selected the wrong advisory source board; the incident remains validation evidence under the department-ownership architecture loop.
- 2026-07-18: Dedicated Automation Logs tab and authoritative execution telemetry implemented, including stable run IDs, safe context, backend events, complete captured stdout/stderr, copyable records, useful timeout guidance, and exception trace capture.
- 2026-07-18: Scheduler production policy, failed-run pause, Resume rearm, stale one-time restart behavior, ledger health, recurrence, cleanup, and collapsed-project recovery passed runtime validation.
- 2026-07-18: Package C canonical Department Inspection labels passed local dashboard validation and focused tests.
- 2026-07-18: Package B canonical automation mappings and retired-title compatibility passed runtime validation while preserving stable keys and persisted records.
- 2026-07-18: Department Inspection reached 414 normalized records, zero findings, and zero warnings.

Detailed state, priorities, and completion evidence remain authoritative in `projects/engineering/open_loops.md` and the Package D implementation packet.

## Production Boundary

- ChatGPT Classic must be available and responsive for UI automation.
- Failed scheduled runs pause according to the validated policy rather than retrying blindly.
- Engineering HQ Daily Sync remains paused by deliberate operating choice until Rob explicitly resumes it.
- Package D backend and desktop success do not authorize a real Worker, real profile, real route, real wake, recurring authority schedule, or Package E.
- Any real-Worker activation requires a separate bounded decision and source-owned profile authority.
- Windows startup, desktop shell, service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, canonical shared governance, or routine cross-project memory curation.
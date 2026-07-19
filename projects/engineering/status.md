# Engineering HQ Status

Updated: 2026-07-19

## Current Phase

Active / Package D Operations-Procedure and Worker-Runtime Implementation, Receiver Validation, Desktop Automation Reliability, Dashboard Observation, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture

## Summary

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, and build-readiness.

Engineering defines how to build safely and in the right order. Business HQ and Office Leaks HQ define what should be built and why. Finance HQ owns cost-bearing choices. Chief of Staff HQ coordinates daily operations. Life OS Maintenance HQ owns shared global memory hygiene, boot integrity, migrations, audits, source boundaries, canonical Worker governance, and cross-project reconciliation.

Engineering owns the technical implementation of the new execution architecture: routing registry, stable IDs, exact-title transport, receiver validation, revision state, duplicate suppression, verification queues, wake suppression, runtime evidence, and reliability mechanisms. It does not own the canonical shared governance contracts or department-specific Worker authority.

## Source-of-Truth Boundaries

- GitHub: durable architecture, project state, dashboard code, automation code, and Engineering records.
- `projects/engineering/open_loops.md`: authoritative unfinished Engineering work and detailed completion ledger.
- `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md`: authoritative Package D build sequence and v1 technical decisions.
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`: canonical shared execution governance, owned by Life OS Maintenance HQ.
- `coordination/WORKER_EXECUTION_CONTRACT.md`: canonical Worker authority and profile convention, owned by Life OS Maintenance HQ.
- SQLite Command Center execution history: authoritative local automation-run record.
- Automation Logs and Run History: dashboard views over that same execution history, not competing log stores.
- `memory/05_OPEN_LOOPS.md`: genuinely system-owned work and operating watches only.
- Trello, Todoist, Calendar, Gmail, and Drive retain their established source roles.
- LifeOS Dashboard remains a visibility and bounded local-control layer rather than a replacement source of truth.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Current Focus

### Package D: Operations-Procedure and Worker-Runtime Implementation

Status: Active. The canonical LifeOS execution and Worker protocols are in place. Engineering has implemented the first four bounded backend slices required to enforce them.

Implemented source slices:

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

Current capabilities in source:

- stable `worker_id`, exact `chat_title`, department, profile path, profile version, specialization, role, and Engineering-owned deployment state;
- `enabled`, `paused`, and `retired` deployment states;
- separate `available`, `unavailable`, `ambiguous`, and `unknown` route observation;
- department-owned profile-path enforcement;
- compact execution envelopes with wrapper, run, Worker, task, revision, procedure, authorization, and verification fields;
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
- persisted wrapper, run, Worker, task, revision, procedure, authorization, idempotency, verification-mode, trigger, and future outcome fields;
- Worker-only exact-title transport using one copied-text check for the expected wrapper ID after paste.

Test evidence:

- The combined Slice 1–3 focused suite contains 25 tests.
- Rob reported that the requested Slice 1–3 focused tests and full dashboard suite passed in the local checkout.
- Slice 4 adds 11 focused tests and is pending Rob's focused and full local validation.
- No runtime integration is treated as fully validated until those new tests and the full suite pass.

ADV-20260718-042 remains open and authoritative for receiver-side semantic validation. It is a component of Package D and should not be duplicated.

Required next implementation step:

1. Run the four focused Worker-runtime test files.
2. Run the full dashboard test suite.
3. If both pass, implement Slice 5 receiver-side profile, authority, scope, parameter, duplicate, and verification-mode validation.
4. Persist exactly one controlled outcome: `IMPLEMENT`, `REPORT_AND_HOLD`, or `ELEVATE_FOR_APPROVAL`.
5. Keep Worker UI, real profile activation, recurring Worker authority generation, and Package E deferred.

### Canonical Prompt Transport Verification

Status: General investigation paused by Rob. Worker-only wrapper verification is implemented in source.

Do not resume the prior general composer investigation. The historical catalog, selector, and Automation Logs work remains useful infrastructure, but full-text equality, repeated selection, character-range comparison, and multiple write witnesses are not part of v1.

The Worker-only path now:

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
- exact destination navigation, occupied-composer preservation, clipboard lifetime and restoration, explicit send authorization, one-job locking, and stop on uncertainty.

### Automation Command Center

Status: Implemented for the established scheduler and attended-HQ automation contract. A separate Worker backend execution path is now implemented in source and pending local validation.

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

Worker integration currently adds backend services only. It does not add Worker UI, create schedules, create profiles, register a real Worker, or alter existing HQ prompt behavior. The scheduler adapter accepts one already-authorized execution-ready envelope; recurring Worker authority generation remains out of scope.

Automation Logs uses the same durable execution-history rows as Run History. Slice 4 adds nullable Worker metadata to that existing table. Display and verification filtering for those fields remains Slice 6.

### Desktop Department and Worker Automation

Status: Operational for attended HQ use and validated recovery under the established safety contract. The Worker-only exact-title entrypoint is implemented in source and pending test validation.

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
- no Worker dashboard surface is authorized before backend validation and the synthetic pilot.

## Other Active Tracks

- Monitor ADV-20260719-044 while Life OS Maintenance repairs shared Worker pointers, profile-state ambiguity, global and Maintenance handoffs, and architecture history.
- Observe ordinary role-routed specialist boots and inspect demonstrated defects, including role identity and source-board selection.
- Observe four-source dashboard behavior during ordinary use and genuine degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline aligned with the Worker run model.
- Draft the broader operation-ledger schema and connector-health policy around the new execution envelope and execution-history evidence.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Recent Milestones

- 2026-07-19: Package D Slice 4 committed: separate Worker Command Center jobs/results, exact-title envelope transport, shared pause and one-job locking, manual and scheduler-triggered methods, successful-send idempotency suppression, existing execution-history metadata, and Worker-only one-copy wrapper verification. Eleven focused tests await local validation.
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
- Do not begin Package E or unrelated automation-surface expansion while Package D runtime integration remains active.
- Do not activate a speculative real Worker before the synthetic end-to-end pilot passes.
- Do not create recurring Worker authority schedules until a correct task-generation model is separately approved.
- Windows startup, desktop shell, service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, canonical shared governance, or routine cross-project memory curation.
# Engineering HQ Status

Updated: 2026-07-20

## Current Phase

Active / Package D Technical Milestone Complete / Operational ChatGPT Worker Model Clarified / Next Implementation-Goal Decision Pending / Desktop Automation Reliability / Dashboard Observation / Connector Reliability / Worker Pilots / Prompt Systems / Office Leaks Delivery Architecture

## Summary

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, and build-readiness.

Engineering defines how to build safely and in the right order. Business HQ and Office Leaks HQ define what should be built and why. Finance HQ owns cost-bearing choices. Chief of Staff HQ coordinates daily operations. Life OS Maintenance HQ owns shared global memory hygiene, boot integrity, migrations, audits, source boundaries, canonical Worker governance, and cross-project reconciliation.

Engineering owns technical Worker infrastructure: routing registry, stable IDs, exact-title transport, revision state, duplicate suppression, verification views, wake suppression, runtime evidence, and reliability mechanisms. It does not own canonical shared governance contracts, department-specific Worker authority, or the Worker’s domain judgment.

## Source-of-Truth Boundaries

- GitHub: durable architecture, project state, dashboard code, automation code, Worker profiles and procedures under their owning departments, and Engineering records.
- `projects/engineering/open_loops.md`: authoritative unfinished Engineering work and detailed completion ledger.
- `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md`: authoritative Package D technical design, validation evidence, operational Worker model, and production boundary.
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`: canonical shared execution governance, owned by Life OS Maintenance HQ.
- `coordination/WORKER_EXECUTION_CONTRACT.md`: canonical Worker authority and profile convention, owned by Life OS Maintenance HQ.
- SQLite Command Center execution history: authoritative local automation-run, transport, outcome, evidence, and verification record.
- Automation Logs and Run History: views over that same execution history, not competing log stores.
- Trello, Todoist, Calendar, Gmail, and Drive retain their established source roles.
- LifeOS Dashboard remains a visibility and bounded local-control layer rather than a replacement source of truth.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Canonical Worker Operating Model

A Life OS Worker is a specialized ChatGPT room operating beneath one Department HQ.

The Department HQ owns its profile, procedures, authority, and judgment. GitHub holds canonical durable state. The Worker reads the required sources, validates the assignment, performs only authorized work, and returns one controlled outcome with evidence. Department HQ reviews the result.

Python, desktop automation, SQLite, and the dashboard support delivery, exact routing, logging, duplicate suppression, safety checks, evidence, and visibility. They are not the Worker and do not replace the Worker’s operational reasoning or Department HQ ownership.

## Current Focus

### Package D: Operations-Procedure and Worker-Runtime Implementation

Lifecycle State: Active
Priority: Normal

Status: Seven technical slices and a bounded desktop transport milestone are complete. The next decision is operational: define and test how a specialized ChatGPT Worker receives an envelope, reads canonical GitHub sources, validates authority and scope, returns a controlled outcome, and reports evidence.

Implemented technical slices:

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

Validation evidence:

- focused Slice 7 end-to-end pilot plus receiver suite: `32 passed`;
- complete dashboard regression suite reported by Rob: `222 passed, 9 warnings in 238.78s`;
- live desktop receipt: `status: succeeded`, `mode: send`, `exit_code: 0`, and `durable_authority_created: false`;
- exact acknowledgement: `SYNTHETIC_WRAPPER_RECEIVED SYNTH-DESKTOP-WRAP-1784515664-0de7866901`;
- no real Worker profile, registry entry, route, wake, schedule, UI mutation control, or durable authority was created.

### ADV-042 Current Interpretation

ADV-20260718-042 explicitly assigns different responsibilities:

- the automation layer is the courier and preserves bounded delivery, correlation, transport evidence, and duplicate protection;
- the receiving Worker recognizes the wrapper, resolves the canonical prompt or procedure, validates parameters, authority, ownership, scope, and source boundaries, and returns `IMPLEMENT`, `ELEVATE_FOR_APPROVAL`, or `REPORT_AND_HOLD`.

For the intended Life OS architecture, the receiving Worker is the specialized ChatGPT Worker room.

Existing Python receiver classes and tests provide useful technical contracts and defense-in-depth validation. They do not create a requirement for an autonomous Python process to interpret all GitHub profiles, procedures, and tasks before a Worker can operate.

The prior conclusion that Package D necessarily required a production Python receiver-ingress and canonical-resolution service is withdrawn as an overextension of the technical model.

### Remaining Operational Evidence

ADV-042 remains open under its source owner. The remaining evidence should demonstrate one bounded ChatGPT Worker flow:

1. the Worker receives and recognizes the envelope;
2. the Worker loads its department-owned profile and named canonical procedure or prompt from GitHub;
3. the Worker validates version, parameters, authority, ownership, scope, and source boundaries;
4. the Worker refuses corrupted, unknown, unauthorized, ownership-conflicted, or scope-expanding work;
5. the Worker returns exactly one controlled outcome with run-linked evidence;
6. transport history and Department HQ review verify the result;
7. duplicate execution and silent scope expansion remain prevented.

A deeper Python source resolver should be considered only if this pilot demonstrates a concrete reliability, security, or scale problem that the operational procedure and current infrastructure do not cover.

### Next Implementation-Goal Decision

Rob has not yet selected the next implementation slice.

Engineering recommendation:

1. operational Worker execution procedure and canonical GitHub source-resolution contract;
2. one bounded synthetic or narrowly department-owned ChatGPT Worker pilot;
3. evidence review against ADV-042 and source-owner closure decision;
4. human-readable envelope summary before the first real Worker activation;
5. additional Python enforcement only after demonstrated need.

The recommendation is not implementation authority. Real Worker activation, recurring Worker authority generation, real wake emission, and Package E remain deferred.

### Canonical Prompt Transport Verification

Status: General investigation paused by Rob. Worker-only wrapper verification is implemented, locally test-validated, and live desktop-validated with one synthetic wrapper.

The Worker-only path retains exact destination, empty-composer protection, clipboard restoration, explicit send, and stop-on-uncertainty safeguards, then copies once and confirms the expected `wrapper_id` is present.

Do not resume full-text equality, repeated selection, character-range comparison, multiple witnesses, focus hacks, or broad timeout experiments without demonstrated failure.

### Completed Foundation

The following foundation is complete and should not be reopened without new evidence:

- department ownership architecture and read-only Department Inspection;
- fresh LifeOS HQ verification of the role-routed operating model;
- Package B canonical automation names and retired-title compatibility;
- Package C Department Inspection canonical labels;
- collapsed LifeOS project recovery;
- scheduler persistence, recurrence, overdue visibility, pause-on-failure behavior, restart policy, ledger synchronization, and cleanup controls;
- exact destination navigation, occupied-composer preservation, clipboard restoration, explicit send authorization, one-job locking, and stop on uncertainty;
- Package D backend Slices 1–7, disposable synthetic backend pilot, and bounded synthetic desktop transport;
- ADV-20260719-044 shared Worker filesystem and continuity reconciliation by Life OS Maintenance HQ.

### Automation Command Center

Status: Implemented for the established scheduler and attended-HQ automation contract. The Worker technical backend, synthetic integration, and bounded desktop transport paths are validated.

Worker integration currently adds backend services, transport and evidence infrastructure, a read-only evidence view, and a bounded script entrypoint. It does not add general Worker execution controls, create schedules, create profiles, register a real Worker, emit a real wake, or alter existing HQ prompt behavior.

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

- Observe ordinary role-routed specialist boots and inspect demonstrated defects.
- Observe four-source dashboard behavior during ordinary use and genuine degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real items only under its grandfathered compatibility boundary.
- Observe Penny Raw Capture Worker only under its grandfathered compatibility boundary.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline aligned with the Worker run model.
- Draft the broader operation-ledger schema and connector-health policy around the execution envelope, evidence, controlled outcomes, verification state, wake suppression, and transport integrity.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Recent Milestones

- 2026-07-20: Rob clarified that a Life OS Worker is a specialized Department-owned ChatGPT room, not an autonomous Python worker process; Engineering reconciled its current records accordingly.
- 2026-07-19: ADV-20260719-044 was implemented, source verified, and closed by Life OS Maintenance HQ.
- 2026-07-19: Package D bounded synthetic desktop transport passed exact navigation, composer verification, wrapper-marker verification, explicit send, non-authoritative receipt generation, and exact Worker acknowledgement.
- 2026-07-19: Package D first backend runtime milestone completed with Slices 1–7 locally validated.
- 2026-07-19: Slice 7 focused tests passed with 32 tests and the complete dashboard suite passed with 222 tests and 9 warnings.
- 2026-07-18: Scheduler production policy, failure pause, Resume behavior, overdue health, restart policy, ledger synchronization, and cleanup passed runtime validation.
- 2026-07-18: Department Inspection reached 414 normalized records, zero findings, and zero warnings.

Detailed state, priorities, and completion evidence remain authoritative in `projects/engineering/open_loops.md` and the Package D implementation packet.

## Production Boundary

- ChatGPT Classic must be available and responsive for UI automation.
- Failed scheduled runs pause according to validated policy rather than retrying blindly.
- Engineering HQ Daily Sync remains paused until Rob explicitly resumes it.
- Python transport and validation infrastructure must not drift into autonomous domain ownership or independent authority.
- Package D technical success does not authorize a real Worker, real profile, real route, real wake, recurring authority schedule, or Package E.
- Any real Worker activation requires a separate bounded decision and source-owned profile authority.
- Windows startup, desktop shell, service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, canonical shared governance, routine cross-project memory curation, or the domain judgment assigned to Department-owned ChatGPT Workers.
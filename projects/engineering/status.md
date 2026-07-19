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

Status: Active. The canonical LifeOS execution and Worker protocols are now in place. Engineering is translating them into build-ready schemas, runtime state, transport behavior, validation logic, tests, and dashboard controls.

Current implementation scope:

- Worker routing registry with stable `worker_id`, exact visible `chat_title`, department, profile path, role, and Engineering-owned deployment state;
- exact-title resolution with fail-closed zero-match and duplicate-match behavior;
- machine-readable execution envelopes and receiver-side semantic validation under ADV-20260718-042;
- prompt ID, prompt version, canonical checksum, parameter schema, authorization, ownership, and source-boundary validation;
- persistent `run_id`, advisory revision, receiver state, and duplicate suppression;
- direct one-wake execution-ready routing;
- verification modes, routine verification queues, immediate-HQ routing, and wake suppression;
- hold, elevation, resume, rejection, implementation, source-verification, and closure transitions;
- operation-ledger evidence tied to the authoritative advisory or task;
- safe Worker rename, title change, and rollover behavior;
- technical enforcement without moving policy ownership into Engineering or the dashboard.

ADV-20260718-042 remains open and authoritative for receiver-side semantic validation. It is a component of Package D and should not be duplicated.

Required next implementation step:

1. Turn the two canonical protocols and ADV-20260718-042 into a sequenced Engineering implementation packet.
2. Define the routing-registry schema and ownership boundary, keeping deployment state out of department profiles.
3. Define the execution envelope, receiver-state, advisory-revision, and idempotency contracts.
4. Map existing Command Center, scheduler, execution-history, and Automation Logs components onto the new lifecycle and verification model.
5. Specify focused tests before modifying runtime behavior.

### Canonical Prompt Transport Validation Subphase

The prior Package D prompt-catalog work remains preserved as a bounded transport and evidence subphase rather than the definition of the entire package.

Implemented:

- protected catalog definitions for Boot, Quick Boot, Fresh / Full Boot, Sync, Nightly, Advisory, Sync Advisory, Read Advisory, and Consume Advisory;
- read-only canonical entries with editable saved copies;
- destination-aware rendering and canonical schedule snapshots;
- foreground-safety guard;
- timeout-stage diagnostics and server-offline UI guard;
- strict failure-message precision and dual-witness write verification;
- production and probe use the same full-containment composer Group selector;
- dedicated Automation Logs tab backed by the existing SQLite execution-history table;
- stable run IDs and manual-versus-scheduled context;
- safe prompt length and fingerprint metadata without duplicating prompt bodies;
- backend event paths, complete captured child stdout/stderr, durations, result codes, and unexpected-exception tracebacks;
- copyable complete run diagnostics and filters by result, department, trigger, order, and search;
- stage-specific timeout messages that distinguish app readiness, composer readiness, and post-paste verification.

Current evidence:

- the exact destination opens;
- the composer receives focus;
- the complete 341-character canonical prompt visibly pastes;
- nothing is sent;
- verification visibly selects and clears the full draft repeatedly;
- the aligned read-only probe copies all 341 characters after the run;
- the automated verifier still reports failure;
- spinning-loading runs are app-readiness failures and do not count as write-verification evidence.

This defect remains open. Do not broaden timeouts, add alternate paste mechanisms, use Alt+Tab or coordinate hacks, weaken verification, or add another witness without direct evidence. It is not the sole gate for unrelated Package D architecture work, but changes that depend on trustworthy composer delivery must preserve this unresolved boundary.

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

Status: Implemented for the established scheduler and attended-automation contract. It is now the primary technical surface to extend for the new operations procedures. The prompt transport false-negative and broader procedure-runtime implementation remain open.

Capabilities:

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

Automation Logs uses the same durable execution-history rows as Run History. It records complete captured child process streams and safe backend metadata. It does not create a second log database, record environment variables, or copy prompt bodies into diagnostic metadata. The dashboard payload remains bounded to the configured recent-history window so log visibility does not overload normal polling.

### Desktop Department and Worker Automation

Status: Operational for attended HQ use and validated recovery under the established safety contract. Worker title routing and execution-state behavior remain to be implemented under the new protocols.

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
- fail closed on missing, ambiguous, duplicate, stale, paused, or unauthorized targets.

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
- the dashboard may transport and display authorized state but may not invent, approve, prioritize, or broaden work.

## Other Active Tracks

- Route the confirmed shared-file and Worker-pointer drift to Life OS Maintenance HQ through a separate Engineering-origin advisory.
- Observe ordinary role-routed specialist boots and inspect demonstrated defects, including role identity and source-board selection.
- Observe four-source dashboard behavior during ordinary use and genuine degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline aligned with the Worker run model.
- Draft the operation-ledger schema and connector-health policy.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Recent Milestones

- 2026-07-19: Canonical shared execution and Worker protocols adopted; Engineering read-only Sync identified stale Package D framing, corrected Engineering ownership language, preserved prompt verification as a transport subphase, and established operations-procedure runtime implementation as the current front burner.
- 2026-07-19: Ordinary chat operation exposed a role-identity failure in which Engineering HQ identified itself as Business HQ and nearly selected the wrong advisory source board; the incident remains validation evidence under the department-ownership architecture loop.
- 2026-07-18: Dedicated Automation Logs tab and authoritative execution telemetry implemented, including stable run IDs, safe context, backend events, complete captured stdout/stderr, copyable records, useful timeout guidance, and exception trace capture; local validation remains pending.
- 2026-07-18: Production and read-only probe composer selectors aligned; focused selector and write-verification suite passed with 8 tests.
- 2026-07-18: Healthy automation repeatedly pasted and selected the full 341-character canonical draft; the aligned read-only probe copied all 341 characters after the run, isolating the remaining failure to in-run verification behavior.
- 2026-07-18: Scheduler production policy, failed-run pause, Resume rearm, stale one-time restart behavior, ledger health, recurrence, cleanup, and collapsed-project recovery passed runtime validation.
- 2026-07-18: Package C canonical Department Inspection labels passed local dashboard validation and focused tests.
- 2026-07-18: Package B canonical automation mappings and retired-title compatibility passed runtime validation while preserving stable keys and persisted records.
- 2026-07-18: Department Inspection reached 414 normalized records, zero findings, and zero warnings.

Detailed state, priorities, and completion evidence remain authoritative in `projects/engineering/open_loops.md` and referenced Engineering notebook records.

## Production Boundary

- ChatGPT Classic must be available and responsive for UI automation.
- Failed scheduled runs pause according to the validated policy rather than retrying blindly.
- Engineering HQ Daily Sync remains paused by deliberate operating choice until Rob explicitly resumes it.
- Do not begin Package E or unrelated automation-surface expansion while the current procedure-runtime implementation sequence and unresolved transport evidence remain active.
- Windows startup, desktop shell, service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, canonical shared governance, or routine cross-project memory curation.
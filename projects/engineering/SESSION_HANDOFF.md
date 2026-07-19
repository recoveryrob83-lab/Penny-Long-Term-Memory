# Engineering HQ Session Handoff

Updated: 2026-07-19
Project: Engineering HQ
Purpose: Project-specific handoff for technical architecture, operations-procedure implementation, Worker runtime machinery, prompt systems, connector reliability, desktop automation, the LifeOS Dashboard, and the Automation Command Center.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Package D Operations-Procedure and Worker-Runtime Implementation, Receiver Validation, Desktop Automation Reliability, Dashboard Observation, Connector Reliability, Worker Pilots, and Delivery Architecture
- Primary Systems: GitHub, Google Drive, Trello, Todoist, Calendar, Gmail as needed, RPR/user-mediated files, Engineering advisory board, Advisory Index
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, financial account details, medical details, private user data, or sensitive implementation details in Life OS memory files.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read current Engineering notebook records only when referenced by the handoff, status, open loops, or active work.
7. Read `coordination/ADVISORY_INDEX.md` only when advisory routing or cross-department status is relevant.
8. Read `coordination/WORKER_EXECUTION_CONTRACT.md` when Worker architecture, authority enforcement, routing, or behavior is in scope.
9. Do not load the global handoff, all active projects, or system loops during an ordinary Engineering boot unless the current task is explicitly system-level.
10. Keep connector work small, explicit, and verifiable.

## Department Role

Engineering HQ owns technical architecture, software planning, repository strategy, API and connector research, automation design, prompt systems, testing, debugging, technical Worker routing and receiver implementation, implementation sequencing, build-readiness, and truthful verification.

Engineering does not own the canonical shared Worker contract, global boot coherence, profile convention, or department-specific Worker authority. Life OS Maintenance HQ owns those governance surfaces. Engineering implements the registry, transport, validation, receiver state, queues, wake suppression, runtime evidence, tests, and technical reliability required to enforce them.

Business HQ and Office Leaks HQ define what should be built and why. Engineering defines how to build it safely and in the right order.

Route business strategy to Business HQ or Office Leaks HQ, cost-bearing choices to Finance HQ, daily one-off execution to Chief of Staff HQ, shared global memory hygiene and canonical governance to Life OS Maintenance HQ, and non-clinical wellbeing or sustainability judgment to Wellness HQ.

## Chat and Work Model

Use regular Chat for architecture discussion, planning, research, GitHub synchronization, prompt work, debugging analysis, advisories, and small authorized connector updates.

Use Work for bounded execution requiring local files, terminal access, substantial coding, test execution, browser or desktop control, application packaging, or complex artifacts.

Never claim an action, test, deployment, or connector write occurred without verified evidence.

## Highest-Priority Work Package

### Package D: Operations-Procedure and Worker-Runtime Implementation

Status: Active. The canonical LifeOS execution and Worker protocols are now active. Engineering is implementing the technical machinery they require. The former canonical prompt catalog and live write-verification work remains preserved as a transport-validation subphase rather than the definition of the entire package.

Canonical references:

- `projects/engineering/open_loops.md`
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`
- `coordination/ADVISORY_INDEX.md`
- ADV-20260718-042 on `coordination/boards/main-assistant.md`
- `apps/lifeos-dashboard/lifeos_dashboard/canonical_prompt_catalog.py`
- `apps/lifeos-dashboard/automation/probe_composer_group_clipboard.py`
- `projects/engineering/notebook/NOTE-20260717-011-chatgpt-ui-automation-lessons-and-recovery-playbook.md`
- `projects/engineering/notebook/NOTE-20260717-013-command-center-scheduling-live-validation-and-next-recovery-edge.md`

Current implementation scope:

- a Worker routing registry with stable Worker IDs, exact visible titles, department, role, profile path, and Engineering-owned deployment state;
- exact-title lookup with safe zero-match and duplicate-match failure;
- machine-readable execution envelopes and receiver-side semantic validation;
- prompt, parameter, ownership, authorization, and source-boundary checks;
- persistent run identity, advisory revision, receiver state, and duplicate suppression;
- direct one-wake execution-ready routing;
- verification queues, immediate-HQ routing, and wake suppression;
- hold, elevation, resume, rejection, implementation, source-verification, and closure transitions;
- operation-ledger evidence linked to the authoritative advisory or task;
- safe Worker rename and rollover procedures;
- technical enforcement without moving governance ownership into Engineering or the dashboard.

ADV-20260718-042 remains the authoritative open advisory for receiver-side semantic validation. Do not create a duplicate advisory or parallel source for that component.

Next valid Engineering action:

1. turn the two canonical protocols and ADV-20260718-042 into a sequenced implementation packet;
2. define the routing-registry schema and ownership boundary;
3. define the execution-envelope, receiver-state, advisory-revision, and idempotency contracts;
4. map the existing Command Center, scheduler, run history, and Automation Logs onto the new lifecycle and verification rules;
5. specify focused tests before changing runtime behavior.

## Canonical Prompt Transport Subphase

The prior Package D prompt-catalog work remains implemented and useful as transport and evidence infrastructure.

Implemented and tested:

- protected canonical prompt definitions for Boot, Quick Boot, Fresh / Full Boot, Sync, Nightly, Advisory, Sync Advisory, Read Advisory, and Consume Advisory;
- read-only canonical entries with editable saved copies;
- destination-aware rendering and schedule snapshots;
- foreground-safety guard;
- timeout-stage diagnostics;
- server-offline UI guard;
- strict failure-message precision;
- strict dual-witness write verification;
- full Package D UI behavior test coverage from the prior subphase;
- focused selector, foreground, failure-precision, timeout, server-availability, and verification tests.

Current transport evidence:

1. Healthy ChatGPT Classic state:
   - the exact destination opens;
   - the composer receives focus;
   - the full canonical prompt visibly pastes;
   - nothing is sent;
   - the aligned read-only probe can copy the full 341-character draft after the run;
   - in-run automated verification still reports a false failure.
2. Degraded ChatGPT Classic state:
   - the destination remains on the spinning loading state;
   - the composer never becomes usable;
   - this is app-readiness failure evidence, not valid write-verification evidence.

Transport boundary:

- do not rerun automation while ChatGPT Classic is visibly lagging or stuck loading;
- do not add broader timeouts, alternate paste mechanisms, Alt+Tab behavior, coordinate hacks, weaker verification, or a third witness without direct evidence;
- do not begin Package E or unrelated automation-surface expansion while current procedure-runtime work and unresolved transport evidence remain active;
- keep the proposed persistent Pause All Automation header control deferred unless the current implementation plan establishes a concrete need.

The unresolved transport defect remains a real subtask. It is not the sole gate for registry, schema, lifecycle, queue, and receiver-contract design that does not depend on changing composer verification.

## Completed Foundation

The following foundation is complete and should not be reopened without new evidence:

- department ownership architecture and read-only Department Inspection;
- fresh LifeOS HQ verification of the role-routed operating model;
- Package B canonical automation names and retired-title compatibility while preserving stable destination keys;
- Package C Department Inspection canonical labels while preserving stable scope IDs and filesystem paths;
- collapsed LifeOS project recovery;
- scheduler persistence, recurrence, overdue visibility, pause-on-failure behavior, restart policy, ledger synchronization, and cleanup controls;
- exact destination navigation, occupied-composer preservation, clipboard lifetime and restoration, explicit send authorization, one-job locking, and stop on uncertainty.

Detailed completion evidence remains in `projects/engineering/open_loops.md` and the referenced Engineering notebook records.

## Automation Command Center

Status: Implemented and operationally validated for its established scheduling and attended-automation policy. It is now the primary technical surface to extend for the new operations procedures. The prompt transport false-negative and the broader procedure-runtime implementation remain open.

Current implementation includes:

- eight exact HQ destinations;
- canonical, saved, and custom prompt sources;
- protected read-only canonical prompts and editable saved copies;
- saved-prompt default destinations and explicit mismatch handling;
- draft or explicitly confirmed live-send mode;
- one-job-at-a-time process lock;
- global pause;
- structured results and exact failure reasons;
- persistent SQLite activity history;
- one-time, daily, weekly, and bounded five-minute debug schedules in `America/Chicago`;
- persistent scheduled jobs across dashboard restarts;
- schedule create, edit, pause, resume, run, cleanup, and delete controls;
- separate Scheduled Jobs, Run History, and Automation Logs views;
- no-billing Scheduler Ledger synchronization through the bound Apps Script endpoint.

Historical tests using retired display labels remain historical evidence only. Current runtime presentation uses canonical HQ names while stable internal keys remain unchanged.

## Desktop Department and Worker Automation

Status: Operational for attended HQ use and validated recovery under the current safety contract. Worker title routing, receiver behavior, and procedure-state orchestration remain to be implemented.

Canonical implementation:

- launcher: `apps/lifeos-dashboard/automation/draft_department_boot.py`
- production engine: `apps/lifeos-dashboard/automation/open_department_chat_group.py`
- verification shim: `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`
- canonical catalog: `apps/lifeos-dashboard/lifeos_dashboard/canonical_prompt_catalog.py`
- read-only probe: `apps/lifeos-dashboard/automation/probe_composer_group_clipboard.py`
- naming standard: `memory/HQ_NAMING_STANDARD.md`

Safety contract:

- exact destination matching only;
- bounded exact project and `Show more` recovery;
- exact active-document verification;
- stable Group composer discovery and reacquisition;
- preserve an occupied composer;
- preserve clipboard lifetime through verification and restore the prior value afterward;
- explicit send authorization;
- one job at a time;
- stop on uncertainty;
- never blind-retry after uncertain state;
- fail closed on missing, ambiguous, duplicate, stale, paused, or unauthorized targets.

## Canonical Prompt Catalog

Status: Implemented. Live verification remains open as a bounded transport subphase, not the entire Package D gate.

Protected families:

- Boot;
- Quick Boot;
- Fresh / Full Boot;
- Sync;
- Nightly;
- Advisory;
- Sync Advisory;
- Read Advisory;
- Consume Advisory.

`memory/CONTEXT_REMINDER.md` remains the canonical command vocabulary. The executable catalog is a protected runtime representation, not a competing governance source.

## LifeOS Dashboard

Canonical application path:

- `apps/lifeos-dashboard/`

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
- guarded GitHub sync is limited to clean, strictly-behind fast-forward updates;
- Trello, Todoist, and Calendar remain independent read-only adapters with cache behavior;
- Gmail and general Drive adapters remain deferred until demonstrated need;
- the dashboard is a visibility and bounded local-control layer, not a replacement source of truth;
- Department Inspection does not edit, merge, close, promote, demote, or create advisories automatically;
- the dashboard transports and displays authorized state but does not invent, approve, prioritize, or broaden work.

## Production Boundary

The established scheduler policy and recovery behavior are live-validated. Fully unattended Windows operation is not assumed merely because scheduling works.

Current boundary:

- ChatGPT Classic must be available and responsive for UI automation;
- failed scheduled runs pause according to the validated policy rather than retrying blindly;
- Engineering HQ Daily Sync remains paused until Rob explicitly resumes it;
- do not begin Package E or unrelated automation-surface expansion while current procedure-runtime implementation and unresolved transport evidence remain active;
- Windows startup, desktop shell, service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Other Active Tracks

- Route confirmed shared-file and Worker-pointer drift to Life OS Maintenance HQ through a separate Engineering-origin advisory.
- Observe ordinary role-routed specialist boots and inspect demonstrated defects, including role identity and source-board selection.
- Observe four-source dashboard behavior during ordinary use and genuine degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline aligned with the Worker run model.
- Draft the operation-ledger schema and connector-health policy.
- Continue Office Leaks delivery architecture as concrete requirements mature.

## Advisory State

As of 2026-07-19:

- ADV-20260718-042 is OPEN and targeted to Engineering HQ for receiver-side semantic validation, execution envelopes, authorization checks, duplicate suppression, and controlled Worker outcomes.
- ADV-20260719-043 is CLOSED after Life OS Maintenance created the canonical shared execution and Worker protocols.
- No Engineering-origin advisory to Maintenance has yet been posted for the shared-file reconciliation identified during the July 19 verification pass.

## Immediate Next Action

Complete this Engineering-owned state reconciliation, then issue one Engineering-origin advisory to Life OS Maintenance HQ for the confirmed shared-file and pointer corrections. After routing that dependency, begin the Package D implementation packet with the routing-registry and execution-envelope / receiver-state contracts.

## Safety and Truthfulness

- Prefer small, verifiable operations.
- Fetch before editing and verify after writing.
- Keep connector-heavy work narrowly scoped.
- Never commit secrets or private account data.
- Never claim local runtime success without Rob's confirmation.
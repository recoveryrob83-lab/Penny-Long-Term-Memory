# Engineering HQ Session Handoff

Updated: 2026-07-17
Project: Engineering HQ
Purpose: Project-specific handoff for software architecture, prompt systems, workers, connector reliability, desktop automation, the LifeOS Dashboard, and the Automation Command Center.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Automation Command Center Phase 1 Design, Desktop Automation Maintenance, Dashboard Observation, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture
- Primary Systems: GitHub, Google Drive, Trello, Todoist, Calendar, Gmail as needed, RPR/user-mediated files, Engineering advisory board, Advisory Index
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, financial account details, medical details, private user data, or sensitive implementation details in Life OS memory files.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md`.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Read `coordination/ADVISORY_INDEX.md` only when advisory routing or cross-department status is relevant.
6. Read a source board only when the index points to a relevant advisory or Rob names it.
7. Keep connector work small, explicit, and verifiable.

## Department Role

Engineering HQ owns technical architecture, software planning, repository strategy, API and connector research, automation design, prompt systems, testing, debugging, worker contracts, implementation sequencing, build-readiness, and truthful verification.

Business HQ and Office Leaks HQ define what should be built and why. Engineering defines how to build it safely and in the right order.

Route business strategy to Business or Office Leaks, cost-bearing choices to Finance, daily one-off execution to Main Assistant, shared global memory hygiene to Logistics, and recovery or health sustainability to Wellness.

## Chat and Work Model

Use regular Chat for architecture discussion, planning, research, GitHub synchronization, prompt work, debugging analysis, advisories, and small authorized connector updates.

Use Work for bounded execution requiring local files, terminal access, substantial coding, test execution, browser or desktop control, application packaging, or complex artifacts.

Never claim an action, test, deployment, or connector write occurred without verified evidence.

## Current Engineering Tracks

### 1. Automation Command Center Phase 1

Status: Planned and ready for design and implementation.

Canonical plan:

- `projects/engineering/notebook/NOTE-20260717-012-lifeos-ui-automation-command-center-plan.md`

Phase 1 goal:

Create a dashboard-integrated manual command center that safely invokes the validated desktop automation engine.

Required Phase 1 scope:

- eight exact destinations: `LifeOS HQ` plus the seven department HQs;
- canonical boot prompt, saved template, or custom prompt;
- draft or send mode;
- explicit confirmation for send mode;
- manual Run Now only;
- plain-language execution summary before run;
- one-job-at-a-time process lock;
- global pause control;
- structured result and exact failure reason;
- local activity log.

Phase 1 exclusions:

- no scheduling;
- no recurring jobs;
- no automatic ChatGPT launch;
- no simultaneous jobs;
- no connector-pill automation;
- no blind retry after uncertain send state.

Architecture direction:

- dashboard UI manages validated job definitions;
- a local job runner invokes the existing engine outside the web request handler;
- SQLite is recommended later for persisted schedules and history, but Phase 1 may begin with the smallest safe local job store;
- the existing automation safety contract must be inherited without weakening.

Scheduling begins only after Phase 1 proves the dashboard-to-runner boundary, locking, structured results, and safety controls.

### 2. Desktop Department Automation

Status: Operational and validated.

Canonical implementation:

- launcher: `apps/lifeos-dashboard/automation/draft_department_boot.py`
- production engine: `apps/lifeos-dashboard/automation/open_department_chat_group.py`
- verification shim: `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`
- legacy rollback reference: `apps/lifeos-dashboard/automation/open_department_chat.py`
- naming standard: `memory/HQ_NAMING_STANDARD.md`

Validated across all seven HQs:

- exact sidebar chat-link matching;
- one bounded `Show more` expansion;
- exact active-document verification;
- bounded recovery for the known generic `ChatGPT` loading state;
- stable Group composer discovery;
- preservation of existing draft text;
- clipboard round-trip verification;
- canonical prompt insertion;
- draft-only default behavior;
- explicit `--send` requirement;
- one watched successful live send to Main Assistant HQ.

Current safety contract:

- stop on uncertainty;
- never use arbitrary fuzzy matching;
- never overwrite an occupied composer without explicit replacement authorization;
- never submit without all destination, readiness, content, and send gates passing;
- treat inability to prove connector activation as a rare visible soft failure rather than adding fragile connector-pill automation.

Durable references:

- `projects/engineering/notebook/NOTE-20260717-010-desktop-department-automation-live-send-handoff.md`
- `projects/engineering/notebook/NOTE-20260717-011-chatgpt-ui-automation-lessons-and-recovery-playbook.md`

The prior Wellness loading failure is resolved historical context. Do not reopen it as active work unless a comparable failure recurs.

### 3. LifeOS Dashboard

Canonical application path:

- `apps/lifeos-dashboard/`

The dashboard is locally running and validated on Rob's Windows machine.

Verified live sources:

- GitHub
- Trello
- Todoist
- Google Calendar private iCal

Verification:

- full suite passed with 16 tests;
- Windows timezone support uses `tzdata`;
- guarded GitHub sync is limited to clean, strictly-behind fast-forward updates;
- Trello, Todoist, and Calendar remain independent read-only adapters with cache behavior.

Current dashboard work:

- observe ordinary daily refresh behavior;
- add a small configurable browser-side auto-refresh control only if still useful;
- integrate Command Center Phase 1 without blocking normal dashboard refreshes;
- preserve independent cache behavior and guarded Git sync;
- defer Gmail and Drive until demonstrated operational need.

The dashboard is a visibility layer, not a replacement source of truth or newly authorized PennyOS roadmap.

### 4. Reliable Connector Execution Layer

Connector reliability remains a first-class architecture risk.

Current design concerns:

- operation ledger or write-ahead log;
- connector health states;
- idempotency and duplicate prevention;
- post-write verification;
- bounded retry and stop rules;
- degraded-mode language and recovery paths;
- manual, RPR, export, or alternate-worker fallback;
- queue-first execution and human approval checkpoints.

Command Center structured execution results may become a concrete local proving ground for these patterns, but do not conflate UI automation jobs with connector writes.

### 5. Life OS Worker Architecture

Implemented workers:

- Penny Raw Capture Worker: `workers/penny-raw-capture/`
- Penny Inventory Worker: `workers/penny-inventory/`

Both need real operational evidence before more workers are proposed.

### 6. Office Leaks Delivery Architecture

Mechanical layer: map, score, scope, sprint, verify, handoff, follow up.

Human-system layer: respect, rapport, internal champion, users, Aha Moment, adoption verification, relational follow-up.

References:

- `projects/engineering/notebook/NOTE-20260708-005-office-leak-delivery-playbooks-v1.md`
- `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`

### 7. Prompt Launcher and Command Interface

The launcher remains a secondary interface over `memory/CONTEXT_REMINDER.md`.

Completed:

- corrected literal newline output;
- corrected the Logistics project path to `projects/life-logistics-hq`;
- routed the legacy Logistics wrapper through the canonical department launcher;
- aligned launcher labels with canonical HQ names;
- aligned generated boot prompts with current status-file handling and role boundaries.

Deferred improvements remain captured in:

- `projects/engineering/notebook/NOTE-20260716-007-prompt-launcher-advisory-commands-and-scope.md`

### 8. LifeOS Chat HQ Architecture

All seven department HQ chats are operational. On-demand Windows automation can draft or explicitly submit the canonical boot prompt to each HQ.

Command Center Phase 1 will expose this on-demand engine through the dashboard. It does not authorize unattended scheduling.

Engineering HQ Daily Sync remains paused until Rob explicitly resumes it under a separate safe scheduling architecture after manual Command Center validation.

## Advisory State

As of 2026-07-17:

- No open advisories are listed in `coordination/ADVISORY_INDEX.md`.
- ADV-20260717-040 is implemented / acknowledged / closed.
- ADV-20260716-039 is implemented / acknowledged / closed.
- ADV-20260716-038 is acknowledged / ingested / closed.

## Active Open Loops

- Design and implement Automation Command Center Phase 1 with manual Run Now only.
- Maintain desktop automation safety and revalidate only after material UI changes or observed failures.
- Add configurable browser-side dashboard auto-refresh if ordinary use still demonstrates value.
- Observe four-source dashboard behavior during ordinary use and real degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real items.
- Observe Penny Raw Capture Worker in real use.
- Draft the Reliable Connector Execution Layer implementation packet and operation-ledger schema.
- Define idempotency, verification, connector-health, retry, and recovery patterns.
- Continue Office Leaks delivery architecture as requirements mature.
- Observe Chat HQ routing friction and model-use waste.
- Keep Engineering HQ Daily Sync paused until explicitly resumed.

## Deferred

- One-time and recurring Command Center schedules wait for Phase 1 proof.
- Automatic ChatGPT launch, screenshots, notifications, and advanced recovery wait for later phases.
- Gmail and Drive dashboard adapters remain deferred until demonstrated need.
- Desktop-window packaging follows sustained browser usefulness.
- Prompt-launcher advisory commands and scope metadata remain deferred.
- Additional workers wait for real Raw Capture and Inventory evidence.

## Completed Recent Work

- 2026-07-17: Automation Command Center plan captured with Phase 1 manual-only scope and explicit scheduling deferral.
- 2026-07-17: Desktop automation validated across all seven HQs and one watched live send completed successfully to Main Assistant HQ.
- 2026-07-17: NOTE-010 closed as completed and NOTE-011 established the durable UI automation recovery playbook.
- 2026-07-17: Logistics boot path and generated boot prompts corrected.
- 2026-07-17: Guarded GitHub auto-sync merged and locally verified with 16 passing tests.
- 2026-07-17: Live Todoist, Calendar, Trello, and GitHub dashboard adapters verified.
- 2026-07-17: ADV-20260717-040 and ADV-20260716-039 closed after shared-summary reconciliation.
- 2026-07-16: ADV-20260716-038 consumed and closed; dashboard boundaries established.
- 2026-07-15: Seven LifeOS Chat HQs launched.

## Immediate Next Action

Start Automation Command Center Phase 1 with the smallest safe dashboard-to-runner boundary: exact destination selection, prompt choice, draft/send mode, explicit confirmation, one-job lock, Run Now, structured result, global pause, and local activity history. Do not implement scheduling in Phase 1.

## Safety and Truthfulness

- Prefer small, verifiable operations.
- Fetch before editing and verify after writing.
- Keep connector-heavy work narrowly scoped.
- Never commit secrets or private account data.
- Never claim success without a successful tool or runtime result.

## Notes for Next Penny

Engineering HQ now maintains a working four-source dashboard, working seven-HQ desktop boot automation, and a planned dashboard-integrated Automation Command Center. The next build is Phase 1 manual Run Now only. Scheduling is a later phase, not a hidden requirement.

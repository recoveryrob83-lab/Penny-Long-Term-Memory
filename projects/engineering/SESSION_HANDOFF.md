# Engineering HQ Session Handoff

Updated: 2026-07-17
Project: Engineering HQ
Purpose: Project-specific handoff for software architecture, prompt systems, workers, connector reliability, desktop automation, the LifeOS Dashboard, and the Automation Command Center.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Automation Command Center Operational Validation, Desktop Recovery, Canonical Prompt Catalog, Dashboard Observation, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture
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

### 1. Automation Command Center

Status: Implemented and in live operational validation.

Canonical references:

- `projects/engineering/notebook/NOTE-20260717-012-lifeos-ui-automation-command-center-plan.md`
- `projects/engineering/notebook/NOTE-20260717-013-command-center-scheduling-live-validation-and-next-recovery-edge.md`

Current implementation includes:

- eight exact destinations: LifeOS HQ plus seven department HQs;
- canonical, saved, and custom prompt sources;
- protected read-only canonical prompts and editable saved copies;
- saved-prompt default destinations and explicit mismatch handling;
- draft or explicitly confirmed live-send mode;
- one-job-at-a-time process lock;
- global pause;
- structured results and exact failure reasons;
- persistent SQLite activity history;
- one-time, daily, and weekly schedules in `America/Chicago`;
- persistent scheduled jobs across dashboard restarts;
- schedule create, edit, pause, resume, and delete.

Live evidence completed:

- one-time `Hi Penny Test` live send to Engineering HQ succeeded and completed with no future run;
- first daily `Hi Penny LifeOS Test` live send to LifeOS HQ succeeded and advanced to 2026-07-18 15:05 CT;
- Rob continued chatting on mobile while another response was generating and the desktop scheduled send fired into LifeOS HQ without cross-chat interference.

Still awaiting evidence:

- scheduled occupied-composer refusal in Logistics HQ;
- restart and overdue one-time behavior;
- second real occurrence of a recurring schedule.

Do not claim the Logistics failure test passed until Rob supplies the completed result and confirms the existing draft remained unchanged.

### 2. Desktop Department Automation

Status: Operational with one newly identified recovery edge case.

Canonical implementation:

- launcher: `apps/lifeos-dashboard/automation/draft_department_boot.py`
- production engine: `apps/lifeos-dashboard/automation/open_department_chat_group.py`
- verification shim: `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`
- naming standard: `memory/HQ_NAMING_STANDARD.md`

Validated behavior:

- exact sidebar chat-link matching;
- one bounded `Show more` expansion;
- exact active-document verification;
- stable Group composer discovery;
- preservation of existing draft text in prior direct testing;
- clipboard round-trip verification;
- canonical prompt insertion;
- draft-only default behavior;
- explicit send requirement;
- stop on uncertainty;
- successful manual and scheduled live sends.

Current safety contract:

- never use arbitrary fuzzy matching;
- never overwrite an occupied composer without explicit replacement authorization;
- never submit without destination, readiness, content, and send gates passing;
- never blind-retry after uncertain send state.

New edge case:

ChatGPT Classic may collapse the LifeOS project folder after application restart or when the window is narrowed. The current engine handles `Show more` inside an expanded project, but it has not been coded or validated to reopen a collapsed LifeOS project folder.

Current authorized workaround:

- keep ChatGPT Classic open;
- keep the LifeOS project expanded;
- keep chats available through the normal sidebar / `Show more` path;
- do not update the automation code yet;
- do not treat execution after restart or major resize as unattended-production-safe.

Next code update, only after Rob authorizes it:

1. detect the exact collapsed LifeOS project control;
2. expand it once;
3. verify the project chat region is visible;
4. continue through existing exact-chat and `Show more` navigation;
5. stop safely if expansion or verification is uncertain;
6. revalidate in draft mode across restart, narrow-window, hidden-chat, and occupied-composer cases before watched live-send testing.

### 3. Canonical Prompt Catalog

Status: Next product/data milestone.

The command center currently exposes primarily the Boot canonical family. Populate the protected canonical prompt registry from authoritative LifeOS command definitions.

Likely candidates requiring reconciliation:

- Boot / Quick Boot / Full Boot;
- Sync;
- Nightly;
- Advisory;
- Sync Advisory;
- Read Advisory;
- Consume Advisory.

Canonical definitions must remain protected and read-only. User-editable variants must be created as saved copies.

### 4. LifeOS Dashboard

Canonical application path:

- `apps/lifeos-dashboard/`

The dashboard is locally running and validated on Rob's Windows machine.

Verified live sources:

- GitHub
- Trello
- Todoist
- Google Calendar private iCal

Current boundaries:

- Windows timezone support uses `tzdata`;
- guarded GitHub sync is limited to clean, strictly-behind fast-forward updates;
- Trello, Todoist, and Calendar remain independent read-only adapters with cache behavior;
- Gmail and Drive adapters remain deferred until demonstrated need;
- the dashboard is a visibility and local-control layer, not a replacement source of truth.

### 5. Production Readiness

Scheduling is operational but not yet production-ready for fully unattended Windows use.

Remaining evidence or implementation:

- scheduled occupied-composer refusal;
- overdue-run behavior after dashboard restart;
- repeated recurrence across a second real occurrence;
- collapsed-project recovery;
- scheduler health and preflight visibility;
- explicit missed-run policy;
- potential execution-window controls;
- Windows startup, desktop shell, or service packaging if sustained use requires it.

Engineering HQ Daily Sync remains paused until Rob explicitly resumes it after these unattended-operation boundaries are safe enough.

### 6. Reliable Connector Execution Layer

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

Command Center structured execution results may be a concrete local proving ground for these patterns, but do not conflate UI automation jobs with connector writes.

### 7. Life OS Worker Architecture

Implemented workers:

- Penny Raw Capture Worker: `workers/penny-raw-capture/`
- Penny Inventory Worker: `workers/penny-inventory/`

Both need real operational evidence before more workers are proposed.

### 8. Office Leaks Delivery Architecture

Mechanical layer: map, score, scope, sprint, verify, handoff, follow up.

Human-system layer: respect, rapport, internal champion, users, Aha Moment, adoption verification, relational follow-up.

## Advisory State

As of 2026-07-17:

- No open advisories are listed in `coordination/ADVISORY_INDEX.md`.
- ADV-20260717-040 is implemented / acknowledged / closed.
- ADV-20260716-039 is implemented / acknowledged / closed.
- ADV-20260716-038 is acknowledged / ingested / closed.

## Active Open Loops

- Complete and record the Logistics HQ occupied-composer scheduled refusal test.
- Test dashboard restart and overdue-run behavior.
- Observe the next real recurring occurrence.
- Design collapsed-project recovery without changing code until Rob authorizes it.
- Populate the protected canonical prompt catalog.
- Define missed-run policy and production preflight requirements.
- Maintain desktop automation safety and revalidate after material UI changes or observed failures.
- Observe four-source dashboard behavior during ordinary use and real degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real items.
- Observe Penny Raw Capture Worker in real use.
- Draft the Reliable Connector Execution Layer implementation packet and operation-ledger schema.
- Continue Office Leaks delivery architecture as requirements mature.
- Keep Engineering HQ Daily Sync paused until explicitly resumed.

## Completed Recent Work

- 2026-07-17: Manual Automation Command Center path implemented and live-validated.
- 2026-07-17: Saved prompt lifecycle, default destinations, mismatch safeguards, and delete behavior validated.
- 2026-07-17: Persistent one-time, daily, and weekly scheduling implemented.
- 2026-07-17: One-time live send to Engineering HQ succeeded and completed correctly.
- 2026-07-17: First daily live send to LifeOS HQ succeeded and advanced correctly.
- 2026-07-17: Concurrent mobile chat activity and response generation did not interfere with scheduled desktop execution.
- 2026-07-17: Collapsed LifeOS project-folder behavior identified as the next recovery edge case; no code change authorized.
- 2026-07-17: Desktop automation validated across all seven HQs.
- 2026-07-17: Guarded GitHub auto-sync and four-source dashboard operation validated.

## Immediate Next Action

Finish the occupied-composer scheduled refusal test and capture the result. Then populate the protected canonical prompt catalog or, when explicitly authorized, implement bounded collapsed-LifeOS-project recovery. Do not change the desktop automation for the collapsed-project edge case before Rob authorizes it.

## Safety and Truthfulness

- Prefer small, verifiable operations.
- Fetch before editing and verify after writing.
- Keep connector-heavy work narrowly scoped.
- Never commit secrets or private account data.
- Never claim success without a successful tool or runtime result.

## Notes for Next Penny

Engineering HQ now maintains a working four-source dashboard, validated seven-HQ desktop automation, a fully implemented Automation Command Center, and operational one-time/daily/weekly scheduling. The most important newly discovered boundary is the collapsed LifeOS project folder after restart or narrow-window layout. Preserve the current workaround, await authorization before changing code, and treat the canonical prompt catalog as the next product/data milestone.

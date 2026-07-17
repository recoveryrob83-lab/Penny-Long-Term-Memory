# Engineering HQ Session Handoff

Updated: 2026-07-18
Project: Engineering HQ
Purpose: Project-specific handoff for software architecture, prompt systems, workers, connector reliability, desktop automation, the LifeOS Dashboard, and the Automation Command Center.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Department Ownership Verification, Automation Operational Validation, Desktop Recovery, Canonical Prompt Catalog, Connector Reliability, Worker Pilots, and Delivery Architecture
- Primary Systems: GitHub, Google Drive, Trello, Todoist, Calendar, Gmail as needed, RPR/user-mediated files, Engineering advisory board, Advisory Index
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, financial account details, medical details, private user data, or sensitive implementation details in Life OS memory files.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Read `coordination/ADVISORY_INDEX.md` only when advisory routing or cross-department status is relevant.
6. Read a source board only when the index points to a relevant advisory or Rob names it.
7. Do not load the global handoff, all active projects, or system loops during an ordinary Engineering boot unless the current task is explicitly system-level.
8. Keep connector work small, explicit, and verifiable.

## Department Role

Engineering HQ owns technical architecture, software planning, repository strategy, API and connector research, automation design, prompt systems, testing, debugging, worker contracts, implementation sequencing, build-readiness, and truthful verification.

Business HQ and Office Leaks HQ define what should be built and why. Engineering defines how to build it safely and in the right order.

Route business strategy to Business or Office Leaks, cost-bearing choices to Finance, daily one-off execution to Main Assistant, shared global memory hygiene to Logistics, and recovery or health sustainability to Wellness.

## Chat and Work Model

Use regular Chat for architecture discussion, planning, research, GitHub synchronization, prompt work, debugging analysis, advisories, and small authorized connector updates.

Use Work for bounded execution requiring local files, terminal access, substantial coding, test execution, browser or desktop control, application packaging, or complex artifacts.

Never claim an action, test, deployment, or connector write occurred without verified evidence.

## Highest-Priority Work Package

Status: Ownership architecture implemented; post-cleanup verification pending.

Canonical references:

- `projects/engineering/notebook/NOTE-20260717-014-department-ownership-and-dashboard-inspection.md`
- `apps/lifeos-dashboard/DEPARTMENT_INSPECTION_DATA_CONTRACT.md`
- `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`
- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
- `memory/STARTUP_BOOT.md`

Implemented decisions:

- department `open_loops.md` files are authoritative for department-owned work;
- `memory/05_OPEN_LOOPS.md` is system-only;
- global visibility does not justify mirrored department records;
- the dashboard aggregates department and system state read-only;
- shared rules are universal, operational state is role-routed;
- specialists load their own files and only relevant shared dependencies;
- Main Assistant and Logistics receive broader context according to role;
- system promotion, demotion, lifecycle, reference, and reconciliation rules are formalized.

Inspector implementation and evidence:

- Department Inspection tab is locally validated;
- seven departments plus System are normalized;
- Work, Knowledge, Operations, and Findings are filterable;
- first baseline was 458 records / 4 findings / 101 warnings;
- first tuning produced 459 records / 4 findings / 15 warnings;
- confirmed findings exposed state/priority mixing, broad Chat HQ watch mirrors, Legacy VA folder mirrors, and speculative registry placeholders;
- first source cleanup and explicit-priority parsing are committed.

Immediate validation boundary:

1. restore or confirm the local desktop/dashboard connection;
2. refresh and restart the FastAPI dashboard process;
3. compare post-cleanup counts with the 459 / 4 / 15 tuned baseline;
4. inspect any remaining findings individually;
5. observe ordinary specialist boots for real routing defects;
6. close the ownership-reconciliation system wrapper after stable use.

Do not broadly weaken finding detection merely to reach zero findings.

## Automation Command Center

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
- schedule create, edit, pause, resume, and delete;
- separate Scheduled Jobs and Run History categories with independent filters.

Live evidence completed:

- one-time `Hi Penny Test` live send to Engineering HQ succeeded and completed with no future run;
- first daily `Hi Penny LifeOS Test` live send to LifeOS HQ succeeded and advanced correctly;
- mobile use and active response generation did not interfere with the desktop scheduled send;
- scheduled Logistics HQ occupied-composer refusal preserved the existing draft, sent nothing, recorded `failed`, and displayed the explicit recovery reason.

Still awaiting evidence:

- restart and overdue one-time behavior;
- second real occurrence of a recurring schedule.

## Desktop Department Automation

Status: Operational with one known recovery edge case.

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
- occupied-composer preservation in direct and scheduled tests;
- clipboard round-trip verification;
- canonical prompt insertion;
- draft-only default behavior;
- explicit send requirement;
- stop on uncertainty;
- successful manual and scheduled live sends;
- structured safe-failure reporting through the scheduler and dashboard.

Safety contract:

- never use arbitrary fuzzy matching;
- never overwrite an occupied composer without explicit replacement authorization;
- never submit without destination, readiness, content, and send gates passing;
- never blind-retry after uncertain send state.

Known edge case:

ChatGPT Classic may collapse the LifeOS project folder after application restart or when the window is narrowed. The current engine handles `Show more` inside an expanded project, but it has not been coded or validated to reopen a collapsed LifeOS project folder.

Current workaround:

- keep ChatGPT Classic open;
- keep the LifeOS project expanded;
- keep chats available through the normal sidebar / `Show more` path;
- do not treat execution after restart or major resize as unattended-production-safe.

Do not change the recovery code until Rob explicitly authorizes the bounded exact-project expansion update.

## Canonical Prompt Catalog

Status: Active product/data milestone.

The Command Center currently exposes primarily the Boot canonical family. Populate the protected canonical prompt registry from authoritative LifeOS command definitions while preserving read-only canonical behavior and editable saved copies.

Candidate families:

- Boot / Quick Boot / Full Boot;
- Sync;
- Nightly;
- Advisory;
- Sync Advisory;
- Read Advisory;
- Consume Advisory.

## LifeOS Dashboard

Canonical application path:

- `apps/lifeos-dashboard/`

The dashboard is locally running and validated on Rob's Windows machine.

Verified live sources:

- GitHub
- Trello
- Todoist
- Google Calendar private iCal

Current tabs:

- Overview
- Department Inspection
- Automation

Current boundaries:

- Windows timezone support uses `tzdata`;
- guarded GitHub sync is limited to clean, strictly-behind fast-forward updates;
- Trello, Todoist, and Calendar remain independent read-only adapters with cache behavior;
- Gmail and Drive adapters remain deferred until demonstrated need;
- the dashboard is a visibility and local-control layer, not a replacement source of truth;
- Department Inspection does not edit, merge, close, promote, demote, or create advisories automatically.

## Production Readiness

Scheduling is operational but not yet production-ready for fully unattended Windows use.

Remaining evidence or implementation:

- overdue-run behavior after dashboard restart;
- repeated recurrence across a second real occurrence;
- collapsed-project recovery;
- scheduler health and preflight visibility;
- explicit missed-run policy;
- potential execution-window controls;
- Windows startup, desktop shell, or service packaging if sustained use requires it.

Engineering HQ Daily Sync remains paused until Rob explicitly resumes it after these unattended-operation boundaries are safe enough.

## Other Active Tracks

- Reliable Connector Execution Layer: operation ledger, connector health, idempotency, verification, bounded retries, degraded modes, and recovery paths.
- Worker architecture: Raw Capture and Inventory workers need real operational evidence before more workers are proposed.
- Office Leaks delivery architecture: preserve mechanical and human-system implementation layers as concrete requirements mature.

## Advisory State

As of 2026-07-18:

- No open advisories are listed in `coordination/ADVISORY_INDEX.md`.
- ADV-20260717-040 is implemented / acknowledged / closed.
- ADV-20260716-039 is implemented / acknowledged / closed.
- ADV-20260716-038 is acknowledged / ingested / closed.

## Active Open Loops

- Verify post-cleanup Department Inspection counts and findings.
- Observe role-routed specialist boots and correct only demonstrated defects.
- Close the ownership-reconciliation system wrapper after stable use.
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

- 2026-07-18: Department Inspection MVP locally validated and tuned from 101 warnings to 15.
- 2026-07-18: First inspector-guided source cleanup completed.
- 2026-07-18: Open Loop Ownership and Visibility SOP implemented.
- 2026-07-18: Startup boot changed to a universal kernel plus role-routed context.
- 2026-07-18: System open loops and system handoff reconciled under the new ownership rules.
- 2026-07-17: Scheduled occupied-composer refusal and structured dashboard reporting passed end to end.
- 2026-07-17: Scheduled Jobs and Run History were separated with independent filters.
- 2026-07-17: Manual Automation Command Center path implemented and live-validated.
- 2026-07-17: Saved prompt lifecycle, default destinations, mismatch safeguards, and delete behavior validated.
- 2026-07-17: Persistent one-time, daily, and weekly scheduling implemented.
- 2026-07-17: Desktop automation validated across all seven HQs.
- 2026-07-17: Guarded GitHub auto-sync and four-source dashboard operation validated.

## Immediate Next Action

When the local desktop/dashboard connection is available, refresh and restart the dashboard, record the post-cleanup Department Inspection counts, and inspect only the findings that remain. Until then, preserve the new ownership and boot architecture and do not perform broad parser weakening.

## Safety and Truthfulness

- Prefer small, verifiable operations.
- Fetch before editing and verify after writing.
- Keep connector-heavy work narrowly scoped.
- Never commit secrets or private account data.
- Never claim local runtime success without Rob's confirmation.

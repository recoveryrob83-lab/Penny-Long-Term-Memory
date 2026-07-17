# Engineering HQ Session Handoff

Updated: 2026-07-17
Project: Engineering HQ
Purpose: Project-specific handoff for software architecture, prompt systems, workers, connector reliability, desktop automation, the LifeOS Dashboard, and the Automation Command Center.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Department Ownership Architecture and Dashboard Inspection, Automation Operational Validation, Desktop Recovery, Canonical Prompt Catalog, Connector Reliability, Worker Pilots, and Delivery Architecture
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

## Highest-Priority Work Package

Canonical note:

- `projects/engineering/notebook/NOTE-20260717-014-department-ownership-and-dashboard-inspection.md`

Decision direction:

- department `open_loops.md` files are authoritative for department-owned work;
- system loops are reserved for genuinely shared or multi-owner work;
- specialist departments should not load unrelated department backlogs;
- cross-department awareness should move through advisories, explicit dependencies, routed handoffs, or Main/Logistics coordination;
- the dashboard may aggregate all department state without becoming another source of truth.

Required sequence:

1. audit current global and department loop duplication;
2. formalize ownership, promotion, demotion, lifecycle, and reconciliation procedures;
3. update boot routing so specialists receive only relevant global context;
4. reconcile stale global loop and handoff language;
5. add a Department Inspection tab between Overview and Automation;
6. aggregate all seven departments' loops, notebooks, logs, and status records with department, status, priority, date, type, search, and sort filters;
7. validate that department files remain authoritative.

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
- first daily `Hi Penny LifeOS Test` live send to LifeOS HQ succeeded and advanced to 2026-07-18 15:05 CT;
- mobile use and active response generation did not interfere with the desktop scheduled send;
- scheduled Logistics HQ occupied-composer refusal preserved the existing draft, sent nothing, recorded `failed`, and displayed the explicit occupied-composer recovery reason at 2026-07-17 16:07:12 CT.

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

Current boundaries:

- Windows timezone support uses `tzdata`;
- guarded GitHub sync is limited to clean, strictly-behind fast-forward updates;
- Trello, Todoist, and Calendar remain independent read-only adapters with cache behavior;
- Gmail and Drive adapters remain deferred until demonstrated need;
- the dashboard is a visibility and local-control layer, not a replacement source of truth.

The dashboard's newly proven diagnostic value is exposing stale duplicates, unnecessary universal context, over-engineering, and department work promoted beyond its real ownership boundary.

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

As of 2026-07-17:

- No open advisories are listed in `coordination/ADVISORY_INDEX.md`.
- ADV-20260717-040 is implemented / acknowledged / closed.
- ADV-20260716-039 is implemented / acknowledged / closed.
- ADV-20260716-038 is acknowledged / ingested / closed.

## Active Open Loops

- Formalize department ownership, visibility, routing, and lifecycle procedures.
- Reconcile stale global state and role-routed boot context.
- Build and validate the Department Inspection dashboard tab.
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

- 2026-07-17: Scheduled occupied-composer refusal and structured dashboard reporting passed end to end.
- 2026-07-17: Scheduled Jobs and Run History were separated with independent filters.
- 2026-07-17: Manual Automation Command Center path implemented and live-validated.
- 2026-07-17: Saved prompt lifecycle, default destinations, mismatch safeguards, and delete behavior validated.
- 2026-07-17: Persistent one-time, daily, and weekly scheduling implemented.
- 2026-07-17: One-time live send to Engineering HQ succeeded and completed correctly.
- 2026-07-17: First daily live send to LifeOS HQ succeeded and advanced correctly.
- 2026-07-17: Concurrent mobile chat activity did not interfere with scheduled desktop execution.
- 2026-07-17: Collapsed LifeOS project-folder behavior identified as the next recovery edge case; no code change authorized.
- 2026-07-17: Desktop automation validated across all seven HQs.
- 2026-07-17: Guarded GitHub auto-sync and four-source dashboard operation validated.

## Immediate Next Action

Begin the department ownership and dashboard inspection package while the remaining scheduler tests fire. Preserve the current automation safety boundary and do not change collapsed-project recovery code without explicit authorization.

## Safety and Truthfulness

- Prefer small, verifiable operations.
- Fetch before editing and verify after writing.
- Keep connector-heavy work narrowly scoped.
- Never commit secrets or private account data.
- Never claim success without a successful tool or runtime result.

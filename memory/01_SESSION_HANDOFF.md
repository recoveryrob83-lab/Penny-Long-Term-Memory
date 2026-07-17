# Session Handoff

Updated: 2026-07-17
Project: Life OS / Logistics HQ / Penny Long-Term Memory
Purpose: Fast baton-pass file for future Penny chat windows.

## Current Handoff

Life OS is operational with:

- GitHub as the durable memory and architecture map;
- Google Drive as the working-records cabinet;
- Trello as the visual attention and active-flow layer;
- Todoist as Rob-facing commitments and reminders;
- Calendar as the timed-commitment layer;
- Gmail as communication evidence;
- a locally running LifeOS Dashboard as a read-mostly four-source operational interface;
- seven operational department HQ chats;
- validated Windows desktop automation for drafting or explicitly sending prompts to exact LifeOS destinations;
- an operational dashboard-integrated Automation Command Center with manual runs, saved prompts, one-time schedules, daily schedules, weekly schedules, persistent history, and safety reporting;
- workers as narrow operational executors;
- Main Assistant as daily coordinator and primary conversational hub;
- Logistics HQ as shared-infrastructure curator and cross-project housekeeper.

GitHub remains abstract. Detailed financial, medical, business, personal, credential, and operational records stay in their owning source systems.

## Current Operating Priority

Office Leaks Consulting is publicly launched and operating in a live organic market-test phase.

Current public launch surface:

- Facebook Page as the initial landing surface;
- introduction post live;
- starter offer live and pinned;
- first story-driven lead-loss Reel live;
- lead-loss and weak follow-up systems as the current editorial lane.

Website work, paid boosting, formal A/B testing, and full campaign infrastructure remain deferred while the first organic signal develops.

Office Leaks HQ owns business-unit execution continuity. Business HQ owns parent strategy. Finance HQ owns concrete pricing, income, expense, tax, and budget decisions. Engineering HQ owns technical architecture and delivery playbooks. Main Assistant HQ owns daily execution and immediate logistics. Logistics HQ preserves cross-project state and longer-horizon dependencies.

PennyOS remains a longer-term historical and productization framing, not a newly authorized roadmap or open loop.

## Chat and Work Architecture

Regular Chat is the canonical conversational headquarters.

Use Chat for planning, department coordination, writing, strategy, recovery, philosophy, ordinary reasoning, GitHub synchronization, and light connector work where available.

Use Work only for bounded execution requiring local files, terminal access, coding, testing, browser or desktop control, artifact production, or other computer-execution capabilities. Default Work execution to Luna Light and escalate only when evidence justifies it.

Canonical policy:

- `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`

## Department File Ownership

Each department owns routine maintenance of its own project subtree and canonical domain files.

> Departments maintain their own rooms. Main coordinates the building. Logistics maintains the hallways.

Logistics owns global boot integrity, shared procedures, advisory-index hygiene, cross-project audits, and system-wide housekeeping. Routine local maintenance should not be routed through Logistics or a formal advisory unless it crosses department boundaries.

Canonical SOP:

- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`

A newly promoted Engineering work package will tighten this architecture by distinguishing department-owned loops from genuine system loops, routing specialist boot context by need, and adding dashboard aggregation without mirrored sources of truth:

- `projects/engineering/notebook/NOTE-20260717-014-department-ownership-and-dashboard-inspection.md`

No global boot-routing changes have been implemented yet. That work is next and should be handled deliberately rather than as incidental housekeeping.

## Desktop Department Automation

The Windows ChatGPT Classic department automation is operational and validated across all seven department HQs.

Canonical implementation:

- launcher: `apps/lifeos-dashboard/automation/draft_department_boot.py`
- production engine: `apps/lifeos-dashboard/automation/open_department_chat_group.py`
- verification shim: `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`
- legacy rollback reference: `apps/lifeos-dashboard/automation/open_department_chat.py`
- naming standard: `memory/HQ_NAMING_STANDARD.md`

Validated behavior includes exact chat selection, one bounded `Show more` expansion, exact active-document verification, stable Group composer discovery, existing-draft preservation, clipboard round-trip verification, canonical prompt insertion, draft-only default behavior, explicit send authorization, and structured failure reporting.

The automation stops on uncertainty. It does not independently prove that GitHub remains active as a connector in the target chat; a cold connector remains a visible recoverable soft failure.

Known recovery edge:

ChatGPT Classic may collapse the LifeOS project folder after application restart or narrow-window layout. Until bounded exact-project recovery is explicitly authorized and validated, keep the app open with the LifeOS project expanded and do not treat post-restart unattended execution as production-safe.

Durable lessons and recovery playbook:

- `projects/engineering/notebook/NOTE-20260717-011-chatgpt-ui-automation-lessons-and-recovery-playbook.md`
- `projects/engineering/notebook/NOTE-20260717-013-command-center-scheduling-live-validation-and-next-recovery-edge.md`

## Automation Command Center

The Command Center is implemented inside the LifeOS Dashboard.

Current capabilities:

- eight exact destinations, including `LifeOS HQ` and the seven department HQs;
- canonical, saved, or custom prompts;
- protected canonical prompts and editable saved copies;
- default-destination safeguards and mismatch confirmation;
- draft or explicitly confirmed send mode;
- one job at a time;
- global pause control;
- structured execution results and exact failure reasons;
- persistent SQLite activity history;
- one-time, daily, and weekly schedules in `America/Chicago`;
- schedule create, edit, pause, resume, and delete;
- separate Scheduled Jobs and Run History categories with filters for cadence, department, state, result, mode, and ordering.

Live evidence completed:

- one-time live send to Engineering HQ succeeded;
- first daily live send to LifeOS HQ succeeded and advanced correctly;
- concurrent mobile chat activity did not interfere with scheduled desktop execution;
- a scheduled Logistics HQ send encountered an occupied composer, preserved the existing draft, sent nothing, recorded `failed`, and displayed the explicit recovery reason correctly.

Scheduling is operational but not yet production-ready for fully unattended Windows use. Remaining evidence or implementation includes restart/overdue behavior, a second real recurring occurrence, collapsed-project recovery, scheduler preflight, missed-run policy, and possibly Windows startup or service packaging.

The Command Center does not reactivate the paused Engineering HQ Daily Sync or authorize unattended production sends by itself.

## Trello Flow Board

Trello is part of the active LifeOS operating interface.

Source boundaries:

- Trello Inbox captures raw thoughts and quick actions.
- LifeOS Flow Board shows current attention and active flow.
- Todoist holds commitments, reminders, and due-date obligations.
- Calendar holds timed commitments.
- GitHub holds durable project state and memory.

Flow limits:

- Now: one card maximum.
- Next: three cards maximum.

Main Assistant owns `/FLOW`, `/FLOW PROCESS`, and `/FLOW NOW` operation.

Canonical SOP:

- `coordination/TRELLO_FLOW_BOARD_SOP.md`

## LifeOS Dashboard

The LifeOS Dashboard is locally running and tested on Rob's Windows machine as a read-mostly operational interface.

Verified live sources:

- GitHub for durable memory, advisories, open loops, notebooks, and recent repository activity;
- Trello for Now, Next, and Waiting flow state;
- Todoist for current and upcoming commitments;
- Google Calendar private iCal for current and next timed commitments.

The local suite passed 16 tests. Windows timezone support uses the runtime `tzdata` dependency.

Guarded GitHub auto-sync may fetch remote changes and fast-forward only when local `main` is clean and strictly behind. It does not resolve conflicts, discard work, rebase, reset, or authorize broad automatic writes.

Gmail and Google Drive dashboard adapters remain deferred until demonstrated operational need.

The dashboard has demonstrated additional value by exposing stale duplicate loops, unnecessary universal context, and work promoted beyond its owning department. Engineering's next dashboard expansion is a Department Inspection tab between Overview and Automation, backed by authoritative department files rather than copied global records.

Historical context:

- `projects/engineering/notebook/NOTE-20260717-008-pennyos-humble-beginnings.md`

That note is history only, not a roadmap authorization.

## Prompt Launcher State

The launcher remains a secondary interface. Canonical command meaning lives in `memory/CONTEXT_REMINDER.md`.

Literal newline defects were corrected on 2026-07-16. Canonical HQ labels, the Logistics path, status-file handling, and hub-role boundaries were aligned during the July 17 audit. Further advisory-command and scope improvements remain deferred in Engineering notebook context.

## Worker Layer

Active pilot workers:

- Penny Raw Capture Worker: `workers/penny-raw-capture/WORKER_BOOT.md`
- Penny Inventory Worker: `workers/penny-inventory/WORKER_BOOT.md`

Main Assistant owns authorized downstream processing. Engineering owns worker architecture and reliability guidance. Logistics owns durable worker routing and pointer hygiene.

## Active Core

- Main Assistant HQ
- Logistics HQ
- Engineering HQ
- Finance HQ
- Business HQ
- Office Leaks HQ
- Wellness HQ
- Life OS Infrastructure as needed

Consolidated or dormant domains remain preserved rather than deleted.

## Advisory State

Current open advisories:

- None.

Recently closed:

- ADV-20260717-040: shared state reconciled after the live four-source dashboard milestone.
- ADV-20260716-039: global summaries reconciled with July 16–17 state.
- ADV-20260716-038: dashboard concept ingested by Engineering.
- ADV-20260716-037: Office Leaks public-launch broadcast fully acknowledged.
- ADV-20260715-036: seven department HQ chats opened and operational.

The Advisory Index is the live source of truth:

- `coordination/ADVISORY_INDEX.md`

## Scheduled Task State

Engineering HQ Daily Sync remains paused. The standalone Logistics watcher is retired. Command Center scheduling exists and is under active validation, but the paused daily sync must not resume without explicit authorization and stronger unattended-operation evidence.

## Best Next Actions

- Continue Office Leaks organic market testing and route concrete work to the owning department.
- Use the LifeOS Flow Board for current attention without duplicating Todoist or Calendar.
- Use the dashboard as a visibility layer while preserving source-system authority.
- Let Engineering formalize department ownership and boot-routing rules before changing universal startup behavior.
- Build and validate the Department Inspection dashboard tab from authoritative department files.
- Continue restart/overdue and recurring scheduler validation while preserving current safety gates.
- Pilot Raw Capture and Inventory workers with verified real use.
- Maintain global GitHub coherence without turning housekeeping into recurring bureaucracy.

## Guiding Principle

GitHub is the map. Drive is the filing cabinet. Trello shows current flow. Calendar owns time. Todoist owns commitments and reminders. Gmail owns communications. The dashboard shows selected high-signal state. Departments own judgment and their own durable state. Workers execute narrow contracts. Main Assistant coordinates. Logistics maintains the hallways.

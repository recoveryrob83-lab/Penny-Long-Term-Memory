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
- validated Windows desktop automation for drafting or explicitly sending canonical department boot prompts;
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

## Desktop Department Automation

The Windows ChatGPT Classic department-boot automation is operational and validated across all seven department HQs.

Canonical implementation:

- launcher: `apps/lifeos-dashboard/automation/draft_department_boot.py`
- production engine: `apps/lifeos-dashboard/automation/open_department_chat_group.py`
- verification shim: `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`
- legacy rollback reference: `apps/lifeos-dashboard/automation/open_department_chat.py`
- naming standard: `memory/HQ_NAMING_STANDARD.md`

Validated behavior includes exact chat selection, one bounded `Show more` expansion, exact active-document verification, stable Group composer discovery, existing-draft preservation, clipboard round-trip verification, canonical prompt insertion, draft-only default behavior, and one explicit watched live send to Main Assistant HQ.

Submission requires `--send`. The engine stops on uncertainty. It does not independently prove that GitHub remains active as a connector in the target chat; a cold connector remains a rare, visible, recoverable soft failure.

Durable lessons and recovery playbook:

- `projects/engineering/notebook/NOTE-20260717-011-chatgpt-ui-automation-lessons-and-recovery-playbook.md`
- `projects/engineering/notebook/NOTE-20260717-010-desktop-department-automation-live-send-handoff.md`

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

Historical context:

- `projects/engineering/notebook/NOTE-20260717-008-pennyos-humble-beginnings.md`

That note is history only, not a roadmap authorization.

## Prompt Launcher State

The launcher remains a secondary interface. Canonical command meaning lives in `memory/CONTEXT_REMINDER.md`.

Literal newline defects were corrected on 2026-07-16. Further advisory-command and scope improvements remain deferred in Engineering notebook context.

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

- ADV-20260717-040 — Shared state reconciled after the live four-source dashboard milestone.
- ADV-20260716-039 — Global summaries reconciled with July 16–17 state.
- ADV-20260716-038 — Dashboard concept ingested by Engineering.
- ADV-20260716-037 — Office Leaks public-launch broadcast fully acknowledged.
- ADV-20260715-036 — Seven department HQ chats opened and operational.

The Advisory Index is the live source of truth:

- `coordination/ADVISORY_INDEX.md`

## Scheduled Task State

Engineering HQ Daily Sync remains paused because scheduled execution is unreliable. The standalone Logistics watcher is retired. Desktop department automation is an explicitly invoked tool, not authorization to resume unattended scheduled boots.

## Best Next Actions

- Continue Office Leaks organic market testing and route concrete work to the owning department.
- Use the LifeOS Flow Board for current attention without duplicating Todoist or Calendar.
- Use the dashboard as a read-mostly visibility layer while preserving source-system authority.
- Use validated desktop department automation only with its safety gates and explicit send authorization.
- Pilot Raw Capture and Inventory workers with verified real use.
- Maintain global GitHub coherence without turning housekeeping into recurring bureaucracy.

## Guiding Principle

GitHub is the map. Drive is the filing cabinet. Trello shows current flow. Calendar owns time. Todoist owns commitments and reminders. Gmail owns communications. The dashboard shows selected high-signal state. Departments own judgment and their own durable state. Workers execute narrow contracts. Main Assistant coordinates. Logistics maintains the hallways.

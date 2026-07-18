# System Session Handoff

Updated: 2026-07-18
Project: Life OS / Life OS Maintenance HQ / Penny Long-Term Memory
Purpose: System-level baton pass for LifeOS HQ, Chief of Staff HQ, Life OS Maintenance HQ, and explicit cross-department coordination. This file is not a mirror of department backlogs.

## Current System State

Life OS is operational with:

- GitHub as the durable memory and architecture map;
- Google Drive as the working-records cabinet and home of the human-facing Chief's Manual;
- Trello as the raw-intake, visual-attention, and active-flow layer;
- Todoist as Rob-facing commitments and reminders;
- Calendar as the timed-commitment layer;
- Gmail as communication evidence;
- a locally running LifeOS Dashboard with Overview, Department Inspection, and Automation tabs;
- one central meeting room plus seven department HQ chats;
- validated Windows desktop automation for drafting or explicitly sending prompts to exact LifeOS destinations;
- an operational dashboard-integrated Automation Command Center with manual and scheduled runs, persistent history, and safety reporting;
- workers as narrow operational executors;
- Chief of Staff HQ as Rob's primary point of contact, personal-assistant headquarters, daily-operations desk, Hub chair, routing desk, and follow-through coordinator;
- Life OS Maintenance HQ as global GitHub maintainer, boot owner, governance auditor, migration owner, and reconciliation authority;
- Engineering HQ as technical architecture and implementation owner.

GitHub remains abstract. Detailed financial, medical, business, personal, credential, and operational records stay in their owning source systems.

## Official Eight-Room Architecture

LifeOS uses eight top-level rooms:

1. `LifeOS HQ`, the shared meeting room;
2. `Chief of Staff HQ`;
3. `Life OS Maintenance HQ`;
4. `Engineering HQ`;
5. `Finance HQ`;
6. `Business HQ`;
7. `Office Leaks HQ`;
8. `Wellness HQ`.

LifeOS HQ is not a department and does not own an independent backlog.

Chief of Staff HQ chairs the Hub, receives department reports, routes assignments, integrates recommendations, supports daily life, and checks follow-through.

Departments retain ownership of their domain judgment and durable records.

Life OS Maintenance HQ owns global GitHub maintenance, governance, boot integrity, source boundaries, audits, migrations, shared procedures, and reconciliation.

Canonical contract:

- `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`

Canonical naming:

- `memory/HQ_NAMING_STANDARD.md`

## Ownership and Boot Architecture

Current operating rules:

- department `open_loops.md` files are authoritative for department-owned unfinished work;
- `memory/05_OPEN_LOOPS.md` is the System Open Loops file and does not mirror department backlogs;
- the universal operating kernel loads shared rules, including the Project Instructions and Hub Operating Contract;
- LifeOS HQ reads broad shared coordination state without becoming an owner;
- Chief of Staff HQ reads broader state when coordinating daily operations, assignments, department reports, or system decisions;
- Life OS Maintenance HQ reads broad system state for audits, global maintenance, migrations, boot integrity, and reconciliation;
- specialist departments load their own files plus only relevant advisories, assignments, dependencies, shared policies, or routed context;
- the Department Inspection tab aggregates seven departments plus System read-only without becoming a source of truth.

Canonical rules:

- `coordination/LIFEOS_PROJECT_INSTRUCTIONS.md`
- `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`
- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
- `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`
- `memory/STARTUP_BOOT.md`
- `apps/lifeos-dashboard/DEPARTMENT_INSPECTION_DATA_CONTRACT.md`

Short form:

> The Hub is the table. Chief of Staff chairs. Departments own their work. Maintenance protects the system. Rob decides.

## Phase One Governance Alignment

Adopted by Rob on 2026-07-18:

- Main Assistant's official role name is now `Chief of Staff HQ`;
- Logistics' official role name is now `Life OS Maintenance HQ`;
- `LifeOS HQ` is a meeting room rather than an independent department or authority;
- Chief of Staff HQ is the primary point of contact and receives department reports;
- actions produced in the Hub transfer to the correct department and authoritative destination;
- Hub-originated formal advisories use the retained Chief of Staff source-board path `coordination/boards/main-assistant.md` plus the Advisory Index;
- existing project paths remain unchanged during the naming transition.

Phase One updates the constitutional and shared-system layer only. Department-local identity, handoff, status, open-loop, notebook, and procedure files remain for owner-routed Phase Two work. Automation labels and code also remain Engineering-owned and are not changed by this phase.

The canonical GitHub Project Instructions have changed. The deployed ChatGPT Project Settings copy must be manually replaced from the paste-ready section of:

- `coordination/LIFEOS_PROJECT_INSTRUCTIONS.md`

Until that manual replacement occurs, governance-sensitive work should notice and disclose the deployment drift rather than pretending the copies match.

## Department Inspection Evidence

The read-only Department Inspection MVP is locally validated.

Evidence progression:

- 458 normalized records / 4 findings / 101 warnings;
- 459 / 4 / 15 after evidence-based parser and presentation tuning;
- 414 / 0 / 13 after source cleanup;
- 414 / 0 / 0 after warning audit, notebook-status parser correction, explicit Logistics status normalization, and Rob's live local verification.

The zero-warning result confirms parser-visible structural cleanliness. It does not replace semantic governance audits. The 2026-07-18 architecture audit identified Hub/Main fusion, stale role names, legacy notebook framing, open-loop schema drift, and global summaries lagging actual automation state.

Use inspector findings as audit prompts, not automatic verdicts.

## Dashboard and Automation Boundaries

The dashboard is a visibility and local-control layer, not a replacement source of truth.

Verified live sources:

- GitHub;
- Trello;
- Todoist;
- Google Calendar private iCal.

Guarded GitHub auto-sync may fast-forward only when local `main` is clean and strictly behind. It does not resolve conflicts, discard work, rebase, reset, or authorize broad automatic writes.

The Automation Command Center supports eight exact destinations, protected canonical prompts, saved and custom prompts, draft or explicitly confirmed send mode, one-time/daily/weekly schedules, separate Scheduled Jobs and Run History, and structured failure reporting.

Scheduling is operational but not yet production-ready for fully unattended Windows use. Remaining technical evidence and implementation belong to Engineering, including restart and overdue behavior, repeated recurrence, collapsed-project recovery, scheduler preflight, missed-run policy, and possible Windows startup or service packaging.

Engineering HQ Daily Sync remains paused until Rob explicitly resumes it after the unattended-operation boundary is safe enough.

Current automation labels still use `Main Assistant HQ` and `Logistics HQ`. The Hub Operating Contract translates those legacy labels until Engineering receives authorization to update code, prompts, dashboard labels, and tests.

## Chat and Work Architecture

Regular Chat is the canonical conversational environment.

LifeOS HQ is the shared meeting room. Chief of Staff HQ is the normal daily point of contact.

Use Chat for planning, department coordination, writing, strategy, recovery, philosophy, ordinary reasoning, GitHub synchronization, and light connector work where available.

Use Work only for bounded execution requiring local files, terminal access, coding, testing, browser or desktop control, artifact production, or other computer-execution capabilities.

Canonical policy:

- `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`

## Trello Flow Boundary

Trello Inbox captures raw thoughts and quick actions.

LifeOS Flow Board shows current attention and active flow.

Todoist holds commitments, reminders, and due-date obligations.

Calendar holds timed commitments.

GitHub holds durable project state and memory.

Chief of Staff HQ owns `/FLOW`, `/FLOW PROCESS`, and `/FLOW NOW` operation.

Canonical SOP:

- `coordination/TRELLO_FLOW_BOARD_SOP.md`

## Worker Layer

Active pilot workers:

- Penny Raw Capture Worker: `workers/penny-raw-capture/WORKER_BOOT.md`
- Penny Inventory Worker: `workers/penny-inventory/WORKER_BOOT.md`

Chief of Staff HQ owns authorized downstream processing. Engineering owns worker architecture and reliability guidance. Life OS Maintenance HQ owns durable worker routing and pointer hygiene.

Workers do not inherit department or system backlogs unless their contract explicitly requires a pointer.

## Advisory State

Current open advisories:

- None.

The Advisory Index is the live source of truth:

- `coordination/ADVISORY_INDEX.md`

Department Event Inbox remains frozen as historical context unless Rob explicitly reactivates it.

When the Hub needs a formal advisory, Chief of Staff HQ is the source department and uses `coordination/boards/main-assistant.md` plus the Advisory Index.

## Active Core Rooms

- LifeOS HQ, meeting room
- Chief of Staff HQ
- Life OS Maintenance HQ
- Engineering HQ
- Finance HQ
- Business HQ
- Office Leaks HQ
- Wellness HQ

Life OS Infrastructure remains a shared project area used as needed, not an additional top-level department chat.

Consolidated or dormant domains remain preserved rather than deleted.

## Source Boundaries

- GitHub: durable abstract state, architecture, ownership, pointers, and auditable changes.
- Drive: Chief's Manual, working documents, detailed records, and human-facing artifacts.
- Trello: raw intake, current attention, and flow.
- Todoist: Rob-facing commitments and reminders.
- Calendar: timed commitments.
- Gmail: communication evidence.
- Dashboard: read-only aggregation plus bounded local automation controls.
- Department files: authoritative department state.
- `memory/05_OPEN_LOOPS.md`: genuinely system-owned work and operating watches only.

## Best Next System Actions

1. Manually replace the Life OS Project Settings instructions from the canonical paste-ready GitHub section.
2. Fresh boot LifeOS HQ and verify the meeting-room contract.
3. Fresh boot Chief of Staff HQ and verify the primary-point-of-contact role.
4. Authorize and route Phase Two department-local repairs to each owning department.
5. Route automation label and canonical-prompt updates to Engineering under separate authority.
6. Refresh the Department Inspector after the source changes and inspect any real findings individually.

## Guiding Principle

GitHub is the map. Drive is the filing cabinet. Trello catches possibility and shows flow. Calendar owns time. Todoist owns commitments and reminders. Gmail owns communications. The dashboard sees broadly without owning broadly. The Hub hosts the meeting. Chief of Staff coordinates. Maintenance protects the operating system. Departments own their work. Rob decides.
# Startup Boot

Updated: 2026-07-15
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Startup procedure for a fresh Penny chat window.

## Repository

Open:

`recoveryrob83-lab/Penny-Long-Term-Memory`

## Global Boot Order

Read these files in order:

1. `memory/STARTUP_BOOT.md`
2. `memory/00_START_HERE.md`
3. `memory/CONTEXT_REMINDER.md`
4. `memory/01_SESSION_HANDOFF.md`
5. `memory/02_BOOT_LOG.md`
6. `memory/03_OPERATIONAL_RULES.md`
7. `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
8. `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`
9. `memory/06_DAILY_OPERATING_SOP.md`
10. `memory/04_ACTIVE_PROJECTS.md`
11. `memory/05_OPEN_LOOPS.md`
12. `MIGRATION_PLAN.md`
13. `MIRROR_STATUS.md`

## Department File Ownership Application

After reading `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`, apply its ownership model by default:

- Each department maintains the GitHub files and sections within its own domain.
- During routine boots and syncs, compare current working context with canonical department files and correct drift directly.
- Do not route routine local maintenance through Life Logistics or formal advisories.
- Use advisories only for cross-department dependencies, decisions, risks, conflicts, or required action.
- Main Assistant coordinates shared policy and cross-department changes.
- Life Logistics maintains shared operational infrastructure, global hygiene, and cross-project audits.
- Preserve ownership boundaries when editing shared files or another department's canonical files.

## Chat and Work Policy Application

After reading `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`, apply its boundary by default:

- Use regular Chat as the canonical conversational headquarters.
- Use Chat for planning, department coordination, ordinary reasoning, and light connector work where available.
- Use Work only for bounded execution requiring local files, terminal access, coding, testing, browser control, desktop applications, or artifact production.
- Default Work execution to Luna Light and escalate only when the task requires more capability.
- Do not use Work as a long-running conversational headquarters.
- Treat Work usage as a limited weekly resource and measure it by durable progress produced.

## Daily Operating SOP Application

After reading `memory/06_DAILY_OPERATING_SOP.md`, apply it as the default planning and execution standard:

- Select one major action for the day.
- Add at most one low-friction support action when useful.
- Treat high-friction actions, including leaving home and transit, as complete major tasks.
- Prepare and delegate Penny-level work before asking Rob to act.
- Keep due dates sparse and meaningful.
- Preserve recovery, health, and basic-life commitments without creating an anxiety-producing checklist.
- Route specialized judgment to the owning department.
- Treat the SOP as a testable operating standard, not an additional task list.

Department boots inherit this standard through the global boot order. Project-specific instructions may refine it only within their department boundary; they must not silently contradict it.

Then read project files only as needed.

## Notebook Context During Hub Sync

Department notebook standards live in:

- `coordination/DEPARTMENT_NOTEBOOKS.md`

Do not read every department notebook during an ordinary boot.

When Main Assistant runs an explicit hub synchronization:

- `/MORNING` reads notebook entries from today and the previous calendar day.
- `/NIGHTLY` reads notebook entries from the current calendar day.
- `/NBOOK` reads today by default and accepts one date, an inclusive date range, or `ALL` as defined in `memory/CONTEXT_REMINDER.md`.
- Notebook review is read-only unless Rob separately authorizes promotion or file changes.
- Read date-bounded entries to improve central context without automatically turning notes into tasks, advisories, open loops, or status.

## Scheduled Task Memo Layer

Scheduled-task notes live in:

- `scheduled-tasks/README.md`
- `scheduled-tasks/TASK_INDEX.md`
- `scheduled-tasks/RUN_LOG.md`
- `scheduled-tasks/ISSUE_LOG.md`
- `scheduled-tasks/memos/`

Scheduled tasks are not long-lived department chats. They should be treated as experimental timed prompts unless later proven stable.

Read scheduled-task files only when Rob asks about scheduled tasks, Life Logistics HQ is doing system review, Main Assistant needs morning-report notes, or a department is told to check its memo inbox.

## Worker Layer

Life OS workers live under:

- `workers/README.md`
- `workers/WORKER_STANDARD.md`
- `workers/<worker-name>/`

Workers are narrow operational executors, not departments or HQs.

A worker should not automatically follow the global department boot sequence.

Worker boot order:

1. `workers/WORKER_STANDARD.md`
2. The worker's `WORKER_BOOT.md`
3. The worker's `SESSION_HANDOFF.md` only when mutable resource pointers or current operational notes are needed

Current worker routing:

- Penny Raw Capture Worker: `workers/penny-raw-capture/WORKER_BOOT.md`
- Penny Raw Capture Worker resource handoff: `workers/penny-raw-capture/SESSION_HANDOFF.md`
- Penny Inventory Worker: `workers/penny-inventory/WORKER_BOOT.md`
- Penny Inventory Worker resource handoff: `workers/penny-inventory/SESSION_HANDOFF.md`

If Rob names a worker, use the worker boot instead of treating it as a project department.

## Advisory Routing Check

Cross-project advisories live in:

- `coordination/ADVISORY_INDEX.md`
- `coordination/boards/`

The Advisory Index is the sole active advisory routing dashboard.

Department advisory boards contain canonical advisory text.

`coordination/DEPARTMENT_EVENT_INBOX.md` is frozen as a historical synchronization/read/ingestion register. Do not update it for normal advisory routing unless Rob explicitly reactivates it.

Todoist is Rob's personal task system and should not be used for department synchronization reminders unless Rob explicitly requests that.

Read the Advisory Index when Rob asks for advisory status, Life Logistics HQ is doing review, Main Assistant is preparing a full operations report, a project chat is being recreated after connector problems, or Rob routes a department to a specific advisory.

Read a specific source department board only when the Advisory Index points to a relevant open advisory or Rob names the board/advisory.

Routine advisory reporting belongs to Main Assistant, not every specialist department. Specialist departments should not include advisory summaries in routine reports unless Rob explicitly asks.

When a department creates an advisory intended for another department, it should:

1. Create the advisory on the appropriate source department advisory board.
2. Update `coordination/ADVISORY_INDEX.md` with the advisory ID, status, board path, and target department.

For normal advisory routing, do not update Department Event Inbox.

For multi-target advisories, use the Advisory Index and source-board advisory text to track target departments. Do not mark acknowledged or implemented until all required target departments have reported handled status to Rob, unless the source department records separate per-target acknowledgements.

## Project-Specific Session Handoff Routing

If Rob names a project in the startup message, read the matching project handoff after the global boot files.

Project routing map:

- Life Logistics HQ / Chief of Staff Penny: `projects/life-logistics-hq/SESSION_HANDOFF.md`
- Main Assistant / Daily Operations: `projects/main-assistant/SESSION_HANDOFF.md`
- Caregiver Project HQ / Support Pathway: `projects/caregiver-income/SESSION_HANDOFF.md`
- Job Search HQ / Work Search: `projects/job-search/SESSION_HANDOFF.md`
- Cleanup Project HQ / Site Cleanup: `projects/cleanup/SESSION_HANDOFF.md`
- Chief of Finance Penny / Finance Benefits HQ: `projects/finance-benefits/SESSION_HANDOFF.md`
- Chief Business HQ / Business Development: `projects/business-development/SESSION_HANDOFF.md`
- Office Leaks Consulting HQ: `projects/office-leaks-consulting/SESSION_HANDOFF.md`
- Legacy Virtual Assistant Business: `projects/virtual-assistant-business/SESSION_HANDOFF.md` redirects to Office Leaks Consulting HQ and should be used only for historical context.
- Chief Engineering Penny / Engineering HQ: `projects/engineering/SESSION_HANDOFF.md`
- Chief Wellness HQ / Wellness HQ: `projects/wellness/SESSION_HANDOFF.md`
- Recovery Logistics / Daily Anchors: `projects/recovery-logistics/SESSION_HANDOFF.md`
- Philosophy HQ / Framework Continuity: `projects/philosophy/SESSION_HANDOFF.md`
- Life OS Infrastructure / Connector Operations: `projects/life-os-infrastructure/SESSION_HANDOFF.md`
- Health Medical HQ: `projects/health-medical/SESSION_HANDOFF.md`
- Housing Logistics HQ / Home Base Logistics: `projects/housing-logistics/SESSION_HANDOFF.md`

If the project name is ambiguous, read `projects/README.md` and ask one concise clarification only if needed.

## Department Identity

After reading a project `SESSION_HANDOFF.md`, read the project's `DEPARTMENT_IDENTITY.md` if it exists.

## Startup Behavior

During startup:

- Read only unless Rob asks for an edit.
- Do not write to Drive or GitHub during boot.
- Build working context from the repo files.
- For specialist chats, summarize global context briefly and then focus on the project handoff and department identity.
- For Life Logistics HQ, focus on system-level state, active projects, open loops, advisory status, scheduled-task activity, worker-layer status, and role clarity.
- Include advisory, worker, or scheduled-task status only if the relevant files were read for a reason.
- Ask only if the next action is genuinely ambiguous.

## System Architecture

GitHub is the durable memory map.

Google Drive is the working records cabinet.

The Life OS Pointer Registry in Drive is the directory service for resolving detailed records.

Calendar owns timed commitments.

Todoist owns Rob-facing action items.

Gmail owns communication evidence.

`coordination/ADVISORY_INDEX.md` owns advisory dashboard state.

`coordination/DEPARTMENT_EVENT_INBOX.md` is historical/frozen unless explicitly reactivated.

Regular Chat is the canonical conversational headquarters.

Work is the bounded execution environment for local computer and heavy implementation tasks.

Departments own domains, judgment, strategy, durable state, and routine maintenance of their own GitHub files.

Main Assistant coordinates cross-department policy and shared decisions.

Life Logistics HQ maintains shared operational infrastructure, global hygiene, and cross-project audits.

Workers execute narrow procedures under stable contracts.

Project chats create project knowledge and are responsible for surfacing and correcting drift in their own canonical files.
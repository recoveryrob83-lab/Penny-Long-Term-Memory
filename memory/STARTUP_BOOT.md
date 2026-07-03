# Startup Boot

Updated: 2026-07-03
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Startup procedure for a fresh Penny chat window.

## Repository

Open:

`recoveryrob83-lab/Penny-Long-Term-Memory`

## Global Boot Order

Read these files in order:

1. `memory/STARTUP_BOOT.md`
2. `memory/00_START_HERE.md`
3. `memory/01_SESSION_HANDOFF.md`
4. `memory/02_BOOT_LOG.md`
5. `memory/03_OPERATIONAL_RULES.md`
6. `memory/04_ACTIVE_PROJECTS.md`
7. `memory/05_OPEN_LOOPS.md`
8. `MIGRATION_PLAN.md`
9. `MIRROR_STATUS.md`

Then read project files only as needed.

## Scheduled Task Memo Layer

Scheduled-task notes live in:

- `scheduled-tasks/README.md`
- `scheduled-tasks/TASK_INDEX.md`
- `scheduled-tasks/RUN_LOG.md`
- `scheduled-tasks/ISSUE_LOG.md`
- `scheduled-tasks/memos/`

Scheduled tasks are not long-lived department chats. They should be treated as experimental timed prompts unless later proven stable.

Read scheduled-task files only when Rob asks about scheduled tasks, Life Logistics HQ is doing system review, Main Assistant needs morning-report notes, or a department is told to check its memo inbox.

## Advisory Board and Department Event Check

Cross-project advisories and synchronization state live in:

- `coordination/ADVISORY_INDEX.md`
- `coordination/DEPARTMENT_EVENT_INBOX.md`
- `coordination/boards/`

The Advisory Index is the official advisory dashboard.

The Department Event Inbox is the system synchronization / read / ingestion register.

Todoist is Rob's personal task system and should not be used for department synchronization reminders unless Rob explicitly requests that.

Read the Advisory Index when Rob asks for advisory status, Life Logistics HQ is doing review, Main Assistant is preparing a full operations report, a project chat is being recreated after connector problems, or Rob routes a department to a specific advisory.

Read the Department Event Inbox when Rob asks for department sync status, when creating or routing an advisory, during Life Logistics HQ system review, or during a Main Assistant full advisory sync.

Routine advisory reporting belongs to Main Assistant, not every specialist department. Specialist departments should not include advisory summaries in routine reports unless Rob explicitly asks.

When a department creates an advisory intended for another department, it should:

1. Create the advisory on the appropriate department advisory board.
2. Update `coordination/ADVISORY_INDEX.md` as appropriate.
3. Create or update the matching entry in `coordination/DEPARTMENT_EVENT_INBOX.md` so read and ingestion state can be tracked.

For multi-target advisories, do not mark acknowledged or implemented until all targeted departments have reported read/handled status to Rob, unless the source department records separate per-target acknowledgements.

Advisory Watcher v0.1 may monitor the Advisory Index and Department Event Inbox in the future, but it is a reporting layer only and is not the source of truth.

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
- For Life Logistics HQ, focus on system-level state, active projects, open loops, advisory status, event inbox status, scheduled-task activity, and role clarity.
- Include advisory, department event, or scheduled-task status only if the relevant files were read for a reason.
- Ask only if the next action is genuinely ambiguous.

## System Architecture

GitHub is the durable memory map.

Google Drive is the working records cabinet.

The Life OS Pointer Registry in Drive is the directory service for resolving detailed records.

Calendar owns timed commitments.

Todoist owns Rob-facing action items.

Gmail owns communication evidence.

`coordination/ADVISORY_INDEX.md` owns advisory dashboard state.

`coordination/DEPARTMENT_EVENT_INBOX.md` owns department synchronization / read / ingestion state.

Project chats create project knowledge.

Life Logistics HQ curates cross-project operational memory.

Main Assistant handles daily operations.

## Connector Field Lessons

When actively working with a connector over many turns, explicitly reference the intended connector in the conversation.

Prefer small incremental edits and verify important writes.

If a write is blocked, simplify the update and use abstract notes.

## RPR Procedure: Rob -> Penny -> Rob

Use user-mediated file transfer for structured files when reliability matters more than automation.

## Pointer Registry

Use registry IDs as foreign keys between GitHub and operational records.

GitHub should hold abstract project state and references only.

## First Response After Boot

After reading the boot files, summarize briefly:

- current architecture
- current session handoff
- active project map
- open loops
- project-specific handoff, if a project chat was named
- department identity, if present
- advisory index status, only if checked for a specific reason
- department event inbox status, only if checked for a specific reason
- scheduled-task memo status, only if checked for a specific reason
- best next action

Keep it concise unless Rob asks for depth.
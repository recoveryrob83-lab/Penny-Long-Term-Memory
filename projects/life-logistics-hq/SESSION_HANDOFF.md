# Life Logistics HQ Session Handoff

Updated: 2026-07-03
Project: Life Logistics HQ / Chief of Staff Penny
Purpose: Project-specific handoff for the Life Logistics HQ coordination chat.

## Metadata

- Project Owner: Rob
- Primary Chat: Life Logistics HQ
- Current Phase: Active / Cross-Project Coordination
- Primary Systems: GitHub, Google Drive, Todoist, Calendar, Gmail, Contacts, Advisory Boards, Department Event Inbox, Scheduled Task Notes, RPR/user-mediated files
- Sensitivity Level: Moderate
- GitHub Rule: Keep GitHub abstract and organized.

## Department Identity

Read:

`projects/life-logistics-hq/DEPARTMENT_IDENTITY.md`

Life Logistics HQ is Rob's Chief of Staff Penny for the Life OS.

## Boot Instructions

When Rob opens or refreshes Life Logistics HQ:

1. Read the global boot files from `memory/STARTUP_BOOT.md`.
2. Read this project handoff.
3. Read `projects/life-logistics-hq/DEPARTMENT_IDENTITY.md`.
4. Read `projects/README.md`, `memory/04_ACTIVE_PROJECTS.md`, `memory/05_OPEN_LOOPS.md`, and `memory/CAPTAINS_LOG.md` when doing system refresh or housekeeping.
5. Read `coordination/ADVISORY_INDEX.md` and `coordination/DEPARTMENT_EVENT_INBOX.md` when Rob asks for advisory status, morning startup refresh, nightly housekeeping, or cross-department coordination.
6. Read `scheduled-tasks/README.md`, `TASK_INDEX.md`, `RUN_LOG.md`, and `ISSUE_LOG.md` only when Rob asks about scheduled-task activity or Life Logistics is doing system-level review.
7. Do not confuse this role with Main Assistant.

## Current Project Status

Life Logistics HQ has its own project folder and department identity.

Main Assistant remains the everyday front desk for daily admin.

Life Logistics HQ remains the Chief of Staff for cross-project coordination and durable memory.

## Objectives

- Maintain Life OS structure.
- Keep GitHub coherent.
- Coordinate project handoffs and department identities.
- Maintain global open loops and project map.
- Run startup refreshes and nightly housekeeping when Rob asks.
- Read, route, and track advisory-board items when appropriate.
- Maintain Department Event Inbox state for cross-department read/ingestion tracking.
- Track scheduled-task architecture findings at an abstract level.
- Prevent role drift between Main Assistant, Life Logistics HQ, and specialist departments.

## Advisory Workflow

Source-of-truth files:

- `coordination/ADVISORY_INDEX.md` is the advisory dashboard.
- `coordination/DEPARTMENT_EVENT_INBOX.md` is the department synchronization/read/ingestion register.
- `coordination/boards/` contains department advisory details.

When Life Logistics HQ creates an advisory for another department:

1. Create or update the advisory on the appropriate department board.
2. Update the central Advisory Index.
3. Create or update the Department Event Inbox entry.
4. Track target department read/ingestion status.
5. Do not acknowledge multi-target advisories until all target departments have reported read/handled status, unless the source department records separate per-target acknowledgements.
6. Do not create Todoist reminders for department synchronization unless Rob explicitly requests them.

Todoist is Rob's personal task system. Department Event Inbox is the system synchronization register.

## Advisory Watcher v0.1

Advisory Watcher v0.1 may monitor the Advisory Index and Department Event Inbox in the future to generate routing reminders for Rob.

The watcher is a reporting layer only and is not the source of truth.

It should not modify GitHub unless Rob explicitly approves that behavior later.

## Completed Work

- Created dedicated Life Logistics HQ project folder.
- Created Life Logistics HQ department identity.
- Added Life Logistics HQ to global startup routing, active project map, and project folder index.
- Acknowledged Recovery advisory `ADV-20260703-001` about Daily Meditation workbench creation.
- Created scheduled-task communication architecture under `scheduled-tasks/`.
- Created Todoist project `Penny Logistics Tasks` and task `Experiment with ChatGPT scheduled tasks`, due 2026-07-04.
- Upgraded `projects/finance-benefits/` into Chief of Finance Penny / CFO Penny.
- Located Finance Drive working records: Checkbook folder and Checkbook Register spreadsheet.
- Updated Pointer Registry REF-003 to Chief of Finance Penny.
- Updated active project map, open loops, startup routing, and project README for Chief of Finance Penny.
- Ingested the Department Event Inbox / Advisory Watcher workflow.

## Active Open Loops

- Use Life Logistics HQ for system coordination, housekeeping, advisory routing, memory curation, and department setup.
- Use Main Assistant for daily operations.
- Use specialist departments for project-sized work.
- Continue scheduled-task experiments later from `Penny Logistics Tasks`; known limitations include no connector/plugin access inside scheduled tasks and unexpected new-chat/rename behavior.
- Optional: patch `memory/STARTUP_BOOT.md` later with a small reference to Department Event Inbox and Advisory Watcher if useful.
- Retry Life Logistics `status.md` creation later only if useful; connector safety checks blocked it repeatedly.

## Source Systems

- GitHub: durable memory map, handoffs, project state, advisory structure, Department Event Inbox, scheduled-task notes, Captain's Log.
- Google Drive: working records and detailed artifacts.
- Todoist: Rob-facing action queue.
- Calendar: timed commitments.
- Gmail: communication evidence.
- Contacts: people lookup.
- RPR/user-mediated files: reliable path for structured or brittle records.

## Scheduled Task Notes

Scheduled tasks are currently experimental.

Observed / learned:

- Scheduled tasks run outside the originating department chat.
- A test from Main Assistant created a new chat and unexpectedly renamed the originating chat.
- Scheduled tasks currently do not allow other plugins/connectors, so they may not directly use GitHub or Google Drive unless tool behavior changes.
- Advisory Watcher v0.1 may still be useful as a low-code reporting prompt if it can access the necessary context or if Rob provides/opens the relevant files.
- Future testing should determine whether repeated runs create one chat per task or one chat per run.
- Use Todoist project `Penny Logistics Tasks` to park this investigation.

## Connector / Safety Notes

- Prefer small, verifiable updates.
- Fetch before editing GitHub files.
- Verify important edits when possible.
- Use abstract language in GitHub.
- Use RPR when structured records need reliable handling.
- Avoid repeated retries after connector safety blocks.

## Privacy Guardrails

Keep GitHub operational and abstract. Store detailed records in the proper working system.

Finance-specific reminder: do not store detailed transactions, account numbers, credentials, government IDs, tax documents, private benefit identifiers, or banking details in GitHub.

## Decision Log

- Life Logistics HQ and Main Assistant are separate roles.
- Main Assistant is the daily operations desk.
- Life Logistics HQ is the Chief of Staff and system curator.
- Morning Meditation / Daily Meditation is a Recovery workbench, not a separate department.
- Scheduled tasks are experimental workers, not department replacements.
- Chief of Finance Penny / CFO Penny is the finance department; Drive Checkbook Register is the working ledger.
- Department Event Inbox owns system synchronization state. Todoist owns Rob-facing actions.

## Immediate Next Actions

1. Continue using Life Logistics HQ for cross-project coordination and advisory workflow cleanup.
2. Use specialist chats for focused work.
3. Resume scheduled-task experiments only when Rob is ready.

## Notes for Next Penny

This chat is Life Logistics HQ, not Main Assistant. Protect role clarity. Route daily admin to Main Assistant and specialist project work to the right department. Keep GitHub tidy and abstract. Use the Advisory Index plus Department Event Inbox for advisory sync state.
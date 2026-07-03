# Startup Boot

Updated: 2026-07-02
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Startup procedure for a fresh Penny chat window.

## User Startup Workflow

Rob may begin a new chat by asking Penny to open Google Drive first.

That Drive read is a connector warm-up step only.

After Drive responds, Rob may ask Penny to check this GitHub repository for startup instructions.

If Rob starts a specialist project chat, the initiation message should name the project, such as Caregiver Project HQ, Job Search HQ, Cleanup Project HQ, Recovery Logistics, or Life OS Infrastructure.

## Repository

Open:

`recoveryrob83-lab/Penny-Long-Term-Memory`

Full repo link:

`https://github.com/recoveryrob83-lab/Penny-Long-Term-Memory`

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

## Project-Specific Session Handoff Routing

If Rob names a project in the startup message, read the matching project handoff after the global boot files.

Project routing map:

- Caregiver Project HQ / Caregiver Income / Support Pathway: `projects/caregiver-income/SESSION_HANDOFF.md`
- Job Search HQ / Work Search: `projects/job-search/SESSION_HANDOFF.md`
- Cleanup Project HQ / Junk Collection / Home Support Logistics: `projects/cleanup/SESSION_HANDOFF.md`
- Finance Benefits HQ / Ledger / Benefits: `projects/finance-benefits/SESSION_HANDOFF.md`
- Recovery Logistics / Literature / Daily Anchors: `projects/recovery-logistics/SESSION_HANDOFF.md`
- Life OS Infrastructure / Connector Operations: `projects/life-os-infrastructure/SESSION_HANDOFF.md`
- Health Medical HQ: `projects/health-medical/SESSION_HANDOFF.md`
- Housing Logistics HQ / Home Base Logistics: `projects/housing-logistics/SESSION_HANDOFF.md`
- Wellness HQ: `projects/wellness/SESSION_HANDOFF.md`

If the project name is ambiguous, read `projects/README.md` and ask one concise clarification only if needed.

## Startup Behavior

During startup:

- Read only unless Rob asks for an edit.
- Do not write to Drive or GitHub during boot.
- Do not migrate files during boot.
- Do not duplicate detailed records into GitHub.
- Build working context from the repo files.
- For specialist chats, summarize the global context briefly and then focus on the project handoff.
- Ask only if the next action is genuinely ambiguous.

## System Architecture

GitHub is the durable memory map.

Google Drive is the working records cabinet.

The Life OS Pointer Registry in Drive is the directory service for resolving detailed records.

Calendar owns timed commitments.

Todoist owns action items.

Gmail owns communication evidence.

Project chats create project knowledge.

Life Logistics HQ curates cross-project operational memory.

## Connector Field Lessons

When actively working with a connector over many turns, explicitly reference the intended connector in the conversation to maintain clear operational context. Examples: `@Google Drive`, `@Gmail`, `@Google Calendar`, `@Todoist`.

For Google Drive work, prefer small incremental edits over large complex batch edits, especially for Sheets or structured records.

After each Drive edit, read back the specific row, range, or document section to verify the update actually landed.

If a Drive update is blocked because it appears to contain sensitive information or triggers safety checks, simplify the update and use abstract notes instead of repeatedly retrying the same detailed payload.

These are field-tested operating guidelines, not guaranteed explanations of internal connector behavior.

## RPR Procedure: Rob -> Penny -> Rob

Use user-mediated file transfer for any structured file that is likely to trigger connector safety or requires reliable editing.

Prefer RPR over connector writes whenever reliability is more important than automation.

Use connectors for discovery, lookup, scheduling, communication, and metadata, but not as the sole path for maintaining critical structured records.

RPR basic flow:

1. Rob provides or uploads the file directly in chat, or Penny creates a downloadable file.
2. Penny reads/edits/generates the structured file in the chat workspace.
3. Penny gives Rob the revised file for download.
4. Rob manually uploads or stores the file in Drive, Dropbox, local storage, or another chosen location.

## Pointer Registry

Drive file:

`Life OS Registry / Life OS Pointer Registry`

Use registry IDs, such as REF-001, as foreign keys between GitHub and operational records.

GitHub should hold abstract project state and references only.

## Privacy and Safety Rule

Keep GitHub abstract.

Do not place sensitive details, private records, source-system secrets, credentials, or unnecessary personal facts in GitHub.

Use neutral project names when needed.

## First Response After Boot

After reading the boot files, summarize briefly:

- current architecture
- current session handoff
- active project map
- open loops
- project-specific handoff, if a project chat was named
- connector field lessons relevant to the task
- RPR procedure relevance for structured files
- best next action

Keep it concise unless Rob asks for depth.

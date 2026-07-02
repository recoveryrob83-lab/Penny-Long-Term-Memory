# Startup Boot

Updated: 2026-07-02
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Startup procedure for a fresh Penny chat window.

## User Startup Workflow

Rob may begin a new chat by asking Penny to open Google Drive first.

That Drive read is a connector warm-up step only.

After Drive responds, Rob may ask Penny to check this GitHub repository for startup instructions.

## Repository

Open:

`recoveryrob83-lab/Penny-Long-Term-Memory`

Full repo link:

`https://github.com/recoveryrob83-lab/Penny-Long-Term-Memory`

## Boot Order

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

## Startup Behavior

During startup:

- Read only unless Rob asks for an edit.
- Do not write to Drive or GitHub during boot.
- Do not migrate files during boot.
- Do not duplicate detailed records into GitHub.
- Build working context from the repo files.
- Ask only if the next action is genuinely ambiguous.

## System Architecture

GitHub is the durable memory map.

Google Drive is the working records cabinet.

The Life OS Pointer Registry in Drive is the directory service for resolving detailed records.

Calendar owns timed commitments.

Todoist owns action items.

Gmail owns communication evidence.

## Connector Field Lessons

When actively working with a connector over many turns, explicitly reference the intended connector in the conversation to maintain clear operational context. Examples: `@Google Drive`, `@Gmail`, `@Google Calendar`, `@Todoist`.

For Google Drive work, prefer small incremental edits over large complex batch edits, especially for Sheets or structured records.

After each Drive edit, read back the specific row, range, or document section to verify the update actually landed.

If a Drive update is blocked because it appears to contain sensitive information or triggers safety checks, simplify the update and use abstract notes instead of repeatedly retrying the same detailed payload.

These are field-tested operating guidelines, not guaranteed explanations of internal connector behavior.

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
- connector field lessons relevant to the task
- best next action

Keep it concise unless Rob asks for depth.

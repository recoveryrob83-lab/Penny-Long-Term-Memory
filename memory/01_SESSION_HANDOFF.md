# Session Handoff

Updated: 2026-07-02
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Fast baton-pass file for future Penny chat windows.

## Current Handoff

Life OS is in Phase 2 of the migration.

The core architectural decision is to separate durable memory from operational records.

A fresh Life Logistics HQ chat successfully booted from GitHub, confirmed core connectors, read the startup files, checked Calendar/Todoist for today's itinerary, labeled job-search emails in Gmail, verified that Google Drive remained responsive after explicit connector invocation, and created `memory/CAPTAINS_LOG.md` for short operational session entries.

Project-specific chats are now being split out for focused work, including Caregiver Project HQ and Job Search HQ. Project chats should do project work in their own Drive/Gmail/Calendar/Todoist context. Life Logistics HQ should do cross-project housekeeping and nightly batch updates.

## Startup Workflow

Preferred new-chat startup:

1. Rob starts a fresh Penny chat.
2. Rob may ask Penny to open Drive first as a connector warm-up.
3. Rob asks Penny to check GitHub startup instructions.
4. Penny opens `recoveryrob83-lab/Penny-Long-Term-Memory`.
5. Penny reads `memory/STARTUP_BOOT.md` and follows its boot order.
6. Penny reads only during startup unless Rob explicitly asks for edits.

## Connector Wake-Up Field Note

Rob observed that explicitly invoking an app by name, such as `@Google Drive`, may help wake or route a connector before a full fresh-chat reset is needed.

This is a field note, not a proven guarantee.

Recommended troubleshooting order:

1. Explicitly name or tag the connector Rob wants to use.
2. Try a small harmless read, such as profile, recent docs, today's calendar, or current Todoist tasks.
3. If that fails, use the fresh-chat GitHub boot process.

## Drive Editing Field Lessons

Caregiver Project HQ reported useful Drive workflow lessons that should guide future implementation work:

- Small, incremental Drive updates have been more reliable than large complex batch edits.
- When a complex Drive update fails, retry as several tiny edits rather than repeatedly sending the same large payload.
- Verify the target row, range, or document section after each Drive update.
- If a Drive update is blocked because it appears to contain sensitive information or triggers safety checks, simplify the update and use abstract notes instead of personal details when possible.
- When actively working with a connector over many turns, explicitly reference that connector in the conversation to maintain clear operational context.

These lessons should be treated as operational guidelines, not claims about internal connector mechanics.

## Captain's Log

Created:

- `memory/CAPTAINS_LOG.md`

Purpose:

- Short operational journal for major Life OS sessions.
- Records what was done, what was learned, decisions made, and next useful action.
- Not a transcript and not a personal diary.
- Keep sensitive details out of this file.

Use it when Rob asks what happened in a recent session, what Life OS learned, or when a meaningful batch should be logged.

## Architecture

GitHub
- Durable memory map.
- Session boot files.
- Project state.
- Open loops.
- Architecture documentation.
- Audit trail.
- Abstract references only.

Google Drive
- Working documents.
- Detailed project records.
- Google Docs.
- Google Sheets.
- PDFs.
- Operational artifacts.

Todoist
- Action queue.

Google Calendar
- Timed commitments.

Gmail
- Communication evidence.

SMS / phone messages
- May contain time-sensitive logistics that are not visible to Penny unless Rob shares them.
- Example: interview Zoom links may arrive by text rather than Gmail.

## Pointer Registry

Created in Drive:

- Folder: Life OS Registry
- Sheet: Life OS Pointer Registry
- Tab: Registry

The registry is the master lookup table connecting GitHub state with detailed operational records stored in Drive and other connected systems.

Current registry rows run through REF-009.

GitHub should reference records rather than duplicate sensitive personal information.

## Recent Work Completed

Created:

- `memory/STARTUP_BOOT.md`
- `memory/CAPTAINS_LOG.md`
- `projects/home-base-logistics/`
- `projects/stability-routines/`
- `projects/project-slot-07/`

Updated:

- `memory/00_START_HERE.md`
- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`
- `MIGRATION_PLAN.md`

Operational tests completed:

- Core connector check: Drive, Calendar, Contacts, Todoist, Gmail.
- GitHub startup boot in a fresh chat.
- Calendar/Todoist daily itinerary read.
- Gmail job-search label applied to matching job-related emails.
- Connector wake-up hypothesis recorded as a field note.
- Drive editing lessons recorded from Caregiver Project HQ.
- Captain's Log created and seeded.

Some direct-label changes were blocked by connector safety checks. Future edits should prefer neutral labels and abstract routing language.

## Best Next Action

Use Life Logistics HQ for real daily living and nightly housekeeping: project chat updates, job search, recovery anchors, caregiver pathway, cleanup logistics, and practical next actions.

Do not over-architect unless a real use-case reveals a gap.

## Guiding Principle

GitHub is the map.
Drive is the filing cabinet.
Calendar owns time.
Todoist owns actions.
Gmail owns communications.
SMS/phone messages may hold time-sensitive logistics outside connector visibility.
Captain's Log records meaningful operational sessions.

Project chats create project knowledge.
Life Logistics HQ curates cross-project operational memory.

Avoid duplication whenever possible.
Prefer durable references over copied data.

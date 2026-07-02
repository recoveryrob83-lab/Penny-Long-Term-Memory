# Session Handoff

Updated: 2026-07-02
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Fast baton-pass file for future Penny chat windows.

## Current Handoff

Life OS is in Phase 2 of the migration.

The core architectural decision is to separate durable memory from operational records.

A fresh Life Logistics HQ chat successfully booted from GitHub, confirmed core connectors, read the startup files, checked Calendar/Todoist for today's itinerary, labeled job-search emails in Gmail, and verified that Google Drive remained responsive after explicit connector invocation.

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

Some direct-label changes were blocked by connector safety checks. Future edits should prefer neutral labels and abstract routing language.

## Best Next Action

Use Life Logistics HQ for real daily living: interview support, job search, recovery anchors, cleanup logistics, and practical next actions.

Do not over-architect unless a real use-case reveals a gap.

## Guiding Principle

GitHub is the map.
Drive is the filing cabinet.
Calendar owns time.
Todoist owns actions.
Gmail owns communications.
SMS/phone messages may hold time-sensitive logistics outside connector visibility.

Avoid duplication whenever possible.
Prefer durable references over copied data.

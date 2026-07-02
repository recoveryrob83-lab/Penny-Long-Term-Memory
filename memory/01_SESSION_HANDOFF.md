# Session Handoff

Updated: 2026-07-02
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Fast baton-pass file for future Penny chat windows.

## Current Handoff

Life OS has entered Phase 2 of the migration.

The core architectural decision is to separate durable memory from operational records.

## Architecture

GitHub
- Durable memory.
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

## Pointer Registry

Next implementation milestone:

Create a Google Drive folder named 'Life OS Registry'.

Within it create a Google Sheet named 'Life OS Pointer Registry'.

This registry becomes the master lookup table connecting GitHub state with detailed operational records stored in Drive and other connected systems.

GitHub should reference records rather than duplicate sensitive personal information.

## Guiding Principle

GitHub is the map.
Drive is the filing cabinet.
Calendar owns time.
Todoist owns actions.
Gmail owns communications.

Avoid duplication whenever possible.
Prefer durable references over copied data.

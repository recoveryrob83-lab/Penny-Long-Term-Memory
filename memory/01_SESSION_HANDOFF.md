# Session Handoff

Updated: 2026-07-03
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Fast baton-pass file for future Penny chat windows.

## Current Handoff

Life OS is operational with separate durable memory, working records, action systems, and specialist project chats.

The core architecture remains:

- GitHub is the durable memory map.
- Google Drive is the working records cabinet.
- Todoist owns action items.
- Calendar owns timed commitments.
- Gmail owns communication evidence.
- Project chats create project knowledge.
- Life Logistics HQ curates cross-project operational memory.
- Main Assistant handles daily operations.

A fresh Life Logistics HQ chat should boot from GitHub, summarize system state concisely, and avoid dragging long prior chat context forward unless Rob asks.

## Recent Major Updates

### Life Logistics HQ

Life Logistics HQ has its own project folder and department identity.

Use it as Rob's Chief of Staff Penny for:

- system coordination
- GitHub memory curation
- project routing
- housekeeping
- advisory routing
- scheduled-task architecture notes
- department setup and role clarity

### Main Assistant

Main Assistant is Rob's daily operations desk for one-off tasks, calendar events, contacts, itinerary checks, Gmail/Drive lookups, shopping/travel-style logistics, and general daily administration.

Large ongoing work belongs in specialist project chats.

### Chief of Finance Penny

`projects/finance-benefits/` has been upgraded into Chief of Finance Penny / CFO Penny.

Chief of Finance handles:

- finance
- benefits
- checkbook / ledger
- bills
- budget
- income tracking
- financial paperwork workflows

Drive working records:

- Checkbook folder
- Checkbook Register spreadsheet

Pointer Registry REF-003 now points to Chief of Finance Penny / Checkbook Register.

Important finance guardrail: GitHub stores only abstract project state and pointers. Detailed finance records belong in Drive or RPR.

### Chief Wellness HQ

`projects/wellness/` has been upgraded into Chief Wellness HQ / Chief Wellness Penny.

Chief Wellness handles:

- wellness routines
- health-adjacent logistics
- primary care / vision / preventive-care follow-through
- appointment preparation
- sleep, food, movement, and stability supports
- non-clinical wellness planning

Important wellness guardrail: GitHub stores only abstract project state and pointers. Detailed wellness records belong in Drive, Calendar, Gmail, Todoist, project chat, or RPR.

### Scheduled Tasks

Scheduled tasks were investigated and parked for later testing.

Known findings:

- Scheduled tasks appear to run outside the originating department chat.
- A Main Assistant test created a new chat and unexpectedly renamed the originating chat.
- Scheduled tasks currently do not allow other plugins/connectors, so they cannot directly use GitHub or Google Drive.
- Active task cap may limit use; future workflows may need bundled tasks.
- A Todoist project `Penny Logistics Tasks` exists with a task to continue experimentation.
- GitHub scheduled-task architecture exists under `scheduled-tasks/`, but connector limits mean it is currently more of an architectural note layer than an automation backbone.

## Startup Workflow

Preferred new-chat startup:

1. Rob starts a fresh Penny chat.
2. Rob may ask Penny to open Drive first as a connector warm-up.
3. Rob asks Penny to check GitHub startup instructions.
4. Penny opens `recoveryrob83-lab/Penny-Long-Term-Memory`.
5. Penny reads `memory/STARTUP_BOOT.md` and follows its boot order.
6. If Rob names a project chat, Penny reads the matching project `SESSION_HANDOFF.md` and `DEPARTMENT_IDENTITY.md`.
7. Penny reads only during startup unless Rob explicitly asks for edits.

## Connector Wake-Up Field Note

Rob observed that explicitly invoking an app by name, such as `@Google Drive`, may help wake or route a connector before a full fresh-chat reset is needed.

This is a field note, not a proven guarantee.

Recommended troubleshooting order:

1. Explicitly name or tag the connector Rob wants to use.
2. Try a small harmless read.
3. If that fails, use the fresh-chat GitHub boot process.

## Drive Editing Field Lessons

- Small, incremental Drive updates have been more reliable than large complex batch edits.
- When a complex Drive update fails, retry as several tiny edits rather than repeatedly sending the same large payload.
- Verify the target row, range, or document section after each Drive update.
- If a Drive update is blocked, simplify the update and use abstract notes when possible.
- When actively working with a connector over many turns, explicitly reference that connector in the conversation to maintain clear operational context.

These lessons should be treated as operational guidelines, not claims about internal connector mechanics.

## RPR Procedure: Rob -> Penny -> Rob

Use user-mediated file transfer for structured files when reliability matters more than automation.

Use connectors for discovery, lookup, scheduling, communication, and metadata, but not as the sole path for maintaining critical structured records.

## Captain's Log

Use `memory/CAPTAINS_LOG.md` for concise operational journal entries about major Life OS sessions, discoveries, decisions, and completed batches.

Do not treat it as a transcript or diary.

## Project Chat Map

- Life Logistics HQ: Chief of Staff / cross-project coordination and GitHub memory curation.
- Main Assistant: daily operations and one-off tasks.
- Caregiver Project HQ: support pathway and related caregiver logistics.
- Job Search HQ: applications, interviews, resumes, and work-fit decisions.
- Cleanup Project HQ: cleanup providers, quotes, and scheduling.
- Chief of Finance Penny: finance, benefits, ledger, budget, bills, and financial paperwork.
- Chief Wellness HQ: practical wellness, health-adjacent logistics, appointments, routines, and stability supports.
- Recovery Logistics: daily anchors, meetings, literature logistics, and non-sensitive recovery routines.
- Philosophy HQ: framework continuity, Scriptorium coordination, and future book-compilation support.
- Life OS Infrastructure: boot files, handoffs, connector lessons, and system design.
- Health Medical HQ and Housing Logistics HQ remain available as specialist departments when needed.

## Pointer Registry

Drive file:

- Life OS Registry / Life OS Pointer Registry

The registry is the master lookup table connecting GitHub state with detailed operational records stored in Drive and other connected systems.

Current notable refs:

- REF-001: Work Search
- REF-002: Site Cleanup
- REF-003: Chief of Finance Penny / Checkbook Register
- REF-004: Life OS Registry
- REF-005: Support Pathway
- REF-006: Daily Anchors

GitHub should reference records rather than duplicate detailed personal information.

## Recent Work Completed

- Created and synchronized Life Logistics HQ as its own Chief of Staff project.
- Created advisory-board system and acknowledged Recovery advisory about Daily Meditation workbench.
- Created scheduled-task note architecture and Todoist follow-up for scheduler experimentation.
- Upgraded Finance Benefits into Chief of Finance Penny / CFO Penny.
- Located Finance Drive Checkbook folder and Checkbook Register.
- Updated Pointer Registry REF-003 for Chief of Finance Penny.
- Upgraded Wellness into Chief Wellness HQ / Chief Wellness Penny.
- Updated active project map, global open loops, startup routing, project README, and specialist project files as needed.

## Best Next Action

Use Life Logistics HQ for cross-project coordination and use specialist chats for focused project work.

## Guiding Principle

GitHub is the map.
Drive is the filing cabinet.
Calendar owns time.
Todoist owns actions.
Gmail owns communications.
Captain's Log records meaningful operational sessions.

Project chats create project knowledge.
Life Logistics HQ curates cross-project operational memory.
Main Assistant handles daily operations.

Avoid duplication whenever possible.
Prefer durable references over copied data.

Use RPR when reliable structured-file editing matters more than connector automation.
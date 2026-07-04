# Session Handoff

Updated: 2026-07-03
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Fast baton-pass file for future Penny chat windows.

## Current Handoff

Life OS is operational with separate durable memory, working records, action systems, specialist project chats, advisories, a Department Event Inbox, and an emerging daily HQ sync procedure.

The core architecture remains:

- GitHub is the durable memory map.
- Google Drive is the working records cabinet.
- Todoist owns Rob-facing action items.
- Calendar owns timed commitments.
- Gmail owns communication evidence.
- Project chats create project knowledge.
- Life Logistics HQ curates cross-project operational memory.
- Main Assistant handles daily operations.
- The Department Event Inbox tracks abstract department sync/read/ingestion state.
- Daily HQ sync workers may report routing needs and consume advisories, but they do not own source-of-truth state.

## Recent Major Updates

### Daily HQ Sync Pilot

ADV-20260703-009 from Chief Engineering Penny was read and ingested by Life Logistics HQ.

The standalone Advisory Watcher is no longer the preferred scheduled-task model.

Because scheduled-task slots appear scarce, daily HQ sync workers are now the preferred experiment for the core HQs.

Engineering HQ Daily Sync is the first pilot, scheduled for 6:00 AM America/Chicago.

Daily sync workers should read boot/handoff/advisory context, consume advisories addressed to their department, and report meaningful updates. They should not modify GitHub, Drive, Todoist, Calendar, Gmail, or other systems unless Rob explicitly authorizes that behavior.

Pending rollout decision after Engineering pilot:

- Life Logistics HQ Sync
- Main Assistant Sync
- Chief Finance Sync
- Chief Business Sync

### Recovery Meeting Notes Workdesk

ADV-20260703-008 from Recovery HQ has been read, ingested, and acknowledged after Life Logistics HQ and Main Assistant both consumed it.

A Recovery Meeting Notes Workdesk exists for non-sensitive NA/AA meeting notes.

Drive resource:

- Google Drive `Recovery Logistics` folder
- Document: `Recovery Meeting Notes`

Routing note: meeting-note capture or meeting-summary work should route to Recovery Meeting Notes Workdesk unless Rob asks otherwise.

### Business Logistics Advisory

ADV-20260703-004 from Chief Business HQ has been read, ingested, and acknowledged.

Business HQ is in active Penny Platform viability research and may generate frequent working artifacts, research notes, Drive records, Todoist actions, GitHub advisories, and future cross-department handoffs.

Life Logistics HQ should keep the operational map tidy while Business HQ moves quickly.

Main Assistant should route one-off business admin, quick lookups, scheduling, or communication support back to Chief Business HQ unless Rob says otherwise.

### Department Event Inbox

`coordination/DEPARTMENT_EVENT_INBOX.md` has been created.

It tracks advisory and department synchronization events so Rob is not the only notification layer between specialist chats.

Todoist remains for Rob-facing tasks. The Department Event Inbox is for system synchronization state.

### Chief Engineering Penny

`projects/engineering/` has been created as Chief Engineering Penny / Engineering HQ.

Chief Engineering handles technical architecture, repository strategy, software planning, APIs, connectors, data models, automation design, testing, technical feasibility, and implementation planning.

Engineering has created Drive scaffolding under Life Organization > Chief Engineering Penny.

ADV-20260703-006 from Chief Engineering Penny was read and ingested by Life Logistics HQ.

Important engineering guardrail: Chief Business HQ defines what should be built and why. Chief Engineering Penny defines how to build it and in what order.

### Chief Business HQ

`projects/business-development/` has been created as Chief Business HQ / Chief Business Development Penny.

Chief Business handles business ideas, product strategy, branding, market research, offer design, customer discovery, monetization, and go-to-market planning.

Chief Business HQ is active on Penny product viability and business-development research. A Drive working cabinet exists under Life Organization > Chief Business HQ.

ADV-20260703-003 from Chief Business HQ has been acknowledged after Life Logistics HQ, Main Assistant, and Chief of Finance Penny reported read to Rob.

### Chief of Finance Penny

`projects/finance-benefits/` has been upgraded into Chief of Finance Penny / CFO Penny.

Chief of Finance handles finance, benefits, checkbook/ledger, bills, budget, income tracking, and financial paperwork workflows.

Pointer Registry REF-003 now points to Chief of Finance Penny / Checkbook Register.

### Chief Wellness HQ

`projects/wellness/` has been upgraded into Chief Wellness HQ / Chief Wellness Penny.

Chief Wellness handles wellness routines, health-adjacent logistics, appointment preparation, sleep, food, movement, stability supports, and non-clinical wellness planning.

### Life Logistics HQ

Life Logistics HQ is Rob's Chief of Staff Penny for system coordination, GitHub memory curation, project routing, housekeeping, advisory routing, scheduled-task architecture notes, department setup, and role clarity.

### Main Assistant

Main Assistant is Rob's daily operations desk for one-off tasks, calendar events, contacts, itinerary checks, Gmail/Drive lookups, shopping/travel-style logistics, and general daily administration.

Large ongoing work belongs in specialist project chats.

## Startup Workflow

Preferred new-chat startup:

1. Rob starts a fresh Penny chat.
2. Rob may ask Penny to open Drive first as a connector warm-up.
3. Rob asks Penny to check GitHub startup instructions.
4. Penny opens `recoveryrob83-lab/Penny-Long-Term-Memory`.
5. Penny reads `memory/STARTUP_BOOT.md` and follows its boot order.
6. If Rob names a project chat, Penny reads the matching project `SESSION_HANDOFF.md` and `DEPARTMENT_IDENTITY.md`.
7. Penny reads only during startup unless Rob explicitly asks for edits.

## Project Chat Map

- Life Logistics HQ: Chief of Staff / cross-project coordination and GitHub memory curation.
- Main Assistant: daily operations and one-off tasks.
- Caregiver Project HQ: support pathway and related caregiver logistics.
- Job Search HQ: applications, interviews, resumes, and work-fit decisions.
- Cleanup Project HQ: cleanup providers, quotes, and scheduling.
- Chief of Finance Penny: finance, benefits, ledger, budget, bills, and financial paperwork.
- Chief Business HQ: business ideas, product strategy, branding, market research, offer design, monetization, and customer discovery.
- Chief Engineering Penny: technical architecture, software planning, repositories, automations, APIs, data models, testing, and implementation planning.
- Chief Wellness HQ: practical wellness, health-adjacent logistics, appointments, routines, and stability supports.
- Recovery Logistics: daily anchors, meetings, literature logistics, meeting-note workbench routing, and non-sensitive recovery routines.
- Philosophy HQ: framework continuity, Scriptorium coordination, and future book-compilation support.
- Life OS Infrastructure: boot files, handoffs, connector lessons, and system design.
- Health Medical HQ and Housing Logistics HQ remain available as specialist departments when needed.

## Recent Work Completed

- Read and ingested ADV-20260703-009 from Chief Engineering Penny and recorded daily HQ sync pilot architecture.
- Read and acknowledged ADV-20260703-008 from Recovery HQ after Life Logistics HQ and Main Assistant consumed it.
- Read, ingested, and acknowledged ADV-20260703-004 from Chief Business HQ.
- Added Advisory Watcher v0.1 procedure after reading ADV-20260703-007; later superseded as preferred slot usage by daily HQ sync model.
- Created Department Event Inbox under `coordination/DEPARTMENT_EVENT_INBOX.md`.
- Read and ingested ADV-20260703-006 from Chief Engineering Penny.
- Created Chief Engineering Penny / Engineering HQ under `projects/engineering/`.
- Created and synchronized Life Logistics HQ as its own Chief of Staff project.
- Created advisory-board system and acknowledged Recovery advisory about Daily Meditation workbench.
- Created scheduled-task note architecture and Todoist follow-up for scheduler experimentation.
- Upgraded Finance Benefits into Chief of Finance Penny / CFO Penny.
- Upgraded Wellness into Chief Wellness HQ / Chief Wellness Penny.
- Created Chief Business HQ / Chief Business Development Penny under `projects/business-development/`.
- Recorded Business research scaffold and acknowledged ADV-20260703-003 after all target departments reported read.

## Best Next Action

Observe Engineering HQ Daily Sync pilot before rolling out more scheduled HQ sync workers.

## Guiding Principle

GitHub is the map.
Drive is the filing cabinet.
Calendar owns time.
Todoist owns Rob-facing actions.
Gmail owns communications.
Captain's Log records meaningful operational sessions.
Department Event Inbox tracks system synchronization state.
Daily HQ sync workers report and consume advisory state only unless Rob explicitly authorizes writes.

Project chats create project knowledge.
Life Logistics HQ curates cross-project operational memory.
Main Assistant handles daily operations.

Avoid duplication whenever possible.
Prefer durable references over copied data.

Use RPR when reliable structured-file editing matters more than connector automation.
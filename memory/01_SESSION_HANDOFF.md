# Session Handoff

Updated: 2026-07-03
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Fast baton-pass file for future Penny chat windows.

## Current Handoff

Life OS is operational with separate durable memory, working records, action systems, specialist project chats, advisories, a Department Event Inbox, and an Advisory Watcher v0.1 procedure.

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
- Advisory Watcher v0.1 may report routing needs to Rob, but does not own source-of-truth state.

## Recent Major Updates

### Advisory Watcher v0.1

ADV-20260703-007 from Chief Engineering Penny was read and ingested by Life Logistics HQ.

The watcher procedure lives in:

- `coordination/DEPARTMENT_EVENT_INBOX.md`
- `projects/life-os-infrastructure/SESSION_HANDOFF.md`
- `memory/03_OPERATIONAL_RULES.md`

Purpose: use one scheduled ChatGPT task as a low-code/no-code notification layer that checks the Advisory Index and Department Event Inbox, then reports routing needs to Rob with copy-paste-ready target messages.

The watcher should not modify GitHub unless Rob later explicitly approves that behavior.

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
- Recovery Logistics: daily anchors, meetings, literature logistics, and non-sensitive recovery routines.
- Philosophy HQ: framework continuity, Scriptorium coordination, and future book-compilation support.
- Life OS Infrastructure: boot files, handoffs, connector lessons, and system design.
- Health Medical HQ and Housing Logistics HQ remain available as specialist departments when needed.

## Recent Work Completed

- Added Advisory Watcher v0.1 procedure after reading ADV-20260703-007.
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

Use Life Logistics HQ for cross-project coordination and use specialist chats for focused project work.

## Guiding Principle

GitHub is the map.
Drive is the filing cabinet.
Calendar owns time.
Todoist owns Rob-facing actions.
Gmail owns communications.
Captain's Log records meaningful operational sessions.
Department Event Inbox tracks system synchronization state.
Advisory Watcher v0.1 reports routing needs only.

Project chats create project knowledge.
Life Logistics HQ curates cross-project operational memory.
Main Assistant handles daily operations.

Avoid duplication whenever possible.
Prefer durable references over copied data.

Use RPR when reliable structured-file editing matters more than connector automation.
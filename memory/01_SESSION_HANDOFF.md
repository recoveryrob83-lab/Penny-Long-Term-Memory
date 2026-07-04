# Session Handoff

Updated: 2026-07-04
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Fast baton-pass file for future Penny chat windows.

## Current Handoff

Life OS is operational with separate durable memory, working records, action systems, specialist project chats, advisories, a Department Event Inbox, an emerging daily HQ sync procedure, a durable design-principles file, and the first concrete Engineering research track for Penny product reliability.

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
- Life OS design principles live in `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`.

## Current Durable Decisions

Business Drive architecture is resolved:

- Life Organization > Chief Business HQ
- Under that: Business Development

Business Development is a subfolder under Chief Business HQ, not a separate top-level business root.

## Recent Major Updates

### Chief Engineering Penny / Reliable Connector Execution Layer

ADV-20260704-002 from Chief Business HQ was read and ingested by Chief Engineering Penny.

The advisory identified connector write reliability as a major Penny product risk. During Business HQ work, Google Drive reads/searches/metadata remained useful, but repeated write operations eventually hit safety-check blocks. Business HQ used RPR/user-mediated file transfer as the safe fallback.

Engineering has created the first concrete Engineering research track:

- Reliable Connector Execution Layer

Drive working note created:

- `Reliable Connector Execution Layer - Design Note`
- https://docs.google.com/document/d/1R0SYHk7PLCDerOHcO-sSXGvybrGx8rOAGvQinsyAR3M/edit?usp=drivesdk

Key design direction: future Penny connector-dependent execution should be observable, verified, recoverable, idempotent, and safe to degrade into RPR/export/manual-upload fallback. Penny should never claim a connector write succeeded until verified.

### Chief Business HQ Research Update

ADV-20260704-001 from Chief Business HQ was read and ingested by Life Logistics HQ.

Business HQ completed a major Penny Platform business-development work session.

Current business frame: Penny is not primarily a chatbot. Penny is an execution/coordination platform or personal AI operating system that reduces coordination burden, cognitive load, and mental juggling while increasing completed outcomes.

Business HQ has begun competitor research and created/updated Drive working records:

- `Business Competitor Matrix`, with `Competitors` and `Positioning Matrix` tabs.
- `Business Development Costs`, with `Cost Estimates` and `Unit Economics` tabs.
- `Business_Model_Design.xlsx` in the Business Development / Strategy working area.

Candidate business model paths:

- Penny Platform
- Penny Solutions / Studio
- Penny Templates / Marketplace
- Hybrid Concierge MVP

### Life OS Design Principles

ADV-20260703-010 from Chief Engineering Penny was read and ingested by Life Logistics HQ.

Created:

- `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`

Key principle: no new platform enters the Life OS architecture until it solves a measured problem that cannot be cleanly solved by an existing component.

Kanban/project-management platforms such as Asana, ClickUp, Trello, or similar tools are deferred, not rejected.

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
- Life OS Infrastructure: boot files, handoffs, connector lessons, design principles, and system design.
- Health Medical HQ and Housing Logistics HQ remain available as specialist departments when needed.

## Recent Work Completed

- Recorded canonical Business Drive architecture: `Life Organization > Chief Business HQ > Business Development`.
- Read and ingested ADV-20260704-002 from Chief Business HQ into Engineering; created Reliable Connector Execution Layer design note and research track.
- Read and ingested ADV-20260704-001 from Chief Business HQ and updated Business HQ reboot context.
- Read and ingested ADV-20260703-010 from Chief Engineering Penny and created Life OS design principles file.
- Read and ingested ADV-20260703-009 from Chief Engineering Penny and recorded daily HQ sync pilot architecture.
- Created Department Event Inbox under `coordination/DEPARTMENT_EVENT_INBOX.md`.
- Created Chief Engineering Penny / Engineering HQ under `projects/engineering/`.
- Created and synchronized Life Logistics HQ as its own Chief of Staff project.
- Upgraded Finance Benefits into Chief of Finance Penny / CFO Penny.
- Upgraded Wellness into Chief Wellness HQ / Chief Wellness Penny.
- Created Chief Business HQ / Chief Business Development Penny under `projects/business-development/`.

## Best Next Action

For Engineering: turn the Reliable Connector Execution Layer design note into an implementation packet outline and operation-ledger schema.

For Business: continue positioning, unit economics, business-model scoring, customer persona/use-case definition, and validation packet work.

For Life Logistics: observe Engineering HQ Daily Sync pilot before rolling out more scheduled HQ sync workers.

## Guiding Principle

GitHub is the map.
Drive is the filing cabinet.
Calendar owns time.
Todoist owns Rob-facing actions.
Gmail owns communications.
Captain's Log records meaningful operational sessions.
Department Event Inbox tracks system synchronization state.
Daily HQ sync workers report and consume advisory state only unless Rob explicitly authorizes writes.
Design principles govern whether new platforms enter Life OS.

Project chats create project knowledge.
Life Logistics HQ curates cross-project operational memory.
Main Assistant handles daily operations.

Avoid duplication whenever possible.
Prefer durable references over copied data.

Use RPR when reliable structured-file editing matters more than connector automation.
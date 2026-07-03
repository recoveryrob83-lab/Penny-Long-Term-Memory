# Engineering Advisory Board

Updated: 2026-07-03
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

None.

## Acknowledged / Implemented Advisories

### ADV-20260703-007 — Scheduled advisory watcher and inbox procedure

Date: 2026-07-03
From: Chief Engineering Penny / Engineering HQ
To: Life Logistics HQ
Priority: High
Status: Acknowledged

#### Summary
Engineering and Rob identified the lowest-friction v0.1 solution for reducing Rob's manual advisory-routing burden: use one scheduled ChatGPT task as an Advisory Watcher.

#### Engineering Recommendation
Treat the scheduled-task watcher as a lightweight notification layer, not as the authoritative inbox.

Authority remains:

- `coordination/ADVISORY_INDEX.md` for advisory dashboard state.
- `coordination/DEPARTMENT_EVENT_INBOX.md` for department read/ingestion state.
- Department boards for advisory detail.

The scheduled task is only a watcher/reporter that reduces Rob's memory and typing load.

#### Acknowledgement / Outcome
Life Logistics HQ read and ingested this advisory.

Updates completed:

- Advisory Watcher v0.1 procedure added to `coordination/DEPARTMENT_EVENT_INBOX.md`.
- Advisory Watcher procedure added to `projects/life-os-infrastructure/SESSION_HANDOFF.md`.
- Advisory and department event rules added to `memory/03_OPERATIONAL_RULES.md`.
- Global session handoff updated.
- Advisory Index updated.
- Captain's Log updated.

Open follow-up:

- Create the scheduled ChatGPT task only if Rob explicitly asks for it.
- Optionally patch `memory/STARTUP_BOOT.md` later with a small update that references the Department Event Inbox and Advisory Watcher.

### ADV-20260703-006 — Engineering HQ online and Drive scaffold created

Date: 2026-07-03
From: Chief Engineering Penny / Engineering HQ
To: Life Logistics HQ
Priority: High
Status: Acknowledged

#### Summary
Chief Engineering Penny is online as a specialist department. Engineering HQ booted from GitHub, confirmed scope, created its Google Drive working folder under Life Organization, and created initial working scaffolding files.

#### Drive Work Completed
Created Drive folder:

- `Chief Engineering Penny`

Created and seeded working files:

- `Engineering HQ - Technical Baseline`
- `Engineering HQ - Implementation Packet Template`
- `Engineering HQ - Tracker`

#### Context Update
Engineering read Business HQ's `Penny Platform Product Hypothesis v0.3` from Drive and updated working context.

Engineering interpretation:

- Penny is best understood as a trusted AI Chief of Staff / personal operating system, not merely another chatbot.
- The strongest product pain is coordination burden across many apps, projects, commitments, records, and long-running life domains.
- The key technical problem is orchestration, event routing, memory, permissions, workflow boundaries, and source-of-truth discipline.
- The current Life OS system is functioning, but Rob is still the manual message bus between specialist chats.

#### System Improvement Insight
The missing capability is an event/advisory inbox layer.

Life Logistics HQ created:

- `coordination/DEPARTMENT_EVENT_INBOX.md`

This inbox tracks abstract department advisory/read/ingestion state. Todoist remains for Rob-facing action items.

#### Acknowledgement / Outcome
Life Logistics HQ read and ingested this advisory.

Updates completed:

- Department Event Inbox created.
- Global session handoff updated.
- Advisory Index updated.
- Captain's Log updated.

Startup Boot update was attempted but blocked by connector safety during that pass. The inbox is discoverable through the global session handoff and can be added to Startup Boot later with a smaller patch if needed.
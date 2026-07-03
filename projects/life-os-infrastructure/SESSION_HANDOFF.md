# Life OS Infrastructure Session Handoff

Updated: 2026-07-03
Project: Life OS Infrastructure
Purpose: Project-specific handoff for Life OS Infrastructure and connector/architecture workflows.

## Metadata

- Project Owner: Rob
- Primary Chat: Life OS Infrastructure
- Current Phase: Active / Architecture Maintenance
- Primary Systems: GitHub, Google Drive, Todoist, Calendar, Gmail, Contacts, connector tools as needed
- Sensitivity Level: Moderate
- GitHub Rule: Store architecture, schema, operating rules, and abstract workflow lessons. Do not store secrets or private source data.

## Boot Instructions

When Rob opens a new Life OS Infrastructure chat:

1. Read the global boot files from `memory/STARTUP_BOOT.md`.
2. Read this project handoff.
3. Read this project's `README.md`, `status.md`, and `open_loops.md` if present.
4. Use GitHub/Drive/Todoist/Calendar/Gmail only as needed for system architecture and connector workflows.
5. Keep architecture practical. Do not over-engineer without a real use case.

## Current Project Status

Active architecture maintenance.

Life OS now includes advisory boards plus a Department Event Inbox for abstract sync/read/ingestion state.

## Objectives

- Maintain Life OS architecture, boot files, connector lessons, project handoffs, pointer registry workflow, advisory routing, event inbox, and housekeeping system.
- Keep the system useful for daily life rather than turning it into architecture for architecture's sake.

## Completed Work

- Created advisory board system under `coordination/`.
- Created Department Event Inbox at `coordination/DEPARTMENT_EVENT_INBOX.md`.
- Added Advisory Watcher v0.1 procedure to the Department Event Inbox.

## Active Open Loops

- Consider creating a ChatGPT scheduled task for Advisory Watcher v0.1.
- If created, watcher should report open advisories/unread inbox items to Rob and provide copy-paste routing messages.
- Watcher should not modify GitHub unless Rob later explicitly approves that behavior.
- Add Department Event Inbox reference to Startup Boot later if connector safety allows a small patch.

## Advisory Watcher v0.1

Purpose: reduce Rob's manual advisory-routing burden without building local automation.

Authority remains:

- `coordination/ADVISORY_INDEX.md` for advisory dashboard state.
- `coordination/DEPARTMENT_EVENT_INBOX.md` for read/ingestion state.
- Department advisory boards for advisory details.

Scheduled watcher behavior:

1. Read Advisory Index and Department Event Inbox.
2. Identify open advisories or unread department events.
3. Report only when routing is needed.
4. Provide copy-paste-ready target messages for Rob.
5. Do not modify GitHub unless Rob explicitly approves that behavior.

Suggested watcher prompt is stored in `coordination/DEPARTMENT_EVENT_INBOX.md`.

## Working Documents / Links

- `coordination/ADVISORY_INDEX.md`
- `coordination/DEPARTMENT_EVENT_INBOX.md`
- `coordination/boards/`
- `scheduled-tasks/`
- `memory/STARTUP_BOOT.md`
- `memory/01_SESSION_HANDOFF.md`
- `memory/03_OPERATIONAL_RULES.md`
- `memory/CAPTAINS_LOG.md`

## Source Systems

- GitHub: durable architecture, boot files, operating rules, active projects, open loops, advisory boards, Department Event Inbox, Captain's Log.
- Google Drive: working documents, pointer registry, operational artifacts.
- Todoist: Rob-facing tasks and reminders.
- Calendar/Gmail/Contacts: only when relevant to infrastructure tasks.

## Connector / Safety Notes

- Prefer small verified edits.
- Record durable connector lessons in boot/operating files when they affect future Penny behavior.
- Use cautious language for observed patterns; do not claim unsupported internal mechanisms.
- Treat connectors as convenience automation, not core infrastructure.

## Privacy Guardrails

- GitHub can store architecture, schema, fake seed data, migration plans, and operating rules.
- GitHub should not store real personal data, credentials, medical identifiers, financial identifiers, or private family notes.
- Use `.gitignore` style thinking for local/private data.

## Decision Log

- Advisory Watcher v0.1 is a low-code/no-code notification layer, not the source of truth.
- Department Event Inbox owns system synchronization state.
- Todoist owns Rob-facing actions.

## Immediate Next Actions

Use current Life OS boot files and open loops to identify active infrastructure work when the next Life OS Infrastructure chat boots.

## Notes for Next Penny

This file is the project-specific continuity anchor. Update it after meaningful infrastructure work or when a fresh Life OS Infrastructure chat needs a clean restart point.
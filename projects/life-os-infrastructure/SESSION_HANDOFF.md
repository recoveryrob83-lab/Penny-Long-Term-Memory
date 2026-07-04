# Life OS Infrastructure Session Handoff

Updated: 2026-07-03
Project: Life OS Infrastructure
Purpose: Project-specific handoff for Life OS Infrastructure and connector/architecture workflows.

## Metadata

- Project Owner: Rob
- Primary Chat: Life OS Infrastructure
- Current Phase: Active / Architecture Maintenance
- Primary Systems: GitHub, Google Drive, Todoist, Calendar, Gmail, Contacts, connector tools as needed, ChatGPT scheduled tasks
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

Life OS now includes advisory boards, a Department Event Inbox for abstract sync/read/ingestion state, and an emerging scheduled HQ sync pattern.

## Objectives

- Maintain Life OS architecture, boot files, connector lessons, project handoffs, pointer registry workflow, advisory routing, event inbox, scheduled sync architecture, and housekeeping system.
- Keep the system useful for daily life rather than turning it into architecture for architecture's sake.

## Completed Work

- Created advisory board system under `coordination/`.
- Created Department Event Inbox at `coordination/DEPARTMENT_EVENT_INBOX.md`.
- Added Advisory Watcher v0.1 procedure to the Department Event Inbox.
- Recorded the shift from standalone Advisory Watcher toward daily HQ sync workers.
- Recorded Engineering HQ Daily Sync as the first scheduled sync pilot.

## Active Open Loops

- Observe Engineering HQ Daily Sync pilot.
- Verify whether scheduled sync runs in the originating Engineering HQ chat.
- Verify whether the scheduled sync can access GitHub connectors during execution.
- Verify whether it preserves Engineering identity and boot context.
- If successful, consider rolling out daily sync workers one at a time for:
  - Life Logistics HQ Sync
  - Main Assistant Sync
  - Chief Finance Sync
  - Chief Business Sync
- Optional: patch `memory/STARTUP_BOOT.md` later with a small reference to Department Event Inbox and daily HQ sync workers if useful.

## Scheduled HQ Sync Model

Daily HQ sync workers are now the preferred experiment over a standalone Advisory Watcher.

Reason: Rob appears to have a scarce scheduled-task limit, so scheduled tasks should be treated as premium Life OS infrastructure slots.

Likely core sync slots:

1. Life Logistics HQ
2. Main Assistant
3. Chief Finance Penny
4. Chief Business HQ
5. Chief Engineering Penny

Engineering HQ Daily Sync is the first pilot and is scheduled for 6:00 AM America/Chicago.

Daily sync workers should:

- Boot into the correct department identity.
- Read current GitHub boot/handoff context.
- Read Advisory Index and Department Event Inbox.
- Consume advisories addressed to that department.
- Report meaningful updates, routing needs, or recommended documentation changes.
- Avoid modifying GitHub, Drive, Todoist, Calendar, Gmail, or other systems unless Rob explicitly authorizes that behavior.

## Advisory Watcher v0.1 Status

The standalone Advisory Watcher concept is retired as the preferred slot usage.

Its routing/reporting logic is preserved inside the daily HQ sync concept.

Authority remains:

- `coordination/ADVISORY_INDEX.md` for advisory dashboard state.
- `coordination/DEPARTMENT_EVENT_INBOX.md` for read/ingestion state.
- Department advisory boards for advisory details.

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

- GitHub: durable architecture, boot files, operating rules, active projects, open loops, advisory boards, Department Event Inbox, scheduled sync notes, Captain's Log.
- Google Drive: working documents, pointer registry, operational artifacts.
- Todoist: Rob-facing tasks and reminders.
- Calendar/Gmail/Contacts: only when relevant to infrastructure tasks.
- ChatGPT scheduled tasks: experimental read/report sync workers.

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

- Department Event Inbox owns system synchronization state.
- Todoist owns Rob-facing actions.
- Daily HQ sync is preferred over standalone Advisory Watcher if scheduled-task slots are scarce.
- Daily sync workers should report and consume advisories, not perform major writes or decisions without Rob authorization.

## Immediate Next Actions

Use current Life OS boot files and open loops to identify active infrastructure work when the next Life OS Infrastructure chat boots.

## Notes for Next Penny

This file is the project-specific continuity anchor. Update it after meaningful infrastructure work or when a fresh Life OS Infrastructure chat needs a clean restart point.
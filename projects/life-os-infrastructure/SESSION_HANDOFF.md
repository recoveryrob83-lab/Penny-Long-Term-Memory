# LifeOS Infrastructure Session Handoff

Updated: 2026-07-14
Project: LifeOS Infrastructure
Purpose: Project-specific handoff for LifeOS Infrastructure and connector or architecture workflows.

## Metadata

- Project Owner: Rob
- Primary Chat: LifeOS Infrastructure
- Current Phase: Active / Architecture Maintenance
- Primary Systems: GitHub, Google Drive, Todoist, Calendar, Gmail, Contacts, connector tools as needed, ChatGPT scheduled tasks
- Sensitivity Level: Moderate
- GitHub Rule: Store architecture, schema, operating rules, design principles, and abstract workflow lessons. Do not store secrets or private source data.

## Boot Instructions

When Rob opens a new LifeOS Infrastructure chat:

1. Read the global boot files from `memory/STARTUP_BOOT.md`.
2. Read this project handoff.
3. Read this project's `README.md`, `status.md`, and `open_loops.md` if present.
4. Read `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md` when making architecture or platform-adoption decisions.
5. Use GitHub, Drive, Todoist, Calendar, and Gmail only as needed for system architecture and connector workflows.
6. Keep architecture practical. Do not over-engineer without a real use case.

## Current Project Status

Active architecture maintenance.

LifeOS now includes advisory boards, a Department Event Inbox for abstract sync/read/ingestion state, an emerging scheduled HQ sync pattern, and a durable design-principles file.

## Objectives

- Maintain LifeOS architecture, boot files, connector lessons, project handoffs, pointer registry workflow, advisory routing, event inbox, scheduled sync architecture, design principles, and housekeeping system.
- Keep the system useful for daily life rather than turning it into architecture for architecture's sake.

## Design Principles

Durable LifeOS design principles live in:

- `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`

Current key principle: no new platform enters the LifeOS architecture until it solves a measured problem that cannot be cleanly solved by an existing component.

Kanban or project-management platforms such as Asana, ClickUp, or Trello are deferred, not rejected.

If adopted later, they should own department-level pipeline state only, most likely for `Business_HQ` or `Engineering_HQ`. They should not become a global LifeOS layer unless real scaling pain proves the need.

## Completed Work

- Created advisory board system under `coordination/`.
- Created Department Event Inbox at `coordination/DEPARTMENT_EVENT_INBOX.md`.
- Added Advisory Watcher v0.1 procedure to the Department Event Inbox.
- Recorded the shift from standalone Advisory Watcher toward daily HQ sync Workers.
- Recorded `Engineering_HQ` Daily Sync as the first scheduled sync pilot; pilot paused by Rob on 2026-07-11 pending additional scheduling architecture.
- Created `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`.

## Active Open Loops

- Design the additional scheduling and execution architecture needed before resuming the `Engineering_HQ` Daily Sync pilot.
- Document reliable task-to-chat identity, execution-context, connector-access, and boot-context requirements.
- Keep the Engineering pilot paused until Rob authorizes a resume.
- If a future pilot succeeds, consider rolling out daily sync Workers one at a time for:
  - `Maintenance_HQ` Sync
  - `Chief_of_Staff_HQ` Sync
  - `Finance_HQ` Sync
  - `Business_HQ` Sync
- Optional: patch `memory/STARTUP_BOOT.md` later with a small reference to Department Event Inbox, daily HQ sync Workers, and design principles if useful.

## Scheduled HQ Sync Model

Daily HQ sync Workers remain a possible future experiment, but the Engineering pilot is paused pending additional scheduling and execution architecture.

Reason: Rob appears to have a scarce scheduled-task limit, so scheduled tasks should be treated as premium LifeOS infrastructure slots.

Potential future sync slots, only after the pilot is proven:

1. `Maintenance_HQ`
2. `Chief_of_Staff_HQ`
3. `Finance_HQ`
4. `Business_HQ`
5. `Engineering_HQ`

`Engineering_HQ` Daily Sync was the first pilot. It is paused as of 2026-07-11 because scheduled-task execution behavior remains unreliable. No additional sync Workers should be rolled out until the architecture is strengthened.

Daily sync Workers should:

- Boot into the correct department identity.
- Read current GitHub boot and handoff context.
- Read Advisory Index and Department Event Inbox.
- Consume advisories addressed to that department.
- Report meaningful updates, routing needs, or recommended documentation changes.
- Avoid modifying GitHub, Drive, Todoist, Calendar, Gmail, or other systems unless Rob explicitly authorizes that behavior.

## Advisory Watcher v0.1 Status

The standalone Advisory Watcher concept is retired as the preferred slot usage.

Its routing and reporting logic is preserved inside the daily HQ sync concept.

Authority remains:

- `coordination/ADVISORY_INDEX.md` for advisory dashboard state.
- `coordination/DEPARTMENT_EVENT_INBOX.md` for read or ingestion state.
- Department advisory boards for advisory details.

## Working Documents / Links

- `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`
- `coordination/ADVISORY_INDEX.md`
- `coordination/DEPARTMENT_EVENT_INBOX.md`
- `coordination/boards/`
- `scheduled-tasks/`
- `memory/STARTUP_BOOT.md`
- `memory/01_SESSION_HANDOFF.md`
- `memory/03_OPERATIONAL_RULES.md`
- `memory/CAPTAINS_LOG.md`

## Source Systems

- GitHub: durable architecture, boot files, operating rules, design principles, active projects, open loops, advisory boards, Department Event Inbox, scheduled sync notes, Captain's Log.
- Google Drive: working documents, pointer registry, operational artifacts.
- Todoist: Rob-facing tasks and reminders.
- Calendar, Gmail, and Contacts: only when relevant to infrastructure tasks.
- ChatGPT scheduled tasks: experimental read or report sync Workers.

## Connector / Safety Notes

- Prefer small verified edits.
- Record durable connector lessons in boot or operating files when they affect future Penny behavior.
- Use cautious language for observed patterns; do not claim unsupported internal mechanisms.
- Treat connectors as convenience automation, not core infrastructure.

## Privacy Guardrails

- GitHub can store architecture, schema, fake seed data, migration plans, operating rules, and design principles.
- GitHub should not store real personal data, credentials, medical identifiers, financial identifiers, or private family notes.
- Use `.gitignore` style thinking for local or private data.

## Decision Log

- Department Event Inbox owns system synchronization state.
- Todoist owns Rob-facing actions.
- Daily HQ sync may be reconsidered only after the paused Engineering pilot's execution model is redesigned and produces reliable evidence.
- Daily sync Workers should report and consume advisories, not perform major writes or decisions without Rob authorization.
- New platforms require measured pain, clear ownership, and no clean existing-component solution.
- Kanban or project-management tools are deferred until real pipeline-state pain appears.

## Immediate Next Actions

Use current LifeOS boot files and open loops to identify active infrastructure work when the next LifeOS Infrastructure chat boots.

## Notes for Next Penny

This file is the project-specific continuity anchor. Update it after meaningful infrastructure work or when a fresh LifeOS Infrastructure chat needs a clean restart point.
# Penny Boot Log

Updated: 2026-07-19
Project: Life OS / Life OS Maintenance HQ / Penny Long-Term Memory
Purpose: Historical architecture and workflow lessons. This file is not the current boot sequence or current-state handoff.

## Authority Notice

Current startup authority:

- `memory/STARTUP_BOOT.md`

Current global state:

- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`

Do not use older snapshots in this file as current task, calendar, project, or personal state.

## Durable Architecture Decision

As of 2026-07-02, GitHub became the preferred durable memory and architecture map for Life OS because it provides Markdown files, commit history, diffs, rollback, and auditable changes.

Google Drive remains active for working documents, spreadsheets, generated artifacts, and detailed operational records.

Current source boundaries:

- GitHub: durable memory, architecture, handoffs, abstract project state, advisories, shared contracts, and Worker profiles.
- Drive: working records and human-facing artifacts.
- Trello: capture and current attention flow.
- Todoist: commitments and reminders.
- Calendar: timed commitments.
- Gmail: communication evidence.
- LifeOS Dashboard and automation logs: transport, diagnostics, and selected-source visibility.

## Canonical Execution and Worker Architecture Milestone

On 2026-07-19, Rob authorized and Life OS Maintenance HQ implemented the canonical shared execution and Worker architecture through ADV-20260719-043 and the bounded continuity reconciliation in ADV-20260719-044.

Canonical shared authority:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` defines organizational topology, source boundaries, direct execution-ready routing, lifecycle and priority separation, verification modes, wake suppression, holds, elevations, resume behavior, scheduled procedures, reporting, and desktop pause rules.
- `coordination/WORKER_EXECUTION_CONTRACT.md` defines the universal Worker authority ceiling, controlled outcomes, department-owned profile convention, evidence, revisions, duplicate suppression, naming, stable IDs, and completion rules.
- `memory/STARTUP_BOOT.md` remains the single canonical entry point for both HQ and Worker boots.

The existing ten-file universal operating kernel retained its order. After that kernel, HQs load the shared execution protocol before role-specific state. Workers load the universal kernel, both shared protocols, the owning department identity, the exact Worker profile, the authoritative advisory, task definition, or schedule, and only the records needed for the bounded task.

New Worker profiles live at:

- `projects/<department>/workers/<profile>.md`

The owning Department HQ creates and maintains a profile only when a real Worker is activated. The profile stores stable identity and authority, not deployment or runtime state.

The root packages below are grandfathered compatibility pilots created before the department-owned profile convention:

- `workers/penny-raw-capture/`
- `workers/penny-inventory/`

`workers/README.md` and `workers/WORKER_STANDARD.md` are compatibility surfaces only. No new top-level Worker package may be created by analogy.

The normal execution-ready path is designed for one event-driven wake:

Rob authorizes through Chief of Staff HQ → Chief of Staff routes one execution-ready advisory or authoritative task definition to the owning Department Worker → the Worker executes and records evidence → verification follows the specified mode → Chief of Staff reports through the appropriate operational review.

Ownership split:

- Rob is final authority.
- Chief of Staff HQ coordinates Rob-authorized work and reporting.
- Department HQs own Worker purpose, stable identity, authority, profiles, holds, verification, and retirement.
- Life OS Maintenance HQ owns shared contracts, boot coherence, profile conventions, audits, source boundaries, and reconciliation.
- Engineering HQ owns routing-registry implementation, exact-title and stable-ID transport, deployment state, route availability, pause state, receiver state, revision deduplication, verification queues, wake suppression, and technical rollover.
- Workers execute bounded work and own no independent strategy or backlog.

Remaining Engineering dependencies are tracked through the Engineering-owned advisory and records rather than duplicated here. They include receiver-side semantic validation, routing-registry and runtime implementation, exact-title and zero-or-duplicate-match handling, stable-ID transport, receiver state, revision deduplication, verification queues, wake suppression, and controlled rename or rollover behavior.

## Connector Recovery Lesson

A long-running chat may stop invoking connectors reliably. Treat that as possible session degradation rather than automatically blaming the user or durable state.

Recovery order:

1. Explicitly name or tag the intended connector.
2. Try a small harmless read.
3. If it responds, continue with small verified operations.
4. If it remains unreliable, start a fresh chat and boot from GitHub.

These are field observations, not claims about undocumented connector internals.

## Drive and Structured-File Lesson

- Prefer small incremental edits over large connector payloads.
- Verify target rows, ranges, or sections after writes.
- Simplify sensitive payloads and keep GitHub abstract.
- Use RPR, Rob → Penny → Rob, when user-mediated file transfer is more reliable than direct connector editing.

## Project Chat Architecture Lesson

Departments maintain their own rooms. Chief of Staff HQ coordinates daily operations and the meeting room. Life OS Maintenance HQ protects the shared operating system.

Project chats create domain knowledge and maintain their own canonical files. Life OS Maintenance HQ owns global boot integrity, shared governance, shared execution contracts, advisory infrastructure, audits, repository structure, source boundaries, and system reconciliation.

## Desktop Department Automation Milestone

On 2026-07-17, Windows ChatGPT Classic automation was validated across all seven Department HQs.

Canonical implementation:

- `apps/lifeos-dashboard/automation/draft_department_boot.py`
- `apps/lifeos-dashboard/automation/open_department_chat_group.py`
- `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`

Validated behavior includes exact chat selection, hidden-sidebar expansion, exact destination verification, stable Group composer discovery, existing-draft preservation, clipboard round-trip verification, draft-only default behavior, explicit send authorization, and one watched successful live send.

Durable recovery playbook:

- `projects/engineering/notebook/NOTE-20260717-011-chatgpt-ui-automation-lessons-and-recovery-playbook.md`

This on-demand automation does not reactivate unattended scheduled HQ syncs.

## LifeOS Dashboard Milestone

The local Windows dashboard is operational with four verified read-mostly sources:

- GitHub
- Trello
- Todoist
- Google Calendar private iCal

The suite passed 16 tests. Guarded GitHub sync only fast-forwards a clean, strictly-behind local `main` branch. Gmail and Drive dashboard adapters remain deferred.

## Historical Preservation Rule

Git history preserves the detailed evolution of earlier snapshots. Avoid reintroducing stale personal facts, old appointments, expired tasks, or superseded project state into current boot reports.

Historical notes and prior commits may retain role names that were accurate when they were created.

## Working Principle

GitHub is the map. Drive is the filing cabinet. Trello shows flow. Todoist owns commitments. Calendar owns time. Gmail owns communications. The dashboard transports and observes. LifeOS HQ hosts the meeting. Chief of Staff HQ coordinates. Departments judge and own. Workers execute. Life OS Maintenance HQ protects durable continuity and shared contracts. Engineering builds the routing machinery. Rob decides.
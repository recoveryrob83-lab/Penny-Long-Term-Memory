# Penny Boot Log

Updated: 2026-07-17
Project: Life OS / Logistics HQ / Penny Long-Term Memory
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

- GitHub: durable memory, architecture, handoffs, abstract project state, advisories, and worker contracts.
- Drive: working records and human-facing artifacts.
- Trello: capture and current attention flow.
- Todoist: commitments and reminders.
- Calendar: timed commitments.
- Gmail: communication evidence.
- LifeOS Dashboard: read-mostly visibility into selected authoritative systems.

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

Departments maintain their own rooms. Main Assistant coordinates the building. Logistics maintains the hallways.

Project chats create domain knowledge and maintain their own canonical files. Logistics owns shared infrastructure, global boot integrity, advisory hygiene, cross-project audits, and system-wide housekeeping.

## Desktop Department Automation Milestone

On 2026-07-17, Windows ChatGPT Classic automation was validated across all seven department HQs.

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

## Working Principle

GitHub is the map. Drive is the filing cabinet. Trello shows flow. Todoist owns commitments. Calendar owns time. Gmail owns communications. The dashboard shows selected state. Main Assistant coordinates daily life. Logistics maintains durable continuity.

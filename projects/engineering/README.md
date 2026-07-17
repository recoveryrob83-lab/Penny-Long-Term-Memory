# Engineering HQ

Updated: 2026-07-17

## Purpose

Engineering HQ coordinates Rob's technical architecture, software planning, repository strategy, automation design, implementation planning, testing, and build-readiness for Life OS and related technical systems.

Engineering turns business requirements into safe, testable, build-ready technical plans and maintains durable state inside its own project domain.

## Role

Use Engineering HQ for:

- Technical architecture.
- Repository strategy.
- Software system design.
- API, connector, and MCP planning.
- Data models.
- Automation design.
- Desktop-control safety and verification.
- LifeOS Dashboard architecture and reliability.
- Automation Command Center architecture.
- Prompt systems and command interfaces.
- Testing strategy.
- Implementation sequencing.
- Build-risk analysis.
- Technical feasibility review.
- Build-ready implementation packets.
- Engineering-owned durable-memory maintenance.

## Current Operating Tracks

- Automation Command Center Phase 1 design and implementation, manual Run Now only.
- Desktop department automation maintenance after successful seven-HQ validation.
- LifeOS Dashboard observation, optional auto-refresh, guarded Git synchronization, and source-health behavior.
- Reliable Connector Execution Layer design, including operation-ledger, idempotency, verification, and retry policy.
- Penny Raw Capture and Inventory Worker pilots.
- Prompt launcher maintenance and deferred command-interface improvements.
- Office Leaks delivery architecture as concrete business requirements mature.

## Not This Department

- Business strategy, branding, market research, monetization, or customer discovery: Business HQ or Office Leaks HQ.
- Finance, benefits, budget, bills, subscriptions, or cost approval: Finance HQ.
- Daily one-off scheduling, ordinary logistics, executive-function support, or quick admin: Main Assistant HQ.
- Shared global boot integrity, advisory-index hygiene, cross-project audits, and system-wide housekeeping: Logistics HQ.
- Recovery, pacing, health, or sustainability judgment: Wellness HQ.

## Department File Ownership

Engineering maintains its own project subtree during routine boots, syncs, and implementation work. This includes its handoff, identity, README, status, open loops, notebooks, decision rules, implementation notes, and Engineering source-board advisory text.

Shared global files, other departments' canonical files, the Advisory Index, and cross-department architecture changes require the appropriate owner, Main Assistant, Logistics, or explicit coordinated authorization.

## Source Systems

- GitHub memory repository: abstract project state, boot files, open loops, advisories, role clarity, Engineering notes, dashboard code, and desktop-automation code.
- Dedicated software repositories: future home for educational projects and substantial standalone software projects.
- Google Drive: working design documents, architecture notes, generated documents, and human-facing engineering artifacts.
- Todoist: Rob-facing implementation tasks and reminders.
- Calendar: meetings, deadlines, and scheduled work.
- Gmail: communication evidence when explicitly queried.
- Trello: current LifeOS attention and flow, consumed read-only by the dashboard.
- RPR/user-mediated files: structured working records and reliable fallback workflows.

## Current Technical State

The LifeOS Dashboard is locally running on Rob's Windows machine with live read-only GitHub, Trello, Todoist, and Google Calendar data. Guarded GitHub synchronization permits only clean, strictly-behind fast-forward updates. The local suite has passed with 16 tests. Gmail and Drive dashboard adapters remain deferred until demonstrated need.

Desktop department automation is operational across all seven HQs. It supports exact navigation, one bounded hidden-sidebar expansion, exact active-document verification, stable Group composer discovery, existing-draft preservation, clipboard round-trip verification, draft-only default behavior, explicit `--send` authorization, and stop-on-uncertainty behavior. A watched live send to Main Assistant HQ succeeded.

The Automation Command Center is planned inside the existing dashboard. Phase 1 will support eight exact destinations, canonical or custom prompts, draft/send mode, explicit send confirmation, manual Run Now, one-job locking, global pause, structured results, and local activity history. Scheduling is explicitly deferred.

Canonical references:

- `apps/lifeos-dashboard/automation/draft_department_boot.py`
- `apps/lifeos-dashboard/automation/open_department_chat_group.py`
- `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`
- `projects/engineering/notebook/NOTE-20260717-011-chatgpt-ui-automation-lessons-and-recovery-playbook.md`
- `projects/engineering/notebook/NOTE-20260717-012-lifeos-ui-automation-command-center-plan.md`

## Security Rule

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, private user data, or sensitive implementation details in Life OS GitHub memory.

Use ignored local environment files or the appropriate secure source system for operational credentials.

## Boot Files

- `projects/engineering/SESSION_HANDOFF.md`
- `projects/engineering/DEPARTMENT_IDENTITY.md`
- `projects/engineering/README.md`
- `projects/engineering/status.md`
- `projects/engineering/open_loops.md`

## Current Status

Active department. Current front burner: build Automation Command Center Phase 1 without importing scheduling complexity, while preserving the validated dashboard and desktop-automation safety contract.

# Engineering HQ

Updated: 2026-07-18

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

- Package D canonical prompt catalog and healthy-state post-paste verification.
- Desktop department automation maintenance under exact-navigation and stop-on-uncertainty rules.
- LifeOS Dashboard observation, optional auto-refresh, guarded Git synchronization, and source-health behavior.
- Reliable Connector Execution Layer design, including operation-ledger, idempotency, verification, and retry policy.
- Penny Raw Capture and Inventory Worker pilots.
- Prompt launcher maintenance and deferred command-interface improvements.
- Office Leaks delivery architecture as concrete business requirements mature.

## Not This Department

- Business strategy, branding, market research, monetization, or customer discovery: Business HQ or Office Leaks HQ.
- Finance, benefits, budget, bills, subscriptions, or cost approval: Finance HQ.
- Daily one-off scheduling, ordinary coordination, executive-function support, or quick administration: Chief of Staff HQ.
- Shared global boot integrity, advisory-index hygiene, cross-project audits, migrations, and system-wide housekeeping: Life OS Maintenance HQ.
- Recovery, pacing, health, or sustainability judgment: Wellness HQ.

## Department File Ownership

Engineering maintains its own project subtree during routine boots, syncs, and implementation work. This includes its handoff, identity, README, status, open loops, notebooks, decision rules, implementation notes, and Engineering source-board advisory text.

Shared global files, other departments' canonical files, the Advisory Index, and cross-department governance changes require the appropriate owner, Chief of Staff HQ, Life OS Maintenance HQ, or explicit coordinated authorization.

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

The LifeOS Dashboard is locally running on Rob's Windows machine with live read-only GitHub, Trello, Todoist, and Google Calendar data. Guarded GitHub synchronization permits only clean, strictly-behind fast-forward updates. Department Inspection has been locally verified at 414 normalized records, zero findings, and zero warnings. Gmail and general Drive dashboard adapters remain deferred until demonstrated need.

Automation naming compatibility and Department Inspection canonical labels are complete. Stable internal destination keys and scope IDs were preserved while current UI labels use Chief of Staff HQ and Life OS Maintenance HQ.

Desktop department automation supports exact destination navigation, bounded project and `Show more` recovery, exact active-document verification, stable Group composer discovery and reacquisition, occupied-composer preservation, clipboard lifetime and restoration, draft-only default behavior, explicit send authorization, one-job locking, and stop on uncertainty.

The Automation Command Center supports eight exact destinations, canonical, saved, and custom prompts, persistent schedules and run history, validated pause-on-failure and restart policy, Scheduler Ledger synchronization, and bounded cleanup controls.

Package D is the current front burner. The protected canonical catalog contains Boot, Quick Boot, Fresh / Full Boot, Sync, Nightly, Advisory, Sync Advisory, Read Advisory, and Consume Advisory. Catalog behavior and automated tests pass. In a healthy ChatGPT Classic state, the exact destination opens, the composer receives focus, and the complete canonical prompt visibly pastes without being sent, but strict clipboard and accessible-text verification still report a false failure. In a degraded spinning-loading state, the composer never becomes usable; those runs are app-readiness failures rather than write-verification evidence.

The next valid diagnostic is one healthy visible paste left untouched in the composer, followed by:

`py .\automation\probe_composer_group_clipboard.py "LifeOS HQ"`

Do not broaden timeouts, add alternate paste or focus mechanisms, weaken verification, add another witness, start Package E, or expand the automation surface before that evidence is inspected.

Canonical references:

- `apps/lifeos-dashboard/automation/draft_department_boot.py`
- `apps/lifeos-dashboard/automation/open_department_chat_group.py`
- `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`
- `apps/lifeos-dashboard/automation/probe_composer_group_clipboard.py`
- `apps/lifeos-dashboard/lifeos_dashboard/canonical_prompt_catalog.py`
- `projects/engineering/open_loops.md`
- `projects/engineering/notebook/NOTE-20260717-011-chatgpt-ui-automation-lessons-and-recovery-playbook.md`
- `projects/engineering/notebook/NOTE-20260717-013-command-center-scheduling-live-validation-and-next-recovery-edge.md`

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

Active department. Current front burner: close Package D through one evidence-led healthy-state composer probe, then validate one manual canonical draft and one fresh scheduled canonical draft. Package E and the proposed persistent Pause All Automation header control remain deferred until that gate passes.

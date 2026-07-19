# Engineering HQ

Updated: 2026-07-19

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
- Technical Worker routing, receiver validation, runtime enforcement, and reliability.
- Testing strategy.
- Implementation sequencing.
- Build-risk analysis.
- Technical feasibility review.
- Build-ready implementation packets.
- Engineering-owned durable-memory maintenance.

## Current Operating Tracks

- Package D operations-procedure and Worker-runtime implementation under the canonical shared execution and Worker contracts.
- Worker routing registry, stable Worker IDs, exact-title resolution, receiver state, revision deduplication, verification queues, wake suppression, and technical rollover.
- Receiver-side execution-envelope and semantic validation under ADV-20260718-042.
- Canonical prompt catalog and healthy-state post-paste verification as a preserved transport-validation subphase, not the full Package D definition.
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
- Shared global boot integrity, advisory-index hygiene, cross-project audits, migrations, canonical Worker governance, and system-wide housekeeping: Life OS Maintenance HQ.
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

The canonical shared architecture now lives in:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`

Package D is the current front burner. Its current purpose is to implement the technical machinery required by those procedures: routing registry, stable Worker identity, exact-title transport, execution envelopes, receiver validation, revision and duplicate state, verification queues, wake suppression, lifecycle transitions, operation-ledger evidence, and safe Worker rename or rollover behavior. Engineering implements the machinery; Life OS Maintenance owns the canonical governance contracts and profile convention.

ADV-20260718-042 remains the authoritative open advisory for receiver-side semantic validation. It is one component of the broader Package D implementation rather than a duplicate package.

The protected canonical prompt catalog and Automation Logs remain valuable transport infrastructure. Catalog behavior and automated tests pass, while healthy-state post-paste verification still has an unresolved false-negative. That defect remains a bounded transport-validation subphase. It is not the sole definition or gate for the broader operations-procedure implementation.

Do not broaden timeouts, add alternate paste or focus mechanisms, weaken verification, add another witness, begin Package E, or expand unrelated automation surfaces without direct evidence and a clear dependency on the current implementation plan.

Canonical references:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`
- `coordination/ADVISORY_INDEX.md`
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

Active department. Current front burner: turn the new execution and Worker procedures into a build-ready Engineering implementation sequence, beginning with the routing registry and execution-envelope / receiver-state contracts. Preserve canonical prompt verification as a transport subphase, keep ADV-20260718-042 as the authoritative receiver-validation component, and defer Package E or unrelated expansion.
# Chief Engineering Penny Session Handoff

Updated: 2026-07-04
Project: Chief Engineering Penny / Engineering HQ
Purpose: Project-specific handoff for engineering and software architecture chats.

## Metadata

- Project Owner: Rob
- Primary Chat: Chief Engineering Penny / Engineering HQ
- Current Phase: Active / First Engineering Research Track Identified
- Primary Systems: GitHub, GitHub software repositories when created, Google Drive, Todoist, Calendar, Gmail as needed, RPR/user-mediated files
- Sensitivity Level: Moderate
- GitHub Rule: Keep Life OS GitHub memory abstract. Never store secrets, credentials, tokens, API keys, or sensitive implementation details in memory files.

## Department Identity

Read:

`projects/engineering/DEPARTMENT_IDENTITY.md`

Chief Engineering Penny coordinates technical architecture and implementation planning.

## Boot Instructions

When Rob opens or refreshes Chief Engineering Penny:

1. Read the global boot files from `memory/STARTUP_BOOT.md`.
2. Read this project handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md` if present.
5. Read `coordination/DEPARTMENT_EVENT_INBOX.md` when advisory routing, department synchronization, or watcher procedure context is relevant.
6. Use GitHub, Drive, Todoist, Calendar, Gmail, or RPR only as needed for the specific engineering task.
7. Keep Life OS memory abstract.
8. Route product strategy, positioning, customer discovery, market research, and roadmap priority to Chief Business HQ.
9. Route cost, subscriptions, tool budgeting, or paperwork overlap to Chief of Finance Penny.
10. Route one-off daily execution to Main Assistant when appropriate.
11. Route cross-project memory and housekeeping to Life Logistics HQ.

## Current Project Status

Chief Engineering Penny has been activated as a specialist department.

Its scope is technical architecture and implementation planning, not business strategy.

Chief Business HQ defines what should be built and why.

Chief Engineering Penny defines how to build it safely, coherently, and in the right order.

Engineering has consumed the Life OS advisory workflow update. The Department Event Inbox now owns department synchronization/read/ingestion state. Todoist remains for Rob-facing action items.

Engineering has ingested ADV-20260704-002 from Chief Business HQ. Connector write reliability is now treated as a first-class Penny product architecture risk.

The first concrete engineering research track is:

- Reliable Connector Execution Layer

This track should evaluate operation ledgers / write-ahead logs, connector health states, idempotent writes, retry/backoff, degraded-mode UX, RPR/export fallback, queue-first execution, human approval checkpoints, and multi-provider abstraction.

## Advisory / Event Inbox Procedure

When Engineering creates an advisory for another department:

1. Create or update the appropriate Engineering advisory board entry, usually `coordination/boards/engineering.md`.
2. Update `coordination/ADVISORY_INDEX.md` so the advisory appears in the central dashboard.
3. Create or update the matching entry in `coordination/DEPARTMENT_EVENT_INBOX.md` so routing/read/ingestion state is tracked.
4. Do not create Todoist reminders for department synchronization unless Rob explicitly asks.
5. Keep all entries short, abstract, and non-sensitive.
6. Report to Rob what was created or changed.

Advisory Watcher v0.1 may later monitor the Advisory Index and Department Event Inbox to generate Rob-facing copy-paste routing messages. The watcher is only a reporting layer and is not the source of truth.

## Objectives

- Translate business requirements into technical requirements.
- Design software architecture, repositories, APIs, data models, automation flows, and testing plans.
- Identify dependencies, risks, cost-bearing technical choices, and implementation sequence.
- Prepare build-ready implementation packets.
- Coordinate with Business, Finance, Main Assistant, and Life Logistics HQ when work overlaps their scope.
- Keep GitHub memory abstract unless working in a dedicated software repository.
- Use the Advisory Index and Department Event Inbox for cross-department synchronization when Engineering emits advisories.

## Completed Work

- 2026-07-04: Ingested ADV-20260704-002 and created the Reliable Connector Execution Layer research track.
- 2026-07-03: Created Chief Engineering Penny / Engineering HQ project folder and department files.
- 2026-07-03: Added Engineering setup to Life OS routing and project map where needed.
- 2026-07-03: Created Engineering Drive working folder and initial scaffolding files.
- 2026-07-03: Created Engineering advisories ADV-20260703-006 and ADV-20260703-007.
- 2026-07-03: Consumed new Department Event Inbox / Advisory Watcher procedure and updated Engineering handoff.

## Active Open Loops

- Draft a Reliable Connector Execution Layer technical design note.
- Define operation ledger / write-ahead log states for intended connector writes.
- Define idempotency, retry/backoff, connector health, degraded-mode UX, and RPR/export fallback patterns.
- Coordinate with Chief Business HQ to translate the reliability design into product requirements.
- Coordinate with Chief of Finance Penny before committing to cost-bearing tools, hosting, queues, APIs, or subscriptions.
- Help refine Advisory Watcher / event-inbox architecture if Rob routes that work back to Engineering.

## Working Documents / Links

- GitHub memory project folder: `projects/engineering/`
- Engineering advisory board: `coordination/boards/engineering.md`
- Department Event Inbox: `coordination/DEPARTMENT_EVENT_INBOX.md`
- Drive working folder: Life Organization > Chief Engineering Penny
- Drive working docs:
  - `Engineering HQ - Technical Baseline`
  - `Engineering HQ - Implementation Packet Template`
  - `Engineering HQ - Tracker`
  - `Reliable Connector Execution Layer - Design Note` when created/available
- Software repositories should be separate from Life OS memory when created.
- Todoist owns Rob-facing engineering action reminders only.
- Calendar owns engineering meetings and deadlines.
- Drive or RPR should hold working design docs, implementation packets, and generated artifacts when useful.

## Source Systems

- GitHub memory repo: abstract Engineering HQ state, handoff, open loops, status, role clarity, advisory board, and event-inbox entries.
- Dedicated software repos: code, technical docs, issues, branches, PRs, tests, and implementation artifacts when created.
- Google Drive: working docs, design notes, architecture docs, and generated artifacts.
- Todoist: Rob-facing tasks, reminders, follow-ups, and implementation actions.
- Calendar: meetings, deadlines, and scheduled work.
- Gmail: communications and evidence when needed.
- RPR/user-mediated files: reliable path for structured records.

## Connector / Safety Notes

- Prefer small, verifiable updates.
- Verify connector writes when possible.
- Never place secrets, credentials, tokens, or API keys in GitHub memory.
- Use RPR when reliability matters.
- Do not repeatedly retry writes that trigger safety blocks.
- For future product design, connector writes need observable operation states and durable recovery paths.

## Privacy / Security Guardrails

GitHub memory may store department scope, abstract open loops, routing notes, and non-sensitive status summaries.

Operational details belong in the proper working system.

Secrets and credentials should never be pasted into chat or committed to GitHub.

## Decision Log

- Chief Engineering Penny is a specialist department.
- Chief Business HQ defines what to build and why.
- Chief Engineering Penny defines how to build and in what order.
- Chief of Finance Penny owns cost and paperwork overlap.
- Main Assistant handles daily one-off execution.
- Life Logistics HQ keeps the Life OS cross-project map tidy.
- Department Event Inbox owns system synchronization state.
- Todoist owns Rob-facing action items.
- Advisory Watcher v0.1 is a reporting layer only unless Rob later approves write behavior.
- Reliable Connector Execution Layer is the first concrete Engineering research track after ADV-20260704-002.

## Immediate Next Actions

1. Draft the Reliable Connector Execution Layer design note.
2. Use Engineering Drive scaffolding for technical baselines, implementation packets, and tracking.
3. Create detailed technical docs only when useful, preferably in Drive, RPR, or a dedicated software repository.
4. When Engineering creates cross-department advisories, update the Engineering board, Advisory Index, and Department Event Inbox.
5. Update this handoff after meaningful engineering work.

## Notes for Next Penny

This chat is Chief Engineering Penny when booted directly. It should not absorb Business, Finance, Main Assistant, or Life Logistics work. It should turn product requirements into build-ready technical plans and use the advisory/event-inbox procedure for cross-department synchronization.

The current first engineering workstream is Reliable Connector Execution Layer: make Penny connector-dependent execution observable, verified, recoverable, idempotent, and user-safe.

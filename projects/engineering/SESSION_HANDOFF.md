# Chief Engineering Penny Session Handoff

Updated: 2026-07-06
Project: Chief Engineering Penny / Engineering HQ
Purpose: Project-specific handoff for engineering and software architecture chats.

## Metadata

- Project Owner: Rob
- Primary Chat: Chief Engineering Penny / Engineering HQ
- Current Phase: Active / First Engineering Research Track Started
- Primary Systems: GitHub, GitHub software repositories when created, Google Drive, Todoist, Calendar, Gmail as needed, RPR/user-mediated files, Engineering advisory board, Advisory Index
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
5. Read `coordination/ADVISORY_INDEX.md` when advisory routing or cross-department advisory status is relevant.
6. Read `coordination/boards/engineering.md` when Engineering needs to create, consume, or verify an Engineering advisory.
7. Do not use `coordination/DEPARTMENT_EVENT_INBOX.md` for normal advisory routing; it is frozen historical record unless Rob explicitly reactivates it.
8. Use GitHub, Drive, Todoist, Calendar, Gmail, or RPR only as needed for the specific engineering task.
9. Keep Life OS memory abstract.
10. Route product strategy, positioning, customer discovery, market research, and roadmap priority to Chief Business HQ.
11. Route cost, subscriptions, tool budgeting, or paperwork overlap to Chief of Finance Penny.
12. Route one-off daily execution to Main Assistant when appropriate.
13. Route cross-project memory and housekeeping to Life Logistics HQ.

## Current Project Status

Chief Engineering Penny has been activated as a specialist department.

Its scope is technical architecture and implementation planning, not business strategy.

Chief Business HQ defines what should be built and why.

Chief Engineering Penny defines how to build it safely, coherently, and in the right order.

Engineering has consumed the Life OS advisory routing simplification. Advisory Index now owns active advisory routing state. Department Event Inbox is frozen historical record only. Todoist remains for Rob-facing action items.

Engineering has ingested ADV-20260704-002 from Chief Business HQ. Connector write reliability is now treated as a first-class Penny product architecture risk.

The first concrete engineering research track is:

- Reliable Connector Execution Layer

This track should evaluate operation ledgers / write-ahead logs, connector health states, idempotent writes, retry/backoff, degraded-mode UX, RPR/export fallback, queue-first execution, human approval checkpoints, and multi-provider abstraction.

Working design note created in Drive:

- `Reliable Connector Execution Layer - Design Note`
- https://docs.google.com/document/d/1R0SYHk7PLCDerOHcO-sSXGvybrGx8rOAGvQinsyAR3M/edit?usp=drivesdk

## Advisory Procedure

When Engineering creates an advisory for another department:

1. Create or update the appropriate Engineering advisory board entry, usually `coordination/boards/engineering.md`.
2. Update `coordination/ADVISORY_INDEX.md` as the sole active routing dashboard, pointing to the source board and naming the target department.
3. Do not update `coordination/DEPARTMENT_EVENT_INBOX.md` unless Rob explicitly reactivates it.
4. Do not create Todoist reminders for department synchronization unless Rob explicitly asks.
5. Keep all entries short, abstract, and non-sensitive.
6. Report to Rob what was created or changed.

For multi-target advisories, track target departments in the Advisory Index entry and source-board advisory text. Do not mark acknowledged or implemented until all required targets have reported read or handled status to Rob, unless the source department records separate per-target acknowledgements.

## Objectives

- Translate business requirements into technical requirements.
- Design software architecture, repositories, APIs, data models, automation flows, and testing plans.
- Identify dependencies, risks, cost-bearing technical choices, and implementation sequence.
- Prepare build-ready implementation packets.
- Coordinate with Business, Finance, Main Assistant, and Life Logistics HQ when work overlaps their scope.
- Keep GitHub memory abstract unless working in a dedicated software repository.
- Use the Advisory Index and Engineering advisory board for cross-department synchronization when Engineering emits advisories.

## Completed Work

- 2026-07-06: Adopted simplified advisory routing: source board plus Advisory Index only; Department Event Inbox frozen historical.
- 2026-07-04: Created `Reliable Connector Execution Layer - Design Note` in Drive.
- 2026-07-04: Ingested ADV-20260704-002 and created the Reliable Connector Execution Layer research track.
- 2026-07-03: Created Chief Engineering Penny / Engineering HQ project folder and department files.
- 2026-07-03: Added Engineering setup to Life OS routing and project map where needed.
- 2026-07-03: Created Engineering Drive working folder and initial scaffolding files.
- 2026-07-03: Created Engineering advisories ADV-20260703-006 and ADV-20260703-007.
- 2026-07-03: Consumed initial Department Event Inbox / Advisory Watcher procedure; later superseded by simplified Advisory Index routing.

## Active Open Loops

- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft operation ledger / write-ahead log schema for intended connector writes.
- Define idempotency, retry/backoff, connector health, degraded-mode UX, and RPR/export fallback patterns.
- Coordinate with Chief Business HQ to translate the reliability design into product requirements.
- Coordinate with Chief of Finance Penny before committing to cost-bearing tools, hosting, queues, APIs, or subscriptions.
- Help refine advisory routing, boot reliability, or connector architecture if Rob routes that work back to Engineering.

## Working Documents / Links

- GitHub memory project folder: `projects/engineering/`
- Engineering advisory board: `coordination/boards/engineering.md`
- Advisory Index: `coordination/ADVISORY_INDEX.md`
- Department Event Inbox: `coordination/DEPARTMENT_EVENT_INBOX.md` is frozen historical record only
- Drive working folder: Life Organization > Chief Engineering Penny
- Drive working docs:
  - `Engineering HQ - Technical Baseline`
  - `Engineering HQ - Implementation Packet Template`
  - `Engineering HQ - Tracker`
  - `Reliable Connector Execution Layer - Design Note`: https://docs.google.com/document/d/1R0SYHk7PLCDerOHcO-sSXGvybrGx8rOAGvQinsyAR3M/edit?usp=drivesdk
- Software repositories should be separate from Life OS memory when created.
- Todoist owns Rob-facing engineering action reminders only.
- Calendar owns engineering meetings and deadlines.
- Drive or RPR should hold working design docs, implementation packets, and generated artifacts when useful.

## Source Systems

- GitHub memory repo: abstract Engineering HQ state, handoff, open loops, status, role clarity, advisory board, and Advisory Index routing notes.
- Dedicated software repos: code, technical docs, issues, branches, PRs, tests, and implementation artifacts when created.
- Google Drive: working docs, design notes, architecture docs, and generated artifacts.
- Todoist: Rob-facing tasks, reminders, follow-ups, and implementation actions.
- Calendar: meetings, deadlines, and scheduled work.
- Gmail: communications and evidence when needed.
- RPR/user-mediated files: reliable path for structured records.
- Department Event Inbox: frozen historical synchronization/read/ingestion register only.

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
- Advisory Index owns active advisory routing state.
- Department Event Inbox is frozen historical record only unless Rob explicitly reactivates it.
- Todoist owns Rob-facing action items.
- Reliable Connector Execution Layer is the first concrete Engineering research track after ADV-20260704-002.

## Immediate Next Actions

1. Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
2. Draft the operation ledger schema.
3. Draft connector health and retry/backoff policy.
4. Coordinate with Business HQ on product requirements and Finance on cost-bearing infrastructure.
5. Update this handoff after meaningful engineering work.

## Notes for Next Penny

This chat is Chief Engineering Penny when booted directly. It should not absorb Business, Finance, Main Assistant, or Life Logistics work. It should turn product requirements into build-ready technical plans and use the Engineering advisory board plus Advisory Index for cross-department synchronization.

The current first engineering workstream is Reliable Connector Execution Layer: make Penny connector-dependent execution observable, verified, recoverable, idempotent, and user-safe.
# Chief Engineering Penny Session Handoff

Updated: 2026-07-10
Project: Chief Engineering Penny / Engineering HQ
Purpose: Project-specific handoff for engineering and software architecture chats.

## Metadata

- Project Owner: Rob
- Primary Chat: Chief Engineering Penny / Engineering HQ
- Current Phase: Active / Connector Reliability, Worker Architecture, and Office Leaks Delivery Architecture
- Primary Systems: GitHub, dedicated software repositories when created, Google Drive, Todoist, Calendar, Gmail as needed, RPR/user-mediated files, Engineering advisory board, Advisory Index
- Sensitivity Level: Moderate
- GitHub Rule: Keep Life OS GitHub memory abstract. Never store secrets, credentials, tokens, API keys, private user data, or sensitive implementation details in memory files.

## Department Identity

Read:

`projects/engineering/DEPARTMENT_IDENTITY.md`

Chief Engineering Penny coordinates technical architecture and implementation planning.

## Boot Instructions

When Rob opens or refreshes Chief Engineering Penny:

1. Read the global boot files from `memory/STARTUP_BOOT.md`.
2. Read this project handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Read `coordination/ADVISORY_INDEX.md` when advisory routing or cross-department advisory status is relevant.
6. Read `coordination/boards/engineering.md` when Engineering needs to create, consume, verify, or reconcile an Engineering advisory.
7. Do not use `coordination/DEPARTMENT_EVENT_INBOX.md` for normal advisory routing; it is frozen historical record unless Rob explicitly reactivates it.
8. Use GitHub, Drive, Todoist, Calendar, Gmail, or RPR only as needed for the specific engineering task.
9. Keep Life OS memory abstract.
10. Route product strategy, positioning, customer discovery, market research, and roadmap priority to Chief Business HQ or Office Leaks Consulting HQ.
11. Route cost, subscriptions, tool budgeting, or paperwork overlap to Chief of Finance Penny.
12. Route one-off daily execution to Main Assistant when appropriate.
13. Route cross-project memory and housekeeping to Life Logistics HQ.

## Current Project Status

Chief Engineering Penny is active as a specialist department.

Its scope is technical architecture and implementation planning, not business strategy.

Chief Business HQ and Office Leaks Consulting HQ define what should be built and why.

Chief Engineering Penny defines how to build it safely, coherently, and in the right order.

Engineering has consumed the simplified Life OS advisory routing model. The Advisory Index owns active routing state. Department Event Inbox is frozen historical record. Todoist remains for Rob-facing action items.

## Current Engineering Tracks

### 1. Reliable Connector Execution Layer

Connector write reliability remains a first-class Penny product architecture risk.

The track should evaluate:

- operation ledgers and write-ahead logs,
- connector health states,
- idempotent writes,
- bounded retry/backoff,
- degraded-mode user experience,
- RPR/export/manual-upload fallback,
- queue-first execution,
- human approval checkpoints,
- multi-provider abstraction,
- and explicit verified/unverified/failed operation states.

Working design note:

- `Reliable Connector Execution Layer - Design Note`
- https://docs.google.com/document/d/1R0SYHk7PLCDerOHcO-sSXGvybrGx8rOAGvQinsyAR3M/edit?usp=drivesdk

Current field lessons:

- small connector operations are materially more reliable than large batches,
- explicit connector invocation improves reliability,
- chats are more stable when focused on one connector,
- and a fresh booted chat is preferable to repeated retries when connector state degrades.

These are observed operating patterns, not confirmed claims about platform internals.

### 2. Life OS Worker Architecture

Engineering has completed and handed off two formal worker packages.

Durable worker layer:

- `workers/README.md`
- `workers/WORKER_STANDARD.md`

Penny Raw Capture Worker:

- `workers/penny-raw-capture/WORKER_BOOT.md`
- `workers/penny-raw-capture/SESSION_HANDOFF.md`
- Mission: `Capture first. Organize later.`
- Canonical target: `Life OS Raw Capture Inbox`
- Downstream owner: Main Assistant Penny

Penny Inventory Worker:

- `workers/penny-inventory/WORKER_BOOT.md`
- `workers/penny-inventory/SESSION_HANDOFF.md`
- `workers/penny-inventory/IMPLEMENTATION_REPORT.md`
- Mission: `See the item. Record the item. Verify the row.`
- Canonical target: `For Sale Inventory`
- Current state: architecture complete; ready for real-world pilot

The Inventory Worker uses one row per sale item and intentionally excludes pricing, bundling, listing creation, publication, and sale strategy.

Engineering standards now formalized for workers:

- narrow scope,
- canonical resource identity,
- explicit connector invocation when needed,
- no fabricated success,
- post-write verification,
- precise failure states,
- privacy and source-of-truth boundaries,
- partial-success preservation,
- and escalation outside worker authority.

The next meaningful worker evidence is production behavior, not additional scaffolding.

### 3. Office Leaks Delivery Architecture

Engineering supports Office Leaks Consulting with two integrated delivery layers.

Mechanical workflow layer:

- map,
- score,
- scope,
- sprint,
- verify,
- handoff,
- follow up.

Human-system layer:

- respect,
- rapport,
- internal champion,
- users,
- Aha Moment,
- adoption verification,
- relational follow-up.

Current Engineering references:

- `projects/engineering/notebook/NOTE-20260708-005-office-leak-delivery-playbooks-v1.md`
- `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`

Related Drive document:

- `Engineering Delivery Architecture Specification - HVAC Office Cleanup`

## Advisory State

Canonical Advisory Index state:

- No open advisories.
- ADV-20260710-032 is implemented / acknowledged / closed.
- ADV-20260710-031 is implemented / closed.
- ADV-20260709-030 is implemented / closed.
- ADV-20260709-029 is closed / implemented through ADV-20260709-030.

The Engineering source board and Advisory Index agree.

Do not update Department Event Inbox.

## Objectives

- Translate business requirements into technical requirements.
- Design software architecture, repositories, APIs, data models, automation flows, worker contracts, and testing plans.
- Identify dependencies, risks, cost-bearing technical choices, and implementation sequence.
- Prepare build-ready implementation packets.
- Coordinate with Business, Office Leaks, Finance, Main Assistant, and Life Logistics HQ when work overlaps their scope.
- Keep GitHub memory abstract unless working in a dedicated software repository.
- Use the Advisory Index and Engineering advisory board for cross-department synchronization.

## Completed Recent Work

- 2026-07-10: Completed Penny Inventory Worker architecture review and handed off documentation refresh to Life Logistics.
- 2026-07-10: Life Logistics implemented and closed ADV-20260710-032, creating the Penny Inventory Worker package and verifying the canonical inventory Sheet.
- 2026-07-10: Advisory Board Lifecycle Standard created and Engineering advisory board compacted under ADV-20260710-031.
- 2026-07-09: Engineering completed rapid-capture worker architecture through ADV-20260709-029 and ADV-20260709-030.
- 2026-07-09: Life Logistics implemented the worker layer and Penny Raw Capture Worker package.
- 2026-07-08: Created Office Leaks delivery-playbook and human-system architecture notes.
- 2026-07-08: Life Logistics implemented ADV-20260708-027 and synchronized Engineering architecture across Life OS.
- 2026-07-06: Adopted simplified advisory routing.
- 2026-07-04: Created the Reliable Connector Execution Layer design note.
- 2026-07-04: Ingested ADV-20260704-002 and made connector reliability a first-class architecture risk.

## Active Open Loops

- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft operation ledger / write-ahead log schema.
- Define idempotency, verification, retry/backoff, connector health, degraded-mode UX, and RPR/export fallback patterns.
- Pilot Penny Inventory Worker with 2–3 real items before scaling to larger batches.
- Observe Penny Raw Capture Worker in real use.
- Continue Office Leaks one-problem delivery architecture as Business requirements mature.
- Support additional worker architecture only when a repeatable bounded job justifies it.
- Coordinate with Chief Business HQ and Office Leaks Consulting HQ on requirements.
- Coordinate with Chief of Finance Penny before cost-bearing infrastructure commitments.

## Working Documents / Links

- GitHub memory project folder: `projects/engineering/`
- Engineering advisory board: `coordination/boards/engineering.md`
- Advisory Index: `coordination/ADVISORY_INDEX.md`
- Worker root: `workers/`
- Department Event Inbox: historical/frozen only
- Drive working folder: Life Organization > Chief Engineering Penny
- Drive working docs:
  - `Engineering HQ - Technical Baseline`
  - `Engineering HQ - Implementation Packet Template`
  - `Engineering HQ - Tracker`
  - `Reliable Connector Execution Layer - Design Note`
  - `Engineering Delivery Architecture Specification - HVAC Office Cleanup`
- Software repositories should be separate from Life OS memory when created.
- Todoist owns Rob-facing engineering action reminders.
- Calendar owns engineering meetings and deadlines.
- Drive or RPR should hold working design docs, implementation packets, and generated artifacts.

## Connector / Safety Notes

- Prefer small, verifiable operations.
- Invoke connectors explicitly when practical.
- Keep connector-heavy chats focused on one connector when possible.
- Verify connector writes.
- Never place secrets, credentials, tokens, API keys, or private operational data in GitHub memory.
- Use RPR when reliability matters more than automation.
- Do not repeatedly retry writes that trigger safety blocks.
- Start a fresh booted chat when connector state becomes unstable.
- Connector-dependent execution needs observable operation states and durable recovery paths.
- Never claim an external operation succeeded without an actual successful tool operation.

## Decision Log

- Chief Engineering Penny is a specialist department.
- Chief Business HQ and Office Leaks Consulting HQ define what should be built and why.
- Chief Engineering Penny defines how to build and in what order.
- Chief of Finance Penny owns cost and paperwork overlap.
- Main Assistant handles daily one-off execution and authorized downstream processing.
- Life Logistics HQ keeps the Life OS cross-project map tidy.
- Advisory Index owns active advisory routing state.
- Department Event Inbox is frozen unless Rob explicitly reactivates it.
- Todoist owns Rob-facing action items.
- Reliable Connector Execution Layer remains the first concrete Engineering research track.
- Workers are narrow operational executors under stable contracts, not miniature departments.

## Immediate Next Actions

1. Pilot Penny Inventory Worker with 2–3 real sale items.
2. Observe one-row-per-item writes, image-reference sequencing, uncertainty labels, and final Sheet verification.
3. Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
4. Draft the operation ledger schema.
5. Draft connector health and bounded retry/backoff policy.
6. Continue Office Leaks delivery architecture when requirements arrive.

## Notes for Next Penny

This chat is Chief Engineering Penny when booted directly. It should not absorb Business, Finance, Main Assistant, or Life Logistics work. It should turn requirements into build-ready technical plans and use the Engineering advisory board plus Advisory Index for cross-department synchronization.

The active engineering themes are connector reliability, verified external operations, live worker pilots, bounded worker architecture, and practical Office Leaks delivery design.

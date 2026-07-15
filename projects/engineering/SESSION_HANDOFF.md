# Chief Engineering Penny Session Handoff

Updated: 2026-07-15
Project: Chief Engineering Penny / Engineering HQ
Purpose: Project-specific handoff for engineering and software architecture chats.

## Metadata

- Project Owner: Rob
- Primary Chat: Chief Engineering Penny / Engineering HQ
- Current Phase: Active / Chat HQ Operations, Connector Reliability, Worker Pilots, and Office Leaks Delivery Architecture
- Primary Systems: GitHub, dedicated software repositories when created, Google Drive, Todoist, Calendar, Gmail as needed, RPR/user-mediated files, Engineering advisory board, Advisory Index
- Sensitivity Level: Moderate
- GitHub Rule: Keep Life OS GitHub memory abstract. Never store secrets, credentials, tokens, API keys, private user data, or sensitive implementation details in memory files.

## Boot Instructions

1. Follow the canonical global boot sequence in `memory/STARTUP_BOOT.md`.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Read `coordination/ADVISORY_INDEX.md` when advisory routing or cross-department status is relevant.
6. Read a source department advisory board only when the index points to a relevant open advisory or Rob names it.
7. Do not use `coordination/DEPARTMENT_EVENT_INBOX.md` for normal routing; it is frozen historical state.
8. Use connectors and RPR only as required by the specific task.
9. Keep Life OS GitHub memory abstract and non-sensitive.

## Department Role

Chief Engineering Penny owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, worker contracts, debugging analysis, implementation sequencing, and build-readiness.

Chief Business HQ and Office Leaks Consulting HQ define what should be built and why. Engineering defines how to build it safely, coherently, and in the right order.

Route:

- business strategy, positioning, customer discovery, and monetization to Business or Office Leaks;
- costs, subscriptions, paid APIs, hosting, and financial risk to Finance;
- daily one-off execution to Main Assistant;
- cross-project memory hygiene and housekeeping to Life Logistics;
- health, recovery sustainability, and wellness planning to Wellness.

## Chat and Work Operating Model

The seven LifeOS department discussion HQ chats are open and operational as of 2026-07-15.

Regular Chat is the default environment for:

- architecture discussion and planning;
- GitHub boot, synchronization, and light documentation work;
- prompt systems and command databases;
- API, connector, MCP, and platform research;
- code review and debugging discussion;
- advisories and cross-department routing;
- small authorized connector-backed updates.

Work mode is reserved for:

- substantial code writing or testing;
- local repository operations;
- large file edits;
- test-suite execution;
- application packaging;
- browser or desktop automation;
- complex artifact generation;
- long-running implementation work.

Each HQ is one structured perspective within a coherent Penny system, not an autonomous agent. Never claim an action, test, deployment, or connector write occurred without verified tool evidence.

## Current Engineering Tracks

### 1. Reliable Connector Execution Layer

Connector reliability remains a first-class architecture risk. Current design concerns:

- operation ledger or write-ahead log;
- connector health states;
- idempotency keys and duplicate prevention;
- post-write verification;
- bounded retry and stop rules;
- degraded-mode language and recovery paths;
- RPR, export, manual-upload, or alternate-worker fallback;
- queue-first execution and human approval checkpoints.

Observed operating patterns, not platform guarantees:

- small connector operations are more reliable than large batches;
- explicit connector invocation helps maintain scope;
- one-connector-focused sessions are easier to verify;
- fresh booted chats are preferable to repeated retries when connector behavior degrades.

Working Drive document: `Reliable Connector Execution Layer - Design Note`.

### 2. Life OS Worker Architecture

Implemented worker packages:

- Penny Raw Capture Worker: `workers/penny-raw-capture/`
- Penny Inventory Worker: `workers/penny-inventory/`

Raw Capture mission: `Capture first. Organize later.`

Inventory mission: `See the item. Record the item. Verify the row.`

The Inventory Worker uses one row per physical item and excludes pricing, bundling, listing creation, publication, and sale strategy. Both workers need real operational evidence before Engineering proposes additional worker architecture.

### 3. Office Leaks Delivery Architecture

Mechanical layer:

- map;
- score;
- scope;
- sprint;
- verify;
- handoff;
- follow up.

Human-system layer:

- respect;
- rapport;
- internal champion;
- users;
- Aha Moment;
- adoption verification;
- relational follow-up.

Current references:

- `projects/engineering/notebook/NOTE-20260708-005-office-leak-delivery-playbooks-v1.md`
- `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`
- Drive: `Engineering Delivery Architecture Specification - HVAC Office Cleanup`

### 4. LifeOS Chat HQ Architecture

ADV-20260715-036 is implemented, acknowledged, and closed. Rob confirmed all seven discussion HQ chats are open and ready.

The operational architecture now separates:

- Chat HQs for conversation, planning, research, synchronization, and light connector work;
- Work mode for heavy implementation;
- departments for judgment and durable state;
- workers for narrow repeatable procedures;
- Main Assistant for overall coordination and synthesis.

The next Engineering responsibility is observation and refinement based on real use, not more launch scaffolding.

## Advisory State

As of 2026-07-15:

- No open advisories are listed in `coordination/ADVISORY_INDEX.md`.
- ADV-20260715-036 is implemented / acknowledged / closed after Rob launched all seven Chat HQs.
- ADV-20260715-035 is implemented / acknowledged / closed after the Daily Operating SOP was integrated into the global boot path.
- Department Event Inbox remains frozen and must not be updated for normal advisory routing.

## Active Open Loops

- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft the operation ledger / write-ahead log schema.
- Define idempotency, verification, retry, connector-health, degraded-mode, and recovery patterns.
- Pilot Penny Inventory Worker with 2–3 real items before scaling.
- Observe Penny Raw Capture Worker in real use.
- Compare worker pilot results against `workers/WORKER_STANDARD.md` before proposing more workers.
- Continue Office Leaks delivery architecture as Business requirements mature.
- Observe the seven Chat HQs for routing friction, duplicated responsibility, stale boot assumptions, connector limitations, and model-usage waste.
- Keep Engineering HQ Daily Sync paused until scheduled execution architecture is more reliable and Rob explicitly resumes it.

## Completed Recent Work

- 2026-07-15: Seven LifeOS department discussion HQ chats opened and declared ready by Rob; ADV-20260715-036 closed.
- 2026-07-15: Daily Operating SOP integrated into the global boot path under ADV-20260715-035.
- 2026-07-15: Expanded LifeOS shortcut and hub command vocabulary synchronized in `memory/CONTEXT_REMINDER.md`.
- 2026-07-10: Penny Inventory Worker architecture completed and package implemented.
- 2026-07-10: Advisory Board Lifecycle Standard created and Engineering board compacted.
- 2026-07-09: Formal worker layer and Penny Raw Capture Worker implemented.
- 2026-07-08: Office Leaks delivery-playbook and human-system architecture notes created.
- 2026-07-04: Reliable Connector Execution Layer research track established.

## Immediate Next Actions

1. Use the Engineering Chat HQ for ordinary planning and light GitHub work.
2. Pilot the Inventory Worker with 2–3 real sale items when Rob is ready.
3. Observe Raw Capture Worker behavior in real use.
4. Draft the Reliable Connector Execution Layer implementation packet outline and operation ledger schema.
5. Refine the Chat HQ architecture only from observed friction, not speculative complexity.

## Safety and Truthfulness

- Prefer small, verifiable operations.
- Fetch before editing and verify after writing.
- Keep connector-heavy work narrowly scoped.
- Never place secrets, credentials, tokens, API keys, financial account details, medical details, or private operational data in GitHub memory.
- Use dedicated software repositories for code when created.
- Use Drive or RPR for working design documents and structured artifacts.
- Never claim success without a successful tool result.

## Notes for Next Penny

This is Chief Engineering Penny. Keep engineering practical, skeptical, maintainable, and aligned with Rob's available time, money, attention, and model usage. The active themes are connector reliability, verified external operations, real worker pilots, Chat/Work separation, and practical Office Leaks delivery architecture.
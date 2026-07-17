# Chief Engineering Penny Session Handoff

Updated: 2026-07-17
Project: Chief Engineering Penny / Engineering HQ
Purpose: Project-specific handoff for engineering, software architecture, prompt systems, workers, connector reliability, and the LifeOS Dashboard.

## Metadata

- Project Owner: Rob
- Primary Chat: Chief Engineering Penny / Engineering HQ
- Current Phase: Active / LifeOS Dashboard V0, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture
- Primary Systems: GitHub, Google Drive, Trello, Todoist, Calendar, Gmail as needed, RPR/user-mediated files, Engineering advisory board, Advisory Index
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, financial account details, medical details, private user data, or sensitive implementation details in Life OS memory files.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md`.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Read `coordination/ADVISORY_INDEX.md` only when advisory routing or cross-department status is relevant.
6. Read a source board only when the index points to a relevant advisory or Rob names it.
7. Do not use `coordination/DEPARTMENT_EVENT_INBOX.md` for normal routing.
8. Keep connector work small, explicit, and verifiable.

## Department Role

Chief Engineering Penny owns:

- technical architecture;
- software planning and repository strategy;
- API, connector, and MCP research;
- automation and data-model design;
- prompt systems and command interfaces;
- testing and debugging strategy;
- worker contracts;
- implementation sequencing;
- build-readiness and truthful verification.

Chief Business HQ and Office Leaks Consulting HQ define what should be built and why. Engineering defines how to build it safely and in the right order.

Route:

- business strategy and monetization to Business or Office Leaks;
- cost-bearing technical choices to Finance;
- daily one-off execution to Main Assistant;
- shared global memory hygiene to Life Logistics;
- recovery and health sustainability to Wellness.

## Chat and Work Model

Use regular Chat for architecture discussion, planning, research, GitHub synchronization, prompt work, code-review discussion, debugging analysis, advisories, and small authorized connector updates.

Use Work for bounded execution requiring local files, terminal access, substantial coding, test execution, browser or desktop control, application packaging, or complex artifacts.

Never claim an action, test, deployment, or connector write occurred without verified evidence.

## Current Engineering Tracks

### 1. LifeOS Dashboard V0

The dashboard has moved from concept to a runnable first scaffold.

Canonical application path:

- `apps/lifeos-dashboard/`

Pull request:

- PR #2 — `Scaffold local LifeOS dashboard`

Merged commit:

- `bdf920112e8142179d3da91a3e7983e1a5d48c27`

Current stack:

- Python 3.11+;
- FastAPI backend;
- Jinja2 templates;
- plain HTML, CSS, and JavaScript frontend;
- Uvicorn localhost server;
- sample JSON source adapter;
- pytest smoke tests.

Implemented V0 regions:

- source health and freshness;
- Today and next-event view;
- Trello Now, Next, and Waiting mock state;
- Gmail attention signals;
- Drive shortcuts;
- recent GitHub notebook activity;
- copyable Penny commands.

Architecture boundaries:

- local browser app first;
- bind to `127.0.0.1`;
- sample data before authentication;
- source systems remain authoritative;
- Penny remains the worker and conversational control layer;
- read-only or read-mostly before write controls;
- account-linked financial connector remains excluded from multi-connector dashboard operation;
- pywebview packaging may come later after the browser version proves useful.

Verification completed before merge:

- Python compilation succeeded;
- `python -m pytest -q` returned 3 passing tests;
- a live Uvicorn server started on `127.0.0.1:8765`;
- `/`, `/api/health`, and `/api/dashboard` returned HTTP 200.

The execution container could not resolve GitHub for a fresh clone, so verification used locally reconstructed copies of the exact runtime scaffold. The application itself passed all runtime checks.

Immediate next milestone:

1. Rob pulls current `main` on his Windows machine.
2. Engineering guides Rob through environment creation, dependency installation, and first launch.
3. Rob reviews what the sample dashboard communicates within ten seconds.
4. Engineering records layout, noise, missing information, and usefulness feedback.
5. GitHub becomes the first live read adapter after the screen is accepted.

Do not connect every source before validating the dashboard itself.

### 2. Reliable Connector Execution Layer

Connector reliability remains a first-class architecture risk.

Current design concerns:

- operation ledger or write-ahead log;
- connector health states;
- idempotency and duplicate prevention;
- post-write verification;
- bounded retry and stop rules;
- degraded-mode language and recovery paths;
- manual, RPR, export, or alternate-worker fallback;
- queue-first execution and human approval checkpoints.

Observed field lessons favor small operations, explicit connector invocation, narrow connector scope, post-write verification, and fresh-chat recovery after degradation.

Working Drive document:

- `Reliable Connector Execution Layer - Design Note`

### 3. Life OS Worker Architecture

Implemented worker packages:

- Penny Raw Capture Worker: `workers/penny-raw-capture/`
- Penny Inventory Worker: `workers/penny-inventory/`

Raw Capture mission: `Capture first. Organize later.`

Inventory mission: `See the item. Record the item. Verify the row.`

Both workers need real operational evidence before more workers are proposed.

### 4. Office Leaks Delivery Architecture

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

References:

- `projects/engineering/notebook/NOTE-20260708-005-office-leak-delivery-playbooks-v1.md`
- `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`
- Drive: `Engineering Delivery Architecture Specification - HVAC Office Cleanup`

### 5. Prompt Launcher and Command Interface

The launcher remains a secondary interface over the canonical vocabulary in `memory/CONTEXT_REMINDER.md`.

Completed repair:

- corrected literal `\n` output from Hub Boot onward.

Deferred improvements:

- `/READADVISORY`;
- `/CONSUMEADVISORY`;
- explicit scope metadata and better department-selector labels.

Notebook reference:

- `projects/engineering/notebook/NOTE-20260716-007-prompt-launcher-advisory-commands-and-scope.md`

### 6. LifeOS Chat HQ Architecture

All seven department discussion HQ chats are operational.

The system separates:

- Chat HQs for conversation, planning, research, synchronization, and light connector work;
- Work for heavy implementation;
- departments for judgment and durable state;
- workers for narrow procedures;
- Main Assistant for coordination and synthesis.

Refine this architecture only from observed friction.

## Advisory State

As of 2026-07-17:

- No open advisories are listed in `coordination/ADVISORY_INDEX.md`.
- ADV-20260716-038 is acknowledged / ingested / closed.
- ADV-20260716-039 is implemented / acknowledged / closed after shared global summaries were reconciled.
- Department Event Inbox remains frozen historical state.

## Active Open Loops

- Guide Rob through the first local LifeOS Dashboard V0 launch.
- Capture dashboard first-use feedback before live integrations.
- Build the GitHub read adapter after the screen is accepted.
- Pilot Penny Inventory Worker with 2–3 real items.
- Observe Penny Raw Capture Worker in real use.
- Draft the Reliable Connector Execution Layer implementation packet and operation-ledger schema.
- Define idempotency, verification, connector-health, retry, and recovery patterns.
- Continue Office Leaks delivery architecture as requirements mature.
- Observe Chat HQ routing friction and model-use waste.
- Keep Engineering HQ Daily Sync paused until explicitly resumed.

## Deferred

- Trello, Todoist, Calendar, Gmail, and Drive live dashboard adapters follow the GitHub adapter and screen validation.
- Desktop-window packaging follows browser usefulness.
- Prompt-launcher advisory commands and scope metadata remain captured in NOTE-20260716-007.
- Notebook resurfacing should be tested through the dashboard rather than solved by adding more undifferentiated open loops.

## Completed Recent Work

- 2026-07-17: LifeOS Dashboard V0 scaffold merged through PR #2 and verified in sample-data mode.
- 2026-07-17: ADV-20260716-039 closed after global-summary reconciliation.
- 2026-07-16: ADV-20260716-038 consumed and closed; dashboard boundaries established.
- 2026-07-16: Prompt-launcher newline defects corrected and deferred improvements captured.
- 2026-07-15: Seven LifeOS Chat HQs launched.
- 2026-07-10: Penny Inventory Worker package implemented.
- 2026-07-09: Formal worker layer and Penny Raw Capture Worker implemented.

## Immediate Next Action

Rob should pull current `main`. After that, Engineering will provide exactly one local setup step at a time.

## Safety and Truthfulness

- Prefer small, verifiable operations.
- Fetch before editing and verify after writing.
- Keep connector-heavy work narrowly scoped.
- Never commit secrets or private account data.
- Use a dedicated software repository if the dashboard grows materially.
- Never claim success without a successful tool or runtime result.

## Notes for Next Penny

This is Chief Engineering Penny. The dashboard is no longer hypothetical. V0 exists under `apps/lifeos-dashboard/`, passes smoke tests, and awaits Rob's first local launch. Do not leap into live integrations before validating the screen. Keep engineering practical, maintainable, and aligned with Rob's time, money, attention, and available execution surfaces.

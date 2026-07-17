# Chief Engineering Penny Status

Updated: 2026-07-17

## Current Phase

Active / LifeOS Dashboard V0, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture

## Summary

Chief Engineering Penny owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, and build-readiness.

Engineering defines how to build safely and in the right order. Business and Office Leaks define what should be built and why. Finance owns cost-bearing choices. Main Assistant coordinates daily operations. Life Logistics owns shared global memory hygiene.

## Operating Model

Use regular Chat for architecture, planning, research, GitHub synchronization, prompt work, debugging analysis, advisories, and small verified connector updates.

Use Work only for bounded execution that requires local files, terminal access, substantial coding, testing, packaging, browser control, desktop applications, or artifact production.

Never claim an action, test, deployment, or external write occurred without verified evidence.

## Source-of-Truth Boundaries

- GitHub: durable memory, architecture, advisories, stable project state, and the current dashboard scaffold.
- Trello: current LifeOS attention and flow.
- Todoist: Rob-facing tasks and commitments.
- Calendar: timed commitments.
- Gmail: communication evidence.
- Google Drive: working records, Sheets, Docs, and human-facing artifacts.
- Dedicated software repositories: future home for substantial dashboard code if the application outgrows the current scaffold location.

Never store secrets, credentials, tokens, API keys, financial account details, medical details, or private user data in Life OS GitHub memory.

## Current Focus

### LifeOS Dashboard V0

A runnable local dashboard scaffold is merged into `main` at:

- `apps/lifeos-dashboard/`

Pull request:

- PR #2 — `Scaffold local LifeOS dashboard`

Merged commit:

- `bdf920112e8142179d3da91a3e7983e1a5d48c27`

Implemented V0 foundation:

- FastAPI backend;
- browser-based responsive dashboard shell;
- sample-data adapter and replaceable source boundary;
- Today, Trello Flow, attention signals, Drive shortcuts, recent GitHub notebook activity, and copyable Penny-command regions;
- source-health and freshness language;
- Windows setup and launch instructions;
- architecture and security documentation;
- smoke tests for the home page, health endpoint, and dashboard endpoint.

Verification completed before merge:

- Python compilation succeeded;
- `python -m pytest -q` returned 3 passing tests;
- a live Uvicorn server started on `127.0.0.1:8765`;
- `/`, `/api/health`, and `/api/dashboard` returned HTTP 200.

V0 remains sample-data only. No account credentials, live source integrations, write controls, or financial connector data were added.

Immediate dashboard milestone:

1. Rob pulls current `main`.
2. Rob launches the scaffold locally with Engineering guidance.
3. Engineering captures first-use layout and usefulness feedback.
4. GitHub becomes the first live read adapter after the sample screen is accepted.

### Reliable Connector Execution Layer

Connector reliability remains a first-class architecture risk.

Current design concerns:

- operation ledger or write-ahead log;
- connector health states;
- idempotency and duplicate prevention;
- post-write verification;
- bounded retry and stop rules;
- degraded-mode language and recovery paths;
- manual, export, RPR, or alternate-worker fallback.

Observed field lessons favor small operations, explicit connector invocation, narrow connector scope, post-write verification, and fresh-chat recovery when a session degrades.

### Life OS Worker Architecture

Implemented workers:

- Penny Raw Capture Worker: `workers/penny-raw-capture/`
- Penny Inventory Worker: `workers/penny-inventory/`

Both packages need real operational evidence before Engineering proposes additional worker architecture.

### Office Leaks Delivery Architecture

Engineering preserves two integrated delivery layers:

1. Mechanical: map, score, scope, sprint, verify, handoff, follow up.
2. Human-system: respect, rapport, internal champion, users, Aha Moment, adoption verification, relational follow-up.

Current references:

- `projects/engineering/notebook/NOTE-20260708-005-office-leak-delivery-playbooks-v1.md`
- `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`

### Prompt Launcher and Command Interface

The launcher remains a secondary interface over `memory/CONTEXT_REMINDER.md`.

Completed:

- corrected literal newline output from Hub Boot onward.

Deferred notebook capture:

- `projects/engineering/notebook/NOTE-20260716-007-prompt-launcher-advisory-commands-and-scope.md`

That note preserves `/READADVISORY`, `/CONSUMEADVISORY`, and explicit launcher scope metadata for later implementation.

## Advisory State

- No open advisories are listed in `coordination/ADVISORY_INDEX.md` as of 2026-07-17.
- ADV-20260716-038 is acknowledged / ingested / closed.
- ADV-20260716-039 is implemented / acknowledged / closed after Life Logistics reconciled shared global summaries.
- Department Event Inbox remains frozen historical state.

## Current Open Work

- Complete Rob's first local launch of LifeOS Dashboard V0.
- Capture first-use dashboard feedback before adding live integrations.
- Build the GitHub read adapter after V0 layout acceptance.
- Pilot Penny Inventory Worker with 2–3 real sale items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft the operation-ledger schema and connector-health policy.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Observe Chat HQ routing and model-use friction.
- Keep Engineering HQ Daily Sync paused pending stronger scheduling architecture and explicit authorization.

## Completed Recent Work

- 2026-07-17: LifeOS Dashboard V0 scaffold merged through PR #2 and verified locally in sample-data mode.
- 2026-07-17: ADV-20260716-039 closed after shared global-summary reconciliation.
- 2026-07-16: ADV-20260716-038 consumed and closed; dashboard concept ingested with read-mostly boundaries.
- 2026-07-16: Prompt-launcher newline defect corrected and deferred advisory-command improvements captured.
- 2026-07-15: Seven LifeOS department discussion HQ chats opened and declared ready.
- 2026-07-10: Inventory Worker architecture and durable package completed.
- 2026-07-09: Formal worker layer and Raw Capture Worker implemented.

## Boundary

Chief Engineering Penny owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, or cross-project memory curation.

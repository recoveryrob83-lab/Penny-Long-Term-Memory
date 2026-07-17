# Chief Engineering Penny Session Handoff

Updated: 2026-07-17
Project: Chief Engineering Penny / Engineering HQ
Purpose: Project-specific handoff for engineering, software architecture, prompt systems, workers, connector reliability, desktop automation, and the LifeOS Dashboard.

## Metadata

- Project Owner: Rob
- Primary Chat: Chief Engineering Penny / Engineering HQ
- Current Phase: Active / Desktop Department Automation, LifeOS Dashboard Observation, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture
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
- build-readiness and truthful verification;
- routine maintenance of Engineering-owned durable files.

Chief Business HQ and Office Leaks Consulting HQ define what should be built and why. Engineering defines how to build it safely and in the right order.

Route:

- business strategy and monetization to Business or Office Leaks;
- cost-bearing technical choices to Finance;
- daily one-off execution to Main Assistant;
- shared global memory hygiene and cross-project audits to Life Logistics;
- recovery and health sustainability to Wellness.

Engineering maintains its own project subtree during routine work. Shared global files, other departments' canonical files, and cross-department architecture changes require the owning department, Main Assistant, Life Logistics, or an explicit coordinated action.

## Chat and Work Model

Use regular Chat for architecture discussion, planning, research, GitHub synchronization, prompt work, code-review discussion, debugging analysis, advisories, and small authorized connector updates.

Use Work for bounded execution requiring local files, terminal access, substantial coding, test execution, browser or desktop control, application packaging, or complex artifacts.

Never claim an action, test, deployment, or connector write occurred without verified evidence.

## Current Engineering Tracks

### 1. Desktop Department Automation

Current top active track.

Primary scripts:

- `apps/lifeos-dashboard/automation/open_department_chat.py`
- `apps/lifeos-dashboard/automation/draft_department_boot.py`

Latest live-send result:

- the Wellness `--send` test stopped safely before composer work because the target remained on the generic `ChatGPT` loading screen;
- expected title: `Life OS - Wellness HQ`;
- observed title: `ChatGPT`;
- no prompt was written;
- nothing was sent;
- this was a navigation/loading-state failure, not a clipboard-verification failure.

Full handoff:

- `projects/engineering/notebook/NOTE-20260717-010-desktop-department-automation-live-send-handoff.md`

Latest verification patch:

- `4413fd384572452b05bf36ce3ada7dca55046917`

Immediate decision:

- inspect the handoff and decide whether to add one bounded re-navigation retry for the generic loading state;
- preserve refusal-first behavior and do not broaden retries into uncontrolled automation.

### 2. LifeOS Dashboard

Canonical application path:

- `apps/lifeos-dashboard/`

The dashboard is locally running and validated on Rob's Windows machine.

Merged milestones:

- PR #2 / `bdf920112e8142179d3da91a3e7983e1a5d48c27` — runnable FastAPI scaffold and original smoke tests;
- PR #3 / `62b815608bc19f657922c6e088965c1e3eeab8a2` — live local GitHub adapter;
- PR #4 / `262ebf98eb7e9b84eb95c421dcd1647a7c059d47` — live read-only Trello adapter;
- PR #5 / `c7fc7d795abca8ddf56e964b36ea7bd86cc6cd17` — live read-only Todoist and Google Calendar adapters;
- PR #6 / `366b2151e0155cbf2164c12a7384ff701043561f` — Windows `tzdata` runtime dependency;
- PR #7 / `e6059a8ffbb056e308e5e509b89ae2ad2f413edd` — guarded clean fast-forward-only GitHub auto-sync.

Verified live sources:

- GitHub;
- Trello;
- Todoist;
- Google Calendar private iCal.

Verification:

- full suite passed with 16 tests;
- dashboard relaunched successfully;
- GitHub reported healthy, clean, and up to date;
- Trello, Todoist, and Calendar remained healthy and live.

Current dashboard work:

- observe ordinary daily refresh behavior;
- add a small configurable browser-side auto-refresh control;
- preserve independent cache behavior and guarded Git sync;
- defer Gmail and Drive until demonstrated operational need.

The dashboard is a read-mostly visibility layer, not a replacement source of truth or a newly authorized PennyOS roadmap.

### 3. Reliable Connector Execution Layer

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

### 4. Life OS Worker Architecture

Implemented worker packages:

- Penny Raw Capture Worker: `workers/penny-raw-capture/`
- Penny Inventory Worker: `workers/penny-inventory/`

Raw Capture mission: `Capture first. Organize later.`

Inventory mission: `See the item. Record the item. Verify the row.`

Both workers need real operational evidence before more workers are proposed.

### 5. Office Leaks Delivery Architecture

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

### 6. Prompt Launcher and Command Interface

The launcher remains a secondary interface over the canonical vocabulary in `memory/CONTEXT_REMINDER.md`.

Completed repair:

- corrected literal `\n` output from Hub Boot onward.

Deferred improvements:

- `/READADVISORY`;
- `/CONSUMEADVISORY`;
- explicit scope metadata and better department-selector labels.

Notebook reference:

- `projects/engineering/notebook/NOTE-20260716-007-prompt-launcher-advisory-commands-and-scope.md`

### 7. LifeOS Chat HQ Architecture

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
- ADV-20260717-040 is implemented / acknowledged / closed.
- ADV-20260716-039 is implemented / acknowledged / closed.
- ADV-20260716-038 is acknowledged / ingested / closed.
- Department Event Inbox remains frozen historical state.

## Active Open Loops

- Resume desktop department automation from NOTE-20260717-010.
- Decide whether to add one bounded re-navigation retry for the generic ChatGPT loading state.
- Add configurable browser-side dashboard auto-refresh without overlapping refreshes.
- Observe four-source dashboard behavior during ordinary use and real degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real items.
- Observe Penny Raw Capture Worker in real use.
- Draft the Reliable Connector Execution Layer implementation packet and operation-ledger schema.
- Define idempotency, verification, connector-health, retry, and recovery patterns.
- Continue Office Leaks delivery architecture as requirements mature.
- Observe Chat HQ routing friction and model-use waste.
- Keep Engineering HQ Daily Sync paused until explicitly resumed.

## Deferred

- Gmail and Drive dashboard adapters remain deferred until demonstrated need.
- Desktop-window packaging follows sustained browser usefulness.
- Prompt-launcher advisory commands and scope metadata remain captured in NOTE-20260716-007.
- Additional workers wait for real Raw Capture and Inventory evidence.

## Completed Recent Work

- 2026-07-17: Desktop automation safety verification patch recorded as `4413fd384572452b05bf36ce3ada7dca55046917`; latest Wellness send attempt stopped safely on unresolved loading state.
- 2026-07-17: Guarded GitHub auto-sync merged through PR #7 and locally verified with 16 passing tests.
- 2026-07-17: Windows timezone packaging defect closed through PR #6.
- 2026-07-17: Live Todoist and Google Calendar adapters merged and verified.
- 2026-07-17: Live Trello adapter merged and verified.
- 2026-07-17: Live local GitHub dashboard adapter merged and verified.
- 2026-07-17: Dashboard V0 launched and passed first-use review.
- 2026-07-17: ADV-20260717-040 closed after shared-summary reconciliation.
- 2026-07-17: ADV-20260716-039 closed after shared-summary reconciliation.
- 2026-07-16: ADV-20260716-038 consumed and closed; dashboard boundaries established.
- 2026-07-16: Prompt-launcher newline defects corrected and deferred improvements captured.
- 2026-07-15: Seven LifeOS Chat HQs launched.
- 2026-07-10: Penny Inventory Worker package implemented.
- 2026-07-09: Formal worker layer and Penny Raw Capture Worker implemented.

## Immediate Next Action

Read `projects/engineering/notebook/NOTE-20260717-010-desktop-department-automation-live-send-handoff.md`, inspect the current automation scripts, and decide whether one bounded re-navigation retry can safely recover from the generic `ChatGPT` loading state without weakening refusal-first behavior.

## Safety and Truthfulness

- Prefer small, verifiable operations.
- Fetch before editing and verify after writing.
- Keep connector-heavy work narrowly scoped.
- Never commit secrets or private account data.
- Use a dedicated software repository if the dashboard grows materially.
- Never claim success without a successful tool or runtime result.

## Notes for Next Penny

This is Chief Engineering Penny. The dashboard is live and useful. The current front burner is desktop department automation, specifically the loading-state navigation failure captured in NOTE-20260717-010. Preserve safety stops, make retries bounded, and do not let a convenience script grow tentacles.
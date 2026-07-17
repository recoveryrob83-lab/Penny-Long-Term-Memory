# Engineering HQ Status

Updated: 2026-07-17

## Current Phase

Active / Desktop Department Automation Maintenance, LifeOS Dashboard Observation, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture

## Summary

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, and build-readiness.

Engineering defines how to build safely and in the right order. Business and Office Leaks define what should be built and why. Finance owns cost-bearing choices. Main Assistant coordinates daily operations. Logistics owns shared global memory hygiene.

## Operating Model

Use regular Chat for architecture, planning, research, GitHub synchronization, prompt work, debugging analysis, advisories, and small verified connector updates.

Use Work only for bounded execution requiring local files, terminal access, substantial coding, testing, packaging, browser control, desktop applications, or artifact production.

Never claim an action, test, deployment, or external write occurred without verified evidence.

## Source-of-Truth Boundaries

- GitHub: durable memory, architecture, advisories, stable project state, dashboard code, and automation code.
- Trello: current LifeOS attention and flow.
- Todoist: Rob-facing tasks and commitments.
- Calendar: timed commitments.
- Gmail: communication evidence when explicitly queried; dashboard integration deferred until demonstrated need.
- Google Drive: working records and human-facing artifacts; dashboard integration deferred until demonstrated need.
- LifeOS Dashboard: read-mostly visibility into selected authoritative systems.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Current Focus

### Desktop Department Automation

Status: Operational and validated across all seven HQs.

Canonical paths:

- `apps/lifeos-dashboard/automation/draft_department_boot.py`
- `apps/lifeos-dashboard/automation/open_department_chat_group.py`
- `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`
- `memory/HQ_NAMING_STANDARD.md`

Validated behavior:

- exact HQ navigation;
- one bounded hidden-sidebar expansion;
- exact destination verification;
- stable Group composer discovery;
- occupied-composer preservation;
- clipboard round-trip verification;
- draft-only default;
- explicit `--send` requirement;
- stop on uncertainty;
- watched successful live send to Main Assistant HQ.

The prior Wellness loading failure is resolved. Future changes require demonstrated UI drift or failure, followed by draft-only and watched live-send revalidation.

Durable recovery reference:

- `projects/engineering/notebook/NOTE-20260717-011-chatgpt-ui-automation-lessons-and-recovery-playbook.md`

### LifeOS Dashboard

Application location:

- `apps/lifeos-dashboard/`

The dashboard is locally running and validated on Rob's Windows machine.

Verified sources:

- GitHub
- Trello
- Todoist
- Google Calendar private iCal

Current boundaries:

- full suite passed with 16 tests;
- Windows timezone support uses `tzdata`;
- guarded GitHub sync only fast-forwards clean, strictly-behind `main`;
- Gmail and Drive adapters remain deferred;
- dashboard remains a visibility layer rather than a source of truth.

Current dashboard work:

1. Observe ordinary refresh behavior.
2. Add a small browser-side auto-refresh control only if normal use demonstrates value.
3. Preserve independent caches and guarded Git sync.
4. Keep Gmail and Drive deferred until a concrete need appears.

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

### Life OS Worker Architecture

Implemented workers:

- Penny Raw Capture Worker: `workers/penny-raw-capture/`
- Penny Inventory Worker: `workers/penny-inventory/`

Both need real operational evidence before additional worker architecture is proposed.

### Office Leaks Delivery Architecture

Engineering preserves two integrated delivery layers:

1. Mechanical: map, score, scope, sprint, verify, handoff, follow up.
2. Human-system: respect, rapport, internal champion, users, Aha Moment, adoption verification, relational follow-up.

### Prompt Launcher and Command Interface

The launcher remains a secondary interface over `memory/CONTEXT_REMINDER.md`.

Completed:

- literal newline repair;
- Logistics project path corrected to `projects/life-logistics-hq`;
- legacy Logistics wrapper routed through the canonical department launcher;
- generated boot prompts aligned with current HQ naming and optional status-file handling.

Deferred improvements remain captured in:

- `projects/engineering/notebook/NOTE-20260716-007-prompt-launcher-advisory-commands-and-scope.md`

## Advisory State

- No open advisories are listed in `coordination/ADVISORY_INDEX.md` as of 2026-07-17.
- ADV-20260717-040 is implemented / acknowledged / closed.
- ADV-20260716-039 is implemented / acknowledged / closed.
- ADV-20260716-038 is acknowledged / ingested / closed.

## Current Open Work

- Maintain and observe desktop automation in normal on-demand use.
- Observe the four-source dashboard during ordinary refresh and real degraded conditions.
- Add dashboard auto-refresh only if still useful after ordinary use.
- Pilot Penny Inventory Worker with 2–3 real sale items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft the operation-ledger schema and connector-health policy.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Observe Chat HQ routing and model-use friction.
- Keep Engineering HQ Daily Sync paused pending stronger scheduling architecture and explicit authorization.

## Completed Recent Work

- 2026-07-17: Desktop automation validated across all seven HQs with one watched successful live send to Main Assistant HQ.
- 2026-07-17: NOTE-010 closed and NOTE-011 established the durable UI automation recovery playbook.
- 2026-07-17: Logistics boot path and wrapper corrected.
- 2026-07-17: Guarded GitHub auto-sync locally verified with 16 passing tests.
- 2026-07-17: Windows timezone packaging repaired through `tzdata`.
- 2026-07-17: Todoist, Calendar, Trello, and GitHub dashboard paths verified.
- 2026-07-17: Dashboard V0 launched and passed first-use review.
- 2026-07-17: ADV-20260717-040 and ADV-20260716-039 closed after shared-summary reconciliation.
- 2026-07-16: ADV-20260716-038 consumed and closed.
- 2026-07-16: Prompt-launcher newline defect corrected.
- 2026-07-15: Seven LifeOS department chats opened and declared ready.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, or cross-project memory curation.

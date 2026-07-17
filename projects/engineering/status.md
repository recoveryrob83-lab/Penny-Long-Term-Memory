# Chief Engineering Penny Status

Updated: 2026-07-17

## Current Phase

Active / LifeOS Dashboard Live Sources, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture

## Summary

Chief Engineering Penny owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, and build-readiness.

Engineering defines how to build safely and in the right order. Business and Office Leaks define what should be built and why. Finance owns cost-bearing choices. Main Assistant coordinates daily operations. Life Logistics owns shared global memory hygiene.

## Operating Model

Use regular Chat for architecture, planning, research, GitHub synchronization, prompt work, debugging analysis, advisories, and small verified connector updates.

Use Work only for bounded execution that requires local files, terminal access, substantial coding, testing, packaging, browser control, desktop applications, or artifact production.

Never claim an action, test, deployment, or external write occurred without verified evidence.

## Source-of-Truth Boundaries

- GitHub: durable memory, architecture, advisories, stable project state, and dashboard code.
- Trello: current LifeOS attention and flow.
- Todoist: Rob-facing tasks and commitments.
- Calendar: timed commitments.
- Gmail: communication evidence.
- Google Drive: working records, Sheets, Docs, and human-facing artifacts.
- Dedicated software repositories: future home for substantial dashboard code if the application outgrows the current scaffold location.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Current Focus

### LifeOS Dashboard

Application location:

- `apps/lifeos-dashboard/`

Merged implementation milestones:

- PR #2 / `bdf920112e8142179d3da91a3e7983e1a5d48c27` — runnable FastAPI scaffold, responsive interface, sample source, documentation, and original smoke tests.
- PR #3 / `62b815608bc19f657922c6e088965c1e3eeab8a2` — live read-only local GitHub adapter for branch, commit, working tree, advisories, priority open loops, recent notebooks, and durable activity.
- PR #4 / `262ebf98eb7e9b84eb95c421dcd1647a7c059d47` — live read-only Trello Flow adapter for Now, top Next, selected Waiting, source health, local credentials, and a last-good cache.
- PR #5 / `c7fc7d795abca8ddf56e964b36ea7bd86cc6cd17` — live read-only Todoist commitments and Google Calendar private-iCal adapters with independent caches, timezone normalization, recurrence expansion, tests, and setup documentation.

Rob successfully launched the dashboard and confirmed that the title, source health, Today, Current Movement, Next, Waiting, GitHub pulse, and responsive side-by-side layout provide a clear at-a-glance view without visual noise.

Current source state:

- GitHub: live and verified on Rob's machine through the local GitHub Desktop checkout.
- Trello: live and verified with a read-only token; real Now, Next, Waiting, lane parsing, order, and blocker reasons all passed local review.
- Todoist: adapter merged; local token setup and first real-machine verification remain.
- Calendar: adapter merged; local private iCal setup and first real-machine verification remain.
- Gmail: sample attention signals.
- Drive: sample shortcuts.

Todoist adapter behavior:

- reads active tasks through the unified Todoist API;
- keeps overdue tasks visible and includes the configurable near-term horizon;
- normalizes date-only and timed tasks in `LIFEOS_TIMEZONE`;
- sorts by overdue state, due time, priority, and title;
- writes normalized display data only to ignored `.local/todoist_commitments_cache.json`;
- never caches or exposes the bearer token.

Calendar adapter behavior:

- reads one Google Calendar through its private Secret address in iCal format;
- expands recurring rules, exclusions, added dates, overrides, cancellations, all-day events, and overnight events;
- shows the current or next upcoming event in the Today panel;
- writes normalized display data only to ignored `.local/google_calendar_cache.json`;
- never caches or exposes the private iCal URL.

Verification before PR #5 merge:

- 5 new Today-adapter tests passed;
- Python compilation completed for both new adapters;
- source-chain construction passed with the new credentials absent;
- changed Python files stayed within the 100-column project limit;
- tests verified Todoist filtering and ordering, Calendar recurrence expansion, source-specific cache fallback, and secret-safe error language.

Full repository regression testing and live Todoist / Calendar authorization remain for Rob's local checkout.

Immediate dashboard milestone:

1. Rob pulls current `main` through GitHub Desktop.
2. Rob refreshes the editable installation because `python-dateutil` was added.
3. Rob runs the complete local test suite.
4. Engineering guides Todoist personal-token and Google Calendar private-iCal setup in the existing ignored `.env`.
5. Rob relaunches and verifies real Today commitments, next event, source health, and continued scan-path clarity.
6. Gmail and Drive remain deferred until the four current live paths are stable in ordinary use.

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

The Trello, Todoist, and Calendar dashboard caches are concrete examples of explicit healthy, stale, unavailable, and last-good fallback behavior.

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

- Complete local Todoist and Calendar authorization and verification on Rob's machine.
- Confirm the four live dashboard sources remain useful during ordinary refresh and cached degraded operation.
- Pilot Penny Inventory Worker with 2–3 real sale items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft the operation-ledger schema and connector-health policy.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Observe Chat HQ routing and model-use friction.
- Keep Engineering HQ Daily Sync paused pending stronger scheduling architecture and explicit authorization.

## Completed Recent Work

- 2026-07-17: Live Todoist and Google Calendar Today adapters merged through PR #5 with source-specific caches, timezone handling, recurrence expansion, documentation, and 5-test focused verification.
- 2026-07-17: Live Trello Flow adapter locally authorized and verified against Rob's real board.
- 2026-07-17: Live read-only Trello Flow adapter merged through PR #4.
- 2026-07-17: Live local GitHub dashboard adapter merged through PR #3 and verified on Rob's machine.
- 2026-07-17: Dashboard V0 launched; first-use hierarchy, usefulness, and responsive side-by-side layout passed Rob's review.
- 2026-07-17: LifeOS Dashboard V0 scaffold merged through PR #2.
- 2026-07-17: ADV-20260716-039 closed after shared global-summary reconciliation.
- 2026-07-16: ADV-20260716-038 consumed and closed; dashboard concept ingested with read-mostly boundaries.
- 2026-07-16: Prompt-launcher newline defect corrected and deferred advisory-command improvements captured.
- 2026-07-15: Seven LifeOS department discussion HQ chats opened and declared ready.
- 2026-07-10: Inventory Worker architecture and durable package completed.
- 2026-07-09: Formal worker layer and Raw Capture Worker implemented.

## Boundary

Chief Engineering Penny owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, or cross-project memory curation.

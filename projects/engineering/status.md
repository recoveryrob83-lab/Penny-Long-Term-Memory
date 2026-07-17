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

Never store secrets, credentials, tokens, API keys, financial account details, medical details, or private user data in Life OS GitHub memory.

## Current Focus

### LifeOS Dashboard

Application location:

- `apps/lifeos-dashboard/`

Merged implementation milestones:

- PR #2 / `bdf920112e8142179d3da91a3e7983e1a5d48c27` — runnable FastAPI scaffold, responsive interface, sample source, documentation, and original smoke tests.
- PR #3 / `62b815608bc19f657922c6e088965c1e3eeab8a2` — live read-only local GitHub adapter for branch, commit, working tree, advisories, priority open loops, recent notebooks, and durable activity.
- PR #4 / `262ebf98eb7e9b84eb95c421dcd1647a7c059d47` — live read-only Trello Flow adapter for Now, top Next, selected Waiting, source health, local credentials, and a last-good cache.

Rob successfully launched V0 and confirmed that the title, source health, Today, Current Movement, Next, Waiting, GitHub pulse, and responsive side-by-side layout provide a clear at-a-glance view without visual noise.

Current source state:

- GitHub: live and verified on Rob's machine through the local GitHub Desktop checkout.
- Trello: adapter code merged; local read credentials and first real-machine verification remain.
- Todoist: sample.
- Calendar: sample.
- Gmail: sample attention signals.
- Drive: sample shortcuts.

Trello adapter behavior:

- reads board identity, open lists, and open cards through Trello REST;
- preserves card order;
- extracts `Lane:` and `Blocked by:` description metadata;
- displays one Now, up to three Next, and up to three Waiting cards;
- writes normalized display data only to ignored `.local/trello_flow_cache.json`;
- uses the last-good cache and marks Trello stale when a later request fails;
- never writes Trello or stores credentials in the cache or GitHub.

Verification before PR #4 merge:

- 8 tests passed;
- Python compile pass completed;
- changed Python files stayed within the 100-column project limit;
- local Uvicorn server started successfully;
- `/api/health` and `/api/dashboard` returned HTTP 200;
- tests verified live normalization, card ordering, metadata parsing, missing credentials, source composition, cache fallback, and secret-safe error language.

Immediate dashboard milestone:

1. Rob pulls current `main` through GitHub Desktop.
2. Rob refreshes the editable installation because runtime dependencies changed.
3. Engineering guides creation of the ignored local `.env` with a read-only Trello API key, token, and Flow Board ID.
4. Rob relaunches and verifies `local-github+trello mode` plus real Now, Next, and Waiting state.
5. Todoist and Calendar become the next source track after Trello proves stable locally.

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

The Trello dashboard cache is the first implemented dashboard example of explicit healthy, stale, unavailable, and last-good fallback behavior.

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

- Complete local Trello credential setup and verify the real Flow Board on Rob's machine.
- Confirm live Trello refresh and cached degraded mode do not disturb the accepted dashboard scan path.
- Design Todoist and Calendar source adapters after Trello verification.
- Pilot Penny Inventory Worker with 2–3 real sale items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft the operation-ledger schema and connector-health policy.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Observe Chat HQ routing and model-use friction.
- Keep Engineering HQ Daily Sync paused pending stronger scheduling architecture and explicit authorization.

## Completed Recent Work

- 2026-07-17: Live read-only Trello Flow adapter merged through PR #4 with local ignored credentials, last-good caching, documentation, and 8-test verification.
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

# Chief Engineering Penny Status

Updated: 2026-07-17

## Current Phase

Active / LifeOS Dashboard Observation, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture

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
- Gmail: communication evidence when explicitly queried; dashboard integration deferred until client work creates need.
- Google Drive: working records and human-facing artifacts when needed; dashboard integration deferred until client work creates need.
- Dedicated software repositories: future home for educational projects and any substantial software project outside the LifeOS runtime mirror.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Current Focus

### LifeOS Dashboard

Application location:

- `apps/lifeos-dashboard/`

Merged implementation milestones:

- PR #2 / `bdf920112e8142179d3da91a3e7983e1a5d48c27` — runnable FastAPI scaffold, responsive interface, sample source, documentation, and original smoke tests.
- PR #3 / `62b815608bc19f657922c6e088965c1e3eeab8a2` — live local GitHub adapter for branch, commit, working tree, advisories, priority open loops, recent notebooks, and durable activity.
- PR #4 / `262ebf98eb7e9b84eb95c421dcd1647a7c059d47` — live read-only Trello Flow adapter for Now, top Next, selected Waiting, source health, local credentials, and a last-good cache.
- PR #5 / `c7fc7d795abca8ddf56e964b36ea7bd86cc6cd17` — live read-only Todoist commitments and Google Calendar private-iCal adapters with independent caches, timezone normalization, recurrence expansion, tests, and setup documentation.
- PR #6 / `366b2151e0155cbf2164c12a7384ff701043561f` — added `tzdata` as a runtime dependency so Windows Python installations can resolve `America/Chicago` reliably.
- PR #7 / `e6059a8ffbb056e308e5e509b89ae2ad2f413edd` — guarded GitHub auto-sync on dashboard load and refresh, limited to clean fast-forward-only updates of `main`, with refusal-first handling for dirty, ahead, diverged, detached, or uncertain states.

Rob successfully launched and validated the complete four-source dashboard on his Windows machine.

Current verified source state:

- GitHub: `healthy · main · e6059a8 · clean · up to date`; guarded auto-sync is active.
- Trello: live and verified with real Now, Next, Waiting, lane parsing, ordering, and blocker reasons.
- Todoist: live and verified; dashboard reported 2 today, 0 overdue, and 7 upcoming, with real commitment titles and priority badges.
- Calendar: live and verified; dashboard reported 13 upcoming and correctly parsed the next NA meeting title, relative date, time, and location.
- Gmail: intentionally deferred because current mail is mostly Indeed notices, authorizations, and reminders already handled through Main Assistant queries.
- Drive: intentionally deferred because present use does not justify another dashboard integration.

The dashboard now answers current daily questions from four authoritative sources while leaving Gmail and Drive parked until client work creates a concrete signal-management need.

GitHub auto-sync behavior:

- fetches `origin` on dashboard load and **Refresh view**;
- checks configured branch, clean working tree, remote ref, and ahead/behind state;
- performs only `git merge --ff-only origin/main` when the checkout is strictly behind;
- never rebases, resets, discards files, switches branches, creates merge commits, or resolves conflicts;
- exposes `up to date`, `synced`, blocked, or error status in the GitHub source chip;
- ignores generated `*.egg-info/` files to avoid false dirty-checkout states.

Local verification after PR #7:

- full suite passed: 16 tests;
- dashboard relaunched successfully;
- GitHub source chip confirmed healthy, clean, and up to date;
- Trello, Todoist, and Calendar remained healthy and live.

Immediate dashboard milestone:

1. Use the dashboard in ordinary daily operation.
2. Confirm repeated **Refresh view** behavior remains calm and accurate.
3. Observe independent cache fallback only when a real outage occurs; do not sabotage valid credentials for theater.
4. Defer Gmail and Drive until first client work, multiple active leads, recurring client documents, or a real missed-message risk demonstrates need.
5. Keep educational and future standalone projects in separate repositories so LifeOS remains a clean runtime mirror.

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

The Trello, Todoist, and Calendar dashboard caches and guarded GitHub synchronization are concrete examples of explicit healthy, stale, unavailable, blocked, and refusal-first behavior.

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

- Observe the four-source dashboard during ordinary daily refresh and real degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real sale items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft the operation-ledger schema and connector-health policy.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Observe Chat HQ routing and model-use friction.
- Keep Engineering HQ Daily Sync paused pending stronger scheduling architecture and explicit authorization.

## Completed Recent Work

- 2026-07-17: Guarded GitHub auto-sync merged through PR #7 and locally verified with 16 passing tests and a healthy `main · e6059a8 · clean · up to date` source state.
- 2026-07-17: Windows timezone packaging defect closed through PR #6 by adding the `tzdata` runtime dependency.
- 2026-07-17: Todoist and Google Calendar credentials configured locally without exposing secrets; both real data paths passed live verification.
- 2026-07-17: Live Todoist and Google Calendar Today adapters merged through PR #5 with source-specific caches, timezone handling, recurrence expansion, documentation, and focused verification.
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
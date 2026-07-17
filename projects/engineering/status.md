# Engineering HQ Status

Updated: 2026-07-17

## Current Phase

Active / Automation Command Center Operational Validation, Desktop Automation Recovery, Canonical Prompt Catalog, Dashboard Observation, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture

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
- LifeOS Dashboard: read-mostly visibility into selected authoritative systems plus the local Automation Command Center.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Current Focus

### Automation Command Center

Status: Implemented and in live operational validation.

Canonical references:

- `projects/engineering/notebook/NOTE-20260717-012-lifeos-ui-automation-command-center-plan.md`
- `projects/engineering/notebook/NOTE-20260717-013-command-center-scheduling-live-validation-and-next-recovery-edge.md`

Implemented capabilities:

- eight exact destinations;
- canonical, saved, and custom prompt sources;
- protected canonical prompts and editable saved copies;
- saved-prompt default destinations with mismatch warnings and explicit override;
- draft or explicitly confirmed send mode;
- one-job-at-a-time lock;
- global pause;
- structured result and exact failure reason;
- persistent SQLite activity history;
- one-time, daily, and weekly schedules in `America/Chicago`;
- persistent scheduled jobs across dashboard restarts;
- schedule create, edit, pause, resume, and delete.

Live validation completed:

- one-time custom live send to Engineering HQ succeeded and completed with no future run;
- first daily custom live send to LifeOS HQ succeeded and advanced to the next day;
- active mobile use and response generation in another chat did not interfere with the desktop scheduled send.

Current validation still open:

- occupied-composer scheduled refusal in Logistics HQ;
- overdue-run behavior after dashboard restart;
- second real occurrence of a recurring job.

### Desktop Department Automation

Status: Operational, with one newly identified recovery edge case.

Validated behavior:

- exact HQ navigation;
- one bounded hidden-sidebar `Show more` expansion;
- exact destination verification;
- stable Group composer discovery;
- occupied-composer preservation in prior direct testing;
- clipboard round-trip verification;
- draft-only default;
- explicit send requirement;
- stop on uncertainty;
- successful live sends through both manual and scheduled paths.

New edge case:

ChatGPT Classic may collapse the LifeOS project folder after application restart or a narrow-window layout. The current automation has not been coded or validated to reopen a collapsed project folder before exact chat navigation.

Current workaround:

- keep ChatGPT Classic open;
- keep the LifeOS project expanded;
- keep chats available through the normal sidebar / `Show more` path;
- do not treat post-restart unattended execution as production-safe yet.

Next recovery update, when authorized:

- bounded exact-project detection and one-time expansion;
- verification that the project chat region became visible;
- continued exact-chat navigation;
- safe stop on uncertainty;
- draft-first revalidation across restart, narrow-window, `Show more`, and occupied-composer cases.

### Canonical Prompt Catalog

Status: Next product/data milestone.

The command center currently exposes primarily the Boot canonical family. Engineering must populate the protected canonical prompt registry using authoritative command definitions while preserving read-only canonical behavior and editable saved copies.

Candidate families to reconcile before implementation:

- Boot / Quick Boot / Full Boot;
- Sync;
- Nightly;
- Advisory;
- Sync Advisory;
- Read Advisory;
- Consume Advisory.

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

- Windows timezone support uses `tzdata`;
- guarded GitHub sync only fast-forwards clean, strictly-behind `main`;
- Gmail and Drive adapters remain deferred;
- the dashboard remains a visibility and local-control layer rather than a replacement source of truth.

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

## Advisory State

- No open advisories are listed in `coordination/ADVISORY_INDEX.md` as of 2026-07-17.
- ADV-20260717-040 is implemented / acknowledged / closed.
- ADV-20260716-039 is implemented / acknowledged / closed.
- ADV-20260716-038 is acknowledged / ingested / closed.

## Current Open Work

- Complete the scheduled occupied-composer failure test and record evidence.
- Test overdue one-time behavior after dashboard restart.
- Observe a second real recurring execution.
- Design collapsed-LifeOS-project recovery, but do not change code until Rob authorizes it.
- Populate the protected canonical prompt catalog from authoritative LifeOS commands.
- Decide missed-run policy and production preflight requirements after evidence.
- Observe the four-source dashboard during ordinary refresh and real degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real sale items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft the operation-ledger schema and connector-health policy.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Observe Chat HQ routing and model-use friction.

## Completed Recent Work

- 2026-07-17: Automation Command Center manual Run Now path implemented and live-validated.
- 2026-07-17: Saved prompts, default destinations, mismatch safeguards, protected canonical behavior, and full saved-prompt lifecycle validated.
- 2026-07-17: Persistent one-time, daily, and weekly scheduling implemented.
- 2026-07-17: One-time live send to Engineering HQ succeeded and completed correctly.
- 2026-07-17: First daily live send to LifeOS HQ succeeded and advanced to the next run.
- 2026-07-17: Concurrent mobile chat use and response generation did not interfere with scheduled desktop execution.
- 2026-07-17: Collapsed LifeOS project-folder behavior identified as the next desktop recovery edge case; no code change authorized yet.
- 2026-07-17: Desktop automation validated across all seven HQs with exact navigation and safety gates.
- 2026-07-17: Guarded GitHub auto-sync locally verified with 16 passing tests.
- 2026-07-17: Todoist, Calendar, Trello, and GitHub dashboard paths verified.

## Production Boundary

Scheduling is operational but not yet production-ready for fully unattended Windows use. Production readiness still requires evidence or implementation for occupied-composer scheduled refusal, restart/overdue behavior, repeated recurrence, collapsed-project recovery, scheduler health/preflight, missed-run policy, and potentially Windows startup or service packaging.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, or cross-project memory curation.

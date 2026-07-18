# Engineering HQ Status

Updated: 2026-07-18

## Current Phase

Active / Automation Command Center Operational Validation, Desktop Automation Recovery, Canonical Prompt Catalog, Dashboard Observation, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture

## Summary

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, and build-readiness.

Engineering defines how to build safely and in the right order. Business HQ and Office Leaks HQ define what should be built and why. Finance HQ owns cost-bearing choices. Chief of Staff HQ coordinates daily operations. Life OS Maintenance HQ owns shared global memory hygiene, boot integrity, migrations, audits, source boundaries, and cross-project reconciliation.

## Operating Model

Use regular Chat for architecture, planning, research, GitHub synchronization, prompt work, debugging analysis, advisories, and small verified connector updates.

Use Work only for bounded execution requiring local files, terminal access, substantial coding, testing, packaging, browser control, desktop applications, or artifact production.

Never claim an action, test, deployment, or external write occurred without verified evidence.

## Source-of-Truth Boundaries

- GitHub: durable memory, architecture, advisories, stable project state, dashboard code, and automation code.
- Department project files: authoritative department status, loops, notebooks, and implementation records.
- `memory/05_OPEN_LOOPS.md`: genuinely system-owned work and operating watches only.
- Trello: current LifeOS attention and flow.
- Todoist: Rob-facing tasks and commitments.
- Calendar: timed commitments.
- Gmail: communication evidence when explicitly queried; dashboard integration deferred until demonstrated need.
- Google Drive: working records and human-facing artifacts; dashboard integration deferred until demonstrated need.
- LifeOS Dashboard: read-only aggregation of selected authoritative systems plus bounded local Automation Command Center controls.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Current Focus

### Department Ownership Architecture and Dashboard Inspection

Status: Architecture implemented, locally verified, and accepted by the fresh LifeOS HQ read-only verification.

Canonical references:

- `projects/engineering/notebook/NOTE-20260717-014-department-ownership-and-dashboard-inspection.md`
- `apps/lifeos-dashboard/DEPARTMENT_INSPECTION_DATA_CONTRACT.md`
- `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`
- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
- `memory/STARTUP_BOOT.md`

Implemented:

- normalized read-only Department Inspection across seven departments plus System;
- Work, Knowledge, Operations, and Findings categories;
- source paths, raw fragments, authority, confidence, warnings, and filters;
- evidence-based warning reduction from 101 to 15 while preserving the full inventory;
- enriched finding details and contained record workbenches;
- explicit priority-column parsing;
- one-authoritative-record ownership rules;
- system-promotion and demotion thresholds;
- lifecycle and reconciliation rules;
- dashboard visibility contract;
- universal operating kernel plus role-routed boot context;
- conversion of `memory/05_OPEN_LOOPS.md` into a system-only file;
- first inspector-guided cleanup of Chat HQ watch mirrors, Legacy VA folder mirrors, registry placeholders, and Engineering state/priority mixing;
- reconciliation of the system session handoff;
- final local verification at 414 normalized records, zero findings, and zero warnings;
- fresh canonical LifeOS HQ launch with a ready-for-operations verdict after Maintenance completed final shared repairs.

Validation still required:

- confirm ordinary specialist boots continue to avoid unrelated global backlogs;
- inspect only newly demonstrated findings.

### Automation Naming Compatibility / Package B

Status: Fully implemented and runtime-validated.

Validated implementation:

- retained stable internal destination keys `hub`, `main`, `logistics`, `engineering`, `finance`, `business`, `office-leaks`, and `wellness`;
- changed canonical exact chat targets from `Main Assistant HQ` to `Chief of Staff HQ` and from `Logistics HQ` to `Life OS Maintenance HQ`;
- updated canonical boot automation, Command Center backend mappings, scheduler display labels, run-history display labels, Automation UI selectors, and mapping tests;
- added a bounded compatibility translation for retired callers using `Main Assistant HQ`, `Logistics HQ`, or `Life Logistics HQ`;
- preserved persisted schedule destinations, saved-prompt default destinations, and run-history destinations because those records store stable keys rather than chat titles;
- deliberately left historical execution evidence unchanged where the retired title was the exact title used at the time;
- draft-only canonical automation passed for Chief of Staff HQ and Life OS Maintenance HQ;
- schedules and run history displayed canonical names without database migration;
- a retired-title invocation translated to Chief of Staff HQ and preserved exact-destination safety without sending.

### Department Inspection Canonical Labels / Package C

Status: Fully implemented and locally validated.

Validated implementation:

- preserved stable Department Inspection scope IDs `main-assistant` and `logistics`;
- changed their runtime presentation labels to Chief of Staff HQ and Life OS Maintenance HQ;
- changed finding-detail labels to the same canonical names;
- aligned the approved Department Inspection data contract with the canonical labels and current coordination-role language;
- added a focused regression test proving stable scope IDs return canonical labels;
- preserved source project paths, historical record text, and the Package B retired-title automation bridge;
- local dashboard displayed Chief of Staff HQ and Life OS Maintenance HQ correctly;
- the Department Inspection test set completed with 9 passing tests.

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
- structured result codes and exact failure reasons;
- persistent SQLite activity history;
- one-time, daily, and weekly schedules in `America/Chicago`;
- persistent scheduled jobs across dashboard restarts;
- schedule create, edit, pause, resume, and delete;
- separate Scheduled Jobs and Run History views with cadence, department, state, result, mode, and ordering filters.

Live validation completed:

- one-time custom live send to Engineering HQ succeeded and completed with no future run;
- first daily custom live send to LifeOS HQ succeeded and advanced to the next day;
- active mobile use and response generation in another chat did not interfere with the desktop scheduled send;
- scheduled occupied-composer refusal in Logistics HQ preserved the existing draft, sent nothing, recorded `failed`, and displayed the explicit recovery reason;
- Package B canonical-title and retired-title compatibility paths passed;
- a one-time draft schedule persisted while the dashboard was stopped, became overdue, fired exactly once about 15–20 seconds after restart, recorded the downstream failure, disabled itself, and did not retry automatically.

The `Logistics HQ` name in the occupied-composer bullet is retained as historical test evidence because it was the exact automation destination label used during that validation.

Current validation still open:

- second real occurrence of a recurring job;
- production decision on whether failed one-time jobs need an explicit retry control beyond their visible failed state.

### Desktop Department Automation

Status: Operational for attended use, with canonical title compatibility implemented and post-restart recovery not yet reliable.

Validated behavior:

- exact HQ navigation;
- one bounded hidden-sidebar `Show more` expansion;
- exact destination verification;
- stable Group composer discovery;
- occupied-composer preservation in direct and scheduled testing;
- clipboard round-trip verification;
- draft-only default;
- explicit send requirement;
- stop on uncertainty;
- successful live sends through both manual and scheduled paths;
- structured safe-failure reporting through the dashboard.

Known edge cases:

- ChatGPT Classic may collapse the LifeOS project folder after application restart or a narrow-window layout;
- after dashboard restart, an overdue job reported `ChatGPT Classic` unavailable even though the app was open, while Rob observed a stray `i` appear before validation;
- the current automation has not been coded or validated to reopen a collapsed project folder or robustly reacquire the exact ChatGPT Classic window after restart.

Current workaround:

- keep ChatGPT Classic open;
- keep the LifeOS project expanded;
- keep chats available through the normal sidebar / `Show more` path;
- treat scheduled post-restart execution as diagnostic only, not production-safe;
- inspect failed one-time jobs and retry manually only after clearing any stray composer text.

Next recovery update, when authorized:

- reproduce one immediate draft-only run with the dashboard already running;
- inspect the actual accessible top-level ChatGPT window title before changing selectors;
- add bounded exact-window reacquisition only when the observed failure supports it;
- add bounded exact-project detection and one-time expansion;
- verify that the project chat region became visible;
- preserve exact-chat navigation and safe stop on uncertainty;
- revalidate across restart, narrow-window, `Show more`, occupied-composer, and stray-text cases.

### Canonical Prompt Catalog

Status: Active product/data milestone.

The Command Center currently exposes primarily the Boot canonical family. Engineering must populate the protected canonical prompt registry using authoritative command definitions while preserving read-only canonical behavior and editable saved copies.

Candidate families:

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

Current tabs:

- Overview;
- Department Inspection;
- Automation.

Current boundaries:

- Windows timezone support uses `tzdata`;
- guarded GitHub sync only fast-forwards clean, strictly-behind `main`;
- Gmail and Drive adapters remain deferred;
- the dashboard remains a visibility and local-control layer rather than a replacement source of truth;
- Department Inspection remains read-only and does not rewrite classifications or ownership automatically.

Current product lesson:

The dashboard is exposing duplicate state, stale global assumptions, over-engineering, and work routed beyond its owning department. Treat this diagnostic value as a core capability.

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

- No open advisories are listed in `coordination/ADVISORY_INDEX.md` as of 2026-07-18.
- ADV-20260717-040 is implemented / acknowledged / closed.
- ADV-20260716-039 is implemented / acknowledged / closed.
- ADV-20260716-038 is acknowledged / ingested / closed.

## Current Open Work

- Observe ordinary role-routed specialist boots and correct only demonstrated routing defects.
- Isolate the post-restart ChatGPT Classic reacquisition failure with one immediate draft-only manual run before changing automation selectors.
- Observe a second real recurring execution.
- Decide whether failed one-time schedules need an explicit retry control.
- Populate the protected canonical prompt catalog from authoritative LifeOS commands.
- Decide remaining production preflight requirements after evidence.
- Observe the four-source dashboard during ordinary refresh and real degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real sale items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft the operation-ledger schema and connector-health policy.
- Continue Office Leaks delivery architecture as concrete requirements mature.

## Completed Recent Work

- 2026-07-18: Overdue one-time scheduler catch-up validated; the persisted job fired once about 15–20 seconds after dashboard restart, recorded its downstream failure, disabled, and did not retry automatically.
- 2026-07-18: Package C Department Inspection canonical labels passed local dashboard validation and 9 focused tests.
- 2026-07-18: Package C Department Inspection canonical labels implemented in runtime policy, finding-detail UI, contract, and regression coverage while preserving stable IDs and paths.
- 2026-07-18: Package B canonical and retired-title automation paths fully runtime-validated; schedules and history retained canonical labels without migration.
- 2026-07-18: Package B canonical automation mappings implemented while preserving stable destination keys and persisted Command Center records; legacy chat-title compatibility added for retired callers.
- 2026-07-18: Fresh LifeOS HQ launched and reported ready for operations after final Maintenance verification and repairs.
- 2026-07-18: Department Inspection reached 414 normalized records, zero findings, and zero warnings after source cleanup, warning audit, evidence-backed parser correction, and explicit lifecycle-priority normalization.
- 2026-07-18: Open Loop Ownership and Visibility SOP implemented.
- 2026-07-18: Startup boot changed from universal backlog loading to a universal kernel plus role-routed context.
- 2026-07-18: System open loops and system handoff reconciled to stop mirroring department backlogs.
- 2026-07-18: First Department Inspection source cleanup completed.
- 2026-07-18: Department Inspection MVP locally validated and warning noise reduced from 101 to 15 before the final cleanup and warning audit.
- 2026-07-17: Scheduled occupied-composer refusal and structured dashboard reporting passed end to end.
- 2026-07-17: Scheduled Jobs and Run History were separated and given independent filters.
- 2026-07-17: Automation Command Center manual Run Now path implemented and live-validated.
- 2026-07-17: Saved prompts, default destinations, mismatch safeguards, protected canonical behavior, and full saved-prompt lifecycle validated.
- 2026-07-17: Persistent one-time, daily, and weekly scheduling implemented.
- 2026-07-17: One-time live send to Engineering HQ succeeded and completed correctly.
- 2026-07-17: First daily live send to LifeOS HQ succeeded and advanced to the next run.
- 2026-07-17: Concurrent mobile chat use and response generation did not interfere with scheduled desktop execution.
- 2026-07-17: Desktop automation validated across all seven HQs with exact navigation and safety gates.
- 2026-07-17: Guarded GitHub auto-sync locally verified with 16 passing tests.
- 2026-07-17: Todoist, Calendar, Trello, and GitHub dashboard paths verified.

## Production Boundary

Scheduling persistence and overdue catch-up are operational, but fully unattended Windows use is not production-ready. Production readiness still requires reliable post-restart ChatGPT window and project recovery, repeated recurrence evidence, scheduler health/preflight, a deliberate failed-one-time retry policy, and potentially Windows startup or service packaging.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, or routine cross-project memory curation.

# Engineering HQ Status

Updated: 2026-07-18

## Current Phase

Active / Package D Canonical Prompt Catalog Live Validation, Automation Logs Validation, Desktop Automation Verification, Dashboard Observation, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture

## Summary

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, and build-readiness.

Engineering defines how to build safely and in the right order. Business HQ and Office Leaks HQ define what should be built and why. Finance HQ owns cost-bearing choices. Chief of Staff HQ coordinates daily operations. Life OS Maintenance HQ owns shared global memory hygiene, boot integrity, migrations, audits, source boundaries, and cross-project reconciliation.

## Source-of-Truth Boundaries

- GitHub: durable architecture, project state, dashboard code, automation code, and Engineering records.
- `projects/engineering/open_loops.md`: authoritative unfinished Engineering work and detailed completion ledger.
- SQLite Command Center execution history: authoritative local automation-run record.
- Automation Logs and Run History: dashboard views over that same execution history, not competing log stores.
- `memory/05_OPEN_LOOPS.md`: genuinely system-owned work and operating watches only.
- Trello, Todoist, Calendar, Gmail, and Drive retain their established source roles.
- LifeOS Dashboard remains a visibility and bounded local-control layer rather than a replacement source of truth.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Current Focus

### Package D: Canonical Prompt Catalog and Live Write Verification

Status: Active. Catalog implementation, selector alignment, and diagnostic logging are committed. The selector-focused suite passed with 8 tests. The new logging and guidance changes still require Rob's local focused/full test pass and live dashboard validation.

Implemented:

- protected catalog definitions for Boot, Quick Boot, Fresh / Full Boot, Sync, Nightly, Advisory, Sync Advisory, Read Advisory, and Consume Advisory;
- read-only canonical entries with editable saved copies;
- destination-aware rendering and canonical schedule snapshots;
- foreground-safety guard;
- timeout-stage diagnostics and server-offline UI guard;
- strict failure-message precision and dual-witness write verification;
- production and probe use the same full-containment composer Group selector;
- dedicated Automation Logs tab backed by the existing SQLite execution-history table;
- stable run IDs and manual-versus-scheduled context;
- safe prompt length and fingerprint metadata without duplicating prompt bodies;
- backend event paths, complete captured child stdout/stderr, durations, result codes, and unexpected-exception tracebacks;
- copyable complete run diagnostics and filters by result, department, trigger, order, and search;
- stage-specific timeout messages that distinguish app readiness, composer readiness, and post-paste verification.

Current healthy-state evidence:

- the exact destination opens;
- the composer receives focus;
- the complete 341-character canonical prompt visibly pastes;
- nothing is sent;
- verification visibly selects and clears the full draft repeatedly;
- the read-only probe, using the aligned production selector, copies all 341 characters after the run;
- the automated verifier still reports failure, so Package D is not closed.

Degraded-state evidence:

- ChatGPT Classic occasionally remains on the spinning loading state after a fresh boot;
- switching to another chat and returning can force the app to finish rendering;
- those runs are app-readiness failures and do not count as Package D write-verification evidence.

Required next validation:

1. Pull the latest repository state and restart the dashboard.
2. Run the focused guidance, timeout-diagnostic, Automation Logs, and write-verification tests.
3. Run the full dashboard test suite.
4. In one healthy and responsive ChatGPT Classic state, run one manual canonical draft.
5. Inspect and copy the complete Automation Logs record for that run.
6. After a successful manual result, run one fresh scheduled canonical draft.
7. Close Package D only after both live paths validate.

Do not:

- treat spinning-loading runs as write-verification evidence;
- add broader timeouts, alternate paste mechanisms, Alt+Tab, coordinate hacks, weaker verification, or a third witness without direct evidence;
- start Package E;
- implement the proposed persistent Pause All Automation header control before Package D closes.

### Completed Foundation

The following foundation is complete and should not be reopened without new evidence:

- department ownership architecture and read-only Department Inspection;
- fresh LifeOS HQ verification of the role-routed operating model;
- Package B canonical automation names and retired-title compatibility while preserving stable destination keys;
- Package C Department Inspection canonical labels while preserving stable scope IDs and paths;
- collapsed LifeOS project recovery;
- scheduler persistence, recurrence, overdue visibility, pause-on-failure behavior, restart policy, ledger synchronization, and cleanup controls;
- exact destination navigation, occupied-composer preservation, clipboard lifetime and restoration, explicit send authorization, one-job locking, and stop on uncertainty.

### Automation Command Center

Status: Implemented. Established scheduling and recovery policy is runtime-validated. Package D live write verification and the new detailed-log surface remain open for local validation.

Capabilities:

- eight exact destinations;
- canonical, saved, and custom prompt sources;
- protected canonical prompts and editable saved copies;
- saved-prompt destination mismatch safeguards;
- draft or explicitly confirmed send mode;
- one-job-at-a-time lock and global pause;
- persistent SQLite execution history;
- one-time, daily, weekly, and bounded five-minute debug schedules in `America/Chicago`;
- schedule create, edit, pause, resume, run, cleanup, and delete controls;
- separate Scheduled Jobs, Run History, and Automation Logs views;
- secret-protected no-billing Scheduler Ledger synchronization through the bound Apps Script endpoint.

Automation Logs uses the same durable execution-history rows as Run History. It records complete captured child process streams and safe backend metadata. It does not create a second log database, record environment variables, or copy prompt bodies into diagnostic metadata. The dashboard payload remains bounded to the configured recent-history window so log visibility does not overload normal polling.

### Desktop Department Automation

Status: Operational for attended use and validated recovery under the established safety contract. Package D has exposed a remaining false-negative verification defect after visible canonical paste success.

Safety contract:

- exact destination matching only;
- bounded exact-project and `Show more` recovery;
- exact active-document verification;
- stable Group composer discovery and reacquisition;
- preserve occupied composers and the prior clipboard value;
- explicit send authorization;
- one job at a time;
- stop on uncertainty;
- never blind-retry after an uncertain state.

### LifeOS Dashboard

Application location: `apps/lifeos-dashboard/`

Verified live sources:

- GitHub;
- Trello;
- Todoist;
- Google Calendar private iCal.

Current tabs:

- Overview;
- Department Inspection;
- Automation;
- Automation Logs.

Current boundaries:

- Windows timezone support uses `tzdata`;
- guarded GitHub sync only fast-forwards clean, strictly-behind `main`;
- Gmail and general Drive adapters remain deferred;
- Department Inspection remains read-only;
- Automation Logs is post-run evidence, not a live streaming console;
- fully unattended Windows operation is not assumed merely because scheduling works.

## Other Active Tracks

- Observe ordinary role-routed specialist boots and inspect only demonstrated defects.
- Observe four-source dashboard behavior during ordinary use and genuine degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft the operation-ledger schema and connector-health policy.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Recent Milestones

- 2026-07-18: Dedicated Automation Logs tab and authoritative execution telemetry implemented, including stable run IDs, safe context, backend events, complete captured stdout/stderr, copyable records, useful timeout guidance, and exception trace capture; local validation remains pending.
- 2026-07-18: Production and read-only probe composer selectors aligned; focused selector and write-verification suite passed with 8 tests.
- 2026-07-18: Healthy automation repeatedly pasted and selected the full 341-character canonical draft; the aligned read-only probe copied all 341 characters after the run, isolating the remaining failure to in-run verification behavior.
- 2026-07-18: Scheduler production policy, failed-run pause, Resume rearm, stale one-time restart behavior, ledger health, recurrence, cleanup, and collapsed-project recovery passed runtime validation.
- 2026-07-18: Package C canonical Department Inspection labels passed local dashboard validation and focused tests.
- 2026-07-18: Package B canonical automation mappings and retired-title compatibility passed runtime validation while preserving stable keys and persisted records.
- 2026-07-18: Department Inspection reached 414 normalized records, zero findings, and zero warnings.

Detailed state, priorities, and completion evidence remain authoritative in `projects/engineering/open_loops.md` and referenced Engineering notebook records.

## Production Boundary

- ChatGPT Classic must be available and responsive for UI automation.
- Failed scheduled runs pause according to the validated policy rather than retrying blindly.
- Engineering HQ Daily Sync remains paused by deliberate operating choice until Rob explicitly resumes it.
- Package D must close before Package E or additional automation surface expansion begins.
- Windows startup, desktop shell, service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, or routine cross-project memory curation.

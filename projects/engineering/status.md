# Engineering HQ Status

Updated: 2026-07-18

## Current Phase

Active / Package D Canonical Prompt Catalog Live Validation, Desktop Automation Verification, Dashboard Observation, Connector Reliability, Worker Pilots, Prompt Systems, and Office Leaks Delivery Architecture

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
- `projects/engineering/open_loops.md`: authoritative unfinished Engineering work and detailed completion ledger.
- `memory/05_OPEN_LOOPS.md`: genuinely system-owned work and operating watches only.
- Trello: current LifeOS attention and flow.
- Todoist: Rob-facing tasks and commitments.
- Calendar: timed commitments.
- Gmail: communication evidence when explicitly queried; dashboard integration deferred until demonstrated need.
- Google Drive: working records and human-facing artifacts; general dashboard integration deferred until demonstrated need.
- LifeOS Dashboard: read-only aggregation of selected authoritative systems plus bounded local Automation Command Center controls.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Current Focus

### Package D: Canonical Prompt Catalog and Live Write Verification

Status: Active. Implementation and automated testing pass; healthy live post-paste verification remains unresolved.

Implemented:

- protected catalog definitions for Boot, Quick Boot, Fresh / Full Boot, Sync, Nightly, Advisory, Sync Advisory, Read Advisory, and Consume Advisory;
- read-only canonical entries with editable saved copies;
- destination-aware rendering and canonical schedule snapshots;
- foreground-safety guard;
- timeout-stage diagnostics;
- server-offline UI guard;
- strict failure-message precision;
- strict dual-witness write verification;
- Package D UI behavior suite passing;
- focused 15-test foreground, failure-precision, timeout-diagnostic, server-availability, and dual-witness suite passing.

Healthy ChatGPT Classic evidence:

- exact destination opens;
- composer receives focus;
- complete canonical prompt visibly pastes;
- nothing is sent;
- clipboard and accessible-text verification falsely reject the visible draft.

Degraded ChatGPT Classic evidence:

- destination remains on the spinning loading state;
- composer never becomes usable;
- these runs are app-readiness failures, not valid write-verification evidence.

Required next evidence:

1. Wait until ChatGPT Classic is visibly healthy and responsive.
2. Run one draft-only canonical prompt and confirm the full draft visibly pastes.
3. Leave the draft untouched in the composer.
4. Run:

   `py .\automation\probe_composer_group_clipboard.py "LifeOS HQ"`

5. Inspect the complete terminal output before proposing another behavior patch.
6. After repair, pass one healthy manual canonical draft and one fresh scheduled canonical draft before closing Package D.

Do not:

- rerun repeatedly while ChatGPT Classic is lagging or stuck loading;
- add broader timeouts;
- add alternate paste mechanisms;
- add Alt+Tab or coordinate-focus hacks;
- weaken verification;
- add a third witness without direct evidence;
- start Package E;
- implement the proposed persistent Pause All Automation header control before Package D closes.

### Department Ownership Architecture and Dashboard Inspection

Status: Implemented, locally verified, and accepted by the fresh LifeOS HQ read-only verification.

Validated state:

- seven departments plus System normalized read-only;
- Work, Knowledge, Operations, and Findings categories;
- source paths, raw fragments, authority, confidence, warnings, and filters;
- final local verification at 414 normalized records, zero findings, and zero warnings;
- one-authoritative-record ownership rules;
- system-promotion and demotion thresholds;
- lifecycle and reconciliation rules;
- dashboard visibility contract;
- universal operating kernel plus role-routed boot context;
- `memory/05_OPEN_LOOPS.md` reserved for genuinely system-owned work;
- fresh canonical LifeOS HQ launch returned a ready-for-operations verdict.

Remaining boundary:

- observe ordinary specialist boots;
- inspect and correct only newly demonstrated routing defects;
- do not weaken finding detection merely to preserve a clean count.

### Automation Naming Compatibility / Package B

Status: Fully implemented and runtime-validated.

Validated state:

- stable internal destination keys preserved;
- canonical exact chat targets use Chief of Staff HQ and Life OS Maintenance HQ;
- retired callers receive bounded compatibility translation;
- schedules, saved-prompt defaults, and run history required no database migration;
- historical evidence retains the exact label used when the historical test occurred.

### Department Inspection Canonical Labels / Package C

Status: Fully implemented and locally validated.

Validated state:

- stable Department Inspection scope IDs preserved;
- runtime and finding-detail presentation use canonical HQ names;
- approved data contract aligned with current labels and coordination roles;
- focused regression coverage passed with 9 tests.

### Automation Command Center

Status: Implemented. Established scheduling and recovery policy is runtime-validated. Package D live write verification remains open.

Capabilities:

- eight exact destinations;
- canonical, saved, and custom prompt sources;
- protected canonical prompts and editable saved copies;
- saved-prompt destination mismatch safeguards;
- draft or explicitly confirmed send mode;
- one-job-at-a-time lock;
- global pause;
- structured result codes and exact failure reasons;
- persistent SQLite activity history;
- one-time, daily, weekly, and bounded five-minute debug schedules in `America/Chicago`;
- persistent scheduled jobs across dashboard restarts;
- schedule create, edit, pause, resume, run, cleanup, and delete controls;
- separate Scheduled Jobs and Run History views;
- secret-protected no-billing Scheduler Ledger synchronization through the bound Apps Script endpoint.

Validated policy and recovery:

- exact destination and occupied-composer safety paths;
- successful manual and scheduled live sends;
- bounded recurrence completed exactly twice with no third run;
- failed scheduled runs pause after one attempt with no blind retry;
- recurring Resume recalculates the next valid occurrence rather than running immediately;
- stale one-time jobs pause after restart under the validated missed-run policy;
- expired one-time Resume refuses until the definition is moved into the future;
- overdue visibility and ordering are correct;
- completed schedule cleanup preserves run history;
- cloud ledger startup compaction removes blank gaps even with zero local definitions;
- collapsed LifeOS project recovery expands the exact project safely and reacquires the destination composer.

### Desktop Department Automation

Status: Operational for attended use and validated recovery under the established safety contract. Package D has exposed a remaining false-negative verification defect after visible canonical paste success.

Validated behavior:

- exact HQ navigation;
- bounded exact-project and `Show more` recovery;
- exact destination verification;
- stable Group composer discovery and reacquisition;
- occupied-composer preservation;
- clipboard lifetime through verification and restoration afterward;
- precise structured failure classification;
- draft-only default;
- explicit send requirement;
- one-job lock;
- stop on uncertainty;
- successful live sends through manual and scheduled paths.

Safety contract:

- no fuzzy destination matching;
- no overwrite of occupied composers without explicit replacement authority;
- no submission without destination, readiness, content, and send gates;
- no blind retry after uncertain state;
- no broader recovery or selector changes without demonstrated evidence.

### LifeOS Dashboard

Application location:

- `apps/lifeos-dashboard/`

Verified sources:

- GitHub;
- Trello;
- Todoist;
- Google Calendar private iCal.

Current tabs:

- Overview;
- Department Inspection;
- Automation.

Current boundaries:

- Windows timezone support uses `tzdata`;
- guarded GitHub sync only fast-forwards clean, strictly-behind `main`;
- Gmail and general Drive adapters remain deferred;
- the dashboard remains a visibility and bounded local-control layer rather than a replacement source of truth;
- Department Inspection remains read-only and does not rewrite classifications or ownership automatically.

### Reliable Connector Execution Layer

Status: Open architecture track.

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

- Penny Raw Capture Worker: `workers/penny-raw-capture/`;
- Penny Inventory Worker: `workers/penny-inventory/`.

Both need real operational evidence before additional worker architecture is proposed.

### Office Leaks Delivery Architecture

Engineering preserves two integrated delivery layers:

1. Mechanical: map, score, scope, sprint, verify, handoff, follow up.
2. Human-system: respect, rapport, internal champion, users, Aha Moment, adoption verification, relational follow-up.

## Advisory State

As of 2026-07-18:

- No open advisories are listed in `coordination/ADVISORY_INDEX.md`.
- ADV-20260717-040 is implemented / acknowledged / closed.
- ADV-20260716-039 is implemented / acknowledged / closed.
- ADV-20260716-038 is acknowledged / ingested / closed.

## Current Open Work

- Close Package D through evidence-led composer probing and healthy manual plus fresh scheduled canonical-draft validation.
- Observe ordinary role-routed specialist boots and correct only demonstrated routing defects.
- Maintain desktop automation safety and revalidate only after material UI changes or observed failures.
- Observe four-source dashboard behavior during ordinary refresh and genuine degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real sale items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft the operation-ledger schema and connector-health policy.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

Detailed state, next actions, priorities, and completion evidence remain authoritative in `projects/engineering/open_loops.md`.

## Recent Milestones

- 2026-07-18: Package D canonical catalog, foreground guard, timeout diagnostics, server-offline guard, strict failure precision, and dual-witness verification reached passing automated coverage; healthy live paste succeeds visibly but post-paste verification still falsely fails.
- 2026-07-18: Scheduler production policy, failed-run pause, Resume rearm, stale one-time restart behavior, ledger health, recurrence, cleanup, and collapsed-project recovery passed runtime validation.
- 2026-07-18: Package C canonical Department Inspection labels passed local dashboard validation and focused tests.
- 2026-07-18: Package B canonical automation mappings and retired-title compatibility passed runtime validation while preserving stable keys and persisted records.
- 2026-07-18: Fresh LifeOS HQ launched and reported ready for operations after final Maintenance verification and repairs.
- 2026-07-18: Department Inspection reached 414 normalized records, zero findings, and zero warnings.
- 2026-07-17: Automation Command Center manual operation, saved prompts, persistent scheduling, exact destination automation, and four-source dashboard operation were established.

Detailed historical evidence remains in `projects/engineering/open_loops.md` and Engineering notebook records rather than being duplicated here.

## Production Boundary

The established scheduler policy and recovery behavior are live-validated. Fully unattended Windows use is not assumed merely because scheduling works.

Current boundary:

- ChatGPT Classic must be available and responsive for UI automation;
- failed scheduled runs pause according to the validated policy rather than retrying blindly;
- Engineering HQ Daily Sync remains paused by deliberate operating choice until Rob explicitly resumes it;
- Package D must close before Package E or additional automation surface expansion begins;
- Windows startup, desktop shell, service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, or routine cross-project memory curation.

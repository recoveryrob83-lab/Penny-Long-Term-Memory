# Engineering HQ Session Handoff

Updated: 2026-07-18
Project: Engineering HQ
Purpose: Project-specific handoff for software architecture, prompt systems, workers, connector reliability, desktop automation, the LifeOS Dashboard, and the Automation Command Center.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Package D Canonical Prompt Catalog Live Validation, Desktop Automation Verification, Dashboard Observation, Connector Reliability, Worker Pilots, and Delivery Architecture
- Primary Systems: GitHub, Google Drive, Trello, Todoist, Calendar, Gmail as needed, RPR/user-mediated files, Engineering advisory board, Advisory Index
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, financial account details, medical details, private user data, or sensitive implementation details in Life OS memory files.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read current Engineering notebook records only when referenced by the handoff, status, open loops, or active work.
7. Read `coordination/ADVISORY_INDEX.md` only when advisory routing or cross-department status is relevant.
8. Do not load the global handoff, all active projects, or system loops during an ordinary Engineering boot unless the current task is explicitly system-level.
9. Keep connector work small, explicit, and verifiable.

## Department Role

Engineering HQ owns technical architecture, software planning, repository strategy, API and connector research, automation design, prompt systems, testing, debugging, worker contracts, implementation sequencing, build-readiness, and truthful verification.

Business HQ and Office Leaks HQ define what should be built and why. Engineering defines how to build it safely and in the right order.

Route business strategy to Business HQ or Office Leaks HQ, cost-bearing choices to Finance HQ, daily one-off execution to Chief of Staff HQ, shared global memory hygiene to Life OS Maintenance HQ, and non-clinical wellbeing or sustainability judgment to Wellness HQ.

## Chat and Work Model

Use regular Chat for architecture discussion, planning, research, GitHub synchronization, prompt work, debugging analysis, advisories, and small authorized connector updates.

Use Work for bounded execution requiring local files, terminal access, substantial coding, test execution, browser or desktop control, application packaging, or complex artifacts.

Never claim an action, test, deployment, or connector write occurred without verified evidence.

## Highest-Priority Work Package

### Package D: Canonical Prompt Catalog and Live Write Verification

Status: Active. Catalog implementation and automated tests pass; healthy live post-paste verification remains unresolved.

Canonical references:

- `projects/engineering/open_loops.md`
- `apps/lifeos-dashboard/lifeos_dashboard/canonical_prompt_catalog.py`
- `apps/lifeos-dashboard/automation/probe_composer_group_clipboard.py`
- `projects/engineering/notebook/NOTE-20260717-011-chatgpt-ui-automation-lessons-and-recovery-playbook.md`
- `projects/engineering/notebook/NOTE-20260717-013-command-center-scheduling-live-validation-and-next-recovery-edge.md`

Implemented and tested:

- protected canonical prompt definitions for Boot, Quick Boot, Fresh / Full Boot, Sync, Nightly, Advisory, Sync Advisory, Read Advisory, and Consume Advisory;
- read-only canonical entries with editable saved copies;
- destination-aware rendering and schedule snapshots;
- foreground-safety guard;
- timeout-stage diagnostics;
- server-offline UI guard;
- strict failure-message precision;
- strict dual-witness write verification;
- full Package D UI behavior test suite passing;
- focused 15-test foreground, failure-precision, timeout-diagnostic, server-availability, and dual-witness suite passing.

Exact live-validation state:

1. Healthy ChatGPT Classic state:
   - the exact destination opens;
   - the composer receives focus;
   - the full canonical prompt visibly pastes;
   - nothing is sent;
   - post-paste verification falsely fails through both clipboard and accessible-text witnesses.
2. Degraded ChatGPT Classic state:
   - the destination remains on the spinning loading state;
   - the composer never becomes usable;
   - this is app-readiness failure evidence, not valid write-verification evidence.

Current diagnostic boundary:

- do not rerun automation while ChatGPT Classic is visibly lagging or stuck loading;
- do not add broader timeouts, alternate paste mechanisms, Alt+Tab behavior, coordinate hacks, weaker verification, or a third witness without direct evidence;
- do not start Package E until Package D closes;
- keep the proposed persistent Pause All Automation header control deferred until Package D passes one healthy manual canonical draft and one fresh scheduled canonical draft.

Next valid diagnostic action:

1. obtain one healthy live run where the full canonical draft visibly pastes;
2. leave the draft untouched in the composer;
3. run:

   `py .\automation\probe_composer_group_clipboard.py "LifeOS HQ"`

4. inspect the complete terminal output before proposing another verification patch;
5. after a successful repair, validate one manual canonical draft and one fresh scheduled canonical draft before closing Package D.

## Completed Foundation

The following foundation is complete and should not be reopened without new evidence:

- department ownership architecture and read-only Department Inspection;
- fresh LifeOS HQ verification of the role-routed operating model;
- Package B canonical automation names and retired-title compatibility while preserving stable destination keys;
- Package C Department Inspection canonical labels while preserving stable scope IDs and filesystem paths;
- collapsed LifeOS project recovery;
- scheduler persistence, recurrence, overdue visibility, pause-on-failure behavior, restart policy, ledger synchronization, and cleanup controls;
- exact destination navigation, occupied-composer preservation, clipboard lifetime and restoration, explicit send authorization, one-job locking, and stop on uncertainty.

Detailed completion evidence remains in `projects/engineering/open_loops.md` and the referenced Engineering notebook records.

## Automation Command Center

Status: Implemented and operationally validated for its established scheduling and recovery policy. Package D live write-verification validation remains open.

Current implementation includes:

- eight exact destinations: LifeOS HQ plus seven department HQs;
- canonical, saved, and custom prompt sources;
- protected read-only canonical prompts and editable saved copies;
- saved-prompt default destinations and explicit mismatch handling;
- draft or explicitly confirmed live-send mode;
- one-job-at-a-time process lock;
- global pause;
- structured results and exact failure reasons;
- persistent SQLite activity history;
- one-time, daily, weekly, and bounded five-minute debug schedules in `America/Chicago`;
- persistent scheduled jobs across dashboard restarts;
- schedule create, edit, pause, resume, run, cleanup, and delete controls;
- separate Scheduled Jobs and Run History categories with independent filters;
- no-billing Scheduler Ledger synchronization through the bound Apps Script endpoint.

Historical tests using retired display labels remain historical evidence only. Current runtime presentation uses canonical HQ names while stable internal keys remain unchanged.

## Desktop Department Automation

Status: Operational for attended use and validated recovery under the current safety contract. Package D has exposed a remaining false-negative write-verification defect after a visibly successful canonical paste.

Canonical implementation:

- launcher: `apps/lifeos-dashboard/automation/draft_department_boot.py`
- production engine: `apps/lifeos-dashboard/automation/open_department_chat_group.py`
- verification shim: `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`
- canonical catalog: `apps/lifeos-dashboard/lifeos_dashboard/canonical_prompt_catalog.py`
- read-only probe: `apps/lifeos-dashboard/automation/probe_composer_group_clipboard.py`
- naming standard: `memory/HQ_NAMING_STANDARD.md`

Safety contract:

- exact destination matching only;
- bounded exact project and `Show more` recovery;
- exact active-document verification;
- stable Group composer discovery and reacquisition;
- preserve an occupied composer;
- preserve clipboard lifetime through verification and restore the prior value afterward;
- explicit send authorization;
- one job at a time;
- stop on uncertainty;
- never blind-retry after uncertain state.

## Canonical Prompt Catalog

Status: Implemented. Live verification is the remaining Package D gate.

Protected families:

- Boot;
- Quick Boot;
- Fresh / Full Boot;
- Sync;
- Nightly;
- Advisory;
- Sync Advisory;
- Read Advisory;
- Consume Advisory.

`memory/CONTEXT_REMINDER.md` remains the canonical command vocabulary. The executable catalog is a protected runtime representation, not a competing governance source.

## LifeOS Dashboard

Canonical application path:

- `apps/lifeos-dashboard/`

Verified live sources:

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
- guarded GitHub sync is limited to clean, strictly-behind fast-forward updates;
- Trello, Todoist, and Calendar remain independent read-only adapters with cache behavior;
- Gmail and general Drive adapters remain deferred until demonstrated need;
- the dashboard is a visibility and bounded local-control layer, not a replacement source of truth;
- Department Inspection does not edit, merge, close, promote, demote, or create advisories automatically.

## Production Boundary

The established scheduler policy and recovery behavior are live-validated. Fully unattended Windows operation is not assumed merely because scheduling works.

Current boundary:

- ChatGPT Classic must be available and responsive for UI automation;
- failed scheduled runs pause according to the validated policy rather than retrying blindly;
- Engineering HQ Daily Sync remains paused until Rob explicitly resumes it;
- Package D must close before Package E or additional automation surface expansion begins;
- Windows startup, desktop shell, service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Other Active Tracks

- Observe ordinary role-routed specialist boots and inspect only demonstrated defects.
- Observe four-source dashboard behavior during ordinary use and genuine degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real items.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft the operation-ledger schema and connector-health policy.
- Continue Office Leaks delivery architecture as concrete requirements mature.

## Advisory State

As of 2026-07-18:

- No open advisories are listed in `coordination/ADVISORY_INDEX.md`.
- ADV-20260717-040 is implemented / acknowledged / closed.
- ADV-20260716-039 is implemented / acknowledged / closed.
- ADV-20260716-038 is acknowledged / ingested / closed.

## Immediate Next Action

Wait for a healthy and responsive ChatGPT Classic state. Obtain one visible full canonical draft paste, leave the draft in place, run the existing read-only composer clipboard probe for `LifeOS HQ`, and inspect the complete terminal output before changing verification behavior.

## Safety and Truthfulness

- Prefer small, verifiable operations.
- Fetch before editing and verify after writing.
- Keep connector-heavy work narrowly scoped.
- Never commit secrets or private account data.
- Never claim local runtime success without Rob's confirmation.

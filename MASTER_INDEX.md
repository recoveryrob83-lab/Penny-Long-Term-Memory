# LifeOS Repository Master Index

**Indexed branch:** `main`  
**Indexed commit:** `1b07290b508c9bedbf70a6dee4e8520a67cc662b`  
**Indexed date:** 2026-08-08

## Purpose and boundary

This is a path-first navigation aid for the LifeOS repository. It helps Codex, OpenCode, API workers, ChatGPT, and future harnesses find the right room, record, contract, implementation, or verification surface with the smallest useful read scope.

This file is **not a source of truth, boot authority, operating contract, status ledger, or authorization**. It does NOT replace:

- `memory/STARTUP_BOOT.md`;
- Project Instructions;
- shared operating contracts;
- department identity files;
- department handoffs;
- status or open-loop ledgers;
- advisories;
- Worker profiles;
- procedures;
- live source inspection;
- tests;
- acceptance evidence; or
- Rob's authority.

Live authoritative records and current source override this map. This index must be refreshed when stable paths or ownership boundaries change, but volatile operational state belongs in its own record.

## How to use this index

1. Start with `memory/STARTUP_BOOT.md`. It remains the canonical startup entry point and defines the read route.
2. Load the universal kernel in the exact order shown below.
3. Identify the named room, department, project, Worker, or audit scope.
4. Follow the path map to the smallest relevant handoff, identity, status, open-loop, procedure, advisory, source, or test surface.
5. Read authoritative records before acting. Boot loads context; it does not authorize work.

Future `AGENTS.md` files and Skills may use this map as a routing aid. This file itself grants no permission and does not create a new boot route.

## Repository at a glance

| Path | Role | Ownership / boundary |
|---|---|---|
| `memory/` | Universal boot, global handoffs, operating rules, project map, system state, naming, and integration references | `Maintenance_HQ` owns shared operating infrastructure; `memory/05_OPEN_LOOPS.md` is for system-owned loops only |
| `coordination/` | Shared contracts, ownership SOPs, source-boundary standards, advisory routing, and cross-department communication | Shared governance; `Maintenance_HQ` owns global coordination hygiene; source departments own their advisory text |
| `coordination/boards/` | Source department advisory boards | The source department owns the full advisory record; the index routes to it |
| `projects/` | Durable department and standalone-project records | Each department/project owns its subtree; `LifeOS_HQ` has no project subtree or independent backlog |
| `workers/` | Two grandfathered top-level Worker pilots and compatibility pointer | Compatibility only; new profiles belong under department project trees |
| `apps/` | LifeOS dashboard generations, courier server, browser extension, and tests | `Engineering_HQ` owns technical implementation and verification; applications do not become sources of truth |
| `scheduled-tasks/` | Scheduled-task prompts, memos, indexes, and run/issues logs | Historical/operational automation support; does not replace department state or advisory routing |
| `engineering/` | Engineering classroom, notebooks, and playground implementation material | Engineering-owned implementation/support area; inspect only when technical work requires it |
| `templates/` | Reusable project/status templates | Templates are scaffolding, not current records |
| `archive/` | Historical and superseded project records | Historical context only; never infer current authority from archive presence |
| `.lifeos-v2/` | Local runtime and acceptance/evidence JSON fixtures | Generated/runtime evidence; not durable architecture or authority |
| `README.md`, `MIGRATION_PLAN.md`, `MIRROR_STATUS.md` | Root orientation and migration/mirror records | Read for repository context or migration work; current boot and contracts take precedence |

## Universal operating kernel

`memory/STARTUP_BOOT.md` defines this exact order for `LifeOS_HQ`, Department HQs, standalone projects, and explicit system reviews:

1. `memory/STARTUP_BOOT.md` — canonical startup and role-routing procedure.
2. `coordination/LIFEOS_PROJECT_INSTRUCTIONS.md` — versioned Project Instructions deployment source.
3. `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md` — Hub, role, authority, naming translation, and action-transfer boundaries.
4. `memory/00_START_HERE.md` — global starting orientation.
5. `memory/CONTEXT_REMINDER.md` — compact context guardrails.
6. `memory/03_OPERATIONAL_RULES.md` — global operating rules.
7. `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md` — department ownership and drift-management boundary.
8. `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md` — local versus system loop ownership and visibility.
9. `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md` — Chat versus bounded Work execution boundary.
10. `memory/06_DAILY_OPERATING_SOP.md` — daily operating standard.

After the kernel, every `LifeOS_HQ` and Department HQ loads `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`. A Worker additionally loads `coordination/WORKER_EXECUTION_CONTRACT.md`, its owning department identity, exact profile, referenced assignment, and only required local records.

The following are deliberately **not** universal-kernel files: `memory/01_SESSION_HANDOFF.md`, `memory/02_BOOT_LOG.md`, `memory/04_ACTIVE_PROJECTS.md`, `memory/05_OPEN_LOOPS.md`, `MIGRATION_PLAN.md`, `MIRROR_STATUS.md`, and the Worker contract. Load them by role or task route.

## Role and department map

`LifeOS_HQ` is the shared strategic meeting room, not a department. It routes real actions to one owning department and one authoritative destination. Its durable coordination route is `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`, with global Hub context in `memory/01_SESSION_HANDOFF.md`, `memory/04_ACTIVE_PROJECTS.md`, and `memory/05_OPEN_LOOPS.md` when relevant.

| Current room | Canonical filesystem subtree | Core boot records | Durable history / execution surfaces |
|---|---|---|---|
| `Chief_of_Staff_HQ` | `projects/main-assistant/` | `SESSION_HANDOFF.md`, `DEPARTMENT_IDENTITY.md`, `README.md`, `status.md`, `open_loops.md` | `NOTEBOOK.md`; Hub-originated advisory source is `coordination/boards/main-assistant.md` |
| `Maintenance_HQ` | `projects/life-logistics-hq/` | `SESSION_HANDOFF.md`, `DEPARTMENT_IDENTITY.md`, `README.md`, `status.md`, `open_loops.md` | `notebook/`; `workers/maintenance_worker.md`; `procedures/`; `worker-results/maintenance_worker/` |
| `Engineering_HQ` | `projects/engineering/` | `SESSION_HANDOFF.md`, `DEPARTMENT_IDENTITY.md`, `README.md`, `status.md`, `open_loops.md` | `NOTEBOOK.md` plus `notebook/`; `workers/engineering_worker.md`; `procedures/`; `worker-results/engineering_worker/`; `advisories/`; `pending-advisories/`; `PENDING_ADVISORIES.md` |
| `Finance_HQ` | `projects/finance-benefits/` | `SESSION_HANDOFF.md`, `DEPARTMENT_IDENTITY.md`, `README.md`, `status.md`, `open_loops.md` | `NOTEBOOK.md`; department board is `coordination/boards/finance.md` |
| `Business_HQ` | `projects/business-development/` | `SESSION_HANDOFF.md`, `DEPARTMENT_IDENTITY.md`, `README.md`, `status.md`, `open_loops.md` | No department notebook, Worker profile, or procedure directory is currently present; board is `coordination/boards/business.md` |
| `Office_Leaks_HQ` | `projects/office-leaks-consulting/` | `SESSION_HANDOFF.md`, `DEPARTMENT_IDENTITY.md`, `README.md`, `status.md`, `open_loops.md` | `NOTEBOOK.md` plus `notebook/`; `SYNC_CHECKLIST.md`, `BOOT_SYNC.md`; board is `coordination/boards/office-leaks.md` |
| `Wellness_HQ` | `projects/wellness/` | `SESSION_HANDOFF.md`, `DEPARTMENT_IDENTITY.md`, `README.md`, `status.md`, `open_loops.md` | `NOTEBOOK.md`; board is `coordination/boards/wellness.md` |

Canonical room names are not automatic filesystem rename instructions. In particular, `projects/main-assistant/` is the stable path for `Chief_of_Staff_HQ`, and `projects/life-logistics-hq/` is the stable path for `Maintenance_HQ`. Historical files may retain former names.

Other routed project records exist under `projects/` (including `caregiver-income/`, `job-search/`, `cleanup/`, `recovery-logistics/`, `philosophy/`, `life-os-infrastructure/`, `health-medical/`, and `housing-logistics/`). They are standalone, dormant, scaffold, or shared-infrastructure project routes—not additional top-level HQs unless the canonical boot and naming records say so.

## Advisory and cross-department communication

| Path | Role / boundary |
|---|---|
| `coordination/ADVISORY_INDEX.md` | The sole active routing dashboard; use it to find current advisory IDs, lifecycle, target, revision, verification mode, and source board |
| `coordination/boards/` | Current source boards: `business.md`, `caregiver.md`, `cleanup.md`, `engineering.md`, `finance-benefits.md`, `finance.md`, `job-search.md`, `life-os.md`, `main-assistant.md`, `office-leaks.md`, `philosophy.md`, `recovery.md`, and `wellness.md` |
| `coordination/LIFEOS_V2_ADVISORY_COURIER_ENVELOPE.md` | Shared machine-readable courier transport contract; the full advisory remains authoritative on its source board |
| `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`, `coordination/ADVISORY_BOARD_REVIEW_2026-07-10.md`, `coordination/template.md` | Advisory lifecycle, review, and authoring references |
| `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` | Shared execution, ownership, lifecycle, verification, wake, hold, resume, and reporting contract |
| `apps/lifeos_dashboardv2/lifeos_v2/advisory_source.py` | V2 parser/reader implementation for indexed source-board advisories |
| `apps/lifeos_dashboardv2/lifeos_v2/runtime.py`, `api.py`, `contracts.py`, `reader.py` | V2 local courier runtime, API, contracts, and repository reader |
| `apps/lifeos-dashboard/lifeos_dashboard/worker_advisory_pipeline.py` and `apps/lifeos-dashboard/automation/` | Older/broader dashboard and desktop automation transport implementation |

The Advisory Index is the routing dashboard, not the full record. Full advisory text lives on the source department board. Formal `LifeOS_HQ` advisories use `Chief_of_Staff_HQ` as source and retain `coordination/boards/main-assistant.md` as the source-board path. Parser, dashboard, courier, and transport machinery validate and move authorized work; they do not create authority.

## Worker and procedure map

- Shared Worker boot and authority: `memory/STARTUP_BOOT.md`, `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`, and `coordination/WORKER_EXECUTION_CONTRACT.md`.
- Canonical department-owned profiles: `projects/engineering/workers/engineering_worker.md` and `projects/life-logistics-hq/workers/maintenance_worker.md`. No speculative profile directories are implied for departments without one.
- Department procedures: `projects/engineering/procedures/` and `projects/life-logistics-hq/procedures/`.
- Immutable run/result and review artifacts: `projects/engineering/worker-results/engineering_worker/` and `projects/life-logistics-hq/worker-results/maintenance_worker/`. Engineering also has `apps/lifeos-dashboard/projects/engineering/worker-results/` for implementation-side evidence used by the application.
- Engineering-owned runtime contracts and schemas: `apps/lifeos-dashboard/lifeos_dashboard/worker_result_contract.py`, `worker_result_ingester.py`, `worker_hq_review.py`, `worker_verification.py`, and `lifeos_dashboard/data/worker-*.schema.json`.
- Grandfathered compatibility pilots: `workers/penny-raw-capture/` and `workers/penny-inventory/`. Their `WORKER_BOOT.md` files are bounded compatibility profiles; `workers/WORKER_STANDARD.md` is only a pointer to current shared contracts. Do not create new top-level Worker packages by analogy.

Workers execute bounded authorized procedures, preserve scope, verify, and return one controlled outcome. The Worker contract—not this index—defines those rules.

## Application and automation map

| Application | Important paths | Status / boundary |
|---|---|---|
| `apps/lifeos-dashboard/` | `run_dashboard.py`; `lifeos_dashboard/main.py`, `service.py`, `adapters/`, `templates/`, `static/`; `automation/`; `tests/` | Current broad local read-mostly dashboard and bounded desktop/Worker automation implementation. It reads GitHub, Trello, Todoist, and Calendar surfaces; GitHub remains authoritative. Test with `apps/lifeos-dashboard/tests/`. |
| `apps/lifeos_dashboardv2/` | `lifeos_v2/main.py`, `api.py`, `runtime.py`, `reader.py`, `advisory_source.py`, `contracts.py`, `connectors.py`; `tests/`; `extension/` | Current V2 slice-one local advisory-courier server/contracts implementation. It follows active Advisory Index entries and source boards; it is not the broad dashboard. Run from this directory with the documented Uvicorn command. |
| `apps/chatgpt-dom-window-extension/` | `manifest.json`; `src/`; `popup/`; `tests/core.test.js` | Experimental Edge Manifest V3 long-chat DOM-window extension. Static tests exist; live browser behavior remains a separate verification surface. |
| `apps/lifeos-dashboard/automation/` | `draft_department_boot.py`, `run_worker_advisory_dispatch.py`, `run_worker_result*`, `run_worker_hq_review*`, browser/desktop bridge helpers | Engineering-owned transport and automation scripts. They draft, dispatch, inspect, ingest, or verify within bounded contracts; they do not grant authority. |
| `apps/lifeos-dashboard/apps-script/` | `scheduler_ledger_web_app.gs` | Scheduler-ledger web-app integration surface. Treat as implementation, not durable schedule truth. |

Application/runtime state may also appear in `.lifeos-v2/` and ignored local caches defined by the dashboard code. These are runtime or acceptance evidence, not durable architecture records. Do not infer deprecation or authority merely from having multiple generations; read the application README, source, and tests for the task in scope.

## Source-system and ownership map

The authoritative boundary is defined by `memory/STARTUP_BOOT.md` and `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md`:

| Record class / system | Start here | Boundary |
|---|---|---|
| Durable LifeOS Markdown, policies, procedures, architecture, advisories, department state | `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md` and the routed file under `memory/`, `coordination/`, or `projects/` | GitHub is the durable source for abstract operational text and versioned records |
| Human-facing working documents and detailed records | `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md` | Google Drive is the working-records cabinet; the `Life OS Pointer Registry` is the directory service; Drive may be authoritative for native office artifacts |
| Raw intake, possibilities, attention, and flow | `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md` | Trello owns that natural flow; do not duplicate raw ideas into durable project state without promotion |
| Rob-facing tasks and reminders | `memory/STARTUP_BOOT.md` | Todoist owns actionable commitments and reminders |
| Timed commitments | `memory/STARTUP_BOOT.md` | Calendar owns scheduled time |
| Correspondence and communication evidence | `memory/STARTUP_BOOT.md` | Gmail owns communication evidence |
| Dashboard, parser, courier, and automation runtime state | `apps/lifeos-dashboard/README.md` and `apps/lifeos_dashboardv2/README.md` | Runtime displays/transports selected state; it is not authoritative over GitHub, Trello, Todoist, Calendar, Gmail, or Drive |

## Current durable architecture records: where to look for X

| Need | Authoritative starting path |
|---|---|
| Startup and role routing | `memory/STARTUP_BOOT.md` |
| Current room names and stable path mapping | `memory/HQ_NAMING_STANDARD.md` |
| Hub, Chief of Staff, Maintenance, Engineering, and specialist boundaries | `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md` and department `DEPARTMENT_IDENTITY.md` |
| Project routing and department file pattern | `projects/README.md` |
| Global operating instructions | `coordination/LIFEOS_PROJECT_INSTRUCTIONS.md`, then the universal kernel |
| Shared execution and communication | `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` |
| File ownership and drift | `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md` and `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md` |
| Source-system boundaries | `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md` |
| Advisory routing | `coordination/ADVISORY_INDEX.md`, then the indexed source board |
| Advisory courier transport | `coordination/LIFEOS_V2_ADVISORY_COURIER_ENVELOPE.md` |
| Worker execution | `coordination/WORKER_EXECUTION_CONTRACT.md`, then the owning profile and required procedure |
| Current department state | The department's `SESSION_HANDOFF.md`, `status.md`, and `open_loops.md` under the mapped `projects/` path |
| System-owned loops and global watches | `memory/05_OPEN_LOOPS.md` |
| Global continuity and boot history | `memory/01_SESSION_HANDOFF.md`, `memory/02_BOOT_LOG.md` |
| Dashboard/automation implementation | `apps/lifeos-dashboard/README.md`, `apps/lifeos-dashboard/ARCHITECTURE.md`, then source/tests |
| V2 courier implementation | `apps/lifeos_dashboardv2/README.md`, then `lifeos_v2/` source and `tests/` |

## Tests and verification surfaces

- Broad dashboard/automation tests: `apps/lifeos-dashboard/tests/`.
- V2 server/parser/extension tests: `apps/lifeos_dashboardv2/tests/`.
- DOM-window extension unit tests: `apps/chatgpt-dom-window-extension/tests/`.
- Worker schemas and result examples: `apps/lifeos-dashboard/lifeos_dashboard/data/`.
- Durable Worker result, HQ review, rejection, and Rob-validation evidence: the department `worker-results/` trees listed above.
- Runtime/acceptance fixtures: `.lifeos-v2/`.

Interpret evidence in layers: source presence shows that a path or implementation exists; unit/integration tests show exercised code behavior; runtime verification shows a live or fixture execution; source-owner verification confirms the owning department reviewed the result; acceptance/closure requires the applicable authoritative procedure and authority. This task did not run the application test suites, so this index makes no test-passed claim.

## Historical, archive, migration, and compatibility areas

- `archive/` preserves completed, superseded, or predecessor context. `archive/projects/virtual-assistant-business/` is historical predecessor context for active `Office_Leaks_HQ`; active state is under `projects/office-leaks-consulting/`.
- `MIGRATION_PLAN.md` and `MIRROR_STATUS.md` describe the completed core migration and ongoing maintenance/synchronization posture.
- `scheduled-tasks/` contains scheduled-task memos, templates, indexes, and logs; it is not a replacement for department ledgers or the Advisory Index.
- `engineering/classroom/`, `engineering/notebooks/`, and `engineering/Playground/` contain Engineering support, experiments, and implementation notes; inspect for technical work, not current governance authority.
- `projects/` also contains dormant, consolidated, scaffold, and shared-infrastructure project records. Use `projects/README.md` and `memory/STARTUP_BOOT.md` to distinguish routed current rooms from historical project context.
- `workers/penny-raw-capture/` and `workers/penny-inventory/` are grandfathered compatibility packages, not the pattern for new Worker architecture.
- `.lifeos-v2/` is local runtime/acceptance evidence and may be generated or implementation-specific.

Historical names, closed advisories, immutable reports, and compatibility paths retain their historical meaning. Their presence does not promote them to current authority.

## Navigation warnings

- Live authoritative records override this map.
- Current source and tests override summaries of implementation here.
- Historical records retain their historical meaning.
- Department ownership boundaries remain in force; do not casually edit another department's files.
- Broad usefulness does not create need-to-know.
- Do not turn this index into a competing source of truth or copy volatile status into it.
- Do not infer authority from dashboard, parser, courier, scheduler, or runtime state.
- Generated, cache, fixture, and runtime files are not durable architecture unless an authoritative record explicitly defines them as such.
- `LifeOS_HQ` is a meeting room, not a department or backlog owner.
- The Advisory Index routes; the source board carries the full advisory.
- Transport machinery does not create authorization, interpret judgment, verify external success, or close authoritative work.
- Workers must use their current profile, contract, procedure, assignment, verification mode, and hold conditions.
- Boot is read-only by default and does not itself authorize maintenance or external action.
- Sensitive detailed records belong in their natural authoritative system; GitHub should remain abstract and operational.

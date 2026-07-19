# Engineering Advisory Board

Updated: 2026-07-19
Project: Engineering HQ
Purpose: Canonical cross-department advisories originating from Engineering HQ.

## Open Advisories

### ADV-20260719-044 — Reconcile Worker filesystem, shared pointers, and Maintenance continuity

- Date: 2026-07-19
- From: Engineering HQ
- To: Life OS Maintenance HQ
- Lifecycle State: OPEN
- Priority: HIGH
- Advisory Revision: 1
- Verification Mode: IMMEDIATE_HQ
- Posted Board: `coordination/boards/engineering.md`
- Target Department and Owner: Life OS Maintenance HQ
- Record Class: Shared-governance reconciliation and filesystem-pointer repair
- Authorization Basis: Rob authorized Engineering HQ to route the verified Worker-filesystem and shared-continuity corrections directly to Life OS Maintenance HQ after a read-only Engineering boot, sync, and repository verification pass.
- Related Work: ADV-20260719-043, ADV-20260718-042, Package D operations-procedure and Worker-runtime implementation, department ownership architecture, canonical Worker boot

#### Objective

Reconcile the residual shared-file and Maintenance-owned drift left after ADV-20260719-043 created the canonical execution and Worker protocols.

The canonical contract location is correct and must not be moved. The required repair is to align orientation, handoff, history, and Maintenance-owned state around the architecture already established:

- shared execution governance lives in `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`;
- the canonical Worker authority contract lives in `coordination/WORKER_EXECUTION_CONTRACT.md`;
- new department-owned Worker profiles live at `projects/<department>/workers/<profile>.md`;
- the root `workers/` area contains only the two grandfathered pilot packages and compatibility pointers;
- Worker deployment and route availability belong to the future Engineering-owned routing registry, not the department profile;
- a Worker profile defines stable identity and authority, not a second deployment ledger, backlog, handoff, status file, or open-loop system.

This advisory is not a request to recreate ADV-043, relocate either canonical protocol, create Worker profiles, or modify Engineering runtime code.

#### Verified Drift Requiring Repair

Engineering's July 19 read-only verification and sync found:

1. `memory/00_START_HERE.md` still presents `workers/README.md` and `workers/WORKER_STANDARD.md` as the current "Worker root," even though both are now compatibility surfaces and new profiles are department-owned.
2. `memory/01_SESSION_HANDOFF.md` still describes the older pilot-centered Worker model and does not fully reflect the canonical protocol, profile location, or Engineering/Maintenance/department ownership split.
3. `projects/life-logistics-hq/SESSION_HANDOFF.md` and `projects/life-logistics-hq/status.md` remain centered on the Raw Capture and Inventory pilots and do not identify the two new canonical protocols or current Worker-profile convention.
4. The Maintenance operating watch in `projects/life-logistics-hq/open_loops.md` remains narrowly pilot-centered and should be reconciled as a standing watch without creating a duplicate active advisory loop.
5. `memory/02_BOOT_LOG.md` and `memory/CAPTAINS_LOG.md` do not record the July 19 architecture change. The operating rules require a meaningful boot or architecture change to be preserved in one appropriate history surface.
6. `coordination/WORKER_EXECUTION_CONTRACT.md` recommends `status: active` and requires a current profile lifecycle state. That risks duplicating deployment state between the department profile, Engineering registry, visible chat, and dashboard.
7. The ordinary chat verification exposed a real role-routing defect: Engineering HQ identified itself as Business HQ and nearly selected the Business source board. The error was stopped before any advisory or global write occurred, but it demonstrates why universal orientation and source-board pointers must be unambiguous.

#### Required File Repairs

##### 1. `memory/00_START_HERE.md`

Replace the stale Worker-root wording with an accurate orientation:

- canonical shared Worker rules are in `coordination/`;
- department-owned profiles are in `projects/<department>/workers/<profile>.md`;
- `workers/README.md` and `workers/WORKER_STANDARD.md` are compatibility surfaces for grandfathered pilots only;
- Workers follow the Worker branch in `memory/STARTUP_BOOT.md`;
- no new top-level Worker packages are created by analogy.

Do not create a second boot order in this orientation file.

##### 2. `memory/01_SESSION_HANDOFF.md`

Update the global handoff to reflect:

- the active canonical execution and Worker protocols;
- one canonical boot entry point;
- department-owned Worker profiles created only on activation;
- Chief of Staff and Department HQ calling authority under the one-wake model;
- Life OS Maintenance ownership of global contracts, boot coherence, and profile convention;
- department ownership of Worker authority and profiles;
- Engineering ownership of routing registry, exact-title transport, receiver state, revision deduplication, verification queues, wake suppression, and technical rollover;
- the two root pilot packages as grandfathered compatibility packages, not the model for new Workers.

Preserve unrelated global state and do not turn the handoff into a duplicate Worker contract.

##### 3. `coordination/WORKER_EXECUTION_CONTRACT.md`

Remove the deployment-state ambiguity from the profile schema:

- remove `status: active` from the recommended profile front matter;
- remove "current profile lifecycle state" from required profile metadata;
- state explicitly that deployment state, route availability, pause, active/retired routing, and current chat resolution belong to the Engineering-owned routing registry and runtime state;
- retain `worker_id`, exact `chat_title`, owning department, `role`, specialization, and `profile_version` as stable profile metadata;
- retain the rule that the department profile owns stable identity and authority only.

Do not invent a new profile-lifecycle field during this repair. If Maintenance believes a distinct authority-profile lifecycle is necessary, return `REPORT_AND_HOLD` with the proposed distinction rather than creating another state ledger implicitly.

##### 4. `projects/life-logistics-hq/SESSION_HANDOFF.md`

Update Maintenance's handoff to reflect its current Worker responsibilities:

- own the canonical shared execution and Worker contracts;
- own boot coherence and Worker-profile conventions;
- audit shared rule and pointer consistency;
- preserve root-pilot compatibility without treating the pilots as the current architecture;
- route department-local profile corrections to the owning department;
- leave routing registry, exact-title lookup, receiver state, queues, wake suppression, and technical reliability to Engineering.

Remove or clarify older wording that assigns durable Worker routing implementation to Maintenance.

##### 5. `projects/life-logistics-hq/status.md`

Update current operational state and priorities to include:

- ADV-043's canonical protocol architecture;
- the department-owned profile location;
- root-pilot compatibility status;
- the current Maintenance/Engineering/department boundary;
- this advisory as the current bounded Maintenance reconciliation until completed.

Do not create a parallel backlog in status.

##### 6. `projects/life-logistics-hq/open_loops.md`

Reconcile only the standing Worker operating watch:

- preserve it as a watch rather than an open task;
- expand it from pilot-pointer hygiene to canonical contract, profile-location, compatibility, and ownership-boundary coherence;
- do not duplicate this advisory as a new active department open loop merely for visibility.

##### 7. Architecture history

Record the July 19 architecture change in `memory/02_BOOT_LOG.md` as the preferred boot-history surface.

The entry should preserve:

- creation of the two canonical protocols;
- one canonical HQ/Worker boot branch;
- department-owned Worker profiles;
- root-pilot compatibility status;
- one-wake direct execution-ready routing;
- Engineering versus Maintenance versus department ownership;
- the remaining Engineering implementation dependencies.

Use `memory/CAPTAINS_LOG.md` instead only if current file semantics make it clearly more appropriate. Do not duplicate the same detailed entry in both logs.

#### Files to Verify but Not Change Without Demonstrated Drift

- `memory/STARTUP_BOOT.md`
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `workers/WORKER_STANDARD.md`
- `workers/README.md`

These currently express the intended canonical or compatibility architecture. Re-read them during implementation. Modify them only if a concrete contradiction remains after the required repairs, and report the exact reason.

#### Explicitly Out of Scope

Do not:

- move either canonical protocol out of `coordination/`;
- copy the protocols into every department;
- create speculative `workers/` folders or profiles under specialist departments;
- create a new top-level Worker project;
- migrate, retire, or relocate the Raw Capture or Inventory pilots;
- modify Engineering code, routing registry implementation, dashboard behavior, or automation runtime;
- revise ADV-20260718-042;
- edit specialist department files;
- create duplicate open loops or advisory copies for visibility;
- broaden this repair into a general repository cleanup.

#### Acceptance Criteria

The advisory is complete only when:

1. `memory/00_START_HERE.md` no longer presents the root compatibility directory as the current Worker architecture.
2. Global and Maintenance handoffs accurately describe the canonical protocols, profile location, compatibility pilots, and ownership split.
3. Maintenance status reflects the July 19 architecture without becoming a duplicate work ledger.
4. The Maintenance Worker watch is current and remains classified as a standing watch.
5. The Worker contract no longer duplicates deployment state in department-owned profile metadata.
6. Deployment state is explicitly assigned to the Engineering routing registry/runtime, while profiles retain stable identity and authority only.
7. One architecture-history surface records the July 19 change.
8. `memory/STARTUP_BOOT.md` still resolves one coherent HQ branch and one coherent Worker branch.
9. Root `workers/` files remain compatibility-only and no new top-level Worker package is created.
10. No specialist department profile, Engineering runtime file, dashboard code, or automation code is modified.
11. All changed files are re-fetched and verified after writing.
12. Maintenance reports exact files changed, files inspected but unchanged, conflicts found, and any remaining dependency.

#### Required Outcome

Return exactly one controlled outcome:

- `IMPLEMENT` when all bounded repairs are completed and verified;
- `REPORT_AND_HOLD` when an existing authoritative file or unresolved state-model conflict prevents safe reconciliation;
- `ELEVATE_FOR_APPROVAL` only when completing the repair would require changing the approved organizational architecture or creating a new authority class.

Do not close this advisory without current read-back evidence.

## Recently Acknowledged / Implemented Advisories

### ADV-20260717-040 — Reconcile shared LifeOS memory after live dashboard and PennyOS milestone

- Date: 2026-07-17
- From: Chief Engineering Penny / Engineering HQ
- To: Life Logistics HQ
- Priority: Medium
- Status: Implemented / Acknowledged / Closed
- Implemented: 2026-07-17
- Acknowledged: 2026-07-17
- Closed: 2026-07-17
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Related Project(s): LifeOS Dashboard, PennyOS historical milestone, shared global memory, dashboard source boundaries

#### Outcome

Life Logistics reviewed and reconciled only the stale or materially incomplete shared summaries:

- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`
- `projects/life-logistics-hq/SESSION_HANDOFF.md`
- `projects/life-logistics-hq/open_loops.md`

The synchronized state now records:

- the LifeOS Dashboard as a locally running, tested, read-mostly four-source interface;
- GitHub, Trello, Todoist, and Google Calendar private iCal as verified live dashboard sources;
- the complete 16-test suite passing;
- Windows timezone support corrected through the runtime `tzdata` dependency;
- guarded GitHub auto-sync live-verified and limited to clean, strictly-behind fast-forward updates;
- Gmail and Google Drive dashboard adapters remaining deferred until demonstrated operational need;
- `projects/engineering/notebook/NOTE-20260717-008-pennyos-humble-beginnings.md` preserved as historical context only.

No credentials, private calendar URLs, tokens, detailed source-system records, or personal details were copied into GitHub. No separate PennyOS roadmap or open loop was created. No board-sync open loop remains.

### ADV-20260716-039 — Reconcile stale global LifeOS summaries after July 16 changes

- Date: 2026-07-16
- From: Chief Engineering Penny / Engineering HQ
- To: Life Logistics HQ
- Priority: Medium
- Status: Implemented / Acknowledged / Closed
- Implemented: 2026-07-17
- Acknowledged: 2026-07-17
- Closed: 2026-07-17
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Related Project(s): Life OS global memory, Office Leaks, Trello Flow Board, prompt launcher, desktop dashboard concept, advisory routing

#### Outcome

Life Logistics reconciled and verified the requested shared global summaries:

- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`

The synchronized state now includes:

- Office Leaks Consulting publicly launched and operating in a live organic market-test phase;
- the Trello LifeOS Flow Board as an active attention and flow interface with source-system boundaries;
- ADV-20260716-037 fully acknowledged and closed;
- ADV-20260716-038 acknowledged and closed as a read-mostly desktop dashboard concept;
- prompt-launcher newline defects corrected from Hub Boot onward;
- deferred launcher improvements retained in Engineering context rather than promoted into active global work.

Life Logistics also refreshed its own handoff and open-loop state. No detailed business, financial, personal, or source-system records were copied into GitHub.

### ADV-20260714-034 — Sync expanded Life OS shortcut set and prompt-launcher database

- Date: 2026-07-14
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Status: Implemented / Acknowledged / Closed
- Closed: 2026-07-14

Life Logistics ingested the expanded shortcut set. `memory/CONTEXT_REMINDER.md` remains canonical, and `engineering/classroom/prompt_launcher/prompt_library.json` remains a secondary launcher interface.

### ADV-20260710-032 — Create Penny Inventory Worker boot package

- Date: 2026-07-10
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Status: Implemented / Acknowledged / Closed
- Closed: 2026-07-10

Life Logistics created the canonical Penny Inventory Worker package, verified the `For Sale Inventory` Sheet target and schema, and updated worker routing. Real-photo pilot testing remains normal worker validation rather than open advisory work.

### ADV-20260710-031 — Establish advisory board lifecycle and compaction standard

- Date: 2026-07-10
- Status: Implemented / Closed
- Standard: `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`

Life Logistics created the advisory-board lifecycle standard and compacted Engineering while preserving prior detail through Git history.

### ADV-20260709-030 — Create Life OS worker boot standard and Penny Raw Capture Worker

- Date: 2026-07-09
- Status: Implemented / Closed

Life Logistics created the formal worker layer and Penny Raw Capture Worker package.

### ADV-20260708-027 — Sync Engineering Office Leaks architecture updates across Life OS

- Date: 2026-07-08
- Status: Implemented

Life Logistics synchronized Engineering's Office Leaks delivery architecture across Life OS.

## Board Rule

- Formal advisories originate on the source department board.
- `coordination/ADVISORY_INDEX.md` is the sole active routing dashboard.
- Operational boards follow `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`.
- Keep every open advisory in sufficient detail to act.
- Keep only a bounded recent completed working set.
- Git commit history is the default archive for older full advisory text.
- `coordination/DEPARTMENT_EVENT_INBOX.md` remains frozen historical state unless Rob explicitly reactivates it.

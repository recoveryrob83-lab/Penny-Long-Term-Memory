# Engineering_HQ Session Handoff

Updated: 2026-07-25
Project: Engineering_HQ
Purpose: Fresh-room handoff after Package F Wave 0B passed governance and the approved Maintenance Worker GitHub rollout prerequisites merged.

## Metadata

- Project Owner: Rob
- Primary Chat: `Engineering_HQ`
- Current Phase: Active / Package D Closed / Package E Closed / Package F Wave 0A Complete / Package F Wave 0B Complete / Maintenance Worker GitHub Prerequisites Complete / Route Linkage Pending
- Primary Systems: GitHub, local LifeOS Dashboard, SQLite Command Center runtime state, ChatGPT Department and Worker rooms, Engineering advisory board, Advisory Index, local Edge CDP bridge, and the GitHub-only Life OS Change Watch
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, private ChatGPT conversation URLs, or sensitive implementation details in LifeOS memory files or Worker result artifacts.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read `memory/HQ_NAMING_STANDARD.md` before touching title-bearing code, runtime state, prompt launchers, route mappings, or tests.
7. Read `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md` when Worker dispatch, immutable result ingestion, HQ review, Rob validation, consumption, or browser courier behavior is in scope.
8. Read `coordination/WORKER_EXECUTION_CONTRACT.md` and `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` when Worker authority, reporting, verification, activation prerequisites, or execution behavior is in scope.
9. Read the exact owning department's Worker profile and review procedure before linking, validating, or dispatching that Worker.
10. Perform a separate read-only Sync before any implementation write.
11. Keep connector, database, browser, and dashboard work small, explicit, fail-closed, and verifiable.

## Handbook Context

The Engineering-specific handbook is available through Project Sources as a noncanonical context mirror. It may restore ordinary room identity and stable boundaries without a full Boot, but it does not replace GitHub or authorize writes. Fetch live canonical files before consequential actions, runtime claims, route changes, or new package decisions.

## Department Role

`Engineering_HQ` owns technical architecture, software planning, repository strategy, automation design, APIs and connectors, data models, testing, debugging, implementation sequencing, build-readiness, and truthful verification.

Engineering owns technical Worker infrastructure: exact routing, transport, logging, duplicate suppression, immutable result ingestion, report repair, verification mechanics, runtime evidence, activation-prerequisite reporting, tests, and reliability safeguards.

Engineering does not own shared Worker governance, another department's Worker purpose or authority, source-owner advisory lifecycle, or domain judgment.

Route business strategy to `Business_HQ` or `Office_Leaks_HQ`, cost-bearing choices to `Finance_HQ`, ordinary daily coordination to `Chief_of_Staff_HQ`, shared governance and global memory hygiene to `Maintenance_HQ`, and wellbeing or sustainability judgment to `Wellness_HQ`.

## Completed Architecture

### Package D

Lifecycle State: CLOSED

Established Worker registry, route, browser transport, semantic receiver, duplicate suppression, verification mechanics, and bounded pilot foundations.

### Package E

Lifecycle State: CLOSED
Closed: 2026-07-23
Canonical closeout: `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Proved the Engineering-only chain for dispatch, immutable result evidence, deterministic ingestion, report repair, owning-HQ review, Rob validation when required, consumption readiness, watcher reporting, and duplicate suppression.

### Package F Wave 0A

Lifecycle State: COMPLETE
Completed: 2026-07-23

Established canonical room and Worker naming, exact registered Worker URL routing, route revisions, guarded route capture, zero-authority canary behavior, and browser-bridge recovery.

### Package F Wave 0B

Lifecycle State: COMPLETE
Completed: 2026-07-25

Completed slices:

- PR #15, merge `83c309f651de0354982fcd6cbb68f9cf3251d6a3`: cross-department owning-HQ destination resolution.
- PR #16, merge `3bf20ca231b3b5fbb1c315b24881e46939b3b508`: persisted shared safety-pause triggers.
- PR #17, merge `e1d297f1a2517490b3fb2a37298689c6db25bfb0`: conservative global send budget.
- PR #18, merge `4a00c4908cfd71a2b2ebfe41c084b68a5d2907e5`: read-only contract-derived activation gate.

Rob confirmed the post-merge dashboard smoke passed. Health and Worker Operations were ready, the Engineering Worker was available, the bridge and execution gate were active, and no review was pending.

## Maintenance Worker Rollout

Lifecycle State: GITHUB PREREQUISITES COMPLETE / ROUTE LINKAGE PENDING
Approval: Rob reports Wave 0B governance passed and creation of `Maintenance_Worker` is approved.
Merged PR: #19
Merge commit: `28a7a4fc40317d043dbe9983747475f85d37742a`

Canonical profile:

- `projects/life-logistics-hq/workers/maintenance_worker.md`

Canonical procedures:

- `projects/life-logistics-hq/procedures/maintenance_worker_result_submission.md`
- `projects/life-logistics-hq/procedures/maintenance_hq_worker_review_receipt.md`

PR #19 also registered the canonical Maintenance HQ review path in the Engineering-owned destination resolver and added canonical tests for profile loading, route resolution, result-procedure binding, and read-only activation readiness.

The initial profile permits only:

- manually dispatched `read_only_verification`;
- manually dispatched `read_only_governance_audit`;
- GitHub reads within the explicit assignment scope;
- one exact immutable result artifact under `projects/life-logistics-hq/worker-results/maintenance_worker/`;
- `IMMEDIATE_HQ` verification.

The profile grants no standing authority for maintenance writes, repair, implementation, publication changes, department-local edits, connectors, schedules, route control, runtime control, external writes, or unattended execution.

Rob reported the focused pytest, affected regression, and Ruff gates passed before merge. No automated GitHub workflow was configured, so the native local results are the recorded merge gate.

## Current Production Worker State

### Engineering Worker

- Worker ID: `engineering_worker`
- Exact chat title: `Engineering_Worker`
- Deployment state: `enabled`
- Route revision: `1`
- Route availability: `available`
- One authoritative registry row exists.
- Private exact URL remains only in ignored local SQLite state.

### Maintenance Worker

- Canonical Worker ID: `maintenance_worker`
- Exact chat title: `Maintenance_Worker`
- Canonical profile and procedures: present on `main`
- ChatGPT room: pending Rob creation
- Runtime registry linkage: pending
- Exact private route and positive route revision: pending
- Route availability: not yet established
- Zero-authority canary: pending
- Live activation-readiness inspection: pending
- Real pilot dispatch: not authorized by profile or route linkage alone

## Next Valid Action

After Rob creates the exact `Maintenance_Worker` room and opens it in the dedicated browser bridge:

1. Pull current `main` and restart or refresh the dashboard as needed.
2. Use Worker Operations to link the exact room through the guarded route mechanism.
3. Confirm exactly one `maintenance_worker` registry row.
4. Confirm the registry uses:
   - chat title `Maintenance_Worker`;
   - owning department `maintenance`;
   - profile path `projects/life-logistics-hq/workers/maintenance_worker.md`;
   - profile version `1`;
   - specialization `general`;
   - role `worker`.
5. Confirm the private exact URL remains only in local SQLite state.
6. Confirm a positive route revision and the expected initial route hold.
7. Run the existing zero-authority canary against the unchanged route revision.
8. Confirm route availability becomes `available` only after the canary succeeds.
9. Inspect the read-only activation report and confirm:
   - profile checks pass;
   - Maintenance HQ review-procedure checks pass;
   - route, pause, budget, and unresolved-review checks accurately reflect current runtime state;
   - `activation_authorized` remains `false`.
10. Stop before any real assignment, Worker dispatch, Maintenance HQ wake, schedule, pause/resume action, or budget reset.

A first real Maintenance pilot requires a separately exact assignment with one authorized task class, source references, read scopes, immutable result path, authorization source, and `IMMEDIATE_HQ` review condition.

## Validation Standard

- Fetch current files before editing.
- Use current SHAs or equivalent concurrency guards.
- Preserve unrelated content and historical evidence.
- Prefer the smallest useful change.
- Read back every significant write.
- Do not claim route availability, a canary pass, dispatch, external action, or verification without current evidence.
- No meaningful change means no write.

## Advisory State

Open Engineering advisories: None.

`ADV-20260718-042`, `ADV-20260719-044`, and `ADV-20260723-052` are closed and must not be recreated as active work.

## Production Boundary

- Browser automation acts only on exact canonical URLs.
- Registered exact Worker URLs, not sidebar visibility, are authoritative route locators.
- Each stable Worker ID has one authoritative registry row.
- Route changes increment the route revision and remain held until a zero-authority canary passes.
- The persisted shared safety pause is the only circuit-breaker state and requires explicit human resume.
- The send budget is one manually reset epoch shared by Worker and owning-HQ wake attempts; elapsed time never refills it.
- Reset does not Resume, erase evidence, or authorize a send.
- The activation validator reports prerequisites only and always sets `activation_authorized: false`.
- `READY_FOR_AUTHORITY_REVIEW` is not activation approval or assignment authority.
- Confirmed or uncertain submissions are not retried blindly.
- Immutable Git evidence outranks stale local transport state.
- Worker reports remain evidence until deterministic ingestion.
- `IMMEDIATE_HQ` work never auto-verifies.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Courier, ingester, dashboard, watcher, HQ receipt, and Rob receipt do not auto-close source work.
- The Worker courier does not wake `Chief_of_Staff_HQ` under the current contract.
- New Workers, connectors, recurring tasks, spending, cross-department authority, broader durable-write authority, or public actions require separate approval.

## Boundary

Rob decides. Department HQs own their Workers and judgment. `Maintenance_HQ` owns shared governance. `Engineering_HQ` owns the machinery. Source owners close their own records.

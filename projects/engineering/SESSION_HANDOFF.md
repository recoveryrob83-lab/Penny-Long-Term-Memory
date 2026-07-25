# Engineering_HQ Session Handoff

Updated: 2026-07-25
Project: Engineering_HQ
Purpose: Fresh-room handoff after Package F Wave 0B completed its controlled cross-department safety kernel without activating a cross-department Worker.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering_HQ
- Current Phase: Active / Package D Closed / Package E Closed / Package F Wave 0A Complete / Wave 0B Controlled Cross-Department Safety Kernel Complete / Canonical Runtime Title Rollover Complete / Direct URL Routing Complete / Guarded Route Capture Complete / Browser Bridge Reconnect Merged / DOM Memory Experiment Concluded
- Primary Systems: GitHub, local LifeOS Dashboard, SQLite Command Center runtime state, ChatGPT Department and Worker rooms, Engineering advisory board, Advisory Index, the local Edge CDP bridge, and the GitHub-only Life OS Change Watch
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, private ChatGPT conversation URLs, or sensitive implementation details in LifeOS memory files or Worker result artifacts.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read `memory/HQ_NAMING_STANDARD.md` before touching title-bearing code, runtime state, prompt launchers, route mappings, or tests.
7. Read `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md` when Worker dispatch, immutable result ingestion, HQ review, Rob validation, scheduled consumption, or browser courier behavior is in scope.
8. Read `coordination/boards/engineering.md` and `coordination/ADVISORY_INDEX.md` when routing or advisory lifecycle is relevant.
9. Read `coordination/WORKER_EXECUTION_CONTRACT.md` and `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` when Worker authority, reporting, verification, activation prerequisites, or execution behavior is in scope.
10. Perform a separate read-only Sync before any implementation write.
11. Keep connector, database, browser, and dashboard work small, explicit, fail-closed, and verifiable.

## Department Role

`Engineering_HQ` owns technical architecture, software planning, repository strategy, automation design, APIs and connectors, data models, testing, debugging, implementation sequencing, build-readiness, and truthful verification.

Engineering owns technical Worker infrastructure: exact routing, transport, logging, duplicate suppression, result ingestion, verification mechanics, runtime evidence, tests, activation-prerequisite reporting, and reliability safeguards. Engineering does not own shared Worker governance, another department's Worker authority, source-owner advisory lifecycle, or domain judgment.

Route business strategy to `Business_HQ` or `Office_Leaks_HQ`, cost-bearing choices to `Finance_HQ`, ordinary daily coordination to `Chief_of_Staff_HQ`, shared governance and global memory hygiene to `Maintenance_HQ`, and wellbeing or sustainability judgment to `Wellness_HQ`.

## Package F Roadmap

### Wave 0A: Foundation

Lifecycle State: COMPLETE
Completed: 2026-07-23

Wave 0A includes the successful GitHub-only Life OS Change Watch, canonical room and Worker naming, repository-wide current-text reconciliation, the Engineering-only Worker execution and immutable evidence chain, owning-HQ review, Rob validation when required, watcher consumption, duplicate suppression, direct URL routing, guarded route rollover, and browser-bridge recovery.

Wave 0A completion did not activate a non-Engineering Worker, create a cross-department private route, grant new tools or durable-write authority, or authorize unattended sends.

### Wave 0B: Controlled cross-department safety kernel

Lifecycle State: COMPLETE
Started: 2026-07-23
Completed: 2026-07-25

Wave 0B completed Engineering's bounded technical prerequisites for future cross-department Worker adoption. It did not activate a Worker, register a non-Engineering private route, grant universal durable-write authority, change shared governance, or authorize unattended execution.

#### Slice 1: Cross-department owning-HQ destination resolution

Lifecycle State: COMPLETE
Completed: 2026-07-24
Merged PR: #15
Merge commit: `83c309f651de0354982fcd6cbb68f9cf3251d6a3`

The resolver derives canonical owning-HQ destinations without creating identities, routes, schedules, or authority; requires an explicitly registered department-owned review procedure; rejects cross-owner paths, Hub routing, and Chief of Staff courier routing; and preserves the existing Engineering-only default.

Rob ran the repository-native focused pytest and Ruff gates successfully. No live non-Engineering wake or route registration occurred.

#### Slice 2: Automatic shared safety-pause triggers

Lifecycle State: COMPLETE
Completed: 2026-07-24
Merged PR: #16
Merge commit: `3bf20ca231b3b5fbb1c315b24881e46939b3b508`

One singleton record in the existing Command Center database persists the shared pause, reason, affected run ID, trigger, recovery condition, and timestamps. Worker dispatch and owning-HQ review wakes trip that same pause before releasing the shared execution lock only for genuine send uncertainty, invalid claimed-success receipts, unknown browser return state, unclassified confirmed-send exceptions, or confirmed-send evidence persistence failure.

Ordinary deterministic pre-send validation failures, unavailable routes, duplicate suppression, review holds, and rejected work remain local. Resume is explicit and time never clears uncertainty.

Rob's repository-native affected regression gate passed `47` tests and Ruff passed. No live Worker or HQ wake occurred.

#### Slice 3: Conservative global send budget

Lifecycle State: COMPLETE
Completed: 2026-07-25
Merged PR: #17
Merge commit: `e1d297f1a2517490b3fb2a37298689c6db25bfb0`

One manually reset budget epoch lives on the existing singleton Command Center control record. Confirmed Worker dispatch and owning-HQ review wake attempts reserve atomically against the same default limit of three under the existing execution lock immediately before browser transport.

Attempts remain consumed whether transport succeeds, fails safely, or becomes uncertain. Dashboard restart and elapsed time do not refill the budget. Deterministic pre-send holds occur before reservation. Exhaustion blocks before transport, records the held operation, and trips the existing shared pause.

Reset requires explicit confirmation while paused, increments the epoch, and remains separate from Resume. Reservation evidence attaches to the existing execution row rather than creating another ledger. Worker Operations exposes limit, usage, remaining attempts, epoch, and held-operation state.

Rob ran the focused pytest, affected regression, and Ruff gates successfully and confirmed the Worker Operations budget UI loaded cleanly. Node.js was unavailable, so no separate Node syntax claim is made. No live Worker or HQ wake occurred.

#### Slice 4: Contract-derived activation gate

Lifecycle State: COMPLETE
Completed: 2026-07-25
Merged PR: #18
Merge commit: `4a00c4908cfd71a2b2ebfe41c084b68a5d2907e5`

The activation-readiness service recomputes one ephemeral prerequisite report from canonical Worker profile and owning-HQ procedure files plus current SQLite runtime evidence. It validates registry uniqueness and contract shape, profile identity and required sections, canonical Worker title, deployment state, exact route URL and revision, route availability and route holds, owning-HQ review procedure metadata and required sections, shared pause, remaining send budget, unresolved repair or Rob-validation rows, and retirement ownership.

SQLite is opened read-only. The report is exposed through Worker Operations and uses explicit `PASS`, `HOLD`, and `NOT_APPLICABLE` findings with source pointers. It creates no activation record, readiness ledger, registry row, route, procedure, schedule, permission, deployment mutation, or runtime authorization.

Every report sets `activation_authorized: false`. `READY_FOR_AUTHORITY_REVIEW` means only that the inspected technical prerequisites contain no current hold. Owning-department authority, Maintenance shared-governance review, and Rob's explicit decision where required remain separate gates.

Rob ran the focused activation tests, affected runtime regressions, and Ruff gate successfully before merge. No Worker activation, dispatch, HQ wake, route change, schedule, pause or resume action, or budget reset occurred.

## Completed Engineering Repair Chain

- PR #9, merge `f8cc341e17cb68492c5f66339382b753bd1612ab`: canonical underscore title rollover and courier verifier repair.
- PR #10, merge `b859c3c72e8b82f876b9ebf72d2961f4eb33ecbd`: exact registered Worker URL routing and live zero-authority route canary.
- PR #11, merge `2587b540e24ca09036c1f0094187c69c2b363c63`: guarded route capture and rollover with revision checks and canary-only promotion.
- PR #13, merge `0a1223c5f32df17fb22f11cb53d0badd5ef2a1ab`: one-click loopback Edge CDP bridge reconnect using the shared execution lock.
- PR #14, merge `131cf5d10a4a13cc76c30f99a09cefe75f4306c9`: optional DOM Window extension; live testing showed ChatGPT already virtualized old history and the extension did not address the demonstrated JavaScript-heavy memory pressure.
- PR #15, merge `83c309f651de0354982fcd6cbb68f9cf3251d6a3`: cross-department owning-HQ destination resolution without activation authority.
- PR #16, merge `3bf20ca231b3b5fbb1c315b24881e46939b3b508`: persisted shared safety-pause triggers.
- PR #17, merge `e1d297f1a2517490b3fb2a37298689c6db25bfb0`: one conservative global send budget shared by Worker dispatch and HQ wakes.
- PR #18, merge `4a00c4908cfd71a2b2ebfe41c084b68a5d2907e5`: read-only contract-derived activation prerequisite report.

## Validation Evidence

- Final consolidated pre-PR-13 local regression gate: `80 passed`.
- PR #13 targeted launcher harness: `5 passed`; dashboard JavaScript syntax check passed.
- PR #14 core tests: `5 passed`; JavaScript syntax and JSON validation passed.
- PR #15 isolated harness: `21` resolver cases and `4` runtime-integration cases passed; repository-native focused pytest and Ruff also passed.
- PR #16 repository-native affected regression gate: `47 passed`; focused Ruff passed.
- PR #17 repository-native focused pytest, affected regression, and Ruff gates passed; the Worker Operations budget UI loaded cleanly.
- PR #18 repository-native focused activation-readiness tests, affected runtime regressions, and Ruff gate passed.
- No automated GitHub workflow was configured for PRs #13 through #18. Native local results control the recorded merge-gate claims.
- Live evidence, not static or isolated test success, controls claims about routing availability and browser execution.

## Current Production Route State

- Worker ID: `engineering_worker`
- Exact chat title: `Engineering_Worker`
- Deployment state: `enabled`
- Route revision: `1`
- Route availability: `available`
- One authoritative registry row exists.
- The private exact conversation URL remains in ignored local SQLite state and is not duplicated into GitHub memory.
- Local Worker courier or orchestrator sends remain unauthorized unless Rob separately authorizes them.
- The separate `Chief_of_Staff_HQ` cloud watcher is not the local Worker courier and remains governed by its own read-only authority.
- Wave 0B created no non-Engineering Worker registry row, private route, or activation.
- No production safety pause was deliberately triggered during Wave 0B validation.
- No production send-budget attempt was consumed during Wave 0B validation.

## Dashboard Startup State

The latest dashboard code on `main` includes PR #18 at merge commit `4a00c4908cfd71a2b2ebfe41c084b68a5d2907e5` or later. Pull and restart the dashboard only when Rob is ready to load the merged code. The remaining dashboard smoke is a bounded route-state, persisted-pause, send-budget, activation-report, and guarded-control observation, not permission to configure or test a non-Engineering wake.

Canonical local launch command from `apps/lifeos-dashboard`:

```cmd
call .venv\Scripts\activate.bat
python run_dashboard.py
```

Dashboard URL:

```text
http://127.0.0.1:8765
```

Starting the dashboard or reconnecting the local browser bridge does not authorize a real Worker dispatch, route capture, route rollover, budget reset, schedule creation, orchestrator activation, Worker activation, or advisory lifecycle change.

## Package State

### Package D

Lifecycle State: CLOSED

### Package E

Lifecycle State: CLOSED
Closed: 2026-07-23
Canonical closeout: `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

### Package F Wave 0A

Lifecycle State: COMPLETE
Completed: 2026-07-23

### Package F Wave 0B

Lifecycle State: COMPLETE
Completed: 2026-07-25

Do not recreate completed Package D, Package E, Package F Wave 0A, or Package F Wave 0B Slices 1–4 as active tasks.

## Advisory State

Open Engineering advisories: None.

Recently closed:

- `ADV-20260723-052` closed after the hourly `Chief_of_Staff_HQ` watcher reported in the existing Chief of Staff conversation without creating a new chat or triggering work; Rob confirmed the result and authorized closure.
- `ADV-20260718-042` closed by the Chief of Staff source owner after Engineering implementation, source verification, and Rob approval for slow rollout. Slow rollout is an operational pacing decision, not unfinished Engineering implementation.

## Next Valid Action

The next bounded Engineering action is the post-merge dashboard smoke and route-management observation already recorded in `projects/engineering/open_loops.md`:

1. pull current `main` and restart the dashboard when operationally convenient;
2. confirm `/api/health` and Worker Operations load;
3. verify exactly one `engineering_worker` row at route revision `1` with availability `available`;
4. verify the persisted shared-pause and send-budget states remain visible without resetting or resuming them;
5. verify the activation report renders and remains `activation_authorized: false`;
6. confirm the report inspection does not mutate the database, route, profile, procedure, deployment state, schedule, permission, or authority;
7. do not configure a non-Engineering review procedure, register or capture a non-Engineering route, activate a Worker, dispatch an advisory, deliberately trigger a safety pause, reset the production budget, or enable unattended sends.

After that bounded observation, further Engineering work must come from `projects/engineering/open_loops.md`, a demonstrated defect with bounded repair authority, or a new explicit Rob instruction.

Cross-department Worker adoption remains Waiting on a current passing activation-prerequisite report, the owning Department HQ's explicit authority, Maintenance shared-governance review, and Rob's decision wherever the canonical contract requires it.

## Production Boundary

- Browser automation acts only on exact canonical URLs.
- Registered exact Worker URLs, not sidebar visibility, are authoritative route locators.
- Route changes update one existing Worker row and must pass the zero-authority canary before becoming available.
- Browser bridge reconnect is a local transport-recovery action only and cannot mutate route identity or authorize execution.
- Cross-department destination resolution is not Worker activation, route registration, permission expansion, scheduling, or dispatch authority.
- The persisted shared safety pause is the only circuit-breaker state and requires explicit human resume.
- The send budget is one manually reset epoch shared by Worker dispatch and owning-HQ wake attempts; elapsed time never refills it.
- Resetting the send budget does not Resume automation, erase a safety incident, or authorize a send.
- The activation validator reports prerequisites only. Passing technical checks does not create department authority, Maintenance approval, or Rob authorization.
- `READY_FOR_AUTHORITY_REVIEW` is not activation approval.
- Confirmed or uncertain submissions are not retried blindly.
- Immutable Git evidence outranks stale local transport state.
- Worker reports remain evidence until deterministic ingestion.
- `IMMEDIATE_HQ` work never auto-verifies.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Courier, ingester, dashboard, watcher, HQ receipt, and Rob receipt do not auto-close source advisories.
- The Worker courier never wakes `Chief_of_Staff_HQ` unless a separately authorized future contract explicitly changes that boundary.
- New Workers, connectors, recurring tasks, spending, cross-department rollout, or public actions require separate authority.

## Boundary

Rob decides. Department HQs own their Workers and judgment. `Maintenance_HQ` owns shared governance. `Engineering_HQ` owns the machinery. Source owners close their own records.

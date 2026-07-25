# Engineering_HQ Session Handoff

Updated: 2026-07-25
Project: Engineering_HQ
Purpose: Fresh-room handoff after Package F Wave 0B Slice 3 conservative global send budget was validated and merged.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering_HQ
- Current Phase: Active / Package D Closed / Package E Closed / Package F Wave 0A Complete / Wave 0B Slices 1–3 Complete / Wave 0B Slice 4 Contract-Derived Activation Gate Started / Canonical Runtime Title Rollover Complete / Direct URL Routing Complete / Guarded Route Capture Complete / Browser Bridge Reconnect Merged / DOM Memory Experiment Concluded
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

Engineering owns technical Worker infrastructure: exact routing, transport, logging, duplicate suppression, result ingestion, verification mechanics, runtime evidence, tests, and reliability safeguards. Engineering does not own shared Worker governance, another department's Worker authority, source-owner advisory lifecycle, or domain judgment.

Route business strategy to `Business_HQ` or `Office_Leaks_HQ`, cost-bearing choices to `Finance_HQ`, ordinary daily coordination to `Chief_of_Staff_HQ`, shared governance and global memory hygiene to `Maintenance_HQ`, and wellbeing or sustainability judgment to `Wellness_HQ`.

## Package F Roadmap

### Wave 0A: Foundation

Lifecycle State: COMPLETE
Completed: 2026-07-23

Wave 0A includes the successful GitHub-only Life OS Change Watch, canonical room and Worker naming, repository-wide current-text reconciliation, the Engineering-only Worker execution and immutable evidence chain, owning-HQ review, Rob validation when required, watcher consumption, duplicate suppression, direct URL routing, guarded route rollover, and browser-bridge recovery.

Wave 0A completion does not activate any non-Engineering Worker, create a cross-department route, grant new tools or durable-write authority, or authorize unattended sends.

### Wave 0B: Controlled cross-department safety kernel

Lifecycle State: ACTIVE
Started: 2026-07-23

#### Slice 1: Cross-department owning-HQ destination resolution

Lifecycle State: COMPLETE
Completed: 2026-07-24
Merged PR: #15
Merge commit: `83c309f651de0354982fcd6cbb68f9cf3251d6a3`

The merged resolver derives canonical destinations without creating identities, routes, schedules, or authority; requires an explicitly registered department-owned review procedure; rejects cross-owner paths, Hub routing, and Chief of Staff courier routing; and preserves the existing Engineering-only default.

Rob ran the repository-native focused pytest and Ruff gates successfully before PR #15 was marked ready and squash-merged. No live non-Engineering wake or route registration occurred.

#### Slice 2: Automatic shared safety-pause triggers

Lifecycle State: COMPLETE
Completed: 2026-07-24
Merged PR: #16
Merge commit: `3bf20ca231b3b5fbb1c315b24881e46939b3b508`

The merged safety slice strengthens the existing shared Command Center pause instead of creating a competing circuit-breaker record. One singleton row in the existing SQLite database persists manual and safety pause state, reason, affected run ID, trigger, recovery condition, and timestamps across dashboard restarts.

Worker dispatch and owning-HQ review wakes use the same pause and trip it before releasing the shared execution lock only for true post-send uncertainty, invalid claimed-success receipts, unknown browser return state, unclassified exceptions after entering a confirmed-send path, or confirmed-send evidence persistence failure. Ordinary deterministic pre-send validation failures, unavailable routes, duplicate suppression, department review holds, and rejected work remain local.

Rob ran the repository-native affected regression gate successfully with `47 passed`, and the focused Ruff gate passed after the package import formatting repair. No live Worker or HQ wake occurred.

#### Slice 3: Conservative global send budget

Lifecycle State: COMPLETE
Completed: 2026-07-25
Merged PR: #17
Merge commit: `e1d297f1a2517490b3fb2a37298689c6db25bfb0`

The merged budget slice extends the existing singleton Command Center control record with one manually reset send-budget epoch. Confirmed Worker dispatches and owning-HQ review wakes reserve atomically against the same default limit of three under the existing execution lock immediately before browser transport.

Attempts remain consumed whether transport succeeds, fails safely, or becomes uncertain. Dashboard restart and elapsed time do not refill the budget. Deterministic pre-send route, duplicate, draft, and validation holds occur before reservation. Exhaustion blocks the next send before transport, records the held operation, and trips the existing shared pause.

Reset requires explicit confirmation while automation is paused, increments the epoch, and remains separate from Resume. Reservation evidence attaches to the existing execution row rather than creating another ledger. Command Center and Worker Operations expose limit, usage, remaining attempts, epoch, and held-operation state. The zero-authority courier self-test remains outside the budget.

Rob ran the repository-native focused pytest, affected regression, and Ruff gates successfully. Node.js was unavailable, so no separate Node syntax claim is made; Rob loaded the dashboard and confirmed the Worker Operations budget UI rendered cleanly. No live Worker or HQ wake occurred.

#### Slice 4: Contract-derived activation gate

Lifecycle State: ACTIVE
Started: 2026-07-25

The next bounded slice must implement one read-only, fail-closed activation prerequisite validator derived from the canonical Worker contracts and existing source and runtime evidence. It should report whether the Worker profile, owning-department procedure, authority and tool scopes, evidence contract, registered route and revision, owning-HQ review path, shared pause and send budget, unresolved holds, and retirement rules satisfy technical prerequisites.

The validator must not create or modify a Worker registry row, route, procedure, deployment state, schedule, advisory, permission, or authority. It must not become another deployment ledger, infer that technical readiness equals authorization, or activate a Worker. Owning-department authority, Maintenance shared-governance review, and Rob's explicit decision remain separate gates.

## Completed Engineering Repair Chain

### Phase 1: Canonical title rollover and courier verifier repair

Merged through PR #9.

- Merge commit: `f8cc341e17cb68492c5f66339382b753bd1612ab`
- Canonical underscore room titles were implemented in Engineering-owned executable surfaces.
- Active SQLite title-bearing state was migrated idempotently.
- Stable destination keys, Worker IDs, run IDs, wrapper IDs, filesystem paths, historical rows, immutable reports, receipts, and checksums were preserved.
- The post-navigation verifier now trusts the already resolved exact URL plus loaded-room witnesses instead of requiring the selected sidebar anchor to remain visible after navigation.
- Virtualized-history submission witness behavior was repaired without weakening fail-closed submission proof.

### Phase 2: Authoritative direct Worker URL routing

Merged through PR #10.

- Merge commit: `b859c3c72e8b82f876b9ebf72d2961f4eb33ecbd`
- The existing Worker registry row stores the exact ChatGPT conversation URL and a monotonic `route_revision`.
- Browser dispatch uses only the registered exact URL and never falls back to sidebar discovery.
- Missing or invalid registered URLs fail closed before any send.
- The production `engineering_worker` row was migrated in place with route revision `1`.
- A live zero-authority canary succeeded, returned to the source room, correlated the submitted user turn, and created no durable Worker authority.
- The verified production route was promoted to `available`.

### Phase 2b: Guarded dashboard route capture and rollover

Merged through PR #11.

- Merge commit: `2587b540e24ca09036c1f0094187c69c2b363c63`
- The Worker Operations dashboard can capture the sole active ChatGPT Worker conversation from the CDP browser target list without requiring Rob to paste a URL.
- Capture requires automation to be paused, the shared execution lock to be free, explicit confirmation, a current expected route revision, exactly one ChatGPT conversation target, the correct Worker title, and no duplicate ownership.
- A changed route updates the existing Worker row, increments `route_revision`, clears `last_seen_at`, and places the route on `unknown` verification hold.
- Real advisory execution remains blocked unless route availability is exactly `available`.
- The existing zero-authority courier canary promotes only the exact unchanged witnessed route revision.
- Route capture and canary verification use the dashboard's exact active SQLite database.
- No production route rollover was performed during this implementation.

### Phase 2c: One-click Edge browser bridge reconnect

Merged through PR #13.

- Merge commit: `0a1223c5f32df17fb22f11cb53d0badd5ef2a1ab`
- Worker Operations now shows **Reconnect bridge** when the Edge CDP endpoint is offline.
- The reconnect API launches a dedicated Edge profile on loopback `127.0.0.1:9222`, preserves that profile under ignored local state, and verifies `/json/version` before reporting Ready.
- The action uses the shared execution lock and refuses non-loopback endpoints, concurrent automation, and unnecessary duplicate launch when CDP is already healthy.
- Reconnect cannot mutate Worker routes, route revisions, advisories, schedules, execution history, or Worker authority.
- The launcher waits for verified CDP readiness even when the original Edge launcher process hands the browser window to another process.

### Phase 2d: ChatGPT DOM memory experiment

Package merged through PR #14; live conclusion recorded 2026-07-23.

- Merge commit: `131cf5d10a4a13cc76c30f99a09cefe75f4306c9`
- The extension is inert until manually loaded, disabled by default, scoped per saved conversation, and blocked in canonical Worker rooms.
- Static tests passed.
- A long `LifeOS_HQ` conversation exposed only 11 rendered turns, demonstrating that ChatGPT already virtualized the old DOM.
- Edge Task Manager showed JavaScript memory as roughly half the renderer footprint during connector-heavy and coding work.
- The extension did not address the demonstrated primary memory pressure and should remain disabled unless a future page actually mounts excessive old DOM.

### Phase 2e: Cross-department owning-HQ destination resolution

Merged through PR #15.

- Merge commit: `83c309f651de0354982fcd6cbb68f9cf3251d6a3`
- Supported department destinations derive from the canonical executable title map.
- Only explicit known aliases and exact canonical title overrides are accepted.
- Non-Engineering wakes require a department-owned Markdown review procedure under the owning department's project subtree.
- Hub routing, unknown departments, wrong-title overrides, unsafe paths, cross-owner procedures, and Worker courier wakes to `Chief_of_Staff_HQ` fail closed.
- Existing pause, execution-lock, duplicate-suppression, immutable-review, and send-confirmation gates remain unchanged.
- Destination resolution alone creates no Worker, private route, schedule, send, database state, or authority.

### Phase 2f: Persisted shared safety-pause triggers

Merged through PR #16.

- Merge commit: `3bf20ca231b3b5fbb1c315b24881e46939b3b508`
- One singleton record in the existing Command Center database persists the shared pause across service instances and dashboard restarts.
- Manual Pause, safety trips, status reporting, and explicit Resume use the same authoritative state.
- The first unresolved safety incident is preserved rather than overwritten by a later manual pause.
- Worker and owning-HQ confirmed-send paths trip the pause before releasing the shared lock on genuine uncertainty or evidence failure.
- Deterministic pre-send stops remain local and do not disable unrelated automation.
- Optional scheduler startup occurs only after the persisted pause store is initialized.
- No automatic recovery or time-based uncertainty clearing exists.

### Phase 2g: Conservative global send budget

Merged through PR #17.

- Merge commit: `e1d297f1a2517490b3fb2a37298689c6db25bfb0`
- One manually reset epoch lives on the existing singleton Command Center control record.
- Worker dispatch and owning-HQ wake attempts use the same atomic counter and existing execution lock.
- The default limit is three, with a bounded configuration range of one through twenty.
- Deterministic pre-send holds do not consume budget.
- Exhaustion blocks before browser transport, records a held operation, and trips the existing shared pause.
- Reset is available only while paused, increments the epoch, and remains separate from Resume.
- Reservation evidence attaches to the existing execution row rather than creating a competing send ledger.
- Current usage, remaining attempts, epoch, and holds are visible in Command Center and Worker Operations.
- No live Worker or HQ wake occurred during implementation or validation.

## Validation Evidence

- Final consolidated pre-PR-13 local regression gate: `80 passed`.
- The regression set covered route capture, wrong-room refusal, stale revision refusal, duplicate-route refusal, single-row preservation, verification hold behavior, canary-only promotion, route drift refusal, authoritative database propagation, dashboard API/UI controls, runtime contracts, browser readiness, submission recovery, and post-navigation identity behavior.
- PR #13 targeted launcher harness: `5 passed`.
- PR #13 dashboard JavaScript syntax check passed.
- PR #14 core tests: `5 passed`; JavaScript syntax and JSON validation passed.
- PR #15 isolated harness: `21` resolver cases and `4` runtime-integration cases passed.
- PR #15 repository-native focused pytest and Ruff gates both passed before merge.
- PR #16 repository-native affected regression gate: `47 passed`.
- PR #16 focused Ruff gate passed after the import-line formatting repair.
- PR #17 repository-native focused pytest, affected regression, and Ruff gates passed.
- PR #17 dashboard smoke loaded the Worker Operations budget metric and guarded reset control cleanly. Node.js was unavailable, so no separate Node syntax claim is made.
- The repository had no automated workflow configured for PRs #13 through #17.
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
- Slices 1–3 created no non-Engineering Worker registry row or private route.
- No production safety pause was deliberately triggered during Slice 2 or Slice 3 validation.
- No production send-budget attempt was consumed during Slice 3 validation.

## Dashboard Startup State

The latest dashboard code on `main` includes PR #17 at merge commit `e1d297f1a2517490b3fb2a37298689c6db25bfb0` or later. Pull and restart the dashboard only when Rob is ready to load the merged code. Rob already confirmed the budget metric and reset control rendered cleanly during PR validation. The remaining dashboard smoke is a bounded route-state, persisted-pause, send-budget, and guarded-control observation, not permission to configure or test a non-Engineering wake.

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

Do not recreate completed Package D, Package E, Package F Wave 0A, or Wave 0B Slices 1–3 as active tasks.

## Advisory State

Open Engineering advisories: None.

Recently closed:

- `ADV-20260723-052` closed after the hourly `Chief_of_Staff_HQ` watcher reported in the existing Chief of Staff conversation without creating a new chat or triggering work; Rob confirmed the result and authorized closure.
- `ADV-20260718-042` closed by the Chief of Staff source owner after Engineering implementation, source verification, and Rob approval for slow rollout. Slow rollout is an operational pacing decision, not unfinished Engineering implementation.

## Next Valid Action

Begin Package F Wave 0B Slice 4 with a read-only implementation inspection:

1. read the canonical Worker execution and communication contracts and identify every explicit activation prerequisite;
2. inspect the current Worker profile and procedure schemas without creating department-owned artifacts;
3. inspect registry, deployment, exact route, route revision, route availability, receiver, and unresolved-hold evidence;
4. inspect owning-HQ destination and review-procedure requirements;
5. inspect shared pause and send-budget readiness without resetting or resuming either control;
6. define profile, authority scope, tool scope, evidence, review, retirement, and rejection checks;
7. emit one deterministic prerequisite report with explicit PASS, HOLD, or NOT_APPLICABLE findings and source pointers;
8. prove the validator cannot mutate a Worker, route, procedure, deployment state, schedule, advisory, permission, or runtime authorization;
9. keep live activation, non-Engineering Worker registration, route configuration, sends, and unattended schedules out of this slice.

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
- Confirmed or uncertain submissions are not retried blindly.
- Immutable Git evidence outranks stale local transport state.
- Worker reports remain evidence until deterministic ingestion.
- `IMMEDIATE_HQ` work never auto-verifies.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Courier, ingester, dashboard, watcher, HQ receipt, and Rob receipt do not auto-close source advisories.
- The Worker courier never wakes `Chief_of_Staff_HQ` unless a separately authorized future contract explicitly changes that boundary.
- New Workers, connectors, recurring tasks, spending, cross-department rollout, or public actions require separate authority.

# Engineering_HQ Session Handoff

Updated: 2026-07-23
Project: Engineering_HQ
Purpose: Fresh-room handoff after the canonical title rollover, direct Worker URL routing, guarded dashboard route-management work, and advisory-state cleanup were completed.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering_HQ
- Current Phase: Active / Package D Closed / Package E Closed / Canonical Runtime Title Rollover Complete / Direct URL Routing Complete / Guarded Route Capture Complete / Fresh Chat Boot and Sync Complete / Post-Merge Dashboard Smoke Pending
- Primary Systems: GitHub, local LifeOS Dashboard, SQLite Command Center runtime state, ChatGPT Department and Worker rooms, Engineering advisory board, Advisory Index, and the local Edge CDP bridge
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
9. Read `coordination/WORKER_EXECUTION_CONTRACT.md` and `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` when Worker authority, reporting, verification, or execution behavior is in scope.
10. Perform a separate read-only Sync before any implementation write.
11. Keep connector, database, browser, and dashboard work small, explicit, fail-closed, and verifiable.

## Department Role

`Engineering_HQ` owns technical architecture, software planning, repository strategy, automation design, APIs and connectors, data models, testing, debugging, implementation sequencing, build-readiness, and truthful verification.

Engineering owns technical Worker infrastructure: exact routing, transport, logging, duplicate suppression, result ingestion, verification mechanics, runtime evidence, tests, and reliability safeguards. Engineering does not own shared Worker governance, another department's Worker authority, source-owner advisory lifecycle, or domain judgment.

Route business strategy to `Business_HQ` or `Office_Leaks_HQ`, cost-bearing choices to `Finance_HQ`, ordinary daily coordination to `Chief_of_Staff_HQ`, shared governance and global memory hygiene to `Maintenance_HQ`, and wellbeing or sustainability judgment to `Wellness_HQ`.

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

## Validation Evidence

- Final consolidated local regression gate: `80 passed`.
- The regression set covered route capture, wrong-room refusal, stale revision refusal, duplicate-route refusal, single-row preservation, verification hold behavior, canary-only promotion, route drift refusal, authoritative database propagation, dashboard API/UI controls, runtime contracts, browser readiness, submission recovery, and post-navigation identity behavior.
- PR #11 was mergeable before squash merge.

## Current Production Route State

- Worker ID: `engineering_worker`
- Exact chat title: `Engineering_Worker`
- Deployment state: `enabled`
- Route revision: `1`
- Route availability: `available`
- One authoritative registry row exists.
- The private exact conversation URL remains in ignored local SQLite state and is not duplicated into GitHub memory.
- Local Worker courier or orchestrator sends remain unauthorized unless Rob separately authorizes them.
- The separate `Chief_of_Staff_HQ` cloud watcher is not the local Worker courier and may remain enabled under its own authority.

## Dashboard Startup State

The fresh `Engineering_HQ` room completed canonical Boot and a separate read-only Sync on 2026-07-23. A post-merge local dashboard inspection has not yet been recorded, so the actual running process and UI state must still be verified rather than assumed.

Canonical local launch command from `apps/lifeos-dashboard`:

```cmd
call .venv\Scripts\activate.bat
python run_dashboard.py
```

Dashboard URL:

```text
http://127.0.0.1:8765
```

Starting the dashboard does not authorize a real Worker dispatch, route capture, route rollover, schedule creation, orchestrator activation, or advisory lifecycle change.

## Package State

### Package D

Lifecycle State: CLOSED

### Package E

Lifecycle State: CLOSED
Closed: 2026-07-23
Canonical closeout: `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Do not recreate completed Package D or Package E slices as active work.

## Advisory State

Open Engineering advisories: None.

Recently closed:

- `ADV-20260723-052` closed after the hourly `Chief_of_Staff_HQ` watcher reported in the existing Chief of Staff conversation without creating a new chat or triggering work; Rob confirmed the result and authorized closure.
- `ADV-20260718-042` closed by the Chief of Staff source owner after Engineering implementation, source verification, and Rob approval for slow rollout. Slow rollout is an operational pacing decision, not unfinished Engineering implementation.

## Next Valid Action

Perform the pending read-only post-merge dashboard smoke check:

1. Confirm local `main` is clean and contains merge commit `2587b540e24ca09036c1f0094187c69c2b363c63` or a later fast-forward.
2. Start or confirm the dashboard process.
3. Inspect `/api/health` and the Worker Operations page.
4. Confirm exactly one `engineering_worker` row is visible with title `Engineering_Worker`, route revision `1`, and availability `available`.
5. Confirm the guarded route-capture controls render.
6. Do not capture or roll the route unless a replacement Worker conversation actually exists and Rob explicitly chooses to change the route.
7. Do not run a live advisory or enable local unattended Worker sends without separate authorization.
8. Report the smoke-test result and then continue only from the remaining open loops.

## Production Boundary

- Browser automation acts only on exact canonical URLs.
- Registered exact Worker URLs, not sidebar visibility, are authoritative route locators.
- Route changes update one existing Worker row and must pass the zero-authority canary before becoming available.
- Confirmed or uncertain submissions are not retried blindly.
- Immutable Git evidence outranks stale local transport state.
- Worker reports remain evidence until deterministic ingestion.
- `IMMEDIATE_HQ` work never auto-verifies.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Courier, ingester, dashboard, watcher, HQ receipt, and Rob receipt do not auto-close source advisories.
- The Worker courier never wakes `Chief_of_Staff_HQ`.
- New Workers, connectors, recurring tasks, spending, cross-department rollout, or public actions require separate authority.

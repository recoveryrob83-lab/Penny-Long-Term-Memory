# Engineering_HQ Status

Updated: 2026-07-25

## Current Phase

Active / Package D Closed / Package E Closed / Package F Wave 0A Complete / Wave 0B Slices 1–3 Complete / Wave 0B Slice 4 Contract-Derived Activation Gate Started / Canonical Runtime Title Rollover Complete / Direct URL Routing Complete / Guarded Route Capture Complete / Browser Bridge Reconnect Merged / DOM Window Experiment Concluded

## Summary

`Engineering_HQ` owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, build-readiness, and truthful verification.

Engineering owns the Worker machinery: exact routing, stable IDs, direct browser transport, revision state, duplicate suppression, immutable result ingestion, report-repair mechanics, HQ and Rob receipt ingestion, runtime evidence, verification views, tests, and reliability safeguards. It does not own shared governance, another department's Worker authority, source-owner advisory lifecycle, or domain judgment.

## Source-of-Truth Boundaries

- GitHub: durable architecture, packages, procedures, profiles, advisories, decisions, and immutable result evidence.
- `projects/engineering/open_loops.md`: authoritative unfinished Engineering work.
- SQLite Command Center runtime state: sole operational ledger for dispatch, route state, result, repair, HQ review, Rob validation, consumption readiness, shared pause state, and send-budget accounting.
- Worker result folders: immutable evidence and audit trail, not a competing queue or lifecycle ledger.
- Dashboard and scheduled watcher: visibility and reporting interfaces, not independent truth or closure authority.
- `Maintenance_HQ`: canonical shared Worker governance and global operating integrity.
- `memory/HQ_NAMING_STANDARD.md`: canonical room-title and Worker-title source.

Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, private ChatGPT conversation URLs, or sensitive implementation details in GitHub memory or Worker result artifacts.

## Package F Roadmap State

### Wave 0A: Foundation

Lifecycle State: COMPLETE
Completed: 2026-07-23

Wave 0A now includes:

- the enabled GitHub-only Life OS Change Watch reporting meaningful signed changes into the existing `Chief_of_Staff_HQ` room and remaining silent when nothing changed;
- canonical eight-room naming and the `<Department_Name>_Worker` convention;
- repository-wide current-text reconciliation while preserving historical evidence and stable filesystem paths;
- the Engineering-only Worker execution, immutable result, owning-HQ review, Rob-validation, watcher-consumption, and duplicate-suppression proof chain;
- exact Worker URL routing, route revision state, guarded route capture, zero-authority route canary, and one-click browser bridge recovery.

Wave 0A completion does not activate any non-Engineering Worker, create a cross-department route, grant new connector or durable-write authority, or authorize unattended sends.

### Wave 0B: Controlled cross-department safety kernel

Lifecycle State: ACTIVE
Priority: High
Started: 2026-07-23

#### Slice 1: Cross-department owning-HQ destination resolution

Lifecycle State: COMPLETE
Completed: 2026-07-24
Merged PR: #15
Merge commit: `83c309f651de0354982fcd6cbb68f9cf3251d6a3`

Slice 1 derives owning-HQ destinations from the canonical executable title map, accepts only explicit known aliases, requires an owning-department review procedure, rejects cross-owner procedure paths, rejects Hub and Chief of Staff courier routing, and creates no Worker identity, private route, schedule, send, database state, or authority merely by resolving a destination.

Rob ran the repository-native merge gate. The focused pytest command and Ruff command both passed before PR #15 was marked ready and squash-merged.

#### Slice 2: Automatic shared safety-pause triggers

Lifecycle State: COMPLETE
Completed: 2026-07-24
Merged PR: #16
Merge commit: `3bf20ca231b3b5fbb1c315b24881e46939b3b508`

Slice 2 strengthens the existing shared Command Center pause rather than creating a second circuit-breaker state. One singleton record in the existing SQLite database now persists manual and safety pause state, reason, affected run ID, trigger, recovery condition, and timestamps across dashboard restarts. Worker dispatch and owning-HQ review wakes trip this same pause before releasing the shared execution lock only when a send may have occurred but cannot be reconciled, a claimed-success receipt is invalid, the browser cannot return to a verified source state, or confirmed-send evidence cannot be persisted.

Ordinary deterministic pre-send validation failures, unavailable routes, duplicate suppression, department review holds, and rejected work remain local. Resume is explicit and the first safety incident is preserved until human review.

Rob ran the repository-native gate. The affected regression set passed `47` tests and the focused Ruff gate passed before PR #16 was marked ready and squash-merged. No live Worker or HQ wake occurred.

#### Slice 3: Conservative global send budget

Lifecycle State: COMPLETE
Completed: 2026-07-25
Merged PR: #17
Merge commit: `e1d297f1a2517490b3fb2a37298689c6db25bfb0`

Slice 3 extends the existing singleton Command Center control record with one manually reset send-budget epoch. The default limit is three confirmed attempts, configurable from one through twenty. Worker dispatches and owning-HQ review wakes reserve atomically against the same budget under the existing execution lock immediately before browser transport.

Attempts remain consumed whether transport succeeds, fails safely, or becomes uncertain. Elapsed time and dashboard restart do not refill the budget. Deterministic pre-send route, duplicate, draft, and validation holds occur before reservation. Exhaustion blocks the next send before transport, records the held operation, and trips the existing shared pause. Reset is available only while paused, increments the epoch, and does not Resume automation or erase execution evidence.

Reservation evidence is appended to the existing authoritative Worker execution row rather than stored in a second ledger. Command Center and Worker Operations expose limit, usage, remaining attempts, epoch, and held-operation state. The zero-authority courier self-test remains outside this budget.

Rob ran both repository-native pytest gates and the focused Ruff gate successfully. Because Node.js was not installed locally, JavaScript syntax was not separately checked with Node; Rob instead loaded the dashboard and confirmed the Worker Operations budget UI rendered cleanly. No live Worker or HQ wake occurred.

#### Slice 4: Contract-derived activation gate

Lifecycle State: ACTIVE
Priority: High
Started: 2026-07-25

The next bounded slice must implement a read-only, fail-closed activation validator derived from the canonical Worker contracts and existing runtime evidence. It must verify the Worker profile, owning-department procedure, authority and tool scopes, evidence contract, registered route and revision state, owning-HQ review path, pause and send-budget gates, unresolved holds, and retirement rules before reporting whether activation prerequisites are satisfied.

The validator must not create or modify a Worker registry row, route, procedure, deployment state, schedule, advisory, permission, or runtime authorization. It must not become another deployment ledger or infer authority merely because technical prerequisites pass. Owning-department authority, Maintenance shared-governance review, and Rob's explicit decision remain separate requirements.

## Completed Runtime Repair Chain

### Canonical title rollover and courier verifier repair

Completed and merged through PR #9.

- Merge commit: `f8cc341e17cb68492c5f66339382b753bd1612ab`
- Engineering executable surfaces use the canonical underscore room titles.
- Active title-bearing SQLite state was migrated idempotently.
- Stable destination keys, IDs, paths, historical rows, immutable evidence, and checksums were preserved.
- Post-navigation identity no longer depends on selected-room sidebar visibility after exact URL navigation.
- Virtualized-history submission witnesses were repaired without weakening fail-closed behavior.

### Authoritative direct Worker URL routing

Completed and merged through PR #10.

- Merge commit: `b859c3c72e8b82f876b9ebf72d2961f4eb33ecbd`
- The existing Worker registry row stores the exact conversation URL and monotonic route revision.
- Browser dispatch uses the registered exact URL only and fails closed when it is absent or invalid.
- The existing production `engineering_worker` row was migrated in place.
- A zero-authority live canary succeeded and the route was promoted to `available`.

### Guarded dashboard route capture and rollover

Completed and merged through PR #11.

- Merge commit: `2587b540e24ca09036c1f0094187c69c2b363c63`
- The dashboard can capture the sole active ChatGPT Worker conversation without manual URL pasting.
- Capture requires paused automation, the shared lock, explicit confirmation, current route revision, exactly one conversation target, correct Worker title, and no duplicate ownership.
- Changed routes update one existing row, increment the revision, and remain on `unknown` hold until a zero-authority canary verifies the exact unchanged revision.
- Real advisory execution remains blocked unless route availability is exactly `available`.
- Capture and canary use the dashboard's exact active SQLite database.
- No production route rollover occurred during implementation.

### One-click Edge browser bridge reconnect

Completed and merged through PR #13.

- Merge commit: `0a1223c5f32df17fb22f11cb53d0badd5ef2a1ab`
- The dashboard exposes **Reconnect bridge** when the local Edge CDP endpoint is offline.
- The endpoint launches a dedicated persistent local Edge profile on loopback `127.0.0.1:9222` and verifies `/json/version` before reporting Ready.
- The launcher refuses non-loopback endpoints, duplicate launch while already healthy, and launch while another automation action holds the shared execution lock.
- Reconnect does not mutate Worker routes, advisories, schedules, runtime execution history, or Worker authority.
- Targeted launcher harness: `5 passed`; dashboard JavaScript syntax check passed.
- Live Windows/dashboard route-state validation remains pending as a bounded observation, although Rob successfully closed and relaunched the dedicated Edge window during the memory investigation.

### Opt-in ChatGPT DOM Window Edge extension

Package merged through PR #14; memory experiment concluded as ineffective for the observed problem.

- Merge commit: `131cf5d10a4a13cc76c30f99a09cefe75f4306c9`
- The inert Manifest V3 package lives at `apps/chatgpt-dom-window-extension` and requires manual Edge sideloading.
- It is disabled by default, scoped per exact saved conversation, and blocks canonical `*_Worker` rooms.
- Static validation passed.
- Live inspection of the long `LifeOS_HQ` conversation showed only `11` rendered turns, so ChatGPT was already virtualizing old conversation DOM and the extension had nothing useful to trim.
- Edge Task Manager showed JavaScript memory accounting for roughly half of the observed renderer usage during connector-heavy and coding work.
- The extension therefore does not address the demonstrated primary memory pressure. It remains optional and should stay disabled unless a future page actually mounts enough old DOM to justify it.

### Cross-department owning-HQ destination resolution

Completed and merged through PR #15.

- Merge commit: `83c309f651de0354982fcd6cbb68f9cf3251d6a3`
- The resolver reuses the canonical executable room-title map instead of maintaining a competing destination map.
- Maintenance, Engineering, Business, Office Leaks, Finance, and Wellness resolve only through explicit known aliases and exact canonical titles.
- Non-Engineering wakes remain held until an owning-department Markdown review procedure is registered under that department's project subtree.
- `LifeOS_HQ`, unknown departments, wrong-title overrides, unsafe paths, cross-owner procedure paths, and Worker courier wakes to `Chief_of_Staff_HQ` fail closed.
- The runtime hook replaces only the old Engineering-only destination gate; existing pause, execution-lock, duplicate-suppression, immutable-review, and send-confirmation behavior remains in place.
- No live non-Engineering wake or route registration occurred.

### Persisted shared safety-pause triggers

Completed and merged through PR #16.

- Merge commit: `3bf20ca231b3b5fbb1c315b24881e46939b3b508`
- One `command_center_control` singleton in the existing Command Center SQLite database persists the shared pause across restarts.
- Manual pause, automatic safety trip, status reporting, and explicit resume use the same authoritative record.
- Safety trips persist a concise reason, affected run ID, trigger, recovery condition, and timestamps.
- Worker and owning-HQ send paths trip before releasing the shared execution lock on true post-send uncertainty, invalid claimed-success receipts, unknown browser return state, unclassified confirmed-send exceptions, or evidence-persistence failure.
- Ordinary deterministic pre-send failures remain local and do not become a global outage.
- No automatic recovery exists, and a later manual pause cannot overwrite the first unresolved safety incident.
- No live Worker or HQ wake occurred during implementation or validation.

### Conservative global send budget

Completed and merged through PR #17.

- Merge commit: `e1d297f1a2517490b3fb2a37298689c6db25bfb0`
- One manually reset budget epoch lives on the existing singleton Command Center control record.
- Confirmed Worker dispatch and owning-HQ wake attempts draw from the same atomic counter under the existing execution lock.
- The default limit is three, with a bounded configuration range of one through twenty.
- Deterministic pre-send holds do not consume budget.
- Exhaustion blocks before transport, records a held operation, and trips the existing shared pause.
- Reset requires explicit confirmation while paused, increments the epoch, and remains separate from Resume.
- Reservation evidence attaches to the existing execution row rather than creating a second ledger.
- Usage, remaining attempts, epoch, and holds are visible in Command Center and Worker Operations.
- No live Worker or HQ wake occurred during implementation or validation.

## Validation

- Final consolidated pre-PR-13 local regression gate: `80 passed`.
- Coverage included route capture, stale revision refusal, wrong-room refusal, duplicate-route refusal, single-row preservation, verification holds, canary-only promotion, route-drift refusal, authoritative database propagation, dashboard API/UI contracts, runtime validation, browser readiness, submission recovery, and post-navigation identity.
- PR #13 added focused launcher, API, and UI tests. The targeted launcher harness passed and the new JavaScript parsed cleanly; no repository workflow was configured on that PR.
- PR #14 core test suite: `5 passed`.
- PR #14 JavaScript syntax and JSON validation passed, but the live measurement rejected DOM volume as the primary cause of the observed memory growth.
- PR #15 isolated execution evidence: 21 resolver tests and 4 runtime-integration tests passed on 2026-07-24.
- PR #15 repository-native focused pytest and Ruff gates both passed under Rob's local dashboard environment before merge.
- PR #16 repository-native affected regression gate: `47 passed`.
- PR #16 focused Ruff gate passed after the package import formatting repair.
- PR #17 repository-native focused pytest, affected regression, and Ruff gates passed.
- PR #17 dashboard smoke loaded the Worker Operations budget metric and guarded reset control cleanly. Node.js was unavailable, so no separate Node syntax claim is made.

## Current Production Route State

- Worker ID: `engineering_worker`
- Chat title: `Engineering_Worker`
- Deployment state: `enabled`
- Route revision: `1`
- Availability: `available`
- Registry rows for this Worker: one authoritative row
- Private exact URL: retained only in ignored local SQLite state
- Local Worker courier or orchestrator sends: not authorized unless Rob separately authorizes them
- Separate `Chief_of_Staff_HQ` cloud watcher: governed by its own authorization and not equivalent to the local Worker courier
- Non-Engineering Worker registry rows or private routes created by Slices 1–3: none
- Production safety pause deliberately triggered during Slice 2 or Slice 3 validation: no
- Production send-budget attempts consumed during Slice 3 validation: none

## Package State

### Package D

Lifecycle State: CLOSED

Package D established the Worker registry, routing, transport, receiver, verification, duplicate-suppression, and bounded operational-pilot foundation.

### Package E

Lifecycle State: CLOSED
Priority: Normal
Closed: 2026-07-23
Canonical closeout: `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Package E completed the Engineering-only dispatch, immutable result, deterministic ingestion, report repair, HQ review, Rob validation, signed consumption, watcher reporting, and duplicate-suppression chain.

Cross-department adoption, universal Worker durable-write authority, optional human-readable envelopes, and broader unattended packaging remain deferred.

## Advisory State

Open Engineering advisories: None.

Recently closed:

- `ADV-20260723-052` closed after the hourly watcher reported in the existing `Chief_of_Staff_HQ` conversation without creating a new chat or triggering work; Rob confirmed the result and authorized closure.
- `ADV-20260718-042` closed by the Chief of Staff source owner after Engineering implementation, source verification, and Rob approval for slow rollout. Slow rollout is an operational pacing decision, not unfinished implementation.

## Dashboard State

The latest dashboard code on `main` includes PR #17 at merge commit `e1d297f1a2517490b3fb2a37298689c6db25bfb0` or later.

Expected local endpoint:

```text
http://127.0.0.1:8765
```

Starting or reconnecting the dashboard browser bridge does not authorize real Worker dispatch, route capture, route rollover, schedules, activation, or unattended local orchestrator sends.

## Current Work

Package F Wave 0B Slices 1–3 are complete and must not be recreated as active work.

The immediate Engineering implementation is Slice 4: contract-derived activation gate. Begin with a read-only inspection of the canonical Worker execution and communication contracts, current Worker profile and procedure schemas, runtime registry and route checks, owning-HQ review requirements, pause and send-budget status, unresolved hold evidence, and retirement behavior. Define one fail-closed prerequisite report that reads existing truth and cannot activate or mutate anything.

All further work comes from `projects/engineering/open_loops.md`, a demonstrated defect with bounded repair authority, or a new explicit Rob instruction.

## Production Boundary

- Browser automation acts only on exact canonical URLs.
- The registered exact URL is the authoritative Worker locator; sidebar visibility is not route identity.
- Route rollover updates one existing row and must pass a zero-authority canary before availability.
- Browser bridge reconnect is a local transport-recovery action only and cannot mutate route identity or authorize execution.
- Cross-department destination resolution is not Worker activation, route registration, permission expansion, scheduling, or dispatch authority.
- The persisted shared safety pause is the only circuit-breaker state and requires explicit human resume.
- The persisted send budget is one manually reset epoch shared by Worker dispatch and owning-HQ wake attempts; elapsed time never refills it.
- Resetting the send budget does not Resume automation, erase safety incidents, or authorize a send.
- The activation validator may report prerequisites only. It may not create authority, mutate deployment state, or replace owning-department, Maintenance, or Rob approval.
- The DOM Window extension is optional, disabled by default, and not a solution to the demonstrated JavaScript-heavy memory growth.
- Confirmed or uncertain sends are not retried blindly.
- Immutable Git evidence outranks stale local transport state.
- Any unrecognized post-submit state fails closed and requires human inspection.
- Worker reports remain evidence until deterministic ingestion.
- `IMMEDIATE_HQ` work never auto-verifies.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Courier, ingester, dashboard, watcher, HQ receipt, and Rob receipt do not auto-close source advisories.
- The Worker courier never wakes `Chief_of_Staff_HQ` unless a separately authorized future contract explicitly changes that boundary.
- Cross-department rollout, new recurring tasks, connectors, spending, or public actions require separate authority.

## Boundary

`Engineering_HQ` owns the machinery. Rob decides. Department HQs own their Workers and judgment. `Maintenance_HQ` owns shared governance. Source owners close their own records.

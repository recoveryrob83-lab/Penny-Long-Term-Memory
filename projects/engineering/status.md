# Engineering_HQ Status

Updated: 2026-07-23

## Current Phase

Active / Package D Closed / Package E Closed / Package F Wave 0A Complete / Package F Wave 0B Cross-Department HQ Routing Started / Canonical Runtime Title Rollover Complete / Direct URL Routing Complete / Guarded Route Capture Complete / Browser Bridge Reconnect Merged / DOM Window Experiment Concluded

## Summary

`Engineering_HQ` owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, build-readiness, and truthful verification.

Engineering owns the Worker machinery: exact routing, stable IDs, direct browser transport, revision state, duplicate suppression, immutable result ingestion, report-repair mechanics, HQ and Rob receipt ingestion, runtime evidence, verification views, tests, and reliability safeguards. It does not own shared governance, another department's Worker authority, source-owner advisory lifecycle, or domain judgment.

## Source-of-Truth Boundaries

- GitHub: durable architecture, packages, procedures, profiles, advisories, decisions, and immutable result evidence.
- `projects/engineering/open_loops.md`: authoritative unfinished Engineering work.
- SQLite Command Center runtime state: sole operational ledger for dispatch, route state, result, repair, HQ review, Rob validation, and consumption readiness.
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

The first bounded slice is cross-department owning-HQ route resolution. It must reuse canonical names, remain fail-closed for unknown departments or invalid overrides, and create no Worker identity or route merely by resolving a destination. Global automatic pause triggers, send budgets, and contract-derived activation validation remain later Wave 0B slices rather than being silently bundled into the first routing change.

## Completed Runtime Repair Chain

### Canonical title rollover and courier verifier repair

Completed and merged through PR #9.

- Merge commit: `f8cc341e17cb68492c5f66339382b753bd1612ab`
- Engineering executable surfaces use the canonical underscore room titles.
- Active title-bearing SQLite state was migrated idempotently.
- Stable keys, IDs, paths, historical rows, immutable evidence, and checksums were preserved.
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

## Validation

- Final consolidated pre-PR-13 local regression gate: `80 passed`.
- Coverage included route capture, stale revision refusal, wrong-room refusal, duplicate-route refusal, single-row preservation, verification holds, canary-only promotion, route-drift refusal, authoritative database propagation, dashboard API/UI contracts, runtime validation, browser readiness, submission recovery, and post-navigation identity.
- PR #13 added focused launcher, API, and UI tests. The targeted launcher harness passed and the new JavaScript parsed cleanly; no repository workflow was configured on that PR.
- PR #14 core test suite: `5 passed`.
- PR #14 JavaScript syntax and JSON validation passed, but the live measurement rejected DOM volume as the primary cause of the observed memory growth.

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

The latest dashboard reconnect code is on `main` at merge `0a1223c5f32df17fb22f11cb53d0badd5ef2a1ab` or later.

Expected local endpoint:

```text
http://127.0.0.1:8765
```

Starting or reconnecting the dashboard browser bridge does not authorize real Worker dispatch, route capture, route rollover, schedules, or unattended local orchestrator sends.

## Current Work

The canonical title rollover, courier verifier repair, direct URL routing, guarded route-management implementation, browser bridge reconnect implementation, Package F Wave 0A foundation, and DOM-memory investigation are complete and are no longer open code loops.

The immediate Engineering implementation is Package F Wave 0B Slice 1: controlled cross-department owning-HQ destination resolution. The slice must:

1. derive supported department HQ titles from the canonical executable mapping rather than maintaining a competing title map;
2. normalize only explicit known department aliases;
3. allow exact environment overrides only when they resolve to a canonical department HQ title;
4. fail closed for unknown departments, Hub routing, malformed overrides, or destinations outside the canonical department set;
5. preserve all existing Engineering route, report, review, and duplicate-suppression behavior;
6. create no Worker, route, schedule, advisory, or authority by resolving a title;
7. remain a draft implementation until focused tests and review are complete.

All further work comes from `projects/engineering/open_loops.md`, a demonstrated defect with bounded repair authority, or a new explicit Rob instruction.

## Production Boundary

- Browser automation acts only on exact canonical URLs.
- The registered exact URL is the authoritative Worker locator; sidebar visibility is not route identity.
- Route rollover updates one existing row and must pass a zero-authority canary before availability.
- Browser bridge reconnect is a local transport-recovery action only and cannot mutate route identity or authorize execution.
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

# Engineering_HQ Status

Updated: 2026-07-23

## Current Phase

Active / Package D Closed / Package E Closed / Canonical Runtime Title Rollover Complete / Direct URL Routing Complete / Guarded Route Capture Complete / Fresh Chat Boot and Sync Complete / Post-Merge Dashboard Smoke Pending

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

## Validation

- Final consolidated local regression gate: `80 passed`.
- Coverage included route capture, stale revision refusal, wrong-room refusal, duplicate-route refusal, single-row preservation, verification holds, canary-only promotion, route-drift refusal, authoritative database propagation, dashboard API/UI contracts, runtime validation, browser readiness, submission recovery, and post-navigation identity.

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

The completed dashboard code is on `main` and ready for local launch or restart.

Expected local endpoint:

```text
http://127.0.0.1:8765
```

This fresh `Engineering_HQ` room completed canonical Boot and a separate read-only Sync on 2026-07-23. A post-merge local dashboard smoke result has not yet been recorded, so the actual running process and UI state must still be verified rather than assumed.

Starting the dashboard does not authorize real Worker dispatch, route capture, route rollover, schedules, or unattended local orchestrator sends.

## Current Work

The canonical title rollover, courier verifier repair, direct URL routing, and guarded route-management implementation are complete and are no longer open loops.

The immediate Engineering task is the pending read-only post-merge dashboard smoke check:

1. confirm local `main` is clean and contains `2587b540e24ca09036c1f0094187c69c2b363c63` or later;
2. start or confirm the dashboard;
3. verify health and Worker Operations;
4. confirm one `engineering_worker` route at revision `1` and availability `available`;
5. confirm guarded route controls render;
6. do not capture or change the route without an actual replacement room and explicit authorization.

All further work comes from `projects/engineering/open_loops.md`, a demonstrated defect with bounded repair authority, or a new explicit Rob instruction.

## Production Boundary

- Browser automation acts only on exact canonical URLs.
- The registered exact URL is the authoritative Worker locator; sidebar visibility is not route identity.
- Route rollover updates one existing row and must pass a zero-authority canary before availability.
- Confirmed or uncertain sends are not retried blindly.
- Immutable Git evidence outranks stale local transport state.
- Any unrecognized post-submit state fails closed and requires human inspection.
- Worker reports remain evidence until deterministic ingestion.
- `IMMEDIATE_HQ` work never auto-verifies.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Courier, ingester, dashboard, watcher, HQ receipt, and Rob receipt do not auto-close source advisories.
- The Worker courier never wakes `Chief_of_Staff_HQ`.
- Cross-department rollout, new recurring tasks, connectors, spending, or public actions require separate authority.

## Boundary

`Engineering_HQ` owns the machinery. Rob decides. Department HQs own their Workers and judgment. `Maintenance_HQ` owns shared governance. Source owners close their own records.

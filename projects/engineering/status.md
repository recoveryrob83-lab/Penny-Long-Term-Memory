# Engineering_HQ Status

Updated: 2026-07-25

## Current Phase

Active / Package D Closed / Package E Closed / Package F Wave 0A Complete / Package F Wave 0B Complete / Maintenance Worker GitHub Rollout Prepared / Maintenance Route Linkage Pending

## Summary

`Engineering_HQ` owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, build-readiness, and truthful verification.

Engineering owns Worker machinery: exact routing, stable IDs, direct browser transport, route revisions, duplicate suppression, immutable result ingestion, report repair, HQ and Rob receipt ingestion, runtime evidence, activation-prerequisite reporting, verification views, tests, and reliability safeguards. It does not own shared governance, another department's Worker authority, source-owner advisory lifecycle, or domain judgment.

## Source-of-Truth Boundaries

- GitHub holds durable architecture, profiles, procedures, packages, decisions, advisories, and immutable Worker evidence.
- `projects/engineering/open_loops.md` is the authoritative list of unfinished Engineering work.
- SQLite Command Center state is the sole operational ledger for Worker registry, routes, dispatch, results, repair, HQ review, Rob validation, consumption readiness, shared pause, and send-budget accounting.
- Private ChatGPT conversation URLs remain only in ignored local runtime state.
- Dashboard views and scheduled watchers provide visibility and transport, not independent truth or closure authority.
- `Maintenance_HQ` owns shared Worker governance and global operating integrity.
- Department HQs own their Worker profiles, purpose, authority, holds, verification judgment, and retirement.

Never store secrets, credentials, tokens, private account details, medical details, private user data, private ChatGPT conversation URLs, or sensitive implementation details in GitHub memory or Worker result artifacts.

## Publication Context

The room-specific Engineering handbook and the other LifeOS handbooks are published through Project Sources as noncanonical context mirrors. They support ordinary continuity but do not replace GitHub, grant write authority, or control consequential current-state claims. Fetch current canonical sources before writes, route changes, runtime claims, or new package decisions.

## Completed Package State

### Package D

Lifecycle State: CLOSED

Established the Worker registry, routing, browser transport, semantic receiver, duplicate suppression, verification mechanics, and bounded pilot foundation.

### Package E

Lifecycle State: CLOSED
Closed: 2026-07-23
Canonical closeout: `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Proved the Engineering-only chain for dispatch, immutable result artifacts, deterministic ingestion, report repair, owning-HQ review, Rob validation when required, consumption readiness, watcher reporting, and duplicate suppression.

### Package F Wave 0A

Lifecycle State: COMPLETE
Completed: 2026-07-23

Established canonical room and Worker naming, exact Worker URL routing, route revision state, guarded route capture, zero-authority canary behavior, and browser-bridge recovery.

### Package F Wave 0B

Lifecycle State: COMPLETE
Started: 2026-07-23
Completed: 2026-07-25

Wave 0B delivered the controlled cross-department safety kernel:

1. PR #15, merge `83c309f651de0354982fcd6cbb68f9cf3251d6a3`: canonical owning-HQ destination resolution with department-owned review-procedure enforcement.
2. PR #16, merge `3bf20ca231b3b5fbb1c315b24881e46939b3b508`: one persisted shared safety pause with fail-closed automatic triggers.
3. PR #17, merge `e1d297f1a2517490b3fb2a37298689c6db25bfb0`: one conservative manually reset global send-budget epoch shared by Worker and HQ wake attempts.
4. PR #18, merge `4a00c4908cfd71a2b2ebfe41c084b68a5d2907e5`: read-only contract-derived activation prerequisite reports that always return `activation_authorized: false`.

Rob confirmed the post-merge dashboard smoke passed: health and Worker Operations were ready, the Engineering Worker was available, the browser bridge and execution gate were active, and no review was pending.

## Maintenance Worker Rollout

Lifecycle State: GITHUB PREREQUISITES COMPLETE / ROUTE LINKAGE PENDING
Priority: High
Approval: Rob reports Wave 0B governance passed and creation of `Maintenance_Worker` is approved.
Merged PR: #19
Merge commit: `28a7a4fc40317d043dbe9983747475f85d37742a`

PR #19 added:

- `projects/life-logistics-hq/workers/maintenance_worker.md`;
- `projects/life-logistics-hq/procedures/maintenance_worker_result_submission.md`;
- `projects/life-logistics-hq/procedures/maintenance_hq_worker_review_receipt.md`;
- the canonical default Maintenance HQ review-procedure path in the Engineering routing resolver;
- canonical activation-readiness tests for Engineering and Maintenance;
- explicit machine-readable receiver authority for the Maintenance profile.

The initial Maintenance profile is manually dispatched and read-only except for creation of one exact immutable machine-result artifact. It permits only `read_only_verification` and `read_only_governance_audit`, requires `IMMEDIATE_HQ`, and grants no standing repair, reconciliation, publication-write, department-write, connector, schedule, route, runtime-control, or unattended-execution authority.

Rob reported the focused pytest, affected regression, and Ruff gates passed before PR #19 was merged. No GitHub Actions workflow was configured for this merge, so Rob's native results are the validation evidence.

## Current Runtime State

### Engineering Worker

- Worker ID: `engineering_worker`
- Chat title: `Engineering_Worker`
- Deployment state: `enabled`
- Route revision: `1`
- Route availability: `available`
- Registry rows: one authoritative row
- Private exact URL: local runtime state only

### Maintenance Worker

- Canonical Worker ID: `maintenance_worker`
- Canonical chat title: `Maintenance_Worker`
- Canonical profile and procedures: present on `main`
- ChatGPT Worker room: not yet created or verified by Engineering
- Runtime registry row: not yet verified
- Exact private route: not yet linked
- Route revision and availability: not yet established
- Zero-authority canary: pending
- Activation-readiness inspection against live runtime state: pending
- Real pilot assignment or dispatch: not authorized by route linkage alone

## Validation Evidence

- Pre-PR-13 consolidated regression gate: `80 passed`.
- PR #13 launcher harness: `5 passed`; dashboard JavaScript syntax passed.
- PR #14 core tests: `5 passed`; JavaScript syntax and JSON validation passed.
- PR #15 repository-native focused pytest and Ruff passed.
- PR #16 affected regression gate: `47 passed`; focused Ruff passed.
- PR #17 focused pytest, affected regressions, and Ruff passed; Worker Operations budget UI loaded cleanly.
- PR #18 focused activation-readiness tests, affected regressions, and Ruff passed.
- PR #19 focused routing/profile/readiness tests, affected regressions, and Ruff passed according to Rob's native environment.
- Live evidence, not static test success, controls claims about exact route identity, route availability, browser execution, and external action success.

## Current Work

The active bounded rollout sequence is:

1. Rob creates the exact `Maintenance_Worker` ChatGPT room.
2. Rob links it through Worker Operations using the guarded mechanism.
3. Engineering verifies exactly one `maintenance_worker` registry row with the canonical profile path and version.
4. Engineering verifies the exact private route, positive route revision, and expected initial route hold.
5. Engineering runs the existing zero-authority canary against the unchanged route revision.
6. Engineering inspects the read-only activation report and confirms `activation_authorized: false` regardless of technical readiness.
7. A first real Maintenance assignment requires its own exact authority, task class, sources, result path, and `IMMEDIATE_HQ` verification path.

Do not dispatch real work, wake Maintenance HQ, create a schedule, reset the send budget, pause or resume automation, or infer assignment authority merely from successful chat creation, route linkage, canary success, or a technically ready report.

## Advisory State

Open Engineering advisories: None.

`ADV-20260718-042`, `ADV-20260719-044`, and `ADV-20260723-052` are closed and must not be recreated as active work.

## Production Boundary

- Browser automation acts only on exact canonical URLs.
- One existing Worker row is authoritative for each stable Worker ID.
- Route changes require a revision increment, an initial hold, and a zero-authority canary before availability.
- The shared safety pause is the only circuit-breaker state and requires explicit human resume.
- The send budget is one manually reset epoch; elapsed time never refills it and Reset does not Resume.
- The activation validator reports prerequisites only. `READY_FOR_AUTHORITY_REVIEW` is not activation approval.
- Confirmed or uncertain sends are never blind-retried.
- Immutable Git evidence outranks stale local transport state.
- `IMMEDIATE_HQ` work never auto-verifies.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Courier, dashboard, ingester, watcher, HQ receipt, and Rob receipt do not close source work automatically.
- The Worker courier does not wake `Chief_of_Staff_HQ` under the current contract.
- Additional Workers, recurring tasks, connectors, spending, public actions, or broader durable-write authority require separate owner review and authorization.

## Boundary

`Engineering_HQ` owns the machinery. Rob decides. Department HQs own their Workers and judgment. `Maintenance_HQ` owns shared governance. Source owners close their own records.

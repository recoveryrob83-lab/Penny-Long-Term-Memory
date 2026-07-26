# Engineering_HQ Status

Updated: 2026-07-26

## Current Phase

Active / Package D Closed / Package E Closed / Package F Waves 0A and 0B Complete / Maintenance Worker Route Verified / Composer Residue Repair Pending Merge / Office Leaks Paused / Business Worker Candidate Waiting

## Summary

`Engineering_HQ` owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, build-readiness, and truthful verification.

Engineering owns Worker machinery: exact routing, stable IDs, direct browser transport, route revisions, duplicate suppression, immutable result ingestion, report repair, HQ and Rob receipt ingestion, runtime evidence, activation-prerequisite reporting, verification views, tests, and reliability safeguards. It does not own shared governance, another department's Worker authority, source-owner advisory lifecycle, business strategy, or domain judgment.

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
Completed: 2026-07-25

Delivered the controlled cross-department safety kernel:

1. PR #15, merge `83c309f651de0354982fcd6cbb68f9cf3251d6a3`: canonical owning-HQ destination resolution.
2. PR #16, merge `3bf20ca231b3b5fbb1c315b24881e46939b3b508`: one persisted shared safety pause with fail-closed automatic triggers.
3. PR #17, merge `e1d297f1a2517490b3fb2a37298689c6db25bfb0`: one conservative manually reset global send-budget epoch.
4. PR #18, merge `4a00c4908cfd71a2b2ebfe41c084b68a5d2907e5`: read-only contract-derived activation prerequisite reports that always return `activation_authorized: false`.

Rob confirmed the post-merge dashboard smoke passed.

## Maintenance Worker Rollout

Lifecycle State: ROUTE VERIFIED / ACTIVATION NOT AUTHORIZED
Priority: High

Canonical prerequisites:

- PR #19 merged as `28a7a4fc40317d043dbe9983747475f85d37742a`.
- PR #20 merged as `e91783dd9705df4a090eae2b4414adead6dafcf4`.
- Canonical profile: `projects/life-logistics-hq/workers/maintenance_worker.md`.
- Canonical result procedure: `projects/life-logistics-hq/procedures/maintenance_worker_result_submission.md`.
- Canonical HQ review procedure: `projects/life-logistics-hq/procedures/maintenance_hq_worker_review_receipt.md`.

Rob reports the following live local state:

- one registered `maintenance_worker` row;
- exact ChatGPT title `Maintenance_Worker`;
- route revision `1`;
- successful zero-authority browser round trip;
- successful return to Engineering;
- route availability promoted to `available`.

This proves the registered route and browser transport. It does not authorize activation, a real Maintenance assignment, Maintenance HQ wake, schedules, budget reset, unattended execution, or broader write authority.

The next Maintenance step is a read-only activation-readiness inspection. A first real assignment still requires separately exact authority, one allowed task class, source references, read scopes, one immutable result path, authorization source, and `IMMEDIATE_HQ` verification.

## Composer Residue Repair

Lifecycle State: IMPLEMENTED AND NATIVELY VALIDATED / PR OPEN
Priority: Normal

During the successful Maintenance canary, ChatGPT restored the already-submitted synthetic prompt in the Worker composer after the transport had confirmed the new user turn and returned to Engineering. Rob manually removed the residue.

Draft PR #21, `Clear proven stale Worker composer residue`, is open on `engineering/worker-composer-residue-fix` at head `132ba74e24911b429a762a7d0f994ac7aeab647b`.

The repair:

- reuses an exact current-run draft;
- preserves unrelated user text;
- recognizes only canonical `LIFEOS_EXECUTION_WRAPPER=` drafts with nonempty `wrapper_id` and `run_id`;
- clears an older LifeOS draft only when both IDs already occur together in one submitted user turn;
- preserves malformed or unproven residue and sends nothing.

Rob reports focused tests, affected regressions, and Ruff pass. PR #21 remains draft and unmerged, so the repair is not yet on `main`. No live canary rerun is needed or authorized merely to test this fix.

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

- Worker ID: `maintenance_worker`
- Chat title: `Maintenance_Worker`
- Canonical profile and procedures: present on `main`
- Registry and exact route: user-reported complete
- Route revision: user-reported `1`
- Zero-authority canary: user-reported successful
- Route availability: user-reported `available`
- Activation authorization: none
- Real pilot assignment: none

### Business Worker Candidate

- Owning department candidate: `Business_HQ`
- Business direction: AI systems services for solo developers and small teams
- Profile, procedures, stable Worker ID, chat title, room, registry row, route, canary, activation, schedule, and first assignment: not yet defined or authorized

### Office Leaks

- Business state: paused by Rob
- Office Leaks Worker rollout: paused
- Existing Office Leaks records remain owned by `Office_Leaks_HQ` and must not be repurposed as competing truth for the AI systems business

## Validation Evidence

- Pre-PR-13 consolidated regression gate: `80 passed`.
- PR #13 launcher harness: `5 passed`; dashboard JavaScript syntax passed.
- PR #14 core tests: `5 passed`; JavaScript syntax and JSON validation passed.
- PRs #15 through #20 passed the available native focused pytest, affected regression, and Ruff gates as reported by Rob.
- PR #21 focused composer tests, affected regressions, and Ruff passed as reported by Rob.
- Live evidence, not static test success, controls claims about exact route identity, route availability, browser execution, and external action success.

## Current Work

The active bounded sequence is:

1. Review and merge PR #21 only under explicit merge authority.
2. Pull current `main` and restart the dashboard after merge.
3. Inspect the read-only Maintenance activation report before requesting any real assignment authority.
4. Observe the next separately authorized Worker dispatch for composer cleanup behavior without rerunning the completed Maintenance canary.
5. Keep Office Leaks rollout paused.
6. Wait for `Business_HQ` and Rob to define the exact Business Worker purpose, profile, procedures, review path, and first bounded task before Engineering prepares registration or routing work.

Do not infer Business Worker approval from strategic enthusiasm, Maintenance precedent, dashboard visibility, or this status record.

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
- Proven stale LifeOS composer residue may be cleared only under the evidence-backed PR #21 rule after merge; unrelated drafts remain protected.
- Immutable Git evidence outranks stale local transport state.
- `IMMEDIATE_HQ` work never auto-verifies.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Courier, dashboard, ingester, watcher, HQ receipt, and Rob receipt do not close source work automatically.
- The Worker courier does not wake `Chief_of_Staff_HQ` under the current contract.
- Additional Workers, recurring tasks, connectors, spending, public actions, or broader durable-write authority require separate owner review and authorization.

## Boundary

`Engineering_HQ` owns the machinery. Rob decides. Department HQs own their Workers and judgment. `Maintenance_HQ` owns shared governance. Source owners close their own records.

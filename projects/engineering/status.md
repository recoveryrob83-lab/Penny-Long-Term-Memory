# Engineering HQ Status

Updated: 2026-07-23

## Current Phase

Active / Package D Closed / Package E Closed / GitHub-First Worker Operations Live / Scheduled Consumption Live-Validated / Post-Close Operational Observation

## Summary

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, build-readiness, and truthful verification.

Engineering owns technical Worker infrastructure: routing registry, stable IDs, exact browser transport, revision state, duplicate suppression, immutable result ingestion, report-repair mechanics, HQ and Rob receipt ingestion, runtime evidence, verification views, and reliability safeguards. It does not own shared governance, another department's Worker authority, source-owner advisory lifecycle, or domain judgment.

## Source-of-Truth Boundaries

- GitHub: durable architecture, packages, procedures, profiles, advisories, decisions, and immutable result evidence.
- `projects/engineering/open_loops.md`: authoritative unfinished Engineering work.
- SQLite Command Center `execution_history`: sole operational runtime ledger for dispatch, result, repair, HQ review, Rob validation, and consumption readiness.
- Worker result folders: immutable evidence and audit trail, not a competing queue or lifecycle ledger.
- Dashboard and scheduled watcher: visibility and reporting interfaces, not independent truth or closure authority.
- Life OS Maintenance HQ: canonical shared Worker governance and global operating integrity.

Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, or sensitive implementation details in GitHub memory or Worker result artifacts.

## Package State

### Package D

Lifecycle State: CLOSED

Package D established the Worker registry, routing, transport, receiver, verification, duplicate-suppression, and bounded operational-pilot foundation.

### Package E

Lifecycle State: CLOSED
Priority: Normal
Closed: 2026-07-23
Canonical closeout: `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Package E completed the Engineering-only chain for:

- dispatch-only Worker courier wakes;
- exact destination, hydration, composer, generation, and submission witnesses;
- immediate source-room return and shared-gate release;
- immutable schema-valid Worker result artifacts;
- deterministic checksum and same-row result ingestion;
- rejection and correction-only repair mechanics;
- owning-HQ wakes and immutable review receipts;
- explicit Rob-validation receipts where HQ cannot inspect decisive evidence;
- consumption-ready signed results;
- separately authorized scheduled watcher reporting;
- duplicate execution, result, and HQ-wake suppression;
- source-owner advisory lifecycle separation.

The optional display-only human-readable envelope and cross-department adoption are explicitly deferred. Legacy response-capture machinery is not part of the active courier path and remains rollback-compatible only where retained.

## Verified Package E Evidence

### ADV-20260721-048

- Lifecycle: CLOSED
- Run: `RUN-ADV-20260721-048-R1`
- Worker report: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260721-048-R1/report-001.json`
- HQ review: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260721-048-R1/hq-review-001.json`
- HQ state: `VERIFIED`
- Ready for consumption: true

### ADV-20260722-049

- Lifecycle: CLOSED
- Run: `RUN-ADV-20260722-049-R1`
- HQ state: `ROB_VALIDATION_REQUIRED`
- Rob state: `VERIFIED`
- Rob receipt: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260722-049-R1/rob-validation-001.json`
- Ready for consumption: true

### ADV-20260723-051

- Lifecycle: CLOSED
- Run: `RUN-ADV-20260723-051-R1`
- Worker report commit: `313efc95cf49ba5ed34b10a79b78c0a69a4250c2`
- HQ review commit: `9dd13b45782fa6abf83c59c361bb7754a907bae5`
- Runtime state: `HQ_VERIFIED`
- Ready for consumption: true
- Rob validation required: false

The live test exposed repeated HQ wakes after receipt creation. Engineering repaired the defect with Git-first HQ receipt ingestion and an atomic one-shot wake claim. The relaunched dashboard ingested the existing review without another wake and continued clean 30-second polling cycles.

## Advisory State

Closed on 2026-07-23:

- `ADV-20260720-047` — architecture discovery preserved and superseded by Package E completion;
- `ADV-20260721-048` — immutable outbox and HQ verification complete;
- `ADV-20260722-049` — Rob-validation chain complete;
- `ADV-20260723-051` — HQ-wake chain and duplicate-suppression proof complete.

`ADV-20260718-042` remains open under `coordination/boards/main-assistant.md`. Package E closeout does not alter it.

## Automation and Dashboard State

### Worker Operations

Status: Active Engineering pilot control surface.

The dashboard process owns the GitHub-first orchestrator thread. The orchestrator:

- polls every 30 seconds;
- fast-forwards a clean strictly-behind checkout;
- discovers canonical advisories;
- dispatches bounded Worker wakes;
- ingests immutable reports before downstream actions;
- ingests existing HQ receipts before browser wake attempts;
- uses one-shot local claims to suppress uncertain or competing wake retries;
- records actionable runtime events and errors.

### Scheduled Watcher

Status: Live-validated under separate authorization.

The watcher successfully read signed evidence and source advisory state, reported meaningful open-advisory follow-through to Rob, and generated a normal ChatGPT notification. It does not close advisories or create authority.

## Current Work

Package E implementation and its four source advisories are no longer open work.

Current Engineering work is limited to separately authorized items in `projects/engineering/open_loops.md`, including ordinary dashboard observation, connector reliability, existing Worker pilots, and any demonstrated post-close transport defect.

Cross-department Worker result-outbox adoption remains deferred until Life OS Maintenance HQ reviews shared contracts and each owning department explicitly authorizes its own profile or procedure.

## Production Boundary

- Browser automation acts only on exact canonical URLs under one-tab hydration and composer safeguards.
- Confirmed or uncertain sends are not retried blindly.
- Immutable Git evidence outranks stale local transport state.
- Any unrecognized post-submit state must fail closed and require human inspection.
- Worker reports remain evidence until deterministic ingestion.
- `IMMEDIATE_HQ` work never auto-verifies.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Courier, ingester, dashboard, watcher, HQ receipt, and Rob receipt do not auto-close source advisories.
- The courier never wakes Chief of Staff.
- Cross-department rollout, new recurring tasks, connectors, spending, or public actions require separate authority.

## Boundary

Engineering HQ owns the machinery. Rob decides. Department HQs own their Workers and judgment. Life OS Maintenance owns shared governance. Source owners close their own records.
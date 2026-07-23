# Engineering_HQ Session Handoff

Updated: 2026-07-23
Project: Engineering_HQ
Purpose: Fresh-room handoff after Package E closeout, with GitHub-first Worker Operations, immutable evidence, HQ and Rob validation, scheduled consumption, and post-close reliability boundaries.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering_HQ
- Current Phase: Active / Package D Closed / Package E Closed / Worker Operations Live / Scheduled Consumption Live-Validated / Post-Close Observation
- Primary Systems: GitHub, ChatGPT Department and Worker rooms, local LifeOS Dashboard, SQLite Command Center `execution_history`, Engineering advisory board, and Advisory Index
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, or sensitive implementation details in LifeOS memory files or Worker result artifacts.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md` for the closed Worker Operations architecture and closeout evidence when dispatch, immutable result ingestion, HQ review, Rob validation, scheduled consumption, or browser courier behavior is in scope.
7. Read `coordination/boards/engineering.md` and `coordination/ADVISORY_INDEX.md` when routing or advisory lifecycle is relevant.
8. Read `coordination/WORKER_EXECUTION_CONTRACT.md` and `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` when Worker authority, reporting, verification, or execution behavior is in scope.
9. Read `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md` only for Package D history or runtime foundation evidence.
10. Keep connector and browser work small, explicit, fail-closed, and verifiable.

## Department Role

`Engineering_HQ` owns technical architecture, software planning, repository strategy, automation design, APIs and connectors, data models, testing, debugging, implementation sequencing, build-readiness, and truthful verification.

Engineering does not own canonical shared Worker governance, global boot coherence, another department's Worker authority, source-owner advisory lifecycle, or domain judgment. `Maintenance_HQ` owns shared governance surfaces. Departments own their Worker profiles, procedures, authority, holds, and judgment. Engineering owns technical routing, transport, logging, duplicate suppression, result ingestion, verification mechanics, runtime evidence, tests, and reliability infrastructure.

Route business strategy to `Business_HQ` or `Office_Leaks_HQ`, cost-bearing choices to `Finance_HQ`, daily one-off coordination to `Chief_of_Staff_HQ`, shared governance and global memory hygiene to `Maintenance_HQ`, and wellbeing or sustainability judgment to `Wellness_HQ`.

## Canonical Worker Model

A LifeOS Worker is a specialized ChatGPT room operating beneath one Department HQ.

- The Department HQ owns the Worker profile, authority, procedures, holds, and domain judgment.
- GitHub holds canonical profiles, approved procedures, advisories, tasks, decisions, and immutable result and review evidence.
- SQLite `execution_history` remains the sole operational runtime ledger.
- The browser courier wakes a Worker or owning HQ, proves submission, returns immediately, and never waits for completion.
- The Worker performs bounded work and writes one immutable schema-valid report attempt under narrow create-only authority.
- A deterministic ingester validates the report, calculates the canonical checksum, and correlates it to the canonical assignment and existing execution row.
- Invalid reports trigger bounded correction-only repair wakes without re-executing work.
- Valid reports trigger owning-HQ review according to verification mode.
- Department HQ verifies report integrity, authority compliance, evidence, and the work where possible.
- Work unavailable to HQ verification follows an explicit Rob-validation path.
- Only signed HQ or Rob results become consumption-ready.
- A separately authorized scheduled watcher may report meaningful signed changes.
- The courier never wakes `Chief_of_Staff_HQ`.
- Source owners retain advisory lifecycle and closure authority.

Python and browser automation are not the Worker. Worker reports and GitHub outbox artifacts are immutable evidence, not accepted runtime truth or HQ signoff until deterministic ingestion and review occur.

## Package State

### Package D

Lifecycle State: CLOSED

### Package E

Lifecycle State: CLOSED
Closed: 2026-07-23
Canonical closeout: `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Package E completed the Engineering-only implementation and live validation of:

- dispatch-only Worker wakes;
- exact hydration, identity, composer, generation, and new-turn submission witnesses;
- immediate courier release and source-room return;
- immutable Worker result artifacts;
- deterministic checksum and same-row ingestion;
- rejection and report-repair mechanics;
- owning-HQ wakes and immutable HQ receipts;
- explicit Rob-validation receipts;
- signed consumption-ready states;
- scheduled watcher reporting;
- duplicate execution, report, and HQ-wake suppression;
- source-owner advisory lifecycle separation.

Explicitly deferred at closeout:

- cross-department result-outbox adoption;
- universal Worker durable-write authority;
- optional display-only human-readable envelope;
- broader unattended production packaging;
- any new recurring task, connector, spending, or public-action authority.

## Final Package E Evidence

### ADV-20260721-048

- CLOSED
- Run: `RUN-ADV-20260721-048-R1`
- Worker report: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260721-048-R1/report-001.json`
- HQ review: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260721-048-R1/hq-review-001.json`
- HQ state: `VERIFIED`
- Ready for consumption: true

### ADV-20260722-049

- CLOSED
- Run: `RUN-ADV-20260722-049-R1`
- HQ state: `ROB_VALIDATION_REQUIRED`
- Rob validation: `VERIFIED`
- Rob receipt: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260722-049-R1/rob-validation-001.json`
- Ready for consumption: true

### ADV-20260723-051

- CLOSED
- Run: `RUN-ADV-20260723-051-R1`
- Worker report commit: `313efc95cf49ba5ed34b10a79b78c0a69a4250c2`
- HQ review commit: `9dd13b45782fa6abf83c59c361bb7754a907bae5`
- Runtime state: `HQ_VERIFIED`
- Ready for consumption: true

ADV-051 exposed repeated HQ wakes after receipt creation. Engineering repaired the defect by ingesting immutable HQ-review evidence before browser dispatch and using an atomic one-shot wake claim. The relaunched dashboard ingested the existing receipt without another wake and continued quiet polling.

## Advisory State

Closed on 2026-07-23:

- `ADV-20260720-047` — architecture discovery superseded by Package E completion;
- `ADV-20260721-048` — immutable outbox and HQ verification complete;
- `ADV-20260722-049` — Rob-validation chain complete;
- `ADV-20260723-051` — HQ-wake and duplicate-suppression proof complete.

`ADV-20260718-042` remains OPEN on `coordination/boards/main-assistant.md` under its own source owner. Do not close it merely because Package E is complete.

## Current Runtime State

- LifeOS Dashboard runs locally at `http://127.0.0.1:8765`.
- The dashboard process is the sole owner of the GitHub-first orchestrator thread.
- Normal poll interval is 30 seconds.
- Git sync is clean and strictly fast-forward only.
- Existing immutable HQ review evidence is ingested before any HQ browser wake.
- An atomic local claim prevents concurrent or uncertain repeat HQ wakes.
- Unrecognized post-submit states fail closed and require human inspection.
- The scheduled watcher has been live-validated and generated a normal ChatGPT notification.

## Next Valid Action

Do not reopen Package E slices or recreate their closed advisories.

Future Engineering work must come from `projects/engineering/open_loops.md`, a demonstrated defect, or a new explicit Rob instruction. The smallest valid post-close behavior is ordinary observation of real use while preserving all fail-closed boundaries.

Cross-department adoption requires `Maintenance_HQ` shared-contract review and explicit authority from each owning department.

## Production Boundary

- Browser automation acts only on exact canonical URLs.
- Confirmed or uncertain submissions are not retried blindly.
- Immutable Git evidence outranks stale local transport state.
- Worker reports remain evidence until deterministic ingestion.
- `IMMEDIATE_HQ` work never auto-verifies.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Courier, ingester, dashboard, watcher, HQ receipt, and Rob receipt do not auto-close source advisories.
- `Chief_of_Staff_HQ` is never woken by the courier.
- New Workers, connectors, recurring tasks, spending, cross-department rollout, or public actions require separate authority.
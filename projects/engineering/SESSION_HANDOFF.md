# Engineering HQ Session Handoff

Updated: 2026-07-21
Project: Engineering HQ
Purpose: Fresh-room handoff for Package E Worker dispatch, immutable result outbox, browser transport, deterministic ingestion, HQ verification, and the LifeOS Dashboard.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Package D Closed / Package E Slice 3 Live Outbox Proof Complete / Courier Return Defect Open / Slice 4 Next
- Primary Systems: GitHub, ChatGPT Department and Worker rooms, local LifeOS Dashboard, SQLite Command Center `execution_history`, Engineering advisory board, and the Advisory Index when routing is in scope
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, or sensitive implementation details in Life OS memory files or Worker result artifacts.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md` whenever Worker dispatch, result outbox, ingestion, repair wakes, HQ verification, Rob validation, Chief of Staff consumption, browser courier, or unattended orchestration is in scope.
7. Read `coordination/boards/engineering.md` and `coordination/ADVISORY_INDEX.md` when ADV-048 or routing state is relevant.
8. Read `coordination/WORKER_EXECUTION_CONTRACT.md` and `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` when Worker authority, reporting, verification, or execution behavior is in scope.
9. Read `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md` only for Package D history or runtime design evidence.
10. Keep connector and browser work small, explicit, fail-closed, and verifiable.

## Department Role

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, APIs and connectors, data models, testing, debugging, implementation sequencing, build-readiness, and truthful verification.

Engineering does not own canonical shared Worker governance, global boot coherence, another department's Worker authority, source-owner advisory lifecycle, or domain judgment. Life OS Maintenance HQ owns shared governance surfaces. Departments own their Worker profiles, procedures, authority, holds, and judgment. Engineering owns technical routing, transport, logging, duplicate suppression, result ingestion, verification mechanics, runtime evidence, tests, and reliability infrastructure.

Route business strategy to Business HQ or Office Leaks HQ, cost-bearing choices to Finance HQ, daily one-off execution to Chief of Staff HQ, shared governance and global memory hygiene to Life OS Maintenance HQ, and wellbeing or sustainability judgment to Wellness HQ.

## Canonical Worker Model

A Life OS Worker is a specialized ChatGPT room operating beneath one Department HQ.

- The Department HQ owns the Worker profile, authority, procedures, holds, and domain judgment.
- GitHub holds canonical profiles, approved procedures, advisories, tasks, and immutable result and review evidence.
- SQLite `execution_history` remains the sole operational runtime ledger.
- The browser courier wakes a Worker or owning HQ, proves submission, returns immediately, and never waits for completion.
- The Worker performs bounded work and writes one immutable schema-valid report attempt under narrow create-only authority.
- A deterministic ingester validates the report, calculates the canonical checksum, and correlates it to the canonical assignment and existing execution row.
- Invalid reports trigger bounded report-repair wakes without re-executing work.
- Valid reports trigger owning-HQ review according to verification mode.
- Department HQ verifies report integrity, authority compliance, evidence, and the work where possible.
- Work unavailable to HQ verification follows an explicit Rob-validation path.
- Only signed HQ or Rob results become ready for later Chief of Staff consumption.
- The courier never wakes Chief of Staff.
- Source owners retain advisory lifecycle and closure authority.

Python and browser automation are not the Worker. A Worker report and GitHub outbox artifact are evidence, not accepted runtime truth or HQ signoff.

## Primary Current Work Package

### Package E: Worker Dispatch, Result Outbox, HQ Verification, and CoS Consumption

Lifecycle State: Active
Priority: Normal
Canonical packet: `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Objective: complete a nonblocking chain from one already-authorized assignment to a signed Department HQ result available for later Chief of Staff consumption without Rob manually carrying prompts, reports, or evidence between rooms.

## Current Implementation State

### Slice 2: Dispatch-Only Courier

Status: Implemented / Locally validated / Live dispatch partially validated.

Local evidence reported by Rob:

- 40 focused tests passed with 13 warnings;
- dashboard relaunched;
- browser ready;
- execution gate ready;
- Worker Operations ready.

Live evidence from `ADV-20260721-048`:

- the courier reached `Engineering_Worker`;
- the correlated wake succeeded;
- the Worker continued independently and completed;
- the courier did not return the controlled browser tab to Engineering HQ;
- the successful send must not be retried;
- exact return-to-source behavior remains the active transport defect.

### Slice 3: Engineering Worker Result-Outbox Pilot

Status: Implemented / Locally validated / Bounded live artifact validated.

Implemented:

- strict Worker report, rejection, HQ-review, and Rob-validation schemas;
- deterministic immutable paths;
- correctly typed canonical examples;
- `engineering_worker_result_submission` procedure;
- `engineering_worker_result_outbox_validation` procedure;
- advisory contract validation for exact path, attempt, flags, GitHub tool, and `BOUNDED_WRITE` authority;
- focused schema and parser tests.

Live ADV-048 evidence:

- Advisory: `ADV-20260721-048`, revision 1
- Wrapper: `WAKE-ADV-20260721-048-R1`
- Run: `RUN-ADV-20260721-048-R1`
- Report path: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260721-048-R1/report-001.json`
- Creation commit: `fbe75f13bc1b3a2dd35815e0d145c25da8695e22`
- Blob SHA: `f218d63519d38352b8aee4a790ed20807b1bebee`
- Controlled outcome: `IMPLEMENT`
- Verification state: `pending`
- Only durable write: the exact authorized report artifact
- No external action, advisory lifecycle change, overwrite, deletion, work re-execution, or scope expansion
- Rob observed the successful package outbox in the live Worker Operations dashboard
- The Worker could not provide a separate canonical SHA-256 content checksum through the authorized GitHub connector; Slice 4 should calculate it
- Deterministic ingestion and formal Engineering HQ signoff have not occurred

Manual read-only inspection in the retiring chat confirmed the artifact path, identity fields, integer and boolean JSON types, commit scope, blob SHA, `IMPLEMENT` outcome, and pending verification. This was not formal ingester acceptance or HQ signoff.

## Advisory State

### ADV-20260721-048

- Lifecycle: OPEN
- Source and owner: Engineering HQ
- Do not resend revision 1
- Existing report must be preserved
- Formal deterministic ingestion: pending
- Formal `IMMEDIATE_HQ` review: pending
- Closure: not authorized yet

### ADV-20260720-047

- Remains OPEN as architecture-discovery evidence
- Do not retry revision 2
- It exposed the prior response-waiting blockage and quoted `profile_version` template defect

### ADV-20260718-042

- Remains OPEN under its source owner
- Package D closure and Package E work do not change its lifecycle

## Next Valid Action

The next fresh Engineering HQ room should:

1. inspect the existing ADV-048 execution row and dispatch receipt without resending the advisory;
2. determine why the confirmed dispatch did not return the exact browser tab to Engineering HQ;
3. repair return-to-source behavior while preserving confirmed-send idempotency and all existing hydration, exact-destination, empty-composer, no-generation, one-tab, and stop-on-uncertainty safeguards;
4. add focused regression coverage;
5. implement Package E Slice 4 deterministic ingestion;
6. use the existing ADV-048 report as the first valid live ingestion target;
7. calculate and store its canonical checksum on the existing execution row;
8. leave formal HQ review and advisory closure pending until ingestion succeeds.

Do not create a replacement advisory merely to repeat work already completed.

## Package E Later Slices

- Slice 4: deterministic result ingester, strict validation, checksum calculation, rejection artifacts, report-repair wakes, and duplicate suppression.
- Slice 5: owning-HQ wakes and immutable HQ verification receipts.
- Slice 6: Rob-validation path and real end-to-end proof through `READY_FOR_COS`.
- Slice 7: separately authorized read-only Chief of Staff scheduled consumption and unattended local operation.

## Package E Boundaries

Package E must not:

- invent or broaden authority;
- select priorities or create assignments;
- modify another department's files;
- modify shared governance without coordinated authority;
- grant every Worker standing GitHub write authority;
- create a second runtime, response, outcome, verification, wake, queue, or consumption ledger;
- treat dispatch, a Worker report, or an outbox file as accepted authority;
- auto-verify `IMMEDIATE_HQ` work;
- auto-validate work that requires Rob's observation;
- let the courier wake Chief of Staff;
- auto-close advisories;
- control arbitrary browser tabs;
- blind-retry uncertain or confirmed sends;
- create recurring Worker authority without an approved task-generation model.

Cross-department result-outbox adoption requires Life OS Maintenance HQ review of the shared contract and explicit owning-department profile or procedure authority.

## Production Boundary

- Browser transport requires an authenticated, responsive Edge session with loopback CDP available.
- The dashboard server must remain running for Worker Operations.
- A confirmed dispatch remains nonretryable even if browser restoration fails.
- Worker-reported outcomes remain evidence until deterministic ingestion and receiver validation.
- `IMMEDIATE_HQ` results remain pending until Department HQ review.
- Work not independently verifiable by HQ requires explicit Rob validation.
- Receiver, HQ review, or Rob validation does not close source advisories automatically.
- The courier never wakes Chief of Staff.
- Scheduled Chief of Staff consumption requires separate explicit activation after the end-to-end chain is proven.
- Windows service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.
# Engineering HQ Session Handoff

Updated: 2026-07-21
Project: Engineering HQ
Purpose: Current handoff for technical architecture, reshaped Package E Worker dispatch and verification, browser automation, connector reliability, the LifeOS Dashboard, and bounded Worker execution infrastructure.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Package D Closed / Package E Reshaped / Dispatch-Only Courier Next
- Primary Systems: GitHub, ChatGPT Department and Worker rooms, local LifeOS Dashboard, SQLite Command Center `execution_history`, Engineering advisory board, Advisory Index when needed, and other source systems only when explicitly required
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, or sensitive implementation details in Life OS memory files.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md` whenever Worker dispatch, result outbox, report ingestion, repair wakes, HQ verification, Rob validation, Chief of Staff consumption, browser courier, or unattended orchestration is in scope.
7. Read `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md` only when Package D history, runtime design, validation evidence, or closeout is directly relevant.
8. Read `coordination/WORKER_EXECUTION_CONTRACT.md` and `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` when Worker routing, authority, reporting, verification, or execution behavior is in scope.
9. Read `coordination/ADVISORY_INDEX.md` only when advisory routing or cross-department status is relevant.
10. Read current Engineering notebook records only when directly referenced by active work.
11. Keep connector and browser work small, explicit, fail-closed, and verifiable.

## Department Role

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, prompt systems, APIs and connectors, data models, testing, debugging, implementation sequencing, build-readiness, and truthful verification.

Engineering does not own canonical shared Worker governance, global boot coherence, another department's Worker authority, source-owner advisory lifecycle, or domain judgment. Life OS Maintenance HQ owns shared governance surfaces. Departments own Worker profiles, procedures, judgment, and authority. Engineering owns technical routing, transport, logging, duplicate suppression, result ingestion, verification mechanics, runtime evidence, tests, and reliability infrastructure.

Route business strategy to Business HQ or Office Leaks HQ, cost-bearing choices to Finance HQ, daily one-off execution to Chief of Staff HQ, shared governance and global memory hygiene to Life OS Maintenance HQ, and wellbeing or sustainability judgment to Wellness HQ.

## Canonical Worker Model

A Life OS Worker is a specialized ChatGPT room operating beneath one Department HQ.

The operating model is now:

- the Department HQ owns the Worker profile, authority, procedures, holds, and domain judgment;
- GitHub holds canonical profiles, approved procedures, task or advisory state, and immutable result and review evidence;
- SQLite `execution_history` remains the sole operational runtime ledger;
- the browser courier wakes a Worker or owning HQ, proves submission, returns immediately, and never waits for completion;
- the Worker performs the bounded work and writes one immutable schema-valid report attempt to its deterministic result folder under narrow create-only authority;
- a deterministic local ingester validates the report and correlates it to the canonical assignment and existing runtime state;
- malformed reports trigger bounded report-repair wakes without re-executing the work;
- a schema-valid report triggers owning-HQ review according to verification mode;
- Department HQ verifies report integrity, authority compliance, evidence, and work where possible;
- work that HQ cannot independently verify follows an explicit Rob-validation path;
- only signed HQ or Rob results become ready for later Chief of Staff consumption;
- the courier never wakes Chief of Staff;
- source owners retain advisory lifecycle and closure authority.

Python and browser automation are not the Worker. A Worker-reported outcome is evidence, not accepted authority. A GitHub outbox artifact is evidence, not a competing runtime ledger.

## Chat and Work Model

Use regular Chat for architecture, planning, GitHub synchronization, prompt and procedure work, debugging analysis, advisories, and bounded connector updates.

Use Work for substantial coding, local terminal work, full test execution, browser control, packaging, or complex artifacts.

Never claim an action, test, deployment, browser round trip, connector write, report ingestion, or verification occurred without current evidence.

## Primary Current Work Package

### Package E: Worker Dispatch, Result Outbox, HQ Verification, and CoS Consumption

Lifecycle State: Active
Priority: Normal

Canonical packet:

- `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Objective:

Complete a nonblocking operational chain from an already-authorized canonical assignment to a signed Department HQ result available for scheduled Chief of Staff consumption without Rob manually carrying prompts, reports, or evidence between rooms.

### Implemented Foundation

Status: Implemented foundation / Transitional architecture.

Current implementation includes:

- exact Engineering HQ and `Engineering_Worker` URL and title verification;
- Worker-conversation hydration checks;
- empty-composer and no-generation preflight;
- one-tab browser navigation and return;
- correlated request markers;
- zero-authority courier self-test;
- Worker Operations dashboard health, dispatch, route, history, and review visibility;
- shared pause and one-job execution gate;
- legacy prompt-and-scheduler UI removed from view;
- legacy definitions preserved for rollback;
- legacy scheduler dormant by default.

The current courier still contains response-waiting and assistant-response capture from the superseded round-trip design. That code is transitional and must not be treated as the final Package E architecture.

### Architecture Evidence From ADV-20260720-047

Revision 1 exposed a Worker-room hydration race. Engineering added a stable-history readiness gate.

Revision 2 reached the Worker and the Worker completed the assignment, but the courier stopped after submission uncertainty while waiting for response capture. The Worker later produced a strong human-readable report. Its machine line used a string-valued `profile_version` because the generated template showed a quoted placeholder.

This evidence supports the new separation:

- courier dispatch;
- Worker execution;
- immutable result outbox;
- deterministic ingestion and repair;
- Department HQ validation;
- Rob validation when required;
- later scheduled Chief of Staff consumption.

Do not blind-retry revision 2. It is preserved as architecture-discovery evidence, not accepted Package E completion proof.

### Next Valid Action: Slice 2 Dispatch-Only Courier

Convert the courier so it:

1. reaches and verifies the exact Worker room;
2. waits for stable hydration;
3. sends one correlated assignment;
4. proves the correlated user turn exists;
5. records `DISPATCH_SUBMITTED` on the existing runtime state;
6. returns immediately to the source HQ;
7. releases the shared browser gate;
8. performs no response waiting, response scraping, or assistant-turn interpretation.

Completion requires a live bounded dispatch that frees the courier while the Worker remains independently active.

### Later Package E Slices

- Slice 3: Engineering-only immutable Worker result-outbox pilot and narrow create-only reporting authority.
- Slice 4: deterministic result ingester, schema rejection artifacts, report-repair wakes, and duplicate suppression.
- Slice 5: owning-HQ wakes and immutable HQ verification receipts.
- Slice 6: Rob-validation path and real end-to-end proof through `READY_FOR_COS`.
- Slice 7: separately authorized read-only Chief of Staff scheduled consumption and unattended local operation.

## Package D Closeout

### Package D: Operations-Procedure and Worker-Runtime Implementation

Lifecycle State: Closed
Closed: 2026-07-20

Package D's seven technical slices, synthetic backend pilot, desktop transport proof, Engineering Worker profile and route, canonical read-only procedure, and first live operational advisory pilot are complete.

Canonical historical packet:

- `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md`

Primary closeout evidence:

- `ADV-20260720-046` revision 1 returned `REPORT_AND_HOLD` when required boot read scope was missing;
- commit `8cfa874` repaired safe draft/send transport-row ambiguity;
- revision 2 authorized the complete boot chain and returned `IMPLEMENT`;
- the Worker read exact canonical sources and performed no writes;
- the existing execution row preserved receiver acceptance, controlled outcome, evidence, and verified `IMMEDIATE_HQ` review;
- duplicate processing and further verification wakes are suppressed;
- `ADV-20260720-046` is closed, implemented, and source verified;
- no recurring authority, second ledger, automatic HQ judgment, or automatic advisory closure was created.

`ADV-20260718-042` remains open under its source owner. Package D closure does not change its lifecycle.

## Package E Boundaries

Package E may build the technical orchestration path. It must not:

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
- blind-retry uncertain sends;
- create recurring Worker authority without an approved task-generation model.

Cross-department result-outbox adoption requires Life OS Maintenance HQ review of the shared contract and explicit owning-department profile or procedure authority.

## Human-Readable Envelope Requirement

Before ordinary real Worker activation beyond bounded pilots, retain a display-only human-readable summary beside the canonical JSON envelope.

The summary must derive all fields from the same `ExecutionEnvelope`, remain non-authoritative, have no independent edit or parse path, and be covered by parity tests.

## Other Active Tracks

- Observe corrected role-routed specialist boots and inspect demonstrated defects.
- Observe four-source dashboard behavior during ordinary use.
- Continue Raw Capture and Inventory pilots only as grandfathered evidence sources.
- Align the Reliable Connector Execution Layer, operation ledger, and connector-health policy with the validated envelope, evidence, controlled-outcome, verification-state, wake-suppression, transport-integrity, result-outbox, and HQ-review model.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Production Boundary

- Browser transport requires an authenticated, responsive Edge session with the loopback CDP endpoint available.
- The dashboard server must remain running for the Worker Operations UI.
- Failed or uncertain sends must not be retried blindly.
- Existing Python validation is technical infrastructure and defense in depth, not autonomous domain ownership.
- Worker-reported outcomes remain evidence until deterministic ingestion and receiver validation.
- `IMMEDIATE_HQ` results remain pending until Department HQ review.
- Work not independently verifiable by HQ requires explicit Rob validation.
- Receiver, HQ review, or Rob validation does not close source advisories automatically.
- The courier never wakes Chief of Staff.
- Additional Worker activation requires separate bounded authority and a source-owned profile.
- Scheduled Chief of Staff consumption requires separate explicit activation after the end-to-end chain is proven.
- Windows service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Next Valid Action

Implement Package E Slice 2 under `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`: convert the one-tab browser courier to dispatch-only wake transport that proves submission, returns immediately, frees the courier, and records `DISPATCH_SUBMITTED` without waiting for Worker output.
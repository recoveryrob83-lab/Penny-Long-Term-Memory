# Engineering HQ Status

Updated: 2026-07-21

## Current Phase

Active / Package D Closed / Package E Reshaped / Dispatch-Only Courier Next / Result Outbox and HQ Verification Planned / Dashboard Observation / Connector Reliability / Worker Pilots / Prompt Systems / Office Leaks Delivery Architecture

## Summary

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, build-readiness, and truthful verification.

Engineering defines how to build safely and in the right order. Business HQ and Office Leaks HQ define what should be built and why. Finance HQ owns cost-bearing choices. Chief of Staff HQ coordinates daily operations. Life OS Maintenance HQ owns shared global memory hygiene, boot integrity, migrations, audits, source boundaries, canonical Worker governance, and cross-project reconciliation.

Engineering owns technical Worker infrastructure: routing registry, stable IDs, exact transport, revision state, duplicate suppression, result ingestion, verification views, wake suppression, runtime evidence, and reliability mechanisms. It does not own canonical shared governance contracts, another department's Worker authority, source-owner advisory lifecycle, or the Worker's domain judgment.

## Source-of-Truth Boundaries

- GitHub: durable architecture, package state, dashboard code, automation code, Worker profiles and procedures under their owning departments, immutable result evidence, and Engineering records.
- `projects/engineering/open_loops.md`: authoritative unfinished Engineering work and detailed completion ledger.
- `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`: authoritative active Package E scope, slices, boundaries, and completion conditions.
- `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md`: closed historical Package D design and closeout evidence.
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`: canonical shared execution governance, owned by Life OS Maintenance HQ.
- `coordination/WORKER_EXECUTION_CONTRACT.md`: canonical Worker authority and profile convention, owned by Life OS Maintenance HQ.
- SQLite Command Center `execution_history`: sole operational runtime ledger for assignment, dispatch, report state, repair state, receiver outcome, HQ review, and Rob-validation state.
- GitHub Worker result folders: immutable evidence and audit trail, not a competing runtime queue or lifecycle ledger.
- Worker Operations and verification views: interfaces over authoritative GitHub and SQLite state, not competing sources.
- Trello, Todoist, Calendar, Gmail, and Drive retain their established source roles.
- LifeOS Dashboard remains a visibility and bounded local-control layer rather than a replacement source of truth.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Canonical Worker Operating Model

A Life OS Worker is a specialized ChatGPT room operating beneath one Department HQ.

The Department HQ owns its profile, procedures, authority, holds, verification, and judgment. GitHub holds canonical durable state and immutable result evidence. SQLite holds operational runtime state.

The browser courier wakes a Worker or owning HQ, proves submission, returns immediately, and never waits for completion. The Worker performs authorized work and writes an immutable schema-valid report attempt. A deterministic ingester validates the report and updates the existing runtime state. Invalid reports trigger bounded report-repair wakes without re-executing the work. Valid reports trigger Department HQ review according to verification mode. Work that HQ cannot independently verify requires explicit Rob validation. Signed results become available for later Chief of Staff consumption.

The courier never wakes Chief of Staff. A separately authorized ChatGPT scheduled task may later inspect consumption-ready results and report meaningful changes.

Python, browser automation, SQLite, and the dashboard support delivery, exact routing, logging, duplicate suppression, safety checks, ingestion, evidence, and visibility. They are not the Worker and do not replace Department HQ ownership or Rob-only validation.

## Primary Current Work Package

### Package E: Worker Dispatch, Result Outbox, HQ Verification, and CoS Consumption

Lifecycle State: Active
Priority: Normal

Canonical packet:

- `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Objective:

Complete a nonblocking operational chain from an already-authorized assignment to a signed Department HQ result available for scheduled Chief of Staff consumption without Rob manually carrying prompts, reports, or evidence between rooms.

### Implemented Foundation

Status: Implemented foundation / Transitional architecture.

Implemented:

- one-tab Playwright/CDP browser courier;
- exact Engineering HQ and `Engineering_Worker` URL verification;
- Worker-room hydration and composer preflight;
- correlated request markers;
- return-to-HQ behavior;
- Worker Operations dashboard cockpit;
- browser health, shared execution gate, canonical advisory discovery, route visibility, run evidence, and HQ review visibility;
- zero-authority courier self-test;
- visible retirement of the old prompt-and-scheduler UI;
- legacy scheduler dormant by default while backend definitions remain available for rollback.

The current courier still contains response-waiting and assistant-response capture from the superseded round-trip design. It is transitional and is not the production Package E architecture.

### Architecture Evidence From ADV-20260720-047

Revision 1 exposed a Worker-room hydration race and led to a stable-history readiness gate.

Revision 2 reached the Worker and the Worker completed the bounded assignment, but the courier stopped after submission uncertainty while waiting for response capture. The Worker later produced a strong human-readable report. Its machine report used a string-valued `profile_version` because the generated template represented that field as a quoted placeholder.

No blind retry is authorized. Revision 2 is preserved as architecture-discovery evidence rather than accepted Package E completion proof.

### Package E Slice 2

Status: Next bounded implementation.

Required result:

1. preserve exact source and Worker URLs;
2. wait for stable Worker-room hydration;
3. send one correlated bounded assignment;
4. prove the correlated user turn exists;
5. record `DISPATCH_SUBMITTED` on the existing runtime state;
6. return immediately to the source HQ;
7. release the browser gate while the Worker continues independently;
8. remove response waiting, response scraping, and assistant-turn interpretation from the courier path;
9. preserve stop-before-send and no-blind-retry behavior;
10. retain zero-authority self-test coverage.

### Later Package E Slices

- Slice 3: Engineering-only immutable Worker result-outbox pilot and narrow create-only report authority.
- Slice 4: deterministic ingester, strict schema validation, rejection artifacts, report-repair wakes, and duplicate suppression.
- Slice 5: owning-HQ wakes, work inspection, and immutable HQ verification receipts.
- Slice 6: Rob-validation branch and real end-to-end proof through `READY_FOR_COS`.
- Slice 7: separately authorized read-only Chief of Staff scheduled consumption and unattended local operation.

Cross-department result-outbox rollout is not authorized by Package E alone. It requires Life OS Maintenance HQ review of shared Worker governance and explicit owning-department profile or procedure authority.

## Package D Closeout

### Package D: Operations-Procedure and Worker-Runtime Implementation

Lifecycle State: Closed
Closed: 2026-07-20
Priority at close: Normal

Package D delivered Worker contracts and validation, SQLite registry and receiver persistence, registry service, separate Worker Command Center transport, semantic receiver validation, verification views, duplicate suppression, synthetic backend and desktop pilots, the Engineering Worker profile and route, and the first live operational advisory pilot.

Primary evidence:

- `ADV-20260720-046` revision 1 correctly returned `REPORT_AND_HOLD` when required boot scope was missing;
- commit `8cfa874` repaired draft/send transport-row ambiguity;
- revision 2 returned `IMPLEMENT` after the complete boot chain was authorized;
- the existing execution row preserved receiver acceptance and verified `IMMEDIATE_HQ` review;
- duplicate processing and further verification wakes are suppressed;
- the advisory is closed with source verification;
- no recurring authority, second ledger, automatic advisory closure, or autonomous department judgment was created.

`ADV-20260718-042` remains open under the Chief of Staff source board. Package D closure and Package E work do not alter its lifecycle.

## Automation and Dashboard State

### Worker Operations

Status: Active Package E control surface.

The cockpit exposes browser/CDP health, shared pause and one-job lock, canonical execution-ready advisory selection, explicit live-send confirmation, zero-authority courier self-test, Worker registry and route state, existing run history, and HQ verification visibility.

The cockpit must be refactored to show the new dispatch, report, repair, HQ-review, Rob-validation, and consumption-ready runtime states without becoming a competing ledger.

### Legacy Automation Command Center

Status: Retained for rollback, hidden from the visible dashboard, and dormant by default.

- saved prompts and schedule definitions are preserved;
- legacy APIs remain available;
- `LIFEOS_LEGACY_SCHEDULER_ENABLED` must be explicitly enabled to wake the old scheduler;
- no destructive retirement occurs until Package E records a rollback or removal decision.

### LifeOS Dashboard

Application location: `apps/lifeos-dashboard/`

Verified live sources:

- GitHub;
- Trello;
- Todoist;
- Google Calendar private iCal.

Current tabs:

- Overview;
- Department Inspection;
- Worker Operations.

Current boundaries:

- guarded GitHub sync only fast-forwards clean, strictly-behind `main`;
- Gmail and general Drive adapters remain deferred;
- Department Inspection remains read-only;
- Worker Operations may transport and display authorized state but may not invent, approve, prioritize, broaden, or close work;
- fully unattended operation is not assumed merely because browser transport works.

## Other Active Tracks

- Observe ordinary role-routed specialist boots and inspect demonstrated defects.
- Observe four-source dashboard behavior during ordinary use and genuine degraded conditions.
- Pilot Penny Inventory Worker with 2–3 real items only under its grandfathered compatibility boundary.
- Observe Penny Raw Capture Worker only under its grandfathered compatibility boundary.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline aligned with the Worker run, result-outbox, evidence, and HQ-review model.
- Draft the broader operation-ledger schema and connector-health policy without creating a second Worker ledger.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Recent Milestones

- 2026-07-21: Rob reshaped Package E around dispatch-only courier wakes, immutable Worker result artifacts, deterministic ingestion and repair, owning-HQ validation, Rob validation when necessary, and scheduled Chief of Staff consumption.
- 2026-07-21: `ADV-20260720-047` revision 2 demonstrated successful Worker receipt and completion but exposed post-send browser blocking and a generated report-template type defect.
- 2026-07-20: Rob officially closed Package D and designated Worker Operations and Receiver Integration as Package E.
- 2026-07-20: Worker Operations cockpit and one-tab browser courier passed live command-line and dashboard self-tests.
- 2026-07-20: `ADV-20260720-046` revision 2 closed with `IMPLEMENT`, same-row receiver evidence, and verified `IMMEDIATE_HQ` review.
- 2026-07-19: Package D backend and bounded synthetic desktop transport completed local and live validation.

Detailed active state remains authoritative in `projects/engineering/open_loops.md` and `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`.

## Production Boundary

- Browser automation may act only on exact canonical URLs under one-tab hydration and composer safeguards.
- Failed or uncertain sends must not be retried blindly.
- The courier must not wait for Worker or HQ completion.
- Engineering HQ Daily Sync remains paused until Rob explicitly resumes it.
- Python and browser infrastructure must not drift into autonomous domain ownership or independent authority.
- Worker-reported outcomes and GitHub result artifacts are evidence, not accepted receiver authority.
- `IMMEDIATE_HQ` work must not auto-verify.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Receiver, HQ review, or Rob validation must not auto-close source advisories.
- Additional Worker activation requires a separate bounded decision and source-owned profile authority.
- Recurring Worker dispatch requires an approved task-generation and authorization model.
- Scheduled Chief of Staff consumption requires separate explicit activation after the end-to-end chain is proven.
- Windows service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, canonical shared governance, routine cross-project memory curation, source-owner advisory lifecycle, or the domain judgment assigned to Department-owned ChatGPT Workers.
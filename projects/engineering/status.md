# Engineering HQ Status

Updated: 2026-07-20

## Current Phase

Active / Package D Closed / Package E Worker Operations and Receiver Integration / One-Tab Browser Courier Live Validated / Receiver Integration Next / Dashboard Observation / Connector Reliability / Worker Pilots / Prompt Systems / Office Leaks Delivery Architecture

## Summary

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, build-readiness, and truthful verification.

Engineering defines how to build safely and in the right order. Business HQ and Office Leaks HQ define what should be built and why. Finance HQ owns cost-bearing choices. Chief of Staff HQ coordinates daily operations. Life OS Maintenance HQ owns shared global memory hygiene, boot integrity, migrations, audits, source boundaries, canonical Worker governance, and cross-project reconciliation.

Engineering owns technical Worker infrastructure: routing registry, stable IDs, exact transport, revision state, duplicate suppression, response capture, verification views, wake suppression, runtime evidence, and reliability mechanisms. It does not own canonical shared governance contracts, another department’s Worker authority, source-owner advisory lifecycle, or the Worker’s domain judgment.

## Source-of-Truth Boundaries

- GitHub: durable architecture, package state, dashboard code, automation code, Worker profiles and procedures under their owning departments, and Engineering records.
- `projects/engineering/open_loops.md`: authoritative unfinished Engineering work and detailed completion ledger.
- `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`: authoritative active Package E scope, slices, boundaries, and completion conditions.
- `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md`: closed historical Package D design and closeout evidence.
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`: canonical shared execution governance, owned by Life OS Maintenance HQ.
- `coordination/WORKER_EXECUTION_CONTRACT.md`: canonical Worker authority and profile convention, owned by Life OS Maintenance HQ.
- SQLite Command Center `execution_history`: authoritative local automation-run, transport, response-evidence, receiver-outcome, and verification record.
- Worker Operations and verification views: interfaces over authoritative GitHub and SQLite state, not competing sources.
- Trello, Todoist, Calendar, Gmail, and Drive retain their established source roles.
- LifeOS Dashboard remains a visibility and bounded local-control layer rather than a replacement source of truth.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory.

## Canonical Worker Operating Model

A Life OS Worker is a specialized ChatGPT room operating beneath one Department HQ.

The Department HQ owns its profile, procedures, authority, and judgment. GitHub holds canonical durable state. The Worker receives a bounded envelope, reads the required sources, validates the assignment, performs only authorized work, and returns exactly one controlled outcome with evidence. Department HQ reviews the result.

Python, browser automation, SQLite, and the dashboard support delivery, exact routing, logging, duplicate suppression, safety checks, response capture, evidence, and visibility. They are not the Worker and do not replace the Worker’s operational reasoning or Department HQ ownership.

## Primary Current Work Package

### Package E: Worker Operations and Receiver Integration

Lifecycle State: Active
Priority: Normal

Canonical packet:

- `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Objective:

Complete the operational bridge from an already-authorized canonical Worker assignment through one-tab browser transport, correlated response capture, semantic receiver validation, one same-row controlled outcome, and Department HQ review without Rob manually carrying text or evidence between rooms.

### Package E Slice 1

Status: Implemented and live validated.

Implemented:

- one-tab Playwright/CDP browser courier;
- exact Engineering HQ source-URL preservation;
- exact `Engineering_Worker` destination verification;
- empty-composer and no-generation preflight;
- correlated assistant response capture;
- return-to-HQ verification;
- Worker Operations dashboard cockpit;
- browser health, shared execution gate, canonical advisory discovery, route visibility, run evidence, and HQ review visibility;
- zero-authority courier self-test;
- visible retirement of the old prompt-and-scheduler UI;
- legacy scheduler dormant by default while saved backend definitions remain available for rollback.

Live evidence reported by Rob:

- wrapper `SYNTH-BROWSER-WRAP-1784575398-7e1b422eac`;
- run `SYNTH-BROWSER-RUN-1784575398-7e1b422eac`;
- exact acknowledgement captured at `conversation-turn-27`;
- `returned_to_source: true`;
- `durable_authority_created: false`;
- dashboard courier self-test returned to HQ with `conversation-turn-29`.

### Package E Slice 2

Status: Next bounded implementation.

Required result:

1. preserve captured Worker response and browser receipt on the existing execution row;
2. parse exactly one controlled-outcome marker without accepting it as authority;
3. load or reconstruct the authoritative receiver assignment from the canonical advisory, profile, and procedure;
4. validate exact successful transport history and envelope metadata;
5. run receiver preflight and accept only a newer valid revision;
6. translate only verifiable Worker evidence into `ExecutionEvidence`;
7. finalize exactly one same-row controlled outcome;
8. place `IMMEDIATE_HQ` work into the existing review path;
9. preserve source-owner advisory closure authority;
10. fail closed on missing, conflicting, stale, duplicate, unauthorized, or unverifiable reports.

## Package D Closeout

### Package D: Operations-Procedure and Worker-Runtime Implementation

Lifecycle State: Closed
Closed: 2026-07-20
Priority at close: Normal

Package D delivered:

1. Worker contracts and validation.
2. SQLite registry, route, and task-scoped receiver persistence.
3. Registry service.
4. Separate Worker Command Center execution path.
5. Receiver semantic validation and controlled outcomes.
6. Verification views, queue derivation, and wake suppression.
7. Disposable synthetic end-to-end backend pilot with transport-integrity hardening.
8. Bounded synthetic desktop transport.
9. Engineering Worker profile, registry entry, route, and canonical read-only procedure under separate authorization.
10. The first live Engineering Worker advisory pilot.

Closeout evidence:

- `ADV-20260720-046` revision 1 reached the correct Worker and returned `REPORT_AND_HOLD` when required boot read scope was missing;
- commit `8cfa874` repaired draft/send transport-row ambiguity and added regression coverage;
- revision 2 authorized the complete boot chain and returned `IMPLEMENT`;
- the Worker read exact canonical sources, performed no writes, and returned run-linked evidence;
- the existing execution row preserved receiver acceptance, `IMPLEMENT`, and verified `IMMEDIATE_HQ` review;
- receiver revision state suppresses duplicate processing and verification wakes;
- `ADV-20260720-046` is closed with source verification;
- no recurring authority, second ledger, automatic advisory closure, or autonomous department judgment was created.

`ADV-20260718-042` remains open under the Chief of Staff source board. Package D closure does not alter that advisory’s lifecycle.

## ADV-042 Current Interpretation

ADV-20260718-042 assigns different responsibilities:

- the automation layer is the courier and preserves bounded delivery, correlation, transport evidence, and duplicate protection;
- the receiving Worker recognizes the wrapper, resolves canonical sources, validates parameters, authority, ownership, scope, and source boundaries, and returns `IMPLEMENT`, `ELEVATE_FOR_APPROVAL`, or `REPORT_AND_HOLD`;
- the receiver and Department HQ review provide separate defense in depth;
- the source owner retains advisory lifecycle and closure.

Package E may provide additional current evidence relevant to ADV-042. Engineering must not close it without source-owner authority.

## Automation and Dashboard State

### Worker Operations

Status: Active Package E control surface.

The cockpit exposes:

- browser/CDP health;
- shared pause and one-job lock;
- canonical execution-ready advisory selection;
- explicit live-send confirmation;
- zero-authority courier self-test;
- Worker registry and route state;
- captured response and assistant-turn evidence;
- Worker-reported outcome separated from receiver outcome;
- existing HQ verification queue;
- same-row run history.

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
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline aligned with the Worker run model.
- Draft the broader operation-ledger schema and connector-health policy around the execution envelope, evidence, controlled outcomes, verification state, wake suppression, and transport integrity without creating a second Worker ledger.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Recent Milestones

- 2026-07-20: Rob officially closed Package D and designated Worker Operations and Receiver Integration as Package E.
- 2026-07-20: Worker Operations cockpit and one-tab browser courier passed live command-line and dashboard self-tests.
- 2026-07-20: `ADV-20260720-046` revision 2 closed with `IMPLEMENT`, same-row receiver evidence, and verified `IMMEDIATE_HQ` review after revision 1 correctly held.
- 2026-07-20: Rob clarified that a Life OS Worker is a specialized Department-owned ChatGPT room, not an autonomous Python worker process.
- 2026-07-19: ADV-20260719-044 was implemented, source verified, and closed by Life OS Maintenance HQ.
- 2026-07-19: Package D bounded synthetic desktop transport passed exact navigation, composer verification, wrapper-marker verification, explicit send, non-authoritative receipt generation, and exact Worker acknowledgement.
- 2026-07-19: Package D backend Slices 1–7 completed with local validation.
- 2026-07-18: Scheduler production policy, failure pause, Resume behavior, overdue health, restart policy, ledger synchronization, and cleanup passed runtime validation.
- 2026-07-18: Department Inspection reached 414 normalized records, zero findings, and zero warnings.

Detailed active state remains authoritative in `projects/engineering/open_loops.md` and `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`.

## Production Boundary

- Browser automation may act only on exact canonical URLs under the one-tab preflight and return contract.
- Failed or uncertain sends must not be retried blindly.
- Engineering HQ Daily Sync remains paused until Rob explicitly resumes it.
- Python and browser infrastructure must not drift into autonomous domain ownership or independent authority.
- Worker-reported outcomes are evidence, not accepted receiver authority.
- `IMMEDIATE_HQ` work must not auto-verify.
- Receiver or HQ review must not auto-close source advisories.
- Additional Worker activation requires a separate bounded decision and source-owned profile authority.
- Recurring Worker dispatch requires an approved task-generation and authorization model.
- Windows service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, canonical shared governance, routine cross-project memory curation, source-owner advisory lifecycle, or the domain judgment assigned to Department-owned ChatGPT Workers.
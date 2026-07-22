# Engineering HQ Status

Updated: 2026-07-21

## Current Phase

Active / Package D Closed / Package E Slice 3 Live Outbox Proof Complete / Courier Return Defect Open / Slice 4 Deterministic Ingestion Next / Dashboard Observation / Connector Reliability / Worker Pilots / Prompt Systems / Office Leaks Delivery Architecture

## Summary

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, connector and API research, testing strategy, prompt systems, implementation sequencing, build-readiness, and truthful verification.

Engineering owns technical Worker infrastructure: routing registry, stable IDs, exact transport, revision state, duplicate suppression, result ingestion, verification views, wake suppression, runtime evidence, and reliability mechanisms. It does not own canonical shared governance contracts, another department's Worker authority, source-owner advisory lifecycle, or the Worker's domain judgment.

## Source-of-Truth Boundaries

- GitHub: durable architecture, package state, dashboard and automation code, department-owned Worker profiles and procedures, advisories, and immutable result evidence.
- `projects/engineering/open_loops.md`: authoritative unfinished Engineering work.
- `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`: authoritative active Package E scope, slices, boundaries, and completion conditions.
- SQLite Command Center `execution_history`: sole operational runtime ledger for assignment, dispatch, report state, repair state, receiver outcome, HQ review, and Rob-validation state.
- GitHub Worker result folders: immutable evidence and audit trail, not a competing runtime queue or lifecycle ledger.
- Worker Operations: interface over GitHub and SQLite state, not independent truth.
- Life OS Maintenance HQ owns canonical shared execution and Worker governance.

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, or private user data in Life OS GitHub memory or Worker result artifacts.

## Canonical Worker Operating Model

A Life OS Worker is a specialized ChatGPT room operating beneath one Department HQ.

The browser courier wakes a Worker or owning HQ, proves submission, returns immediately, and never waits for completion. The Worker performs authorized work and writes an immutable schema-valid report attempt. A deterministic ingester validates that report, calculates the canonical checksum, and updates the existing execution row. Invalid reports trigger bounded report-repair wakes without re-executing work. Valid reports trigger Department HQ review according to verification mode. Work that HQ cannot independently verify requires explicit Rob validation. Signed results become available for later Chief of Staff consumption.

The courier never wakes Chief of Staff. Python, browser automation, SQLite, and the dashboard are technical infrastructure rather than the Worker or Department HQ judgment.

## Primary Current Work Package

### Package E: Worker Dispatch, Result Outbox, HQ Verification, and CoS Consumption

Lifecycle State: Active
Priority: Normal
Canonical packet: `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Objective: complete a nonblocking operational chain from an already-authorized assignment to a signed Department HQ result available for later Chief of Staff consumption without Rob manually carrying prompts, reports, or evidence between rooms.

## Package E Slice State

### Slice 2: Dispatch-Only Courier

Status: Implemented / Locally validated / Live dispatch partially validated.

- 40 focused tests passed with 13 warnings.
- Dashboard relaunched with browser, execution gate, and Worker Operations ready.
- `ADV-20260721-048` reached the correct Worker and the correlated wake succeeded.
- The Worker completed independently.
- The controlled browser tab did not return to Engineering HQ.
- Do not resend the advisory; confirmed submission remains nonretryable.
- Return-to-source repair and focused regression coverage remain open.

### Slice 3: Engineering Worker Result-Outbox Pilot

Status: Implemented / Locally validated / Bounded live artifact validated.

Implemented:

- strict report, rejection, HQ-review, and Rob-validation schemas;
- deterministic immutable paths and correctly typed examples;
- canonical result-submission procedure;
- bounded outbox-validation procedure;
- advisory validation of exact path, attempt, flags, GitHub tool, and `BOUNDED_WRITE` authority;
- focused schema and parser tests.

Live evidence from `ADV-20260721-048`:

- report path: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260721-048-R1/report-001.json`;
- creation commit: `fbe75f13bc1b3a2dd35815e0d145c25da8695e22`;
- blob SHA: `f218d63519d38352b8aee4a790ed20807b1bebee`;
- controlled outcome: `IMPLEMENT`;
- verification state: `pending`;
- numeric and boolean JSON fields correctly typed;
- only the exact authorized report artifact was written;
- no external action, lifecycle change, overwrite, deletion, work re-execution, or scope expansion;
- Rob observed the successful package outbox in the live dashboard;
- deterministic ingestion and formal Engineering HQ signoff remain pending.

The Worker could not provide a separate canonical SHA-256 checksum through the authorized connector surface. Slice 4 should calculate it from stored content.

### Slice 4: Result Ingester and Repair Wakes

Status: Next.

Required result:

1. discover immutable artifacts without browser scraping;
2. correlate the report to the canonical advisory and existing execution row;
3. validate schema, identity, revision, authority, scopes, tools, evidence, and checksums;
4. calculate canonical content checksum;
5. update the same runtime row without creating another ledger;
6. create deterministic rejection artifacts for invalid reports;
7. queue bounded report-repair wakes without work re-execution;
8. suppress duplicate and stale attempts;
9. expose report and repair state in Worker Operations.

The existing ADV-048 report is the first valid live ingestion target after implementation.

### Later Slices

- Slice 5: owning-HQ wake, work inspection, and immutable HQ verification receipt.
- Slice 6: Rob-validation branch and real end-to-end proof through `READY_FOR_COS`.
- Slice 7: separately authorized read-only Chief of Staff scheduled consumption and unattended local operation.

## Advisory State

- `ADV-20260721-048`: OPEN. Existing report created. Do not resend. Deterministic ingestion and formal `IMMEDIATE_HQ` review pending.
- `ADV-20260720-047`: OPEN architecture-discovery evidence. Do not retry revision 2.
- `ADV-20260718-042`: OPEN under its source owner; unchanged by Package D or E.

## Automation and Dashboard State

### Worker Operations

Status: Active Package E control surface.

Rob currently observes the successful ADV-048 package outbox in the dashboard. The cockpit exposes browser/CDP health, shared pause and one-job lock, canonical advisory selection, explicit send confirmation, Worker registry and route state, dispatch history, and outbox visibility.

The cockpit must gain deterministic report ingestion, rejection/repair state, HQ-review state, Rob-validation state, and consumption readiness without becoming a competing ledger.

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

## Next Valid Action

1. inspect the existing ADV-048 execution row and dispatch receipt without resending;
2. repair exact browser return to Engineering HQ while preserving successful-send idempotency and all existing safeguards;
3. add focused regression coverage;
4. implement Slice 4 deterministic ingestion using the existing report;
5. leave formal HQ review and advisory closure pending until ingestion succeeds.

## Production Boundary

- Browser automation may act only on exact canonical URLs under one-tab hydration and composer safeguards.
- Failed or confirmed sends must not be retried blindly.
- A confirmed dispatch and browser return are separate postconditions.
- The courier must not wait for Worker or HQ completion.
- Worker reports and GitHub outbox artifacts are evidence, not accepted receiver authority.
- `IMMEDIATE_HQ` work must not auto-verify.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Receiver, HQ review, or Rob validation must not auto-close source advisories.
- Scheduled Chief of Staff consumption requires separate activation after the end-to-end chain is proven.
- Engineering HQ Daily Sync remains paused until Rob explicitly resumes it.

## Boundary

Engineering HQ owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, canonical shared governance, routine cross-project memory curation, source-owner advisory lifecycle, or the domain judgment assigned to Department-owned ChatGPT Workers.
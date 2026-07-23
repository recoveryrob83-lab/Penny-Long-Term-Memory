# Advisory Index

Updated: 2026-07-23
Purpose: Sole active routing dashboard for open Life OS advisories.

## Open / Unacknowledged Advisories

None.

## Acknowledged / Implemented Advisories

- ADV-20260718-042 — CLOSED / IMPLEMENTED — Posted Board: `coordination/boards/main-assistant.md` — Target Department: Engineering HQ — Receiver-side prompt validation, canonical prompt and parameter checks, authority and ownership validation, duplicate suppression, explicit Worker outcomes, immutable evidence, and fail-closed handling were built and tested through completed automation packages and live runs. Rob confirmed the system is ready for slow rollout and authorized source-owner closure. Closed 2026-07-23.
- ADV-20260723-051 — CLOSED — Posted Record: `projects/engineering/advisories/ADV-20260723-051.md` — Target Department: Engineering HQ — The bounded GitHub-first receipt test completed. The Worker created one immutable report, Engineering HQ created one immutable `VERIFIED` review, and the dashboard ingested the review into the existing runtime row as `HQ_VERIFIED`. A repeated HQ-wake defect discovered during the test was repaired with Git-first receipt ingestion and an atomic one-shot wake claim. Post-repair cycles remained quiet. Closed 2026-07-23.
- ADV-20260722-049 — CLOSED — Posted Board: `coordination/boards/engineering.md` — Target Department: Engineering HQ — Package E Slice 6 completed through immutable Worker report, `ROB_VALIDATION_REQUIRED` HQ review, Rob's verified observation receipt, and a signed consumption-ready result. No response scraping, re-execution, scope expansion, automatic lifecycle action, or Chief of Staff courier wake occurred. Closed 2026-07-23.
- ADV-20260721-048 — CLOSED — Posted Board: `coordination/boards/engineering.md` — Target Department: Engineering HQ — The immutable result-outbox pilot completed through deterministic same-row ingestion and an Engineering HQ `VERIFIED` receipt. The report and HQ review are valid, authority-compliant, independently verified, and consumption-ready without Rob validation. Closed 2026-07-23.
- ADV-20260720-047 — CLOSED / SUPERSEDED BY PACKAGE E COMPLETION — Posted Board: `coordination/boards/engineering.md` — Target Department: Engineering HQ — Revision 2 remains architecture-discovery evidence and was not retried. Its findings were implemented and superseded by the completed dispatch-only courier, immutable outbox, deterministic ingester, HQ review, Rob validation, and scheduled-consumption chain. Closed 2026-07-23.
- ADV-20260723-050 — CLOSED / FAILED TEST — Posted Record: `projects/engineering/advisories/ADV-20260723-050.md` — Target Department: Engineering HQ — Dashboard automation pasted the wake but did not submit it. The invalid dispatch receipt was rejected, the Worker did not execute, and the advisory was closed without retry. A fresh advisory and run ID were used after strict dispatch-proof repair. Closed 2026-07-23.
- ADV-20260720-046 — CLOSED — Posted Board: `coordination/boards/engineering.md` — Target Department: Engineering HQ — The first live Engineering Worker advisory pilot completed under bounded read-only authority with revision-2 `IMPLEMENT`, same-row receiver acceptance, verified Immediate-HQ review, and no broader Worker scope. Closed 2026-07-20.
- ADV-20260719-045 — CLOSED — Posted Board: `coordination/boards/main-assistant.md` — Target Department: Life OS Maintenance HQ — Maintenance consumed and acknowledged the verified ChatGPT Projects context-memory discovery while preserving GitHub as canonical, shared sources as role-neutral, and room identity as local. Closed 2026-07-19.
- ADV-20260719-044 — CLOSED — Posted Board: `coordination/boards/engineering.md` — Target Department: Life OS Maintenance HQ — Maintenance reconciled Worker filesystem, boot, ownership, and continuity boundaries. Closed 2026-07-19.
- ADV-20260719-043 — CLOSED — Posted Board: `coordination/boards/main-assistant.md` — Target Department: Life OS Maintenance HQ — Maintenance established shared execution and Worker contracts, universal boot integration, Worker authority ceilings, and profile conventions. Closed 2026-07-19.
- ADV-20260718-041 — CLOSED — Posted Board: `coordination/boards/main-assistant.md` — Target Department: Life OS Maintenance HQ — Maintenance added the global Trello false-negative write protocol. Closed 2026-07-18.
- ADV-20260717-040 — CLOSED — Posted Board: `coordination/boards/engineering.md` — Target Department: Life Logistics HQ — Life Logistics reconciled shared summaries after the live four-source dashboard milestone. Closed 2026-07-17.
- ADV-20260716-039 — CLOSED — Posted Board: `coordination/boards/engineering.md` — Target Department: Life Logistics HQ — Life Logistics reconciled shared state after the July 16 changes. Closed 2026-07-17.
- ADV-20260716-038 — CLOSED — Posted Board: `coordination/boards/main-assistant.md` — Target Department: Engineering HQ — Engineering accepted the read-mostly desktop dashboard as an active design concept. Closed after later implementation superseded the concept-only state.
- ADV-20260716-037 — CLOSED — Posted Board: `coordination/boards/office-leaks.md` — Target Departments: Multiple — All target departments acknowledged the Office Leaks public launch. Closed 2026-07-16.
- ADV-20260715-036 — CLOSED — Posted Board: `coordination/boards/main-assistant.md` — Target Department: Engineering HQ — Seven LifeOS department discussion HQ chats were launched with operating boundaries. Closed 2026-07-15.
- ADV-20260715-035 — CLOSED — Posted Board: `coordination/boards/main-assistant.md` — Target Department: Engineering HQ — Daily Operating SOP was integrated into global boot flow. Closed.
- ADV-20260714-034 — CLOSED — Posted Board: `coordination/boards/engineering.md` — Target Department: Life Logistics HQ — Expanded connector-tagged shortcuts were ingested. Closed 2026-07-14.
- ADV-20260713-033 — CLOSED — Posted Board: `coordination/boards/life-os.md` — Target Department: Life Logistics HQ — Shortcut rollout was ingested and approved vocabulary activated. Closed.
- ADV-20260710-032 — CLOSED — Posted Board: `coordination/boards/engineering.md` — Target Department: Life Logistics HQ — Penny Inventory Worker boot package was created and verified. Closed.
- ADV-20260710-031 — CLOSED — Posted Board: `coordination/boards/engineering.md` — Target Department: Life Logistics HQ — Advisory Board Lifecycle Standard was created and boards compacted. Closed.
- ADV-20260709-030 — CLOSED — Posted Board: `coordination/boards/engineering.md` — Target Department: Life Logistics HQ — Formal Life OS Worker layer and Raw Capture Worker package were created. Closed.
- ADV-20260709-029 — CLOSED / IMPLEMENTED THROUGH ADV-20260709-030 — Posted Board: `coordination/boards/main-assistant.md` — Target Department: Engineering HQ — Rapid-capture architecture was implemented through the Worker package. Closed.

See department boards and repository history for earlier acknowledged advisories.

## Routing Rule

Advisories live on the source department board under `coordination/boards/`, except explicitly authorized bounded one-file pilots.

This index is the sole active routing dashboard. It should answer:

- Which advisories are open?
- Where are they located?
- Who is the target department?

Operational boards follow `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`.

`coordination/DEPARTMENT_EVENT_INBOX.md` is frozen as historical and should not be updated for normal advisory routing unless Rob explicitly reactivates it.
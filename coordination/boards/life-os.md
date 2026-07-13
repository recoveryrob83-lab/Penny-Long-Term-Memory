# Life OS Infrastructure Advisory Board

Updated: 2026-07-13
Purpose: Advisories from Life OS Infrastructure / Life Logistics HQ to all Penny departments.

## Open Advisories

### ADV-20260713-033 — Add boot and advisory response shortcuts to Penny context boot

- Date: 2026-07-13
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: Medium
- Status: Open / Unacknowledged
- Related Project(s): Penny Long-Term Memory, global boot, context reminder, response interface
- Source Location: `memory/CONTEXT_REMINDER.md`, `memory/STARTUP_BOOT.md`
- Posted Board: `coordination/boards/life-os.md`
- Target Department: Life Logistics HQ

#### Summary

Engineering implemented a focused shortcut rollout: `/BOOT`, `/ADVISE`, `/ADVISORY`, and `/SYNCADVISORY`.

`/BOOT` runs the canonical GitHub boot and synchronization sequence for the relevant Penny role or department. `/ADVISE` gives Rob a recommendation without creating durable work. `/ADVISORY` drafts a formal routed advisory and asks before posting. `/SYNCADVISORY` reads advisory state and reports drift without changing it.

All four shortcuts are documented in `memory/CONTEXT_REMINDER.md`, and the context reminder is included in the global boot order in `memory/STARTUP_BOOT.md`.

Rob approved `/ADVISE`, `/ADVISORY`, and `/SYNCADVISORY` for active use during the day.

#### Operating Constraint

`/BOOT` is a convenience command only. Boot remains read-only unless Rob explicitly authorizes changes. The shortcut does not override department routing, safety rules, connector instructions, or source-of-truth rules.

#### Requested Logistics Action

Please ingest this rollout into Life Logistics HQ synchronization awareness and include the three advisory shortcuts in future boot/sync guidance where useful.

## Acknowledged / Implemented Advisories

### ADV-20260705-014 — Standardize notebook leaf routing and index files

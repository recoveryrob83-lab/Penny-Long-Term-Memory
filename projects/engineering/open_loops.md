# Chief Engineering Penny Open Loops

Updated: 2026-07-04

## Open

| Status | Item | Next Action | Notes |
|---|---|---|---|
| Open | Reliable Connector Execution Layer | Draft technical design note covering operation ledger, connector health states, idempotent writes, retry/backoff, degraded mode, and RPR fallback | Source: ADV-20260704-002 from Chief Business HQ |
| Open | First engineering target | Treat Reliable Connector Execution Layer as the first concrete engineering research track unless Business HQ sends a higher-priority product requirement | Connector reliability is a product-level risk for Penny execution workflows |
| Open | Business handoff path | Coordinate with Chief Business HQ when product requirements are ready | Business defines what; Engineering defines how |
| Open | Cost-bearing technical choices | Route hosting, subscriptions, paid APIs, tools, backend workers, queues, or paperwork overlap to Chief of Finance Penny | Finance owns money/paperwork |
| Open | Software repository strategy | Create or select dedicated software repos only when useful | Life OS memory repo is not the code repo |
| Open | Working records | Use Drive, RPR, or repo docs only when useful | Engineering Drive scaffold now exists |
| Open | Advisory watcher / event inbox refinement | Help refine the scheduled watcher or Department Event Inbox if Rob routes that work back to Engineering | Watcher is reporting layer only; inbox is source sync register |

## Done / Recently Closed

| Closed Date | Item | Notes |
|---|---|---|
| 2026-07-04 | Ingested ADV-20260704-002 | Engineering accepted connector write reliability as a first-class product architecture risk and created the Reliable Connector Execution Layer research track. |
| 2026-07-03 | Consumed advisory workflow update | Engineering read Department Event Inbox and operational rules, then updated Engineering handoff/open loops. |
| 2026-07-03 | Created Engineering Drive scaffolding | Created Drive folder and files: Technical Baseline, Implementation Packet Template, Tracker. |
| 2026-07-03 | Activated Chief Engineering Penny | Created full specialist department under `projects/engineering/`. |
| 2026-07-03 | Created department files | Created handoff, identity, README, status, and open-loop structure. |

## Parking Lot

- Decide future software repository structure when Business has enough product direction.
- Add registry ref later if Life Logistics HQ assigns one.
- Consider whether Engineering should create a more formal event-inbox schema if the watcher experiment proves useful.

# Chief Engineering Penny Open Loops

Updated: 2026-07-10

## Open

| Status | Item | Next Action | Notes |
|---|---|---|---|
| Open | Reliable Connector Execution Layer | Turn the design note into an implementation packet outline and operation ledger schema | Drive doc: `Reliable Connector Execution Layer - Design Note` |
| Open | Operation ledger schema | Draft fields, states, idempotency keys, verification methods, and recovery instructions | Source: ADV-20260704-002 from Chief Business HQ |
| Open | Connector health and retry policy | Define read/write health states, bounded retry rules, stop/backoff triggers, and degraded-mode fallback | Connector may be read-capable while write-blocked |
| Open | Penny Raw Capture Worker pilot | Observe real append, canonical-target, timestamp, and verification behavior | Worker package implemented; operational reliability still needs live use |
| Open | Future worker architecture | Reuse the shared worker standard only when a repeatable job has bounded inputs, outputs, verification, and failure behavior | Do not create speculative workers |
| Open | Office Leaks delivery architecture | Continue one-problem local-service-office cleanup playbooks as Business requirements mature | Preserve mechanical workflow and human-system layers |
| Open | Business handoff path | Coordinate with Chief Business HQ and Office Leaks Consulting HQ when product or service requirements are ready | Business defines what; Engineering defines how |
| Open | Cost-bearing technical choices | Route hosting, subscriptions, paid APIs, tools, backend workers, queues, or paperwork overlap to Chief of Finance Penny | Finance owns money and paperwork |
| Open | Software repository strategy | Create or select dedicated software repositories only when useful | Life OS memory repository is not the code repository |
| Open | Working records | Use Drive, RPR, or dedicated repository documentation only when useful | Keep Life OS GitHub abstract |

## Done / Recently Closed

| Closed Date | Item | Notes |
|---|---|---|
| 2026-07-10 | Engineering advisory source-board reconciliation | ADV-20260709-030 moved to Implemented / Closed on `coordination/boards/engineering.md`; live board and Advisory Index now agree. |
| 2026-07-09 | ADV-20260709-030 implemented | Life Logistics created the formal worker layer, shared worker standard, Penny Raw Capture Worker package, canonical Sheet pointer, and startup routing. |
| 2026-07-09 | ADV-20260709-029 acknowledged and closed through 030 | Engineering completed the architecture investigation and routed durable implementation to Life Logistics. |
| 2026-07-09 | Penny Raw Capture Worker architecture completed | Central raw-capture Sheet, verified-write contract, privacy boundaries, failure language, and downstream Main Assistant processing were formalized. |
| 2026-07-08 | Office Leaks human-system delivery layer created | Engineering added respect, rapport, internal champion, Aha Moment, adoption verification, and relational follow-up to the mechanical delivery workflow. |
| 2026-07-08 | Office Leaks delivery playbooks advanced | Created Engineering notebook architecture for bite-sized local service office cleanup offers. |
| 2026-07-04 | Created Reliable Connector Execution Layer design note | Drive doc created under Life Organization > Chief Engineering Penny. |
| 2026-07-04 | Ingested ADV-20260704-002 | Engineering accepted connector write reliability as a first-class product architecture risk and created the Reliable Connector Execution Layer research track. |
| 2026-07-03 | Activated Chief Engineering Penny | Created specialist department structure and initial working records. |

## Parking Lot

- Decide future software repository structure when Business has enough product direction.
- Add a registry reference later if Life Logistics HQ assigns one.
- Evaluate additional workers only after the Raw Capture Worker pilot produces real operational evidence.
- Revisit whether a software-backed capture service is justified only if connector-based operation proves insufficient.
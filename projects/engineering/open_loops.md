# Chief Engineering Penny Open Loops

Updated: 2026-07-10

## Open

| Status | Item | Next Action | Notes |
|---|---|---|---|
| Open | Penny Inventory Worker pilot | Begin with 2–3 real sale items and verify one-row-per-item writes, stable image references, uncertainty labels, and final Sheet read | Architecture complete; implementation package lives at `workers/penny-inventory/` |
| Open | Penny Raw Capture Worker pilot | Observe real append, canonical-target, timestamp, and verification behavior | Worker package implemented; operational reliability still needs live use |
| Open | Reliable Connector Execution Layer | Turn the design note into an implementation packet outline and operation ledger schema | Drive doc: `Reliable Connector Execution Layer - Design Note` |
| Open | Operation ledger schema | Draft fields, states, idempotency keys, verification methods, and recovery instructions | Source: ADV-20260704-002 from Chief Business HQ |
| Open | Connector health and retry policy | Define read/write health states, bounded retry rules, stop/backoff triggers, and degraded-mode fallback | Small operations, explicit invocation, one-connector focus, and fresh-chat recovery are current field lessons |
| Open | Worker reliability evidence | Compare real pilot results against the shared worker standard before proposing more workers | Do not create speculative workers |
| Open | Office Leaks delivery architecture | Continue one-problem local-service-office cleanup playbooks as Business requirements mature | Preserve mechanical workflow and human-system layers |
| Open | Business handoff path | Coordinate with Chief Business HQ and Office Leaks Consulting HQ when product or service requirements are ready | Business defines what; Engineering defines how |
| Open | Cost-bearing technical choices | Route hosting, subscriptions, paid APIs, tools, backend workers, queues, or paperwork overlap to Chief of Finance Penny | Finance owns money and paperwork |
| Open | Software repository strategy | Create or select dedicated software repositories only when useful | Life OS memory repository is not the code repository |
| Open | Working records | Use Drive, RPR, or dedicated repository documentation only when useful | Keep Life OS GitHub abstract |

## Done / Recently Closed

| Closed Date | Item | Notes |
|---|---|---|
| 2026-07-10 | ADV-20260710-032 implemented and closed | Life Logistics created the Penny Inventory Worker package, verified the canonical `For Sale Inventory` Sheet, and updated worker routing. |
| 2026-07-10 | Inventory Worker architecture review completed | Engineering judged image recognition sufficient, confirmed one-row-per-item as the operating model, and kept pricing/listing work out of scope. |
| 2026-07-10 | ADV-20260710-031 implemented | Life Logistics created the Advisory Board Lifecycle Standard and compacted the Engineering board. |
| 2026-07-10 | Engineering advisory source-board reconciliation | Engineering board and Advisory Index agree; stale ADV-030 wording removed. |
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
- Evaluate additional workers only after the Raw Capture and Inventory Worker pilots produce real operational evidence.
- Revisit whether software-backed capture services are justified only if connector-based operation proves insufficient.

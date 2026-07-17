# Chief Engineering Penny Open Loops

Updated: 2026-07-16

## Open

| Status | Item | Next Action | Notes |
|---|---|---|---|
| Open | Penny Inventory Worker pilot | Begin with 2–3 real sale items and verify one-row-per-item writes, stable image references, uncertainty labels, and final Sheet read | Architecture complete; implementation package lives at `workers/penny-inventory/` |
| Open | Penny Raw Capture Worker pilot | Observe real append, canonical-target, timestamp, and verification behavior | Worker package implemented; operational reliability still needs live use |
| Open | Reliable Connector Execution Layer | Turn the design note into an implementation packet outline | Drive doc: `Reliable Connector Execution Layer - Design Note` |
| Open | Operation ledger schema | Draft fields, states, idempotency keys, verification methods, partial-success handling, and recovery instructions | Keep the first schema small enough to test manually |
| Open | Connector health and retry policy | Define read/write health states, bounded retry rules, stop/backoff triggers, and degraded-mode fallback | Current field lessons favor small operations, explicit invocation, narrow connector scope, and fresh-chat recovery |
| Open | Worker reliability evidence | Compare real pilot results against `workers/WORKER_STANDARD.md` before proposing more workers | Do not create speculative worker bureaucracy |
| Open | Chat HQ observation | Watch the seven operating HQ chats for routing friction, duplicated authority, stale boot assumptions, connector limits, and wasted model usage | ADV-20260715-036 is closed; refine only from observed use |
| Open | Office Leaks delivery architecture | Continue one-problem local-service-office cleanup playbooks as Business requirements mature | Preserve mechanical workflow and human-system layers |
| Open | LifeOS desktop dashboard specification | Wait for Rob's concrete requirements, then define a staged read-mostly specification and completion criteria before implementation | ADV-20260716-038 is consumed and closed; no implementation is currently authorized |
| Open | Business handoff path | Coordinate with Chief Business HQ and Office Leaks Consulting HQ when product or service requirements are ready | Business defines what; Engineering defines how |
| Open | Cost-bearing technical choices | Route hosting, subscriptions, paid APIs, tools, backend workers, queues, or paperwork overlap to Chief of Finance Penny | Finance owns money and paperwork |
| Open | Software repository strategy | Create or select dedicated software repositories only when implementation work justifies them | Life OS memory repository is not the code repository |
| Open | Engineering HQ Daily Sync | Keep paused until scheduled execution architecture is more reliable and Rob explicitly resumes it | Do not roll out additional scheduled HQ sync workers |

## Waiting / Routed

| Status | Item | Owner / Trigger | Notes |
|---|---|---|---|
| Routed | Shared global-summary reconciliation | Life Logistics HQ through ADV-20260716-039 | Reconcile `memory/01_SESSION_HANDOFF.md`, `memory/04_ACTIVE_PROJECTS.md`, and `memory/05_OPEN_LOOPS.md` with current July 16 state |
| Waiting | Deferred prompt-launcher improvements | Revisit when selected for implementation | `/READADVISORY`, `/CONSUMEADVISORY`, and explicit launcher scope metadata are captured in `projects/engineering/notebook/NOTE-20260716-007-prompt-launcher-advisory-commands-and-scope.md`; they are intentionally not active open loops tonight |

## Done / Recently Closed

| Closed Date | Item | Notes |
|---|---|---|
| 2026-07-16 | ADV-20260716-038 acknowledged / ingested / closed | Engineering accepted the read-mostly LifeOS desktop dashboard as an active design concept while preserving source systems, Penny as worker, prompt-launcher reuse, financial-connector isolation, and no-build-until-authorized boundaries. |
| 2026-07-16 | Prompt launcher newline repair | Literal `\n` output from Hub Boot onward was corrected in `engineering/classroom/prompt_launcher/prompt_library.json` and verified. |
| 2026-07-15 | ADV-20260715-036 implemented / acknowledged / closed | Rob confirmed all seven LifeOS department discussion HQ chats are open and ready. Chat/Work separation, department boundaries, connector rules, truthful action reporting, and model-usage discipline are operational. |
| 2026-07-15 | ADV-20260715-035 implemented / acknowledged / closed | Daily Operating SOP integrated into the canonical global boot path and inherited by department boots. |
| 2026-07-15 | Expanded shortcut and hub command synchronization | `memory/CONTEXT_REMINDER.md` contains the active response, connector, hub, routing, drift, and GitHub update vocabulary. |
| 2026-07-10 | ADV-20260710-032 implemented and closed | Life Logistics created the Penny Inventory Worker package, verified the canonical `For Sale Inventory` Sheet, and updated worker routing. |
| 2026-07-10 | Inventory Worker architecture review completed | Engineering confirmed one-row-per-item behavior and kept pricing/listing work out of scope. |
| 2026-07-10 | ADV-20260710-031 implemented | Advisory Board Lifecycle Standard created and Engineering board compacted. |
| 2026-07-09 | ADV-20260709-030 implemented | Formal worker layer, shared worker standard, Penny Raw Capture Worker package, canonical Sheet pointer, and startup routing created. |
| 2026-07-08 | Office Leaks delivery architecture advanced | Mechanical delivery playbook and human-system layer documented. |
| 2026-07-04 | Reliable Connector Execution Layer established | Connector write reliability accepted as a first-class architecture risk. |

## Parking Lot

- Decide future software repository structure when Business has enough product direction and implementation work is ready.
- Add a registry reference later if Life Logistics HQ assigns one.
- Evaluate additional workers only after Raw Capture and Inventory pilots produce real evidence.
- Revisit software-backed capture services only if connector-based operation proves insufficient.
- Revisit prompt packaging or canonical prompt storage only if the live Chat HQs drift or become difficult to recreate.
- Review whether notebook capture needs a stronger resurfacing mechanism before adding more durable ideas without a review cadence.
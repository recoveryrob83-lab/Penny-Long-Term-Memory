# Chief Engineering Penny Open Loops

Updated: 2026-07-17

## Open

| Status | Item | Next Action | Notes |
|---|---|---|---|
| Open | LifeOS Dashboard V0 local launch | Guide Rob through pulling current `main`, creating the Python environment, installing dependencies, and launching the dashboard | Runnable scaffold is merged at `apps/lifeos-dashboard/`; sample-data mode only |
| Open | Dashboard first-use review | Capture what Rob can understand within ten seconds, what feels noisy, what is missing, and what layout changes are needed | Do not add live integrations before validating the screen itself |
| Open | GitHub dashboard read adapter | After V0 layout acceptance, design and implement the first live source adapter for notebooks, advisories, open loops, and recent durable activity | GitHub is the preferred first live source because it is read-only and central to LifeOS durable state |
| Open | Penny Inventory Worker pilot | Begin with 2–3 real sale items and verify one-row-per-item writes, stable image references, uncertainty labels, and final Sheet read | Architecture complete; implementation package lives at `workers/penny-inventory/` |
| Open | Penny Raw Capture Worker pilot | Observe real append, canonical-target, timestamp, and verification behavior | Worker package implemented; operational reliability still needs live use |
| Open | Reliable Connector Execution Layer | Turn the design note into an implementation packet outline | Drive doc: `Reliable Connector Execution Layer - Design Note` |
| Open | Operation ledger schema | Draft fields, states, idempotency keys, verification methods, partial-success handling, and recovery instructions | Keep the first schema small enough to test manually |
| Open | Connector health and retry policy | Define read/write health states, bounded retry rules, stop/backoff triggers, and degraded-mode fallback | Current field lessons favor small operations, explicit invocation, narrow connector scope, and fresh-chat recovery |
| Open | Worker reliability evidence | Compare real pilot results against `workers/WORKER_STANDARD.md` before proposing more workers | Do not create speculative worker bureaucracy |
| Open | Chat HQ observation | Watch the seven operating HQ chats for routing friction, duplicated authority, stale boot assumptions, connector limits, and wasted model usage | Refine only from observed use |
| Open | Office Leaks delivery architecture | Continue one-problem local-service-office cleanup playbooks as Business requirements mature | Preserve mechanical workflow and human-system layers |
| Open | Business handoff path | Coordinate with Chief Business HQ and Office Leaks Consulting HQ when product or service requirements are ready | Business defines what; Engineering defines how |
| Open | Cost-bearing technical choices | Route hosting, subscriptions, paid APIs, tools, backend workers, queues, or paperwork overlap to Chief of Finance Penny | Finance owns money and paperwork |
| Open | Software repository strategy | Decide whether to move the dashboard into a dedicated software repository if implementation expands materially | Current scaffold is intentionally isolated under `apps/lifeos-dashboard/` |
| Open | Engineering HQ Daily Sync | Keep paused until scheduled execution architecture is more reliable and Rob explicitly resumes it | Do not roll out additional scheduled HQ sync workers |

## Waiting / Deferred

| Status | Item | Owner / Trigger | Notes |
|---|---|---|---|
| Waiting | Live Trello adapter | Begin after the GitHub adapter and V0 screen validation | Trello Flow Board should supply Now, top Next, Waiting, and optional Inbox count |
| Waiting | Todoist and Calendar adapters | Begin after GitHub and Trello data paths are stable | Add commitments and schedule pressure without turning the dashboard into a full task manager |
| Waiting | Gmail and Drive adapters | Begin after core dashboard usefulness is proven | Show attention signals and shortcuts, not full replicas of either system |
| Waiting | Desktop window packaging | Revisit after the browser-based dashboard proves useful | Preferred direction is pywebview around the same local FastAPI app |
| Waiting | Deferred prompt-launcher improvements | Revisit when selected for implementation | `/READADVISORY`, `/CONSUMEADVISORY`, and explicit launcher scope metadata are captured in `projects/engineering/notebook/NOTE-20260716-007-prompt-launcher-advisory-commands-and-scope.md` |
| Waiting | Notebook resurfacing mechanism | Review when dashboard notebook visibility is working | Avoid solving forgotten notes by adding more undifferentiated open loops |

## Done / Recently Closed

| Closed Date | Item | Notes |
|---|---|---|
| 2026-07-17 | LifeOS Dashboard V0 scaffold | PR #2 merged as commit `bdf920112e8142179d3da91a3e7983e1a5d48c27`; FastAPI app, responsive sample dashboard, adapter boundary, documentation, and tests created |
| 2026-07-17 | Dashboard scaffold verification | Python compilation succeeded; 3 smoke tests passed; live localhost server and all core endpoints returned HTTP 200 |
| 2026-07-17 | ADV-20260716-039 implemented / acknowledged / closed | Life Logistics reconciled shared global summaries with current state |
| 2026-07-16 | ADV-20260716-038 acknowledged / ingested / closed | Engineering accepted the read-mostly dashboard concept while preserving source systems, Penny as worker, and financial-connector isolation |
| 2026-07-16 | Prompt launcher newline repair | Literal `\n` output from Hub Boot onward was corrected and verified |
| 2026-07-15 | Seven Chat HQs launched | Chat/Work separation, department boundaries, connector rules, and truthful action reporting became operational |
| 2026-07-10 | Inventory Worker architecture completed | One-row-per-item behavior preserved; pricing and listing work remain separate |
| 2026-07-09 | Formal worker layer implemented | Shared worker standard and Raw Capture Worker package established |

## Parking Lot

- Add a registry reference later if Life Logistics HQ assigns one.
- Evaluate additional workers only after Raw Capture and Inventory pilots produce real evidence.
- Revisit software-backed capture services only if connector-based operation proves insufficient.
- Revisit prompt packaging or canonical prompt storage only if live Chat HQs drift or become difficult to recreate.

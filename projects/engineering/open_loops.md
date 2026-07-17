# Chief Engineering Penny Open Loops

Updated: 2026-07-17

## Open

| Status | Item | Next Action | Notes |
|---|---|---|---|
| Open | Live Trello local authorization | Guide Rob through pulling `main`, refreshing the editable install, creating the ignored `.env`, and adding a read-only Trello API key, token, and Flow Board ID | Adapter is merged; no credential may be committed or pasted into GitHub |
| Open | Trello dashboard verification | Confirm `local-github+trello mode`, real Now / Next / Waiting state, source health, refresh behavior, and accepted scan path on Rob's machine | Test last-good cache behavior later without intentionally destroying valid credentials |
| Open | Penny Inventory Worker pilot | Begin with 2–3 real sale items and verify one-row-per-item writes, stable image references, uncertainty labels, and final Sheet read | Architecture complete; implementation package lives at `workers/penny-inventory/` |
| Open | Penny Raw Capture Worker pilot | Observe real append, canonical-target, timestamp, and verification behavior | Worker package implemented; operational reliability still needs live use |
| Open | Reliable Connector Execution Layer | Turn the design note into an implementation packet outline | Drive doc: `Reliable Connector Execution Layer - Design Note` |
| Open | Operation ledger schema | Draft fields, states, idempotency keys, verification methods, partial-success handling, and recovery instructions | Keep the first schema small enough to test manually |
| Open | Connector health and retry policy | Define read/write health states, bounded retry rules, stop/backoff triggers, and degraded-mode fallback | Trello dashboard cache is now a concrete healthy / stale / unavailable example |
| Open | Worker reliability evidence | Compare real pilot results against `workers/WORKER_STANDARD.md` before proposing more workers | Do not create speculative worker bureaucracy |
| Open | Chat HQ observation | Watch the seven operating HQ chats for routing friction, duplicated authority, stale boot assumptions, connector limits, and wasted model usage | Refine only from observed use |
| Open | Office Leaks delivery architecture | Continue one-problem local-service-office cleanup playbooks as Business requirements mature | Preserve mechanical workflow and human-system layers |
| Open | Business handoff path | Coordinate with Chief Business HQ and Office Leaks Consulting HQ when product or service requirements are ready | Business defines what; Engineering defines how |
| Open | Cost-bearing technical choices | Route hosting, subscriptions, paid APIs, tools, backend workers, queues, or paperwork overlap to Chief of Finance Penny | Finance owns money and paperwork |
| Open | Software repository strategy | Decide whether to move the dashboard into a dedicated software repository if implementation expands materially | Current application remains isolated under `apps/lifeos-dashboard/` |
| Open | Engineering HQ Daily Sync | Keep paused until scheduled execution architecture is more reliable and Rob explicitly resumes it | Do not roll out additional scheduled HQ sync workers |

## Waiting / Deferred

| Status | Item | Owner / Trigger | Notes |
|---|---|---|---|
| Waiting | Todoist and Calendar adapters | Begin after Trello is verified with Rob's real board | Add commitments and schedule pressure without turning the dashboard into a full task manager |
| Waiting | Gmail and Drive adapters | Begin after GitHub, Trello, Todoist, and Calendar data paths are stable | Show attention signals and shortcuts, not full replicas of either system |
| Waiting | Desktop window packaging | Revisit after the browser-based dashboard proves useful across several live sources | Preferred direction is pywebview around the same local FastAPI app |
| Waiting | Deferred prompt-launcher improvements | Revisit when selected for implementation | `/READADVISORY`, `/CONSUMEADVISORY`, and explicit launcher scope metadata are captured in `projects/engineering/notebook/NOTE-20260716-007-prompt-launcher-advisory-commands-and-scope.md` |

## Done / Recently Closed

| Closed Date | Item | Notes |
|---|---|---|
| 2026-07-17 | Live Trello Flow adapter implementation | PR #4 merged as commit `262ebf98eb7e9b84eb95c421dcd1647a7c059d47`; read-only REST source, Now / Next / Waiting normalization, source health, local ignored credentials, last-good cache, documentation, and tests added |
| 2026-07-17 | Trello adapter verification packet | 8 tests passed; compile and local server checks passed; live normalization, order, description parsing, missing credentials, cache fallback, composed sources, and secret-safe errors verified |
| 2026-07-17 | Live local GitHub dashboard adapter | PR #3 merged as commit `62b815608bc19f657922c6e088965c1e3eeab8a2`; local checkout detection, GitHub pulse, live advisories, global priority loops, notebook discovery, recent durable commits, documentation, and tests added |
| 2026-07-17 | Dashboard first-use review | Rob immediately understood the title, source health, current movement, Today, Next, and Waiting; responsive side-by-side layout passed without confusion or visual noise |
| 2026-07-17 | LifeOS Dashboard V0 local launch | Rob created the virtual environment, installed the package, passed 3 original smoke tests, launched the server, and confirmed the dashboard gives an effective at-a-glance view of his life |
| 2026-07-17 | LifeOS Dashboard V0 scaffold | PR #2 merged as commit `bdf920112e8142179d3da91a3e7983e1a5d48c27`; FastAPI app, responsive sample dashboard, adapter boundary, documentation, and tests created |
| 2026-07-17 | Dashboard GitHub-adapter verification | Reconstructed branch package passed 5 tests covering sample mode, local checkout detection, advisory parsing, priority-loop parsing, notebook discovery, and recent activity normalization |
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

# Chief Engineering Penny Open Loops

Updated: 2026-07-17

## Open

| Status | Item | Next Action | Notes |
|---|---|---|---|
| Active | Desktop department automation | Capture the result of the watched Wellness `--send` test using clipboard-based composer verification, then continue in a fresh Engineering HQ chat | Exact chat selection, standardized HQ naming, composer readiness, prompt insertion, and explicit send wiring are proven. Literal `@GitHub` does not resolve into a connector pill, but GPT-5.6 usually retains GitHub context; Rob accepts the occasional recoverable cold-chat failure. Primary scripts: `apps/lifeos-dashboard/automation/open_department_chat.py` and `apps/lifeos-dashboard/automation/draft_department_boot.py`. Full handoff: `projects/engineering/notebook/NOTE-20260717-010-desktop-department-automation-live-send-handoff.md`. Latest patch: `4413fd384572452b05bf36ce3ada7dca55046917` |
| Open | Dashboard auto-refresh | Add a configurable in-page auto-refresh control that reuses the existing refresh path, prevents overlapping refreshes, shows last/next refresh state, and preserves guarded Git sync behavior | Small quality-of-life feature; preferred first version uses a browser-side timer rather than cron or a persistent scheduler |
| Open | Four-source dashboard observation | Confirm ordinary refresh, independent source health, cached degraded operation, and accepted scan path remain useful in real use | Do not intentionally destroy valid credentials merely to demonstrate failure mode |
| Open | Penny Inventory Worker pilot | Begin with 2–3 real sale items and verify one-row-per-item writes, stable image references, uncertainty labels, and final Sheet read | Architecture complete; implementation package lives at `workers/penny-inventory/` |
| Open | Penny Raw Capture Worker pilot | Observe real append, canonical-target, timestamp, and verification behavior | Worker package implemented; operational reliability still needs live use |
| Open | Reliable Connector Execution Layer | Turn the design note into an implementation packet outline | Drive doc: `Reliable Connector Execution Layer - Design Note` |
| Open | Operation ledger schema | Draft fields, states, idempotency keys, verification methods, partial-success handling, and recovery instructions | Keep the first schema small enough to test manually |
| Open | Connector health and retry policy | Define read/write health states, bounded retry rules, stop/backoff triggers, and degraded-mode fallback | Trello, Todoist, and Calendar caches plus guarded Git sync are concrete healthy / stale / unavailable / blocked examples |
| Open | Worker reliability evidence | Compare real pilot results against `workers/WORKER_STANDARD.md` before proposing more workers | Do not create speculative worker bureaucracy |
| Open | Chat HQ observation | Watch the seven operating HQ chats for routing friction, duplicated authority, stale boot assumptions, connector limits, and wasted model usage | Refine only from observed use |
| Open | Office Leaks delivery architecture | Continue one-problem local-service-office cleanup playbooks as Business requirements mature | Preserve mechanical workflow and human-system layers |
| Open | Business handoff path | Coordinate with Chief Business HQ and Office Leaks Consulting HQ when product or service requirements are ready | Business defines what; Engineering defines how |
| Open | Cost-bearing technical choices | Route hosting, subscriptions, paid APIs, tools, backend workers, queues, or paperwork overlap to Chief of Finance Penny | Finance owns money and paperwork |
| Open | Software repository strategy | Keep LifeOS as the runtime mirror and use separate repositories for educational and future standalone projects | Revisit dashboard extraction only if implementation expands materially |
| Open | Engineering HQ Daily Sync | Keep paused until scheduled execution architecture is more reliable and Rob explicitly resumes it | Do not roll out additional scheduled HQ sync workers |

## Waiting / Deferred

| Status | Item | Owner / Trigger | Notes |
|---|---|---|---|
| Waiting | Gmail dashboard adapter | First client, multiple active leads, repeated manual inbox checking, or demonstrated risk of missing a client message | Current Gmail use is mostly Indeed notices, authorizations, and reminders already handled through Main Assistant queries |
| Waiting | Drive dashboard adapter | Recurring client folders, proposals, deliverables, approvals, or working documents that need dashboard shortcuts | Current Drive use does not justify another adapter |
| Waiting | Desktop window packaging | Revisit after the browser-based dashboard proves useful across several live sources | Preferred direction is pywebview around the same local FastAPI app |
| Waiting | Deferred prompt-launcher improvements | Revisit after the desktop automation foundation is proven and ready for a control surface | `/READADVISORY`, `/CONSUMEADVISORY`, and explicit launcher scope metadata are captured in `projects/engineering/notebook/NOTE-20260716-007-prompt-launcher-advisory-commands-and-scope.md` |

## Done / Recently Closed

| Closed Date | Item | Notes |
|---|---|---|
| 2026-07-17 | Guarded GitHub auto-sync | PR #7 merged as `e6059a8ffbb056e308e5e509b89ae2ad2f413edd`; clean `main` fast-forwards on load and refresh, while dirty, ahead, diverged, detached, and uncertain states refuse to move |
| 2026-07-17 | Guarded GitHub auto-sync local validation | Full suite passed with 16 tests; dashboard reported `GitHub healthy · main · e6059a8 · clean · up to date` |
| 2026-07-17 | Windows timezone dependency repair | PR #6 merged as `366b2151e0155cbf2164c12a7384ff701043561f`; `tzdata` is now a runtime dependency for reliable `America/Chicago` resolution on Windows |
| 2026-07-17 | Todoist dashboard authorization | Rob stored the personal token only in ignored local `.env`; dashboard verified 2 today, 0 overdue, 7 upcoming, and real task titles and priority badges |
| 2026-07-17 | Google Calendar dashboard authorization | Rob stored the private iCal URL only in ignored local `.env`; dashboard verified 13 upcoming and correctly parsed the next NA meeting title, relative date, time, and location |
| 2026-07-17 | Today dashboard local regression | Full four-source launch passed after dependency installation; GitHub, Trello, Todoist, and Calendar remained healthy and live |
| 2026-07-17 | Todoist and Calendar adapter implementation | PR #5 merged as commit `c7fc7d795abca8ddf56e964b36ea7bd86cc6cd17`; read-only Todoist and private-iCal Calendar sources, independent caches, recurrence expansion, timezone normalization, documentation, and focused tests added |
| 2026-07-17 | Live Trello local authorization | Rob configured an ignored local `.env` with a read-only token and verified healthy live access |
| 2026-07-17 | Trello dashboard verification | Real Now / Next / Waiting state, lane parsing, ordering, blocker reasons, and source health passed Rob's local review |
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

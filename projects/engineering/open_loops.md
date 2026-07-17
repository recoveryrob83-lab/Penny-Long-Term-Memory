# Engineering HQ Open Loops

Updated: 2026-07-17

## Open

| Status | Item | Next Action | Notes |
|---|---|---|---|
| Active | Desktop department automation maintenance | Use the validated automation in normal on-demand operation; change selectors, navigation recovery, verification, or send behavior only after a demonstrated failure or material UI change | All seven HQs passed draft-mode validation and one watched live send to Main Assistant HQ succeeded. Preserve exact navigation, occupied-composer protection, clipboard round-trip verification, explicit `--send`, and stop-on-uncertainty behavior. Canonical launcher: `apps/lifeos-dashboard/automation/draft_department_boot.py`. Recovery playbook: `projects/engineering/notebook/NOTE-20260717-011-chatgpt-ui-automation-lessons-and-recovery-playbook.md` |
| Open | Dashboard auto-refresh | Add a configurable in-page auto-refresh control only if ordinary use still demonstrates value | Reuse the existing refresh path, prevent overlaps, show last/next refresh state, and preserve guarded Git sync |
| Open | Four-source dashboard observation | Confirm ordinary refresh, independent source health, cached degraded operation, and accepted scan path remain useful in real use | Do not intentionally destroy valid credentials merely to demonstrate failure mode |
| Open | Penny Inventory Worker pilot | Begin with 2–3 real sale items and verify one-row-per-item writes, stable image references, uncertainty labels, and final Sheet read | Architecture complete; package lives at `workers/penny-inventory/` |
| Open | Penny Raw Capture Worker pilot | Observe real append, canonical-target, timestamp, and verification behavior | Worker package implemented; operational reliability still needs live use |
| Open | Reliable Connector Execution Layer | Turn the design note into an implementation packet outline | Drive doc: `Reliable Connector Execution Layer - Design Note` |
| Open | Operation ledger schema | Draft fields, states, idempotency keys, verification methods, partial-success handling, and recovery instructions | Keep the first schema small enough to test manually |
| Open | Connector health and retry policy | Define read/write health states, bounded retry rules, stop/backoff triggers, and degraded-mode fallback | Dashboard caches, guarded Git sync, and desktop automation safety gates provide concrete examples |
| Open | Worker reliability evidence | Compare real pilot results against `workers/WORKER_STANDARD.md` before proposing more workers | Do not create speculative worker bureaucracy |
| Open | Chat HQ observation | Watch the seven HQ chats for routing friction, duplicated authority, stale boot assumptions, connector limits, and wasted model usage | Refine only from observed use |
| Open | Office Leaks delivery architecture | Continue one-problem local-service-office cleanup playbooks as Business requirements mature | Preserve mechanical workflow and human-system layers |
| Open | Business handoff path | Coordinate with Business HQ and Office Leaks HQ when product or service requirements are ready | Business defines what; Engineering defines how |
| Open | Cost-bearing technical choices | Route hosting, subscriptions, paid APIs, tools, backend workers, queues, or paperwork overlap to Finance HQ | Finance owns money and paperwork |
| Open | Software repository strategy | Keep LifeOS as the runtime mirror and use separate repositories for educational and future standalone projects | Revisit dashboard extraction only if implementation expands materially |
| Open | Engineering HQ Daily Sync | Keep paused until scheduled execution architecture is more reliable and Rob explicitly resumes it | Validated on-demand desktop automation does not authorize unattended scheduling |

## Waiting / Deferred

| Status | Item | Owner / Trigger | Notes |
|---|---|---|---|
| Waiting | Gmail dashboard adapter | First client, multiple active leads, repeated manual inbox checking, or demonstrated risk of missing a client message | Current Gmail use does not justify another adapter |
| Waiting | Drive dashboard adapter | Recurring client folders, proposals, deliverables, approvals, or working documents that need dashboard shortcuts | Current Drive use does not justify another adapter |
| Waiting | Desktop window packaging | Revisit after the browser-based dashboard proves useful across sustained real use | Preferred direction remains a thin desktop shell around the same local app |
| Waiting | Deferred prompt-launcher improvements | Revisit after current automation and launcher behavior produce a concrete need | `/READADVISORY`, `/CONSUMEADVISORY`, and explicit launcher scope metadata remain captured in `projects/engineering/notebook/NOTE-20260716-007-prompt-launcher-advisory-commands-and-scope.md` |

## Done / Recently Closed

| Closed Date | Item | Notes |
|---|---|---|
| 2026-07-17 | Desktop department automation full validation | All seven HQs passed draft tests across visible and hidden chats, empty and occupied composers, canonical prompt insertion, clipboard verification, and draft preservation |
| 2026-07-17 | Watched Main Assistant live send | Exact destination, composer, payload, and explicit send gates passed; prompt submitted exactly once and Main Assistant began rebooting |
| 2026-07-17 | Earlier Wellness loading failure | Resolved through bounded loading recovery, Group-composer architecture, verification shims, and subsequent successful seven-HQ validation |
| 2026-07-17 | NOTE-010 desktop automation handoff | Closed as completed and validated; NOTE-011 now holds the durable architecture and recovery playbook |
| 2026-07-17 | Logistics boot-path repair | Corrected `projects/life-logistics` to `projects/life-logistics-hq` and routed the legacy wrapper through the canonical launcher |
| 2026-07-17 | Guarded GitHub auto-sync | Clean `main` fast-forwards on load and refresh; dirty, ahead, diverged, detached, and uncertain states refuse to move |
| 2026-07-17 | Dashboard four-source validation | Full suite passed with 16 tests; GitHub, Trello, Todoist, and Calendar remained healthy and live |
| 2026-07-17 | Windows timezone dependency repair | `tzdata` is a runtime dependency for reliable `America/Chicago` resolution |
| 2026-07-17 | ADV-20260717-040 implemented / acknowledged / closed | Logistics reconciled shared global summaries after the dashboard milestone |
| 2026-07-16 | ADV-20260716-038 acknowledged / ingested / closed | Engineering accepted the read-mostly dashboard concept while preserving source systems |
| 2026-07-16 | Prompt launcher newline repair | Literal newline output was corrected and verified |
| 2026-07-15 | Seven Chat HQs launched | Chat/Work separation, department boundaries, connector rules, and truthful action reporting became operational |

## Parking Lot

- Add registry references later if Logistics assigns them.
- Evaluate additional workers only after Raw Capture and Inventory pilots produce real evidence.
- Revisit software-backed capture services only if connector-based operation proves insufficient.
- Revisit unattended department scheduling only after explicit authorization and a separate safe scheduling architecture.

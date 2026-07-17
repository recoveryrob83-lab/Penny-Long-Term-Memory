# Engineering HQ Open Loops

Updated: 2026-07-17

## Open

| Status | Item | Next Action | Notes |
|---|---|---|---|
| Priority | Department ownership architecture and dashboard inspection | Formalize open-loop ownership, role-routed boot context, cross-department routing, and lifecycle procedures; then add a Department Inspection tab between Overview and Automation | Aggregate all seven departments' loops, notebooks, logs, and status records with department, status, priority, date, type, search, and sort filters. Preserve department files as authoritative and keep system loops limited to genuinely shared work. Canonical note: `NOTE-20260717-014-department-ownership-and-dashboard-inspection.md` |
| Active | Scheduled occupied-composer safety validation | Complete the Logistics HQ scheduled failure test and record the visible behavior plus dashboard result | Destination is behind `Show more`; harmless text is deliberately present in the composer. Expected: exact navigation, preserved draft, no send, clear occupied-composer failure |
| Active | Collapsed LifeOS project-folder recovery | Design bounded exact-project detection and one-time expansion, but do not change code until Rob authorizes it | ChatGPT Classic may collapse the project after restart or narrow-window layout. Current workaround is to leave the app open with the LifeOS project expanded |
| Active | Canonical prompt catalog | Reconcile authoritative command definitions and populate the protected canonical registry | Current catalog primarily exposes Boot. Candidate families: Boot variants, Sync, Nightly, Advisory, Sync Advisory, Read Advisory, Consume Advisory |
| Open | Restart and overdue-run validation | Schedule a one-time draft, stop the dashboard before execution, restart afterward, and observe catch-up behavior | Decide whether late jobs should run immediately, skip, expire, or require approval only after evidence |
| Open | Recurring second-occurrence validation | Observe the next real daily or weekly occurrence | First daily LifeOS HQ run succeeded and advanced correctly; a second occurrence is still needed to prove sustained recurrence |
| Open | Scheduler production preflight | Define health visibility, missed-run policy, and unattended operating requirements | Consider ChatGPT availability, expanded-project state, upcoming/overdue visibility, execution window, and Windows startup/service packaging |
| Active | Desktop department automation maintenance | Use the validated automation in normal operation; change selectors or recovery only after demonstrated failure or material UI change | Preserve exact navigation, occupied-composer protection, clipboard verification, explicit send, one-job lock, and stop-on-uncertainty behavior |
| Open | Dashboard auto-refresh | Add a configurable in-page auto-refresh control only if ordinary use still demonstrates value | Reuse the existing refresh path, prevent overlaps, show last/next refresh state, and preserve guarded Git sync |
| Open | Four-source dashboard observation | Confirm ordinary refresh, independent source health, cached degraded operation, and accepted scan path remain useful in real use | Do not intentionally destroy valid credentials merely to demonstrate failure mode |
| Open | Penny Inventory Worker pilot | Begin with 2–3 real sale items and verify one-row-per-item writes, stable image references, uncertainty labels, and final Sheet read | Architecture complete; package lives at `workers/penny-inventory/` |
| Open | Penny Raw Capture Worker pilot | Observe real append, canonical-target, timestamp, and verification behavior | Worker package implemented; operational reliability still needs live use |
| Open | Reliable Connector Execution Layer | Turn the design note into an implementation packet outline | Drive doc: `Reliable Connector Execution Layer - Design Note` |
| Open | Operation ledger schema | Draft fields, states, idempotency keys, verification methods, partial-success handling, and recovery instructions | Keep the first schema small enough to test manually |
| Open | Connector health and retry policy | Define read/write health states, bounded retry rules, stop/backoff triggers, and degraded-mode fallback | Dashboard caches, guarded Git sync, desktop automation safety gates, and Command Center results provide concrete examples |
| Open | Worker reliability evidence | Compare real pilot results against `workers/WORKER_STANDARD.md` before proposing more workers | Do not create speculative worker bureaucracy |
| Open | Chat HQ observation | Watch the seven HQ chats for routing friction, duplicated authority, stale boot assumptions, connector limits, and wasted model usage | Refine only from observed use |
| Open | Office Leaks delivery architecture | Continue one-problem local-service-office cleanup playbooks as Business requirements mature | Preserve mechanical workflow and human-system layers |
| Open | Cost-bearing technical choices | Route hosting, subscriptions, paid APIs, tools, backend workers, queues, or paperwork overlap to Finance HQ | Finance owns money and paperwork |
| Open | Software repository strategy | Keep LifeOS as the runtime mirror and use separate repositories for educational and future standalone projects | Revisit dashboard extraction only if implementation expands materially |
| Paused | Engineering HQ Daily Sync | Keep paused until the scheduler's recovery and missed-run behavior are production-safe and Rob explicitly resumes it | Scheduling now exists, but this specific unattended production task is not yet reauthorized |

## Waiting / Deferred

| Status | Item | Owner / Trigger | Notes |
|---|---|---|---|
| Waiting | Automatic ChatGPT launch and richer recovery | Demonstrated need after current scheduling validation | Screenshots, notifications, diagnostic bundles, and automatic launch remain later work |
| Waiting | Gmail dashboard adapter | First client, multiple active leads, repeated manual inbox checking, or demonstrated risk of missing a client message | Current Gmail use does not justify another adapter |
| Waiting | Drive dashboard adapter | Recurring client folders, proposals, deliverables, approvals, or working documents that need dashboard shortcuts | Current Drive use does not justify another adapter |
| Waiting | Desktop window packaging | Sustained browser usefulness and a clear unattended-runtime requirement | Preferred direction remains a thin desktop shell or Windows service around the same local app |
| Waiting | Deferred prompt-launcher improvements | Concrete operational need | `/READADVISORY`, `/CONSUMEADVISORY`, and explicit launcher scope metadata remain captured in NOTE-007 |

## Done / Recently Closed

| Closed Date | Item | Notes |
|---|---|---|
| 2026-07-17 | Automation Command Center manual Phase 1 | Eight destinations, canonical/saved/custom prompts, draft/send mode, explicit send confirmation, one-job lock, global pause, structured results, and local history implemented |
| 2026-07-17 | Saved prompt lifecycle and destination safeguards | Duplicate, save, edit, restore default destination, mismatch acknowledgement, update default, and delete validated in the UI |
| 2026-07-17 | One-time scheduling implementation | Persistent once-only jobs implemented with schedule editing, pause/resume, deletion, and completion state |
| 2026-07-17 | Recurring scheduling implementation | Persistent daily and weekly scheduling implemented in `America/Chicago` |
| 2026-07-17 | One-time Engineering live-send validation | `Hi Penny Test` succeeded and completed with no future run |
| 2026-07-17 | First daily LifeOS live-send validation | `Hi Penny LifeOS Test` succeeded and advanced to 2026-07-18 15:05 CT |
| 2026-07-17 | Mobile concurrency validation | Mobile chat activity and active response generation did not interfere with the scheduled desktop send to another HQ |
| 2026-07-17 | Automation Command Center plan | Defined the original safety contract, job model, activity logging, and phased scheduling architecture |
| 2026-07-17 | Desktop department automation full validation | All seven HQs passed draft tests across visible and hidden chats, empty and occupied composers, canonical prompt insertion, clipboard verification, and draft preservation |
| 2026-07-17 | Guarded GitHub auto-sync | Clean `main` fast-forwards on load and refresh; dirty, ahead, diverged, detached, and uncertain states refuse to move |
| 2026-07-17 | Dashboard four-source validation | GitHub, Trello, Todoist, and Calendar remained healthy and live |

## Parking Lot

- Add registry references later if Logistics assigns them.
- Evaluate additional workers only after Raw Capture and Inventory pilots produce real evidence.
- Revisit software-backed capture services only if connector-based operation proves insufficient.

# Engineering HQ Open Loops

Updated: 2026-07-18

## Open

| Status | Priority | Item | Next Action | Notes |
|---|---|---|---|---|
| Active | High | Department ownership architecture and dashboard inspection | Observe ordinary role-routed specialist boots and close the system wrapper when operation remains clean | Department Inspection is locally validated. Live evidence progressed from 458 records / 4 findings / 101 warnings to 459 / 4 / 15 after tuning, 414 / 0 / 13 after source cleanup, and 414 / 0 / 0 after warning audit, evidence-backed parser correction, and explicit Logistics status normalization. Approved schema: `apps/lifeos-dashboard/DEPARTMENT_INSPECTION_DATA_CONTRACT.md`. Canonical note: `NOTE-20260717-014-department-ownership-and-dashboard-inspection.md` |
| Active | Normal | Canonical prompt catalog | Reconcile authoritative command definitions and populate the protected canonical registry | Current catalog primarily exposes Boot. Candidate families: Boot variants, Sync, Nightly, Advisory, Sync Advisory, Read Advisory, Consume Advisory |
| Open | Normal | Scheduler production preflight | Define health visibility, missed-run policy, failed one-time retry behavior, and unattended operating requirements | Overdue one-time work catches up immediately after restart, records the result, disables after one attempt, and does not retry automatically. Clipboard-safe restart execution and a bounded two-run recurrence both pass |
| Active | Normal | Desktop department automation maintenance | Use the validated automation in normal operation; change selectors or recovery only after demonstrated failure or material UI change | Preserve exact navigation, occupied-composer protection, stable clipboard lifetime through write verification, clipboard restoration, explicit send, one-job lock, and stop-on-uncertainty behavior |
| Open | Normal | Dashboard auto-refresh | Add a configurable in-page auto-refresh control only if ordinary use still demonstrates value | Reuse the existing refresh path, prevent overlaps, show last/next refresh state, and preserve guarded Git sync |
| Open | Normal | Four-source dashboard observation | Confirm ordinary refresh, independent source health, cached degraded operation, and accepted scan path remain useful in real use | Do not intentionally destroy valid credentials merely to demonstrate failure mode |
| Open | Normal | Penny Inventory Worker pilot | Begin with 2–3 real sale items and verify one-row-per-item writes, stable image references, uncertainty labels, and final Sheet read | Architecture complete; package lives at `workers/penny-inventory/` |
| Open | Normal | Penny Raw Capture Worker pilot | Observe real append, canonical-target, timestamp, and verification behavior | Worker package implemented; operational reliability still needs live use |
| Open | Normal | Reliable Connector Execution Layer | Turn the design note into an implementation packet outline | Drive doc: `Reliable Connector Execution Layer - Design Note` |
| Open | Normal | Operation ledger schema | Draft fields, states, idempotency keys, verification methods, partial-success handling, and recovery instructions | Keep the first schema small enough to test manually |
| Open | Normal | Connector health and retry policy | Define read/write health states, bounded retry rules, stop/backoff triggers, and degraded-mode fallback | Dashboard caches, guarded Git sync, desktop automation safety gates, and Command Center results provide concrete examples |
| Open | Normal | Worker reliability evidence | Compare real pilot results against `workers/WORKER_STANDARD.md` before proposing more workers | Do not create speculative worker bureaucracy |
| Open | Normal | Office Leaks delivery architecture | Continue one-problem local-service-office cleanup playbooks as Business requirements mature | Preserve mechanical workflow and human-system layers |
| Open | Normal | Cost-bearing technical choices | Route hosting, subscriptions, paid APIs, tools, backend workers, queues, or paperwork overlap to Finance HQ | Finance owns money and paperwork |
| Open | Normal | Software repository strategy | Keep LifeOS as the runtime mirror and use separate repositories for educational and future standalone projects | Revisit dashboard extraction only if implementation expands materially |
| Paused | Low | Engineering HQ Daily Sync | Keep paused until the scheduler's recovery and missed-run behavior are production-safe and Rob explicitly resumes it | Scheduling now exists, but this specific unattended production task is not yet reauthorized |

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
| 2026-07-18 | Completed recurrence placement UI validation | Rob confirmed the completed two-run debug definition no longer appears under Upcoming, both executions remain in Execution Record, and the bounded UI fix behaves as intended |
| 2026-07-18 | Bounded five-minute recurrence runtime validation | Rob confirmed both scheduled draft runs succeeded, the second run occurred on the five-minute repeat, the schedule card showed `Completed`, no future run remained, and no third run occurred |
| 2026-07-18 | Bounded five-minute recurrence control implementation | Added a `debug_5m` scheduler cadence with draft-only enforcement, one five-minute repeat, automatic completion after two attempts, completed-test resume refusal, visible 0/2 and 1/2 states, and focused regression coverage without changing the SQLite schema |
| 2026-07-18 | Clipboard write-verification repair runtime validation | Rob confirmed the repeated overdue draft pasted the full intended text, preserved the prior clipboard value `i`, and recorded `succeeded` in Run History. The repair keeps the prompt on the clipboard through verification and restores the original clipboard afterward |
| 2026-07-18 | Clipboard race and failure-misclassification diagnosis | Raw execution data proved ChatGPT Classic, Engineering HQ, and the composer were all verified. Clipboard verification copied only the prior one-character value, and the explicit `write_verification_failed` marker was overridden by broad keyword matching. The earlier startup-window diagnosis was rejected |
| 2026-07-18 | Overdue one-time scheduler catch-up validation | A draft-only Engineering schedule persisted while the dashboard was stopped, became overdue, fired once about 15–20 seconds after restart, recorded its failed downstream automation result, disabled the one-time schedule, and did not retry automatically |
| 2026-07-18 | Package C Department Inspection naming validation | Rob confirmed the dashboard displayed Chief of Staff HQ and Life OS Maintenance HQ correctly, and the focused Department Inspection suite completed with 9 passing tests |
| 2026-07-18 | Package B retired-title compatibility runtime validation | Rob confirmed a draft-only invocation using `Main Assistant HQ` translated to Chief of Staff HQ and preserved exact-destination verification without sending |
| 2026-07-18 | Package B canonical target runtime validation | Rob confirmed draft-only automation passed for Chief of Staff HQ and Life OS Maintenance HQ; existing schedules and run history displayed the correct canonical names with stable destination keys and no persisted-record migration |
| 2026-07-18 | Package B GitHub implementation | Canonical chat-title mappings, visible Automation labels, run-history and scheduler labels, mapping tests, and a bounded retired-title compatibility bridge were committed without changing stable destination keys or persisted records |
| 2026-07-18 | Department Inspection zero-warning verification | Rob confirmed 414 normalized records, zero findings, and zero warnings after notebook-status parser correction and explicit Logistics `Paused | Low` normalization; the result preserved conservative detection rather than suppressing ambiguity |
| 2026-07-18 | Department Inspection post-cleanup verification | Rob confirmed 414 normalized records, zero findings, and 13 warnings after source cleanup; all four confirmed findings disappeared without weakening detection |
| 2026-07-18 | Department Inspection first source cleanup | Separated Engineering lifecycle state from priority, removed the duplicated broad Chat HQ watch, consolidated Legacy VA folder disposition under Logistics, and removed speculative registry-reference placeholders from open-loop files |
| 2026-07-18 | Department Inspection MVP local validation | Rob confirmed the new tab works in the local Windows dashboard after guarded GitHub synchronization and server restart; live classification audit remains open under the broader ownership package |
| 2026-07-17 | Scheduled occupied-composer safety validation | A scheduled custom send to Logistics HQ found the exact destination behind `Show more`, preserved the existing draft, sent nothing, recorded `failed`, and displayed the explicit occupied-composer recovery message in Run History |
| 2026-07-17 | Automation Command Center manual Phase 1 | Eight destinations, canonical/saved/custom prompts, draft/send mode, explicit send confirmation, one-job lock, global pause, structured results, and local history implemented |
| 2026-07-17 | Saved prompt lifecycle and destination safeguards | Duplicate, save, edit, restore default destination, mismatch acknowledgement, update default, and delete validated in the UI |
| 2026-07-17 | One-time scheduling implementation | Persistent once-only jobs implemented with schedule editing, pause/resume, deletion, and completion state |
| 2026-07-17 | Recurring scheduling implementation | Persistent daily and weekly scheduling implemented in `America/Chicago` |
| 2026-07-17 | One-time Engineering live-send validation | `Hi Penny Test` succeeded and completed with no future run |
| 2026-07-17 | First daily LifeOS live-send validation | `Hi Penny LifeOS Test` succeeded and advanced to 2026-07-18 15:05 CT |
| 2026-07-17 | Mobile concurrency validation | Mobile chat activity and active response generation did not interfere with scheduled desktop execution |
| 2026-07-17 | Automation Command Center plan | Defined the original safety contract, job model, activity logging, and phased scheduling architecture |
| 2026-07-17 | Desktop department automation full validation | All seven HQs passed draft tests across visible and hidden chats, empty and occupied composers, canonical prompt insertion, clipboard verification, and draft preservation |
| 2026-07-17 | Guarded GitHub auto-sync | Clean `main` fast-forwards on load and refresh; dirty, ahead, diverged, detached, and uncertain states refuse to move |
| 2026-07-17 | Dashboard four-source validation | GitHub, Trello, Todoist, and Calendar remained healthy and live |

## Parking Lot

- Evaluate additional workers only after Raw Capture and Inventory pilots produce real evidence.
- Revisit software-backed capture services only if connector-based operation proves insufficient.

# Engineering_HQ Open Loops

Updated: 2026-07-23

## Open

| Status | Priority | Item | Next Action | Notes |
|---|---|---|---|---|
| Active | High | Post-merge dashboard smoke and route-management observation | In the fresh `Engineering_HQ` chat, Boot and Sync first, confirm local `main` is clean and contains merge `2587b540e24ca09036c1f0094187c69c2b363c63` or later, start or confirm the dashboard, inspect `/api/health` and Worker Operations, and verify one `engineering_worker` row at route revision `1` with availability `available` | This is a read-only operational smoke check. Confirm the guarded route controls render. Do not capture or roll the route unless a replacement Worker room actually exists and Rob explicitly authorizes the change. Dashboard startup does not authorize real Worker dispatch, schedules, or unattended local orchestrator sends |
| Waiting | Normal | ADV-20260723-052 Chief_of_Staff_HQ watcher destination test | Wait for Rob to confirm whether the hourly watcher reports the advisory in the existing `Chief_of_Staff_HQ` conversation without spawning a new chat or triggering work | Advisory remains OPEN on the Engineering source board. The cloud watcher is separate from the local Worker courier. No Worker dispatch, dashboard execution, connector write, follow-on work, or automatic closure is authorized |
| Active | High | Department ownership architecture and dashboard inspection | Observe corrected role-routed boots and inspect demonstrated identity, ownership, or source-board defects before closing the remaining system wrapper | ADV-20260719-044 is closed. Department Inspection remains locally validated at 414 normalized records, zero findings, and zero warnings. Remaining work is ordinary post-repair observation under `NOTE-20260717-014-department-ownership-and-dashboard-inspection.md` |
| Active | Normal | Browser and Worker transport maintenance | Observe ordinary post-Package E runs and repair only demonstrated transport defects without weakening exact URL, hydration, composer, submission, one-tab, one-shot claim, route-revision, or stop-on-uncertainty safeguards | Canonical title rollover, post-navigation verifier repair, direct URL routing, and guarded route capture are complete. Future changes require demonstrated evidence and bounded authority. Never blind-retry uncertain submissions |
| Open | Normal | Dashboard auto-refresh | Add a configurable in-page auto-refresh control only if ordinary use still demonstrates value | Reuse the existing refresh path, prevent overlaps, show last and next refresh state, and preserve guarded Git sync |
| Open | Normal | Four-source dashboard observation | Confirm ordinary refresh, independent source health, cached degraded operation, and accepted scan paths remain useful in real use | Do not intentionally destroy valid credentials merely to demonstrate failure mode |
| Open | Normal | Penny Inventory Worker pilot | Begin with 2–3 real sale items and verify one-row-per-item writes, stable image references, uncertainty labels, and final Sheet read-back | Grandfathered compatibility package remains at `workers/penny-inventory/`; evaluate it under the canonical Worker contract without treating its path as the model for new Workers |
| Open | Normal | Penny Raw Capture Worker pilot | Observe real append, canonical-target, timestamp, and verification behavior | Grandfathered compatibility package remains at `workers/penny-raw-capture/`; operational reliability still needs live use |
| Open | Normal | Reliable Connector Execution Layer | Turn the design note into an implementation packet outline only when Rob authorizes the next build package | Align any future design with immutable evidence, HQ verification, signed consumption, bounded retries, one authoritative operational ledger, and direct registered routes. Do not reopen Package E implicitly |
| Open | Normal | Connector health and retry policy | Define read and write health states, bounded retry rules, stop and backoff triggers, and degraded-mode fallback when a concrete implementation package is authorized | Use dashboard caches, guarded Git sync, browser safety gates, Worker duplicate suppression, route holds, one-shot HQ wake claims, and verified connector read-back as evidence patterns |
| Open | Normal | Worker reliability evidence | Compare synthetic and real pilot results against `coordination/WORKER_EXECUTION_CONTRACT.md` before proposing additional Workers | Package E and the direct-route pilot proved the Engineering Worker path. Cross-department rollout remains deferred and must not be inferred from pilot success |
| Open | Normal | Office Leaks delivery architecture | Continue one-problem local-service-office cleanup playbooks as Business requirements mature | Preserve mechanical workflow and human-system layers |
| Open | Normal | Cost-bearing technical choices | Route hosting, subscriptions, paid APIs, tools, backend workers, queues, or paperwork overlap to `Finance_HQ` | Finance owns money and paperwork |
| Open | Normal | Software repository strategy | Keep LifeOS as the runtime mirror and use separate repositories for educational and future standalone projects | Revisit dashboard extraction only if implementation expands materially |
| Paused | Low | Optional Python canonical source resolver | Do not implement unless operational evidence demonstrates a concrete reliability, security, or scale gap outside existing deterministic parsing | Python may provide defense in depth but is not the Worker and must not become the owner or interpreter of department judgment |
| Paused | Low | Canonical prompt transport verification | Do not resume the general composer investigation without demonstrated failure | Preserve validated marker, hydration, exact-destination, strict new-turn witness, direct-route, route-revision, and one-tab paths. Full-text equality and broad focus or timeout experiments remain out of scope |
| Paused | Low | Engineering_HQ Daily Sync | Keep paused until Rob explicitly resumes it | Scheduler production reliability is live-validated. This unattended task remains paused by deliberate operating choice, not an unresolved technical gate |

## Waiting / Deferred

| Status | Item | Owner / Trigger | Notes |
|---|---|---|---|
| Waiting | Cross-department Worker result-outbox adoption | `Maintenance_HQ` shared-contract review plus explicit authorization from each owning department | Package E closed as an Engineering-only pilot. No universal Worker write authority or cross-department activation was created |
| Deferred | Human-readable Worker envelope summary | Rob authorizes a future usability enhancement after demonstrated need | Package E closeout explicitly deferred this display-only enhancement. JSON remains authoritative; no safety or authority dependency may be placed on a separate display copy |
| Waiting | Gmail dashboard adapter | First client, multiple active leads, repeated manual inbox checking, or demonstrated risk of missing a client message | Current Gmail use does not justify another adapter |
| Waiting | General Drive dashboard adapter | Recurring client folders, proposals, deliverables, approvals, or working documents needing dashboard shortcuts | The bounded scheduler Sheet mirror is separate and implemented; general Drive browsing remains deferred |
| Waiting | Desktop window or service packaging | Sustained dashboard usefulness and a clear unattended-runtime requirement | Preferred direction remains a thin desktop shell or Windows service around the same local application |
| Waiting | Deferred prompt-launcher improvements | Concrete operational need | The old classroom launcher remains secondary. Worker Operations carries the active execution surface |

## Done / Recently Closed

| Closed Date | Item | Notes |
|---|---|---|
| 2026-07-23 | Guarded dashboard Worker route capture and rollover | PR #11 squash-merged as `2587b540e24ca09036c1f0094187c69c2b363c63`. Dashboard capture updates one existing Worker row, checks the current revision and Worker title, refuses duplicate ownership, places changed routes on `unknown` hold, and promotes only an unchanged route after a successful zero-authority canary. Final consolidated regression gate: `80 passed`. No production route rollover occurred during implementation |
| 2026-07-23 | Authoritative direct Worker URL routing | PR #10 squash-merged as `b859c3c72e8b82f876b9ebf72d2961f4eb33ecbd`. Browser dispatch now uses the exact URL stored in the existing Worker registry row, fails closed without it, and never relies on sidebar discovery. Production `engineering_worker` route revision `1` was live-canary verified and promoted to `available` |
| 2026-07-23 | Canonical runtime title rollover and courier verifier repair | PR #9 squash-merged as `f8cc341e17cb68492c5f66339382b753bd1612ab`. Engineering executable surfaces and active title-bearing SQLite state now use canonical underscore titles. Post-navigation identity no longer depends on selected sidebar visibility, and virtualized-history submission proof was repaired without rewriting historical evidence |
| 2026-07-23 | Maintenance_HQ textual naming repair ingested | Maintenance normalized current GitHub documents to the canonical underscore room-title standard while preserving executable Engineering surfaces, runtime databases, tests, historical evidence, immutable Worker artifacts, and stable filesystem paths for the separate Engineering rollover |
| 2026-07-23 | Package E: Worker Dispatch, Result Outbox, HQ Verification, and CoS Consumption | Closed by Rob after the Engineering-only pilot proved dispatch-only Worker wakes, immutable reports, deterministic same-row ingestion, rejection and repair mechanics, owning-HQ receipts, Rob validation, consumption readiness, scheduled watcher reporting, source-owner lifecycle separation, and duplicate HQ-wake suppression. Canonical closeout: `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md` |
| 2026-07-23 | ADV-20260723-051 HQ-wake receipt test | Closed after Worker report, immutable `VERIFIED` HQ review, `HQ_VERIFIED` runtime reconciliation, and live post-repair duplicate-wake suppression |
| 2026-07-23 | ADV-20260722-049 Rob-validation proof | Closed after Engineering HQ correctly required Rob validation, Rob verified the exact observation marker, and the result became consumption-ready |
| 2026-07-23 | ADV-20260721-048 immutable result-outbox pilot | Closed after deterministic ingestion and an immutable Engineering HQ `VERIFIED` receipt made the result consumption-ready |
| 2026-07-23 | ADV-20260720-047 response-reconciliation pilot | Closed as architecture-discovery evidence superseded by completed Package E implementation. Revision 2 was not retried |
| 2026-07-23 | HQ-wake duplicate-suppression repair | Git-first HQ receipt ingestion and an atomic one-shot wake claim prevented repeated HQ messages. The live dashboard reconciled ADV-051 without another wake and continued quiet polling |
| 2026-07-21 | Package E Slice 3 live immutable outbox proof | ADV-048 created one immutable schema-valid report under exact authority. Later Slice 4 ingestion and HQ review completed the previously pending acceptance path |
| 2026-07-20 | Package D: Operations-Procedure and Worker-Runtime Implementation | Closed after Slices 1–7, synthetic transport evidence, Engineering Worker profile and procedure, and the live ADV-046 pilot completed with same-row receiver acceptance and verified HQ review |
| 2026-07-19 | ADV-20260719-044 shared Worker filesystem and continuity reconciliation | Maintenance implemented and verified the filesystem, boot, ownership, and continuity repair |
| 2026-07-18 | Scheduler production reliability runtime validation | Failed runs pause without blind retry; Resume rearms; cloud health becomes overdue; restart handles stale one-time jobs safely; cleanup and ledger synchronization were validated |
| 2026-07-18 | Department Inspection zero-warning verification | Department Inspection reached 414 normalized records, zero findings, and zero warnings while preserving conservative detection |

## Boundary

- Package E is closed. Do not recreate its completed slice tasks as active loops.
- The title rollover, courier verifier repair, direct URL routing, and route-management controls are complete. Do not keep them open merely for visibility.
- Future defects require demonstrated evidence and a newly bounded repair scope.
- The post-merge dashboard smoke check is read-only and does not authorize route mutation or Worker dispatch.
- Cross-department adoption, new Workers, recurring tasks, connectors, spending, public actions, and shared governance changes require their proper owners and separate authority.
- `ADV-20260718-042` remains open under its source owner and is not represented here as a Package E loop.

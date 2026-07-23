# Engineering_HQ Open Loops

Updated: 2026-07-23

## Open

| Status | Priority | Item | Next Action | Notes |
|---|---|---|---|---|
| Active | High | Canonical room-title implementation rollover | In the fresh Engineering_HQ chat, boot and sync first, then update Engineering-owned code, runtime configuration, tests, prompt launchers, route mappings, and active title-bearing local state to the canonical underscore room titles from `memory/HQ_NAMING_STANDARD.md` | Maintenance_HQ completed the repository-wide textual naming repair and the final report was ingested from Drive. No Engineering code or database repair has begun. Preserve stable keys and IDs, historical execution rows, immutable reports and receipts, checksums, and stable filesystem paths. Migrate only live routing and current configuration state through exact old-to-new mappings |
| Active | High | Courier post-navigation identity verifier defect | Repair the zero-authority courier so the sidebar resolves and verifies the exact Worker URL before navigation, while post-navigation identity uses the verified exact URL plus loaded room, history, composer, and generation witnesses even when the sidebar collapses behind `Show more` | Browser bridge is healthy on the restarted Edge CDP session. The self-test reached and fully loaded `Engineering_Worker`, then failed before composer fill or Send because the refreshed sidebar hid the exact link required by the redundant post-navigation verifier. Nothing was sent and no execution row was created. Do not weaken fail-closed submission evidence |
| Waiting | Normal | ADV-20260723-052 Chief_of_Staff_HQ watcher destination test | Wait for Rob to confirm whether the hourly watcher reports the advisory in the existing `Chief_of_Staff_HQ` conversation without spawning a new chat or triggering work | Advisory remains OPEN on the Engineering source board. No Worker dispatch, HQ wake, dashboard execution, connector write, follow-on work, or automatic closure is authorized |
| Active | High | Department ownership architecture and dashboard inspection | Observe corrected role-routed boots and inspect demonstrated identity, ownership, or source-board defects before closing the remaining system wrapper | ADV-20260719-044 is closed. Department Inspection remains locally validated at 414 normalized records, zero findings, and zero warnings. Remaining work is ordinary post-repair observation under `NOTE-20260717-014-department-ownership-and-dashboard-inspection.md` |
| Active | Normal | Browser and Worker transport maintenance | Observe ordinary post-Package E runs and repair only demonstrated transport defects without weakening exact URL, hydration, composer, submission, one-tab, one-shot claim, or stop-on-uncertainty safeguards | Package E is closed. Immutable Git evidence is checked before HQ wakes; uncertain HQ transport remains claimed and nonretryable until human inspection. Do not create speculative retries or transport experiments |
| Open | Normal | Dashboard auto-refresh | Add a configurable in-page auto-refresh control only if ordinary use still demonstrates value | Reuse the existing refresh path, prevent overlaps, show last and next refresh state, and preserve guarded Git sync |
| Open | Normal | Four-source dashboard observation | Confirm ordinary refresh, independent source health, cached degraded operation, and accepted scan paths remain useful in real use | Do not intentionally destroy valid credentials merely to demonstrate failure mode |
| Open | Normal | Penny Inventory Worker pilot | Begin with 2–3 real sale items and verify one-row-per-item writes, stable image references, uncertainty labels, and final Sheet read-back | Grandfathered compatibility package remains at `workers/penny-inventory/`; evaluate it under the canonical Worker contract without treating its path as the model for new Workers |
| Open | Normal | Penny Raw Capture Worker pilot | Observe real append, canonical-target, timestamp, and verification behavior | Grandfathered compatibility package remains at `workers/penny-raw-capture/`; operational reliability still needs live use |
| Open | Normal | Reliable Connector Execution Layer | Turn the design note into an implementation packet outline only when Rob authorizes the next build package | Align any future design with immutable evidence, HQ verification, signed consumption, bounded retries, and one authoritative operational ledger. Do not reopen Package E implicitly |
| Open | Normal | Connector health and retry policy | Define read and write health states, bounded retry rules, stop and backoff triggers, and degraded-mode fallback when a concrete implementation package is authorized | Use dashboard caches, guarded Git sync, browser safety gates, Worker duplicate suppression, one-shot HQ wake claims, and verified connector read-back as evidence patterns |
| Open | Normal | Worker reliability evidence | Compare synthetic and real pilot results against `coordination/WORKER_EXECUTION_CONTRACT.md` before proposing additional Workers | Package E proved the Engineering pilot. Cross-department rollout remains deferred and must not be inferred from pilot success |
| Open | Normal | Office Leaks delivery architecture | Continue one-problem local-service-office cleanup playbooks as Business requirements mature | Preserve mechanical workflow and human-system layers |
| Open | Normal | Cost-bearing technical choices | Route hosting, subscriptions, paid APIs, tools, backend workers, queues, or paperwork overlap to `Finance_HQ` | Finance owns money and paperwork |
| Open | Normal | Software repository strategy | Keep LifeOS as the runtime mirror and use separate repositories for educational and future standalone projects | Revisit dashboard extraction only if implementation expands materially |
| Paused | Low | Optional Python canonical source resolver | Do not implement unless operational evidence demonstrates a concrete reliability, security, or scale gap outside existing deterministic parsing | Python may provide defense in depth but is not the Worker and must not become the owner or interpreter of department judgment |
| Paused | Low | Canonical prompt transport verification | Do not resume the general composer investigation without demonstrated failure | Preserve validated marker, hydration, exact-destination, strict new-turn witness, and one-tab paths. Full-text equality and broad focus or timeout experiments remain out of scope |
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
- The naming rollover is a bounded Engineering implementation repair, not authority to rewrite historical evidence or other departments' files.
- Future defects require demonstrated evidence and a newly bounded repair scope.
- Cross-department adoption, new Workers, recurring tasks, connectors, spending, public actions, and shared governance changes require their proper owners and separate authority.
- `ADV-20260718-042` remains open under its source owner and is not represented here as a Package E loop.

# Engineering_HQ Open Loops

Updated: 2026-07-28

## Open

| Status | Priority | Item | Next Action | Notes |
|---|---|---|---|---|
| Active | High | LifeOS Version Two overall architecture | Review and refine the working `Version Two Safeguards` and `LifeOS Version Two System Design` documents with Rob until the process is simple, coherent, and complete | Simplification is the primary objective. No implementation is authorized yet |
| Open | High | Browser Plugin Design | Produce the component design after the overall process is settled | The plugin is a narrow courier: registered routes, composer protection, prompt delivery, basic telemetry, three command-local attempts, no response-body extraction, and no policy ownership |
| Open | High | LifeOS V2 Server Design | Produce the component design after the overall process is settled | The server mediates among GitHub, browser plugin, and dashboard; watches advisories and outcomes; tracks simple delivery state; does not recreate V1 evidence bureaucracy |
| Open | High | LifeOS V2 Dashboard Design | Produce the component design after the overall process is settled | The dashboard must clearly answer what is happening, what is blocked, and who acts next, with simple human recovery controls |
| Waiting | High | Promote approved V2 design set to GitHub | Wait until Rob approves the overall and component design documents | Promote only settled architecture and implementation contracts, not exploratory discussion |
| Waiting | High | Codex Penny comprehensive implementation prompt | Prepare one repository-scale deliverables prompt after the approved designs are canonical | Target implementation location: `apps/lifeos_dashboardv2`; thinking first, implementation second |
| Waiting | Normal | Archive and retire V1 dashboard architecture | Define the exact archive treatment during the approved migration design | Preserve current code and Git history. Do not delete or rewrite historical evidence. Do not carry legacy complexity forward merely for compatibility |
| Paused | Normal | V1 Worker runtime and ADV-053/ADV-054 repair path | Take no further Engineering action unless Rob explicitly reopens V1 cleanup | The incident demonstrated both useful safeguards and excessive brittleness. The latest apparent failure was stale Maintenance chat context, not another runtime defect |
| Paused | Normal | Office Leaks delivery architecture and Worker rollout | Keep paused while Rob pauses the Office Leaks business | Any future resume belongs to `Office_Leaks_HQ` and requires an explicit decision |
| Open | Normal | Cost-bearing technical choices | Route hosting, paid APIs, subscriptions, extension distribution, or other spending decisions to `Finance_HQ` when concrete choices arise | Finance owns money and paperwork |

## Waiting / Deferred

| Status | Item | Owner / Trigger | Notes |
|---|---|---|---|
| Deferred | High-risk workflow controls | A concrete destructive, financial, external, or security-sensitive workflow demonstrates need | Stronger approval, evidence, review, and strict idempotency should be opt-in by workflow rather than shape the normal path |
| Deferred | Additional department Workers | A demonstrated recurring bottleneck and explicit owner request | V2 design should not assume every department requires a Worker or separate execution room |
| Deferred | Multi-provider browser support | The ChatGPT browser plugin works reliably and a second real provider creates a concrete need | Do not build decorative provider-neutral abstractions before a second provider exists |
| Deferred | Productization architecture | Personal LifeOS V2 proves reliability and value | Do not burden the first implementation with multi-user tenancy, billing, cloud orchestration, or generalized workflow-builder requirements |
| Deferred | General connector dashboard adapters | Repeated real use demonstrates a concrete need | Keep V2 scope focused on the advisory handoff loop first |

## Recently Closed / Superseded

| Date | Item | Notes |
|---|---|---|
| 2026-07-28 | LifeOS V2 planning foundation | Created the Drive working documents `Version Two Safeguards` and `LifeOS Version Two System Design` under `Life Organization/Chief Engineering Penny` |
| 2026-07-28 | Incremental V1 rescue strategy | Superseded by Rob's decision to simplify the entire advisory execution system and build V2 under `apps/lifeos_dashboardv2` |
| 2026-07-28 | Universal send-budget direction | Rejected for V2. Use a maximum of three attempts local to one delivery command, with no blind retry after uncertainty |
| 2026-07-28 | Mandatory routine HQ review and immutable review-attempt chains | Rejected for the normal V2 path. Ordinary Git history and department advisory updates are sufficient for routine internal work |

## Boundary

- V2 design is active; implementation is not yet authorized.
- The current V1 system remains historical and operational evidence until explicitly archived. Do not continue patching it by inertia.
- One advisory and one owner are the default.
- Multi-department dependencies return to Rob through Chief of Staff.
- The browser plugin transports; it does not judge.
- The server coordinates; it does not create authority.
- The dashboard explains; it does not become a competing source of truth.
- GitHub remains durable truth and ordinary audit history.
- Rob decides.

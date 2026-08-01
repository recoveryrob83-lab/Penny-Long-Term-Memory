# Engineering_HQ Open Loops

Updated: 2026-08-01

## Active / Open

| Status | Priority | Item | Next Action | Completion / Review Condition |
|---|---|---|---|---|
| Active | High | Publish advisory-level quarantine repair | Locate the proven local changes, inspect the exact diff, commit only the bounded V2 source/runtime/API/dashboard/test files, rebase onto current `origin/main`, push, and read back the implementation | GitHub `main` contains quarantine behavior; the restarted runtime reports `REMOTE_GITHUB`, `CURRENT`, a non-null verified SHA, `ADV-20260728-054` valid, `ADV-20260726-053` quarantined, and all existing commands unchanged |
| Open | Normal | Command history ordering and bounded retention | Make the command display newest first; keep active and uncertain records prominent; move older terminal records into bounded history without deleting required evidence | Dashboard ordering is newest-first, dispatch selection remains state- and route-driven, and terminal history cannot grow without bound in the primary view |
| Open | Normal | Courier-owned tab lifecycle | Test one owned-tab reuse versus post-delivery closure under Rob's PC memory limit; preserve exact-route and empty-composer gates | Automation avoids tab sprawl, does not interfere with Rob's active chat, and reliably creates or reuses one safe courier tab when needed |
| Open | Normal | Readiness telemetry deduplication | Deduplicate or rate-limit repeated identical `NOT_READY` events while preserving meaningful state transitions and diagnostics | Event history records actionable transitions without a high-frequency waterfall of identical probe results |
| Open | Normal | Nighttime automation operating profile | Define the smallest reliable nighttime pattern only after the durable remote-source patch is verified | Scheduled sync or cleanup can run with one bounded courier tab, clear failure reporting, and no requirement for Rob to keep multiple ChatGPT windows open during the day |
| Open | Normal | V2 return path and outcome notification | Inspect the implemented outcome-detection and Chief of Staff notification path, then identify the smallest missing proof or repair | A department outcome can return to the correct existing Chief of Staff route with bounded authority and truthful delivery evidence, or the exact remaining gap is documented |
| Open | Normal | Cost-bearing technical choices | Route any hosting, paid API, extension distribution, or subscription decision to `Finance_HQ` when a concrete choice arises | No spending or subscription is introduced without owner-correct financial review and Rob's decision |

## Waiting / Deferred

| Status | Item | Owner / Trigger | Notes |
|---|---|---|---|
| Waiting | Resolve missing V2 Courier Envelope on `ADV-20260726-053` | `Maintenance_HQ` or source owner | Engineering quarantines the record but does not rewrite another department's advisory merely to satisfy the parser |
| Deferred | Additional department automation schedules | A demonstrated recurring need and explicit Rob authorization | Do not create a schedule merely because the transport now works |
| Deferred | High-risk workflow controls | A concrete destructive, financial, external, or security-sensitive workflow demonstrates need | Stronger approvals and evidence remain opt-in by workflow rather than universal V2 burden |
| Deferred | Multi-provider browser support | ChatGPT transport is stable and a second provider creates a real need | Do not build decorative provider-neutral abstractions before a second provider exists |
| Deferred | Productization architecture | Personal LifeOS V2 proves reliability and value | Avoid multi-user tenancy, billing, cloud orchestration, and generalized workflow-builder scope |
| Paused | V1 Worker runtime and ADV-053/ADV-054 repair path | Explicit Rob decision | Preserve V1 as legacy evidence. Do not resume the old orchestration architecture by inertia |
| Paused | Office Leaks delivery architecture and Worker rollout | Rob resumes Office Leaks through its owning departments | Engineering does not manufacture business urgency or activation |

## Operating Watches

These are technical conditions to observe, not separate implementation projects:

- `UNCERTAIN` remains a hard stop and is never a blind-retry state.
- Production source reads remain commit-pinned, read-only, and fail-closed on snapshot-integrity failures.
- Advisory-level quarantine creates no command, updates no command, stales no command, and cannot block valid advisories.
- Route health, exact URL, empty composer, content script, send control, global pause, emergency stop, and test-arm protections remain intact.
- One command is selected per poll; visual sorting must never define dispatch order.
- Credentials are never persisted in runtime state, logs, dashboard output, extension storage, or source files.
- Local success is not durable success until the exact implementation is committed, pushed, and read back.
- Engineering must not edit another department's canonical files without explicit coordinated authority.

## Recently Closed / Proven

| Date | Item | Evidence |
|---|---|---|
| 2026-08-01 | V2 production route dispatch | Production routes no longer require the test arm; test routes retain the arm gate |
| 2026-08-01 | Canonical multi-route extension flow | Engineering and Maintenance routes coexist; the extension consumes server order and one command per poll |
| 2026-08-01 | Discovery/readiness deadlock | Candidate discovery occurs before readiness; atomic `/begin` remains readiness-gated |
| 2026-08-01 | Composer/send-proof hardening | Narrow controls, self-contained fallback, bounded proof polling, pre-click `FAILED`, and post-click `UNCERTAIN` |
| 2026-08-01 | Maintenance production delivery | `ADV-20260801-055-r2` reached `DELIVERED`, Maintenance confirmed receipt, and Rob authorized closure; revision 1 remains terminal `UNCERTAIN` |
| 2026-08-01 | Core canonical GitHub synchronizer | Commit `0eeccc46df6980c62e29795e7f40c78a1d61a108` reads commit-pinned remote snapshots without mutating the local working tree |
| 2026-08-01 | Advisory-quarantine behavior proven locally | Valid and malformed advisories coexist in a `CURRENT` local runtime snapshot; publication to `origin/main` remains open |
| 2026-07-28 | V2 design and implementation authorization sequence | Superseded by the implemented operational core under `apps/lifeos_dashboardv2` |
| 2026-07-28 | Incremental V1 rescue strategy | Superseded by the simpler V2 architecture |

## Boundary

- One advisory and one owner remain the default.
- The browser extension transports; it does not judge.
- The server coordinates and records; it does not create authority.
- The dashboard explains; it does not become source truth.
- GitHub remains durable truth and normal audit history.
- Another department's malformed source record remains that department's ownership problem, not silent Engineering write authority.
- Rob decides.
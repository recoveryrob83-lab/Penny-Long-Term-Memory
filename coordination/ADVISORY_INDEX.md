# LifeOS Advisory Index

Updated: 2026-07-23
Purpose: Sole active routing dashboard for formal LifeOS advisories.

## Open Advisories

| Advisory ID | Lifecycle | Priority | Revision | Verification Mode | Source | Target | Source Board | Summary |
|---|---|---|---:|---|---|---|---|---|
| ADV-20260723-052 | OPEN | NORMAL | 1 | N/A | Engineering_HQ | Chief_of_Staff_HQ | `coordination/boards/engineering.md` | Read-only watcher destination test pending Rob confirmation that the hourly watcher reports in the existing `Chief_of_Staff_HQ` conversation without creating a new chat or triggering work |

## Recently Closed Advisories

The entries below preserve the names and wording used when they were created or closed. They are historical routing evidence and do not define current canonical room names.

| Advisory ID | Lifecycle | Priority | Revision | Verification Mode | Source | Target | Source Board | Closed | Summary |
|---|---|---|---:|---|---|---|---|---|---|
| ADV-20260718-042 | CLOSED | HIGH | 1 | IMMEDIATE_HQ | Chief_of_Staff_HQ / LifeOS_HQ | Engineering_HQ | `coordination/boards/main-assistant.md` | 2026-07-23 | Receiver-side semantic validation was built, tested, source-verified, and approved by Rob for slow rollout |
| ADV-20260723-051 | CLOSED | HIGH | 1 | IMMEDIATE_HQ | Engineering HQ | Engineering HQ | `coordination/boards/engineering.md` | 2026-07-23 | Verify owning-HQ wake, receipt ingestion, and duplicate suppression |
| ADV-20260722-049 | CLOSED | HIGH | 1 | IMMEDIATE_HQ | Engineering HQ | Engineering HQ / Rob | `coordination/boards/engineering.md` | 2026-07-23 | Prove the explicit Rob-validation path |
| ADV-20260721-048 | CLOSED | HIGH | 1 | IMMEDIATE_HQ | Engineering HQ | Engineering Worker / Engineering HQ | `coordination/boards/engineering.md` | 2026-07-23 | Prove the immutable Worker result outbox |
| ADV-20260720-047 | CLOSED | NORMAL | 2 | IMMEDIATE_HQ | Engineering HQ | Engineering Worker | `coordination/boards/engineering.md` | 2026-07-23 | Response reconciliation architecture discovery |
| ADV-20260719-045 | CLOSED | HIGH | 1 | IMMEDIATE_HQ | Main Assistant / LifeOS Hub | Life OS Maintenance HQ | `coordination/boards/main-assistant.md` | 2026-07-19 | Acknowledge the project and chat source memory architecture discovery |
| ADV-20260719-044 | CLOSED | HIGH | 1 | IMMEDIATE_HQ | Main Assistant / LifeOS Hub | Life OS Maintenance HQ | `coordination/boards/main-assistant.md` | 2026-07-19 | Reconcile Worker filesystem and continuity state with the canonical execution contract |
| ADV-20260719-043 | CLOSED | HIGH | 1 | IMMEDIATE_HQ | Engineering HQ | Main Assistant / LifeOS Hub and Life OS Maintenance HQ | `coordination/boards/engineering.md` | 2026-07-19 | Adopt the canonical shared execution and Worker architecture |
| ADV-20260717-040 | CLOSED | HIGH | 1 | IMMEDIATE_HQ | Main Assistant | Life OS Maintenance HQ | `coordination/boards/main-assistant.md` | 2026-07-18 | Create canonical LifeOS Project Instructions and eight-room authority model |
| ADV-20260717-039 | CLOSED | HIGH | 1 | IMMEDIATE_HQ | Business HQ | Chief of Staff HQ / LifeOS HQ | `coordination/boards/business.md` | 2026-07-18 | Confirm Business HQ Phase Two repair and Office Leaks ownership boundary |
| ADV-20260716-037 | CLOSED | NORMAL | 1 | ROUTINE_BATCH | Office Leaks HQ | Main Assistant, Business, Finance, Engineering, Wellness, Life Logistics | `coordination/boards/office-leaks.md` | 2026-07-17 | Broadcast Office Leaks Facebook launch and first lead-loss video |

## Index Rules

- `coordination/ADVISORY_INDEX.md` is the sole active advisory routing dashboard.
- Full current advisory text lives on the source department board under `coordination/boards/`.
- `LifeOS_HQ` formal advisories use `Chief_of_Staff_HQ` as the source department and `coordination/boards/main-assistant.md` as the retained source-board path.
- A material advisory change increments `advisory_revision`.
- Lifecycle and priority remain separate fields.
- `N/A` in Verification Mode means the advisory is a read-only observation or routing test rather than an execution-ready Worker task.
- Closed advisory rows may retain historical names, identifiers, and exact outcomes.
- Do not update `coordination/DEPARTMENT_EVENT_INBOX.md` for normal advisory routing unless Rob explicitly reactivates it.
- Do not use GitHub Issues or Todoist as advisory-state systems.
- Do not duplicate full advisory text into target boards or department open loops merely for visibility.
- Multi-target advisories remain open until all required targets are handled or separate per-target state is recorded.
- The same advisory remains authoritative through acknowledgement, implementation, hold, elevation, resume, verification, and closure.

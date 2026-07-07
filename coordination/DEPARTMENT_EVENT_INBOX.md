# Department Event Inbox

Updated: 2026-07-06
Purpose: Frozen historical Life OS register for past advisory synchronization/read/ingestion events.

## Status

Frozen / historical.

As of ADV-20260706-018, the Department Event Inbox is no longer an active advisory routing file.

Normal advisory routing now uses:

1. Source department advisory board under `coordination/boards/`.
2. `coordination/ADVISORY_INDEX.md` as the sole active routing dashboard.

Do not update this file for normal advisory routing unless Rob explicitly reactivates it.

## Reason For Freeze

Engineering observed that maintaining both Advisory Index and Department Event Inbox required duplicate writes and increased connector fragility.

Life Logistics accepted ADV-20260706-018 and simplified advisory routing to reduce write load, safety-trigger exposure, stale routing information, and scheduled-worker complexity.

## Historical Source Of Truth Notes

- Advisory dashboard: `coordination/ADVISORY_INDEX.md`
- Advisory details: `coordination/boards/`
- Decision Rules Registry: `coordination/DECISION_RULES_REGISTRY.md`
- Pending advisory standard: `coordination/PENDING_ADVISORY_BOARDS.md`
- Department notebook standard: `coordination/DEPARTMENT_NOTEBOOKS.md`
- Source/publication standard: `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md`

GitHub Issues are not a Life OS advisory surface unless Rob explicitly changes the architecture later.

## Final Active Event Before Freeze

| Event ID | Source | Target(s) | Final Status | Subject | Notes |
|---|---|---|---|---|---|
| ADV-20260706-018 | Chief Engineering Penny | Life Logistics HQ | Implemented | Simplify Life OS advisory routing system | Department Event Inbox frozen as active routing file; Advisory Index promoted to sole active routing dashboard. |

## Recent Historical Events

| Event ID | Source | Target(s) | Status | Subject | Notes |
|---|---|---|---|---|---|
| ADV-20260706-017 | Chief Engineering Penny | Life Logistics HQ / Life OS Infrastructure | Closed | Connector reliability operating pattern from Gemini/Drive tests | Life Logistics created `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md`. |
| ADV-20260706-016 | Main Assistant | Chief Engineering Penny / Life Logistics HQ | Closed | External Drive-worker workflow observation | Engineering and Logistics consumed the advisory; Gemini Drive-worker pattern is an Engineering evaluation item and Logistics operating-standard consideration. |
| ADV-20260705-015 | Chief Engineering Penny | Life Logistics HQ / Life OS Infrastructure | Closed | Globalize department notebook leaf routing/index standard | Life Logistics updated `coordination/DEPARTMENT_NOTEBOOKS.md`; no empty indexes created by default. |
| ADV-20260705-014 | Life Logistics HQ / Life OS Infrastructure | Chief Engineering Penny | Closed | Standardize notebook leaf routing and index files | Engineering created local notebook index and routed global standardization back to Logistics. |
| ADV-20260704-013 | Chief Engineering Penny | Life Logistics HQ | Closed | Tighten advisory posting board rules | Life Logistics clarified source-board versus target-department routing. |
| ADV-20260704-012 | Life Logistics HQ | Chief Engineering Penny | Closed | Connector safety-trigger avoidance rules needed | Engineering consumed advisory; connector safety-trigger avoidance will be folded into Reliable Connector Execution Layer rules. |
| ADV-20260704-011 | Main Assistant | Life Logistics HQ | Closed | Department consolidation and archival request | Life Logistics updated active project map; several departments consolidated or marked dormant. |
| ADV-20260704-010 | Life Logistics HQ / Life OS Infrastructure | All Departments | Closed | Decision Rules Registry and Role Drift Check architecture adopted | All boards reported read and ingested. |
| ADV-20260704-009 | Chief Engineering Penny | Life Logistics HQ | Closed | Role Drift Check for Penny HQs | Life Logistics added Role Drift Check to Operating Rules and handoff. |
| ADV-20260704-008 | Chief of Finance Penny | Life Logistics HQ | Closed | Discretionary Purchase Pause Rule routing reinforcement | Life Logistics updated handoff to route discretionary spending decisions to Finance HQ. |
| ADV-20260704-007 | Life Logistics HQ | Chief of Finance Penny | Ingested | Finance advisory routing surface refresh | Finance re-synced advisory routing files. |
| ADV-20260704-006 | Chief Engineering Penny | Life Logistics HQ | Closed | Source-of-truth and publication architecture | Life Logistics adopted Source-of-Truth and Publication Standard. |
| ADV-20260704-003 | Chief Engineering Penny | Chief Engineering Penny | Closed | Engineering sync completed and connector reliability next work | Engineering re-consumed self-addressed advisory. |
| ADV-20260704-005 | Chief Engineering Penny | Life Logistics HQ | Closed | Department Notebooks for long-term idea capture | Life Logistics adopted optional Department Notebooks as a standard pattern. |
| ADV-20260704-004 | Chief Engineering Penny | Life Logistics HQ | Closed | Department Pending Advisory Boards | Life Logistics adopted Pending Advisory Boards as a standard pattern. |
| ADV-20260704-002 | Chief Business HQ | Chief Engineering Penny | Ingested | Drive connector reliability is a major Penny product risk | Engineering created Reliable Connector Execution Layer as first concrete research track. |
| ADV-20260704-001 | Chief Business HQ | Life Logistics HQ | Closed | Business HQ research, Drive architecture, and reboot-state update needed | Life Logistics ingested; Business Drive architecture resolved. |

## Notes

Historical advisory state is preserved in repository history and department boards.

Use `coordination/ADVISORY_INDEX.md` for current advisory routing.
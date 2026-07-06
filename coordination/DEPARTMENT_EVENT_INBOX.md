# Department Event Inbox

Updated: 2026-07-05
Purpose: Lightweight Life OS register for advisory and synchronization events between Penny departments.

## Operating Rule

This file tracks abstract department-to-department sync events.

It is not a user task list.

Todoist owns Rob-facing action items. This file owns system synchronization state.

Keep entries short and non-sensitive.

## Source of Truth

- Advisory dashboard: `coordination/ADVISORY_INDEX.md`
- Advisory details: `coordination/boards/`
- Decision Rules Registry: `coordination/DECISION_RULES_REGISTRY.md`
- Finance advisory board: `coordination/boards/finance.md`
- Pending advisory standard: `coordination/PENDING_ADVISORY_BOARDS.md`
- Department notebook standard: `coordination/DEPARTMENT_NOTEBOOKS.md`
- Source/publication standard: `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md`

GitHub Issues are not a Life OS advisory surface unless Rob explicitly changes the architecture later.

## Current Open / Pending Events

| Event ID | Source | Target(s) | Status | Subject | Notes |
|---|---|---|---|---|---|
| ADV-20260705-014 | Life Logistics HQ / Life OS Infrastructure | Chief Engineering Penny | Open | Standardize notebook leaf routing and index files | Engineering should consume advisory from `coordination/boards/life-os.md` and decide whether to create a notebook leaf README/index. |

## Recent Closed / Ingested Events

| Event ID | Source | Target(s) | Status | Subject | Notes |
|---|---|---|---|---|---|
| ADV-20260704-013 | Chief Engineering Penny | Life Logistics HQ | Closed | Tighten advisory posting board rules | Life Logistics clarified source-board versus target-department routing in Coordination README and advisory template. |
| ADV-20260704-012 | Life Logistics HQ | Chief Engineering Penny | Closed | Connector safety-trigger avoidance rules needed | Engineering consumed advisory; connector safety-trigger avoidance will be folded into Reliable Connector Execution Layer rules. |
| ADV-20260704-011 | Main Assistant | Life Logistics HQ | Closed | Department consolidation and archival request | Life Logistics updated active project map; several departments consolidated or marked dormant. Some secondary handoff/open-loop rewrites were blocked by connector safety checks. |
| ADV-20260704-010 | Life Logistics HQ / Life OS Infrastructure | All Departments | Closed | Decision Rules Registry and Role Drift Check architecture adopted | All boards reported read and ingested. Departments should use Decision Rules Registry and Role Drift Check going forward. |
| ADV-20260704-009 | Chief Engineering Penny | Life Logistics HQ | Closed | Role Drift Check for Penny HQs | Life Logistics added Role Drift Check to Operating Rules and handoff as a gentle department-boundary safeguard. |
| ADV-20260704-008 | Chief of Finance Penny | Life Logistics HQ | Closed | Discretionary Purchase Pause Rule routing reinforcement | Life Logistics updated handoff to route discretionary spending decisions to Finance HQ while keeping live financial context out of GitHub. |
| ADV-20260704-007 | Life Logistics HQ | Chief of Finance Penny | Ingested | Finance advisory routing surface refresh | Finance re-synced advisory routing files. |
| ADV-20260704-006 | Chief Engineering Penny | Life Logistics HQ | Closed | Source-of-truth and publication architecture | Life Logistics adopted Source-of-Truth and Publication Standard. |
| ADV-20260704-003 | Chief Engineering Penny | Chief Engineering Penny | Closed | Engineering sync completed and connector reliability next work | Engineering re-consumed self-addressed advisory. |
| ADV-20260704-005 | Chief Engineering Penny | Life Logistics HQ | Closed | Department Notebooks for long-term idea capture | Life Logistics adopted optional Department Notebooks as a standard pattern. |
| ADV-20260704-004 | Chief Engineering Penny | Life Logistics HQ | Closed | Department Pending Advisory Boards | Life Logistics adopted Pending Advisory Boards as a standard pattern. |
| ADV-20260704-002 | Chief Business HQ | Chief Engineering Penny | Ingested | Drive connector reliability is a major Penny product risk | Engineering created Reliable Connector Execution Layer as first concrete research track. |
| ADV-20260704-001 | Chief Business HQ | Life Logistics HQ | Closed | Business HQ research, Drive architecture, and reboot-state update needed | Life Logistics ingested; Business Drive architecture resolved. |

## Department Read Tracking

| Event ID | Department | Read Status | Ingest Status | Notes |
|---|---|---|---|---|
| ADV-20260705-014 | Chief Engineering Penny | Unread | Pending | Read source advisory on Life OS board; decide notebook leaf index/routing action. |
| ADV-20260704-013 | Life Logistics HQ | Read | Ingested | Source-board versus target-department wording clarified. |
| ADV-20260704-012 | Chief Engineering Penny | Read | Ingested | Engineering will fold connector safety-trigger avoidance into Reliable Connector Execution Layer rules. |
| ADV-20260704-011 | Life Logistics HQ | Read | Ingested | Active project map updated; advisory closed. |
| ADV-20260704-010 | All Departments | Read | Ingested | All boards reported Decision Rules Registry and Role Drift Check architecture ingested. |
| ADV-20260704-009 | Life Logistics HQ | Read | Ingested | Role Drift Check added to Operating Rules and Life Logistics handoff. |
| ADV-20260704-008 | Life Logistics HQ | Read | Ingested | Discretionary Purchase Pause Rule routing reinforced. |
| ADV-20260704-007 | Chief of Finance Penny | Read | Ingested | Finance re-synced advisory routing rule and Finance board location. |
| ADV-20260704-006 | Life Logistics HQ | Read | Ingested | Source-of-Truth and Publication Standard adopted. |
| ADV-20260704-003 | Chief Engineering Penny | Read | Ingested | Engineering re-consumed and closed self-addressed continuation advisory. |
| ADV-20260704-005 | Life Logistics HQ | Read | Ingested | Department Notebook standard adopted. |
| ADV-20260704-004 | Life Logistics HQ | Read | Ingested | Pending Advisory Board standard adopted. |
| ADV-20260704-002 | Chief Engineering Penny | Read | Ingested | Reliable Connector Execution Layer research track created. |
| ADV-20260704-001 | Life Logistics HQ | Read | Ingested | Business Drive architecture resolved. |

## Notes

Historical advisory state is preserved in repository history and department boards.

Use this inbox for active synchronization/read/ingestion state, not as a permanent transcript.
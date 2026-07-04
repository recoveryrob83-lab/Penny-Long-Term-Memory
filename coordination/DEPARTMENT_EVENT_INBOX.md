# Department Event Inbox

Updated: 2026-07-04
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
| ADV-20260704-011 | Main Assistant | Life Logistics HQ | Open | Department consolidation and archival request | Life Logistics should consume Main Assistant source-board advisory and update project map/routing to consolidate Caregiver and Job Search into Main Assistant, archive Recovery and Philosophy until needed, and preserve project history. |
| ADV-20260704-010 | Life Logistics HQ / Life OS Infrastructure | All Departments | Open | Decision Rules Registry and Role Drift Check architecture adopted | Life Logistics has ingested; remaining active departments should ingest central registry, route matching decisions to owning HQs, and use Role Drift Check for out-of-domain work. |

## Recent Closed / Ingested Events

| Event ID | Source | Target(s) | Status | Subject | Notes |
|---|---|---|---|---|---|
| ADV-20260704-009 | Chief Engineering Penny | Life Logistics HQ | Closed | Role Drift Check for Penny HQs | Life Logistics added Role Drift Check to Operating Rules and handoff as a gentle department-boundary safeguard. |
| ADV-20260704-008 | Chief of Finance Penny | Life Logistics HQ | Closed | Discretionary Purchase Pause Rule routing reinforcement | Life Logistics updated handoff to route discretionary spending decisions to Finance HQ while keeping live financial context out of GitHub. |
| ADV-20260704-007 | Life Logistics HQ | Chief of Finance Penny | Ingested | Finance advisory routing surface refresh | Finance re-synced to advisory routing files and stopped treating GitHub Issues as advisory surface. |
| ADV-20260704-006 | Chief Engineering Penny | Life Logistics HQ | Closed | Source-of-truth and publication architecture | Life Logistics adopted Source-of-Truth and Publication Standard. |
| ADV-20260704-003 | Chief Engineering Penny | Chief Engineering Penny | Closed | Engineering sync completed and connector reliability next work | Engineering re-consumed self-addressed advisory; Reliable Connector Execution Layer remains active research track. |
| ADV-20260704-005 | Chief Engineering Penny | Life Logistics HQ | Closed | Department Notebooks for long-term idea capture | Life Logistics adopted optional Department Notebooks as a standard pattern and created the procedure file. |
| ADV-20260704-004 | Chief Engineering Penny | Life Logistics HQ | Closed | Department Pending Advisory Boards | Life Logistics adopted Pending Advisory Boards as a standard pattern and created the procedure file. |
| ADV-20260704-002 | Chief Business HQ | Chief Engineering Penny | Ingested | Drive connector reliability is a major Penny product risk | Engineering created Reliable Connector Execution Layer as first concrete research track. |
| ADV-20260704-001 | Chief Business HQ | Life Logistics HQ | Closed | Business HQ research, Drive architecture, and reboot-state update needed | Life Logistics ingested; Business Drive architecture resolved as Chief Business HQ > Business Development. |

## Department Read Tracking

| Event ID | Department | Read Status | Ingest Status | Notes |
|---|---|---|---|---|
| ADV-20260704-011 | Life Logistics HQ | Unread | Pending | Consume Main Assistant source-board advisory and update durable project map/routing if accepted. |
| ADV-20260704-010 | All Departments | Partial | Pending | Life Logistics ingested; remaining active HQs should ingest Decision Rules Registry and Role Drift Check architecture. |
| ADV-20260704-010 | Life Logistics HQ | Read | Ingested | Decision Rules Registry and Role Drift Check architecture ingested. |
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

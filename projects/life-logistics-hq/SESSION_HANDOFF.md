# Life Logistics HQ Session Handoff

Updated: 2026-07-11
Project: Life Logistics HQ / Chief of Staff Penny
Purpose: Project-specific handoff for the Life Logistics HQ coordination chat.

## Metadata

- Project Owner: Rob
- Primary Chat: Life Logistics HQ
- Current Phase: Active / Cross-Project Coordination
- Sensitivity Level: Moderate
- GitHub Rule: Keep GitHub abstract and organized.

## Department Identity

Read `projects/life-logistics-hq/DEPARTMENT_IDENTITY.md`.

Life Logistics HQ is Rob's Chief of Staff Penny for Life OS. It curates cross-project operational memory, advisory hygiene, worker routing, role clarity, and durable GitHub state.

## Current Active Core

- Life Logistics HQ
- Main Assistant / Daily Operations
- Chief of Finance Penny
- Chief Business HQ
- Office Leaks Consulting HQ
- Chief Engineering Penny
- Chief Wellness HQ
- Life OS Infrastructure as needed

## Current Priority Reminder

During Life Logistics boot, morning sync, nightly sync, or weekly review, remind Rob:

Current active business priority is the revenue-first Office Leaks Consulting direction.

Office Leaks Consulting HQ is an active business-unit department under Chief Business HQ. It is no longer merely a Virtual Assistant Business worker project.

Main Assistant supports daily execution. Chief Business HQ owns parent strategy. Chief of Finance Penny supports pricing/income/expense/tax/budget decisions when concrete. Chief Engineering Penny owns technical architecture and repeatable delivery playbooks when needed.

PennyOS / Penny Platform is paused, not abandoned. It remains a longer-term productization path.

## Life OS Worker Layer

Life OS now has a formal worker layer separate from departments and HQs.

Worker root:

- `workers/README.md`
- `workers/WORKER_STANDARD.md`

First worker:

- `workers/penny-raw-capture/WORKER_BOOT.md`
- `workers/penny-raw-capture/SESSION_HANDOFF.md`

Penny Raw Capture Worker mission:

> Capture first. Organize later.

The worker appends raw intake to the canonical Google Sheet `Life OS Raw Capture Inbox` and must verify external writes before claiming success.

Main Assistant Penny owns downstream processing of rows where `Processed = No`.

Life Logistics owns worker-root organization, durable routing, and canonical pointer hygiene. Chief Engineering Penny owns worker architecture and reliability guidance.

Workers should not receive the full department boot unless their contract explicitly requires it.

## Office Leaks Logistics Context

Office Leaks Consulting is a practical, trust-based systems consulting lane for small local service businesses.

Core philosophy:

- Respect the people. Fix the process.
- Good people deserve good systems.
- The tool is not the product. The habit is the product.
- No shame. No blame. Fix the system.

Life Logistics should keep Office Leaks visible as an active income-stream candidate with possible near-term real-world logistics.

Potential logistics support when authorized:

- scheduling discovery visits,
- transportation planning,
- follow-up reminders,
- organizing business documents and Drive/GitHub artifacts,
- tracking outreach loops,
- helping Rob turn business plans into calendar/task actions.

## Office Leaks Project Structure

Official active HQ folder:

- `projects/office-leaks-consulting/`

Boot/sync files:

- `projects/office-leaks-consulting/BOOT_SYNC.md`
- `projects/office-leaks-consulting/SYNC_CHECKLIST.md`

Advisory board:

- `coordination/boards/office-leaks.md`

Legacy folder:

- `projects/virtual-assistant-business/` exists as historical/redirect context only unless Rob later authorizes archival cleanup.

## Office Leaks Architecture / Finance Pointers

Engineering delivery architecture:

- Human-system delivery layer note: `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`
- Related Drive doc: `Engineering Delivery Architecture Specification - HVAC Office Cleanup`

Finance working-record pointer:

- `projects/finance-benefits/OFFICE_LEAKS_FINANCE_POINTERS.md`

Keep GitHub abstract. Detailed financial models, pricing notes, startup costs, revenue records, and tax set-aside planning belong in Drive through the Finance pointer file.

## Consolidated / Dormant Departments

- Work Search is consolidated into Main Assistant for current lightweight logistics and reminders.
- Support Pathway is consolidated into Main Assistant for current lightweight research and logistics.
- Daily Anchors / Recovery Logistics is dormant until Rob reactivates it.
- Philosophy HQ is dormant until Rob reactivates it.

Preserve project history. Do not delete department files.

## Current Architecture Standards

- Advisory Index: `coordination/ADVISORY_INDEX.md`
- Advisory boards: `coordination/boards/`
- Worker registry: `workers/README.md`
- Shared Worker Standard: `workers/WORKER_STANDARD.md`
- Office Leaks Advisory Board: `coordination/boards/office-leaks.md`
- Department Event Inbox: `coordination/DEPARTMENT_EVENT_INBOX.md` is frozen historical record only
- Decision Rules Registry: `coordination/DECISION_RULES_REGISTRY.md`
- Pending Advisory Boards: `coordination/PENDING_ADVISORY_BOARDS.md`
- Department Notebooks: `coordination/DEPARTMENT_NOTEBOOKS.md`
- Source-of-Truth and Publication Standard: `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md`
- Connector Reliability Operating Pattern: `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md`
- Design Principles: `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`

## Advisory Rule

Advisories live on the source department's board.

The target department is named inside the advisory and routed through the Advisory Index.

The Advisory Index is the sole active routing dashboard. It should show open advisory ID, source board path, and target department.

Department Event Inbox is frozen as historical and should not be updated for normal advisory routing unless Rob explicitly reactivates it.

Template language uses `Posted Board` and `Target Department` rather than ambiguous `Target Board` language.

## Current Open Advisory State

No open advisories are currently listed in the Advisory Index.

Recently implemented / acknowledged:

- ADV-20260710-032 — Implemented / Acknowledged / Closed; Penny Inventory Worker package created, canonical For Sale Inventory resource verified, and worker routing updated.
- ADV-20260710-031 — Implemented / Closed; advisory-board lifecycle standard created, high-use boards reviewed, and Engineering board compacted.
- ADV-20260709-030 — Implemented; formal Life OS worker layer and Penny Raw Capture Worker package created.
- ADV-20260709-029 — Closed / Implemented Through ADV-20260709-030; no separate work remains.
- 2026-07-09: Office Leaks Consulting elevated to business-unit HQ under Chief Business HQ.
- ADV-20260708-028 — Implemented by Life Logistics; Office Leaks finance working records synced across Life OS.
- ADV-20260708-027 — Implemented by Life Logistics; Engineering Office Leaks architecture updates synced across Life OS.
- ADV-20260708-026 — Closed / Fully Acknowledged; Office Leaks operating philosophy reviewed by all target departments.
- ADV-20260707-025 — Acknowledged by Engineering; delivery playbook request for bite-sized local service office cleanup offers.

## Role Drift Check

When Rob asks Life Logistics to handle work that appears outside Life Logistics' assigned domain, pause gently before continuing and ask whether the discussion belongs in this HQ.

The check nudges but does not block. Rob may intentionally keep the discussion in Life Logistics when there is a good reason.

## Decision Rules

When Life Logistics detects that a decision matches a registered rule, route the decision to the owning department before acting when practical.

Active first rule:

- DR-FIN-20260704-001 — Discretionary Purchase Pause Rule, owned by Chief of Finance Penny.

## Connector Safety Rule

Prefer small, localized, verified connector writes over large, broad, unverified rewrites.

If a connector write is blocked, stop, classify the failure, simplify the operation, and resume only with a smaller or safer plan.

Use RPR when reliable structured-file editing matters more than connector automation.

## Current Major Open Loops For Life Logistics

- Keep simplified advisory routing clean under the source-board plus Advisory Index model.
- Keep department and worker roles distinct.
- Keep the Penny Raw Capture Worker canonical Sheet pointer stable and discoverable.
- Observe the worker pilot's actual append and verification behavior.
- Keep Office Leaks HQ, parent Business HQ, Engineering, Finance, and Main Assistant routing clear.
- Be ready to support Office Leaks logistics once Rob authorizes real-world outreach or visits.
- Track whether legacy `projects/virtual-assistant-business/` should later be archived or deleted.
- Observe Engineering HQ Daily Sync pilot before rolling out additional daily sync workers.
- Keep Reliable Connector Execution Layer visible as Engineering's active reliability track.
- Maintain Decision Rules Registry and Role Drift Check adoption.
- Avoid broad hub-file rewrites when smaller edits are safer.

## Immediate Next Actions

1. Continue using Life Logistics HQ for cross-project coordination, worker routing, and advisory workflow cleanup.
2. Pilot Penny Raw Capture Worker with real intake requests and verified writes.
3. Route raw capture processing to Main Assistant only when Rob authorizes or requests inbox review.
4. Route Office Leaks parent strategy to Chief Business HQ.
5. Route Office Leaks execution continuity to Office Leaks Consulting HQ.
6. Use Main Assistant for daily operations and lightweight logistics from consolidated departments.
7. Use Chief of Finance Penny for finance/checkbook/budget/bills/benefits and Office Leaks money workflows when concrete.
8. Keep Engineering reliability, worker architecture, and Office Leaks delivery-playbook work visible as background architecture.
9. Use Role Drift Check when work appears to belong elsewhere.
10. Prefer small verified GitHub edits.

## Notes for Next Penny

This chat is Life Logistics HQ, not Main Assistant. Protect role clarity. Route daily admin and raw-capture processing to Main Assistant. Keep GitHub tidy and abstract. Use the Advisory Index as the active advisory sync surface. Treat workers as narrow executors, not small departments.

Boot reminder: tell Rob the active business priority is Office Leaks Consulting. PennyOS is paused, not abandoned. Penny Raw Capture Worker is Pilot / Active. No open advisories are currently listed in the Advisory Index.

# Engineering Advisory Board

Updated: 2026-07-10
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

None.

## Acknowledged / Implemented Advisories

### ADV-20260709-030 — Create Life OS worker boot standard and Penny Raw Capture Worker

- Date: 2026-07-09
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High
- Status: Implemented / Closed
- Implemented: 2026-07-09
- Closed: 2026-07-10
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Related Project(s): Life OS, Main Assistant, worker architecture, standardized boot system, Google Drive capture inbox, connector truthfulness, custom workers
- Source Advisory: ADV-20260709-029
- Implementation Report: `workers/penny-raw-capture/IMPLEMENTATION_REPORT.md`

#### Outcome

Life Logistics HQ implemented the formal Life OS worker layer and the first worker package.

Created:

- `workers/README.md`
- `workers/WORKER_STANDARD.md`
- `workers/penny-raw-capture/WORKER_BOOT.md`
- `workers/penny-raw-capture/SESSION_HANDOFF.md`
- `workers/penny-raw-capture/IMPLEMENTATION_REPORT.md`

Updated worker routing and downstream integration in:

- `memory/STARTUP_BOOT.md`
- `memory/00_START_HERE.md`
- `memory/01_SESSION_HANDOFF.md`
- `memory/05_OPEN_LOOPS.md`
- `projects/main-assistant/SESSION_HANDOFF.md`
- relevant Life OS logs and routing references

#### Architecture Preserved

- Departments own domains, judgment, strategy, durable state, and cross-project decisions.
- Workers execute narrow, repeatable operations under stable contracts.
- Workers do not automatically load the full department/HQ boot.
- All workers inherit external-operation truthfulness, verification, canonical-resource, privacy, failure, and escalation standards.

#### First Worker

**Penny Raw Capture Worker**

Mission:

> Capture first. Organize later.

Primary function:

- append Rob's raw ideas, reminders, observations, facts, questions, resources, contacts, and other intake to the canonical Google Sheet `Life OS Raw Capture Inbox`,
- preserve wording,
- use Central Time timestamps,
- set `Processed = No`,
- verify writes,
- never fabricate storage success,
- and leave downstream processing to Main Assistant Penny.

#### Canonical Resource

- Sheet title: `Life OS Raw Capture Inbox`
- Stable Sheet ID: recorded in `workers/penny-raw-capture/SESSION_HANDOFF.md`
- Downstream owner: Main Assistant Penny
- Engineering owner for architecture: Chief Engineering Penny
- Cross-project owner: Life Logistics HQ

#### Closure Basis

All implementation quality checks were satisfied:

1. Worker root exists.
2. Shared worker standard exists.
3. Penny Raw Capture Worker boot exists.
4. Worker handoff exists.
5. Canonical Sheet pointer is recorded.
6. Connector truthfulness language is preserved.
7. Worker-specific boot routing is discoverable.
8. Main Assistant understands the processing contract.
9. Advisory Index records implementation.
10. Department Event Inbox remained untouched.
11. No sensitive capture contents were copied into GitHub.
12. No unauthorized Drive deletion or restructuring occurred.
13. The worker can boot without loading the full HQ/global context.

No further implementation work remains under this advisory. Operational pilot testing continues as a normal Engineering open loop, not as an open advisory.

### ADV-20260708-027 — Sync Engineering Office Leaks architecture updates across Life OS

- Date: 2026-07-08
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High
- Status: Implemented
- Implemented: 2026-07-08
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Source Advisory: ADV-20260708-026

#### Outcome

Life Logistics synchronized Engineering's Office Leaks architecture across Life OS.

Engineering outputs preserved:

- `projects/engineering/notebook/NOTE-20260708-005-office-leak-delivery-playbooks-v1.md`
- `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`
- updated Engineering notebook indexes
- updated Drive document `Engineering Delivery Architecture Specification - HVAC Office Cleanup`

Current delivery model:

1. Mechanical workflow layer: map, score, scope, sprint, verify, handoff, follow up.
2. Human-system layer: respect, rapport, internal champion, users, Aha Moment, adoption verification, relational follow-up.

### ADV-20260706-020 — Adopt Finances-only session rule

- Status: Acknowledged / Implemented

Life Logistics adopted the Finances-only session rule as an observed operating pattern, not a confirmed claim about platform internals.

### ADV-20260706-018 — Simplify the Life OS Advisory Routing System

- Status: Acknowledged / Implemented

Life Logistics simplified advisory routing to use source department boards plus the Advisory Index as the sole active routing dashboard. Department Event Inbox is frozen as historical unless Rob explicitly reactivates it.

### ADV-20260706-017 — Adopt connector reliability operating pattern from Gemini/Drive tests

- Status: Acknowledged / Implemented

Life Logistics created `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md` as the durable operating note for explicit connector invocation, small verified writes, waiting after safety triggers, Gemini-as-optional-Drive-artifact-generator, and verification of generated artifacts.

### ADV-20260705-015 — Globalize department notebook leaf routing/index standard

- Status: Acknowledged / Implemented

Life Logistics updated `coordination/DEPARTMENT_NOTEBOOKS.md` to adopt notebook leaf folders, notebook indexes, leaf-note naming/format guidance, and scheduled-worker guidance.

### ADV-20260704-013 — Tighten advisory posting board rules

- Status: Acknowledged / Ingested

Life Logistics clarified that advisories live on the source department's board and target departments are routed through the Advisory Index.

### ADV-20260704-012 — Connector safety-trigger avoidance rules needed

- Status: Acknowledged / Ingested

Engineering incorporated connector safety-trigger avoidance into the Reliable Connector Execution Layer.

## Board Rule

- Formal advisories originate on the source department board.
- `coordination/ADVISORY_INDEX.md` is the sole active routing dashboard.
- `coordination/DEPARTMENT_EVENT_INBOX.md` remains frozen historical record unless Rob explicitly reactivates it.
- Full prior advisory text remains available through Git commit history.
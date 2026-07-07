# Session Handoff

Updated: 2026-07-06
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Fast baton-pass file for future Penny chat windows.

## Current Handoff

Life OS is operational with GitHub as durable memory map, Drive as working records cabinet, Todoist as Rob-facing action queue, Calendar as timed commitments, Gmail as communication evidence, project chats as knowledge producers, and Life Logistics HQ as cross-project curator.

## Current Active Core

- Life Logistics HQ
- Main Assistant / Daily Operations
- Chief of Finance Penny
- Chief Business HQ
- Chief Engineering Penny
- Chief Wellness HQ
- Life OS Infrastructure as needed

## Consolidated / Dormant Departments

- Work Search is consolidated into Main Assistant for current lightweight logistics and reminders.
- Support Pathway is consolidated into Main Assistant for current lightweight research and logistics.
- Daily Anchors / Recovery Logistics is dormant until Rob reactivates it.
- Philosophy HQ is dormant until Rob reactivates it.

Preserve project history. Do not delete department files.

## Current Durable Architecture

- Active Projects is the authoritative current project map: `memory/04_ACTIVE_PROJECTS.md`.
- Open Loops tracks current unfinished work: `memory/05_OPEN_LOOPS.md`.
- Advisory dashboard: `coordination/ADVISORY_INDEX.md`.
- Department Event Inbox: `coordination/DEPARTMENT_EVENT_INBOX.md`.
- Advisory details: `coordination/boards/`.
- Decision Rules Registry: `coordination/DECISION_RULES_REGISTRY.md`.
- Pending Advisory Boards standard: `coordination/PENDING_ADVISORY_BOARDS.md`.
- Department Notebooks standard: `coordination/DEPARTMENT_NOTEBOOKS.md`.
- Source-of-Truth and Publication Standard: `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md`.
- Connector Reliability Operating Pattern: `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md`.
- Design Principles: `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`.

## Current Advisory Rule

Advisories live on the source department's board.

The target department is named inside the advisory and routed through the Advisory Index and Department Event Inbox.

Template language uses `Posted Board` and `Target Department` rather than ambiguous `Target Board` language.

## Current Decision Rules

Decision Rules are reusable decision procedures.

Central registry:

- `coordination/DECISION_RULES_REGISTRY.md`

Active first rule:

- DR-FIN-20260704-001 — Discretionary Purchase Pause Rule, owned by Chief of Finance Penny.

## Current Engineering Reliability Track

Chief Engineering Penny owns Reliable Connector Execution Layer work.

Accepted connector safety rule:

> Prefer small, localized, verified connector writes over large, broad, unverified rewrites. If a connector write is blocked, stop, classify the failure, simplify the operation, and resume only with a smaller or safer plan.

Additional connector reliability pattern:

- Use explicit connector invocation when practical.
- Use small verified writes.
- Stop and wait after safety-trigger blocks.
- Use Gemini only as an optional Drive artifact-generation fallback or companion when direct Drive writes are risky.

## Current Open Advisory State

As of the 2026-07-06 nightly sync, ADV-20260706-018 is the only open advisory. It asks Life Logistics to evaluate whether the Department Event Inbox should remain an active routing file or whether the Advisory Index should become the sole active routing dashboard.

## Best Next Actions

- For Life Logistics: evaluate ADV-20260706-018 and decide whether to simplify advisory routing.
- For Engineering: continue connector safety-trigger rule design inside Reliable Connector Execution Layer.
- For Business: continue positioning, unit economics, business-model scoring, customer persona/use-case definition, and validation packet work.
- For Main Assistant: absorb lightweight daily logistics from consolidated departments.

## Guiding Principle

GitHub is the map. Drive is the filing cabinet. Calendar owns time. Todoist owns Rob-facing actions. Gmail owns communications. Captain's Log records meaningful operational sessions.

Use RPR when reliable structured-file editing matters more than connector automation.
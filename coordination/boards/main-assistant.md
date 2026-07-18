# Chief of Staff HQ Advisory Board

Updated: 2026-07-18
Purpose: Canonical advisory text sourced from Chief of Staff HQ, including formal advisories arising from LifeOS HQ meetings. The retained filesystem path remains `coordination/boards/main-assistant.md`.

## Open Advisories

### ADV-20260718-041 — Create a global Trello connector write SOP

- Date: 2026-07-18
- From: Chief of Staff HQ / LifeOS HQ
- To: Life OS Maintenance HQ
- Priority: High
- Status: Open / Routed
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Life OS Maintenance HQ
- Record Class: Global operating SOP request
- Authoritative Destination: Maintenance-owned global SOP path selected under existing repository ownership rules
- Lifecycle State: Open / Routed
- Review Trigger: Maintenance reads this advisory and inspects the verified Trello connector behavior
- Completion Condition: A global Trello connector SOP is created or an existing global connector SOP is updated, the advisory is acknowledged, and the Advisory Index routing state is reconciled

#### Context

During a LifeOS Hub capture session, Trello card creation and checklist creation succeeded. Checklist-item writes then returned a workspace-authorization error even though the requested items were written successfully after a delay. A later verification read showed that all separately submitted checklist items had landed.

The observed connector behavior creates a false-negative risk: an assistant may treat a successful write as failed, retry in bulk, create duplicates, overwrite useful state, or report an inaccurate outcome.

#### Requested Maintenance Work

Create or update a global Trello connector write SOP that can be inherited by every department permitted to perform Trello writes. The SOP should document at least:

1. Prefer small, bounded Trello writes rather than large multi-part payloads.
2. For checklist population, submit one checklist item per connector call.
3. Treat a connector error as inconclusive when prior behavior shows possible delayed success.
4. After any ambiguous Trello write response, perform a read-back verification against the live card, checklist, or Inbox state before retrying or reporting failure.
5. Do not duplicate a card, checklist, or checklist item until verification confirms the original write did not land.
6. Report the verified live state rather than relying solely on the connector receipt.
7. Preserve source-system boundaries: Trello remains the capture and flow layer, and this SOP must not authorize promotion into GitHub or creation of Rob-facing commitments.
8. Note that basic Inbox card creation was separately tested and succeeded, isolating the observed defect primarily to checklist-item and some update paths.

#### Verified Reproduction Evidence

- One idea-bundle card was created successfully.
- Eight checklist groups were created successfully.
- Initial checklist-item calls returned workspace-permission errors.
- Live read-back showed delayed successful writes.
- Fourteen remaining ideas were then submitted as fourteen separate connector calls.
- Every call reported the same misleading error.
- Final live read-back verified all sixteen intended checklist items across all eight groups.

#### Boundaries

- Maintenance owns the global SOP and advisory reconciliation.
- Engineering may later investigate or compensate for connector behavior, but this advisory does not assign implementation work to Engineering.
- Do not edit department-local files unless needed pointers are explicitly authorized under normal ownership rules.
- Do not create a duplicate system open loop merely for visibility unless the SOP work genuinely requires durable tracking under the existing operating rules.

## Acknowledged / Implemented Advisories

Historical entries below retain names and wording that were accurate when they were created.

### ADV-20260716-038 — Explore a read-mostly LifeOS desktop dashboard window

- Date: 2026-07-16
- From: Main Assistant Penny / LifeOS Coordination Hub
- To: Chief Engineering Penny
- Priority: Medium
- Status: Acknowledged / Ingested / Closed
- Acknowledged: 2026-07-16
- Closed: 2026-07-16
- Related Project(s): Life OS, desktop tooling, prompt launcher, Trello, Todoist, Google Calendar, Gmail, Google Drive
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny

#### Context

Rob is developing an early concept for a LifeOS desktop dashboard. The intent is not to replace Trello, Todoist, Google Calendar, Gmail, Google Drive, or Penny. It is a single desktop window that shows the most important active state from each system while Penny remains the worker that performs changes through conversation and connector-backed actions.

#### Ingested Engineering Direction

Engineering recognizes the dashboard as an active design concept with these boundaries:

- treat the dashboard as a window into LifeOS rather than a replacement productivity platform;
- preserve Trello, Todoist, Calendar, Gmail, and Drive as authoritative source systems;
- keep Penny as the conversational worker, coordinator, and connector operator;
- retain and reuse the existing prompt launcher and prompt database;
- center the first useful view on high-signal current state, especially Trello `Now`, top `Next`, daily commitments, near-term calendar pressure, mail-attention signals, and pinned working files;
- begin read-only or read-mostly;
- avoid direct write controls until observed need justifies them;
- keep account-linked financial connector data excluded from Hub or multi-connector operation under `coordination/FINANCIAL_CONNECTOR_ISOLATION_SOP.md`;
- turn the concept into a staged specification when Rob supplies further requirements.

No software implementation was authorized or performed under this advisory. The requested Engineering ingestion is complete.

### ADV-20260715-036 — Design prompts for seven LifeOS department discussion HQs

- Date: 2026-07-15
- From: Main Assistant Penny / LifeOS Coordination Hub
- To: Chief Engineering Penny
- Priority: High
- Status: Implemented / Acknowledged / Closed
- Implemented: 2026-07-15
- Acknowledged: 2026-07-15
- Closed: 2026-07-15
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny

#### Outcome

Rob confirmed that all seven LifeOS department discussion HQ chats are open and ready. The operating model preserves Chat/Work separation, explicit department boundaries, connector rules, truthful action reporting, Main Assistant coordination, and Rob's final authority. No separate prompt-design advisory work remains.

### ADV-20260715-035 — Standardize Rob's friction-aware daily operating pattern

- Date: 2026-07-15
- From: Main Assistant Penny / Daily Operations
- To: Chief Engineering Penny
- Priority: High
- Status: Implemented / Acknowledged / Closed
- Implemented: 2026-07-15
- Acknowledged: 2026-07-15
- Closed: 2026-07-15
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny

#### Outcome

Engineering verified that `memory/06_DAILY_OPERATING_SOP.md` is included in the canonical global boot order. Every department boot inherits the friction-aware daily pattern. No external task, calendar, mail, or Drive systems were changed.

### ADV-20260709-029 — Engineering implementation request for dedicated rapid capture worker GPT

- Date: 2026-07-09
- From: Main Assistant Penny
- To: Chief Engineering Penny
- Status: Closed / Implemented Through ADV-20260709-030
- Closed: 2026-07-09
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny

#### Outcome

Engineering defined a technology-independent worker contract. Life Logistics implemented the formal worker layer and Penny Raw Capture Worker package under ADV-20260709-030. No separate work remains.

## Current Board Rules

- Read `coordination/ADVISORY_INDEX.md` first rather than scanning every board.
- This retained path is the Chief of Staff HQ source board despite its legacy filename.
- When an advisory arises from a LifeOS HQ meeting, identify its source as `Chief of Staff HQ / LifeOS HQ`.
- LifeOS HQ does not maintain a separate advisory board.
- Keep canonical advisory text here and routing state in the Advisory Index.
- Do not duplicate advisory text into target boards or matching department open loops merely for visibility.
- Do not mark an advisory implemented or closed without verified handling.
- Keep all open advisories in enough detail to act and a bounded recent completed working set. Git history preserves older detail removed during compaction.
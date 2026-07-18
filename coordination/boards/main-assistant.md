# Chief of Staff HQ Advisory Board

Updated: 2026-07-18
Purpose: Canonical advisory text sourced from Chief of Staff HQ, including formal advisories arising from LifeOS HQ meetings. The retained filesystem path remains `coordination/boards/main-assistant.md`.

## Open Advisories

None.

## Acknowledged / Implemented Advisories

Historical entries below retain names and wording that were accurate when they were created.

### ADV-20260718-041 — Create a global Trello connector write SOP

- Date: 2026-07-18
- From: Chief of Staff HQ / LifeOS HQ
- To: Life OS Maintenance HQ
- Priority: High
- Status: Implemented / Acknowledged / Closed
- Implemented: 2026-07-18
- Acknowledged: 2026-07-18
- Closed: 2026-07-18
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Life OS Maintenance HQ
- Record Class: Global operating SOP request
- Durable Output: `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md`

#### Outcome

Life OS Maintenance HQ updated the existing global Connector Reliability Operating Pattern rather than creating a competing Trello-only source of truth. The global SOP now documents:

- small, bounded Trello mutations;
- exactly one checklist item per connector call;
- ambiguous connector errors as inconclusive when delayed success is possible;
- mandatory live read-back before retrying or reporting failure;
- card, checklist, checklist-item, and update duplicate prevention;
- verified live-state reporting when the connector receipt is misleading;
- the separately verified success of basic Inbox card creation;
- the observed false-negative risk around checklist-item and some update paths;
- Trello's continued role as the capture, possibility, attention, and flow layer;
- and the rule that Trello writes do not authorize GitHub promotion, Todoist commitments, Calendar events, or duplicate source records.

The SOP preserves the behavior as observed evidence rather than claiming platform internals, assigns later technical compensation to Engineering only if separately authorized, and creates no duplicate system open loop. The advisory's completion condition is satisfied.

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
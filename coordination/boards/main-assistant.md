# Main Assistant Advisory Board

Updated: 2026-07-16
Purpose: Advisories to or from Main Assistant / Daily Operations.

## Open Advisories

None.

## Acknowledged / Implemented Advisories

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

Rob confirmed that all seven LifeOS department discussion HQ chats are open and ready. The operating model preserves Chat/Work separation, explicit department boundaries, truthful connector reporting, Main Assistant coordination, and Rob's final authority. No separate prompt-design advisory work remains.

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

## Notes

Main Assistant should read `coordination/ADVISORY_INDEX.md` first rather than scanning every board.

This board keeps current open items and a bounded recent completed working set. Git history preserves prior detail removed during compaction.
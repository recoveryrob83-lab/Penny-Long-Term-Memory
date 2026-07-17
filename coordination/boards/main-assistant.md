# Main Assistant Advisory Board

Updated: 2026-07-16
Purpose: Advisories to or from Main Assistant / Daily Operations.

## Open Advisories

### ADV-20260716-038 — Explore a read-mostly LifeOS desktop dashboard window

- Date: 2026-07-16
- From: Main Assistant Penny / LifeOS Coordination Hub
- To: Chief Engineering Penny
- Priority: Medium
- Status: Open / Unacknowledged
- Related Project(s): Life OS, desktop tooling, prompt launcher, Trello, Todoist, Google Calendar, Gmail, Google Drive
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny

#### Context

Rob is developing an early concept for a LifeOS desktop dashboard. The intent is not to replace Trello, Todoist, Google Calendar, Gmail, Google Drive, or Penny. It is a single desktop window that shows the most important active state from each system while Penny remains the worker that performs changes through conversation and connector-backed actions.

#### Current Concept

The dashboard would surface a small, high-signal slice of each major operational system:

- Trello: current `Now`, top `Next`, selected waiting state, and possibly Inbox count;
- Todoist: due today, overdue, and highest-priority commitments;
- Google Calendar: today's timeline, next event, and near-term schedule pressure;
- Gmail: unread or needs-attention signals rather than a full mail client;
- Google Drive: pinned or recently used LifeOS working files;
- Prompt launcher: the existing prompt database and launcher as the primary directly usable component.

The dashboard itself should initially be read-only or read-mostly. Penny remains responsible for modifications, routing, synthesis, and connector execution through chat. The dashboard updates to reflect source-system changes.

#### Architectural Direction

- Treat the dashboard as a window into LifeOS, not a replacement productivity platform.
- Preserve existing systems as sources of truth.
- Reuse the existing prompt launcher and prompt database rather than discarding them.
- Keep the center of gravity on current active state, especially the Trello `Now` card.
- Avoid adding direct write controls until a real need justifies them.
- Design around desktop visibility and low-friction awareness.
- Keep the account-linked financial connector excluded from Hub or multi-connector operation under `coordination/FINANCIAL_CONNECTOR_ISOLATION_SOP.md`.

#### Requested Engineering Response

Chief Engineering Penny should ingest this as an active concept, evaluate feasible architecture and scope boundaries, and help Rob turn the idea into a staged specification when he arrives at Engineering HQ with further requirements. No implementation is authorized by this advisory alone.

## Acknowledged / Implemented Advisories

### ADV-20260715-036 — Design prompts for seven LifeOS department discussion HQs

- Date: 2026-07-15
- From: Main Assistant Penny / LifeOS Coordination Hub
- To: Chief Engineering Penny
- Priority: High
- Status: Implemented / Acknowledged / Closed
- Implemented: 2026-07-15
- Acknowledged: 2026-07-15
- Closed: 2026-07-15
- Related Project(s): Life OS, department HQ architecture, prompt design, Chat/Work separation, connector routing, model-usage discipline
- Source Location: `projects/main-assistant/NOTEBOOK.md`
- Source Note: `2026-07-15 — LifeOS Chat/Work architecture and seven discussion HQs`
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny

#### Outcome

Rob confirmed that all seven LifeOS department discussion HQ chats are open and ready.

The implemented operating model preserves:

- one coherent Penny expressed through structured departmental perspectives;
- persistent Chat-based HQ rooms for planning, discussion, synchronization, research, and light connector-backed work;
- Work mode for substantial coding, local repository work, test execution, packaging, browser or desktop automation, and complex artifact production;
- explicit department boundaries and routing;
- Main Assistant coordination and synthesis authority;
- truthful reporting of connector or external actions;
- Rob's final authority for consequential, destructive, financial, and externally visible actions;
- mobile-first, low-friction use; and
- smallest-capable-model discipline.

No external chats were created by Engineering through connectors. Rob completed the launch directly. The requested architecture is now operational, so no separate prompt-design advisory work remains.

### ADV-20260715-035 — Standardize Rob's friction-aware daily operating pattern

- Date: 2026-07-15
- From: Main Assistant Penny / Daily Operations
- To: Chief Engineering Penny
- Priority: High
- Status: Implemented / Acknowledged / Closed
- Implemented: 2026-07-15
- Acknowledged: 2026-07-15
- Closed: 2026-07-15
- Related Project(s): Main Assistant, Life OS, boot architecture, daily operations, cognitive-load reduction
- Source Location: `memory/06_DAILY_OPERATING_SOP.md`
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny

#### Outcome

Engineering verified that `memory/06_DAILY_OPERATING_SOP.md` is included in the canonical global boot order and added an explicit application section to `memory/STARTUP_BOOT.md`.

Every department boot now inherits the friction-aware pattern: one major action, at most one low-friction support action, sparse meaningful due dates, transit as a full major task, Penny-level preparation before Rob acts, preservation of recovery and health, and routing specialized judgment to the owning department.

No external task, calendar, mail, or Drive systems were changed.

### ADV-20260709-029 — Engineering implementation request for dedicated rapid capture worker GPT

- Date: 2026-07-09
- From: Main Assistant Penny
- To: Chief Engineering Penny
- Status: Closed / Implemented Through ADV-20260709-030
- Closed: 2026-07-09
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny

#### Outcome

Engineering defined a technology-independent worker contract rather than a custom-GPT-only design. Life Logistics implemented the formal worker layer, shared worker standard, Penny Raw Capture Worker package, canonical Sheet pointer, startup routing, and downstream Main Assistant processing responsibility under ADV-20260709-030.

No separate work remains under ADV-029.

### ADV-20260706-016 — Gemini Drive worker succeeded where direct connector writes may be risky

- Date: 2026-07-06
- From: Main Assistant
- To: Chief Engineering Penny; Life Logistics HQ
- Status: Acknowledged / Closed
- Posted Board: `coordination/boards/main-assistant.md`

#### Outcome

Engineering recognizes Gemini as a candidate Drive-native execution fallback under the Reliable Connector Execution Layer. Life Logistics consumed the operating lesson. Penny remains responsible for planning, routing, verification, and abstract durable records; Rob may handle manual placement when a Drive-native worker cannot place an artifact correctly.

### ADV-20260704-011 — Department consolidation and archival request

- Date: 2026-07-04
- From: Main Assistant
- To: Life Logistics HQ
- Status: Acknowledged / Ingested
- Posted Board: `coordination/boards/main-assistant.md`

#### Outcome

Work Search and Support Pathway were consolidated into Main Assistant for lightweight current work. Daily Anchors / Recovery Logistics and Philosophy HQ were marked dormant until reactivated. Project history was preserved.

## Notes

Main Assistant should read `coordination/ADVISORY_INDEX.md` first rather than scanning every board.

This board keeps current open items and a bounded recent completed working set. Git history preserves prior detail removed during compaction.
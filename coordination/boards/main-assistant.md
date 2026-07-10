# Main Assistant Advisory Board

Updated: 2026-07-09
Purpose: Advisories to or from Main Assistant / Daily Operations.

## Open Advisories

None.

## Acknowledged / Implemented Advisories

### ADV-20260709-029 — Engineering implementation request for dedicated rapid capture worker GPT

- Date: 2026-07-09
- From: Main Assistant Penny
- To: Chief Engineering Penny
- Priority: High
- Status: Closed / Implemented Through ADV-20260709-030
- Closed: 2026-07-09
- Related Project(s): Life OS, Main Assistant, worker architecture, rapid capture workflow, connector routing, raw capture processing
- Source Location: `projects/main-assistant/NOTEBOOK.md`
- Source Note: `2026-07-09 — Dedicated rapid capture worker GPT`
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny
- Engineering Follow-up Advisory: `ADV-20260709-030`

#### Summary

Rob requested a dedicated lightweight worker for rapid midday idea and request capture, especially when several requests or ideas arrive in quick succession.

The requested outcome was a narrow, low-friction intake path that preserves information first and leaves classification, routing, prioritization, task creation, advisories, and project-state changes for later processing.

#### Engineering Architecture Decision

Chief Engineering Penny completed the architecture investigation and determined that the durable abstraction should be a technology-independent Life OS worker contract rather than a custom-GPT-only design.

Engineering selected this MVP architecture:

- One formal Life OS worker layer, separate from departments and HQs.
- One central Google Sheet inbox rather than direct routing into multiple GitHub notebooks during intake.
- Penny Raw Capture Worker as the first worker.
- Main Assistant Penny as the downstream processor.
- Mandatory connector invocation, canonical resource identity, post-write verification, failure truthfulness, and privacy boundaries.

Engineering routed the durable implementation package to Life Logistics HQ through ADV-20260709-030.

#### Implementation Outcome

Life Logistics HQ implemented the complete package under ADV-20260709-030.

Created:

- `workers/README.md`
- `workers/WORKER_STANDARD.md`
- `workers/penny-raw-capture/WORKER_BOOT.md`
- `workers/penny-raw-capture/SESSION_HANDOFF.md`
- `workers/penny-raw-capture/IMPLEMENTATION_REPORT.md`

Canonical capture Sheet verified:

- Title: `Life OS Raw Capture Inbox`
- Stable Sheet ID recorded in `workers/penny-raw-capture/SESSION_HANDOFF.md`
- Schema: `Captured At`, `Raw Note`, `Processed`

Boot routing, Main Assistant downstream processing responsibility, global handoff, open loops, and advisory state were updated.

#### Final Closure

ADV-20260709-029 and ADV-20260709-030 are one completed package of work:

1. ADV-029 defined the need and requested Engineering architecture.
2. Engineering completed the architecture and created ADV-030.
3. ADV-030 carried the durable implementation to Life Logistics.
4. Life Logistics implemented and verified the worker layer.

No separate implementation work remains under ADV-029.

### ADV-20260706-016 — Gemini Drive worker succeeded where direct connector writes may be risky

- Date: 2026-07-06
- From: Main Assistant
- To: Chief Engineering Penny; Life Logistics HQ
- Priority: High
- Status: Acknowledged / Closed
- Related Project(s): Life OS, Google Drive workflows, connector reliability, Reliable Connector Execution Layer, Gemini worker evaluation
- Source Location: Main Assistant chat
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department(s): Chief Engineering Penny; Life Logistics HQ

#### Summary

Rob tested a workflow where Gemini created a Google Drive spreadsheet template that contained structured life-administration intake fields. This is the type of Drive artifact that may be cumbersome or risky for direct ChatGPT Drive connector writes because prior structured-document workflows have triggered connector safety blocks.

Gemini created the sheet quickly and with little friction. Rob reported that it completed the file faster than Main Assistant likely could have through direct Drive connector operations.

The observed limitation was placement: Gemini could create the sheet, but could not move it into the correct Drive folder. Rob moved the sheet manually.

#### Why It Matters

This suggests Gemini may be useful as a Drive-native worker for certain Google Docs or Sheets creation tasks, while Penny remains responsible for planning, prompt crafting, routing, audit, GitHub memory, and process coordination.

Possible Life OS division of labor:

- Penny: plan the artifact, craft the Gemini prompt, keep GitHub records abstract, and audit the outcome.
- Gemini: create or edit selected Drive-native artifacts.
- Rob: manually move the file when Gemini cannot place it correctly.

#### Suggested Engineering Review

Chief Engineering Penny should evaluate whether Gemini handoff belongs in the Reliable Connector Execution Layer as a fallback or companion workflow for Drive artifact creation.

Engineering questions:

- When should Penny route a Drive artifact build to Gemini instead of direct connector write attempts?
- What file types fit this pattern best?
- What verification steps should Penny use after Rob reports Gemini completed the file?
- How should folder-placement limitations be logged and handled?

#### Suggested Logistics Review

Life Logistics HQ should decide whether this needs a durable operating note or standard procedure for Gemini-as-Drive-worker handoffs.

Suggested standard pattern:

- Use Penny to craft the Gemini prompt.
- Keep durable GitHub notes abstract.
- Keep detailed working records in Drive.
- Have Rob manually move the created file when needed.
- Record only the artifact purpose and pointer/reference in durable memory.

#### Acknowledgement / Outcome

Engineering and Life Logistics consumed this advisory on 2026-07-06.

Outcome:

- Engineering recognizes Gemini as a candidate Google Workspace / Drive execution worker to evaluate under the Reliable Connector Execution Layer.
- Life Logistics consumed the advisory as an operating-standard consideration.
- Advisory closed after both targets consumed it.

### ADV-20260704-011 — Department consolidation and archival request

- Date: 2026-07-04
- From: Main Assistant
- To: Life Logistics HQ
- Priority: High
- Status: Acknowledged / Ingested
- Related Project(s): Main Assistant, Life Logistics HQ, Recovery Logistics, Philosophy HQ, Job Search HQ, Caregiver Project HQ, Life OS
- Source Location: Main Assistant chat
- Source Board: `coordination/boards/main-assistant.md`

#### Summary

Rob decided to reduce active Penny department load by consolidating several departments into Main Assistant / Daily Operations and marking some specialist departments dormant until needed.

#### Outcome

Life Logistics updated the active project map in `memory/04_ACTIVE_PROJECTS.md`.

Implemented routing:

- Work Search consolidated into Main Assistant for current lightweight logistics.
- Support Pathway consolidated into Main Assistant for current lightweight logistics.
- Daily Anchors / Recovery Logistics marked dormant until Rob reactivates it.
- Philosophy HQ marked dormant until Rob reactivates it.
- Project history is preserved; department files were not deleted.

Note: attempts to update `memory/05_OPEN_LOOPS.md` and `projects/life-logistics-hq/SESSION_HANDOFF.md` were blocked by connector safety checks. The canonical project map update succeeded.

## Notes

Main Assistant should usually read `coordination/ADVISORY_INDEX.md` first rather than scanning every board.

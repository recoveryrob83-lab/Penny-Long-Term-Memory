# Main Assistant Advisory Board

Updated: 2026-07-06
Purpose: Advisories to or from Main Assistant / Daily Operations.

## Open Advisories

None.

## Acknowledged / Implemented Advisories

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

Use this board when daily operations needs to notify or receive guidance from other departments.

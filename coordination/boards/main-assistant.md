# Main Assistant Advisory Board

Updated: 2026-07-09
Purpose: Advisories to or from Main Assistant / Daily Operations.

## Open Advisories

### ADV-20260709-029 — Engineering implementation request for dedicated rapid capture worker GPT

- Date: 2026-07-09
- From: Main Assistant Penny
- To: Chief Engineering Penny
- Priority: High
- Status: Open / Unacknowledged
- Related Project(s): Life OS, Main Assistant, GitHub notebooks, custom GPT workers, rapid capture workflow, connector routing, nightly notebook review
- Source Location: `projects/main-assistant/NOTEBOOK.md`
- Source Note: `2026-07-09 — Dedicated rapid capture worker GPT`
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department(s): Chief Engineering Penny

#### Summary

Rob wants to implement a dedicated lightweight GPT / worker for rapid midday idea and request capture, especially when Marqueto provides several requests or ideas in quick succession.

The worker should let Rob type or speak quickly, determine the likely department or project, apply standard routing metadata, and write the capture into the appropriate GitHub notebook using a consistent template.

The worker is not intended to replace Main Assistant, department HQs, or nightly review. Its role is narrow: preserve incoming thoughts and requests with minimal friction so they can be reviewed, deduplicated, prioritized, promoted, or discarded later.

#### Core Design Principle

Optimize for speed and preservation, not judgment.

The worker should capture first and avoid premature planning, task creation, advisory creation, or project-state changes unless Rob explicitly requests them.

#### Required Worker Behavior

The first implementation should support:

- Rapid typed or spoken intake.
- GitHub connector access with permission to read notebook routing instructions and write notebook captures.
- Automatic selection of the most likely department or project notebook.
- A standard capture template.
- Preservation of Rob's raw wording where practical.
- Explicit status marking as `Raw / unprocessed`.
- No automatic Todoist tasks, Open Loop changes, advisories, project plans, or source-of-truth updates.
- A safe fallback destination when routing confidence is low, likely Main Assistant Notebook or a dedicated capture inbox.
- Compatibility with the existing 9:00 PM notebook review workflow.

#### Proposed Capture Fields

- Date / timestamp.
- Source or context.
- Raw capture.
- Suggested routing destination.
- Capture type: task candidate, idea, preference, fact, question, reminder, or project input.
- Urgency signal only when clearly stated by Rob.
- Status: Raw / unprocessed.

#### Suggested Engineering Deliverables

Chief Engineering Penny should evaluate and produce the smallest viable implementation package, likely including:

1. A formal worker specification document.
2. Reusable custom GPT instruction text.
3. A GitHub notebook routing table.
4. Standard capture templates for notebook entries and leaf notes.
5. Connector setup and permission checklist.
6. Fallback behavior for uncertain routing or failed writes.
7. Verification rules after a GitHub write.
8. Nightly reconciliation contract between the capture worker and Main Assistant.
9. A simple first-run test plan using real but non-sensitive capture examples.

#### Engineering Questions

- Should the worker write directly into department notebooks or write first into one central capture inbox that Main Assistant routes later?
- What minimum routing taxonomy is needed for Main Assistant, Office Leaks, Housing Logistics, Job Search, Caregiver, Finance, Engineering, and Recovery-related captures?
- How should the worker avoid overwriting or restructuring existing notebook files?
- Should each capture append to a department `NOTEBOOK.md`, create a dated leaf note, or choose based on size/type?
- What verification step confirms that the write succeeded and landed in the intended location?
- What guardrails are needed to prevent sensitive personal, medical, financial, client, or credential data from entering GitHub?
- How should the worker behave when Rob's spoken input contains several distinct items for different departments?

#### Suggested First Test Case

Use the Marqueto rapid-request scenario as the first test:

- Rob speaks or types several household, caregiver, scheduling, and personal requests in one burst.
- Worker separates distinct captures without overinterpreting them.
- Worker routes each item to the correct notebook or fallback inbox.
- Worker confirms what was captured and where.
- Main Assistant reviews the captures during the nightly notebook review and promotes only the items that warrant action.

#### Requested Outcome

Chief Engineering Penny should acknowledge this advisory, review the source note, recommend the MVP architecture, and create the first implementation package for Rob to use as a practical custom GPT case study.

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

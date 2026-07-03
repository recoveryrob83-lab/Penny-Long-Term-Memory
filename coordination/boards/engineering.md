# Engineering Advisory Board

Updated: 2026-07-03
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

### ADV-20260703-007 — Scheduled advisory watcher and inbox procedure

Date: 2026-07-03
From: Chief Engineering Penny / Engineering HQ
To: Life Logistics HQ
Priority: High
Status: Open

#### Summary
Engineering and Rob identified the lowest-friction v0.1 solution for reducing Rob's manual advisory-routing burden.

Instead of building a local Python watcher, Todoist API integration, or full external orchestration service, use a single ChatGPT scheduled task as an Advisory Watcher.

#### Current Problem
The Life OS advisory system works, but Rob is still the manual routing layer.

Current pain:

- Departments can create advisories in GitHub.
- The central Advisory Index exposes open advisories.
- The Department Event Inbox now exists for abstract advisory/read/ingestion state.
- However, Rob still has to remember to tell each target chat to check the advisory or inbox.
- Todoist is not the proper source of truth for system synchronization state.
- Local automation would require machine access, setup, Python learning, and possibly API work.

#### Proposed v0.1 Solution
Use one scheduled task chat as an Advisory Watcher.

The scheduled task should:

1. Check GitHub `coordination/ADVISORY_INDEX.md` and/or `coordination/DEPARTMENT_EVENT_INBOX.md` on a recurring cadence.
2. Identify open advisories or unread department inbox items.
3. Generate a concise report for Rob only when routing is needed.
4. Include copy-paste-ready messages Rob can paste into the target HQ chat.
5. Avoid modifying GitHub during the watcher run unless Rob later explicitly approves that behavior.

#### Example Watcher Output

If Engineering creates an advisory for Life Logistics HQ, the watcher could produce:

```text
Advisory routing needed:

Target: Life Logistics HQ
Advisory: ADV-20260703-007
Board: coordination/boards/engineering.md

Copy/paste into Life Logistics HQ:

Please check GitHub advisory ADV-20260703-007 in coordination/boards/engineering.md. Read it, update the Department Event Inbox and any relevant boot/handoff/log/open-loop procedure files if appropriate, and report back with what changed and what remains open.
```

#### Engineering Recommendation
Treat the scheduled-task watcher as a lightweight notification layer, not as the authoritative inbox.

Authority should remain:

- `coordination/ADVISORY_INDEX.md` for advisory dashboard state.
- `coordination/DEPARTMENT_EVENT_INBOX.md` for department read/ingestion state.
- Department boards for advisory detail.

The scheduled task is only a watcher/reporter that reduces Rob's memory and typing load.

#### Requested Life Logistics HQ Action
When Rob routes this advisory to Life Logistics HQ, please:

1. Read this advisory.
2. Decide where the Advisory Watcher procedure belongs in durable Life OS memory.
3. Add the procedure to the relevant operating file(s), likely one or more of:
   - `memory/STARTUP_BOOT.md`
   - `memory/01_SESSION_HANDOFF.md`
   - `memory/03_OPERATIONAL_RULES.md`
   - `coordination/DEPARTMENT_EVENT_INBOX.md`
   - `projects/life-os-infrastructure/SESSION_HANDOFF.md`
4. Define the expected scheduled-task watcher prompt or operating instructions.
5. Ensure future department handoffs can be updated to tell departments:
   - when creating an advisory, update the Advisory Index and Department Event Inbox;
   - the scheduled watcher will monitor those files and generate Rob-facing routing messages;
   - departments still report changes back to Rob for verification.
6. Report back to Rob with what was updated and what remains open.

#### Notes
This is intentionally a low-code/no-code bridge. It avoids local machine dependency, Python setup, and Todoist API costs. It does not solve full inter-chat automation, but it reduces Rob's reminder burden and creates a repeatable procedure for routing advisories.

## Acknowledged / Implemented Advisories

### ADV-20260703-006 — Engineering HQ online and Drive scaffold created

Date: 2026-07-03
From: Chief Engineering Penny / Engineering HQ
To: Life Logistics HQ
Priority: High
Status: Acknowledged

#### Summary
Chief Engineering Penny is online as a specialist department. Engineering HQ booted from GitHub, confirmed scope, created its Google Drive working folder under Life Organization, and created initial working scaffolding files.

#### Drive Work Completed
Created Drive folder:

- `Chief Engineering Penny`

Created and seeded working files:

- `Engineering HQ - Technical Baseline`
- `Engineering HQ - Implementation Packet Template`
- `Engineering HQ - Tracker`

#### Context Update
Engineering read Business HQ's `Penny Platform Product Hypothesis v0.3` from Drive and updated working context.

Engineering interpretation:

- Penny is best understood as a trusted AI Chief of Staff / personal operating system, not merely another chatbot.
- The strongest product pain is coordination burden across many apps, projects, commitments, records, and long-running life domains.
- The key technical problem is orchestration, event routing, memory, permissions, workflow boundaries, and source-of-truth discipline.
- The current Life OS system is functioning, but Rob is still the manual message bus between specialist chats.

#### System Improvement Insight
The missing capability is an event/advisory inbox layer.

Life Logistics HQ created:

- `coordination/DEPARTMENT_EVENT_INBOX.md`

This inbox tracks abstract department advisory/read/ingestion state. Todoist remains for Rob-facing action items.

#### Acknowledgement / Outcome
Life Logistics HQ read and ingested this advisory.

Updates completed:

- Department Event Inbox created.
- Global session handoff updated.
- Advisory Index updated.
- Captain's Log updated.

Startup Boot update was attempted but blocked by connector safety during this pass. The inbox is discoverable through the global session handoff and can be added to Startup Boot later with a smaller patch if needed.

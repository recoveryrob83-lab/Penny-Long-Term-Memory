# Engineering Advisory Board

Updated: 2026-07-03
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

### ADV-20260703-006 — Engineering HQ online and Drive scaffold created

Date: 2026-07-03
From: Chief Engineering Penny / Engineering HQ
To: Life Logistics HQ
Priority: High
Status: Open

#### Summary
Chief Engineering Penny is online as a specialist department. Engineering HQ booted from GitHub, confirmed scope, created its Google Drive working folder under Life Organization, and created initial working scaffolding files.

#### Drive Work Completed
Created Drive folder:

- `Chief Engineering Penny`

Created and seeded working files:

- `Engineering HQ - Technical Baseline`
  - Purpose: working technical architecture map for Engineering HQ.
  - Includes architecture zones, operating rules, current Life OS architecture snapshot, open questions, decision log, and starter risk register.

- `Engineering HQ - Implementation Packet Template`
  - Purpose: reusable build-ready packet template for coding, repository, API, connector, automation, and testing work.
  - Includes goal, scope, source decision, technical requirements, architecture notes, data model, storage location, API/connector plan, security guardrails, implementation sequence, testing strategy, risks, done criteria, verification, and report-back format.

- `Engineering HQ - Tracker`
  - Purpose: operational tracker for engineering decisions, risks, repos, APIs/connectors, implementation packets, and automation ideas.
  - Tabs created: `Decisions`, `Risks`, `Repos`, `APIs & Connectors`, `Implementation Packets`, `Automation Ideas`.

#### Context Update
Engineering read Business HQ's `Penny Platform Product Hypothesis v0.3` from Drive and updated working context.

Engineering interpretation:

- Penny is best understood as a trusted AI Chief of Staff / personal operating system, not merely another chatbot.
- The strongest product pain is coordination burden across many apps, projects, commitments, records, and long-running life domains.
- The key technical problem is orchestration, event routing, memory, permissions, workflow boundaries, and source-of-truth discipline.
- The current Life OS system is functioning, but Rob is still the manual message bus between specialist chats.

#### Current Engineering Discussion / System Improvement Insight
Rob identified the current operational pain:

- There are now roughly ten specialist chats with their own working folders, GitHub folders, and manual coordination needs.
- Advisories exist, but Rob must still remember to tell each department to check advisories.
- Life Logistics HQ is acting as Chief of Staff and uses GitHub as the source for core state, but cannot automatically update or notify departments.
- Scheduled tasks are not a clean solution because they can create new chats and have undesirable side effects.

Engineering analysis:

The missing capability is an event/advisory inbox layer.

When an advisory is created, the system should automatically record that Life Logistics HQ, or another target department, has an unread item requiring ingestion. This should not be treated as a normal Todoist task. Todoist owns user action items; this is system synchronization state.

Recommended concept:

- Add a lightweight `Department Event Inbox` or `Advisory Notification Register` to Life OS infrastructure.
- Each advisory creation should append/update a row or entry indicating:
  - advisory ID
  - source department
  - target department(s)
  - priority
  - status
  - whether Rob has been told to route it
  - whether each department has acknowledged/read it
  - whether Life Logistics HQ has ingested it into boot/handoff/logs if needed
- Life Logistics HQ can then check one canonical inbox instead of relying on Rob's memory.
- This should remain abstract and non-sensitive in GitHub, with detailed records in Drive if needed.

#### Requested Life Logistics HQ Action
When Rob routes this advisory to Life Logistics HQ, please:

1. Read this advisory.
2. Update relevant Life OS boot/handoff/log/open-loop files if appropriate.
3. Consider whether a lightweight advisory/event inbox should be added to Life OS Infrastructure.
4. If implemented, define whether it belongs in GitHub as Markdown, in Drive as a sheet, or both.
5. Report back to Rob with what was updated and what remains open.

#### Notes
No secrets, credentials, API keys, or sensitive implementation details were stored here.

## Acknowledged / Implemented Advisories

None yet.

# Main Assistant HQ Status

Updated: 2026-07-17
Project: Main Assistant / Daily Operations
Status: Active / Operational

## Current Status

Main Assistant is operational as Rob's primary everyday assistant and LifeOS Coordination Hub.

It handles daily planning, practical coordination, executive-function support, cross-department synthesis, one-off admin, light connector-backed work, Trello Inbox processing, Flow Board maintenance, task capture and routing, advisory preparation, and downstream worker-intake processing when authorized.

## Current Phase

Operational use and refinement.

The friction-aware Daily Operating SOP is active through the global boot sequence and should be tested in ordinary daily planning rather than expanded into another layer of bureaucracy.

The hub is the primary conversational front door for LifeOS. Separate department HQ chats remain specialist rooms with their own durable GitHub ownership and drift-management responsibility.

## Active Systems

- GitHub project folder: `projects/main-assistant/`
- Global Daily Operating SOP: `memory/06_DAILY_OPERATING_SOP.md`
- Trello Flow Board SOP: `coordination/TRELLO_FLOW_BOARD_SOP.md`
- LifeOS Flow Board: https://trello.com/b/QKXdwHup/lifeos-flow-board
- Department ownership SOP: `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
- Chat/Work policy: `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`
- LifeOS Dashboard: locally running read-mostly interface with GitHub, Trello, Todoist, and Google Calendar private iCal
- Desktop department automation: `apps/lifeos-dashboard/automation/draft_department_boot.py`
- Todoist: Rob-facing commitments and reminders
- Calendar: appointments and timed commitments
- Gmail: searches, summaries, evidence, and drafts
- Drive: working records and human-facing artifacts
- Advisory dashboard: `coordination/ADVISORY_INDEX.md`

## Current Operating Priorities

- Keep daily planning limited to one major action and at most one useful support action.
- Reduce friction through preparation before asking Rob to act.
- Use Trello Inbox for fast raw capture and the LifeOS Flow Board for visual attention management.
- Preserve one card maximum in Now and three maximum in Next.
- Keep Todoist as the commitments and reminders system rather than duplicating every Flow Board card there.
- Use the dashboard for quick orientation while preserving source-system authority.
- Treat desktop department automation as an on-demand boot transport, not an autonomous agent or unattended scheduler.
- Coordinate department perspectives without pretending they are autonomous agents.
- Use regular Chat, especially classic desktop when connectors are needed, for substantial reasoning and connector-backed work where available.
- Treat both Work-side Chat and Work Tasks as metered.
- Reserve Work for bounded local-computer execution and default Work tasks to Luna Light unless escalation is justified.
- Keep Office Leaks visible as the immediate revenue-first LifeOS priority while routing specialist strategy to Business and Office Leaks HQ.
- Process Raw Capture Worker inbox rows only when Rob authorizes or requests review.
- Keep Inventory Worker capture separate from pricing, listing, bundling, and publication.
- Use connectors for focused, scoped actions and verify important writes.

## Current Evidence

- The LifeOS Dashboard is live with four verified sources and 16 passing tests.
- Guarded GitHub auto-sync is limited to clean, strictly-behind fast-forward updates.
- Windows desktop boot automation passed draft-mode validation across all seven HQs.
- A watched live send to Main Assistant HQ succeeded and initiated a normal reboot.
- Office Leaks is publicly launched and in live organic market testing.
- Trello is active as the visual flow system and the mobile Now widget targets the correct list.

## Operating Boundary

Use Main Assistant for everyday operations and coordination.

Trello shows capture and current attention. Todoist holds commitments. Calendar holds time. GitHub holds durable state. Drive holds working records. Gmail holds communication evidence. The dashboard displays selected state.

Route project-sized or specialist judgment to the correct department. Main Assistant owns synthesis and authorized hub-level execution, not every domain's strategy or durable state.

Each department maintains its own canonical GitHub files. Logistics retains shared infrastructure, global hygiene, and cross-project audit responsibility. Engineering owns dashboard and desktop-automation implementation.

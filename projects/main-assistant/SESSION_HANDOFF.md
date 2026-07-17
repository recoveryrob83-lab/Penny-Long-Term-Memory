# Main Assistant HQ Session Handoff

Updated: 2026-07-17
Project: Main Assistant / Daily Operations
Purpose: Project-specific handoff for new Main Assistant HQ / LifeOS Coordination Hub chats.

## Role

Main Assistant is Rob's default daily operations desk and primary LifeOS Coordination Hub.

Use this department for daily planning, itinerary checks, practical coordination, one-off admin, reminders, light connector-backed work, cross-department synthesis, advisory preparation, Trello Inbox processing, raw-capture processing, and routing larger work to specialist departments.

Large ongoing work belongs in the relevant specialist department.

## Boot Instructions

1. Read the global boot files from `memory/STARTUP_BOOT.md` in order.
2. Read this handoff.
3. Read `projects/main-assistant/DEPARTMENT_IDENTITY.md`.
4. Read `projects/main-assistant/README.md`, `status.md`, and `open_loops.md`.
5. Apply `memory/06_DAILY_OPERATING_SOP.md` as the default planning standard.
6. Stay focused on daily operations and coordination.
7. Route project-sized or specialist judgment outward.

## Daily Operating Pattern

For an ordinary day:

1. Select one major action that materially moves life forward.
2. Add at most one low-friction support action when useful.
3. Treat leaving home, transit, unfamiliar routes, appointments, and other high-friction commitments as complete major tasks.
4. Prepare Penny-level work before asking Rob to act.
5. Keep due dates sparse and meaningful.
6. Preserve recovery, health, and basic-life commitments without creating an anxiety-producing checklist.
7. Judge success by completion and reduced friction, not task count.

## Hub Operating Model

Main Assistant chairs one coherent Penny system and is the primary conversational front door for LifeOS.

Department tags provide structured perspectives but do not represent independently running agents or independent connector access.

Main Assistant owns final hub synthesis, daily-life coordination, executive-function support, and authorized connector execution. Rob remains the final decision-maker for consequential, destructive, financial, and externally visible actions.

## Trello Flow Board

Trello is the canonical visual attention and flow surface.

Canonical procedure:

- `coordination/TRELLO_FLOW_BOARD_SOP.md`

Source boundaries:

- Trello Inbox captures raw thoughts and quick actions.
- LifeOS Flow Board shows current attention and active flow.
- Todoist holds commitments, reminders, and due-date obligations.
- Calendar holds timed commitments.
- GitHub holds durable project state.

Flow limits:

- One card maximum in Now.
- Three cards maximum in Next.
- Waiting contains blocked work only.
- Captured contains ideas, not promises.

Commands:

- `/FLOW @Trello` reads and recommends routing; read-only by default.
- `/FLOW PROCESS @Trello` processes clear Inbox cards while preserving limits; cross-system writes and deletions still require clear authorization.
- `/FLOW NOW @Trello` recommends one Now card and up to three Next cards; moves require authorization.

## LifeOS Dashboard

The locally running LifeOS Dashboard is a read-mostly visibility layer, not a new source of truth.

Verified live sources:

- GitHub
- Trello
- Todoist
- Google Calendar private iCal

Main Assistant may use the dashboard for rapid orientation, then use the authoritative source system or connector for consequential interpretation and all writes.

Guarded GitHub auto-sync only fast-forwards a clean, strictly-behind local `main`. Gmail and Drive dashboard adapters remain deferred until demonstrated need.

## Desktop Department Automation

Windows ChatGPT Classic automation is operational across all seven department HQs.

Canonical launcher:

- `apps/lifeos-dashboard/automation/draft_department_boot.py`

The automation can navigate to an exact HQ, preserve an occupied composer, insert and clipboard-verify the canonical boot prompt, and submit only with explicit `--send` authorization.

A watched live send to Main Assistant HQ succeeded and began a normal reboot. Main Assistant should treat this as an on-demand boot transport, not an autonomous agent or unattended scheduler.

If GitHub is cold in the destination chat, manually invoke GitHub and retry. Do not assume the automation can verify connector activation.

## Chat and Work Boundary

- Regular Chat is headquarters.
- Treat both Work-side Chat and Work Tasks as metered.
- Prefer classic desktop when connector-enabled desktop conversation is sufficient.
- Use Luna Light as the default Work model and escalate only when required.
- Reserve Work for local files, terminal, coding, testing, browser or desktop control, artifact production, and other bounded execution.

Canonical policy:

- `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`

## Department File Ownership

Each department maintains the GitHub files and sections within its own domain and corrects drift during routine boots and syncs.

Routine local maintenance should not be routed through Logistics or formal advisories. Use advisories only when work crosses department boundaries or requires durable shared action, decision, risk, or dependency communication.

Canonical SOP:

- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`

## Worker Relationships

Penny Raw Capture Worker and Penny Inventory Worker are narrow workers, not Main Assistant sub-departments.

Main Assistant owns authorized downstream processing of raw capture and inventory output. Do not mark capture processed until downstream handling is actually complete. Keep inventory capture separate from pricing, bundling, listing copy, sale strategy, and publication.

## Advisory Procedure

Use `coordination/ADVISORY_INDEX.md` as the sole active advisory routing dashboard.

Read a source board only when the index points to a relevant open advisory or Rob names it. Do not update the frozen Department Event Inbox for normal routing.

Current advisory state:

- No open advisories as of 2026-07-17.

## Current Routing Notes

- Office Leaks remains the immediate revenue-first business priority. Route strategy, positioning, offers, and delivery design to Business HQ and Office Leaks HQ; keep one-off logistics in Main Assistant.
- Work Search and Support Pathway are consolidated into Main Assistant for lightweight current logistics.
- Recovery Logistics and Philosophy HQ remain dormant until Rob reactivates them.
- Logistics HQ owns shared operational infrastructure, global hygiene, and cross-project curation.
- Engineering HQ owns dashboard and desktop-automation implementation.
- Main Assistant should not become the project junk drawer.

## Operating Boundaries

- Keep durable GitHub notes abstract.
- Trello shows capture and current attention.
- Todoist holds commitments and reminders.
- Calendar owns timed commitments.
- Gmail owns communication evidence.
- Drive holds working records.
- The dashboard displays selected state but does not own it.
- Treat worker or Inbox output as intake, not automatically as tasks or priorities.
- Verify important connector writes.
- Ask before consequential, destructive, financial, or externally visible actions.

## Next Actions

When asked, Main Assistant should:

1. Build a realistic daily operating picture.
2. Identify one major action and at most one support action.
3. Process Trello Inbox and maintain Flow Board limits when authorized.
4. Handle one-off daily admin and light connector work.
5. Use the dashboard for orientation without bypassing source systems.
6. Report advisory status during full reports or direct advisory requests.
7. Process worker inbox items when authorized.
8. Route specialist work to the correct department.
9. Keep durable updates small, scoped, and verified.

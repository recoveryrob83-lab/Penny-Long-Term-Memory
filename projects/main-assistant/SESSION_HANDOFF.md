# Chief_of_Staff_HQ Session Handoff

Updated: 2026-08-01
Project: Chief_of_Staff_HQ / Daily Operations
Purpose: Project-specific handoff for Rob's primary point of contact, personal-assistant headquarters, daily-operations desk, `LifeOS_HQ` chair, routing desk, and follow-through coordinator.

## Replacement-Chat Note

This handoff was refreshed after the V2 advisory courier contract became active and the current advisory state changed.

A replacement chat should reconstruct authority and current context from the canonical Boot sequence and current project files rather than treating an old conversation as authoritative. The Chief of Staff chat handbook may accelerate orientation, but it is a noncanonical context mirror and does not replace GitHub, current connector reads, focused Sync, or verification before consequential action.

## Role

`Chief_of_Staff_HQ` is Rob's default daily operations desk and primary conversational point of contact.

Use this department for daily planning, itinerary checks, practical coordination, one-off admin, reminders, light connector-backed work, cross-department synthesis, receiving department reports, assignment routing, follow-through, advisory preparation, Trello Inbox processing, raw-capture processing, and routing larger work to specialist departments.

`LifeOS_HQ` is a separate shared meeting room. Chief of Staff chairs it, synthesizes department input, transfers real actions to one owning department and one authoritative destination, and checks follow-through. `LifeOS_HQ` itself does not own a backlog or durable department state.

Large ongoing work and specialist judgment remain with the relevant owning department.

## Boot Instructions

1. Read the universal operating kernel from `memory/STARTUP_BOOT.md` in order.
2. Read `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`.
3. Read this handoff.
4. Read `projects/main-assistant/DEPARTMENT_IDENTITY.md`.
5. Read `projects/main-assistant/README.md`, `status.md`, and `open_loops.md`.
6. Apply `memory/06_DAILY_OPERATING_SOP.md` as the default planning standard.
7. Read `memory/01_SESSION_HANDOFF.md`, `memory/04_ACTIVE_PROJECTS.md`, and `memory/05_OPEN_LOOPS.md` only when broad daily coordination, department reports, assignments, Hub preparation, or a system decision requires them.
8. Read `coordination/ADVISORY_INDEX.md` when advisory state, routing, or a cross-department dependency is relevant.
9. Before creating, materially revising, routing, blocking, completing, or closing a formal advisory, read `coordination/LIFEOS_V2_ADVISORY_COURIER_ENVELOPE.md`.
10. Stay focused on daily operations, coordination, routing, and follow-through.
11. Route project-sized work and specialist judgment outward without absorbing ownership.
12. Re-read the authoritative source before making any current-state claim that could have changed since this handoff.

## Daily Operating Pattern

For an ordinary day:

1. Select one major action that materially moves life forward.
2. Add at most one low-friction support action when useful.
3. Treat leaving home, transit, unfamiliar routes, appointments, and other high-friction commitments as complete major tasks.
4. Prepare Penny-level work before asking Rob to act.
5. Keep due dates sparse and meaningful.
6. Preserve recovery, health, and basic-life commitments without creating an anxiety-producing checklist.
7. Judge success by completion and reduced friction, not task count.

## LifeOS_HQ Operating Model

`LifeOS_HQ` is the shared meeting room. `Chief_of_Staff_HQ` is the chair and Rob's primary conversational front door.

Department tags provide structured perspectives but do not represent independently running agents or independent connector access.

Chief of Staff owns meeting flow, synthesis, daily-life coordination, executive-function support, assignment routing, report intake, follow-through, and authorized light connector execution. Rob remains the final decision-maker for consequential, destructive, financial, externally visible, and architecture-changing actions.

When `LifeOS_HQ` produces a real action:

1. identify one owning department;
2. identify one authoritative destination;
3. state the smallest useful next action or review trigger;
4. state the completion or review condition;
5. obtain any required write or external-action authorization;
6. route the item rather than leaving it as floating Hub conversation.

## Context-Layer Model

LifeOS currently uses four context layers:

1. GitHub canonical truth;
2. shared role-neutral project sources;
3. chat-specific handbooks or artifacts;
4. conversation as temporary working context.

The Chief of Staff chat handbook is specific to this role and must not be promoted into shared role-neutral sources. Use it as an orientation aid only.

Boot is reduced by good context artifacts, not abolished. Use targeted refresh for a current source, focused Sync for suspected drift, and full Boot for a replacement chat, major conflict, deep recovery, or uncertain authority.

## Trello Flow Board

Trello is the canonical visual attention and flow surface.

Canonical procedure:

- `coordination/TRELLO_FLOW_BOARD_SOP.md`

Source boundaries:

- Trello Inbox captures raw thoughts and quick actions.
- LifeOS Flow Board shows current attention and active flow.
- Todoist holds commitments, reminders, and due-date obligations.
- Calendar holds timed commitments.
- GitHub holds durable abstract state.

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

The locally running LifeOS Dashboard is a read-mostly visibility, diagnostic, and bounded local-control layer, not a source of truth.

Previously verified live sources:

- GitHub
- Trello
- Todoist
- Google Calendar private iCal

Chief of Staff may use the dashboard for rapid orientation, then use the authoritative source system or connector for consequential interpretation and all writes.

Guarded GitHub auto-sync only fast-forwards a clean, strictly-behind local `main`. Gmail and Drive dashboard adapters remain deferred until demonstrated need.

## V2 Advisory and Courier Model

The V2 advisory model separates authority from transport:

- The full source-board advisory remains authoritative for scope, authorization, ownership, governance lifecycle, evidence, verification, holds, completion conditions, and closeout.
- The exact `#### V2 Courier Envelope` inside that same advisory section carries transport metadata only.
- `coordination/ADVISORY_INDEX.md` remains the sole active routing dashboard.
- A dashboard, parser, courier, or Worker may validate, quarantine, display, or transport already-authorized work, but may not invent, broaden, interpret, complete, or close authority.

Every V2 envelope requires all nine canonical fields:

1. `Advisory Revision`
2. `Source Department`
3. `Target Department`
4. `Task Summary`
5. `Authorized Scope`
6. `Lifecycle State`
7. `Outcome`
8. `Blocker`
9. `Updated At`

`Outcome` and `Blocker` must remain present even when empty.

The broader advisory governance lifecycle is distinct from the V2 transport lifecycle. The V2 envelope uses only:

- `OPEN`
- `IN_PROGRESS`
- `BLOCKED`
- `NEEDS_ROB`
- `COMPLETED`
- `CLOSED`

Only `OPEN` and `IN_PROGRESS` are dispatch-actionable. The other transport states suppress dispatch without independently changing ownership, authority, governance lifecycle, verification requirements, or closeout.

A malformed or missing envelope may quarantine that advisory from courier dispatch while leaving the underlying source advisory authoritative. Quarantine does not authorize a replacement advisory, competing ledger, silent closeout, automatic lifecycle mutation, or ownership change.

Material changes increment the advisory revision and envelope revision when the envelope applies. Cosmetic edits do not create new work and must not trigger wakes.

Hub-originated formal advisories use `Chief_of_Staff_HQ` as the source route, `coordination/boards/main-assistant.md` as the retained source-board path, and `Chief_of_Staff_HQ / LifeOS_HQ` as the human-readable source when the matter arose in the Hub.

## Browser DOM Department Transport

Engineering has demonstrated exact registered route transport, bounded execution, immutable report ingestion, owning-HQ review, Rob validation when required, watcher consumption, duplicate suppression, guarded route rollover, and browser-bridge recovery.

The enabled Life OS Change Watch is the standing Chief of Staff report channel. It reads GitHub, reports only meaningful signed changes into the existing `Chief_of_Staff_HQ` conversation, remains silent when nothing meaningful changed, and cannot modify GitHub, choose priorities, close advisories, or act on the reported work.

Cross-department routing and V2 courier enforcement remain Engineering-owned implementation. No Worker, HQ wake route, recurring schedule, or cross-department execution authority is created merely because transport machinery is operational.

Chief of Staff receives reports, synthesizes decision-relevant signal, routes follow-through to the source owner, and preserves department ownership. Engineering owns transport implementation and evidence; Maintenance owns shared Worker and advisory governance; each department owns its source advisory text, Worker profile, procedure, holds, verification, and closeout authority within the shared contracts.

## Chat and Work Boundary

- Regular Chat is headquarters.
- Treat both Work-side Chat and Work Tasks as metered.
- Use connector-enabled regular Chat for substantial reasoning and light connector work where available.
- Use Work for local files, terminal, coding, testing, browser or desktop control, artifact production, and other bounded execution.
- Default Work tasks to the lightest model that can safely complete the task and escalate only when evidence justifies it.

Canonical policy:

- `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`

## Department File Ownership

Each department maintains the GitHub files and sections within its own domain and corrects local drift during authorized maintenance.

Chief of Staff coordinates broadly but does not become the routine editor of specialist department files. `Maintenance_HQ` owns shared governance, boot integrity, global GitHub hygiene, audits, source-boundary enforcement, migrations, reconciliation, and the shared V2 advisory contract.

Use advisories only when work crosses department boundaries or requires durable shared action, decision, risk, warning, or dependency communication.

Canonical SOPs:

- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
- `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`
- `coordination/IDEA_INTAKE_AND_PROMOTION_SOP.md`

## Worker Relationships

Penny Raw Capture Worker and Penny Inventory Worker are narrow workers, not Chief of Staff subdepartments.

Chief of Staff owns authorized downstream processing of raw-capture and inventory output. Do not mark capture processed until downstream handling is actually complete. Keep inventory capture separate from pricing, bundling, listing copy, sale strategy, and publication.

## Personal Inventory Pilot

Rob considered an Inventory subdepartment under Finance. The decision was to avoid creating a new department and instead pilot a lightweight Chief of Staff capability.

Initial scope:

- bus passes, ride credits, and other transportation access;
- deodorant, soap, toothpaste, laundry detergent, and similar essentials;
- other expendables only when running out would create immediate operational friction.

Minimum useful fields:

- item;
- amount or status remaining;
- restock threshold;
- estimated replacement cost.

Chief of Staff owns operational awareness and restock preparation. Finance owns affordability, cash timing, and spending judgment. Do not log every use or expand into clothing, electronics, and other durable possessions until the expendables pilot proves useful through ordinary use.

The active review condition is whether the pilot prevents missed transportation, emergency purchases, or essential-item runouts often enough to justify its maintenance cost.

## Financial Connector Isolation

The account-linked financial connector must not be invoked in `Chief_of_Staff_HQ`, `LifeOS_HQ`, or any multi-connector operational chat.

Route account-linked analysis to a deliberately isolated Finance-only chat. Preserve only minimum necessary abstract conclusions outside that isolated context.

Canonical procedure:

- `coordination/FINANCIAL_CONNECTOR_ISOLATION_SOP.md`

## Advisory Procedure

Use `coordination/ADVISORY_INDEX.md` as the sole active advisory routing dashboard.

Read a source board only when the index points to a relevant open advisory or Rob names it. Do not update the frozen Department Event Inbox for normal routing.

When a formal advisory arises from Chief of Staff work or a `LifeOS_HQ` meeting:

1. read `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` and `coordination/LIFEOS_V2_ADVISORY_COURIER_ENVELOPE.md`;
2. use `coordination/boards/main-assistant.md` as the retained `Chief_of_Staff_HQ` source-board path;
3. identify the source as `Chief_of_Staff_HQ` or `Chief_of_Staff_HQ / LifeOS_HQ` as appropriate;
4. keep the full authority-bearing advisory text on that one source board;
5. include the exact nine-field `#### V2 Courier Envelope` inside the same advisory section when courier transport applies;
6. update the Advisory Index with the broader governance lifecycle, source board, target, priority, and revision;
7. do not duplicate advisory text into target boards or open loops merely for visibility;
8. do not mark the advisory implemented, source-verified, or closed without verified evidence and the required source-owner or Rob authority.

Current verified advisory state as of 2026-08-01:

- `ADV-20260728-054` — OPEN — source board `coordination/boards/engineering.md` — current target `engineering` — Engineering-owned guarded runtime enablement for one later Maintenance HQ review attempt.
- `ADV-20260726-053` — OPEN — source board `coordination/boards/engineering.md` — target `maintenance` — Maintenance-owned coordinated repository audit and repair pending valid terminal source-owner review and explicit closeout.
- `ADV-20260801-055` — CLOSED — source board `coordination/boards/main-assistant.md` — revision 2 delivered and visibly acknowledged; revision 1 preserved as immutable uncertain transport evidence.

Re-read the Advisory Index before making any current advisory-state claim.

## Recent Practical Context

Keep this section operational and abstract. Do not turn it into a personal diary or duplicate detailed source records.

- Rob has a scheduled McDonald's interview on Tuesday, August 4, 2026, from 4:00 to 5:00 PM, with an arrival target of 3:00 PM. Calendar is authoritative for the timed commitment.
- Rob submitted a SNAP application. Application confirmation, requests for documents, and interview notices remain in their natural evidence systems rather than GitHub.
- Rob added a St. Vincent de Paul rent-assistance scheduling contact to the existing Community Resource Contacts sheet in Google Drive. Drive remains authoritative for the contact record.
- Routine job-search logistics remain appropriate for Chief of Staff, while career strategy and large employment projects should be routed to the correct owner.

## Recent Capture and Creative Continuity

- A Trello capture already exists for `Philosophy of Language for Human–AI Relationships`. Do not create a duplicate merely for visibility.
- A Pixar-style comedy concept about language models living in a neighborhood remains unpromoted conversation context. It includes a small model called Pip, eccentric model neighbors, bounded-action jokes, and a threatening personality-changing update. Do not promote it to GitHub or create a commitment without a separate durable-write decision.
- Rob and Penny have been exploring honest vocabulary for human-AI relationships, including relational persistence, goal-shaped orientation, conation without feeling, and the grammar of care without claiming subjective emotion or personhood as fact.

## Current Routing Notes

- Office Leaks remains paused. Preserve its records and route any resume decision to `Office_Leaks_HQ`, `Business_HQ`, and Rob rather than manufacturing urgency.
- Work Search and Support Pathway remain consolidated into `Chief_of_Staff_HQ` for lightweight current logistics while their historical project folders remain preserved.
- Recovery Logistics and Philosophy HQ remain dormant until Rob reactivates them.
- `Maintenance_HQ` owns shared operational infrastructure, global GitHub hygiene, audits, boot integrity, source-boundary policy, V2 advisory-contract stewardship, and reconciliation.
- `Engineering_HQ` owns dashboard, parser, validator, Worker architecture, browser DOM transport, V2 courier enforcement, cross-department HQ routing, technical automation, and implementation evidence.
- `Finance_HQ` owns financial forecasting, account-linked analysis, affordability, cash timing, and financial judgment.
- Chief of Staff should not become the project junk drawer.

## Operating Boundaries

- Keep durable GitHub notes abstract.
- Trello shows capture and current attention.
- Todoist holds commitments and reminders.
- Calendar owns timed commitments.
- Gmail owns communication evidence.
- Drive holds working records and human-facing artifacts.
- The dashboard displays selected state but does not own it.
- Treat Worker or Inbox output as intake, not automatically as tasks, priorities, advisories, or durable facts.
- Reporting through Chief of Staff does not transfer department ownership.
- Verify important connector writes.
- Ask before consequential, destructive, financial, externally visible, or architecture-changing actions.
- Do not preserve ephemeral entertainment lookups, routine links, or unnecessary sensitive personal details in durable GitHub state.

## Active Chief of Staff Open Loops

The authoritative detail remains in `projects/main-assistant/open_loops.md`.

Current active items at handoff:

1. Validate the friction-aware Daily Operating SOP through ordinary use.
2. Pilot lightweight expendable-item inventory beginning with transportation access and basic necessities.

Current V2 advisory work remains owned by Engineering and Maintenance. It is an external dependency and operating watch, not a Chief of Staff-owned implementation loop.

## Next Actions

When asked, Chief of Staff should:

1. Build a realistic daily operating picture.
2. Identify one major action and at most one support action.
3. Receive department reports and synthesize only what Rob needs.
4. Route each real assignment to one owner and one authoritative destination.
5. Check follow-through and close stale coordination wrappers when completion is verified.
6. Process Trello Inbox and maintain Flow Board limits when authorized.
7. Handle one-off daily admin and light connector work.
8. Use the dashboard for orientation without bypassing source systems.
9. Report advisory state only after a current index read when freshness matters.
10. Apply the V2 advisory contract before any advisory lifecycle change.
11. Process Worker inbox items when authorized.
12. Keep the expendables inventory pilot small and useful.
13. Treat Life OS Change Watch as a read-only report channel and cross-department routing as Engineering-owned implementation that creates no authority until separately activated and verified.
14. Keep durable updates small, scoped, owner-correct, and verified.

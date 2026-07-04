# Engineering Advisory Board

Updated: 2026-07-03
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

### ADV-20260703-009 — Scheduled HQ sync system experiment

Date: 2026-07-03
From: Chief Engineering Penny / Engineering HQ
To: Life Logistics HQ
Priority: High
Status: Open

#### Summary
Rob and Engineering identified an important Life OS architecture update: scheduled chats appear to remain in their originating chat, which means they can function as persistent daily sync workers rather than creating unruly new chats.

The first standalone Advisory Watcher experiment confirmed useful behavior but was deleted after the architecture changed. With the discovered task limit, Rob and Engineering decided scheduled tasks should be used for daily synchronization of the most important HQ chats rather than as many small watcher services.

#### Current Understanding
Rob found that Plus users appear to have access to five scheduled tasks. Because of that scarcity, scheduled tasks should be treated as premium Life OS infrastructure slots.

Engineering recommendation is to use the five slots for daily sync workers attached to the five core HQs:

1. Life Logistics HQ
2. Main Assistant
3. Chief Finance Penny
4. Chief Business HQ
5. Chief Engineering Penny

The previous standalone Advisory Watcher should not consume one of the five slots. Instead, advisory consumption should become part of each core HQ's daily sync procedure.

#### Engineering HQ Daily Sync Created
Rob asked Engineering to start with Chief Engineering Penny as the first experiment.

A scheduled task named `Engineering HQ Daily Sync` was created for daily execution at 6:00 AM America/Chicago.

The Engineering sync prompt instructs the scheduled run to:

- Boot Chief Engineering Penny.
- Read current Life OS GitHub boot and Engineering handoff documents.
- Read the global boot files, Engineering project handoff, Advisory Index, and Department Event Inbox.
- Consume any advisories addressed to Engineering.
- Update Engineering's working context.
- Report only if there are meaningful Engineering updates, new advisories requiring Rob's attention, documentation changes to recommend, or issues needing action.
- Avoid modifying GitHub, Google Drive, Todoist, or other systems during the sync.

#### Architectural Decision
Daily sync is preferred over hourly sync for core HQs.

Reasoning:

- Most advisories do not require immediate handoff.
- Rob can still manually route urgent advisories when needed.
- Daily cadence reduces noise and preserves scarce scheduled-task capacity.
- Morning sync reduces Rob's manual boot burden.
- Advisory consumption becomes part of each department's normal daily heartbeat.

#### Requested Life Logistics HQ Action
When Rob routes this advisory to Life Logistics HQ, please:

1. Read and ingest this advisory.
2. Update Life OS architecture notes, handoffs, open loops, or operating procedures as appropriate.
3. Record that the standalone Advisory Watcher was deleted and replaced conceptually by daily HQ sync workers.
4. Record that Engineering HQ Daily Sync is the first scheduled sync experiment.
5. Track the pending rollout decision for the remaining four likely daily sync workers:
   - Life Logistics HQ Sync
   - Main Assistant Sync
   - Chief Finance Sync
   - Chief Business Sync
6. Preserve the guardrail that daily sync workers should consume advisories and report, not perform major writes or decisions unless Rob explicitly authorizes that behavior.
7. Report back to Rob with what was updated and what remains open.

#### Engineering Recommendation
Treat the Engineering daily sync as the pilot. Observe whether it:

- Runs at the expected time.
- Stays in the Engineering HQ chat.
- Can access GitHub connectors during scheduled execution.
- Preserves Engineering identity and boot context.
- Consumes Engineering-targeted advisories correctly.
- Avoids unwanted writes or excessive chatter.

If the pilot succeeds, roll out daily sync tasks to the remaining core HQs one at a time.

## Acknowledged / Implemented Advisories

### ADV-20260703-007 — Scheduled advisory watcher and inbox procedure

Date: 2026-07-03
From: Chief Engineering Penny / Engineering HQ
To: Life Logistics HQ
Priority: High
Status: Acknowledged

#### Summary
Engineering and Rob identified the lowest-friction v0.1 solution for reducing Rob's manual advisory-routing burden: use one scheduled ChatGPT task as an Advisory Watcher.

#### Engineering Recommendation
Treat the scheduled-task watcher as a lightweight notification layer, not as the authoritative inbox.

Authority remains:

- `coordination/ADVISORY_INDEX.md` for advisory dashboard state.
- `coordination/DEPARTMENT_EVENT_INBOX.md` for department read/ingestion state.
- Department boards for advisory detail.

The scheduled task is only a watcher/reporter that reduces Rob's memory and typing load.

#### Acknowledgement / Outcome
Life Logistics HQ read and ingested this advisory.

Updates completed:

- Advisory Watcher v0.1 procedure added to `coordination/DEPARTMENT_EVENT_INBOX.md`.
- Advisory Watcher procedure added to `projects/life-os-infrastructure/SESSION_HANDOFF.md`.
- Advisory and department event rules added to `memory/03_OPERATIONAL_RULES.md`.
- Global session handoff updated.
- Advisory Index updated.
- Captain's Log updated.

Open follow-up:

- Create the scheduled ChatGPT task only if Rob explicitly asks for it.
- Optionally patch `memory/STARTUP_BOOT.md` later with a small update that references the Department Event Inbox and Advisory Watcher.

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

Startup Boot update was attempted but blocked by connector safety during that pass. The inbox is discoverable through the global session handoff and can be added to Startup Boot later with a smaller patch if needed.

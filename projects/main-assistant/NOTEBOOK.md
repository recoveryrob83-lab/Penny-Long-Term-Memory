# Chief of Staff HQ Notebook

Updated: 2026-07-18
Purpose: Preserve promoted Chief of Staff reasoning, decisions, experiments, validation, discoveries, and useful history that do not belong in handoff, status, open loops, advisories, standing procedures, or Drive artifacts.

Notebook entries are durable context, not a raw idea inbox or implicit task list. Raw ideas normally belong in Trello. A notebook entry does not automatically update the Advisory Index, Todoist, Calendar, open loops, status, or another department's records. Further promotion requires its own owner, destination, lifecycle, priority, next action or review trigger, completion condition, duplicate check, and authorization.

Historical entries may retain names and assumptions that were accurate when written. Current authority comes from the universal operating kernel, `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`, and the current Chief of Staff project files.

## Entries

### 2026-07-18 — Chief of Staff and LifeOS HQ separation adopted

- Status: Active decision / current architecture
- Priority: N/A
- Owner: Chief of Staff HQ
- Record class: Architecture decision and role clarification

Rob adopted the eight-room architecture in which LifeOS HQ is the shared meeting room and Chief of Staff HQ is a distinct department that chairs it.

Current operating conclusions:

- Chief of Staff HQ is Rob's primary point of contact, personal-assistant headquarters, daily-operations desk, routing desk, report-intake point, and follow-through coordinator.
- LifeOS HQ is the meeting table, not an independent department, executive, or backlog owner.
- Departments retain ownership of their specialized judgment, strategy, durable records, procedures, and backlogs.
- Reporting through Chief of Staff does not transfer ownership.
- When the Hub produces a real action, Chief of Staff identifies one owner, one authoritative destination, a next action or review trigger, and a completion condition before routing it.
- Hub-originated formal advisories use the retained path `coordination/boards/main-assistant.md` and identify the source as `Chief of Staff HQ / LifeOS HQ` when appropriate.
- The filesystem path `projects/main-assistant/` remains stable during the naming transition.
- Automation labels, shared governance files, specialist files, and external systems remain with their own owners and are not silently changed through Chief of Staff maintenance.

This decision supersedes earlier wording that described Main Assistant as the Hub itself while preserving the valid daily-operations and coordination functions developed under that name.

### 2026-07-15 — LifeOS Chat/Work architecture and seven discussion HQs

- Status: Historical / partially superseded by the eight-room authority model
- Priority: N/A
- Owner at time of record: Main Assistant / LifeOS coordination discussion
- Current interpretation: Chat/Work findings remain useful. Legacy room names and the fusion of Main Assistant with the Hub are superseded by the 2026-07-18 contract.

Rob and the LifeOS coordination hub tested the new ChatGPT desktop experience and established a practical operating architecture based on observed behavior rather than product assumptions.

#### Observed product behavior

- Normal ChatGPT chats and legacy Projects remain available across mobile, web, and classic desktop, though web Project presentation may be changing.
- The new desktop Work environment uses separate Work Projects and Tasks rather than normal chats.
- A disposable synchronization test confirmed that a Work Project and Task did not appear on mobile, web, or classic desktop.
- Existing normal ChatGPT Projects did not appear inside the new Work environment.
- Work therefore currently behaves as a separate workshop and execution surface rather than a synchronized replacement for normal ChatGPT.
- Connector access was unavailable in the desktop chat-only surface tested there, but remained usable through mobile and classic desktop Chat at the time.

#### Usage observations

Work usage resets weekly. Rob also had one free reset available until approximately August 21, pending exact verification.

Observed usage breakdown at the time:

- Building the Python desktop prompt database with Terra High registered about 3% Work usage.
- Extended conversation inside Work using Luna Light added about 7%.
- A Sol 5.6 conversation plus the small Work synchronization test added about 3%.
- Extended Sol 5.6 conversation in ordinary mobile Chat did not visibly increase Work usage.

The strongest working inference was that sustained conversation inside Work could consume substantial weekly Work allocation even on a light model, while ordinary Chat outside Work did not appear to consume that allocation. Reasoning level mattered, but environment and session length may have mattered more.

These are historical field observations, not permanent product facts. Re-test only after meaningful product change or demonstrated friction.

#### Chosen operating architecture

Core mental model:

- Chat = think, discuss, coordinate, and perform light connector-backed work.
- Work = execute tasks that genuinely require local tools or a heavier computer environment.
- GitHub = durable technical memory and source of truth.
- Google Drive = documents and working files.
- Desktop computer = execution surface.

Regular ChatGPT remained the primary LifeOS conversational environment because it preserved mobile access, ordinary conversational continuity, planning, recovery work, philosophy, strategy, and light connector operations.

The LifeOS Work Project remained a bounded execution workshop for:

- coding and testing;
- local-file inspection or transformation;
- large artifact production;
- browser automation;
- desktop application control;
- heavy implementation tasks that could not be completed safely through Chat connectors.

Operating rule:

> Think and decide in Chat. Enter Work with a bounded objective. Execute, verify, and leave.

Long open-ended conversation inside Work was specifically discouraged because it spent the weekly execution budget on activity Chat could perform without moving the Work meter.

#### Model policy at the time

- GPT-5.5 Instant was the default for routine conversation, coordination, capture, and planning.
- GPT-5.6 Terra Medium was the normal escalation point for heavier synthesis or planning.
- Terra High was expected to be rare and justified by task complexity.
- Sol was considered unnecessary for ordinary LifeOS planning and execution.
- The smallest capable model should be used first; capability escalates only when the task requires it.

Model names, availability, and metering are product-dependent observations rather than permanent architecture rules.

#### Department HQ decision

Rob planned seven persistent department HQ chats as planning and discussion spaces in regular ChatGPT rather than Work Projects.

The purpose was to preserve specialized departmental context while keeping every department part of one coherent Penny organization. The HQs were conference rooms for one assistant wearing different operational hats, not autonomous agents running loose.

Expected core departments at the time included:

- Main Assistant / LifeOS Coordination Hub
- Life Logistics
- Engineering
- Finance
- Business
- Wellness
- one additional department to be confirmed during Engineering review

Current translation under the adopted architecture:

- LifeOS HQ is the shared meeting room.
- Chief of Staff HQ replaces the official Main Assistant role name.
- Life OS Maintenance HQ replaces the official Logistics role name.
- Office Leaks HQ is the seventh department HQ.

The coordination discussion demonstrated value by giving Rob multiple department perspectives in one conversation without requiring him to switch chats while planning from mobile.

#### Connector and execution policy

While connector access remained available through mobile or classic desktop Chat:

- department HQs could perform light connector work such as GitHub updates, itinerary checks, task review, and ordinary record coordination;
- the chair coordinated cross-department connector actions in the shared meeting room unless Rob explicitly directed otherwise;
- no department could claim an external action occurred unless a connector or Work result confirmed it.

If OpenAI later moved connector use fully into Work, the architecture was expected to survive. Planning and departmental discussion would remain in Chat, while connector-backed execution moved across the boundary through concise task briefs.

#### Meeting decision and follow-up

The architecture discussion was complete enough to proceed.

A formal advisory, ADV-20260715-036, was routed to Engineering to design prompts for all seven department HQs. Engineering performed that prompt work in Engineering HQ rather than expanding the coordination discussion.

The immediate priority remained practical use of the system, not further platform archaeology or infrastructure for its own sake. Work should support real engineering, business delivery, and automation without displacing immediate income and real-world action.

### 2026-07-15 — Friction-aware daily operating pattern

- Status: Active validated reasoning / implemented in `memory/06_DAILY_OPERATING_SOP.md`
- Priority: Normal review through ordinary use
- Owner: Chief of Staff HQ / Daily Operations
- Review condition: Revise only from observed daily-use evidence.

Rob identified a daily operating pattern that plays to his strengths while respecting executive dysfunction and the high cognitive cost of leaving the house.

Core principle:

- Reduce friction and cognitive load so each day has one or two solid actions, not an overloaded itinerary.
- Treat leaving the house by transit as a full major task. Route planning, transfers, timing buffers, walking, weather, battery, and the return trip are part of the task.
- Use due dates for real anchors and chosen priorities, not every possible task. Backlog items, waiting-on-someone items, and Penny-handled work generally remain undated.
- Select one major action that moves life forward. Add one low-friction support action only if capacity remains.
- Classify work by friction: high for appointments, interviews, unfamiliar travel, and multi-step applications; medium for calls, forms, and coordination; low for planning, recovery reading, journaling, systemizing, learning, and idea creation; Penny-level for research, drafting, Todoist shaping, checklists, summaries, and call preparation.
- Pair a high-friction outside action with a low-friction home action rather than stacking multiple high-friction demands.
- Use transit and waiting time as recovery or productivity-lite time: NA reading or audio, a short journal prompt, music or a podcast, grounding, reviewing one action, or one easy note to Penny.

Suggested daily selection template:

1. Main action: one appointment, interview, errand, or other action that materially moves life forward.
2. Friction note: what makes it high-load and what can be prepared in advance.
3. Support action: one small low-friction action, only if useful.
4. Penny support: identify anything Penny can research, draft, organize, schedule, or prepare.
5. Completion standard: progress counts; the day is not a failure if the main action required the available capacity.

This pattern is intended for repeated use and later refinement. It should reduce the feeling of an ever-growing itinerary while preserving meaningful commitments and the activities that naturally motivate Rob: systemizing, LifeOS design, recovery work, philosophy, learning, programming, software design, art, planning, and idea creation.

### 2026-07-09 — GitHub notebook as frictionless idea inbox

- Status: Historical / superseded
- Priority: N/A
- Current replacement: Trello captures raw ideas; GitHub notebooks preserve promoted reasoning and useful durable history under `coordination/IDEA_INTAKE_AND_PROMOTION_SOP.md` and `coordination/DEPARTMENT_NOTEBOOKS.md`.

Rob wanted a simple idea-capture system where he could say something like `@GitHub notebook:` during the day and have Penny capture the idea in the appropriate GitHub department notebook without immediately turning it into a plan or task.

The proposed operating pattern was:

- Capture ideas quickly in the relevant GitHub notebook.
- Treat notebook entries as raw material, not commitments.
- Review captured ideas later during the appropriate department session or nightly review.
- Promote only selected ideas into plans, Todoist tasks, Drive working docs, Open Loops, advisories, or project work.
- Preserve the distinction between capture and processing so Rob could empty his head without forcing immediate decisions.

The valid underlying need was low-friction capture. The current architecture satisfies that need through Trello and narrow workers without turning department notebooks into raw inboxes.

### 2026-07-09 — Dedicated rapid capture worker GPT

- Status: Completed / implemented historical design record
- Priority: N/A
- Durable implementation: Worker architecture and the Penny Raw Capture Worker package were implemented through ADV-20260709-030.

Rob identified that midday capture could become a dedicated GPT or worker role rather than requiring a full Main Assistant interaction every time.

Concept:

- Create a lightweight worker whose only primary job is rapid idea and request capture.
- Connect it to the approved capture resource.
- Give it a worker document, routing prompt, connector instructions, and clear boundaries during setup.
- Let Rob type or speak quickly, especially when Marqueto is giving several requests or ideas in rapid succession.
- Have the worker identify likely routing metadata and preserve the raw capture.
- Do not analyze deeply, plan, create tasks, or promote the note unless Rob explicitly asks.
- Leave cleanup, deduplication, prioritization, task promotion, and project routing for authorized downstream processing.

Possible standard capture fields considered at the time:

- Timestamp or date.
- Source or context, such as Marqueto, personal thought, Office Leaks, job search, housing, caregiver, finance, or engineering.
- Raw capture in Rob's own language.
- Suggested routing destination.
- Capture type, such as task candidate, idea, preference, fact, question, reminder, or project input.
- Urgency signal only when clearly stated.
- Status: raw or unprocessed.

Design principle:

> The worker should optimize for speed and preservation, not judgment.

The successful architecture separated worker capture from Chief of Staff downstream processing and from durable promotion. Worker output remains intake until authorized processing is actually complete.

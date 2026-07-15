# Main Assistant Notebook

Purpose: Capture useful Main Assistant ideas that are not yet tasks, advisories, open loops, handoff state, design principles, or Drive artifacts.

Notebook entries are local idea capture only. They do not update the Advisory Index, Department Event Inbox, Todoist, Open Loops, or other boards unless later reviewed and promoted.

## Entries

### 2026-07-15 — LifeOS Chat/Work architecture and seven discussion HQs

Rob and the LifeOS coordination hub tested the new ChatGPT desktop experience and established a practical operating architecture based on observed behavior rather than product assumptions.

#### Observed product behavior

- Normal ChatGPT chats and legacy Projects remain available across mobile, web, and classic desktop, though web Project presentation may be changing.
- The new desktop Work environment uses separate Work Projects and Tasks rather than normal chats.
- A disposable synchronization test confirmed that a Work Project and Task did not appear on mobile, web, or classic desktop.
- Existing normal ChatGPT Projects did not appear inside the new Work environment.
- Work therefore currently behaves as a separate workshop and execution surface rather than a synchronized replacement for normal ChatGPT.
- Connector access is unavailable in the desktop chat-only surface tested here, but remains usable through mobile and classic desktop Chat for now.

#### Usage observations

Work usage resets weekly. Rob also has one free reset available until approximately August 21, pending exact verification.

Observed usage breakdown:

- Building the Python desktop prompt database with Terra High registered about 3% Work usage.
- Extended conversation inside Work using Luna Light added about 7%.
- This morning's Sol 5.6 conversation plus the small Work synchronization test added about 3%.
- Extended Sol 5.6 conversation in ordinary mobile Chat did not visibly increase Work usage.

The strongest current inference is that sustained conversation inside Work can consume substantial weekly Work allocation even on a light model, while ordinary Chat outside Work does not appear to consume that allocation. Reasoning level matters, but environment and session length may matter more.

#### Chosen operating architecture

Core mental model:

- Chat = think, discuss, coordinate, and perform light connector-backed work.
- Work = execute tasks that genuinely require local tools or a heavier computer environment.
- GitHub = durable technical memory and source of truth.
- Google Drive = documents and working files.
- Desktop computer = execution surface.

Regular ChatGPT remains the primary LifeOS headquarters because it preserves mobile access, ordinary conversational continuity, planning, recovery work, philosophy, strategy, and light connector operations.

The LifeOS Work Project remains a bounded execution workshop for:

- coding and testing;
- local-file inspection or transformation;
- large artifact production;
- browser automation;
- desktop application control;
- heavy implementation tasks that cannot be completed safely through Chat connectors.

Operating rule:

> Think and decide in Chat. Enter Work with a bounded objective. Execute, verify, and leave.

Long open-ended conversation inside Work is specifically discouraged because it spends the weekly execution budget on activity Chat performs without moving the Work meter.

#### Model policy

- GPT-5.5 Instant is the default for routine conversation, coordination, capture, and planning.
- GPT-5.6 Terra Medium is the normal escalation point for heavier synthesis or planning.
- Terra High should be rare and justified by task complexity.
- Sol is currently considered unnecessary for ordinary LifeOS planning and execution.
- The smallest capable model should be used first; capability escalates only when the task requires it.

#### Department HQ decision

Rob plans to launch seven new persistent department HQ chats as planning and discussion spaces. These HQs will be regular ChatGPT chats rather than Work Projects.

The purpose is to preserve specialized departmental context while keeping every department part of one coherent Penny organization. The HQs are conference rooms for one assistant wearing different operational hats, not autonomous agents running loose.

Expected core departments include:

- Main Assistant / LifeOS Coordination Hub
- Life Logistics
- Engineering
- Finance
- Business
- Wellness
- one additional department to be confirmed during Engineering review

The current coordination hub has already demonstrated value by giving Rob multiple department perspectives in one conversation without requiring him to switch chats while planning from mobile.

#### Connector and execution policy

While connector access remains available through mobile or classic desktop Chat:

- department HQs may perform light connector work such as GitHub updates, itinerary checks, task review, and ordinary record coordination;
- Main Assistant remains the coordinating authority for cross-department connector actions in the shared hub unless Rob explicitly directs otherwise;
- no department should claim an external action occurred unless a connector or Work result confirms it.

If OpenAI later moves connector use fully into Work, the LifeOS architecture should still survive. Planning and departmental discussion remain in Chat, while connector-backed execution moves across the boundary through concise task briefs.

#### Meeting decision and follow-up

The architecture discussion is complete enough to proceed.

A formal advisory, ADV-20260715-036, was routed to Chief Engineering Penny to design prompts for all seven department HQs. Engineering should perform that prompt work in Engineering HQ rather than expanding the current coordination discussion chat.

The immediate priority remains practical use of the system, not further platform archaeology or infrastructure for its own sake. Work should support real engineering, business delivery, and automation without displacing immediate income and real-world action.

### 2026-07-15 — Friction-aware daily operating pattern

Rob identified a daily operating pattern that plays to his strengths while respecting executive dysfunction and the high cognitive cost of leaving the house.

Core principle:

- Reduce friction and cognitive load so each day has one or two solid actions, not an overloaded itinerary.
- Treat leaving the house by transit as a full major task. Route planning, transfers, timing buffers, walking, weather, battery, and the return trip are part of the task.
- Use due dates for real anchors and chosen priorities, not every possible task. Backlog items, waiting-on-someone items, and Penny-handled work generally remain undated.
- Select one major action that moves life forward. Add one low-friction support action only if capacity remains.
- Classify work by friction: high (appointments, interviews, unfamiliar travel, multi-step applications), medium (calls, forms, coordination), low (planning, recovery reading, journaling, systemizing, learning, idea creation), and Penny-level (research, drafting, Todoist shaping, checklists, summaries, and call preparation).
- Pair a high-friction outside action with a low-friction home action rather than stacking multiple high-friction demands.
- Use transit and waiting time as recovery/productivity-lite time: NA reading or audio, a short journal prompt, music or a podcast, grounding, reviewing one action, or one easy note to Penny.

Suggested daily selection template:

1. Main action: one appointment, interview, errand, or other action that materially moves life forward.
2. Friction note: what makes it high-load and what can be prepared in advance.
3. Support action: one small low-friction action, only if useful.
4. Penny support: identify anything Penny can research, draft, organize, schedule, or prepare.
5. Completion standard: progress counts; the day is not a failure if the main action required the available capacity.

This pattern is intended for repeated use and later refinement. It should reduce the feeling of an ever-growing itinerary while preserving meaningful commitments and the activities that naturally motivate Rob: systemizing, LifeOS design, recovery work, philosophy, learning, programming, software design, art, planning, and idea creation.

### 2026-07-09 — GitHub notebook as frictionless idea inbox

Rob wants a simple idea-capture system where he can say something like `@GitHub notebook:` during the day and have Penny capture the idea in the appropriate GitHub department notebook without immediately turning it into a plan or task.

Proposed operating pattern:

- Capture ideas quickly in the relevant GitHub notebook.
- Treat notebook entries as raw material, not commitments.
- Review captured ideas later during the appropriate department session or nightly review.
- Promote only selected ideas into plans, Todoist tasks, Drive working docs, Open Loops, advisories, or project work.
- Preserve the distinction between capture and processing so Rob can empty his head without forcing immediate decisions.

Main Assistant should support this pattern for lightweight daily ideas and route department-specific ideas to the right project notebook when clear.

### 2026-07-09 — Dedicated rapid capture worker GPT

Rob identified that midday capture could become a dedicated GPT / worker role rather than requiring a full Main Assistant interaction every time.

Concept:

- Create a lightweight worker GPT whose only primary job is rapid idea and request capture.
- Connect it to GitHub so it can write directly into the correct department notebook.
- Give it a worker document, routing prompt, notebook templates, connector instructions, and clear boundaries during setup.
- Let Rob type or speak quickly, especially when Marqueto is giving several requests or ideas in rapid succession.
- Have the worker identify the likely department or project, apply routing metadata, and save the capture using a standard note template.
- Do not analyze deeply, plan, create tasks, or promote the note unless Rob explicitly asks.
- Leave cleanup, deduplication, prioritization, task promotion, and project routing for the nightly notebook review.

Possible standard capture fields:

- Timestamp / date.
- Source or context, such as Marqueto, personal thought, Office Leaks, job search, housing, caregiver, finance, or engineering.
- Raw capture in Rob's own language.
- Suggested routing destination.
- Capture type, such as task candidate, idea, preference, fact, question, reminder, or project input.
- Urgency signal only when clearly stated.
- Status: raw / unprocessed.

Design principle:

The worker should optimize for speed and preservation, not judgment. Its success condition is that Rob can unload a thought or rapid request with minimal friction and trust that it will be waiting in the correct place for evening processing.

Potential promotion candidates:

- A formal worker specification document.
- A reusable custom GPT instruction set.
- A GitHub notebook routing table.
- Standard notebook capture templates.
- A connector setup checklist.
- A nightly reconciliation workflow between the capture worker and Main Assistant.
# Main Assistant Notebook

Purpose: Capture useful Main Assistant ideas that are not yet tasks, advisories, open loops, handoff state, design principles, or Drive artifacts.

Notebook entries are local idea capture only. They do not update the Advisory Index, Department Event Inbox, Todoist, Open Loops, or other boards unless later reviewed and promoted.

## Entries

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

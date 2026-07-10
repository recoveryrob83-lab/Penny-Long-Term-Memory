# Main Assistant Notebook

Purpose: Capture useful Main Assistant ideas that are not yet tasks, advisories, open loops, handoff state, design principles, or Drive artifacts.

Notebook entries are local idea capture only. They do not update the Advisory Index, Department Event Inbox, Todoist, Open Loops, or other boards unless later reviewed and promoted.

## Entries

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

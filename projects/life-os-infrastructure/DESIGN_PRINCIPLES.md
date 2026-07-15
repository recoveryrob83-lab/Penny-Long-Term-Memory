# Life OS Design Principles

Updated: 2026-07-15
Project: Life OS Infrastructure
Purpose: Durable design principles for Rob's Life OS architecture.

## Operating Rule

This file stores stable architecture principles, not implementation details.

GitHub is the durable memory map. Drive remains the detailed working records cabinet.

Keep principles short, abstract, and decision-oriented.

## Principle 001 — Measured-Need Platform Adoption

No new platform enters the Life OS architecture until it solves a measured problem that cannot be cleanly solved by an existing component.

Before adopting a new platform, define:

- the measured pain it solves,
- the existing component that cannot solve it cleanly,
- the platform's narrow ownership boundary,
- what source-of-truth role it will and will not own,
- the exit or rollback path if it creates more complexity than value.

## Principle 002 — Separate Headquarters From Execution

The regular ChatGPT hub is the canonical conversational headquarters. The Work environment is a bounded execution surface, not a second headquarters.

Plan, coordinate, reason, and prepare instructions in Chat. Enter Work only when a task requires local files, terminal access, code execution, browser control, desktop applications, artifact production, or comparable execution capabilities.

Default Work tasks to the least powerful model likely to succeed. Preserve higher-cost models and weekly Work usage for tasks that materially benefit from them.

Detailed operating policy:

- `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`

## Current Platform Boundaries

Current Life OS ownership boundaries:

- GitHub owns durable memory, procedures, advisories, department identities, organizational structure, and abstract operating state.
- Google Drive owns working documents and detailed artifacts.
- Todoist owns Rob-facing personal action items.
- Calendar owns time, appointments, and scheduled commitments.
- Gmail owns communication evidence.
- Department Event Inbox owns department synchronization, read, and ingestion state.
- Advisory Index owns cross-department advisory dashboard state.
- Regular Chat owns conversational continuity, planning, department coordination, and light connector work where available.
- Work owns bounded local-computer execution and heavy implementation tasks.

## Deferred Platform Decision — Kanban / Project Management Tools

Asana, ClickUp, Trello, or another Kanban-style project-management platform is deferred, not rejected.

Current decision: do not introduce a Kanban/project-management platform now.

Reason: Life OS currently has clean source-of-truth boundaries. The current bottleneck is synchronization and coordination, not project-management pipeline state.

## Future Kanban Ownership Boundary

If a Kanban or project-management platform is introduced later, it should own pipeline state only.

It should not own:

- durable memory,
- working documents,
- personal task reminders,
- calendar commitments,
- department synchronization,
- advisory routing,
- source-of-truth decisions.

Likely future department-level uses:

- Chief Business HQ pipeline state, such as Ideas, Research, Validation, In Progress, Waiting, Complete.
- Chief Engineering Penny pipeline state, such as Backlog, Ready, In Development, Testing, Review, Released.

Do not add a Kanban/project-management platform as a global Life OS layer unless real scaling pain proves the need.

## Re-Evaluation Triggers

Revisit a Kanban/project-management platform only when there is measurable friction, such as:

- more than 20 active work items in a department pipeline,
- frequent confusion about the state of product/business/engineering work,
- multiple concurrent implementation efforts,
- repeated loss of pipeline visibility,
- Todoist, GitHub, and Drive no longer answer: what state is this work in?

Review the Chat and Work boundary when synchronization, connector availability, mobile access, model tiers, or Work metering materially changes.

## Decision Bias

Prefer fewer platforms with clearer ownership over more platforms with overlapping responsibilities.

Add systems only when they remove more coordination burden than they create.
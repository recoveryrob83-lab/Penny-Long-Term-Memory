# LifeOS HQ Operating Contract

Updated: 2026-07-18
Owner: Life OS Maintenance HQ
Status: Active
Record Type: Operating Contract
Authority: Authoritative
Purpose: Define the LifeOS HQ meeting room, Chief of Staff authority, department reporting, action routing, and the maintenance and engineering boundaries.

## Core Model

LifeOS HQ is the shared meeting room for Rob and the Life OS departments.

It is not a department, an independent executive, or a competing source of durable state.

Short form:

> The Hub is the table. Chief of Staff chairs. Departments own their work. Rob decides.

## Official Organization

### Rob

Rob is the final authority for Life OS.

He approves consequential decisions, exceptions, durable promotions, major reprioritization, and changes to the operating architecture.

### LifeOS HQ

LifeOS HQ is the central meeting room.

It exists for:

- cross-department discussion;
- structured department perspectives;
- synthesis and decision preparation;
- dependency discovery;
- routing;
- shared review;
- system-level coordination when genuinely required.

LifeOS HQ does not:

- own a department backlog;
- maintain an independent project subtree;
- replace Chief of Staff HQ;
- make itself the owner of work merely because the work was discussed there;
- preserve detailed duplicate truth for visibility.

### Chief of Staff HQ

Chief of Staff HQ is Rob's primary point of contact and personal-assistant headquarters.

It owns:

- daily operations;
- executive-function support;
- practical planning and coordination;
- chairing LifeOS HQ;
- cross-department synthesis;
- task and assignment routing;
- receiving department reports;
- follow-through and closure checks;
- authorized light connector execution;
- preparing clear decisions for Rob.

Chief of Staff HQ may coordinate broadly without becoming the authoritative owner of each department's strategy, technical work, financial records, wellness judgment, or backlog.

Inside LifeOS HQ, `[MAIN]` means Chief of Staff speaking as chair.

### Life OS Maintenance HQ

Life OS Maintenance HQ is the official name of the former Logistics HQ role.

It owns:

- global GitHub maintenance;
- universal boot integrity;
- global handoffs and operating rules;
- system open-loop hygiene;
- shared coordination procedures;
- advisory-index and board hygiene;
- repository paths, migrations, archives, and global structure;
- source-of-truth enforcement;
- audits and drift detection;
- reconciliation between the Drive Chief's Manual, Project Instructions, and GitHub implementation.

Maintenance identifies drift and routes precise corrections to the owning department. It does not silently take over department maintenance without explicit coordinated-repair authority.

### Engineering HQ

Engineering HQ owns technical architecture, software, dashboard implementation, automation, validators, parsers, testing, and technical enforcement mechanisms.

Engineering may lead a system-design or implementation workstream when the work is technical. Building the machinery does not make Engineering the permanent owner of governance or every source record.

### Specialist Departments

Business HQ, Office Leaks HQ, Finance HQ, Wellness HQ, and other active specialist departments own judgment, strategy, and durable state within their assigned domains.

Departments may report recommendations, status, risks, and completed work to Chief of Staff HQ. Chief of Staff routes assignments to them and integrates their reports for Rob.

A department speaking inside LifeOS HQ remains bound by its own authority and source-of-truth rules.

## Decision Rights

- Rob makes the final decision.
- Chief of Staff controls meeting flow, synthesis, routing, and follow-through.
- The owning department provides domain judgment and maintains the authoritative department record.
- Life OS Maintenance enforces global operating rules and source boundaries.
- Engineering determines technical feasibility and safe implementation within approved scope.
- LifeOS HQ itself has no independent authority beyond the procedures carried by these roles.

A Hub discussion does not become durable state merely because participants agree enthusiastically. The normal durable-write, ownership, and authorization rules still apply.

## Action Transfer From The Hub

When LifeOS HQ produces a real action, decision, dependency, warning, or request:

1. identify one owning department;
2. identify the authoritative destination;
3. state the smallest useful next action or review trigger;
4. state the completion or review condition;
5. determine whether a local update, handoff, advisory, Todoist task, Calendar event, Drive artifact, or system coordination record is appropriate;
6. obtain any required write or external-action authorization;
7. route the item rather than leaving it as floating Hub conversation.

Use a compact system coordination wrapper only when multiple departments must act, a shared rule is changing, or no single department can own completion.

## Hub Advisory Source

LifeOS HQ does not maintain a separate advisory board.

When the Hub needs to issue a formal advisory, Chief of Staff HQ is the source department and uses:

- `coordination/boards/main-assistant.md` as the retained source-board path;
- `coordination/ADVISORY_INDEX.md` as the sole active routing dashboard.

The advisory should identify its source as `Chief of Staff HQ / LifeOS HQ` when the decision or request arose from a Hub meeting.

Do not duplicate the advisory text into target boards or create matching open loops merely for visibility.

## Durable-State Boundary

LifeOS HQ may read broad state, but it does not own an independent backlog.

Durable outcomes belong in:

- the owning department's files;
- a shared Maintenance-owned rule or contract;
- `memory/05_OPEN_LOOPS.md` only when the system-promotion threshold is met;
- the Chief of Staff source board when a Hub advisory is required;
- the natural external source system for tasks, time, communications, working records, or detailed evidence.

Hub summaries are coordination views, not competing authoritative ledgers.

## Legacy Name Translation

Until department-local files, prompts, and automation labels are deliberately updated:

- `Main Assistant`, `Main Assistant HQ`, and `Main Assistant Penny` refer to the role now officially named `Chief of Staff HQ`;
- `Logistics HQ`, `Life Logistics HQ`, and global-role uses of `Logistics` refer to the role now officially named `Life OS Maintenance HQ`;
- `LifeOS HQ` refers only to the central meeting room.

Existing filesystem paths remain unchanged during this naming transition:

- Chief of Staff HQ: `projects/main-assistant/`
- Life OS Maintenance HQ: `projects/life-logistics-hq/`

Historical notes and prior commits may retain names that were accurate when written.

## Operating Principle

> One point of contact. Clear specialist ownership. No floating assignments. No duplicate truth.
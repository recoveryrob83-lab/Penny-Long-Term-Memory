# Codex Penny Mission 02: Dashboard

- Owning Department: Engineering_HQ
- Execution Surface: Codex Penny / local repository
- Target: `apps/lifeos_dashboardv2`
- Prerequisite: Mission 01 accepted by Engineering and Rob
- Lifecycle State: Waiting for explicit resume authorization
- Priority: High
- Verification Mode: IMMEDIATE_HQ
- Stop Condition: Stop after the Slice Two acceptance gate. Do not begin browser-extension implementation.

## Objective

Build the human-facing LifeOS V2 dashboard against the accepted Slice One API and contracts. Preserve the approved visual language while implementing the three V2 sections: Overview, Department Inspector, and Automation.

## Required Reads

Follow the canonical boot sequence beginning with `memory/STARTUP_BOOT.md`.

Then read:

- `projects/engineering/DEPARTMENT_IDENTITY.md`
- `projects/engineering/README.md`
- `projects/engineering/status.md`
- `projects/engineering/open_loops.md`
- `projects/engineering/notebook/NOTE-20260729-015-lifeos-v2-final-design.md`
- `projects/engineering/notebook/NOTE-20260729-016-lifeos-v2-integration-packet.md`
- `projects/engineering/notebook/NOTE-20260729-017-dashboard-visual-behavior.md`
- `projects/engineering/codex_missions/README.md`
- `projects/engineering/codex_missions/MISSION-01-server-and-contracts.md`
- the accepted Mission 01 completion report and current code

Inspect the approved Drive screenshots when available. Use V1 code only for proven visual and interaction behavior, not product semantics.

## Authentication and Repository Preflight

Run the bounded Git/GitHub preflight defined in the mission README. Remote failure does not block local work. Do not spend the mission repeatedly repairing credentials.

Before editing, run the full accepted Slice One test suite and establish a clean baseline. If Slice One is broken, stop and report rather than hiding server defects inside dashboard work.

## Scope and Build Order

Implement in this order:

1. shared dashboard shell and client API layer;
2. Automation;
3. Department Inspector;
4. Overview connector adapters and panels;
5. responsive, accessibility, and non-happy-path verification.

Keep Overview connectors separate from automation transport modules.

Recommended internal shape:

```text
dashboard/
  shared/
  automation/
  department_inspector/
  overview/
connectors/
  github_connector.*
  todoist_connector.*
  calendar_connector.*
  trello_connector.*
```

Exact framework and module names may follow the accepted repository stack. Do not introduce a second frontend stack without evidence.

## Shared Shell

Implement:

- dark command-window visual language;
- centered maximum-width layout;
- responsive header;
- last completed refresh time;
- `Refresh view` control with duplicate-request protection;
- independent source-health cards;
- exactly three top-level tabs: Overview, Department Inspector, Automation;
- remembered active tab;
- semantic tab roles and arrow-key navigation;
- visible focus states;
- loading, empty, stale, partial, and error states.

One source failure must not collapse healthy panels.

## Automation Section

Automation consumes the accepted Slice One server APIs. It does not read or mutate source-system records directly.

Show:

- global Running or Paused state;
- server/API health;
- browser-extension connection state when available;
- registered route count;
- active and pending commands;
- failed or uncertain commands requiring attention;
- route label, target, exact assigned ChatGPT URL, registration time, verification time, and health;
- command ID, advisory ID and revision, source, target, concise task summary, delivery state, attempts, timestamps, and concise error;
- recent courier run history.

Approved controls:

- pause or resume;
- retry only a clearly pre-send failure;
- cancel pending delivery;
- open advisory;
- open target chat;
- change or re-register route;
- refresh Automation.

Do not provide normal controls to mark work complete, mark an advisory complete, reset advisory state, replay uncertain sends, or infer success from assistant text.

Because Mission 03 is not built yet, extension-dependent states may use a clear unavailable or not-connected state and test fixtures. Do not build extension code in this mission.

## Department Inspector

Build a read-only configured-path GitHub inspection surface.

Summary:

- normalized records;
- findings;
- records with warnings;
- visible records and findings.

Filters:

- department;
- category;
- record type;
- lifecycle state;
- priority;
- date range;
- cross-department state;
- authority;
- sort order;
- search;
- warnings only;
- reset.

Filters combine with AND logic and update without full-page reload.

Group results into Work, Knowledge, Operations, and Findings.

Record cards show department, subtype, title, state, priority, summary, record type, authority, parse confidence, best date, warning count, source path, canonical source link, and an in-place raw-source disclosure.

State and priority remain separate. Findings are prompts for review, not verdicts and not write actions.

Perform only the bounded repository manifest discovery described in the integration packet. Save configured paths and do not crawl the repository on every refresh.

## Overview

Overview is read-only and answers:

- What needs attention now?
- What is scheduled?
- What is currently moving?
- What durable work changed recently?

### Today

Use Google Calendar and Todoist.

- show current local date;
- emphasize the next relevant primary-calendar event;
- list active configured Todoist commitments;
- preserve all-day behavior;
- show overdue and due-today badges;
- open canonical source URLs;
- do not complete or reprioritize tasks.

### Flow

Use the configured LifeOS Flow Board.

- show Now, Next, and Waiting using configured list IDs;
- open canonical Trello records;
- do not move cards;
- do not blend the Space RPG board into default LifeOS attention.

### Attention

Implement only source signals supported by the approved scope and existing connectors. Signals are compact summaries, not full inboxes. Do not expand this mission into Gmail client work unless an accepted current design explicitly requires the existing read-only summary.

### Drive Shortcuts

Use a curated configuration, not unrestricted Drive crawling. Open canonical Drive items. Do not duplicate document content.

### GitHub and Recent LifeOS Activity

Show configured durable pulse, open advisories, priority open loops, and recent meaningful notebook or durable-state records. Provide canonical source links and compact summaries.

## Connector Requirements

Use the approved integration packet's live nonsecret manifests and required fields.

- GitHub: configured paths only.
- Todoist: active tasks from configured projects.
- Calendar: primary calendar by default; holiday calendar optional.
- Trello: LifeOS Flow Board enabled by default.

Use sanitized fixtures for normal tests. Guard live tests behind explicit environment flags.

Store last successful refresh per connector. Preserve safe last-known data with a visible stale label. Never show stale data as current.

## Responsive Behavior

Implement the approved breakpoints and intent:

- wide: maximum-width multi-column layout;
- medium: reduced columns and content wrapping;
- small: full-width stacked cards and controls;
- no horizontal page scrolling in normal viewports;
- content-driven card heights;
- bounded scrolling only for raw or diagnostic content;
- table-to-card conversion where needed on narrow screens.

Test representative wide, medium, and narrow widths. Screenshots should remain recognizably aligned with the approved visual references.

## Required Tests

At minimum test:

- shared shell and exactly three tabs;
- remembered active tab;
- keyboard tab navigation;
- refresh duplicate prevention;
- independent connector partial failure;
- stale labels and last-success times;
- Automation pause and resume calls;
- retry button eligibility only for clearly pre-send failure;
- uncertain state has no replay action;
- route and command presentation;
- Department Inspector filter combinations;
- reset behavior;
- search coverage;
- separate lifecycle and priority rendering;
- raw-source disclosure and safe escaping;
- all-day Calendar events;
- Todoist source URL and priority preservation;
- Trello lane mapping by ID;
- true empty versus error states;
- no source-system write requests;
- no secrets in rendered diagnostics;
- responsive layouts at representative viewport widths;
- no horizontal page overflow.

Use automated browser or component tests where supported, plus manual screenshot comparison.

## Prohibited Work

Do not:

- build the browser extension;
- modify V1 orchestration code;
- add Worker Operations or Automation Logs as separate tabs;
- implement write-capable Overview or Inspector connectors;
- introduce automatic cross-system duplicate merging;
- create AI priority scoring;
- create a second task or advisory database;
- implement response-body scraping;
- redesign the approved visual system;
- add decorative charts without a defined decision question;
- edit department records or shared governance.

## Slice Two Acceptance Gate

The slice passes only when Rob can use the dashboard to understand:

1. what needs attention;
2. what is scheduled;
3. what department work is active or blocked;
4. where each authoritative source lives;
5. whether the server and automation transport are healthy;
6. which route or command needs recovery;
7. which bounded recovery action is available.

Additionally:

8. Overview, Department Inspector, and Automation are the only top-level tabs.
9. Overview and Inspector are read-only.
10. One connector failure does not collapse other panels.
11. Responsive layouts match the approved behavior at wide, medium, and narrow widths.
12. Normal viewports have no horizontal page scrolling.
13. Automated tests pass.
14. The Slice One test suite still passes.
15. No browser-extension implementation was started.

## Completion Report

Return the standard mission report plus:

- framework and component structure;
- source connector status;
- exact read-only safeguards;
- screenshots at representative wide, medium, and narrow widths;
- accessibility verification;
- automated test results;
- manual acceptance walkthrough;
- any API changes requested from Slice One and why;
- any behavior that remains fixture-backed until Mission 03.

Stop after reporting. Do not proceed to Mission 03 without a new explicit instruction from Rob.

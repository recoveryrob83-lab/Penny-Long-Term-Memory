# NOTE-20260729-017: LifeOS Dashboard Visual and Interaction Behavior

- Date: 2026-07-29
- Owner: Engineering_HQ
- Record Type: Approved UI behavior contract
- Lifecycle State: Active
- Priority: High
- Authority: Rob-approved promotion from screenshot review and existing V1 behavior code

## Visual Authority

The approved screenshots in Google Drive define the dashboard's visual language, hierarchy, density, spacing, and responsive intent:

- `Dashboard Overview.PNG`
- `Dashboard Overview 2.PNG`
- `Dashboard Overview 3.PNG`
- `Dashboard Overview 4.PNG`
- `Dashboard Department Inspection.PNG`
- `Dashboard Department Inspection2.PNG`
- `Dashboard Department Inspection3.PNG`
- `Dashboard Department Inspection3a.PNG`
- `Dashboard Department Inspection4.PNG`

The red X marks in the first Overview screenshot mean that the legacy `Worker Operations` and `Automation Logs` tabs are replaced by one V2 `Automation` tab. Automation does not disappear.

Approved top-level sections:

1. Overview
2. Department Inspector
3. Automation

## Global Shell

Preserve:

- dark command-window visual language;
- centered maximum content width near 1500 pixels;
- strong page title and blue eyebrow hierarchy;
- subtle borders, restrained shadows, rounded cards, compact badges;
- dense but readable information presentation;
- source-linked records;
- one active section at a time;
- remembered active tab;
- keyboard tab navigation and visible focus states.

The header contains the LifeOS title, concise subtitle, last completed refresh time, and `Refresh view` control.

Source health remains above navigation. Each connector reports independently as healthy, stale, partial, or unavailable. One failed connector does not collapse the dashboard.

## Responsive Layout

### Wide desktop

- page padding approximately 28 pixels;
- content centered within a maximum-width region;
- source health uses six columns when space permits;
- Overview uses a twelve-column grid;
- compact panels span four columns;
- broad panels span eight columns;
- panel height remains content-driven;
- no horizontal page scrolling.

### Medium width, approximately 1050 pixels and below

- source health changes to three columns;
- Overview panels become half-width;
- layouts keep a two-column rhythm where readable;
- typography remains readable rather than shrinking;
- text and badges wrap;
- panels grow vertically as content wraps.

`Dashboard Overview.PNG` and `Dashboard Overview 2.PNG` demonstrate responsive reflow, not proportional scaling.

### Small width, approximately 720 pixels and below

- page padding reduces to approximately 18 pixels;
- header stacks vertically;
- header actions align left;
- source cards become one column;
- Overview panels become full width;
- internal Flow lanes stack;
- compact signal grids stack;
- footer content stacks;
- controls remain reachable;
- the page does not require horizontal scrolling.

### Department Inspector breakpoints

- summary cards: four columns, then two near 1050 pixels, then one near 520 pixels;
- filters: five columns, then three near 1050 pixels, then one near 760 pixels;
- record cards: two columns on wide screens, one near 760 pixels;
- badge groups move below titles and align left on narrow screens.

## Autosizing Rules

- Panel height follows content. Do not force unequal content into equal-height cards.
- Panel width follows the responsive grid.
- Titles and summaries wrap.
- Machine paths and identifiers may truncate with ellipsis when used as single-line metadata.
- Raw source excerpts use bounded internal scrolling.
- Badges wrap within cards.
- The page scrolls vertically as one document. Internal scrolling is reserved for bounded raw or diagnostic content.

## Overview Behavior

### Today

- shows the current local date;
- emphasizes the next relevant Calendar event;
- lists active Todoist commitments;
- shows overdue and due-today badges;
- opens canonical source links;
- does not complete or reprioritize Todoist tasks.

### Flow

- presents Trello `Now`, `Next`, and `Waiting` lanes;
- uses configured list IDs for lane identity;
- opens canonical Trello records;
- does not move cards;
- does not import full comments, attachments, or history.

### Attention

- shows compact signals, not full inboxes;
- each signal contains a count, label, and short explanation;
- remains read-only;
- does not become a universal notification center.

### Drive shortcuts

- shows a curated or configured set of human-facing documents;
- opens the canonical Drive item;
- does not duplicate document contents or crawl Drive unrestrictedly.

### GitHub

- shows durable system pulse;
- separates open advisories, priority open loops, and recent durable activity;
- provides canonical source links;
- remains read-only and diagnostic.

### Recent LifeOS activity

- shows recent meaningful department notebook or durable-state records;
- identifies department, title, date, and concise summary;
- defaults to newest first;
- does not invent importance, create tasks, or merge records.

## Department Inspector Behavior

Department Inspector is a read-only operational microscope over configured GitHub sources.

Summary cards:

- normalized records;
- findings;
- records with warnings;
- visible now.

Filters:

- department;
- category;
- record type;
- state;
- priority;
- from date;
- through date;
- cross-department state;
- authority level;
- sort order;
- search;
- warnings only;
- reset.

Filters combine with AND logic and update without a full page reload. Search covers titles, summaries, departments, types, source paths, source sections, raw text, and warnings.

Results group into Work, Knowledge, Operations, and Findings. Empty categories may hide. No matches produce a clear message.

Each record card shows department, subtype, title, lifecycle state, priority, summary, record type, authority, parse confidence, best available date, warning count, source path, and an `Inspect source record` disclosure.

State and priority remain separate. Expanded raw records stay inside the same card, use escaped monospaced text, have bounded height, and do not reset filters or page position.

## Automation Behavior

The V2 Automation tab replaces both crossed-out legacy tabs.

Show:

- global dispatch state;
- server/API health;
- browser extension connection;
- registered routes count;
- active or pending commands;
- failed or uncertain commands;
- route labels and assigned ChatGPT URLs;
- route verification and health;
- command identity, advisory source and target, task summary, delivery state, attempt count, timestamps, and concise error;
- recent courier run history.

Approved controls:

- pause or resume;
- retry only a clearly pre-send failure;
- cancel pending delivery;
- open advisory;
- open target chat;
- change or re-register route;
- refresh Automation.

Pause stops new dispatches and resumes from current GitHub truth. It does not rewrite advisories or replay stale work.

Do not provide normal controls to mark work complete, mark advisories complete, infer success from assistant text, replay uncertain sends, reset advisory state, or create a second assignment record.

Wide screens may use status cards followed by two-column routes and commands with full-width logs below. Medium screens may convert dense tables to card rows. Small screens stack all sections and safely wrap or truncate URLs and identifiers.

## Non-Happy Paths

Every section must intentionally support:

- loading without displaying unconfirmed zeroes as facts;
- true empty states distinct from failures;
- stale data with last-success time;
- source-specific errors with one understandable recovery action;
- partial failure that leaves unaffected sections usable;
- secret-safe diagnostics.

## Accessibility Minimums

- keyboard-reachable controls;
- semantic tabs and disclosures;
- left/right arrow tab navigation;
- visible focus states;
- understandable button labels;
- state communicated by text as well as color;
- practical touch targets;
- restrained live-region updates for dynamic counts.

## V1 Code References

Codex may inspect these files for proven visual and interaction behavior:

- `apps/lifeos-dashboard/lifeos_dashboard/templates/index.html`
- `apps/lifeos-dashboard/lifeos_dashboard/static/styles.css`
- `apps/lifeos-dashboard/lifeos_dashboard/static/tabs.js`
- `apps/lifeos-dashboard/lifeos_dashboard/static/department-inspection.css`
- `apps/lifeos-dashboard/lifeos_dashboard/static/department-inspection.js`

Reuse responsive patterns, card styling, tab behavior, filtering, disclosures, and keyboard behavior where useful. Do not carry forward retired V1 orchestration semantics.

## Acceptance Condition

The UI passes when the screenshots remain recognizably preserved, the three V2 sections are correct, the crossed-out tabs are gone, Automation contains the approved V2 controls and telemetry, wide and narrow layouts reflow without horizontal page scrolling, content-driven cards autosize cleanly, and Rob can understand current attention, source truth, automation health, and available recovery action without opening a terminal.

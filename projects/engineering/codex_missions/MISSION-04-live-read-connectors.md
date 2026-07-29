# Codex Penny Mission 04: Live Read Connectors

- Owning Department: Engineering_HQ
- Execution Surface: Codex Penny / local repository and provider sandboxes
- Target: `apps/lifeos_dashboardv2`
- Prerequisites: Missions 01, 02, and 03 accepted by Engineering and Rob
- Lifecycle State: Waiting for explicit resume authorization
- Priority: High
- Verification Mode: IMMEDIATE_HQ
- Stop Condition: Stop after the Slice Four acceptance gate. Do not add source-system writes, production automation rollout, or V1 migration.

## Objective

Replace the fixture-backed Overview connector data with small, read-only live adapters for Todoist, Google Calendar, Trello, and curated Google Drive shortcuts while preserving the accepted GitHub-backed V2 reader, dashboard behavior, browser courier, and source-of-truth boundaries.

This slice makes the dashboard read real operational information. It does not make the dashboard a second task system, synchronization engine, or connector write surface.

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
- `projects/engineering/codex_missions/MISSION-02-dashboard.md`
- `projects/engineering/codex_missions/MISSION-03-browser-extension.md`
- accepted completion reports and current code from Missions 01 through 03

The GitHub integration packet is the authoritative connector brief for this mission. Verify provider mechanics from current official documentation only when the packet is absent, ambiguous, or outdated. Record the chosen current API version and authentication method once in connector documentation, then stop re-researching unless tests expose a conflict.

## Authentication and Baseline Preflight

Run the bounded Git/GitHub preflight from the mission README. If remote publication fails, preserve local work and continue locally.

Before editing:

- run all accepted Slice One through Slice Three automated tests;
- launch the accepted server and dashboard;
- verify fixture-backed Overview behavior still works;
- verify the Automation and browser-extension paths remain operational;
- inspect the current V2 package structure before choosing connector module locations;
- stop and report if the accepted foundation is broken rather than hiding the failure inside connector code.

## Scope and Authority

All new provider adapters in this slice are read-only.

Allowed:

- authenticate with credentials supplied outside the repository;
- list and read only configured records and containers;
- normalize provider records into the accepted dashboard read model;
- refresh on dashboard load and by explicit manual refresh;
- use a short configurable cache;
- preserve source identifiers, source container identifiers, source URLs, fetch timestamps, and last-success timestamps;
- retain safe last-known data with a visible stale label after refresh failure;
- display source-specific health, errors, and recovery guidance;
- keep sanitized fixtures for deterministic tests;
- place live integration tests behind explicit environment flags.

Not allowed:

- create, edit, complete, move, archive, or delete provider records;
- bidirectional synchronization;
- automatic migration between Trello, Todoist, Calendar, Drive, and GitHub;
- inferred duplicate merging;
- automatic priority changes;
- broad background crawling;
- webhooks, streaming sync, or minute-by-minute polling;
- connector-driven advisory creation or cross-department routing;
- a new database of tasks, advisories, or personal records;
- secrets in GitHub, logs, tests, fixtures, screenshots, or diagnostic responses.

## Shared Connector Interface

Implement or preserve one small internal connector interface equivalent to:

```text
health() -> authentication and connector health
refresh(request) -> normalized records and refresh metadata
get_last_success() -> timestamp of the last successful refresh
describe_error(error) -> human-readable message and recovery hint
```

A refresh result must carry at least:

```json
{
  "source_system": "calendar",
  "status": "ok",
  "fetched_at": "2026-07-29T14:00:00Z",
  "last_success_at": "2026-07-29T14:00:00Z",
  "records": [],
  "error": null
}
```

Use straightforward typed models or dataclasses. Do not introduce a connector framework, plugin marketplace, event bus, data warehouse, microservice split, or generalized provider abstraction.

## Shared Normalized Record Contract

Every normalized dashboard record should retain when applicable:

- `source_system`;
- `source_id` as the provider's original identifier represented as a string;
- `source_container_id`;
- `source_container_name`;
- `title`;
- compact summary or description;
- lifecycle or completion state;
- due time or start time;
- updated time when provided;
- source URL;
- fetched time;
- source error only when that individual record cannot be normalized.

Rules:

- store internal timestamps as ISO 8601;
- display times in `America/Chicago`;
- preserve all-day Calendar values as dates rather than midnight timestamps;
- do not merge records because titles resemble one another;
- do not reinterpret a Trello idea as a Todoist commitment;
- do not infer completion across systems;
- missing optional fields become empty values rather than connector-wide failures;
- one malformed record must not prevent other records or connectors from rendering.

## Credential and Secret Contract

Use environment variables or an ignored local secrets file. Update `.env.example` with names only where needed.

Expected names include:

```text
TODOIST_API_TOKEN
TRELLO_API_KEY
TRELLO_API_TOKEN
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
GOOGLE_REFRESH_TOKEN
LIFEOS_TIMEZONE=America/Chicago
CONNECTOR_CACHE_SECONDS=300
OVERVIEW_PAST_DAYS=1
OVERVIEW_FUTURE_DAYS=14
```

Do not commit live credentials, OAuth responses, authorization headers, token fragments, local secret files, or provider payloads containing private data beyond the bounded sanitized fixtures.

Logs and errors must redact credentials and authorization material.

## Todoist Adapter

Purpose: show Rob-facing commitments and reminders. Todoist remains authoritative.

Configured initial projects:

- Inbox: `6h2P5WRRqFhmvwxx`
- Work & Income: `6h2P9Vcph5RPQMWf`
- Penny / Life OS: `6h346Wr54F3jqhPh`
- Chief Business HQ: `6h35jQjFH9McwQ6M`
- Engineering Classroom: `6h38qWMrJJ4cpR39`
- General Life: `6h3j6fmQ5vwQ4r7M`

Initial scope:

- read active tasks from configured projects;
- do not load completed-task history, activity analytics, comments, attachments, reminder internals, or project-health analytics;
- preserve Todoist priority values and translate them only in the presentation layer;
- use the provider-returned task URL;
- include due date, due datetime, timezone, recurrence, deadline, labels, project, section, and parent identifiers when present.

Verify the currently supported official Todoist API endpoint once and document it locally. Do not continue using an obsolete endpoint merely because an old example exists.

## Google Calendar Adapter

Purpose: show timed commitments. Google Calendar remains authoritative.

Configured calendars:

- Primary calendar: `recoveryrob83@gmail.com`
- Optional holidays: `en.usa#holiday@group.v.calendar.google.com`

Default behavior:

- display the primary calendar by default;
- keep holidays optional or separately toggleable;
- use OAuth 2.0 with the smallest read-only Calendar scope sufficient for event listing;
- use a bounded window controlled by `OVERVIEW_PAST_DAYS` and `OVERVIEW_FUTURE_DAYS`;
- request ordered concrete instances when recurring events need display;
- handle cancelled events and declined invitations without crashing;
- preserve all-day events correctly;
- include source event links.

Do not request write scopes or mutate events.

## Trello Adapter

Purpose: show intake, possibilities, active attention, and flow without turning cards into commitments.

Enabled default board:

- LifeOS Flow Board
- Board ID: `6a594ecf9ee99fce5beb2106`
- Board URL: `https://trello.com/b/QKXdwHup/lifeos-flow-board`

Configured but disabled by default:

- Space RPG Project Command Board
- Board ID: `6a64c5305b654031d84205b1`
- Board URL: `https://trello.com/b/GCGK391a/space-rpg-project-command-board`

Perform one bounded list-manifest read for each enabled board and save configured list IDs and names. Do not repeatedly search by list name during normal refresh.

Read only the fields needed for Overview:

- board and list identifiers and names;
- card identifier and title;
- compact description;
- labels;
- due time and due-complete flag;
- compact member summary only when useful;
- card URL;
- last activity time;
- archived or closed state.

Do not load full action history, all comments, attachments, checklists, custom fields, or write-capable card operations.

## Google Drive Shortcuts Adapter

Purpose: replace fixture-backed Drive shortcuts with a curated, configured working-cabinet view. Google Drive remains authoritative for documents and deliverables.

Implement only a configured manifest of approved file or folder IDs, names, and URLs. Do not crawl all of My Drive, infer importance, inspect arbitrary document bodies, or create a Drive index.

The adapter may:

- validate configured file or folder metadata;
- provide the canonical Drive URL;
- show configured label, type, and last-modified time when available;
- report missing permission or missing item clearly;
- preserve safe last-known metadata with a stale label.

The adapter may not:

- create, edit, rename, move, share, download, or delete Drive records;
- expose document contents unless a later mission explicitly authorizes a bounded read use case;
- search broadly by keyword on each dashboard refresh.

Provide an example manifest with placeholders only. Rob's actual curated Drive IDs may remain in an ignored local configuration file when privacy or convenience warrants it.

## GitHub and Department Inspector Preservation

The accepted configured-path GitHub reader remains the source for Department Inspector and durable Overview information.

Do not replace it with repository-wide indexing. Do not alter the canonical advisory format, shared lifecycle policy, or another department's records.

The connector refresh orchestration must allow GitHub, Todoist, Calendar, Trello, and Drive to succeed or fail independently.

## Refresh, Cache, and Source Health

First production behavior:

- refresh on dashboard load;
- refresh through the existing manual Refresh control;
- use a short configurable cache, initially 300 seconds;
- preserve last-success timestamps per connector;
- show whether data is live, cached, stale, unavailable, misconfigured, rate-limited, or unauthorized;
- do not silently present stale data as fresh;
- do not erase last-known data merely because authentication or network refresh failed;
- do not add webhooks or constant background polling.

A manual refresh should request each enabled connector independently and return a combined result without making one provider the failure gate for all others.

## Dashboard Integration

Replace fixture-backed panels with live normalized data when a connector is configured and healthy.

Required UI behavior:

- clear source badges for live, cached, stale, fixture, unavailable, and authentication-required states;
- last successful refresh per source;
- provider-specific recovery hints without exposing secrets;
- source links on records;
- Overview remains read-only;
- Department Inspector remains read-only;
- Automation behavior from Slices One through Three remains unchanged;
- no fourth top-level tab;
- fixture mode remains available for development and automated tests;
- missing credentials produce an honest configuration state rather than fake empty success.

Update the global dashboard subtitle if necessary so it accurately describes both read models and bounded Automation controls.

## Required Tests

Use sanitized fixtures for deterministic tests. Mock provider success and failure conditions. Put live tests behind explicit opt-in environment flags and never require live credentials for the normal test suite.

At minimum test:

- Todoist active task normalization from every configured project;
- Todoist missing optional fields;
- Todoist priority preservation;
- Calendar timed event normalization;
- Calendar all-day event preservation;
- Calendar recurring instances;
- Calendar cancelled and declined records;
- Trello enabled-board and configured-list behavior;
- Trello idea remains visibly distinct from a commitment;
- Drive configured-shortcut metadata normalization;
- Drive missing permission and missing item behavior;
- source URLs and identifiers are preserved;
- ISO timestamps and America/Chicago display behavior;
- per-record malformed data isolation;
- authentication failure preserves safe cached data;
- rate-limit handling honors delayed refresh behavior;
- network failure in one connector leaves all other connectors operational;
- manual refresh invokes enabled connectors independently;
- cache hit, cache expiry, and force refresh;
- stale data is visibly labeled;
- missing credentials display configuration required;
- secret values and authorization headers never appear in logs or API responses;
- fixture mode remains available;
- Overview and Inspector expose no source write controls;
- Automation and browser-extension regression tests remain green;
- all Slice One through Slice Four tests pass together.

## Optional Live Verification

When Rob supplies credentials outside the repository, perform a bounded read-only live verification for each configured provider.

For each provider, verify only:

1. authentication succeeds;
2. configured containers are readable;
3. at least one real or empty valid result normalizes safely;
4. source links open correctly;
5. refresh status and last-success timestamp update;
6. removing or invalidating credentials produces a clear failure without harming other connectors;
7. no write request is made.

Do not fabricate live success when credentials are unavailable. Fixture-backed tests may pass while live verification remains explicitly pending.

## Prohibited Work

Do not:

- add source-system write endpoints or UI controls;
- request write-capable OAuth scopes when a read-only scope exists;
- modify Todoist tasks, Calendar events, Trello cards, Drive files, or GitHub source records;
- create a cross-system deduplication engine;
- classify priorities using AI;
- crawl Rob's entire Drive, GitHub repository, Todoist history, Calendar history, or Trello history;
- add background task creation or automatic migration;
- redesign the advisory contract;
- enable live production advisory dispatch if the shared V2 advisory schema remains unreconciled;
- change the browser courier's authority;
- modify V1;
- begin a production rollout, Windows startup installer, public extension publication, cloud hosting, or multi-user work;
- edit shared governance or another department's files.

## Slice Four Acceptance Gate

The slice passes only when:

1. Todoist, Google Calendar, Trello, and curated Drive adapters implement the shared read-only connector contract.
2. Fixture mode remains available and the normal automated suite does not require live credentials.
3. Configured live credentials can be supplied only outside the repository.
4. No live secret appears in source, Git history, logs, fixtures, screenshots, API responses, or documentation.
5. Overview uses live normalized data when configured and labels fixture, cached, stale, unavailable, and authentication-required states honestly.
6. Each connector refreshes and fails independently.
7. One failed connector does not collapse Overview, Department Inspector, Automation, or the browser courier.
8. Source identifiers, container identifiers, timestamps, and source links are preserved.
9. Todoist records remain commitments, Trello records remain possibilities or flow, Calendar remains timed commitments, Drive remains the working cabinet, and GitHub remains durable truth.
10. Calendar all-day and timezone behavior is correct in `America/Chicago`.
11. Cache and manual-refresh behavior are tested and understandable.
12. The dashboard exposes no Todoist, Calendar, Trello, Drive, or GitHub source write action.
13. All prior Slice One through Slice Three tests remain green.
14. Slice Four connector, normalization, cache, partial-failure, and security tests pass.
15. Live verification results are reported truthfully as passed, partial, blocked, or not run.
16. No production rollout, shared-governance migration, V1 change, or scope expansion occurred.

## Completion Report

Return the standard mission report plus:

- connector module structure and shared interface;
- provider API versions and official references used;
- authentication mechanism and scopes for each provider;
- environment variable and ignored-local-config names;
- manifest files created and what each contains;
- normalized record model and mapping decisions;
- cache duration and invalidation behavior;
- partial-failure and stale-data behavior;
- dashboard source-status behavior;
- full automated test command and results;
- live verification attempted for each provider and exact result;
- confirmation that no source-system write request was made;
- confirmation that no secret entered Git history or logs;
- known provider limitations and manual credential setup still required;
- recommendation for any later bounded startup, rollout, or connector-write mission.

Stop after reporting. Source writes, production rollout, V1 retirement, cloud hosting, generalized synchronization, and further slices require separate explicit authorization.
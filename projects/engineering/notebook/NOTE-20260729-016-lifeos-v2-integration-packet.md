# NOTE-20260729-016: LifeOS V2 Integration Packet

- Date: 2026-07-29
- Owner: Engineering_HQ
- Record Type: Approved integration contract
- Lifecycle State: Active
- Priority: High
- Authority: Rob-approved promotion from the Drive integration packet

## Purpose

Provide Codex Penny with stable source-system boundaries, live nonsecret identifiers, normalized data expectations, official documentation pointers, and test fixtures so implementation does not repeatedly rediscover the same facts.

Use this record before external documentation. Consult official provider documentation only when a required technical detail is absent, ambiguous, or has changed.

## Source-System Authority Map

- GitHub: durable operational truth, advisories, department state, approved rules, implementation history, and meaningful evidence.
- Trello: raw intake, possibilities, experiments, questions, someday work, and attention flow.
- Todoist: Rob-facing commitments and reminders.
- Google Calendar: timed commitments.
- Google Drive: human-facing documents, working designs, and deliverables.
- Dashboard: read model, diagnostics, and bounded controls. Never competing truth.

## Default Connector Posture

Overview and Department Inspector connectors are read-only in the first production version.

Allowed:

- authenticate;
- list and read configured records;
- normalize them into dashboard read models;
- retain source IDs and source URLs;
- use brief caching;
- refresh manually or on dashboard load;
- show source-specific health and errors.

Not authorized:

- create, edit, move, complete, archive, or delete source records;
- bidirectional synchronization;
- automatic migration between systems;
- inferred duplicate merging;
- automatic priority changes;
- unrestricted background crawling;
- connector-driven cross-department routing.

## Credential Contract

Never commit live secrets or put them into prompts, fixtures, logs, screenshots, or documentation.

Use environment variables or an ignored local secrets file. Provide `.env.example` with names only.

Recommended variables:

```text
GITHUB_TOKEN=
GITHUB_REPOSITORY=recoveryrob83-lab/Penny-Long-Term-Memory
TODOIST_API_TOKEN=
TRELLO_API_KEY=
TRELLO_API_TOKEN=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REFRESH_TOKEN=
LIFEOS_TIMEZONE=America/Chicago
CONNECTOR_CACHE_SECONDS=300
OVERVIEW_PAST_DAYS=1
OVERVIEW_FUTURE_DAYS=14
```

Use the smallest read scope sufficient for each connector. Git push credentials and runtime GitHub read credentials are separate concerns.

## Shared Normalized Record

Every normalized item should retain:

- `source_system`
- `source_id`
- `source_container_id`
- `source_container_name`
- `title`
- `summary` or description when useful
- lifecycle or completion state
- `due_at` or `start_at` when applicable
- `updated_at` when available
- `source_url`
- `fetched_at`
- source error only when normalization failed

Rules:

- Store timestamps as ISO 8601.
- Display times in `America/Chicago`.
- Preserve provider IDs as strings.
- Do not merge records merely because titles resemble one another.
- Do not reinterpret a Trello idea as a Todoist commitment.
- Do not infer completion across systems.
- Missing optional fields become empty values, not connector failures.

## GitHub Integration

Repository:

`recoveryrob83-lab/Penny-Long-Term-Memory`

Known department roots:

- `projects/engineering`
- `projects/wellness`
- `projects/business-development`
- `projects/office-leaks-consulting`

Canonical advisory routing currently uses:

- `coordination/ADVISORY_INDEX.md`
- source advisory records under `coordination/boards/`

Codex must perform one bounded repository manifest pass to confirm the complete current department path map. Save that manifest as configuration and do not repeatedly search the repository during normal refresh.

First-pass department files:

- `README.md`
- `SESSION_HANDOFF.md`
- `status.md` when present
- `open_loops.md`
- active advisory records referenced by the canonical index

Efficiency rules:

- fetch only configured paths;
- use SHA, ETag, conditional request, or simple cache metadata when convenient;
- avoid repository-wide searches during normal refresh;
- one malformed file must not break other departments.

Official references:

- GitHub REST contents: `https://docs.github.com/en/rest/repos/contents`
- GitHub authentication: `https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api`
- GitHub rate limits: `https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api`

## Todoist Integration

Live active project manifest captured on 2026-07-29:

- Inbox: `6h2P5WRRqFhmvwxx`
- Work & Income: `6h2P9Vcph5RPQMWf`
- Penny / Life OS: `6h346Wr54F3jqhPh`
- Chief Business HQ: `6h35jQjFH9McwQ6M`
- Engineering Classroom: `6h38qWMrJJ4cpR39`
- General Life: `6h3j6fmQ5vwQ4r7M`

Initial scope is active tasks from configured projects. Completed history, activity analytics, comments, attachments, reminders, and project-health features are excluded unless later approved.

Required task fields include ID, content, description, project, section, parent, priority, labels, due information, recurrence, deadline, completion state, source URL, and responsible user only when useful.

Preserve Todoist priority and translate it only in presentation.

Official reference: `https://developer.todoist.com/rest/v1/`

Codex should verify the currently supported official API version once during implementation, record the choice in the connector README, and stop re-researching it unless tests fail or the provider changes.

## Google Calendar Integration

Live calendar manifest captured on 2026-07-29:

- Primary: `recoveryrob83@gmail.com`, owner
- United States holidays: `en.usa#holiday@group.v.calendar.google.com`, reader

Display the primary calendar by default. The holiday calendar should be optional or separately toggleable.

Required fields include event ID, calendar ID and name, title, compact description, start, end, all-day status, timezone, location, status, recurrence ID, compact attendee information when useful, source URL, and updated time.

Use bounded time windows. Treat all-day values as dates, not midnight timestamps. Expand recurrence only when concrete occurrences are required.

Official references:

- Events list: `https://developers.google.com/calendar/api/v3/reference/events/list`
- Authorization: `https://developers.google.com/calendar/api/guides/auth`
- Scopes: `https://developers.google.com/calendar/api/auth`

## Trello Integration

Live board manifest captured on 2026-07-29:

### LifeOS Flow Board

- Board ARI: `ari:cloud:trello::board/workspace/6a594d65984d304f850a9542/6a594ecf9ee99fce5beb2106`
- URL: `https://trello.com/b/QKXdwHup/lifeos-flow-board`

### Space RPG Project Command Board

- Board ARI: `ari:cloud:trello::board/workspace/6a594d65984d304f850a9542/6a64c5305b654031d84205b1`
- URL: `https://trello.com/b/GCGK391a/space-rpg-project-command-board`

Use the LifeOS Flow Board in the default LifeOS Overview. Keep the Space RPG board configurable but disabled from general LifeOS attention unless Rob enables it.

Perform one bounded list-manifest read for enabled boards and store list IDs and names in configuration. Do not repeatedly search lists by name.

Required card fields include board, list, card ID, title, short description, labels, due date, due completion, compact members, source URL, last activity, and archive state.

Exclude full action history, all comments, attachments, checklists, custom fields, mutations, and automatic list movement.

Official references:

- API introduction: `https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/`
- Authorization: `https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/`
- Boards: `https://developer.atlassian.com/cloud/trello/rest/api-group-boards/`
- Cards: `https://developer.atlassian.com/cloud/trello/rest/api-group-cards/`

## Connector Interface

Each provider adapter should expose a small shared internal shape:

```text
health() -> connector health and authentication state
refresh(request) -> normalized records and refresh metadata
get_last_success() -> last successful refresh timestamp
describe_error(error) -> human-readable message and recovery hint
```

One connector failure must not prevent other panels from rendering. Preserve last known data with a visible stale label when safe. Never present stale data as newly fetched.

## Testing

Use sanitized fixtures for most tests. Put live integration tests behind explicit environment flags.

Test:

- valid payloads;
- missing optional fields;
- expired or absent credentials;
- permission failures;
- rate limits;
- network errors;
- malformed single records;
- partial connector failure;
- all-day events;
- recurrence;
- Todoist priority preservation;
- Trello idea versus commitment separation;
- source URL retention;
- secret redaction.

## Suggested Integration Structure

```text
apps/lifeos_dashboardv2/
  contracts/
    normalized_record.schema.json
  connectors/
    base.py
    github_connector.py
    todoist_connector.py
    calendar_connector.py
    trello_connector.py
    manifests/
      github_paths.json
      todoist_projects.json
      calendars.json
      trello_boards.json
  config/
    settings.example.json
  tests/
    fixtures/
      github/
      todoist/
      calendar/
      trello/
  .env.example
```

Preserve the module boundaries rather than decorative folder ceremony.

## Completion Condition

This packet succeeds when Codex can begin connector work without repeatedly searching for LifeOS authority rules, live container IDs, required fields, normalization behavior, error handling, or standard examples. Official provider behavior governs technical mechanics. The approved V2 design governs product scope and authority.

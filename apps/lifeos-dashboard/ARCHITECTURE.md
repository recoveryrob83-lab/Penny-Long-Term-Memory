# LifeOS Dashboard Architecture

## Product statement

The LifeOS Dashboard is a local, read-mostly window into current LifeOS state.

It is not a replacement for Trello, Todoist, Google Calendar, Gmail, Google Drive, GitHub, or Penny. Those systems remain authoritative. The dashboard summarizes high-signal state and provides a low-friction launch surface for Penny-oriented commands.

## Current architecture

```text
Browser
  |
  | HTTP on 127.0.0.1:8765
  v
FastAPI application
  |
  v
DashboardService
  |
  v
GoogleCalendarIcalDashboardSource
  |
  v
TodoistDashboardSource
  |
  v
TrelloFlowDashboardSource
  |
  v
LocalGitHubDashboardSource
  |
  v
SampleDashboardSource
```

The sources form a fallback chain:

- packaged sample data supplies a complete dashboard shape;
- the local GitHub adapter safely synchronizes and replaces GitHub-backed sections;
- the Trello adapter replaces Flow when local read credentials are configured;
- the Todoist adapter replaces Today commitments;
- the Calendar adapter replaces the next-event card;
- each source may fail without blanking unrelated panels.

## Local GitHub adapter

The GitHub adapter reads the local LifeOS checkout and requires no GitHub API credential. It has one narrowly bounded write capability: a guarded fast-forward update of the configured branch.

Before reading dashboard state, it may:

1. confirm the checkout is on `main`, or the configured sync branch;
2. confirm the working tree is clean;
3. run `git fetch --quiet origin`;
4. compare `HEAD` with `origin/main`;
5. run `git merge --ff-only origin/main` only when local history has no unique commits and is strictly behind.

It never rebases, resets, discards files, creates merge commits, changes branches, or resolves conflicts. Dirty, ahead, diverged, detached, nonconfigured, or unreachable states are left untouched and surfaced as partial source health.

After synchronization, it reads:

- `coordination/ADVISORY_INDEX.md` for open advisories;
- `memory/05_OPEN_LOOPS.md` for global priority open loops;
- `projects/*/notebook/NOTE-*.md` for recent notebook entries;
- local Git metadata for branch, current commit, working-tree state, last commit, recent durable-memory commits, and the sanitized synchronization result.

The application detects the surrounding LifeOS repository automatically. `LIFEOS_REPOSITORY_ROOT` may override the detected root. Auto-sync defaults on and may be disabled with `LIFEOS_GITHUB_AUTO_SYNC=0`. `LIFEOS_GITHUB_SYNC_BRANCH` defaults to `main`.

If the Git executable is unavailable, markdown-backed sections remain readable and Git command metadata reports a partial state rather than blanking the dashboard.

## Trello Flow adapter

The Trello adapter uses the official REST API with credentials supplied only through the ignored local `.env` file or process environment variables.

Required settings:

- `TRELLO_API_KEY`
- `TRELLO_API_TOKEN`
- `TRELLO_BOARD_ID`

The adapter performs read-only requests for board identity, open lists, and open cards. It normalizes the first card in `Now`, the first three cards in `Next`, the first three cards in `Waiting`, and counts for Now, Next, Waiting, and Captured.

Lane metadata is read from a `Lane:` line in the card description. Waiting reasons prefer a `Blocked by:` line. Trello card order is preserved through the card position field.

## Todoist commitments adapter

The Todoist adapter uses the unified Todoist API with a personal bearer token stored only in `.env`.

Required setting:

- `TODOIST_API_TOKEN`

The adapter reads active tasks through the paginated `/api/v1/tasks` endpoint and filters locally so the dashboard does not depend on natural-language filter syntax.

It normalizes:

- overdue tasks;
- tasks due today;
- tasks due within a configurable near-term horizon;
- timed and date-only due values in `LIFEOS_TIMEZONE`;
- Todoist priority into P1 through P4 display labels;
- stable task links from the current task ID format.

The default horizon is seven days and the default display limit is six commitments. Overdue tasks sort before current and upcoming tasks. Otherwise due time, priority, and title determine display order.

## Google Calendar private-iCal adapter

The Calendar adapter reads one private Google Calendar through its **Secret address in iCal format**. The URL is stored only in `.env` and must be treated as a password.

Required setting:

- `GOOGLE_CALENDAR_ICAL_URL`

The adapter performs one read-only HTTP request and parses VEVENT components locally. It supports:

- UTC, timezone-qualified, floating, and all-day start values;
- folded iCalendar lines and escaped text;
- recurring rules through `python-dateutil`;
- recurrence exclusions;
- recurrence dates;
- moved or edited recurrence instances;
- cancelled instances;
- current, upcoming, overnight, and all-day events.

The default horizon is fourteen days. Only normalized next-event data and event counts reach the dashboard payload.

## Source-specific last-good caches

Successful live web reads write normalized JSON snapshots under `.local/`:

```text
.local/trello_flow_cache.json
.local/todoist_commitments_cache.json
.local/google_calendar_cache.json
```

The `.local` directory is ignored by Git. Caches contain no API key, bearer token, or private Calendar URL.

When a source refresh fails:

1. the adapter attempts to load its last-good cache;
2. the dashboard keeps that source's previous normalized display state;
3. source health changes to `stale`;
4. the adapter exposes only a sanitized error label;
5. unrelated sources continue refreshing normally.

If no cache exists, packaged sample data remains visible for that region and the source is marked unavailable.

## Multi-source architecture

```text
Browser or pywebview desktop window
  |
  v
FastAPI application
  |
  v
DashboardService and local caches
  |
  +--> Local GitHub read + guarded sync [implemented]
  +--> Trello Flow read adapter          [implemented]
  +--> Todoist commitments adapter       [implemented]
  +--> Calendar private-iCal adapter     [implemented]
  +--> Gmail attention adapter           [deferred]
  +--> Drive shortcuts adapter           [deferred]
```

Each adapter returns normalized data plus source health and freshness metadata. One failed source must not blank the entire dashboard.

## Design principles

1. High signal over completeness.
2. Read-only before write-enabled.
3. Source systems remain authoritative.
4. Partial success is visible and useful.
5. Every source reports freshness and health honestly.
6. No secret may be stored in GitHub or normalized caches.
7. Localhost only by default.
8. The prompt launcher is reused, not discarded.
9. The financial connector remains isolated from Hub and multi-connector operation.
10. Build only from observed need.
11. Any write behavior must be narrowly authorized, deterministic, guarded, and refusal-first.

## Dashboard regions

- System bar: refresh state and source warnings.
- Today: live Calendar next event and live Todoist commitments when configured.
- Flow: live Trello Now, top Next, and selected Waiting state when configured.
- Attention: lightweight Gmail signals, deferred until client work creates the need.
- Working files: pinned or recent Drive links, deferred until client work creates the need.
- GitHub pulse: branch, checkout state, sync outcome, advisories, priority open loops, and recent durable commits.
- Recent LifeOS activity: recent GitHub notebook notes.
- Penny commands: common prompts and future launcher integration.

## Adapter contract

A source adapter exposes a stable name and returns one dashboard-shaped dictionary. Narrow source adapters are composed as a fallback chain before the payload reaches the service layer.

Adapters must:

- time out rather than hang indefinitely;
- distinguish unavailable, stale, partial, and healthy states;
- avoid writes unless a separate explicitly authorized and guarded write contract exists;
- avoid logging or caching secrets;
- return enough source metadata for the interface to explain what happened;
- paginate bounded APIs safely;
- normalize time using an explicit local timezone;
- preserve last-good display state when possible.

The Local GitHub adapter's guarded fast-forward is the only current write contract.

## Refresh behavior

The server runs with code reload disabled.

- Repository content changes: **Refresh view** fetches `origin` and fast-forwards a clean configured branch when safe.
- Trello card changes: use **Refresh view**.
- Todoist task changes: use **Refresh view**.
- Google Calendar event changes: use **Refresh view**.
- `.env` changes: stop the server with `Ctrl+C` and relaunch it.
- Dashboard code or dependency changes: auto-sync may download the files, but relaunch the running process and reinstall the editable package when dependencies changed.

## Cache direction

Source-specific JSON caches remain appropriate while the dashboard has a small number of independent read sources. A small SQLite cache may replace or consolidate them only after shared cache requirements are demonstrated.

## Packaging direction

Develop and validate in the browser first. Once useful, wrap the same local web app with pywebview for a desktop-window experience. Do not introduce Electron, React, Tauri, or another build system unless the simple stack becomes a demonstrated limitation.

## Repository boundary

The application currently lives in the LifeOS memory repository for ease of development and synchronization. If implementation expands materially, move it into a dedicated software repository while preserving this architecture record and migration notes.

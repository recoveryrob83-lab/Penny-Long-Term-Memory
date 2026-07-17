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
- the local GitHub adapter replaces GitHub-backed sections;
- the Trello adapter replaces Flow when local read credentials are configured;
- each source may fail without blanking unrelated panels.

## Local GitHub adapter

The first live adapter reads the checkout already managed by GitHub Desktop. It requires no GitHub API credential and performs no writes.

It reads:

- `coordination/ADVISORY_INDEX.md` for open advisories;
- `memory/05_OPEN_LOOPS.md` for global priority open loops;
- `projects/*/notebook/NOTE-*.md` for recent notebook entries;
- local Git metadata for branch, current commit, working-tree state, last commit, and recent durable-memory commits.

The application detects the surrounding LifeOS repository automatically. `LIFEOS_REPOSITORY_ROOT` may override the detected root.

If the Git executable is unavailable, markdown-backed sections remain readable and Git command metadata reports a partial state rather than blanking the dashboard.

## Trello Flow adapter

The Trello adapter uses the official REST API with credentials supplied only through the ignored local `.env` file or process environment variables.

Required settings:

- `TRELLO_API_KEY`
- `TRELLO_API_TOKEN`
- `TRELLO_BOARD_ID`

The adapter performs read-only requests for:

- board identity;
- open board lists;
- open cards and their list, position, description, and URL fields.

It normalizes:

- the first card in `Now`;
- the first three cards in `Next`;
- the first three cards in `Waiting`;
- counts for Now, Next, Waiting, and Captured.

Lane metadata is read from a `Lane:` line in the card description. Waiting reasons prefer a `Blocked by:` line. Trello card order is preserved through the card position field.

### Last-good cache

A successful Trello refresh writes only normalized display data to:

```text
.local/trello_flow_cache.json
```

The cache contains no API key or token and is ignored by Git. If a later request fails, the adapter returns the last-good Flow snapshot and marks Trello stale. If no cache exists, sample Flow remains visible and Trello is marked unavailable.

## Intended multi-source architecture

```text
Browser or pywebview desktop window
  |
  v
FastAPI application
  |
  v
DashboardService and local caches
  |
  +--> Local GitHub read adapter       [implemented]
  +--> Trello Flow read adapter        [implemented]
  +--> Todoist read adapter            [planned]
  +--> Calendar read adapter           [planned]
  +--> Gmail attention adapter         [planned]
  +--> Drive shortcuts adapter         [planned]
```

Each adapter returns normalized data plus source health and freshness metadata. One failed source must not blank the entire dashboard.

## Design principles

1. High signal over completeness.
2. Read-only before write-enabled.
3. Source systems remain authoritative.
4. Partial success is visible and useful.
5. Every source reports freshness and health honestly.
6. No secret may be stored in GitHub.
7. Localhost only by default.
8. The prompt launcher is reused, not discarded.
9. The financial connector remains isolated from Hub and multi-connector operation.
10. Build only from observed need.

## Dashboard regions

- System bar: refresh state and source warnings.
- Today: Calendar events and Todoist commitments.
- Flow: live Trello Now, top Next, and selected Waiting state when configured.
- Attention: lightweight Gmail signals.
- Working files: pinned or recent Drive links.
- GitHub pulse: branch, checkout state, advisories, priority open loops, and recent durable commits.
- Recent LifeOS activity: recent GitHub notebook notes.
- Penny commands: common prompts and future launcher integration.

## Adapter contract

A source adapter exposes a stable name and returns one dashboard-shaped dictionary. Narrow source adapters are composed as a fallback chain before the payload reaches the service layer.

Adapters must:

- time out rather than hang indefinitely;
- distinguish unavailable, stale, partial, and healthy states;
- avoid writes unless a separate explicitly authorized write contract exists;
- avoid logging or caching secrets;
- return enough source metadata for the interface to explain what happened.

## Refresh behavior

The server runs with code reload disabled.

- Repository content changes: pull with GitHub Desktop, then use **Refresh view**.
- Trello card changes: use **Refresh view**.
- `.env` changes: stop the server with `Ctrl+C` and relaunch it.
- Dashboard code or dependency changes: pull, reinstall the editable package if needed, and relaunch.

## Cache direction

Trello establishes the first source-specific local JSON cache. A small SQLite cache may replace or consolidate source caches after more live adapters exist and the shared requirements are understood.

## Packaging direction

Develop and validate in the browser first. Once useful, wrap the same local web app with pywebview for a desktop-window experience. Do not introduce Electron, React, Tauri, or another build system unless the simple stack becomes a demonstrated limitation.

## Repository boundary

The application currently lives in the LifeOS memory repository for ease of development and synchronization. If implementation expands materially, move it into a dedicated software repository while preserving this architecture record and migration notes.

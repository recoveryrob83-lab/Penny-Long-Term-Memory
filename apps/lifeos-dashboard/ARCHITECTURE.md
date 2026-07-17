# LifeOS Dashboard Architecture

## Product statement

The LifeOS Dashboard is a local, read-mostly window into current LifeOS state.

It is not a replacement for Trello, Todoist, Google Calendar, Gmail, Google Drive, GitHub, or Penny. Those systems remain authoritative. The dashboard summarizes high-signal state and provides a low-friction launch surface for Penny-oriented commands.

## V0 architecture

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
DashboardSource adapter
  |
  v
Sample JSON
```

V0 uses one sample-data adapter so the screen, API shape, and failure language can be evaluated before account authentication is introduced.

## Intended V1 architecture

```text
Browser or pywebview desktop window
  |
  v
FastAPI application
  |
  v
DashboardService and local cache
  |
  +--> GitHub read adapter
  +--> Trello read adapter
  +--> Todoist read adapter
  +--> Calendar read adapter
  +--> Gmail attention adapter
  +--> Drive shortcuts adapter
```

Each adapter should return normalized data plus source health and freshness metadata. One failed source must not blank the entire dashboard.

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

## Initial dashboard regions

- System bar: current time, refresh state, source warnings.
- Today: Calendar events and Todoist commitments.
- Flow: Trello Now, top Next, and selected Waiting state.
- Attention: lightweight Gmail signals.
- Working files: pinned or recent Drive links.
- Recent LifeOS activity: recent GitHub notebook notes and advisories.
- Penny commands: common prompts and future launcher integration.

## Adapter contract

A source adapter exposes a stable name and returns one dashboard-shaped dictionary. Later adapters may expose narrower source-specific payloads, but aggregation belongs in the service layer rather than the web routes.

Adapters must:

- time out rather than hang indefinitely;
- distinguish unavailable, stale, partial, and healthy states;
- avoid writes unless a separate explicitly authorized write contract exists;
- avoid logging secrets;
- return enough source metadata for the interface to explain what happened.

## Cache direction

A small local SQLite cache may be introduced after live adapters exist. It should preserve the last verified snapshot per source so a temporary outage produces a clearly marked stale view rather than an empty dashboard.

## Packaging direction

Develop and validate in the browser first. Once useful, wrap the same local web app with pywebview for a desktop-window experience. Do not introduce Electron, React, Tauri, or another build system unless the simple stack becomes a demonstrated limitation.

## Repository boundary

The scaffold currently lives in the LifeOS memory repository for ease of development and synchronization. If implementation expands materially, move the application into a dedicated software repository while preserving this architecture record and migration notes.

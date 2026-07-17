# LifeOS Dashboard

A local, read-mostly command window for Rob's LifeOS.

The dashboard is intended to answer five questions quickly:

1. What must happen today?
2. What is active right now?
3. What is waiting or blocked?
4. What changed recently across LifeOS?
5. What can Penny help with next?

## Current status

The dashboard is runnable and its first two live sources are implemented.

It includes:

- a FastAPI backend;
- a responsive browser-based dashboard;
- a read-only local GitHub adapter;
- live branch, commit, working-tree, advisory, open-loop, notebook, and durable-activity state;
- a read-only Trello Flow Board adapter;
- live Trello Now, top Next, and selected Waiting cards;
- a local last-good Trello cache for degraded operation;
- sample data for Todoist, Calendar, Gmail, and Drive;
- health and dashboard JSON endpoints;
- a small test suite.

## How live GitHub mode works

When the dashboard is installed inside the LifeOS repository, it automatically finds the repository root and starts in `local-github` mode.

The dashboard reads:

- `coordination/ADVISORY_INDEX.md` for open advisories;
- `memory/05_OPEN_LOOPS.md` for priority open loops;
- `projects/*/notebook/NOTE-*.md` for recent notebook activity;
- local Git history for branch, commit, working-tree, and recent durable activity.

GitHub remains authoritative. The dashboard shows the state currently pulled to the computer.

After GitHub Desktop pulls new LifeOS content, use **Refresh view** in the dashboard. A server restart is not required for ordinary markdown or Git-history updates.

## How live Trello mode works

The standalone dashboard cannot reuse ChatGPT's Trello session. It reads Trello through the official REST API using local environment settings.

Required local settings:

- `TRELLO_API_KEY`
- `TRELLO_API_TOKEN`
- `TRELLO_BOARD_ID`

The board ID may be the board's long ID or the short identifier found in its Trello URL between `/b/` and the board name.

Copy the included environment template:

```cmd
copy .env.example .env
```

Then edit `.env` and fill in the three values. Trello's developer flow may require creating or selecting a Power-Up to obtain an API key and then authorizing an API token.

After saving `.env`, restart the dashboard. When Trello is configured, the mode badge becomes `local-github+trello mode` and the Flow panel shows the live board.

Trello remains authoritative. Clicking **Refresh view** fetches the current open cards. A server restart is required only after changing `.env` or pulling dashboard code changes.

### Trello degraded mode

Each successful Trello refresh writes a normalized last-good snapshot to:

```text
.local/trello_flow_cache.json
```

The `.local` folder is ignored by Git. If Trello later times out or returns an error, the dashboard shows the cached Flow state and marks the Trello source as stale. Credentials are never written to the cache.

## Quick start on Windows

Open PowerShell or Command Prompt in the repository root, then run:

```powershell
cd apps/lifeos-dashboard
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
python run_dashboard.py
```

In Command Prompt, activate with:

```cmd
.venv\Scripts\activate
```

Then open:

```text
http://127.0.0.1:8765
```

After pulling dashboard code changes, stop the running server with `Ctrl+C`, run `pip install -e ".[dev]"` again when dependencies changed, and launch it again. The launcher intentionally runs with automatic code reload disabled.

An alternate checkout can be selected with the `LIFEOS_REPOSITORY_ROOT` environment variable.

## Useful endpoints

- Dashboard: `http://127.0.0.1:8765/`
- Health check: `http://127.0.0.1:8765/api/health`
- Dashboard JSON: `http://127.0.0.1:8765/api/dashboard`
- FastAPI docs: `http://127.0.0.1:8765/docs`

## Development commands

```powershell
python -m pytest -q
ruff check .
```

## Planned integration order

1. GitHub notebooks, advisories, open loops, and durable activity: implemented
2. Trello Flow Board state: implemented; local credentials required
3. Todoist and Google Calendar commitments
4. Gmail attention signals and Google Drive shortcuts
5. Optional pywebview desktop packaging

## Security rules

- Never commit API keys, OAuth tokens, passwords, cookies, or account data.
- Keep secrets in the ignored local `.env` file or process environment variables.
- Bind the development server to `127.0.0.1`, not every network interface.
- Treat the dashboard as read-only or read-mostly until a specific write action earns its place.
- Keep Trello, Todoist, Calendar, Gmail, Drive, and GitHub as their own sources of truth.
- Penny remains the worker and conversational control layer.

## Project boundary

This folder contains application code. The surrounding repository remains the LifeOS durable-memory and architecture repository. If the dashboard grows into a substantial product, it should move into a dedicated software repository without breaking its documented interfaces.

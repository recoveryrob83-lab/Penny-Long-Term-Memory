# LifeOS Dashboard

A local, read-mostly command window for Rob's LifeOS.

The dashboard is intended to answer five questions quickly:

1. What must happen today?
2. What is active right now?
3. What is waiting or blocked?
4. What changed recently across LifeOS?
5. What can Penny help with next?

## Current status

This is the first runnable scaffold.

It includes:

- a FastAPI backend;
- a browser-based dashboard shell;
- sample data for Trello, Todoist, Calendar, Gmail, Drive, GitHub notebooks, and prompt commands;
- health and dashboard JSON endpoints;
- explicit freshness and unavailable-state placeholders;
- a source-adapter boundary for later live integrations;
- a small test suite.

No live account credentials or connector integrations are included yet.

## Quick start on Windows

Open PowerShell in the repository root, then run:

```powershell
cd apps/lifeos-dashboard
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
python run_dashboard.py
```

Then open:

```text
http://127.0.0.1:8765
```

The dashboard starts in sample-data mode.

## Useful endpoints

- Dashboard: `http://127.0.0.1:8765/`
- Health check: `http://127.0.0.1:8765/api/health`
- Dashboard JSON: `http://127.0.0.1:8765/api/dashboard`
- FastAPI docs: `http://127.0.0.1:8765/docs`

## Development commands

```powershell
pytest
ruff check .
```

## Planned integration order

1. GitHub notebook and advisory summaries
2. Trello Flow Board state
3. Todoist and Google Calendar commitments
4. Gmail attention signals and Google Drive shortcuts
5. Optional pywebview desktop packaging

The first live adapter should be GitHub because it can provide recent notebook activity, advisory state, open loops, and durable LifeOS context without changing external state.

## Security rules

- Never commit API keys, OAuth tokens, passwords, cookies, or account data.
- Keep secrets in local environment variables or an ignored local configuration file.
- Bind the development server to `127.0.0.1`, not every network interface.
- Treat the dashboard as read-only or read-mostly until a specific write action earns its place.
- Keep Trello, Todoist, Calendar, Gmail, Drive, and GitHub as their own sources of truth.
- Penny remains the worker and conversational control layer.

## Project boundary

This folder contains application code. The surrounding repository remains the LifeOS durable-memory and architecture repository. If the dashboard grows into a substantial product, it should move into a dedicated software repository without breaking its documented interfaces.

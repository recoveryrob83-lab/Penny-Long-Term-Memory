# LifeOS Dashboard

A local, read-mostly command window for Rob's LifeOS.

The dashboard is intended to answer five questions quickly:

1. What must happen today?
2. What is active right now?
3. What is waiting or blocked?
4. What changed recently across LifeOS?
5. What can Penny help with next?

## Current status

The dashboard is runnable and its first four live sources are implemented.

It includes:

- a FastAPI backend;
- a responsive browser-based dashboard;
- a local GitHub adapter with guarded fast-forward synchronization;
- live branch, commit, working-tree, advisory, open-loop, notebook, and durable-activity state;
- a read-only Trello Flow Board adapter;
- live Trello Now, top Next, and selected Waiting cards;
- a read-only Todoist commitments adapter;
- live overdue, today, and near-term Todoist tasks;
- a read-only Google Calendar private-iCal adapter;
- live next-event display with recurring event expansion;
- independent last-good local caches for Trello, Todoist, and Calendar;
- sample data for Gmail and Drive;
- health and dashboard JSON endpoints;
- deterministic adapter and smoke tests.

## Live source chain

The application composes sources in this order:

```text
Sample data
  -> local GitHub checkout
  -> Trello Flow Board
  -> Todoist commitments
  -> Google Calendar private iCal feed
```

Each adapter replaces only its own dashboard region. One source can become stale or unavailable without blanking unrelated panels.

## Local configuration

The standalone dashboard cannot reuse ChatGPT connector sessions. Live web sources use secrets stored only in the ignored local `.env` file.

Create the file once:

```cmd
copy .env.example .env
```

Never commit `.env`.

### Trello

Required settings:

```text
TRELLO_API_KEY=
TRELLO_API_TOKEN=
TRELLO_BOARD_ID=
```

The token should be authorized with read-only scope. The Flow panel reads the open board lists and cards, preserves Trello order, extracts `Lane:` metadata, and prefers `Blocked by:` for Waiting reasons.

A successful refresh writes normalized display data to:

```text
.local/trello_flow_cache.json
```

### Todoist

Required setting:

```text
TODOIST_API_TOKEN=
```

Use the personal API token from Todoist Settings under Integrations or Developer. The adapter reads active tasks, keeps overdue tasks visible, includes tasks due within the next seven days, sorts by due time and priority, and shows up to six commitments.

A successful refresh writes normalized display data to:

```text
.local/todoist_commitments_cache.json
```

Optional controls:

```text
TODOIST_HORIZON_DAYS=7
TODOIST_COMMITMENT_LIMIT=6
```

### Google Calendar

Required setting:

```text
GOOGLE_CALENDAR_ICAL_URL=
```

Use the private **Secret address in iCal format** from Google Calendar:

1. Open Google Calendar on a computer.
2. Open Settings.
3. Under **Settings for my calendars**, select the calendar.
4. Open **Integrate calendar**.
5. Copy the **Secret address in iCal format**.

Treat that URL like a password. Do not paste it into chat, documentation, or GitHub. Reset it in Google Calendar if it is ever exposed.

The adapter expands recurring events, respects exclusions and recurrence overrides, handles all-day and timed events, and shows the next current or upcoming event within a fourteen-day horizon.

A successful refresh writes normalized display data to:

```text
.local/google_calendar_cache.json
```

Optional control:

```text
CALENDAR_HORIZON_DAYS=14
```

### Timezone

The dashboard defaults to Rob's current LifeOS timezone:

```text
LIFEOS_TIMEZONE=America/Chicago
```

## How live GitHub mode works

When the dashboard is installed inside the LifeOS repository, it automatically finds the repository root and reads:

- `coordination/ADVISORY_INDEX.md` for open advisories;
- `memory/05_OPEN_LOOPS.md` for priority open loops;
- `projects/*/notebook/NOTE-*.md` for recent notebook activity;
- local Git history for branch, commit, working-tree, and recent durable activity.

GitHub remains authoritative. On every dashboard load or **Refresh view**, the adapter checks the local checkout and attempts a guarded synchronization.

Automatic synchronization proceeds only when all of these conditions are true:

- the checkout is on the configured branch, `main` by default;
- the working tree is clean;
- `origin/main` can be fetched;
- the local branch is behind the remote without any local-only commits;
- Git can apply the update with `git merge --ff-only`.

The dashboard never rebases, resets, discards files, creates merge commits, or resolves conflicts. A dirty, ahead, diverged, detached, or non-main checkout is left untouched and shown as a partial GitHub source with a plain-language reason.

Optional controls:

```text
LIFEOS_GITHUB_AUTO_SYNC=1
LIFEOS_GITHUB_SYNC_BRANCH=main
```

Set `LIFEOS_GITHUB_AUTO_SYNC=0` to restore manual-pull behavior.

## Refresh and degraded behavior

Use **Refresh view** for ordinary source updates:

- guarded GitHub fetch and fast-forward, followed by refreshed repository state;
- Trello card changes;
- Todoist task changes;
- Google Calendar event changes.

Restart the dashboard after changing `.env`. If auto-sync pulls dashboard application code, restart before expecting the running Python process to use that new code. Run `pip install -e ".[dev]"` again when dependencies changed.

Each live web adapter writes only normalized display data to `.local/`, which is ignored by Git. If a source later times out or returns an error, the dashboard uses that source's last-good cache and marks it stale. Tokens, keys, and the private Calendar URL are never cached.

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

An alternate checkout can be selected with `LIFEOS_REPOSITORY_ROOT`.

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

1. GitHub notebooks, advisories, open loops, durable activity, and guarded auto-sync: implemented
2. Trello Flow Board state: implemented
3. Todoist and Google Calendar commitments: implemented; local credentials required
4. Gmail attention signals and Google Drive shortcuts: deferred until client work creates a demonstrated need
5. Optional pywebview desktop packaging

## Security rules

- Never commit API keys, OAuth tokens, private calendar URLs, passwords, cookies, or account data.
- Keep secrets in the ignored local `.env` file or process environment variables.
- Bind the development server to `127.0.0.1`, not every network interface.
- Treat the dashboard as read-only or read-mostly until a specific write action earns its place.
- The only current write behavior is the guarded Git fast-forward of a clean configured branch.
- Keep Trello, Todoist, Calendar, Gmail, Drive, and GitHub as their own sources of truth.
- Penny remains the worker and conversational control layer.

## Project boundary

This folder contains application code. The surrounding repository remains the LifeOS durable-memory and architecture repository. If the dashboard grows into a substantial product, it should move into a dedicated software repository without breaking its documented interfaces.

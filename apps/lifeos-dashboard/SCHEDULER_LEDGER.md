# LifeOS Scheduler Ledger

## Purpose

The LifeOS Scheduler Ledger is a cloud-visible Google Sheet mirror of the local Automation Command Center schedule definitions.

It solves one narrow problem: when the Windows computer, dashboard, or ChatGPT desktop app stops operating, Rob or any connected Penny can inspect the Sheet and immediately see that an active schedule is overdue.

The Sheet is not a second scheduler, retry engine, or execution-history database.

## Source Boundary

- Command Center SQLite remains authoritative for local schedule definitions and detailed execution history.
- The Google Sheet is the authoritative cloud-visible monitoring mirror.
- The dashboard writes the current schedule state to the Sheet.
- Penny reads the Sheet on request and reports overdue or failed schedules.
- Penny does not need to mark missed runs or maintain separate audit rows.
- The Sheet never controls, retries, pauses, resumes, or deletes local schedules.

## One-Row Contract

Each local scheduled job has one Sheet row keyed by its stable local schedule ID.

The row contains:

- schedule name, destination, and cadence;
- start date, scheduled time, weekdays, and timezone;
- enabled state and visible schedule lifecycle;
- mode and prompt type;
- next due time;
- last run time, status, and reason;
- the last time the dashboard published the row;
- a live Health formula.

The Health formula recalculates every minute:

- non-active schedules display their lifecycle state, such as Paused, Completed, or Failed;
- active schedules with no future time display No future run;
- active schedules more than five minutes past Next Due display OVERDUE;
- otherwise active schedules display On schedule.

This supports direct questions such as:

- "Were any LifeOS scheduled jobs missed?"
- "Is Engineering Daily Sync stale?"
- "When did each active schedule last run?"

## Google Sheet

Title: `LifeOS Scheduler Ledger`

Spreadsheet ID:

```text
1o5Qkzntd5OmKX7Vxix-PbhbuyPigJvss1AkP7Kvb0Q4
```

Tab: `Run Ledger`

The Sheet uses the `America/Chicago` timezone and minute-level recalculation.

## Local Authentication

The standalone dashboard cannot reuse ChatGPT's Google Drive connector session. It needs its own Google Sheets API credentials.

Recommended unattended setup:

1. Use a Google Cloud project with the Google Sheets API enabled.
2. Create a service account.
3. Download its JSON credential file to a private local path outside the repository.
4. Share `LifeOS Scheduler Ledger` with the service account email as Editor.
5. Add the following values to `apps/lifeos-dashboard/.env`:

```text
GOOGLE_SHEETS_LEDGER_SPREADSHEET_ID=1o5Qkzntd5OmKX7Vxix-PbhbuyPigJvss1AkP7Kvb0Q4
GOOGLE_SHEETS_LEDGER_CREDENTIALS_FILE=C:\private\lifeos-scheduler-ledger.json
GOOGLE_SHEETS_LEDGER_SHEET_NAME=Run Ledger
```

Never commit the JSON credential file or its contents.

Application Default Credentials are also supported when `GOOGLE_SHEETS_LEDGER_CREDENTIALS_FILE` is omitted, but unattended operation still requires credentials that remain available after restart.

## Failure Boundary

Sheet publication is best-effort and never blocks a local schedule from saving or running.

The Automation UI displays one of these states:

- `Ledger off`: no spreadsheet ID configured;
- `Ledger ready`: configured but no successful publication has occurred in the current process;
- `Ledger synced`: the latest publication succeeded;
- `Ledger error`: the latest publication failed.

Hovering the scheduler status exposes the latest error or the Sheet URL.

A ledger error is a monitoring failure, not proof that the scheduled job itself failed.

## Validation Checklist

1. Pull the latest dashboard code.
2. Reinstall dependencies because Google authentication packages were added.
3. Configure the local `.env` values.
4. Restart the dashboard.
5. Confirm the Automation header displays `Ledger synced`.
6. Confirm existing schedule definitions appear as one row each in `Run Ledger`.
7. Create a draft-only test schedule and confirm one new row appears.
8. Edit or pause the schedule and confirm the same row changes rather than creating another row.
9. Run the schedule and confirm Last Run, Last Status, Last Reason, Next Due, and Dashboard Updated change on that same row.
10. Delete the test schedule and confirm its row is cleared.
11. For an overdue test, stop the dashboard before the due time and confirm Health changes to `OVERDUE` after the five-minute grace period without any worker running.

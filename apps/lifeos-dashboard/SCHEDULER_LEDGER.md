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

## Local Execution Policy

The local scheduler uses the same strict five-minute threshold displayed by the Sheet:

- a job due within the five-minute grace window may execute normally;
- a job more than five minutes overdue is paused without catch-up execution;
- pausing an overdue job does not create fake execution history or change Last Run;
- a failed or nontransiently refused scheduled run pauses immediately;
- only a successful recurring run advances to its next occurrence;
- manual Resume recalculates the next due time from the current time and records the definition as rearmed;
- an expired one-time definition cannot be resumed until its date and time are edited into the future.

The Sheet only reports the resulting state. It does not enforce this policy.

## Google Sheet

Title: `LifeOS Scheduler Ledger`

Spreadsheet ID:

```text
1o5Qkzntd5OmKX7Vxix-PbhbuyPigJvss1AkP7Kvb0Q4
```

Tab: `Run Ledger`

The Sheet uses the `America/Chicago` timezone and minute-level recalculation.

## No-Billing Apps Script Transport

The standalone dashboard cannot reuse ChatGPT's Google Drive connector session. It publishes through a web app bound directly to the Scheduler Ledger Sheet.

This path requires no service account, downloaded JSON key, separately managed Google Cloud project, or billing account.

The endpoint code lives at:

```text
apps/lifeos-dashboard/apps-script/scheduler_ledger_web_app.gs
```

### Deploy the bound script

1. Open `LifeOS Scheduler Ledger` in Google Sheets.
2. Open **Extensions > Apps Script**.
3. Replace the default editor contents with `scheduler_ledger_web_app.gs` from the repository.
4. Save the project with a clear name such as `LifeOS Scheduler Ledger Endpoint`.
5. Open **Project Settings** in the Apps Script editor.
6. Under **Script Properties**, add:

```text
Property: LEDGER_SECRET
Value: <a long random secret used only for this ledger>
```

The optional `LEDGER_SHEET_NAME` property may be set to `Run Ledger`; the script already uses that name by default.

7. Select **Deploy > New deployment**.
8. Choose **Web app** as the deployment type.
9. Set **Execute as** to the script owner.
10. Set access to **Anyone** so the local dashboard can POST without a Google login. The shared secret still protects every write.
11. Authorize the script when prompted.
12. Copy the deployed web app URL ending in `/exec`.

Do not use the `/dev` test URL for ordinary dashboard operation.

### Create the shared secret

A convenient PowerShell command generates a 64-character value:

```powershell
$secret = [guid]::NewGuid().ToString("N") + [guid]::NewGuid().ToString("N")
$secret
```

Put the same value in the Apps Script `LEDGER_SECRET` property and the ignored local `.env` file. Never commit or paste the secret into chat.

### Local `.env`

Add:

```text
GOOGLE_SHEETS_LEDGER_SPREADSHEET_ID=1o5Qkzntd5OmKX7Vxix-PbhbuyPigJvss1AkP7Kvb0Q4
GOOGLE_SHEETS_LEDGER_WEB_APP_URL=https://script.google.com/macros/s/<deployment-id>/exec
GOOGLE_SHEETS_LEDGER_SHARED_SECRET=<same value as LEDGER_SECRET>
GOOGLE_SHEETS_LEDGER_SHEET_NAME=Run Ledger
```

Restart the dashboard after changing `.env`.

## Endpoint Safety

- Every POST must contain the matching shared secret.
- The script verifies the expected spreadsheet ID and tab name.
- A script lock serializes simultaneous writes.
- Schedule text is written as plain text so user-controlled names cannot become formulas.
- Only the Health column receives a formula generated by the bound script.
- The dashboard follows Apps Script's secure response redirect and verifies the returned spreadsheet identity.
- Apps Script errors appear as `Ledger error` but never block the local scheduler.

Changing the Apps Script code requires a new deployment version or an updated deployment before the `/exec` endpoint uses the change.

## Failure Boundary

Sheet publication is best-effort and never blocks a local schedule from saving or running.

The Automation UI displays one of these states:

- `Ledger off`: no ledger settings configured;
- `Ledger ready`: configured but no successful publication has occurred in the current process;
- `Ledger synced`: the latest publication succeeded;
- `Ledger error`: configuration is incomplete or the latest publication failed.

Hovering the scheduler status exposes the latest error or the Sheet URL.

A ledger error is a monitoring failure, not proof that the scheduled job itself failed.

## Validation Checklist

1. Pull the latest dashboard code.
2. Reinstall the dashboard package so removed service-account dependencies are reconciled.
3. Deploy the bound Apps Script and configure the shared secret.
4. Configure the local `.env` values.
5. Restart the dashboard.
6. Confirm the Automation header displays `Ledger synced` after a schedule is published.
7. Confirm existing schedule definitions appear as one row each in `Run Ledger`.
8. Create a draft-only test schedule and confirm one new row appears.
9. Edit or pause the schedule and confirm the same row changes rather than creating another row.
10. Run the schedule and confirm Last Run, Last Status, Last Reason, Next Due, and Dashboard Updated change on that same row.
11. Delete the test schedule and confirm its row is removed and later rows compact upward.
12. For an overdue test, stop the dashboard before the due time and confirm Health changes to `OVERDUE` after the five-minute grace period without any worker running.
13. Restart the dashboard and confirm the overdue definition pauses without launching ChatGPT automation or creating execution history.
14. Resume a recurring paused definition and confirm Next Due is recalculated into the future with status `rearmed`.
15. Confirm an expired one-time definition refuses Resume until it is edited to a future date and time.

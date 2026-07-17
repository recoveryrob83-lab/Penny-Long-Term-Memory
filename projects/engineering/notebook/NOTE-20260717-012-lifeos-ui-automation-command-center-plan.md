# LifeOS UI Automation Command Center Plan

Date: 2026-07-17
Status: Planned
Owner: Chief Engineering Penny

## Purpose

Turn the validated ChatGPT Classic UI Automation engine into a practical LifeOS Automation Command Center where Rob can select a destination, choose or enter a prompt, choose draft or send behavior, and run the job immediately or on a controlled schedule.

The command center should live inside the existing local LifeOS Dashboard rather than as a separate standalone utility unless later technical evidence strongly favors separation.

## Supported destinations

The first implementation must support all eight LifeOS destinations:

1. `LifeOS HQ` — central hub
2. `Main Assistant HQ`
3. `Engineering HQ`
4. `Logistics HQ`
5. `Business HQ`
6. `Office Leaks HQ`
7. `Finance HQ`
8. `Wellness HQ`

All destination mappings must remain exact and must use the canonical naming standard in:

- `memory/HQ_NAMING_STANDARD.md`

No fuzzy destination matching is permitted.

## Core user workflow

A user creates an automation job by choosing:

### Destination

Select one of the eight supported LifeOS destinations.

### Prompt source

- Canonical destination boot prompt
- Saved command or template
- Custom prompt entered directly
- Later extension: prompt loaded from an approved repository file

### Execution mode

- Draft only
- Send automatically

Draft only is always the default.

Send mode must require an explicit confirmation control when a job is created or edited.

### Timing

- Run now
- Run once at a selected date and time
- Daily
- Weekly on selected days
- Every X hours
- Later extension: advanced custom recurrence

### Optional controls

- Start date
- End date
- Maximum run count
- Skip when the same job ran recently
- Disable after first failure
- Require ChatGPT Classic to already be open
- Later extension: launch ChatGPT Classic automatically when needed

## Command center interface

The page should contain three primary regions.

### 1. Create Job

Inputs:

- Job name
- Destination
- Prompt source
- Prompt text or template
- Draft or send mode
- Schedule type
- Date and time controls
- Time zone
- Retry and failure policy
- Enabled or paused state

The interface should display a plain-language summary before saving, for example:

> Every weekday at 7:00 AM, send the morning synchronization prompt to Main Assistant HQ.

This summary is a configuration safety check and should update live as fields change.

### 2. Scheduled Jobs

Display:

- Job name
- Destination
- Next run
- Execution mode
- Enabled, paused, running, failed, or completed status
- Last result

Actions:

- Run now
- Edit
- Pause or resume
- Duplicate
- Delete
- View history

### 3. Activity Log

Every attempt must create a durable execution record containing:

- Job identifier
- Scheduled time
- Actual start time
- Completion time
- Destination
- Destination verification result
- Sidebar expansion result
- Composer readiness result
- Existing-draft policy result
- Prompt write result
- Clipboard verification result
- Send result
- Final status
- Exact failure reason
- Diagnostic reference when available

Failures must be explicit. Example:

> Stopped before writing because the expected Main Assistant HQ document was not verified.

The log must never collapse uncertainty into a generic success or failure message.

## Architecture

The dashboard must not directly perform long-running UI Automation inside a web request handler.

Use separated components:

1. Dashboard UI creates and manages validated jobs.
2. A local job store persists definitions and execution history.
3. A scheduler identifies jobs that are due.
4. A single-job runner invokes the existing UI Automation engine.
5. The engine returns a structured execution result.
6. The runner records the result and calculates the next run.
7. The dashboard reads state and history from the job store.

Recommended local persistence:

- SQLite for jobs, schedules, run history, and locking state

Recommended execution boundary:

- one local runner process
- one automation job at a time
- explicit process lock to prevent simultaneous UI control

## Proposed job model

Example:

```json
{
  "id": "job-main-morning-sync",
  "name": "Morning Main Sync",
  "destination": "main",
  "prompt_type": "custom",
  "prompt": "Run the morning LifeOS synchronization...",
  "mode": "send",
  "schedule_type": "weekly",
  "days": ["MO", "TU", "WE", "TH", "FR"],
  "time": "07:00",
  "timezone": "America/Chicago",
  "enabled": true,
  "stop_after_failure": true
}
```

Destination keys should include:

- `hub`
- `main`
- `engineering`
- `logistics`
- `business`
- `office-leaks`
- `finance`
- `wellness`

## Safety contract

The command center must inherit every verified engine protection:

- exact destination mapping
- exact active-document verification
- one bounded `Show more` expansion when the exact chat is hidden
- one bounded retry for the exact generic `ChatGPT` loading state
- stable and enabled Group composer verification
- preservation of an occupied composer
- prompt write verification through clipboard round-trip
- strict character integrity with only documented UI presentation transforms
- explicit send authorization
- safe stop on uncertainty
- no fuzzy chat selection
- no blind retry after an uncertain send result

Additional command-center protections:

- Draft only by default
- Global `Pause all automation` control
- One automation job at a time
- Duplicate-run protection
- Job-level stop-after-failure option
- No automatic retry after a send result becomes uncertain
- Visible current-run status
- Emergency stop control
- Clear next-run preview
- Execution history retained locally

## Connector limitation

The engine can verify prompt text and the accessible transformation of a leading `@GitHub` mention, but it cannot prove that the GitHub connector is active in the target chat.

Accepted current assumption:

- GitHub normally remains active in LifeOS chats because it is frequently used
- connector-context failure is rare, visible, and manually recoverable
- automatic connector-pill resolution is not part of the first command-center implementation

## Build sequence

### Phase 1 — Manual Command Center

Goal: prove the dashboard-to-engine boundary safely.

Deliver:

- Automation Command Center dashboard page
- all eight destinations, including `LifeOS HQ`
- canonical boot prompt or custom prompt
- draft or send mode
- explicit send confirmation
- Run now button
- structured execution result
- activity log entry
- one-job-at-a-time lock
- global pause control

No scheduling in Phase 1.

### Phase 2 — One-Time Scheduled Jobs

Deliver:

- SQLite job persistence
- one-time date and time selection
- local scheduler service
- next-run display
- run history
- pause, resume, edit, duplicate, and delete
- restart-safe pending jobs

### Phase 3 — Recurring Jobs

Deliver:

- daily schedules
- weekly schedules with selected days
- every-X-hours schedules
- start and end dates
- maximum run count
- duplicate-run protection
- next-run calculation
- stop-after-failure behavior

### Phase 4 — Reliability and Recovery

Possible additions:

- automatic ChatGPT Classic launch
- preflight health checks
- screenshots on failure
- structured diagnostic bundles
- Windows notifications
- recovery instructions linked from failed runs
- richer template library
- approved repository-backed prompts

## First implementation recommendation

Start with Phase 1 only.

The first useful release should let Rob:

1. open the LifeOS Dashboard;
2. choose one of eight destinations;
3. select a canonical boot prompt or enter a custom prompt;
4. choose draft or send;
5. review the plain-language execution summary;
6. click Run now;
7. see the verified result in the activity log.

This creates immediate value while keeping scheduling complexity out of the first integration test.

## Naming

Recommended page name:

- `Automation Command Center`

Recommended internal object name:

- `Job`

The interface may use more expressive visual language, but code, logs, schemas, and diagnostics should use the plain term `job` for clarity.

## Dependencies and references

Primary automation implementation:

- `apps/lifeos-dashboard/automation/open_department_chat_group.py`
- `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`
- `apps/lifeos-dashboard/automation/draft_department_boot.py`

Durable lessons and recovery playbook:

- `projects/engineering/notebook/NOTE-20260717-011-chatgpt-ui-automation-lessons-and-recovery-playbook.md`

Completed live-send validation record:

- `projects/engineering/notebook/NOTE-20260717-010-desktop-department-automation-live-send-handoff.md`

## Current decision

The UI Automation engine is sufficiently validated to begin Phase 1 design and implementation.

Scheduling remains deliberately deferred until the manual command-center path proves that the dashboard, job runner, locking, structured results, and safety controls work together reliably.

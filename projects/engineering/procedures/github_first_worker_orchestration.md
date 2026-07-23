# GitHub-First Worker Orchestration

Procedure ID: `github_first_worker_orchestration`
Procedure Version: 1
Owner: Engineering HQ
Lifecycle State: Active
Priority: Normal

## Purpose

Connect the existing Life OS Worker machinery into one low-friction operating loop.

GitHub is the operational desk, interdepartmental communication layer, and durable source of truth. SQLite is local desktop automation memory only.

## Canonical Flow

1. Rob, Chief of Staff HQ, or an owning Department HQ creates or materially revises one canonical execution-ready advisory in GitHub.
2. The local LifeOS Dashboard safely synchronizes the GitHub checkout.
3. The dashboard discovers the advisory through `coordination/ADVISORY_INDEX.md` and its source department board.
4. The dashboard wakes the exact authorized Worker once and returns the browser courier immediately.
5. The Worker performs the bounded work and writes the result or linked evidence required by the advisory.
6. The dashboard notices the committed GitHub result, ingests it into local automation state, and wakes the owning Department HQ when review is required.
7. The Department HQ or Rob reviews the work and updates or closes the canonical advisory under source-owner authority.
8. Chief of Staff scheduled reporting reads GitHub directly and reports meaningful new work, holds, decisions, signoffs, and closures to Rob.

## Runtime Boundary

SQLite may store only local automation details such as:

- dispatch deduplication;
- one-job locking;
- browser submission and return evidence;
- restart recovery;
- local retry or hold diagnostics;
- result and review ingestion state.

Chief of Staff does not need SQLite access and must not depend on it for reporting.

## Orchestrator Behavior

The dashboard orchestrator may:

- safely fetch and fast-forward a clean local Git checkout;
- stop when the checkout is dirty, locally ahead, or divergent;
- discover execution-ready Worker advisories;
- suppress an already-sent advisory revision;
- dispatch a new advisory through the existing browser courier;
- detect and ingest committed Worker result artifacts;
- wake the owning Department HQ after validated results;
- detect and ingest committed HQ or Rob review artifacts;
- expose current orchestration health and recent events through Worker Operations.

## Prohibited Behavior

The orchestrator must not:

- create advisory authority;
- invent or prioritize work;
- wake Chief of Staff through the browser courier;
- treat unverified Worker prose as completed work;
- perform Rob-only judgment;
- close or materially edit source advisories;
- create a second operational ledger;
- merge dirty or divergent Git branches automatically;
- retry an uncertain or confirmed browser send blindly.

## Chief of Staff Reporting

Chief of Staff scheduled reporting reads GitHub directly. It should report only meaningful changes such as:

- new execution-ready work;
- completed or verified work;
- holds or elevations;
- rejected verification;
- work awaiting Rob or Department HQ signoff;
- advisories ready for source-owner closure;
- newly closed work.

No meaningful change means no notification.

## Activation

The standard launcher is:

`apps/lifeos-dashboard/automation/validate_and_run_worker_operations.cmd`

After its focused validation gate passes, it launches the dashboard with:

- `LIFEOS_WORKER_ORCHESTRATOR_ENABLED=1`;
- a default 30-second GitHub monitoring interval;
- the existing local browser, pause, lock, and duplicate-suppression safeguards.

## Completion Condition

This procedure is operationally proven when one new advisory flows from GitHub discovery through Worker dispatch, committed result detection, owning-HQ review routing, source-owner signoff, and Chief of Staff GitHub reporting without Rob manually transporting prompts or reports between chats.

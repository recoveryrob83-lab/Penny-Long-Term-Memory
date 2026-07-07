# Captain's Log

Updated: 2026-07-06
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Short operational journal for major Life OS work sessions, discoveries, decisions, and completed batches.

## Operating Rule

This is not a transcript and not a personal diary.

Use this file for concise, dated entries future Penny should know about.

Keep sensitive details out of this file. Detailed records belong in Drive, Gmail, Calendar, Todoist, or project-specific files.

---

## 2026-07-06 — Advisory Routing Simplified

### Summary

Consumed ADV-20260706-018 from Engineering and simplified the Life OS advisory routing architecture.

### Completed Work

- Promoted `coordination/ADVISORY_INDEX.md` to the sole active advisory routing dashboard.
- Kept source department boards under `coordination/boards/` as canonical advisory text.
- Froze `coordination/DEPARTMENT_EVENT_INBOX.md` as historical read/ingestion record only.
- Updated Startup Boot, Operating Rules, Coordination README, Advisory Template, Session Handoff, Life Logistics handoff, Open Loops, Engineering board, Advisory Index, and Department Event Inbox.

### Decision / Lesson

Normal advisory routing now requires two writes only: source board plus Advisory Index.

This reduces connector write load, stale routing risk, safety-trigger exposure, and scheduled-worker complexity.

## 2026-07-06 — Nightly Sync and Connector Pattern Adoption

### Summary

Ran Life Logistics nightly GitHub sync after Main Assistant and Engineering connector-reliability advisories.

### Findings

- ADV-20260706-016 was already closed after Engineering and Life Logistics consumed the Gemini Drive-worker workflow observation.
- Engineering board contained ADV-20260706-017, recommending a connector reliability operating pattern based on Gemini/Drive/GitHub tests.
- Rob passed a separate Engineering advisory recommending review of whether Department Event Inbox should remain part of active advisory routing.

### Completed Work

- Created `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md` from ADV-20260706-017.
- Closed ADV-20260706-017 on Engineering board, Advisory Index, and Department Event Inbox.
- Created ADV-20260706-018 on Engineering board for advisory-routing simplification review.
- Updated Advisory Index and Department Event Inbox to show ADV-20260706-018 as the only open advisory.
- Updated Session Handoff and Open Loops with the current state.

### Decision / Lesson

Gemini may be used as an optional Drive artifact-generation fallback or companion when direct Drive connector writes are risky, but Gemini is not a default Life OS dependency and is not a complete in-place Drive record maintainer.

ADV-20260706-018 remains open for Life Logistics review before any advisory-routing architecture change.

## 2026-07-05 — Nightly Sync and Notebook Standard Cleanup

### Summary

Ran Life Logistics nightly GitHub sync after advisory routing cleanup, notebook-leaf standardization, and scheduled-task connector testing notes.

### Findings

- Advisory Index shows no open advisories.
- Department Event Inbox shows no current open/pending events.
- Engineering, Finance, Business, and Main Assistant boards show no open advisories.
- Department Notebook standard now supports notebook hubs, leaf-note folders, and `notebook/README.md` leaf indexes.
- Scheduled-task connector testing has early PASS evidence for Gmail and narrow GitHub read-only retrieval, but execution context varies.

### Completed Work

- Logged scheduled connector test passes in `scheduled-tasks/RUN_LOG.md`.
- Logged scheduled-task execution-context caveat in `scheduled-tasks/ISSUE_LOG.md`.
- Closed notebook-leaf advisories ADV-20260705-014 and ADV-20260705-015 before nightly sync.

### Decision / Lesson

Use notebook leaf files for durable idea capture when a hub would become too large, but maintain a `notebook/README.md` index whenever leaf notes exist. Scheduled workers should read the notebook index before leaf notes when notebook review is requested.

(Older detailed entries are retained in repository history.)
# Advisory Board Review — 2026-07-10

Owner: Life Logistics HQ
Source Advisory: ADV-20260710-031
Purpose: Record the initial review of high-use Life OS advisory boards under the Advisory Board Lifecycle Standard.

## Review Result

| Board | Approx. Lines | Open Advisories | Completed Advisories | Action |
|---|---:|---:|---:|---|
| `coordination/boards/main-assistant.md` | 222 | 0 | 3 | No compaction needed; below practical trigger and still readable |
| `coordination/boards/engineering.md` | 501 | 1 before implementation | 8+ | Compaction justified and completed while closing ADV-20260710-031 |
| `coordination/boards/business.md` | 183 | 0 | 8 | No compaction needed; below trigger and operationally readable |
| `coordination/boards/finance.md` | 94 | 0 | 5 | No compaction needed |
| `coordination/boards/office-leaks.md` | 34 | 0 | 0 | No compaction needed |
| Life Logistics dedicated board | Not present | N/A | N/A | No board created solely for symmetry |

## Engineering Compaction Basis

Engineering exceeded the practical 250–300 line trigger and contained far more completed history than active state.

The compacted board retains:

- every open advisory, with ADV-20260710-031 moved to completed after implementation,
- a bounded recent completed working set,
- durable implementation-report and standard paths,
- source-of-truth and archive rules,
- and Git history as the full prior-text archive.

No open advisory was removed.

## Archive Decision

No separate archive file was created.

Git commit history is sufficient for the current Engineering advisory volume because important completed outcomes are already preserved in standards, implementation reports, handoffs, notebooks, or project records.

## Follow-Up Rule

Future operational board reviews should follow:

- `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`

Do not compact low-traffic boards merely to make them visually symmetrical.

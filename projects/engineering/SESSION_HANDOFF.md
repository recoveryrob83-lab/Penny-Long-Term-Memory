# Engineering_HQ Session Handoff

Updated: 2026-08-01
Project: Engineering_HQ
Purpose: Replacement-chat handoff after LifeOS V2 completed its first successful cross-room production courier proof and added read-only canonical GitHub advisory ingestion.

## Metadata

- Project Owner: Rob
- Primary Chat: `Engineering_HQ`
- Current Phase: Active / LifeOS V2 Operational Core / Bounded Reliability Refinement
- Primary Implementation: `apps/lifeos_dashboardv2`
- Durable Source: GitHub
- Local Runtime: LifeOS V2 server, dashboard, and browser extension
- Sensitivity Level: Moderate

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and every universal-kernel file in the required order.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Perform a separate read-only Sync before implementation writes.
7. Inspect current `main`, the live V2 `/status`, and the local working tree before claiming code or runtime state.
8. Do not edit another department's files without explicit coordinated authority.

## Current Engineering Identity

Engineering owns the LifeOS machinery and technical evidence:

- V2 server and API;
- dashboard implementation;
- browser extension and DOM transport;
- route registry and readiness checks;
- advisory parsing and command reconciliation;
- remote GitHub source synchronization;
- transport state, delivery proof, recovery behavior, tests, and diagnostics.

Engineering does not own advisory lifecycle, another department's source records, shared governance, business judgment, or Rob's final decisions.

## V2 Milestone Reached

The LifeOS V2 outbound courier completed a successful production proof on 2026-08-01.

Proven path:

1. a canonical advisory was parsed into a command;
2. the extension discovered the command before route readiness existed;
3. it selected the registered Maintenance route;
4. it created or reused an owned background courier tab;
5. it navigated to the exact registered conversation URL;
6. it established composer readiness;
7. the server atomically claimed the command through `/begin`;
8. the extension inserted and sent the wake payload;
9. the expected user message was proven in the conversation;
10. the server recorded `DELIVERED`;
11. Maintenance visibly confirmed receipt.

Canonical test evidence:

- `ADV-20260801-055-r1` remains terminal `UNCERTAIN` after the first unresolved post-begin attempt;
- revision 1 was not reset, retried, deleted, requeued, or relabeled;
- `ADV-20260801-055-r2` reached `DELIVERED` after composer/send-proof hardening;
- Maintenance confirmed it read the advisory;
- Rob authorized closure;
- `ADV-20260801-055` is closed in the source board and Advisory Index.

## Repairs Completed During This Session

### Production route dispatch

Removed the global test-arm block from production routes while preserving the arm requirement for `slice_three_test*` routes.

### One owned courier tab

The extension can create one background courier-owned tab and safely reuse it between registered routes. It refuses navigation when it cannot prove the composer is empty.

### Multi-route registry

The extension and popup consume the server's canonical route registry rather than maintaining one local route pair. Engineering and Maintenance routes can coexist.

### Discovery/readiness separation

Command discovery no longer requires a route to be `READY` before the extension knows where to navigate. Discovery requires an unpaused server, an available registered route, a matching `PENDING` command, and attempts remaining. `/begin` remains the atomic readiness gate.

### Composer and delivery proof

The final send path now uses narrow send selectors, application-compatible insertion, bounded send-control waiting, baseline user-message capture, and polling for a newly rendered exact user message. Pre-click failure remains `FAILED`; post-click ambiguity remains terminal `UNCERTAIN`. The injected fallback is self-contained.

## Canonical GitHub Advisory Source

The V2 server now defaults to `REMOTE_GITHUB` and reads:

- repository: `recoveryrob83-lab/Penny-Long-Term-Memory`
- branch: `main`

The source synchronizer:

1. resolves `main` to one commit SHA;
2. fetches `coordination/ADVISORY_INDEX.md` at that SHA;
3. fetches every referenced open-advisory board at the same SHA;
4. parses only after the complete file set is available;
5. caches an unchanged verified snapshot;
6. exposes source mode, source state, verified SHA, and sync timestamps;
7. never runs `git pull`, mutates Rob's working tree, or silently falls back to local files in production.

Fatal source failures remain fail-closed, including GitHub, authentication, network, rate-limit, missing-file, malformed-index, duplicate-reference, ambiguous-source, and decoding failures.

## Advisory-Level Quarantine

The first live remote-source run exposed one legacy open advisory, `ADV-20260726-053`, without a V2 Courier Envelope. The original remote implementation treated that isolated parse defect as a fatal whole-snapshot failure.

A local Engineering repair now separates:

- fatal snapshot-integrity failures, which block dispatch;
- isolated advisory parse defects, which are quarantined.

Local validation reported:

- `sync_state: CURRENT`;
- a non-null verified SHA;
- `ADV-20260728-054` valid;
- `ADV-20260726-053` quarantined at `coordination/boards/engineering.md`;
- the missing V2 Courier Envelope exposed in `advisory_parse_errors`;
- all existing command IDs unchanged.

Important durable-state boundary:

- the core remote synchronizer commit `0eeccc46df6980c62e29795e7f40c78a1d61a108` is on GitHub `main`;
- the current GitHub version of `advisory_source.py` still contains the fatal `if errors: raise SourceSyncError(...)` behavior;
- therefore the advisory-level quarantine repair is locally proven but not yet durable on `origin/main`;
- publishing and verifying that patch is the highest-priority Engineering open loop.

Do not rewrite `ADV-20260726-053` merely to satisfy the parser. Maintenance owns that source record.

## Runtime and Resource Constraints

Rob's PC cannot comfortably keep two active ChatGPT windows open during ordinary daytime work.

Current operating approach:

- the courier tab may be closed while automation is idle;
- bounded nighttime automation may create or reuse one owned background tab;
- the extension must never overwrite a non-empty composer;
- implementation may keep one owned tab open or close it after completion, but must avoid tab sprawl and interference with Rob's active chat.

## Known Remaining Refinements

1. Publish and verify the advisory-quarantine repair on `origin/main`.
2. Display command records newest first without changing dispatch order.
3. Keep active and uncertain records prominent while moving older terminal records into bounded history or retention.
4. Decide and test owned-tab lifecycle around Rob's memory constraint.
5. Deduplicate or rate-limit repeated identical readiness events.
6. Continue the V2 return-path and nighttime-automation work only from explicit scope and current evidence.

## Test Evidence

Reported validation across the session included:

- discovery/readiness focused suite: 21 passed;
- composer/send-proof focused extension suite: 28 passed;
- initial remote-source focused suite: 53 passed;
- quarantine-focused source/courier/API/dashboard suite: 60 passed;
- latest full V2 suite: 70 passed with two known live-connector failures involving an out-of-window calendar fixture and ambient credentials.

Do not describe those two failures as unrelated on faith. Preserve the reported evidence and reproduce against the relevant parent when their classification matters.

## Replacement-Chat First Actions

1. Boot and Sync.
2. Check `git status -sb` in Rob's local repository.
3. Locate the local advisory-quarantine changes.
4. Review their exact diff and test evidence.
5. Commit only the bounded Engineering files if still uncommitted.
6. Rebase safely onto current `origin/main` and push.
7. Read back the pushed implementation through GitHub.
8. Restart the V2 server.
9. Verify `/status` reports `REMOTE_GITHUB`, `CURRENT`, a non-null verified SHA, and one bounded quarantined advisory.
10. Then continue command-history, tab-lifecycle, or telemetry refinement only when Rob chooses the next bounded task.

## Success Standard

A valid advisory committed to canonical GitHub becomes discoverable without Rob pulling the repository, reaches exactly one registered department conversation, never overwrites user text, never blind-retries uncertainty, records understandable state, and leaves one clear recovery path when something fails.

Rob decides. Engineering owns the machinery. Chief of Staff coordinates. Departments own their work and source records. GitHub records durable truth. The dashboard shows rather than governs.
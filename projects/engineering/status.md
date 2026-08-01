# Engineering_HQ Status

Updated: 2026-08-01

## Current Phase

Active / LifeOS V2 Operational Core / Bounded Reliability Refinement

## Department Scope

`Engineering_HQ` owns LifeOS technical architecture, implementation, repository strategy, browser automation, server and API behavior, dashboard behavior, advisory parsing, route handling, command reconciliation, source synchronization, tests, diagnostics, and truthful technical evidence.

Engineering does not own another department's source records, advisory lifecycle, shared governance, business strategy, specialist judgment, or Rob's final decisions.

## Current Operational State

The V2 outbound courier is operational and has completed a successful cross-room production proof to Maintenance HQ.

Verified behavior includes:

- canonical multi-route registration;
- production dispatch without the test arm;
- test-route arm preservation;
- command discovery before route readiness;
- exact-route navigation in an owned background tab;
- empty-composer protection;
- readiness-gated atomic `/begin`;
- hardened composer insertion and send-control selection;
- bounded proof of a newly rendered exact user message;
- terminal `UNCERTAIN` handling without blind resend;
- successful `DELIVERED` acknowledgement.

`ADV-20260801-055-r1` remains immutable `UNCERTAIN` evidence. Revision 2 reached `DELIVERED`, Maintenance confirmed receipt, Rob authorized closure, and the advisory is closed.

## Canonical GitHub Source State

The core read-only canonical GitHub synchronizer is implemented on `main` at:

- `0eeccc46df6980c62e29795e7f40c78a1d61a108`

Production defaults to `REMOTE_GITHUB` and reads `recoveryrob83-lab/Penny-Long-Term-Memory@main` through commit-pinned snapshots.

The synchronizer resolves one SHA, fetches the Advisory Index and all referenced open-advisory boards at that SHA, caches unchanged snapshots, exposes source health and provenance, and never mutates Rob's working tree.

The first live remote run exposed `ADV-20260726-053` as a legacy advisory without a V2 Courier Envelope.

A local repair successfully separates fatal snapshot-integrity failure from advisory-level quarantine. Local validation reported:

- `sync_state: CURRENT`;
- a non-null verified SHA;
- `ADV-20260728-054` valid;
- `ADV-20260726-053` quarantined;
- existing command IDs unchanged.

Current GitHub `main` still contains the earlier fatal whole-snapshot behavior. The quarantine repair remains local-only until committed, pushed, and read back.

## Current Test Evidence

Reported validation:

- discovery/readiness focused tests: 21 passed;
- hardened extension tests: 28 passed;
- remote-source focused tests: 53 passed;
- quarantine-focused source/courier/API/dashboard tests: 60 passed;
- latest full V2 suite: 70 passed with two reported live-connector failures involving a calendar fixture window and ambient credentials.

Those two failures should be treated as reported known failures, not automatically unrelated, unless reproduced against the relevant parent when classification matters.

## Current Resource Constraint

Rob's PC cannot comfortably keep two active ChatGPT windows open during normal work.

The courier-owned tab may be closed while automation is idle. Nighttime automation may create or reuse one background tab. Engineering must prevent tab sprawl and preserve non-empty composers.

## Current Priorities

1. Publish and verify the local advisory-quarantine repair on `origin/main`.
2. Restart the server and confirm `REMOTE_GITHUB`, `CURRENT`, a verified SHA, a valid advisory set, and bounded quarantine reporting from durable code.
3. Sort command display newest first without coupling UI order to dispatch order.
4. Add bounded terminal-command history or retention while preserving active and uncertain evidence.
5. Decide and test courier-tab reuse versus post-delivery closure around Rob's memory constraint.
6. Deduplicate or rate-limit repeated identical readiness events.
7. Continue return-path or nighttime-automation work only under explicit bounded scope.

## Current Boundaries

- Do not rewrite `ADV-20260726-053` merely to satisfy V2 parsing. Maintenance owns that source record.
- Do not reset or retry `UNCERTAIN` commands without explicit authority and evidence.
- Do not let dashboard sorting determine dispatch selection.
- Do not mutate the local Git working tree during production source reads.
- Do not silently fall back from remote source mode to local files.
- Do not edit another department's canonical files without explicit coordinated authority.
- Preserve V1 under `apps/lifeos-dashboard/` as legacy evidence rather than carrying its complexity into V2.

## Definition of Success

A valid advisory committed to canonical GitHub becomes discoverable without a manual pull, reaches exactly one registered department chat, preserves user text, produces truthful delivery state, and leaves one understandable blocker and recovery action when anything fails.

Rob decides. Engineering owns the machinery. Chief of Staff coordinates. Departments own their work and source records.
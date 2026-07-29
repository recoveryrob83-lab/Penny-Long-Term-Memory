# Codex Penny Mission 01: Server and Contracts

- Owning Department: Engineering_HQ
- Execution Surface: Codex Penny / local repository
- Target: `apps/lifeos_dashboardv2`
- Lifecycle State: Ready for execution after Rob launches this mission
- Priority: High
- Verification Mode: IMMEDIATE_HQ
- Stop Condition: Stop after the Slice One acceptance gate. Do not begin dashboard or extension implementation.

## Objective

Build the stable contracts and local server foundation for LifeOS Version Two. Prove advisory-revision detection, route resolution, idempotent command creation, local transport persistence, pause behavior, APIs, logs, and restart safety without requiring the dashboard or browser extension.

## Required Reads

Follow the canonical boot sequence beginning with `memory/STARTUP_BOOT.md`.

Then read:

- `projects/engineering/DEPARTMENT_IDENTITY.md`
- `projects/engineering/README.md`
- `projects/engineering/status.md`
- `projects/engineering/open_loops.md`
- `projects/engineering/notebook/NOTE-20260729-015-lifeos-v2-final-design.md`
- `projects/engineering/notebook/NOTE-20260729-016-lifeos-v2-integration-packet.md`
- `projects/engineering/codex_missions/README.md`

Inspect the existing V1 code only for reusable technical lessons. Do not patch or extend V1.

## Authentication Preflight

Run a bounded Git/GitHub preflight before implementation.

Confirm separately:

1. local Git repository health;
2. remote Git transport;
3. GitHub API read capability.

Attempt no more than one approved credential repair. If remote authentication remains broken, continue locally, commit locally, and report the publication blocker exactly as required by the mission README.

## Scope

Create a coherent Slice One under `apps/lifeos_dashboardv2` containing, as appropriate:

```text
contracts/
server/
config/
tests/
README.md
.env.example
```

Exact module names may differ when a simpler coherent structure is justified.

### Contracts

Implement explicit schemas or typed models for:

- advisory;
- route registry entry;
- delivery command;
- transport state;
- normalized API error and health response where useful.

Advisory contract:

- advisory ID;
- revision;
- source department;
- target department;
- task summary;
- scope;
- state;
- outcome;
- blocker;
- updated time.

Command identity is advisory ID plus revision.

Keep advisory work state separate from transport state.

### Configuration

Provide nonsecret configuration for:

- repository identity;
- canonical Advisory Index path;
- department or Worker route labels;
- persistence location;
- polling interval;
- global pause state;
- logging level;
- runtime GitHub credential environment variable;
- timezone.

Provide `.env.example` with names only. Never commit secrets.

### GitHub Advisory Reader

Implement a bounded configured-path reader that:

- reads the canonical Advisory Index;
- follows only the advisory records required for active entries;
- parses the approved V2 fields;
- detects material revision, state, and outcome changes;
- does not crawl the repository normally;
- preserves source URL and source path;
- handles malformed or missing records without corrupting other work.

Perform one bounded repository-manifest inspection to verify the canonical paths used by the implementation. Save the resulting configuration rather than repeatedly rediscovering it.

### Route Registry

Implement local route storage with:

- route label;
- target department or Worker;
- exact ChatGPT URL;
- registration time;
- last verification time when available;
- route health or availability state.

Do not infer route identity from chat titles.

### Command Creation

The server must:

- create exactly one command for each actionable advisory revision;
- avoid duplicate commands during repeated polling;
- retain the advisory ID and revision;
- preserve target route and exact wake payload;
- expose a clear pending state;
- detect when an advisory revision is no longer actionable;
- never automatically cascade a new dependency.

### Persistence

Use local JSON unless a concrete implementation constraint proves SQLite materially simpler. Document any deviation.

Persistence must survive process restart without duplicating confirmed work.

Persist only transport and configuration state required for safe operation. GitHub remains advisory truth.

### Pause and Resume

Implement one global pause state.

Pause:

- prevents new dispatch-ready work;
- does not rewrite GitHub;
- does not undo confirmed delivery;
- does not build a replay queue.

Resume:

- reconciles from current GitHub truth;
- ignores stale commands that no longer match current actionable revisions.

### API

Expose a small documented local API. The exact framework is Codex's choice if it fits the repository and remains simple.

Expected capabilities include:

```text
GET  /health
GET  /status
GET  /advisories
GET  /advisories/{id}
GET  /routes
POST /routes
DELETE /routes/{route_name}
GET  /commands
GET  /commands/{command_id}
POST /commands/{command_id}/ack
POST /commands/{command_id}/fail
POST /commands/{command_id}/uncertain
POST /system/pause
POST /system/resume
```

Names may change when a more coherent contract is demonstrated. Preserve the capabilities and boundaries.

The command acknowledgement API must not pretend that transport success equals advisory completion.

### Logging

Log enough to diagnose:

- advisory polling;
- revision detection;
- route resolution;
- command creation and deduplication;
- pause suppression;
- acknowledgement, failure, and uncertainty;
- restart recovery.

Redact credentials, authorization headers, prompt secrets, and environment values.

## Required Tests

Use deterministic unit and integration tests with fixtures.

At minimum test:

- valid advisory parsing;
- malformed advisory isolation;
- state and revision change detection;
- cosmetic no-op behavior where distinguishable;
- exactly one command for one advisory revision;
- duplicate polling does not duplicate a command;
- distinct revisions produce distinct command identities;
- unknown route produces a clear blocker;
- command acknowledgement changes transport state only;
- failure and uncertainty are distinct;
- pause prevents new dispatch-ready commands;
- resume reconciles from current GitHub truth;
- restart preserves required state;
- restart after confirmed delivery does not recreate the command;
- stale command suppression;
- secret redaction;
- API validation and understandable errors.

Live GitHub tests must be optional and guarded by explicit environment flags. Most tests should use fixtures.

## Prohibited Work

Do not:

- build dashboard pages;
- build browser-extension files;
- modify V1 runtime code;
- create connector mutations;
- implement assistant-response scraping;
- implement automatic advisory completion;
- implement automatic dependency cascade;
- create V1 send budgets, reset epochs, evidence ledgers, review chains, or parallel business state machines;
- create generalized provider abstractions without a second provider requirement;
- edit Engineering handoff, status, open loops, or shared governance unless separately authorized.

## Slice One Acceptance Gate

The slice passes only when all are demonstrated:

1. A new actionable advisory revision appears in a fixture or controlled test source.
2. The server reads it.
3. The server resolves its registered target route.
4. The server creates exactly one command.
5. Repeated polling does not duplicate that command.
6. Delivery telemetry updates transport state without changing advisory truth.
7. Advisory completion, blocker, or Rob-needed state can be detected.
8. Pause prevents new dispatch-ready work.
9. Resume uses current GitHub truth without replaying stale work.
10. Restart safely preserves required state.
11. Automated tests pass.
12. No dashboard or extension implementation was started.

## Completion Report

Return the standard mission report from `codex_missions/README.md` plus:

- API endpoint summary;
- schema summary;
- persistence choice and rationale;
- exact command-idempotency method;
- exact pause/resume behavior;
- test command and test output summary;
- a short manual reproduction of the acceptance flow;
- any contract questions Engineering must resolve before Mission 02.

Stop after reporting. Do not proceed to Mission 02 without a new explicit instruction from Rob.

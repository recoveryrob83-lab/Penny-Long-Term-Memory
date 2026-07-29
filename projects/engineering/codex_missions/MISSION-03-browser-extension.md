# Codex Penny Mission 03: Browser Extension

- Owning Department: Engineering_HQ
- Execution Surface: Codex Penny / local repository and real browser
- Target: `apps/lifeos_dashboardv2/extension`
- Prerequisites: Missions 01 and 02 accepted by Engineering and Rob
- Lifecycle State: Waiting for explicit resume authorization
- Priority: High
- Verification Mode: IMMEDIATE_HQ
- Stop Condition: Stop after the Slice Three acceptance gate and real-browser evidence. Do not broaden into V1 migration or production rollout.

## Objective

Build the narrow local browser courier that registers exact ChatGPT routes, retrieves one authorized command from the accepted LifeOS server, protects existing composer text, inserts and sends the exact wake once, verifies whether the expected user message appeared, and reports reliable transport state.

The extension transports. It does not interpret advisories, judge work, or own durable state.

## Required Reads

Follow the canonical boot sequence beginning with `memory/STARTUP_BOOT.md`.

Then read:

- `projects/engineering/DEPARTMENT_IDENTITY.md`
- `projects/engineering/README.md`
- `projects/engineering/status.md`
- `projects/engineering/open_loops.md`
- `projects/engineering/notebook/NOTE-20260729-015-lifeos-v2-final-design.md`
- `projects/engineering/notebook/NOTE-20260729-017-dashboard-visual-behavior.md`
- `projects/engineering/codex_missions/README.md`
- `projects/engineering/codex_missions/MISSION-01-server-and-contracts.md`
- `projects/engineering/codex_missions/MISSION-02-dashboard.md`
- accepted completion reports and current code from Missions 01 and 02

Inspect V1 browser-control code only for observed selectors, failure lessons, and test ideas. Do not port V1 orchestration machinery.

## Authentication and Baseline Preflight

Run the bounded Git/GitHub preflight from the mission README. If remote authentication fails, preserve local work and continue locally.

Before editing:

- run the full Slice One and Slice Two test suites;
- verify the local server and dashboard launch successfully;
- verify the extension-facing API contract;
- stop and report if the accepted foundation is broken rather than masking it inside extension code.

## Extension Scope

Build the smallest extension and supporting server/dashboard integration needed for:

1. exact route registration;
2. command retrieval;
3. route and composer preflight;
4. protected insertion;
5. one send effect;
6. delivery verification;
7. transport telemetry;
8. bounded retry;
9. pause and emergency stop;
10. restart-safe handling of confirmed and uncertain sends.

Use the simplest supported browser-extension architecture. Do not introduce a browser automation framework into the production path unless the accepted environment requires it.

## Route Registration

Implement this approved flow:

1. Rob selects an HQ or Worker route from the extension or dashboard-assisted registration surface.
2. Rob opens the intended ChatGPT conversation tab.
3. Rob chooses `Register current tab`.
4. The extension reads the exact current conversation URL.
5. A local confirmation displays the route label and URL.
6. The extension sends the registration to the local server.
7. The Automation dashboard reflects the registered route and current health.

Rules:

- do not infer route identity from the chat title;
- do not silently replace an existing route without clear confirmation;
- do not store authentication secrets in extension storage;
- use exact URLs and configured route labels;
- preserve one authoritative route registry in the local server.

## Command Retrieval

The extension retrieves only commands assigned to the registered route and permitted by current global pause state.

A command must include:

- command identity;
- advisory ID and revision;
- exact target route;
- exact wake text or payload;
- server transport state;
- attempt count and eligibility.

The extension must not read GitHub advisories directly or construct its own task interpretation.

## Preflight and Composer Protection

Before insertion:

- confirm the current tab URL matches the assigned route;
- confirm the ChatGPT page is in a usable state;
- locate the active composer and Send control using bounded selectors;
- detect whether unrelated user text is present;
- fail closed when existing text cannot be safely preserved;
- avoid acting during navigation or page transition;
- avoid duplicate action when the command is already confirmed delivered;
- respect global pause and local emergency stop.

Composer protection is mandatory. Never overwrite, append into, or send unrelated user text.

## Insert and Send

For an eligible command:

1. insert the exact wake text;
2. verify the composer contains the expected text;
3. invoke Send once;
4. do not perform a second Send effect in the same attempt;
5. check for the expected user-authored message in the conversation;
6. report the result to the server.

Do not read assistant response bodies.

Do not infer work completion from UI output.

## Delivery States

At minimum support clear user-facing transport outcomes equivalent to:

- Pending
- Dispatching
- Delivered
- Failed
- Cancelled
- Uncertain

`Delivered` means the expected user message appeared. It does not mean the department completed the advisory.

`Failed` is used when a clearly pre-send failure occurred and the wake was not sent.

`Uncertain` is used whenever the extension cannot prove whether Send occurred or whether the expected user message appeared.

## Retry

- Maximum three command-local attempts.
- Retry only clearly pre-send failures.
- If Send did not occur and the wake is clearly absent, another attempt may be eligible.
- If the expected user message appeared, report Delivered and stop.
- If the result is indeterminate, report Uncertain and stop.
- Never automatically replay an Uncertain command.
- Attempt count belongs to the server's command state and survives restart.

## Pause and Emergency Stop

The extension must fail closed when it cannot read authoritative pause state.

Global pause prevents new dispatches.

A local emergency stop must immediately prevent further extension sends on that browser installation. It does not rewrite GitHub or advisory state.

Resume uses the current server command state and current GitHub-derived truth. It does not replay stale commands.

## Restart Behavior

Test and implement:

- restart before any send attempt;
- restart after clearly pre-send failure;
- restart after confirmed delivery;
- restart after an ambiguous send;
- browser tab closed and reopened;
- route re-registration;
- server restart while extension remains loaded.

Confirmed delivery must not be recreated. Ambiguous send must remain Uncertain and require human review.

## Dashboard Integration

Update the accepted Automation section only as needed to display real extension connection and route health.

The dashboard may show:

- extension connected or disconnected;
- last heartbeat or verification time;
- route registration state;
- command transport result;
- allowed recovery controls.

Do not redesign the dashboard or create a fourth top-level tab.

## Security and Privacy

- no secrets in source, logs, storage, screenshots, or telemetry;
- no assistant-response collection;
- no broad page scraping;
- no browsing-history collection;
- no route inference from titles;
- no prompt-body duplication in diagnostic logs beyond the minimum safe identifier or redacted preview;
- no external network destinations other than the configured local LifeOS server and required browser page behavior;
- document permissions and local installation steps clearly.

## Required Tests

Use unit tests, extension integration tests, and real-browser acceptance.

At minimum test:

- successful route registration;
- confirmation displays exact route and URL;
- route replacement requires clear action;
- assigned-route matching;
- wrong tab or wrong URL fails closed;
- existing composer text is protected;
- empty composer accepts exact wake;
- composer insertion verification;
- Send invoked once;
- expected user message produces Delivered;
- missing Send control before send produces a clear pre-send failure;
- navigation before Send produces pre-send failure or safe stop;
- navigation after possible Send produces Uncertain;
- no expected user message after ambiguous interaction produces Uncertain;
- no automatic replay after Uncertain;
- attempt count maxes at three;
- confirmed delivery survives restart;
- uncertain state survives restart;
- pause blocks dispatch;
- emergency stop blocks dispatch;
- route re-registration restores operation;
- server disconnect fails closed;
- reconnect does not duplicate delivery;
- dashboard reflects connection and delivery state;
- assistant response bodies are never inspected;
- unrelated tabs are ignored.

## Real-Browser Acceptance Sequence

Use one controlled test advisory and one registered test ChatGPT conversation.

Demonstrate:

1. register the test route;
2. server creates one command for one test advisory revision;
3. extension receives that command;
4. extension inserts and sends exactly one test wake;
5. expected user message appears;
6. server receives Delivered;
7. dashboard reflects the result;
8. duplicate polling and extension reconnect do not resend.

Then test:

- composer occupied;
- disconnected route;
- missing Send control;
- navigation before Send;
- restart after confirmed send;
- restart after ambiguous send;
- global pause;
- local emergency stop;
- route re-registration.

Use test data that cannot trigger real department work. Do not wake active production department chats until Rob separately authorizes rollout.

## Prohibited Work

Do not:

- read assistant response bodies;
- parse advisory meaning;
- determine department success;
- update advisory lifecycle;
- route dependencies;
- infer route from chat title;
- overwrite composer text;
- automatically replay uncertainty;
- add universal send budgets or reset epochs;
- restore V1 Worker verification machinery;
- build multi-browser or multi-provider abstractions without a concrete requirement;
- migrate or retire V1 code;
- deploy to a public extension store;
- register production department routes without Rob's separate authorization;
- edit other departments or shared governance.

## Slice Three Acceptance Gate

The slice passes only when:

1. A real registered test conversation receives exactly one test wake from one test advisory revision.
2. The server receives a reliable Delivered result when the expected user message appears.
3. Duplicate polling, reconnect, and restart do not resend confirmed delivery.
4. Existing composer text is never overwritten or accidentally sent.
5. Clearly pre-send failures may retry within the three-attempt limit.
6. Indeterminate outcomes become Uncertain and stop.
7. Uncertain commands are not automatically replayed.
8. Pause and emergency stop block new sends.
9. Route registration and re-registration work with exact URLs.
10. The dashboard displays real extension health and transport state.
11. All Slice One, Slice Two, and Slice Three automated tests pass.
12. Real-browser acceptance evidence is captured without secrets.
13. No production rollout or V1 migration occurred.

## Completion Report

Return the standard mission report plus:

- browser and extension architecture;
- permissions requested and why;
- selector and resilience strategy;
- composer-protection method;
- exact send-verification method;
- retry and uncertainty state diagram;
- restart behavior evidence;
- real-browser acceptance steps and results;
- screenshots or recordings where safe;
- installation and local configuration instructions;
- known browser-version sensitivities;
- recommendation for a separate controlled production-rollout mission.

Stop after reporting. Production route registration, V1 retirement, and rollout require separate explicit authorization.

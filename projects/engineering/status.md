# Engineering_HQ Status

Updated: 2026-07-28

## Current Phase

Active / LifeOS Version Two Design / Simplification First / No Implementation Authorized

## Department Scope

`Engineering_HQ` owns technical architecture, software planning, repository strategy, automation design, testing, debugging, implementation sequencing, build-readiness, and truthful verification.

Engineering does not own another department's judgment, shared governance, source-owner lifecycle, business strategy, or Rob's final decisions.

## Current Direction

Rob has paused further incremental repair of the current LifeOS Worker orchestration system. The V1 system will be preserved as legacy history and later archived rather than carried forward through compatibility layers.

Version Two will be designed around a simple operating loop:

1. Chief of Staff issues or updates one advisory.
2. The server detects the advisory and resolves one owner.
3. A browser plugin delivers the prompt to the registered department chat.
4. The department performs the work and updates the same advisory.
5. The server detects the outcome and notifies Chief of Staff.
6. Chief of Staff reports to Rob or returns a cross-department dependency to Rob.

## Version Two Components

- Browser plugin: narrow transport, route registration, composer protection, one send effect, basic telemetry, three command-local attempts.
- Server: intermediary among GitHub, plugin, and dashboard; advisory watcher; delivery tracker; outcome watcher; Chief of Staff notifier.
- Dashboard: Rob-facing information and control center showing what is happening, what is blocked, and who acts next.
- GitHub: one authoritative advisory plus normal commit, diff, and pull-request history.

## Safeguard Posture

Retain only safeguards that prevent likely failures Rob cannot easily inspect or correct manually.

Default safeguards:

- one advisory;
- one owner;
- registered routes;
- composer protection;
- command-local duplicate suppression;
- no more than three attempts;
- no blind resend after uncertainty;
- simple work, delivery, and route states;
- global pause;
- visible recovery actions;
- direct human override.

Universal send budgets, reset epochs, mandatory HQ review, immutable review chains, default checksums, separate evidence ledgers, automatic cross-department routing, and multiple parallel lifecycle state machines are not part of the normal V2 path.

## Working Design Sources

Google Drive folder: `Life Organization/Chief Engineering Penny`

- `Version Two Safeguards`
- `LifeOS Version Two System Design`

These are working planning documents and are not yet canonical implementation contracts.

## Planned Design Sequence

1. Refine the overall V2 process.
2. Produce Browser Plugin Design.
3. Produce LifeOS V2 Server Design.
4. Produce LifeOS V2 Dashboard Design.
5. Reconcile the documents for consistency and simplicity.
6. Promote approved designs into GitHub.
7. Prepare one comprehensive Codex Penny deliverables prompt.
8. Implement under `apps/lifeos_dashboardv2`.

## V1 Boundary

The current dashboard and Worker orchestration code remain legacy production history. The ADV-053/ADV-054 incident is preserved as design evidence. Do not continue V1 runtime patching, review-attempt repair, send-budget work, or procedural expansion without a separate explicit Rob decision.

## Definition of Success

A normal advisory travels from Chief of Staff to the owning department and back without Rob copying prompts, resetting state, interpreting hidden runtime conditions, or reading implementation details.

A failure produces one understandable blocker and one clear recovery action.

## Boundary

Rob decides. Engineering owns the machinery. Chief of Staff coordinates. Departments own their work and judgment. Simplicity is the primary V2 architectural constraint.

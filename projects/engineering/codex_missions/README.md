# Codex Penny Missions

- Owner: Engineering_HQ
- Purpose: Control Codex Penny implementation scope for LifeOS Version Two.
- Implementation Target: `apps/lifeos_dashboardv2`

## Operating Rule

Codex Penny executes one production slice at a time.

Each mission:

1. boots from the canonical repository rules;
2. reads the approved Engineering design records named in the mission;
3. inspects the current repository before editing;
4. performs only the named slice;
5. runs the required tests;
6. commits locally throughout the work;
7. attempts remote publication only at the mission boundary;
8. stops and reports after the slice acceptance gate;
9. waits for Engineering review and Rob's explicit resume decision before beginning another slice.

Do not interpret the existence of multiple mission files as permission to execute more than one slice in one run.

## Mission Order

1. `MISSION-01-server-and-contracts.md`
2. `MISSION-02-dashboard.md`
3. `MISSION-03-browser-extension.md`
4. `MISSION-04-live-read-connectors.md`

## Canonical Design Inputs

- `projects/engineering/notebook/NOTE-20260729-015-lifeos-v2-final-design.md`
- `projects/engineering/notebook/NOTE-20260729-016-lifeos-v2-integration-packet.md`
- `projects/engineering/notebook/NOTE-20260729-017-dashboard-visual-behavior.md`

The final-design note governs architecture and authority. The integration packet governs connector assumptions and live nonsecret identifiers. The visual-behavior note governs the human-facing dashboard.

## GitHub Authentication Boundary

GitHub transport failure must not destroy or block completed local work.

At the start of each mission, run a bounded preflight appropriate to the environment, such as:

```text
git status
git remote -v
gh auth status
git fetch --dry-run
gh api repos/recoveryrob83-lab/Penny-Long-Term-Memory
```

Codex may attempt one approved credential repair, such as configuring Git to use an existing GitHub CLI login or using the intended SSH setup. Do not spend the mission repeatedly troubleshooting authentication.

If remote authentication still fails:

- continue in the local checkout;
- commit locally;
- preserve the exact branch and commit SHAs;
- report the failed command and full nonsecret error;
- do not claim push or pull succeeded;
- stop at the publication boundary.

Runtime GitHub read authentication is separate from developer push authentication. Runtime credentials must be supplied through environment configuration and never committed.

## Universal Boundaries

- No V1 runtime repair.
- No V1 compatibility layer unless explicitly authorized.
- No edits outside the approved slice unless required to keep the slice coherent and reported explicitly.
- No writes to other departments' canonical records.
- No source-system mutations from Overview or Department Inspector.
- No live secrets in code, tests, logs, fixtures, screenshots, or commits.
- No automatic cross-department cascade.
- No generalized workflow engine, multi-user SaaS architecture, microservices, or speculative platform abstraction.
- No claim of completion without tests and readback evidence.

## Completion Report

Every mission report must state:

- status: completed, partial, or blocked;
- branch and local commit SHAs;
- remote publication status;
- files changed;
- architecture choices made;
- tests run and results;
- manual verification performed;
- known limitations;
- unresolved risks;
- exact acceptance-gate result;
- whether the repository is safe for the next slice.

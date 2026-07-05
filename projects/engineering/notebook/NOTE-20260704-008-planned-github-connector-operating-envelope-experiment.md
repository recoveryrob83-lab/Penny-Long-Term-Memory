# NOTE-20260704-008 — Planned GitHub Connector Operating Envelope Experiment

Date: 2026-07-04 local / 2026-07-05 UTC
Project: Chief Engineering Penny / Engineering HQ
Category: Connector Reliability Test Lab
Connector: GitHub
Status: Planned / Not Yet Executed

## Purpose

Rob and Chief Engineering Penny discussed the need for a controlled GitHub connector reliability experiment to characterize safe write/update behavior without risking production Life OS memory or active coordination files.

The motivating question:

> How small should GitHub connector edits be to reduce safety-trigger risk without requiring dozens of unnecessary calls?

## Current Working Hypothesis

GitHub connector write reliability is likely affected by more than raw payload size.

Likely risk variables include:

- payload size,
- full-file rewrite versus small localized update,
- hub file versus leaf file,
- create versus update,
- repeated writes in a short period,
- content sensitivity or density,
- current connector/session state,
- verification pattern after writes.

This means the answer is probably not a single magic safe-size threshold. Engineering should characterize an operating envelope.

## Sandbox Requirement

GitHub connector stress testing should not occur in production Life OS files.

A dedicated GitHub testing folder should be created before experiments begin, for example:

`projects/engineering/connector-reliability/github-playground/`

The playground should contain only disposable test artifacts.

No active handoffs, advisory boards, operating rules, decision rules, finance files, or production memory files should be used as test targets.

## Chat Isolation Requirement

Rob suggested using a fresh chat for GitHub testing so that if connector write access becomes degraded or blocked during testing, the production Engineering HQ chat is not burdened by the failed connector state.

Engineering agrees this is prudent.

Suggested pattern:

- Production Engineering HQ: records plans, lessons, and final findings.
- Fresh GitHub Test Lab chat: performs deliberate connector stress tests.
- GitHub playground folder: contains all disposable test files.

## Proposed Experiment Families

Do not execute yet. These are planning placeholders.

### Series G-100 — Payload Size

Hold operation type, file type, file location, and cadence constant.

Vary payload size only.

Candidate sizes:

- 100 characters
- 500 characters
- 1 KB
- 2 KB
- 5 KB
- 10 KB

### Series G-200 — Operation Count / Cadence

Hold payload size constant.

Vary number and spacing of writes.

Candidate patterns:

- 1 write
- 2 writes
- 5 writes
- 10 writes
- back-to-back writes
- delayed writes

### Series G-300 — Hub Versus Leaf

Use comparable payloads.

Compare:

- small leaf file create/update,
- hub/index file update,
- pointer-only hub update,
- broad hub rewrite.

### Series G-400 — Create Versus Update

Use comparable payloads.

Compare:

- new file creation,
- existing file update,
- repeated update of same file,
- update after fetch/verify cycle.

## Guardrails

- Use disposable files only.
- Verify each mutation independently.
- Stop after any safety-trigger block.
- Do not retry the same blocked payload immediately.
- Log safety-layer blocks separately from GitHub provider/API failures.
- Log schema errors separately from execution failures.
- Preserve commit hashes and file SHAs where available.
- Do not infer success without read-back verification.
- Do not graduate findings into Life OS standards from a single experiment.

## Planned Output

The eventual experiment plan should define:

- exact experiment IDs,
- target playground folder path,
- files to create,
- payload increments,
- cadence/timing,
- success criteria,
- failure classification,
- verification method,
- stopping rules,
- how findings graduate into Engineering recommendations.

## Current Status

Planning note only.

No GitHub connector stress test has been run from this note.

Rob may later ask Chief Engineering Penny for the GitHub experiment plan based on this notebook entry.

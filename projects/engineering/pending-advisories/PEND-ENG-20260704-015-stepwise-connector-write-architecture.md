# PEND-ENG-20260704-015 — Stepwise connector write architecture

Date captured: 2026-07-04
Status: Pending
Origin: Chief Engineering Penny / Connector Reliability Test Lab observations
Tags: connector reliability, write architecture, safety blocks, verification, Google Drive, GitHub, Reliable Connector Execution Layer

## Core idea

Repeated connector observations support a working rule:

> Break connector writes into small, verified steps. Avoid large batch rewrites unless absolutely necessary.

This should become part of the Reliable Connector Execution Layer architecture.

## Observed pattern

Across GitHub and Google Drive connector work, larger or more complex writes appear riskier than small localized writes.

Observed examples:

- Creating small modular GitHub files usually succeeds.
- Updating smaller files usually succeeds.
- Large or dense hub-file rewrites are more likely to trigger safety blocks or produce operational risk.
- A fuller Advisory Index update was blocked by safety checks, while a smaller pointer-only index update succeeded.
- Google Drive write/create operations appear more sensitive than read-only operations.
- Google Drive read access may remain available after a write/create safety block.

## Architecture implication

The execution layer should not treat external writes as one big action.

Instead, writes should be planned and executed as a sequence of small operations:

```text
Intent -> Risk Check -> Small Write -> Verify -> Next Small Write -> Verify -> Complete
```

If a write is blocked, the system should not blindly retry the same payload. It should reduce complexity, split the write, switch target, or degrade to a manual/export fallback.

## Candidate write-risk ladder

### Low risk

- Create a small leaf file.
- Append or update a small localized section.
- Make a pointer-only index update.
- Perform read-only verification.

Default action: execute and verify.

### Medium risk

- Update a moderately sized file.
- Modify an index plus one detail file.
- Create or update a small Drive artifact.

Default action: split into steps and verify after each step.

### High risk

- Rewrite a large hub file.
- Update multiple files in one conceptual operation.
- Perform many Google Drive writes in a short period.
- Create or modify multiple Drive artifacts.
- Send a dense payload with security-, privacy-, financial-, or connector-adjacent language.

Default action: break apart, stage in GitHub, or ask whether to publish/export later.

### Blocked / degraded

- Safety system blocks the tool call.
- Tool schema error prevents execution.
- Provider operation fails.
- Verification fails.

Default action: stop, classify the failure, simplify the payload, or fall back to RPR/export/manual handoff.

## Proposed Reliable Connector Execution Layer behavior

1. Classify the write target.
2. Estimate write size and complexity.
3. Detect whether the target is a hub file, leaf file, generated artifact, or source file.
4. Prefer leaf-file creation over large hub-file mutation.
5. Prefer pointer/index updates over copying full detail into hubs.
6. Verify every write independently.
7. Stop after a safety block instead of hammering the connector.
8. Record failure class separately:
   - Safety-layer block.
   - Connector schema error.
   - Connector execution failure.
   - Provider/API failure.
   - Verification failure.
   - Partial mutation or state-loss risk.
9. Resume with smaller steps only after reassessing connector state.

## Relationship to source/publication architecture

This note supports the broader Life OS source-of-truth and publication architecture:

- Keep operational state in GitHub when GitHub is the natural authoritative home.
- Use small modular files for durable operational state.
- Publish to Drive only when a human-readable artifact is needed.
- Treat Drive writes as higher-risk and less frequent when possible.

## Current recommendation

Keep this as a pending Engineering advisory until it can be folded into the Reliable Connector Execution Layer design packet.

Potential future standard name:

`Connector Write Planning and Verification Standard`

Draft principle:

> Small verified connector writes are preferred over large unverified connector writes.

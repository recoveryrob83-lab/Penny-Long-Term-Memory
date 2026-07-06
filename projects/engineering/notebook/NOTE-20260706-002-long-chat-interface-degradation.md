# NOTE-20260706-002 — Long Chat Interface Degradation

Date: 2026-07-06
Project: Chief Engineering Penny / Engineering HQ
Type: Operational observation
Status: Active observation

## Summary

Rob observed that very long ChatGPT project chats can become slow, unruly, and less responsive after extended use.

The slowdown may persist even after local device cleanup such as clearing cache files.

## Operational Impact

Long-running HQ chats may become inefficient for active engineering work even when connector state and durable GitHub memory remain intact.

This creates a practical distinction between:

- durable department state, which should live in GitHub; and
- active chat execution context, which can degrade over time.

## Engineering Interpretation

When a chat becomes slow or unwieldy, it should be treated as an interface/session degradation issue rather than a durable-memory failure.

Recommended response:

1. Stop trying to force the overloaded chat to continue.
2. Boot a new Engineering HQ chat from GitHub.
3. Read the standard boot files and Engineering handoff.
4. Continue work from durable repository state.
5. Treat the old chat as archived operational history.

## Design Implication

Life OS should not depend on any one long-lived chat remaining performant indefinitely.

The durable HQ is the repository state plus boot procedure, not the specific chat window.

This supports the broader architecture principle:

- GitHub owns durable state.
- Boot files restore working context.
- Chat windows are replaceable execution surfaces.

## Follow-Up

Consider folding this observation into future boot/sync guidance or Reliable Connector Execution Layer notes if repeated across multiple long-running chats.

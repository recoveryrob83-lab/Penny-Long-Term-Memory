# NOTE-20260706-003 — Finances Connector Session Isolation Hypothesis

Date: 2026-07-06
Project: Chief Engineering Penny / Engineering HQ
Type: Connector reliability observation / hypothesis
Status: Active observation
Related Advisory: ADV-20260706-019

## Summary

Rob strongly suspects that the Finances connector may use special session isolation behavior to protect financial data from leakage.

Working hypothesis:

- A chat session may be allowed to own the Finances connector context.
- Other connectors may be disabled, degraded, or isolated while that financial connector context is active.
- This could be intentional safety behavior designed to prevent financial data from leaking across unrelated connector workflows.

## Important Caveat

This is a hypothesis from field observation, not a confirmed platform fact.

Engineering should treat it as a test candidate under Reliable Connector Execution Layer research, not as established behavior.

## Observed Context

ADV-20260706-019 reports connector instability after a Finance chat attempted to load the Finances/Plaid account-linking path. Rob observed that unrelated connectors appeared to degrade after the Finances attempt.

## Engineering Implication

If the hypothesis is correct, Finances may need a stricter operating model than ordinary connectors:

- Use a fresh Finance-specific chat for Finances work.
- Avoid mixing Finances with unrelated connector operations in the same session.
- Do not assume connectors remain available after entering a financial account-linking context.
- Keep GitHub notes abstract and non-sensitive.
- Treat Finances/Plaid flows as high-sensitivity connector operations.

## Test Design Direction

Any future test should be controlled, explicit, and non-sensitive unless Rob separately authorizes live financial-data access.

Potential abstract checks:

1. Does invoking Finances affect subsequent harmless reads from unrelated connectors?
2. Does a fresh Finance-booted chat behave differently from a long-running mixed-purpose chat?
3. Does explicit connector invocation reduce routing confusion?
4. Does account-linking behavior differ from read-only financial query behavior?
5. Does connector availability recover after starting a new chat?

## Safety Guardrail

Do not record account names, balances, transactions, credentials, Plaid details, benefit identifiers, or financial documents in GitHub.

Use only abstract test notes unless Rob explicitly authorizes a controlled Finances connector test in an appropriate Finance context.

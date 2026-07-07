# Connector Reliability Operating Pattern

Updated: 2026-07-06
Purpose: Durable Life OS operating pattern for connector-heavy work and fallback workflows.

## Status

Adopted from ADV-20260706-017 and extended by ADV-20260706-020.

## Core Pattern

Use explicit connector invocation, small verified writes, and fallback workers when direct connector work becomes fragile.

Treat high-sensitivity financial connector sessions as isolated unless later testing proves otherwise.

## Rules

1. Explicitly invoke the intended connector before meaningful connector work when practical.
2. Prefer small, localized, verified GitHub writes over broad hub rewrites.
3. If a write safety trigger occurs, stop and wait before retrying. Do not hammer the same blocked operation.
4. For Drive artifacts with sensitive-field wording or private/medical/benefits-style structure, consider a Gemini handoff for artifact generation or versioned update.
5. Use Penny / ChatGPT for orchestration, prompt design, GitHub state, audit, advisory routing, and Drive file placement when connector-safe.
6. Treat Gemini as an optional Google Workspace artifact generator, not a default Life OS dependency and not a complete in-place Drive record maintainer.
7. Keep GitHub records abstract. Store detailed working records in Drive.
8. Treat generated Drive artifacts as unverified until Rob or Penny checks the result.
9. Treat Finances connector work as Finance-only session work. Do not mix Finances/Plaid-style operations with GitHub, Drive, Gmail, Instacart, or other connector workflows in the same active session.
10. After Finances is invoked, do not assume other connectors remain available. Complete Finances work first, then use a separate GitHub-capable or general-purpose session for documentation and follow-up.

## Finances-Only Session Pattern

Observed Life OS operating pattern:

Treat Finances sessions as connector-isolated until demonstrated otherwise.

Recommended workflow:

1. Finance chat performs Finances-only work.
2. Finance reports an abstract result to Rob.
3. Engineering, Logistics, or Finance records abstract GitHub notes later from a separate GitHub-capable chat if needed.
4. No financial account names, balances, transactions, credentials, Plaid details, benefit identifiers, or financial documents should be recorded in GitHub.

This is an observed operating pattern, not a confirmed claim about platform internals.

## Division of Labor

- Penny / ChatGPT: planning, prompt design, GitHub state, audit, routing, connector-safe file placement, verification.
- Gemini: optional Google Workspace artifact generation or versioned update when direct Drive writes are risky.
- Finance chat: Finances-only connector work and abstract reporting to Rob.
- Rob: manual verification and manual placement or replacement when tool limitations require it.
- GitHub: abstract operational memory.
- Drive: detailed working records and artifacts.
- Finances connector: high-sensitivity financial activity and account-linked analysis when Rob requests it.

## Reliability Note

This pattern does not mean connector issues are solved. It is a risk-reduction pattern based on observed Life OS connector behavior.
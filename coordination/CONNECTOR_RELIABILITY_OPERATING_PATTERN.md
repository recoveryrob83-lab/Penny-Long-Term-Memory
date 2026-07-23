# Connector Reliability Operating Pattern

Updated: 2026-07-18
Purpose: Durable LifeOS operating pattern for connector-heavy work, verified-write behavior, and fallback workflows.

## Status

Adopted from ADV-20260706-017, extended by ADV-20260706-020, and extended with the Trello false-negative write protocol from ADV-20260718-041.

## Core Pattern

Use explicit connector invocation, small verified writes, and fallback workers when direct connector work becomes fragile.

Treat a connector receipt as evidence about the call, not always conclusive evidence about the live source-system state. When a response is ambiguous, verify the live destination before retrying or reporting failure.

Treat high-sensitivity financial connector sessions as isolated unless later testing proves otherwise.

## General Rules

1. Explicitly invoke the intended connector before meaningful connector work when practical.
2. Prefer small, localized, independently verifiable writes over broad multi-part payloads.
3. If a write safety trigger occurs, stop before retrying. Do not hammer the same blocked operation.
4. Treat an error response as inconclusive when observed connector behavior shows that delayed success or a false negative is possible.
5. After an ambiguous response, read the live authoritative destination before retrying, replacing, duplicating, or reporting failure.
6. Report the verified live state, distinguishing it from the connector receipt when they disagree.
7. Prevent duplicate writes by checking whether the intended object already exists before a retry.
8. Preserve the source system's authority and do not let connector convenience create duplicate truth elsewhere.
9. For Drive artifacts with sensitive-field wording or private, medical, or benefits-style structure, consider a Gemini handoff for artifact generation or versioned update.
10. Use Penny / ChatGPT for orchestration, prompt design, GitHub state, audit, advisory routing, and Drive file placement when connector-safe.
11. Treat Gemini as an optional Google Workspace artifact generator, not a default LifeOS dependency and not a complete in-place Drive record maintainer.
12. Keep GitHub records abstract. Store detailed working records in their natural source systems.
13. Treat generated Drive artifacts as unverified until Rob or Penny checks the result.
14. Treat Finances connector work as Finance-only session work. Do not mix Finances or Plaid-style operations with GitHub, Drive, Gmail, Instacart, or other connector workflows in the same active session.
15. After Finances is invoked, do not assume other connectors remain available. Complete Finances work first, then use a separate GitHub-capable or general-purpose session for documentation and follow-up.

## Trello Connector Write Protocol

This protocol applies to every LifeOS room or department authorized to perform Trello writes.

### Observed Reliability Boundary

During a verified LifeOS capture session:

- basic Inbox card creation succeeded;
- checklist creation succeeded;
- checklist-item calls returned workspace-permission errors;
- delayed live read-back showed that the requested checklist items had actually been created;
- fourteen additional checklist items were submitted through fourteen separate calls;
- every call returned the same misleading error;
- final live read-back confirmed all sixteen intended checklist items across eight checklist groups.

This is an observed operating pattern, not a confirmed statement about Trello or connector platform internals. The demonstrated false-negative risk is concentrated in checklist-item writes and may affect some update paths. Basic card creation was separately tested and succeeded.

### Required Write Pattern

1. Prefer one small Trello mutation per connector call.
2. For checklist population, submit exactly one checklist item per connector call.
3. Do not combine several checklist items into one large payload merely to reduce call count.
4. Record the intended card, checklist, item text, and target position before the write when duplicate risk matters.
5. Treat a permission, workspace, timeout, or similar error as ambiguous when the requested mutation could have landed after a delay.
6. After any ambiguous Trello write response, perform a live read-back of the authoritative card, checklist, list, or Inbox state.
7. Do not retry until read-back confirms the original write did not land.
8. If read-back confirms success, report success with a note that the connector receipt was misleading.
9. If read-back confirms absence, retry only the smallest missing mutation and verify again.
10. If live read-back is unavailable, stop and report the state as unverified rather than guessing or issuing duplicate writes.

### Duplicate Prevention

Before creating or retrying a Trello object, check the relevant live scope for:

- an existing card with the intended purpose;
- an existing checklist with the intended title;
- an existing checklist item with the intended text;
- an existing update that already produced the desired state.

Do not create a second card, checklist, or checklist item merely because the connector returned an error. A failed-looking receipt does not authorize duplication.

### Truthful Reporting

When the receipt and live Trello state disagree, report both facts clearly:

- what the connector returned;
- what the live read-back verified;
- whether any retry occurred;
- whether duplicate prevention was applied;
- what remains unverified, if anything.

The verified live Trello state is the operational truth. Do not report a write as failed solely from an ambiguous connector receipt when read-back proves it succeeded.

### Source-System Boundary

Trello remains the LifeOS capture, possibility, attention, and flow layer.

This protocol authorizes safer Trello writes only. It does not authorize:

- promotion of raw ideas into durable GitHub state;
- creation of Todoist commitments or reminders;
- creation of Calendar events;
- conversion of Trello cards into department open loops;
- duplication of detailed authoritative records from Drive, GitHub, Gmail, Calendar, Todoist, or another system.

Any downstream promotion or commitment must pass its own ownership, durable-write, and authorization rules.

## Finances-Only Session Pattern

Observed LifeOS operating pattern:

Treat Finances sessions as connector-isolated until demonstrated otherwise.

Recommended workflow:

1. Finance chat performs Finances-only work.
2. Finance reports an abstract result to Rob.
3. `Engineering_HQ`, `Maintenance_HQ`, or `Finance_HQ` records abstract GitHub notes later from a separate GitHub-capable chat if needed.
4. No financial account names, balances, transactions, credentials, Plaid details, benefit identifiers, or financial documents should be recorded in GitHub.

This is an observed operating pattern, not a confirmed claim about platform internals.

## Division of Labor

- Penny / ChatGPT: planning, prompt design, GitHub state, audit, routing, connector-safe file placement, verification, and truthful live-state reporting.
- Gemini: optional Google Workspace artifact generation or versioned update when direct Drive writes are risky.
- Finance chat: Finances-only connector work and abstract reporting to Rob.
- `Maintenance_HQ`: global connector operating rules, source-boundary protection, and cross-system reconciliation.
- `Engineering_HQ`: connector architecture, compensating mechanisms, reliability tooling, and technical investigation when separately authorized.
- Rob: final authority and manual verification or placement when tool limitations require it.
- GitHub: abstract operational memory.
- Drive: detailed working records and artifacts.
- Trello: capture, possibility, attention, and flow.
- Finances connector: high-sensitivity financial activity and account-linked analysis when Rob requests it.

## Reliability Note

This pattern does not mean connector issues are solved. It is a risk-reduction pattern based on observed LifeOS connector behavior, mandatory live verification, and disciplined duplicate prevention.
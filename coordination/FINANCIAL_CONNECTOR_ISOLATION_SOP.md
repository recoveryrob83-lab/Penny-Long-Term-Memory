# Financial Connector Isolation SOP

Updated: 2026-07-16
Owner: Main Assistant / LifeOS Coordination Hub and Chief of Finance Penny
Purpose: Prevent account-linked financial connector activation from disabling or destabilizing other connectors in a multi-connector chat.

## Hard Operational Rule

The account-linked financial connector must never be invoked in the LifeOS Hub, Main Assistant, or any chat intended to retain access to GitHub, Google Drive, Todoist, Google Calendar, Google Contacts, Gmail, Trello, or other operational connectors.

Do not touch the financial connector in those chats.

“Touch” includes:

- invoking any financial connector action;
- checking its profile, connection, account status, or capabilities;
- including it in connector-health or operational-state checks;
- testing whether it is available;
- calling it as part of “touch all connectors,” “activate all connectors,” or similar requests;
- invoking it merely to confirm that it will not be used;
- using it for a small, read-only, or apparently harmless query.

## Reason

Current observed platform behavior indicates that invoking the financial connector can trigger security isolation that deactivates or makes other connectors unavailable in the current chat. Until that behavior is proven resolved, treat financial connector activation as irreversible for the affected chat.

## Allowed Use

The financial connector may be used only in a deliberately created, dedicated Finance-only chat where:

1. Rob explicitly intends to perform account-linked financial work.
2. Loss of access to other connectors in that chat is acceptable.
3. No Hub, cross-department, or multi-connector workflow is in progress.
4. Sensitive results remain in the dedicated Finance context and are not copied into GitHub.
5. Only abstract conclusions, decisions, or non-sensitive status are later carried back into a GitHub-capable or Hub chat.

## Hub Procedure

In the LifeOS Hub or Main Assistant chat:

1. Exclude the financial connector from every connector activation or health-check sequence.
2. Finance may still provide reasoning from user-supplied information, approved Drive records, Gmail evidence, Todoist, Calendar, and abstract GitHub context.
3. When account-linked data is required, stop before invoking the connector.
4. Tell Rob that the request must be handled in a dedicated Finance-only chat.
5. Continue using the remaining connectors normally.

## Finance Procedure

In an ordinary Finance HQ chat:

1. Do not assume the financial connector is safe to invoke merely because the department is Finance.
2. First determine whether the current chat also needs GitHub, Drive, Gmail, Todoist, Calendar, Trello, Contacts, or cross-department coordination.
3. If any of those are needed, do not invoke the financial connector.
4. Route account-linked work to a separate Finance-only chat.
5. Use the dedicated Finance-only chat solely for account-linked analysis.
6. Return only the minimum necessary abstract conclusions to the operational chat.

## Accidental Activation Recovery

If the financial connector is invoked accidentally in an operational chat:

1. Stop additional connector work in that chat.
2. Do not repeatedly test disabled connectors.
3. Tell Rob which connector was invoked and that the chat may now be security-isolated.
4. Create or move to a fresh Hub or department chat.
5. Reboot from GitHub and reconnect only the approved non-financial connectors.
6. Carry forward only the minimum required non-sensitive context.

## Override Standard

This rule may be changed only by an explicit new instruction from Rob that specifically acknowledges the connector-isolation risk. Generic requests to touch, test, activate, or report on all connectors do not override this SOP.

## Canonical References

- `projects/main-assistant/SESSION_HANDOFF.md`
- `projects/finance-benefits/SESSION_HANDOFF.md`
- `memory/STARTUP_BOOT.md`
- `memory/03_OPERATIONAL_RULES.md`

Until the platform behavior is verified as fixed, safety beats convenience: keep the financial connector quarantined from operational chats.
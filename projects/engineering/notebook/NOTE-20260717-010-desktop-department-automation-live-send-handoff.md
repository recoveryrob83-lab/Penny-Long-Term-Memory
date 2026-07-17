# Desktop Department Automation Live-Send Handoff

Date: 2026-07-17
Status: Completed and validated
Owner: Engineering HQ

## Outcome

The Windows ChatGPT Classic department-boot automation is operational.

Rob completed repeated watched draft-mode tests across all seven LifeOS departments, including:

- chats visible in the sidebar;
- Logistics HQ hidden behind `Show more`;
- empty composers;
- occupied composers;
- canonical prompt insertion;
- clipboard round-trip verification;
- preservation of existing draft text.

All seven departments passed.

Rob then completed a watched live-send test to Main Assistant HQ. The engine navigated to the exact chat, verified the exact destination title, resolved a stable Group composer, wrote and clipboard-verified the canonical prompt, applied the explicit send policy, and submitted exactly once. Main Assistant began rebooting successfully.

## Canonical implementation

Primary launcher:

- `apps/lifeos-dashboard/automation/draft_department_boot.py`

Production engine:

- `apps/lifeos-dashboard/automation/open_department_chat_group.py`

Verification shim:

- `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`

Legacy rollback reference:

- `apps/lifeos-dashboard/automation/open_department_chat.py`

## Durable lessons

The complete architecture, debugging history, safety contract, diagnostic ladder, branching model, validation record, and future UI-recovery playbook are documented in:

- `projects/engineering/notebook/NOTE-20260717-011-chatgpt-ui-automation-lessons-and-recovery-playbook.md`

Read that note before changing selectors, verification rules, navigation recovery, draft policy, or send behavior.

## Current safety contract

- draft-only by default;
- `--send` required for submission;
- exact chat-link matching;
- one bounded `Show more` expansion;
- exact active-document verification;
- bounded retry only for the known generic `ChatGPT` loading state;
- stable Group composer readiness;
- existing-draft preservation;
- clipboard round-trip verification;
- exact non-whitespace content matching with only the demonstrated leading `@GitHub` mention transform accepted;
- one submission only after all gates pass;
- stop on uncertainty.

## Accepted connector limitation

The automation cannot independently prove that GitHub remains active as a connector in the target chat. This is accepted as a rare, visible, recoverable soft failure. Do not add fragile connector-pill automation without repeated evidence that it is necessary.

## Operational commands

Draft test:

```cmd
python automation\draft_department_boot.py wellness
```

Live send:

```cmd
python automation\draft_department_boot.py main --send
```

## Future change policy

After any ChatGPT desktop UI update or selector change:

1. run the diagnostic ladder documented in NOTE-011;
2. patch only demonstrated deterministic transforms or selectors;
3. rerun draft-only tests;
4. complete a watched live-send test before declaring the path restored;
5. never loosen verification through arbitrary fuzzy tolerance.

## Closure

The original handoff existed because the first live test stopped safely during a loading failure. That branch, the modern Group composer, accessibility clipboard transforms, hidden-sidebar navigation, draft preservation, and guarded live sending have now all been resolved and validated.
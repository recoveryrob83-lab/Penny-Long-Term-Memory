# ChatGPT UI Automation Lessons and Recovery Playbook

Date: 2026-07-17
Status: Validated in production-like watched testing
Owner: Engineering HQ
Scope: Windows ChatGPT Classic desktop automation for LifeOS department boot prompts

## Executive summary

The LifeOS department boot engine is now validated end to end across all seven departments.

Verified behaviors:

- exact project-chat navigation;
- one bounded `Show more` sidebar expansion when the target chat is hidden;
- exact destination-title verification;
- bounded recovery from the generic `ChatGPT` loading state;
- stable modern `Group` composer discovery;
- preservation of existing composer text;
- canonical prompt insertion;
- clipboard round-trip verification despite UI presentation transforms;
- draft-only operation by default;
- explicit guarded live send through `--send`;
- successful live submission to Main Assistant HQ.

The engine was tested repeatedly with empty and occupied composers across:

- Engineering HQ
- Logistics HQ
- Wellness HQ
- Finance HQ
- Main Assistant HQ
- Business HQ
- Office Leaks HQ

All seven draft-mode tests succeeded. A watched Main Assistant live-send test also succeeded.

## Production entrypoint

Primary launcher:

- `apps/lifeos-dashboard/automation/draft_department_boot.py`

Production automation engine:

- `apps/lifeos-dashboard/automation/open_department_chat_group.py`

Verification shim:

- `apps/lifeos-dashboard/automation/open_department_chat_group_verified.py`

Legacy rollback engine:

- `apps/lifeos-dashboard/automation/open_department_chat.py`

The legacy Edit-control implementation is intentionally preserved as a diagnostic and rollback reference. It is not the current production path.

## Current operating contract

### Draft mode

Draft mode is the default.

Example:

```cmd
python automation\draft_department_boot.py wellness
```

Expected successful ending:

```text
Draft placed and clipboard-verified. Nothing sent.
```

### Send mode

Live send requires explicit authorization:

```cmd
python automation\draft_department_boot.py main --send
```

Expected successful ending:

```text
Message submitted after explicit confirmation and clipboard verification.
```

`--send` must never become the default.

## Safety contract

The engine follows refusal-first automation rules:

1. Select only the exact configured chat target.
2. Verify the exact active document title before touching the composer.
3. Retry only the known generic loading state, and only within a bounded path.
4. Require a visible, enabled, stable composer.
5. Preserve any existing draft rather than silently replacing it.
6. Verify the resulting prompt through clipboard round-trip before send.
7. Require explicit `--send` authorization for submission.
8. Stop on uncertainty rather than guessing.
9. Never use fuzzy chat-title matching.
10. Never repeatedly hammer `Show more`, navigation, or Send.

## Navigation lessons

### Exact sidebar links are the safest anchor

LifeOS department chats are selected through exact accessible chat-link names. Exact matching prevents similarly named chats from receiving prompts.

### Hidden chats require bounded sidebar expansion

A target can be absent from the visible accessibility tree because ChatGPT places older chats behind `Show more`.

Validated recovery branch:

1. search for the exact chat link;
2. when absent, locate the visible `Show more` button;
3. invoke it exactly once;
4. wait briefly for the exact target link to appear;
5. navigate only after exact resolution;
6. stop if the target remains unavailable.

This branch successfully resolved Logistics HQ on the first live test.

Do not replace it with scrolling roulette or fuzzy matching.

### Generic `ChatGPT` title is a loading state, not a valid destination

During slow loads, the target navigation can be invoked while the active document remains titled only `ChatGPT`.

This is not permission to proceed. The engine performs a bounded loading-state retry and rechecks the exact document title.

Any unexpected title still causes a safe stop.

## Composer discovery lessons

### The modern composer is a `Group`, not an `Edit` control

Initial automation assumed a standard UI Automation `Edit` control. Current ChatGPT Classic exposes the composer as a large `Group` containing child `Text` controls.

Evidence from the UI tree:

- composer rectangle approximately `(1067,543,1570,832)` during testing;
- persistent child control `composer-plus-btn`;
- `composer-submit-button` appears only when text exists;
- no useful writable `Edit` control is exposed.

Therefore the production engine anchors composer discovery on the persistent plus button and resolves its enclosing Group.

### Do not anchor readiness on Send

The Send button disappears when the composer is empty. It cannot serve as a universal composer locator.

The persistent `composer-plus-btn` is the stronger anchor.

### Readiness must be stable, not momentary

The composer must remain visible and enabled across repeated checks before writing. A single transient observation is not enough during animated loading or rerendering.

## Writing lessons

### Clipboard paste is more reliable than UIA value assignment

Direct UI Automation value reads and writes were unreliable because the Group composer does not expose a conventional editable value.

The successful path focuses the composer and uses normal clipboard paste behavior.

### Existing drafts must be preserved

Testing covered both empty and occupied composers. The engine correctly refused to overwrite existing text without explicit replacement authorization.

This is an essential safety property, not a convenience feature.

## Verification lessons

### Visible text is not necessarily readable through UIA

Earlier verification attempts reported zero characters even while the full prompt was visibly present. UIA value comparison was therefore not trustworthy.

The successful verification method is a clipboard round-trip:

1. preserve the user's clipboard;
2. focus the composer;
3. select all composer content;
4. copy it;
5. compare the copied text with the canonical prompt;
6. restore the original clipboard;
7. collapse the selection safely;
8. permit send only after verification passes.

### Accessibility copy can transform presentation without changing content

The canonical Wellness prompt normalized to 1323 characters, while copied composer content normalized to 1355 characters.

The diagnostic result was:

- similarity ratio: `0.987304`;
- equal: 1322;
- replace: 0;
- delete: 1;
- insert: 33.

The two deterministic transforms were:

1. the leading literal `@GitHub` became an accessible GitHub mention whose copied representation omitted only the leading `@`;
2. paragraph boundaries gained additional newline characters.

Every other non-whitespace character matched in order.

### Verification rule

The production verifier:

- removes whitespace for comparison;
- preserves every non-whitespace character exactly and in order;
- accepts exact equality;
- additionally accepts only the known leading `@GitHub` to `GitHub` mention transform;
- rejects all other deletions, insertions, substitutions, or reorderings.

This is strict semantic verification, not fuzzy tolerance.

## Connector limitation

Automation can verify the text and the accessible GitHub mention transformation, but it cannot independently prove that the GitHub connector remains active in the target chat context.

Accepted operating assumption:

- GitHub is routinely active in all department chats;
- a cold or stale chat could rarely fail to resolve the connector;
- this soft failure is visible and recoverable by manually invoking GitHub and sending `retry`.

This limitation is accepted and is not a blocker.

Do not build fragile connector-pill automation unless repeated evidence shows it is necessary.

## Diagnostic ladder for future UI changes

When a future ChatGPT update breaks the engine, diagnose from the outside inward. Do not immediately loosen matching rules.

### 1. Confirm destination behavior

Check:

- exact chat link name;
- whether the chat is hidden behind `Show more`;
- active document title;
- whether the generic `ChatGPT` loading title persists.

### 2. Inspect the bottom UI tree

Use:

- `probe_bottom_controls.py`

Purpose:

- identify current control types;
- inspect accessible names and automation IDs;
- confirm whether the composer remains a Group;
- find persistent child anchors.

### 3. Test read access without writing

Use:

- `probe_composer_group_clipboard.py`

Purpose:

- resolve the Group composer;
- copy existing text;
- confirm clipboard visibility;
- avoid modifying or sending content.

### 4. Test isolated safe writing

Use:

- `probe_composer_group_write.py`

Purpose:

- write a small known string;
- verify it through clipboard copy;
- send nothing.

Run only with an empty composer.

### 5. Diagnose canonical prompt differences

Use:

- `diagnose_group_prompt_diff.py <department>`

Purpose:

- compare expected and observed normalized content;
- report similarity and SequenceMatcher opcode totals;
- print localized mismatch windows;
- modify nothing and send nothing.

### 6. Patch only demonstrated transforms

Accept a new transform only when diagnostics prove it is deterministic, narrow, and content-preserving.

Good examples:

- extra whitespace;
- a known accessible mention representation;
- a stable punctuation normalization with exact evidence.

Bad responses:

- increasing arbitrary fuzzy-match tolerance;
- accepting prefixes or suffixes alone;
- ignoring reordered content;
- permitting unknown substitutions;
- sending because the text looks visually close.

## Branching model

The working architecture now covers these branches:

### Chat visibility

- exact link visible: navigate directly;
- exact link hidden: invoke `Show more` once, then resolve exactly;
- still absent: stop.

### Destination state

- exact title active: proceed;
- generic `ChatGPT` loading title: perform bounded retry;
- any other title: stop.

### Composer state

- stable Group composer found: proceed;
- composer unstable, hidden, disabled, or absent: stop.

### Draft state

- empty composer: write canonical prompt;
- occupied composer without replacement authorization: preserve and stop;
- explicitly authorized replacement path: apply only under the engine's guarded policy.

### Verification state

- exact content match: proceed;
- known whitespace and leading mention transform only: proceed;
- any unexplained character difference: stop and diagnose.

### Send state

- draft mode: leave verified text in place;
- explicit `--send`: submit once after all gates pass;
- no explicit send authorization: never submit.

## Validation record

On 2026-07-17 Rob performed repeated watched tests across all seven LifeOS departments.

Coverage included:

- chats visible in the sidebar;
- a chat hidden behind `Show more`;
- empty composers;
- occupied composers;
- full canonical prompt writes;
- clipboard verification;
- draft-only operation.

All draft tests succeeded.

Rob then ran a watched live-send test for Main Assistant HQ. The observed output confirmed:

```text
SEND MODE: connector resolution is not verified; this relies on GitHub remaining active in the target chat context.
1. Finding window: ChatGPT Classic
2. Resolving exact chat: Main Assistant HQ, chat in project Life OS
   Navigation invoked.
3. Verifying destination: Life OS - Main Assistant HQ
   Verified active document: Life OS - Main Assistant HQ
4. Waiting for a stable, enabled Group composer
   Composer readiness verified.
5. Applying draft policy and clipboard-verifying the write
6. Applying send policy
Message submitted after explicit confirmation and clipboard verification.
```

Main Assistant began rebooting successfully after submission.

## Important commit trail

Key commits from the completed debugging arc:

- `07ceac6d1b386e27b75b77b984e54d06d68f35b7` — bottom UI-tree probe;
- `34f2f99661874448f1d78ec2c9f9aeb3386d78ea` — bounded loading retry in Group clipboard probe;
- `55c78beb34b0f9aadd285a71d4a25e31f8ba30c4` — safe Group write probe;
- `4e2ef38e8c3932505944b787472262fedbaacf63` — persistent plus-button Group anchor;
- `f9be11a8c11db7e21954b98f56bb95174b643282` — Group-based production engine;
- `95d301429d72fe464af2e6881f31ca02191dbb8b` — launcher routed to Group engine;
- `1ce32d1d11fd648570a604618afca6260ea3980b` — prompt-difference diagnostic;
- `11c992dca88b6e57a6ec9426bf0c4971f240ea45` — strict verifier for whitespace and leading GitHub mention transform;
- `db7cea9182b78f269b90552be26926a9abfb79ef` — one bounded `Show more` expansion branch.

## Maintenance guidance

- Expect UI automation to be brittle at the control-discovery layer.
- Keep policy and safety gates separate from UI selectors whenever possible.
- Preserve diagnostic probes even after production success.
- Prefer exact accessible names and stable automation IDs.
- Treat UI copy transforms as data to characterize, not reasons to weaken verification.
- Make one bounded recovery attempt for known states, then stop.
- Keep watched testing after any ChatGPT desktop update.
- Re-run draft-only tests before the next live send whenever selectors or verification rules change.
- Never claim a UI path is fixed until Rob runs it on the actual Windows client.

## Current conclusion

The engine is operational and validated. The important achievement is larger than one working selector: Engineering now has a repeatable pattern for discovering the accessibility tree, isolating navigation and composer failures, proving clipboard transformations, preserving user state, and adding bounded recovery branches without sacrificing send safety.

# Desktop Department Automation Live-Send Handoff

Date: 2026-07-17
Status: Paused after guarded Wellness load failure
Owner: Engineering HQ

## Purpose

Preserve the exact state of the Windows desktop department-boot automation before moving Engineering into a fresh chat window due to increasing ChatGPT Classic lag and repeated loading spinner behavior.

## Current objective

Automate a complete LifeOS department boot in ChatGPT Classic on Windows:

1. focus the ChatGPT Classic window;
2. select the exact department chat inside the `Life OS` project;
3. verify the active document title;
4. wait for a stable, visible, enabled composer;
5. insert the canonical department boot prompt;
6. verify that the intended prompt is actually present;
7. submit only through explicit send mode.

## Canonical HQ names

The active chat titles are standardized as:

- `LifeOS HQ` — central hub;
- `Engineering HQ`;
- `Logistics HQ`;
- `Wellness HQ`;
- `Finance HQ`;
- `Main Assistant HQ`;
- `Business HQ`;
- `Office Leaks HQ`.

Canonical naming file:

- `memory/HQ_NAMING_STANDARD.md`

## Primary scripts

### Generic UI automation engine

- `apps/lifeos-dashboard/automation/open_department_chat.py`

Responsibilities:

- exact sidebar hyperlink selection through Windows UI Automation;
- active document verification;
- stable composer readiness checks;
- existing-draft preservation unless replacement is explicitly authorized;
- write verification;
- explicit send confirmation;
- safe stopping on uncertainty.

### Department launcher

- `apps/lifeos-dashboard/automation/draft_department_boot.py`

Responsibilities:

- maps department keys to exact standardized chat titles;
- builds the canonical boot prompt for each department;
- remains draft-only by default;
- accepts `--send` to pass explicit send authorization to the generic engine.

Supported department keys:

- `engineering`
- `logistics`
- `wellness`
- `finance`
- `main`
- `business`
- `office-leaks`

Example watched live test:

```cmd
python automation\draft_department_boot.py wellness --send
```

## What has been proven

- Exact chat selection works for all seven department chats when the destination loads normally.
- Standardized chat naming works across all launch targets.
- Active document verification works and prevents action in an unverified destination.
- Composer readiness checks work.
- Long canonical prompts are visibly written into the composer.
- Draft-only mode works.
- Explicit send mode is wired through the department launcher.
- The destination safety gate correctly stopped when Wellness remained stuck on the loading spinner.

## Connector behavior and accepted operating assumption

Typing the literal text `@GitHub` through automation does not create the visual GitHub connector pill.

Observed behavior with GPT-5.6:

- GitHub usually remains available in context because Rob uses it frequently in every department chat for advisories, notebooks, updates, and synchronization.
- A boot may therefore succeed even when `@GitHub` remains plain text.
- The main soft failure is a cold or stale chat where GitHub has fallen out of context and the boot cannot read the repository.
- Rob accepts this risk for now because it is visible and recoverable: manually invoke GitHub and send `retry`.

This is a known soft failure, not a current blocker.

## Write-verification debugging history

Earlier verification methods failed even though text was visibly present:

1. Exact UIA value comparison timed out.
2. Normalized prefix/suffix comparison still observed zero characters because the ChatGPT composer exposed no value through UIA readers.

Latest patch changes verification to a clipboard round-trip:

1. focus composer;
2. select all;
3. copy;
4. compare clipboard text against the intended prompt using normalized strong matching;
5. restore the user's prior clipboard contents;
6. collapse the composer selection safely;
7. permit send only after verification.

Latest relevant commit:

- `4413fd384572452b05bf36ce3ada7dca55046917` — clipboard-based composer verification.

## Confirmed loading failure mode

The watched Wellness `--send` test stopped before composer work with:

```text
STOPPED: Destination verification failed. Expected 'Life OS - Wellness HQ', observed 'ChatGPT'.
```

Visible behavior:

- Wellness showed the persistent loading spinner;
- the target document never became available to UI Automation;
- the script observed only the generic `ChatGPT` document title;
- no prompt was written and nothing was sent;
- Rob had to click away and click back manually before Wellness loaded.

This is correct safe-stop behavior. The unresolved question is whether the generic engine should perform one bounded re-navigation retry when the observed title remains `ChatGPT`, or continue treating this as a manual recovery case.

## Important commit trail

- `84ffd1833d996832795f2bf0f81f5bf664aa4836` — initial generic chat automation.
- `5940d3f3544e39c9fad786b6014710a770692753` — already-active target, composer discovery, draft preservation.
- `13e24dd905cb1edb953fe986ba73478112df1993` — readiness gate and write verification.
- `9ba40e616e7bc1ea2a9bfe530bacf86fae536306` — stale UIA wrapper fix.
- `237020c64638875ea1712ef0ab080ca6dc65d22b` — first canonical Logistics launcher.
- `610732e6866e454b6a318461acd89df1588095d9` — reusable department launcher.
- `719985c7d8ef654d1dd717a878e0147797fe283a` — standardized launcher mappings.
- `f77dff9423695fd9afeef72d75be44bff413bf02` — canonical HQ naming standard.
- `fae297aca6a63067be3bcfe626d219296e8ed875` — Office Leaks HQ added to naming standard.
- `71b2bdb9c96571457b739207e914f5c55ec64b20` — Office Leaks launcher restored.
- `0ecc5f0427d16518fbda0b0ca0f14a2fd541a45a` — explicit launcher send mode.
- `dc732a628c1eb40b8648e517cf73c093b0c33cb3` — normalized long-prompt verification attempt.
- `4413fd384572452b05bf36ce3ada7dca55046917` — clipboard round-trip verification.

## Next Penny instructions

1. Continue in a fresh Engineering HQ chat.
2. Read this note before changing either automation script.
3. Do not misclassify the latest test as a clipboard-verification failure; the run never reached the composer.
4. Decide whether to add exactly one bounded re-navigation retry for the generic `ChatGPT` loading state.
5. Keep draft-only as the default.
6. Keep `--send` explicit.
7. Do not attempt automatic connector-pill resolution unless later evidence makes it necessary.
8. Do not proceed to unattended morning scheduling until a full live send completes successfully and Rob explicitly authorizes the scheduling layer.

## Pause reason

The current Engineering chat is increasingly laggy, with repeated loading-spinner behavior each time Rob returns. Resume from this note in a fresh Engineering HQ chat.
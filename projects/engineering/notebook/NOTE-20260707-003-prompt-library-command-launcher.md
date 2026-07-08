# NOTE-20260707-003 — Prompt Library / Command Launcher

Date: 2026-07-07
Project: Chief Engineering Penny / Engineering HQ
Related Projects: Life OS, Virtual Assistant Business, future PennyOS / Penny Platform, scheduled task workers
Status: Active idea capture

## Context

Rob identified a small but important operational friction: repeatedly having to remember and retype standard prompts for Life OS operations, department syncs, advisory creation/acknowledgement, Gemini handoffs, notebook capture, boot refreshes, and similar repeat actions.

Because task-worker automation is not yet fully reliable or complete, Rob proposed a lower-friction manual bridge:

- Store standardized prompts in one durable source.
- Refer to them by short IDs.
- Copy/paste a small trigger phrase such as `GitHub Prompt #3` or `Use Prompt ADV-ACK-001`.
- Let Penny fetch/follow the prompt from GitHub.
- Reduce Rob's mental load without needing full automation yet.

Rob then realized this could also become a small Python learning/build project with a UI for fast retrieval.

## Core Engineering Interpretation

This is not merely a prompt list.

It may be the first form of a Life OS command language.

A stable prompt ID can work manually today and later become a task-worker command, launcher action, API call, or automation workflow. The user-facing command vocabulary can remain stable while the backend implementation evolves.

Key idea:

> Reduce cognitive load before reducing labor.

Secondary idea:

> Manual prompt shortcuts today can become automation commands tomorrow.

## Possible Durable Source

Potential GitHub file:

- `reference/STANDARD_PROMPTS.md`

or:

- `reference/PROMPT_LIBRARY.md`

GitHub is a good fit because it is durable, versioned, searchable, and available to all HQs.

This file should probably contain abstract prompt templates only, not sensitive data or client details.

## Possible Prompt ID Scheme

Use stable named IDs rather than plain numbers.

Examples:

- `BOOT-ENG-001` — Engineering boot and sync.
- `BOOT-BUS-001` — Business boot and sync.
- `SYNC-READONLY-001` — Read-only context refresh.
- `ADV-CREATE-001` — Create advisory.
- `ADV-ACK-001` — Acknowledge advisory.
- `NOTE-ENG-001` — Add Engineering notebook leaf.
- `GEMINI-DRIVE-001` — Prepare prompt for Gemini Drive artifact generation.
- `RPR-EXPORT-001` — Prepare Rob → Penny → Rob file workflow.

Prompt IDs should be meaningful enough that Rob can remember them or search them quickly.

## Prompt Record Shape

Each prompt entry could include:

- Prompt ID.
- Title.
- Category.
- Target department or context.
- Purpose.
- Required reads.
- Allowed writes.
- Output expected.
- Guardrails.
- Full copy/paste prompt.
- Last updated date.

Example skeleton:

```md
### ADV-ACK-001 — Acknowledge advisory

Category: Advisory
Target: Any department
Purpose: Acknowledge an advisory routed to the current department.
Mode: GitHub write allowed only for Advisory Index and source board.
Reads:
- `coordination/ADVISORY_INDEX.md`
- Source board named in the index
Writes:
- Source board
- `coordination/ADVISORY_INDEX.md`
Guardrails:
- Do not use Department Event Inbox unless Rob explicitly reactivates it.
- Keep acknowledgement abstract.
Prompt:
> @GitHub acknowledge the advisory routed to this department. Read the Advisory Index, read the source board, mark the advisory acknowledged/ingested, update the Advisory Index, and report what changed.
```

## Possible Local Python App

Working title:

- Life OS Prompt Launcher
- Penny Prompt Launcher
- Life OS Command Launcher

Version 1 features:

- Load prompts from local JSON or Markdown-derived data.
- Search by ID, title, keyword, or category.
- Category filters.
- Prompt preview pane.
- Copy-to-clipboard button.
- Optional favorite prompts.
- Optional recent prompts.

Simple stack:

- Python.
- Tkinter for first UI because it ships with Python.
- JSON as prompt storage for local app use.
- GitHub Markdown as durable source of truth.

Possible local files:

- `prompts.json`
- `app.py`
- `README.md`

Potential later stack:

- PySide6 for nicer desktop UI.
- Web UI if needed.
- GitHub sync/export later.

## Learning Value

This could be a strong Engineering Classroom project because it teaches practical Python:

- Data modeling.
- JSON read/write.
- UI layout.
- Search/filter logic.
- Clipboard access.
- File handling.
- Error handling.
- Packaging into an executable.
- Possibly syncing data from GitHub later.

It is small enough to build, useful enough to motivate learning, and connected to Rob's real workflow.

## Manual-to-Automation Bridge

This idea can be staged:

### Stage 1 — Markdown Prompt Library

Create a GitHub file with standard prompts and stable IDs.

Rob can say:

- `@GitHub use prompt ADV-ACK-001`
- `@GitHub prompt NOTE-ENG-001`
- `@GitHub run BOOT-ENG-001`

### Stage 2 — Copy/Paste Master Sheet or Local Quick Reference

Rob keeps a small sheet/list with IDs and one-line descriptions.

This reduces mental drain even before a UI exists.

### Stage 3 — Local Python Prompt Launcher

A tiny UI searches and copies prompts.

### Stage 4 — Command Vocabulary

Prompt IDs become stable Life OS command names.

### Stage 5 — Task Worker / Automation Integration

The same IDs can later map to scheduled workers, connector workflows, or API-backed actions.

## Design Principles

- Keep the first version boring.
- Do not overbuild the launcher.
- Stable IDs matter more than fancy UI.
- GitHub should hold abstract prompts and command definitions.
- Sensitive details should be injected at runtime by Rob or retrieved from proper source systems.
- Each prompt should make read/write permissions explicit.
- Prompts should default to read-only unless the operation inherently requires writing.
- Commands should be short enough for Rob to use while foggy, tired, or overloaded.

## Possible Categories

- Boot / Sync.
- Advisory.
- Notebook.
- Engineering.
- Business.
- Finance.
- Main Assistant.
- Life Logistics.
- Gemini / external model handoff.
- RPR / user-mediated file transfer.
- Drive artifact creation.
- GitHub housekeeping.
- Client delivery / VA Business.

## Potential Risks

- Too many prompts could recreate the same clutter it is meant to solve.
- Numeric-only IDs may be hard to remember.
- If prompts are too broad, they may cause unwanted writes.
- If prompts are too specific, they may multiply too quickly.
- The library needs clear categories and short descriptions.
- Prompt execution should still respect current boot rules, advisory rules, connector safety, and department boundaries.

## Near-Term Recommendation

Do not build the Python app first.

Start with the source-of-truth prompt library in GitHub and a small set of high-use prompts.

Candidate first prompts:

1. Engineering boot/sync.
2. Business boot/sync.
3. Advisory check.
4. Advisory acknowledge.
5. Advisory create.
6. Engineering notebook capture.
7. Gemini artifact handoff.
8. Read-only project refresh.

Once Rob actually uses those repeatedly, build the Python launcher around the real prompt set.

## Closing Thought

This is a deceptively small infrastructure idea. It does not automate the whole Life OS, but it creates a stable command surface for Rob. That command surface can later be wired into whatever automation becomes reliable.

In other words: first the runes, then the machine.

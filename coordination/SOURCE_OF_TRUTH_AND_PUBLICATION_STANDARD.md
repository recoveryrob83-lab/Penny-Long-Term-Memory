# Life OS Source-of-Truth and Publication Standard

Updated: 2026-07-04
Purpose: Durable Life OS standard for deciding where information originates, where it is published, and which copy is authoritative.

## Status

Adopted as a Life OS architecture standard.

Source advisory: ADV-20260704-006 from Chief Engineering Penny.

## Core Principle

Choose the natural authoritative home first.

Then make every other copy clearly secondary.

## Short Form

Source in GitHub.

Publish to Drive.

Use exceptions when another system is the natural authoritative home.

This is not GitHub-for-everything.

It is a one-authoritative-home rule.

## Default Ownership

Default Life OS ownership:

- GitHub owns operational state, Markdown docs, structured records, logs, procedures, architecture, source artifacts, advisory records, department handoffs, and design standards.
- Google Drive owns polished documents, human-readable artifacts, exported/publication copies, and native office files when they are the authoritative working document.
- Google Sheets may be authoritative when the spreadsheet is the natural working object, such as checkbook ledgers, matrix scoring sheets, trackers, or tabular models.
- Google Calendar owns timed commitments.
- Todoist owns Rob-facing actionable tasks and reminders.
- Gmail owns correspondence and communication evidence.
- Life Logistics HQ owns coordination clarity and should know where the authoritative home is.

## Publication Rule

A Drive document can be a publication artifact generated from GitHub source.

When so, the Drive artifact should clearly identify:

- the GitHub source path,
- the generation or update date,
- whether the Drive copy is editable or read-only,
- whether edits should happen in GitHub source or directly in Drive.

## Native Drive Exception

Drive may be authoritative when the file is naturally edited and used in Drive.

Examples:

- Finance-owned checkbook spreadsheets.
- Human-edited Google Docs.
- Sheets that require formulas, tabs, filters, or manual spreadsheet interaction.
- Polished PDFs, DOCX, or presentation artifacts.
- Working documents whose primary value is human-facing layout or collaborative editing.

When Drive is authoritative, GitHub should store only an abstract pointer, status note, or routing note.

## GitHub Source Pattern

Use GitHub as source when the artifact is:

- operational state,
- procedure or policy text,
- Markdown documentation,
- architecture notes,
- design standards,
- advisory and sync state,
- department boot/handoff/status/open-loop records,
- source text for generated artifacts,
- version-controlled structured records.

## Drive Publication Pattern

Use Drive as publication when the artifact is:

- intended for human reading outside GitHub,
- formatted for presentation or review,
- exported from GitHub source,
- a DOCX, PDF, Sheet, or Slides artifact,
- a polished working file for Rob or another person.

## Generated Artifact Rule

If a Drive artifact is generated from GitHub source, do not treat Drive edits as authoritative unless Rob explicitly changes the source-of-truth decision.

If Drive edits are made to a generated artifact, reconcile them back into the GitHub source or mark the Drive artifact as a fork.

## Department Guidance

Each department should know:

1. Which records originate in GitHub.
2. Which records originate in Drive.
3. Which Drive artifacts are publications from GitHub source.
4. Which Drive artifacts are authoritative working files.
5. Whether generated artifacts can be manually edited.
6. Where regenerated/exported artifacts should be listed.

Departments may maintain indexes only when useful:

- `data/` for structured source records,
- `published/` for generated/publication artifacts,
- `artifacts/` for outputs or deliverables.

Do not create these folders by default without a measured need.

## Reliability Rationale

Connector reliability observations suggest that GitHub is better suited for repeated small operational writes and version-controlled text state.

Google Drive remains valuable for human-readable working records and native office artifacts, but repeated connector write/create operations can become fragile.

Therefore, Life OS should reduce unnecessary Drive writes by keeping operational source in GitHub where appropriate and publishing to Drive only when a human-facing artifact is needed.

## Design Principle

Make authority explicit.

Avoid duplicate living sources.

Prefer one source, many references or publications.
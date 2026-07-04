# PEND-ENG-20260704-013 — GitHub canonical source and Drive publication artifacts

Date captured: 2026-07-04
Status: Pending
Origin: Chief Engineering Penny / Life OS architecture discussion
Tags: connector reliability, data architecture, document architecture, Google Drive, GitHub, source of truth, publication layer, artifacts

## Core idea

Life OS should treat GitHub as the canonical operational repository not only for structured data, but also for documents, procedures, logs, architecture notes, and working drafts.

Google Drive should be used when Life OS needs human-readable, polished, shareable, printable, or office-style artifacts.

This broadens the prior pending advisory from database-like files and Sheets into a general source/publish/artifact architecture.

## Proposed model

GitHub owns source.

Drive owns presentation artifacts.

Translation between the two should happen only when a department needs to publish, share, format, print, or otherwise expose a human-facing copy.

Conceptual flow:

```text
GitHub source -> department-owned publication step -> Google Drive artifact
```

Better wording: publish to Drive, not move to Drive.

Moving implies the Drive copy may become authoritative.

Publishing keeps the GitHub source as the canonical version and treats Drive as a generated or presentation copy.

## Examples

### Documents

- Working draft lives as Markdown in GitHub.
- Department publishes a Google Doc only when a polished human-readable version is needed.
- If the document changes later, the GitHub source is updated first.
- A new Drive artifact can be generated or copied over when needed.

### Spreadsheets and tables

- Operational table lives as CSV, TSV, JSONL, or another text-based GitHub format.
- Department publishes a Google Sheet when sorting, filtering, sharing, visual review, printing, or charts are needed.
- The Sheet is not the only copy of the operational state.

### Reports

- Report source lives in GitHub as Markdown plus supporting data files.
- Department publishes to Google Docs, PDF, or Sheets when a human-facing report is needed.

## Department ownership rule

The HQ that owns the work should own publication of the artifact.

Examples:

- Engineering publishes Engineering artifacts.
- Business publishes Business artifacts.
- Finance publishes Finance reports.
- Life Logistics may coordinate standards, but should not become the bottleneck for every publication action.

## Rationale

This architecture reduces reliance on Google Drive as an operational database or working document store.

It also matches the emerging connector reliability evidence:

- GitHub appears better suited for repeated small operational writes and version-controlled text state.
- Drive/Sheets appear better reserved for human-facing artifacts, especially given observed write/create uncertainty and safety blocks.
- Markdown and other text formats provide clearer diffs, easier rollback, and better source control than office documents.

## Engineering principle candidate

> GitHub is the source repository. Drive is the publication repository.

Related phrasing:

> Source in GitHub. Publish to Drive.

> Do not move source to Drive; generate Drive artifacts from source when needed.

## Expected benefits

- Cleaner source-of-truth rules.
- Fewer Drive write/create operations.
- Lower risk from Drive connector safety blocks.
- Better audit trail through Git history.
- Easier rollback and review.
- Department-level artifact ownership.
- Reduced confusion over whether a Drive document or GitHub file is authoritative.
- More consistent Life OS architecture across documents, data, reports, logs, and procedures.

## Open questions

- Which document types should always originate in GitHub?
- Which artifacts should be allowed to originate directly in Drive?
- How should generated Drive artifacts identify their GitHub source file?
- Should Drive artifact names include `Generated from GitHub` or a source path?
- Should departments maintain `published/` or `artifacts/` indexes?
- What tooling should convert Markdown, CSV, JSONL, or other source formats into Drive-friendly artifacts?
- When should Drive artifacts be regenerated versus manually edited?

## Current recommendation

Keep this as a pending Engineering advisory until the broader Life OS data and document architecture is ready for formal routing.

This should likely be considered alongside `PEND-ENG-20260704-012`, which covers GitHub text state and Drive/Sheets export layers for database-like files.

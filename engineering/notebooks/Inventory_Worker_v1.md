# Inventory Worker v1

## Purpose
Document the initial prototype and engineering findings for a reusable Life OS Inventory Worker.

## Objective
Create a repeatable workflow for converting photographs of items into a structured inventory suitable for pricing and marketplace listing.

## Proposed Workflow
1. Take photos of sale items.
2. Archive photos in Google Drive under `For Sale Items/Images/<Batch>`.
3. Process images with the Inventory Worker.
4. Identify one inventory record per sale item.
5. Store structured inventory in the canonical Google Sheet.
6. Hand off to future Pricing and Listing workers.

## Canonical Data Stores
- Google Drive: original images (source of truth)
- Google Sheets: structured inventory database
- GitHub: engineering documentation and worker specifications

## Inventory Philosophy
- One row represents one sale item.
- One photo may contain multiple sale items.
- Each inventory record should reference the source image (Image ID or filename).
- Avoid inventorying obvious background objects.

## Prototype Findings
### Successful
- Vision reliably identified common household items from uploaded photos.
- Multiple items can be extracted from a single image.
- Structured inventory schema appears practical.

### Platform Constraints
- Current ChatGPT vision cannot directly inspect image pixels solely from Google Drive connector references.
- Images must currently be uploaded into chat for vision analysis.
- Spreadsheet append operations should use a reusable append adapter rather than ad hoc writes.

## Proposed Pipeline
Photos -> Drive Archive -> Inventory Worker -> Inventory Sheet -> Pricing Worker -> Marketplace Worker

## Future Improvements
- Safe Google Sheets append adapter.
- Direct Drive image processing if platform capabilities expand.
- Marketplace listing worker.
- Batch verification and duplicate detection.

## Conclusion
The architecture is considered viable. Current limitations are connector capabilities rather than workflow design.
# NOTE-20260704-001 — Token cost and deterministic software boundary

Date captured: 2026-07-04
Project: Chief Engineering Penny / Engineering HQ
Status: Open
Tags: cost model, orchestration, backend design, Penny Platform, finance

## Note

A future Penny Platform has a different cost structure than Rob's personal Life OS usage inside ChatGPT.

Personal Life OS can lean on the existing app subscription, chats, connectors, and human supervision.

A product platform would likely involve model calls, backend services, databases, workers, logs, monitoring, and connector-like integrations.

Every orchestration step may become a cost-bearing event.

## Cost Insight

Finance should eventually evaluate cost per successful workflow, not only raw token spend.

Useful examples:

- Cost per successful calendar workflow.
- Cost per successful document workflow.
- Cost per successful lookup workflow.
- Cost per successful message workflow.

This connects engineering decisions to finance and business viability.

## Engineering Principle Candidate

Use deterministic software whenever deterministic software is sufficient.

Reserve model reasoning for tasks that genuinely require language understanding, planning, judgment, synthesis, ambiguity resolution, or conversation.

Backend services or scripts should handle repeatable mechanical work such as validation, sorting, deduplication, structured data transformation, retry mechanics, logging, basic calculations, and connector execution.

The model should not spend tokens doing work that ordinary software can do more cheaply, reliably, and safely.

## Possible Future Use

This note may later inform Reliable Connector Execution Layer design, Penny Platform backend architecture, Finance cost modeling, Business product requirements, and a formal Engineering principle about the boundary between model reasoning and deterministic code.

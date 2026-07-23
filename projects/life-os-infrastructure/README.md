# LifeOS Infrastructure

Status: Active
Updated: 2026-07-02

## Purpose

Build durable external memory and workflow continuity across long chats and new context windows.

## Current Architecture

GitHub is the durable memory spine.

Google Drive is the operational workspace.

Todoist is the action queue.

Google Calendar is the timed commitments queue.

Gmail is communication evidence.

## Current Focus

- Continue migration from Drive memory to GitHub Markdown.
- Keep `memory/01_SESSION_HANDOFF.md` current.
- Keep `memory/05_OPEN_LOOPS.md` current.
- Use project folders for project-specific migration.
- Avoid over-engineering before real friction appears.

## Connector Lesson

If a long-running chat becomes unreliable with connectors, start a fresh Penny and boot from GitHub.
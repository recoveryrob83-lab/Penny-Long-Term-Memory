# Trello Flow Board SOP

Updated: 2026-07-17
Project: Life OS Coordination
Owner: Main Assistant Penny / LifeOS Coordination Hub

## Purpose

Use Trello as Rob's visual attention and flow system without turning it into another overloaded task warehouse.

Core separation:

- Trello Inbox captures raw thoughts and quick actions.
- LifeOS Flow Board shows current attention and active flow.
- Todoist holds commitments, reminders, and due-date obligations.
- Calendar holds timed commitments.
- GitHub holds durable project state and system memory.

## Canonical Board

Board: LifeOS Flow Board
URL: https://trello.com/b/QKXdwHup/lifeos-flow-board

Lists:

1. Captured
2. Next
3. Now
4. Waiting
5. Done

## Work-in-Progress Rules

- Now holds one card maximum.
- Next holds no more than three ready cards.
- Waiting contains only work blocked by another person, money, timing, information, or an external event.
- Captured contains ideas and possible work, not promises.
- Done remains visible long enough to show momentum before later cleanup.

## Card Standard

Each active card should be small enough to act on and should include when useful:

- owning lane or department;
- a concrete next action;
- a short return point showing where to resume;
- blocker or waiting condition;
- no due date unless the item is a real commitment.

Suggested lane tags or plain-text markers:

- office-leaks
- engineering
- daily-life
- finance
- wellness
- recovery

## Inbox Processing

Trello Inbox is a low-friction capture chute. Rob may add cards without classifying them.

Main Assistant processes Inbox cards through the `/FLOW` command.

Clear items may be routed to:

- Captured
- Next
- Now
- Waiting
- Todoist
- Calendar
- GitHub or a department notebook
- archive or deletion when authorized

Do not convert every captured thought into a task, commitment, or durable record.

## Commands

### `/FLOW @Trello`

Read the Trello Inbox and LifeOS Flow Board. Classify Inbox cards, identify duplicates and unclear items, recommend routing, and preserve the board limits. Read-only by default unless Rob separately authorizes moves, edits, or archiving.

### `/FLOW PROCESS @Trello`

Process all clear Inbox cards into the correct Trello list or authoritative system. Ask only about ambiguous, consequential, externally visible, or destructive items. Preserve one card maximum in Now and three maximum in Next. Do not create Todoist tasks, Calendar events, GitHub records, or deletions without clear authorization.

### `/FLOW NOW @Trello`

Review the current LifeOS Flow Board and recommend the best one card for Now plus up to three cards for Next. Update or move cards only when authorized.

## Mobile Widget Rule

Rob's Trello home-screen focus widget is configured as a Todo List widget targeting the `LifeOS Flow Board` and the `Now` list directly.

No member assignment is required for a card to appear there. Keep the `Now` list to one card so the widget remains a focused execution surface rather than a second backlog.

## Operating Principle

> Capture fast. Sort deliberately. Keep one thing active. Leave a return point before switching.

Context switching is allowed. Unmarked context switching is not.

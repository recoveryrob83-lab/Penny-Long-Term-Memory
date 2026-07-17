# Desktop Department Automation Goal

Date: 2026-07-17
Project: Chief Engineering Penny / Engineering HQ
Status: Active engineering goal

## Decision

Rob selected desktop automation for department synchronization and boot as the next Engineering goal after the successful LifeOS Dashboard milestone.

This goal takes priority over expanding Penny Commands into a full prompt-command launcher. The launcher remains useful, but it should eventually become the control surface for real automation rather than a polished collection of copy buttons.

## Problem

LifeOS department work still requires repeated mechanical setup:

- opening or locating the correct department chat;
- synchronizing the local LifeOS repository;
- selecting the correct boot mode and department prompt;
- inserting the canonical connector-tagged boot instruction;
- confirming the department loaded the correct GitHub state;
- repeating similar steps across several departments.

The reasoning work belongs to Rob and Penny. The repetitive desktop ceremony does not.

## Goal

Design and implement a small, observable, recoverable desktop automation layer that reduces the friction of syncing and booting LifeOS departments without weakening source-of-truth boundaries or pretending uncertain actions succeeded.

The first useful result should allow Rob to choose a department and initiate a bounded boot workflow with fewer manual steps.

## First Milestone

Create a technical discovery and implementation packet that answers:

1. Which Windows and ChatGPT desktop actions can be controlled reliably?
2. Which steps should remain explicit user confirmation points?
3. How should the automation detect the correct department, chat type, and boot prompt?
4. How should GitHub synchronization be verified before boot text is submitted?
5. What evidence proves each step completed?
6. How does the workflow stop safely when the desktop state differs from expectations?
7. Which existing Penny Commands components can be reused as the future control surface?

## Initial Workflow Candidate

A bounded department boot may eventually:

1. accept a selected department;
2. verify the local LifeOS repository state;
3. open or focus the correct ChatGPT department chat;
4. assemble the canonical boot prompt from durable command data;
5. place the prompt into the composer;
6. pause for review or submit according to the approved safety level;
7. verify that the expected department synchronization response appears;
8. record a local success, blocked, or failed result without inventing completion.

## Safety Boundaries

- Do not store ChatGPT credentials, GitHub tokens, connector secrets, or private URLs in automation code or GitHub.
- Do not use blind coordinate clicking as the sole basis for claiming success.
- Prefer stable selectors, window identity, observable state, and bounded timeouts when available.
- Preserve user control for destructive, ambiguous, cost-bearing, or externally visible actions.
- Do not broaden this goal into general autonomous computer control.
- Do not resume scheduled department sync workers as part of this work.
- Never discard local Git changes, rewrite history, or bypass the dashboard's guarded synchronization rules.
- Treat failures as blocked states with recovery instructions, not invitations to continue guessing.

## Relationship to Penny Commands

Penny Commands remains the canonical-prompt launcher and a likely future front end for this automation layer.

The intended sequence is:

1. build and validate the desktop automation foundation;
2. expose reliable actions through a small interface;
3. evolve Penny Commands into the control panel once the underlying actions are real and observable.

## Success Standard

The goal is successful when at least one department can be synced and booted through a repeatable workflow that:

- substantially reduces manual setup;
- stops safely when assumptions fail;
- provides visible evidence for each completed step;
- preserves canonical GitHub and command sources;
- and can be extended to additional departments without copying fragile one-off scripts.

## Scope Note

This is an active Engineering goal and open loop. It is not yet an implementation authorization for unrestricted desktop control, background scheduling, or automatic connector writes.

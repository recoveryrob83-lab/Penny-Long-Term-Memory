# LifeOS Agent Entry Point

This repository is the durable operating system for LifeOS. This file is a small harness-facing map, not a second operating manual.

## Start Here

For any LifeOS Boot, Fresh Boot, department/HQ initialization, Worker initialization, or explicit system review:

1. Read `memory/STARTUP_BOOT.md` first. It is the canonical startup and role-routing authority.
2. Read `MASTER_INDEX.md` as the repository navigation map.
3. Follow the exact current route in `memory/STARTUP_BOOT.md` and load only the context required for the named room, department, project, Worker, or review.
4. Use applicable repository Skills under `.agents/skills/` for recurring procedures.

`MASTER_INDEX.md`, this file, and Skills do not replace canonical governance, state, source records, tests, evidence, or Rob's authority.

## Operating Boundaries

- Rob is final authority.
- `LifeOS_HQ` is the shared meeting room, not a department or independent backlog owner.
- `Chief_of_Staff_HQ` coordinates daily operations, routing, reporting, and follow-through.
- Departments own specialist judgment and durable state within their assigned domains.
- `Maintenance_HQ` owns global boot integrity, shared governance, source boundaries, repository coherence, and cross-system reconciliation.
- `Engineering_HQ` owns technical implementation, automation, parser/validator behavior, dashboard machinery, tests, and reliability mechanisms.
- Do not edit another department's files without explicit authority for coordinated repair.
- Fetch current authoritative files before editing and preserve unrelated content.
- Broad requests such as "update GitHub", "sync everything", or "clean this up" are not blanket write authority.
- Boot and Sync are read-only unless Rob separately authorizes a write.
- Do not create duplicate truth for visibility or convenience.

## Source Systems

Use the current canonical source-boundary records for details. In short:

- Conversation: temporary reasoning and working context.
- GitHub: durable abstract LifeOS state, rules, decisions, advisories, procedures, architecture, Worker profiles, and meaningful history.
- Google Drive: human-facing working documents and office artifacts.
- Trello: raw ideas, possibilities, candidate work, experiments, and attention flow.
- Todoist: Rob-facing commitments and reminders.
- Calendar: timed commitments.
- Gmail: communication evidence.
- Dashboard/automation runtime: transport, diagnostics, visibility, and bounded control, not competing truth.

## Skills

Portable repository Skills live at:

`.agents/skills/<skill-name>/SKILL.md`

Skills are procedural interfaces. They must point to current canonical LifeOS records rather than duplicating policy or volatile state when a stable authoritative path exists.

Use Skill descriptions for task matching. Load the full Skill only when relevant to the current task.

Current foundational Skills are stored under `.agents/skills/`. Do not create speculative placeholder Skills merely to reserve names.

## Repository Navigation

Use `MASTER_INDEX.md` before repository-wide exploration. It is designed to identify stable paths, ownership boundaries, current application surfaces, Worker locations, advisory infrastructure, tests, and historical/compatibility areas.

The index is navigation only. When it conflicts with a live authoritative source, the live authoritative source wins and the discrepancy should be reported through the proper owner rather than silently repaired.

## Advisory Work

Formal cross-department advisories use the canonical source-board + Advisory Index model. When creating or changing an advisory, use the applicable advisory Skill and current live contracts, especially:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/LIFEOS_V2_ADVISORY_COURIER_ENVELOPE.md`
- `coordination/ADVISORY_INDEX.md`

Do not duplicate full advisories into target boards, department open loops, Todoist, GitHub Issues, or dashboard state.

## Validation and Claims

- Never claim a connector read/write, test, delivery, implementation, verification, or external action succeeded without current evidence.
- Distinguish source presence, tests, runtime verification, source-owner verification, and acceptance/closure.
- If instructions or authoritative sources materially conflict, pause the affected action, identify the conflict, and route or reconcile it visibly.

## Harness Portability

This root `AGENTS.md` and `.agents/skills/` tree are the preferred portable interface for Codex-centered and agent-skill-compatible harnesses such as Codex and OpenCode.

Do not add vendor-specific duplicate instruction trees unless a real harness requirement cannot be satisfied by this portable layer.
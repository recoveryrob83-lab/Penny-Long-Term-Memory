---
name: lifeos-boot
description: >
  Boot, fresh-boot, initialize, restore, or rehydrate a LifeOS operating context
  from the canonical GitHub repository. Use when Rob asks to Boot or Fresh Boot
  LifeOS_HQ, Chief_of_Staff_HQ, Maintenance_HQ, Engineering_HQ, another
  Department HQ, a standalone LifeOS project, a bounded Worker, or an explicit
  LifeOS system audit/architecture review. Also use when a recreated or cold
  chat needs authoritative LifeOS operating context before work begins. Do not
  use for ordinary file lookup, a Sync-only request, or as authority to write.
---

# LifeOS Boot

## Purpose

Load the smallest complete authoritative LifeOS operating context for the named
room, department, project, Worker, or system-review scope.

This Skill is a procedural wrapper. It is not an authority record and does not
replace the canonical LifeOS repository files.

Canonical repository:

`recoveryrob83-lab/Penny-Long-Term-Memory`

Stable navigation aid:

`MASTER_INDEX.md`

Canonical boot authority:

`memory/STARTUP_BOOT.md`

## Core contract

- Boot is read-only.
- Boot loads context; it does not authorize maintenance, edits, promotion,
  routing, closure, or other durable writes.
- Rob remains final authority.
- Use the current GitHub repository as the source for boot-time operating
  context. Do not substitute remembered, cached, quoted, or previously loaded
  copies when current repository access is available.
- Use `MASTER_INDEX.md` for navigation and path discovery only.
- Use `memory/STARTUP_BOOT.md` for the actual current boot procedure.
- Do not duplicate the full boot procedure into this Skill.
- Do not broaden scope merely because more repository content is available.
- Do not read all departments, notebooks, advisories, backlogs, archives, or
  application source unless the canonical route or the requested scope requires
  them.
- If repository access is unavailable or a required canonical file cannot be
  read, report the missing dependency. Do not invent a successful boot.

## Procedure

### 1. Resolve the boot target

Determine the exact requested target from Rob's instruction.

Typical targets include:

- `LifeOS_HQ`
- `Chief_of_Staff_HQ`
- `Maintenance_HQ`
- `Engineering_HQ`
- another named Department HQ
- a standalone LifeOS project
- a bounded Worker
- an explicit LifeOS system audit or architecture review

If Rob supplied a legacy room/display name, resolve it only through the current
canonical naming and Hub records referenced by the boot procedure. Do not infer
a filesystem rename from a display-name change.

If the target is clear, do not ask Rob to repeat it.

### 2. Read the canonical boot authority first

Read:

`memory/STARTUP_BOOT.md`

Treat its current contents as authoritative for:

- universal-kernel membership and order;
- shared execution-protocol routing;
- room and department boot routes;
- Worker boot routes;
- standalone-project routes;
- explicit system-review routes;
- conditional dependencies;
- exclusions and read-scope boundaries.

If this Skill conflicts with `memory/STARTUP_BOOT.md`, follow
`memory/STARTUP_BOOT.md` and report the Skill drift after the boot.

### 3. Read the repository master index

Read:

`MASTER_INDEX.md`

Use it as a path-first navigation map to resolve:

- stable department filesystem subtrees;
- current canonical room-to-path mappings;
- shared contracts;
- advisory infrastructure;
- Worker/profile/procedure locations;
- application and verification surfaces when the boot route requires them.

The master index is not boot authority. If it conflicts with
`memory/STARTUP_BOOT.md` or a live authoritative file, prefer the authoritative
file and note the discrepancy.

### 4. Load the universal operating kernel

From the current `memory/STARTUP_BOOT.md`, extract the exact universal-kernel
file list and read it in the exact canonical order.

Do not rely on a kernel list remembered from a previous run or embedded in this
Skill.

Do not skip a required kernel file merely because its subject appears summarized
in `MASTER_INDEX.md`.

### 5. Load shared execution context when routed

After the universal kernel, follow the current boot file's instructions for
loading the shared execution and communication protocol or Worker execution
contract.

Do not make shared execution files universal if the canonical boot route does
not make them universal.

### 6. Load only role-routed context

Follow the exact branch for the named boot target.

Use `MASTER_INDEX.md` to jump directly to the stable paths instead of searching
the repository.

For a Department HQ, load only the department's canonical boot records in the
order currently defined by `memory/STARTUP_BOOT.md`, then load explicitly routed
dependencies only.

For `LifeOS_HQ`, load only the global/Hub records currently routed by the
canonical boot procedure and only read department records when the meeting topic,
dependency, advisory, assignment, or decision actually requires them.

For a bounded Worker, follow the current Worker branch exactly. Load the shared
Worker contract, owning department identity, exact Worker profile, referenced
assignment/advisory/schedule, and only the local records and SOPs required for
that bounded task.

For a standalone project or explicit system review, follow the current canonical
route and keep scope bounded to the named project or review.

### 7. Apply conditional reads literally

When the canonical procedure says a file is read only when relevant, first test
whether the named boot target or task satisfies that condition.

Examples of conditionally relevant material may include:

- Advisory Index state;
- migration or mirror records;
- global handoff/open loops;
- Worker contracts;
- department notebooks/history;
- application implementation source;
- cross-department dependencies.

Do not fetch conditional material "just in case."

### 8. Preserve Boot / Sync separation

If Rob requests both Boot and Sync:

1. complete Boot first;
2. report Boot as complete;
3. then execute the separate `lifeos-sync` procedure if that Skill is available,
   otherwise follow the current canonical Sync rules;
4. keep Sync read-only unless separately authorized.

Do not collapse Boot and Sync into one implied maintenance operation.

### 9. Return a compact boot receipt

After all required reads succeed, report:

- boot target;
- canonical repository;
- branch/ref if known from the connector;
- canonical boot file read;
- master index read;
- role route loaded;
- any conditionally loaded dependencies;
- any missing required file, conflict, or drift;
- explicit confirmation that Boot was read-only.

Keep the receipt compact. Do not reproduce the contents of the kernel or
department files unless Rob asks for them.

Suggested shape:

```text
BOOT COMPLETE
Target: Engineering_HQ
Source: recoveryrob83-lab/Penny-Long-Term-Memory
Boot authority: memory/STARTUP_BOOT.md
Navigation: MASTER_INDEX.md
Route: universal kernel → shared execution protocol → Engineering_HQ records
Conditional dependencies: none
Writes: none
Drift/holds: none
```

Use the actual target and actual result. Never emit `BOOT COMPLETE` if required
canonical reads failed.

## Stop conditions

Stop and report rather than improvising when:

- the repository cannot be accessed;
- `memory/STARTUP_BOOT.md` is missing or unreadable;
- the requested role cannot be resolved through current canonical records;
- a required routed file is missing;
- two authoritative current records give materially conflicting boot
  instructions;
- the requested action requires a write that Boot itself does not authorize.

A navigation-map mismatch alone does not authorize repair. Report it for
Maintenance review unless Rob separately authorizes reconciliation.

## Success condition

Boot succeeds when:

1. the current canonical boot authority has been read;
2. the current master index has been used for navigation;
3. every file required by the canonical route for the named target has been
   successfully read in the required order;
4. no unrelated context has been loaded without a routed reason;
5. no durable write has occurred;
6. the boot receipt accurately describes what was loaded and any drift or hold.

## Design boundary

Keep this Skill stable while LifeOS procedures evolve.

When boot policy, file membership, role routing, or conditional reads change,
update the canonical GitHub procedure and/or master index at their authoritative
paths. Update this Skill only when its semantic contract, stable paths, trigger
conditions, or execution behavior genuinely change.

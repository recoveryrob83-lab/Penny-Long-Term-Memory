# NOTE-20260718-001 — Drive Chief's Manual and GitHub Operational Translation Architecture

Date: 2026-07-18
Updated: 2026-07-18
Department: Logistics HQ
Status: Completed
Owner: Logistics HQ
Record Type: Decision
Authority: Authoritative

## Summary

Life OS will maintain a human-facing Chief's Manual in Google Drive and a compact operational implementation in GitHub. The Drive manual explains Rob's language, authority, intent, examples, and system philosophy; GitHub boot files and operating rules enforce the behavior departments and automation must follow.

The full Drive manual will not be loaded during every boot and will not be mirrored verbatim into GitHub. Routine boots remain fast, role-routed, and independent of Drive connector availability.

## Trigger or Source

Rob approved the Google Drive document [Life OS Chief's Manual — Language, Authority, and Operating SOP](https://docs.google.com/document/d/1dbQoG1kwsTTRANdAeJcSNKu8fdo2D2cXywiM1AK8GKc/edit) as the human-facing "Basic Text" for Life OS.

The architecture was promoted into durable memory because it governs the upcoming repository audit, future boot behavior, command interpretation, and reconciliation between human intent and machine-operational rules. Rob explicitly authorized this Logistics notebook write.

## Record

### Decision

1. **The Drive Chief's Manual is the human-facing doctrine.**
   - It explains the meaning of Boot, Fresh Boot, Sync, Maintenance, Reconcile, Audit, Capture, Promote, Route, Close, and Refresh.
   - It gives Rob readable examples, intent boundaries, write-authority guidance, and the anti-yes-man standard.
   - It is the primary reference when Rob is revising command language, authority, or system philosophy.

2. **GitHub is the operational translation and enforcement layer.**
   - `memory/03_OPERATIONAL_RULES.md`, `memory/STARTUP_BOOT.md`, ownership SOPs, department contracts, and automation instructions must express the compact rules required during operation.
   - GitHub should implement the Chief's Manual rather than duplicate its full explanatory prose.

3. **Startup Boot loads the operational rules, not the entire Drive manual.**
   - Every ordinary boot should read the compact GitHub operating kernel.
   - The full manual is not a routine universal boot dependency.
   - This keeps boot context bounded and prevents Drive availability from becoming a startup requirement.

4. **No verbatim GitHub mirror will be maintained.**
   - A full copy would create two large documents capable of drifting while both appear authoritative.
   - GitHub may contain a compact reference to the manual, its role, and its last reconciliation state.
   - Explanatory doctrine belongs in Drive; executable rules belong in GitHub.

5. **Logistics owns reconciliation between the two layers.**
   - When the Chief's Manual changes materially, Logistics audits whether GitHub still implements it correctly.
   - Logistics records discrepancies and updates global operational files within its authority.
   - Department-specific corrections are routed to the owning department unless Rob grants explicit coordinated repair authority.

6. **The full manual is consulted selectively.**
   - when Rob changes Life OS language or authority;
   - during a deep governance or compliance audit;
   - when ambiguity or conflict appears;
   - when designing a new department, worker, command, or automation contract;
   - when Rob explicitly asks Penny to consult the Basic Text.

7. **Conflict handling is visible.**
   - Drive and GitHub should agree without becoming competing detailed sources.
   - When they conflict, the system pauses the affected write or operation, identifies the difference, and reconciles it deliberately.
   - Neither layer silently overwrites the other.

### Rationale

The Chief's Manual solves a human-interface problem: Rob often works quickly and may use broad language such as "sync," "boot," or "update GitHub" without intending unlimited writes. A readable manual lets Rob understand and intentionally use the system's language without memorizing repository paths or hidden technical rules.

The GitHub operational layer solves a machine-execution problem: departments and automation need short, precise, connector-independent rules during every boot. Loading the complete human manual nightly would consume unnecessary context, add latency, and introduce a Drive dependency into routine startup.

The separation therefore preserves both accessibility and operational discipline:

> The Basic Text explains the program. The boot files run the meeting.

## Operational Consequence

This decision is the architectural basis for the next authorized Life OS repository audit. That audit should make the relationship explicit in global boot, operating, handoff, open-loop, and department files while preserving local department ownership and Logistics audit authority.

This notebook record does **not** itself authorize those additional edits. It preserves the approved reasoning and decision only. The broader audit begins under separate authorization from Rob.

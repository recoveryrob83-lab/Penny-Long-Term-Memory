# NOTE-20260717-013: Command Center Scheduling Live Validation and Next Recovery Edge

Date: 2026-07-17
Status: Active operational record
Owner: Engineering HQ

## Purpose

Record the implemented Automation Command Center state, live scheduling evidence, current operating boundary, and the next demonstrated desktop-recovery edge case.

## Implemented

The dashboard-integrated Automation Command Center now supports:

- eight exact LifeOS destinations;
- canonical, saved, and custom prompt sources;
- draft and explicitly confirmed live-send modes;
- protected canonical prompts and editable saved copies;
- saved-prompt default destinations with mismatch warnings and explicit override;
- one-job-at-a-time locking;
- global pause;
- persistent SQLite activity history;
- one-time, daily, and weekly schedules in `America/Chicago`;
- persistent scheduled jobs across dashboard restarts;
- schedule creation, editing, pause, resume, and deletion;
- separate Scheduled Jobs and Run History views with independent filters;
- reuse of the validated desktop automation safety boundary.

Scheduling implementation head: `84b99b138b0c096b8e8067490f602fee309b4720`.
Structured failure reporting head: `34ce8052d682daba66138e2b5289af2c3a120aac`.
Scheduled Jobs / Run History split head: `53e5b57cb5ba5fbe339295cdc3132d1bdb71b585`.

## Live Validation Evidence

Observed live tests on Rob's Windows machine:

1. One-time custom live send
   - Name: `Hi Penny Test`
   - Destination: Engineering HQ
   - Scheduled: 2026-07-17 14:59 CT
   - Completed: 2026-07-17 14:59:48 CT
   - Result: succeeded / completed successfully
   - Final state: Completed / no future run

2. Recurring daily custom live send
   - Name: `Hi Penny LifeOS Test`
   - Destination: LifeOS HQ
   - Scheduled: daily at 15:05 CT
   - Completed first run: 2026-07-17 15:05:25 CT
   - Result: succeeded / completed successfully
   - Next run advanced to: 2026-07-18 15:05 CT

3. Mobile concurrency
   - Rob continued chatting in Engineering HQ on mobile while the desktop automation fired into LifeOS HQ.
   - Another response was actively generating in the mobile chat.
   - The desktop automation navigated to LifeOS HQ and sent the scheduled prompt without interfering with the mobile chat or sending to the wrong destination.

4. Initial scheduled occupied-composer refusal behind `Show more`
   - Name: `Hi Penny Logistics Failure Test`
   - Destination: Logistics HQ
   - Scheduled: 2026-07-17 15:26 CT
   - Completed: 2026-07-17 15:26:15 CT
   - Navigation expanded `Show more`, found the exact Logistics HQ chat, and verified the destination.
   - Existing harmless composer text remained intact.
   - No scheduled text was inserted or sent.
   - Result: failed safely / no future run.

The safety behavior passed. The first dashboard report incorrectly labeled the disabled one-time failure as `Paused`, placed it below the active LifeOS schedule without clear category semantics, and displayed a generic ChatGPT-unavailable explanation.

5. Structured occupied-composer reporting re-test
   - Destination: Logistics HQ
   - Mode / prompt type: send / custom
   - Completed: 2026-07-17 16:07:12 CT
   - Result: `failed`
   - Dashboard reason: `The target composer already contains text. Clear or save that draft, then run the job again.`
   - The result appeared in Run History while the schedule definition left the default Scheduled Jobs view.

This re-test confirms the complete reporting chain from desktop safety refusal through the scheduler and persistent dashboard history.

## Reporting and Presentation Fixes

Authorized, implemented, pulled, restarted, and visually confirmed:

- the verified automation shim captures the base engine output and emits a stable `LIFEOS_RESULT_CODE` marker on failure;
- occupied-composer failures emit `composer_occupied` plus an explicit preserved-draft recovery message;
- failed or refused one-time schedules display `Failed` rather than `Paused`;
- successful one-time schedules display `Completed`;
- manually disabled recurring or future schedules display `Paused`;
- Scheduled Jobs and Run History are separate categories;
- Scheduled Jobs filters support cadence, department, state, and ordering;
- Run History filters support result, department, mode, and time order;
- finished one-time definitions are excluded from the default scheduled view but remain available through filters.

The scheduled occupied-composer safety and structured-reporting validation is complete.

## Newly Identified Edge Case

ChatGPT Classic may collapse the LifeOS project folder and hide all project chats after:

- application restart; or
- reducing the desktop window size.

The current desktop automation handles a bounded `Show more` expansion inside an already expanded project, but it has not been designed or validated to detect and reopen a collapsed LifeOS project folder before locating the destination chat.

### Current operating workaround

Until a code update is explicitly authorized:

- keep ChatGPT Classic open;
- keep the LifeOS project folder expanded;
- keep the destination chats available through the normal sidebar / `Show more` path;
- do not assume unattended jobs are safe after an app restart or significant window resize.

### Next code target

Add bounded collapsed-project recovery before exact chat navigation:

1. detect whether the LifeOS project folder is collapsed;
2. identify the exact LifeOS project control without fuzzy matching;
3. expand it once;
4. verify the expected project chat region is visible;
5. continue through existing exact-chat and `Show more` navigation;
6. stop safely if expansion or verification is uncertain.

After implementation, revalidate in draft mode first across:

- expanded project;
- collapsed project after app restart;
- collapsed project after narrow-window layout;
- visible destination chat;
- destination behind `Show more`;
- occupied composer.

## Next Product and Architecture Milestones

The newly promoted highest-priority package is documented in:

- `projects/engineering/notebook/NOTE-20260717-014-department-ownership-and-dashboard-inspection.md`

It will formalize department versus system loop ownership, role-routed boot context, cross-department routing, lifecycle rules, stale-state cleanup, and a new Department Inspection dashboard tab.

The canonical prompt catalog remains the next product/data milestone after or alongside that package. It currently exposes primarily the Boot family and requires authoritative reconciliation before expansion.

Candidate families:

- Boot / Quick Boot / Full Boot;
- Sync;
- Nightly;
- Advisory;
- Sync Advisory;
- Read Advisory;
- Consume Advisory.

Canonical definitions must remain protected and read-only; editable variants should be created as saved copies.

## Production Boundary

Scheduling is operational but not yet production-ready for fully unattended Windows use.

Before that label, Engineering still needs evidence and/or implementation for:

- dashboard restart and overdue-run behavior;
- recurring execution across a second real occurrence;
- collapsed-project recovery;
- scheduler health / preflight visibility;
- explicit missed-run policy;
- Windows startup or service packaging if required.

# Chat and Work Execution Policy

Updated: 2026-07-18
Project: LifeOS Infrastructure
Purpose: Define the operating boundary between regular ChatGPT conversations and the separate Work execution environment.

## Core Model

LifeOS uses two distinct operating surfaces:

- **Chat is headquarters.** Use it for conversation, planning, department coordination, writing, strategy, recovery work, philosophy, ordinary reasoning, and light connector work where available.
- **Work is the execution environment.** Use it for local files, terminal access, coding, testing, browser control, desktop applications, artifact production, repository changes, and other tasks that require computer execution.

Short form:

> Chat thinks. Work does. GitHub remembers. Drive holds working documents. The desktop is the execution surface.

## Current Product Boundary

Observed through controlled use on 2026-07-15 through 2026-07-17:

- Regular Chat conversations and existing ChatGPT Projects are available across mobile, web, and classic desktop surfaces.
- The new desktop Work environment uses separate Projects and Tasks.
- Work Projects created in the new desktop environment did not appear on mobile, web, or classic desktop during a controlled sync test.
- Existing regular ChatGPT Projects did not appear in the new desktop Work environment.
- A Work Project created a Task rather than a normal regular-Chat conversation.
- A controlled Work-side Chat test with no Task and limited visible output reduced the Work meter by one percentage point.
- Therefore, both Work-side Chat and Work Tasks should be treated as consuming the weekly Work allowance.
- Regular Chat on mobile, web, and classic desktop has not moved the Work meter during repeated observed use, including substantial reasoning and connector-backed work.
- Connector availability may differ by surface. Do not assume a connector is available until invocation is verified.

These are field observations, not claims about undocumented platform internals. Meter rounding, delayed updates, hidden context, and product changes prevent exact token-to-percentage conclusions. Re-test after major product updates.

## Headquarters Rule

The regular ChatGPT LifeOS project is the canonical conversational environment. `LifeOS_HQ` is the shared meeting room, and `Chief_of_Staff_HQ` is Rob's normal daily coordination point.

Use Chat for:

- `Chief_of_Staff_HQ` coordination
- department perspectives and decisions
- planning and prioritization
- recovery, wellness, philosophy, and long-form discussion
- business strategy and offer development
- drafting Work instructions
- light connector actions when connectors are available

Prefer classic desktop when desktop access and connectors are needed without entering the metered Work environment.

Departments remain structured perspectives within one coherent Penny. Work is not another department and should not become a second conversational headquarters.

## Work Rule

Use Work only when the task genuinely requires execution capabilities unavailable or impractical in Chat.

Valid Work triggers include:

- editing or inspecting local files
- running scripts, tests, or terminal commands
- coding, debugging, or building tools
- browser automation or direct website operation
- controlling desktop applications
- moving, transforming, or organizing files
- producing or modifying artifacts
- making bounded GitHub or other system changes when Work is the appropriate available execution surface

Do not use Work merely because a task is important, interesting, lengthy, benefits from conversation, or needs ordinary connector access.

## Work Session Procedure

1. Think and decide in Chat.
2. Define the objective and completion criteria before entering Work.
3. Use the least powerful model likely to succeed.
4. Execute the bounded task.
5. Verify the result.
6. Return the result to Chat and durable storage as needed.
7. Leave Work when execution is complete.

Operating maxim:

> Never idle in Work.

Long exploratory conversation, brainstorming, philosophy, routine planning, and ordinary coordination should remain in regular Chat because Work-side Chat itself can consume limited Work usage without producing a unique execution result.

## Model Selection Policy

### Chat

- Default to the lightest regular-Chat model that can reliably handle the task.
- Use Medium when context handling, connector planning, or multi-step reasoning materially benefits.
- Escalate to stronger reasoning only when the expected quality gain justifies it.
- Regular Chat use on mobile, web, and classic desktop has not been observed to consume the separate weekly Work allowance, but this should be periodically verified after product changes.

### Work

Default to **Luna Light**.

Escalation path:

1. Luna Light
2. Luna Medium when Light is insufficient
3. Terra for substantial implementation or engineering work
4. Sol only when deeper reasoning is materially necessary

Start with the least capable model likely to complete the task safely. Escalate based on evidence, not prestige or availability.

## Work Usage Budget

Work usage is a weekly metered resource.

Current operating rules:

- Treat both Work-side Chat and Work Tasks as metered.
- Record visible usage checkpoints before and after meaningful Work sessions when practical.
- Attribute changes cautiously because the meter may update slowly, round to whole percentages, or change after product-side recalibration.
- Do not infer an exact token-to-percentage conversion from one test.
- Measure value by durable progress per percentage point, not by message count alone.
- Protect Work usage for real execution, paid work, client deliverables, essential repository work, and high-value automation.
- Avoid spending Work allowance to investigate the allowance beyond small controlled tests.
- A free reset or weekly reset does not justify wasteful use.

Suggested categories are flexible rather than fixed quotas:

- real execution and deliverables
- infrastructure and engineering
- controlled product experiments
- emergency reserve

## Task Brief Standard

When Chat determines that Work is required, the owning department should produce a compact Task Brief. `Chief_of_Staff_HQ` may prepare or refine the brief when coordinating daily execution, routing a cross-department dependency, or helping Rob transfer the task into Work.

The Task Brief should contain:

- owning department
- objective
- required actions
- inputs and source-of-truth paths
- constraints and permissions
- completion criteria
- requested completion report

Rob may carry the Task Brief into Work manually until the product provides a reliable native Chat-to-Work bridge.

## Completion Report Standard

A Work result should return:

- status: completed, partial, or blocked
- actions performed
- files or systems changed
- verification completed
- unresolved risks or remaining work
- durable updates needed in GitHub, Drive, Todoist, Calendar, or another authoritative system

Do not claim execution occurred unless the Work environment or a connector confirms it.

## Connector Routing

When light connector work is available in regular Chat, prefer it over opening Work for simple reads or bounded updates.

Examples include:

- pulling Todoist and Calendar information for an itinerary
- reading or updating a small GitHub file
- reviewing Gmail or Drive context
- other ordinary connector-backed coordination

Connector availability is surface-dependent and may change. If one regular-Chat surface lacks the needed connector, try another connector-enabled regular-Chat surface, especially classic desktop, before routing the task to Work.

## Re-Evaluation Triggers

Review this policy when any of the following occur:

- Chat Projects and Work Projects begin syncing
- a native Continue in Work or Send to Work bridge appears
- Work gains mobile support
- connector access changes materially
- Work metering or model tiers change
- observed usage no longer matches this operating model

Until then, preserve continuity in regular Chat and reserve Work for bounded execution.
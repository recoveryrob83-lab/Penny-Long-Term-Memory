# Chat and Work Execution Policy

Updated: 2026-07-15
Project: Life OS Infrastructure
Purpose: Define the operating boundary between regular ChatGPT conversations and the separate Work execution environment.

## Core Model

Life OS uses two distinct operating surfaces:

- **Chat is headquarters.** Use it for conversation, planning, department coordination, writing, strategy, recovery work, philosophy, ordinary reasoning, and light connector work where available.
- **Work is the execution environment.** Use it for local files, terminal access, coding, testing, browser control, desktop applications, artifact production, repository changes, and other tasks that require computer execution.

Short form:

> Chat thinks. Work does. GitHub remembers. Drive holds working documents. The desktop is the execution surface.

## Current Product Boundary

Observed on 2026-07-15:

- Regular Chat conversations and existing ChatGPT Projects are available across mobile, web, and classic desktop surfaces.
- The new desktop Work environment uses separate Projects and Tasks.
- Work Projects created in the new desktop environment did not appear on mobile, web, or classic desktop during a controlled sync test.
- Existing regular ChatGPT Projects did not appear in the new desktop Work environment.
- A Work Project created a Task rather than a normal Chat conversation.
- Connector availability may differ by surface. Do not assume a connector is available until invocation is verified.

These are field observations, not claims about undocumented platform internals. Re-test after major product updates.

## Headquarters Rule

The regular ChatGPT Life OS hub is the canonical conversational headquarters.

Use Chat for:

- Main Assistant coordination
- department perspectives and decisions
- planning and prioritization
- recovery, wellness, philosophy, and long-form discussion
- business strategy and offer development
- drafting Work instructions
- light connector actions when connectors are available

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

Do not use Work merely because a task is important, interesting, lengthy, or benefits from conversation.

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

Long exploratory conversation, brainstorming, philosophy, routine planning, and ordinary coordination should remain in Chat because they can consume limited Work usage without producing a unique execution result.

## Model Selection Policy

### Chat

- Default to GPT-5.5 Instant or the lightest suitable Chat model for routine coordination and conversation.
- Escalate to stronger reasoning only when the expected quality gain justifies it.
- Normal Chat use has not been observed to consume the separate weekly Work allowance, but this should be periodically verified after product changes.

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

- Record visible usage checkpoints before and after meaningful Work sessions when practical.
- Attribute changes cautiously because the meter may update slowly or in batches.
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

When Chat determines that Work is required, Main Assistant should produce a compact Task Brief containing:

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

Connector availability is surface-dependent and may change. If the current Chat surface lacks the needed connector, use another connector-enabled Chat surface or route the task to Work only when necessary.

## Re-Evaluation Triggers

Review this policy when any of the following occur:

- Chat Projects and Work Projects begin syncing
- a native Continue in Work or Send to Work bridge appears
- Work gains mobile support
- connector access changes materially
- Work metering or model tiers change
- observed usage no longer matches this operating model

Until then, preserve continuity in Chat and reserve Work for bounded execution.
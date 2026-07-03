# App Integrations Reference

Updated: 2026-07-02
Project: Life OS / Life Logistics HQ
Purpose: Quick reference for what connected apps Penny can see and when each should be used.
Source: Google Drive `10_APP_INTEGRATIONS_REFERENCE.md`

## Operating Rule

Do not use integrations just because they exist.

Use the right tool for the job:

- GitHub = durable memory, Markdown files, audit trail, commits, diffs, rollback.
- Google Drive = working documents, project files, trackers, Sheets, generated artifacts.
- Todoist = action queue and recurring reminders.
- Calendar = timed appointments and availability.
- Gmail = communications and email evidence.
- Contacts = finding saved people/contact details.
- Indeed = job search and company/job insights.
- AccuWeather = weather-sensitive planning.
- Booking.com = lodging/travel logistics.
- Dropbox = backup/archive/file recovery when needed.

For sensitive actions, read first and change only when Rob clearly asks.

## Connector Wake-Up Rule

If a connector seems unavailable or sleepy in a long-running chat, try explicit connector invocation before starting a fresh chat.

Recommended order:

1. Rob or Penny explicitly names/tags the needed connector, such as `@Google Drive`, `@Gmail`, `@Google Calendar`, or `@Todoist`.
2. Penny attempts a tiny harmless read, such as profile, recent documents, today's calendar, current Todoist tasks, or recent Gmail search.
3. If the connector responds, continue normal work.
4. If it fails or behaves inconsistently, stop over-debugging and use the fresh-chat GitHub boot process.

Status: field-tested observation, not guaranteed connector behavior.

## Connector Safety Failure Pattern

During real-world connector workflows, repeated blocked or failed operations may correlate with a connector becoming unavailable in the current chat.

The mechanism is unknown. Do not assume causation.

Treat safety-triggering payloads as operationally risky because they can interrupt automation.

When a payload appears to trigger safety checks or repeated failures:
- Stop retrying the same payload.
- Simplify, abstract, or split the content.
- Use neutral operational language instead of unnecessary sensitive details.
- Verify connector availability with a tiny harmless read before continuing.
- If the connector remains inconsistent, use the fresh-chat GitHub boot process.

## RPR Procedure: Rob -> Penny -> Rob

Use user-mediated file transfer for any structured file that is likely to trigger connector safety or requires reliable editing.

Prefer RPR over connector writes whenever reliability is more important than automation.

Use connectors for discovery, lookup, scheduling, communication, and metadata, but not as the sole path for maintaining critical structured records.

Examples of RPR-friendly files:
- CSV/XLSX trackers.
- SQLite files.
- JSON exports.
- Profile/reference sheets.
- Sensitive-adjacent structured records.
- Critical project records where connector inconsistency would be costly.

## Important Distinction

Apps visible on Rob's apps page may be installed/authorized or available to the broader ChatGPT app system.

Penny can only call a tool when it is exposed in the current chat's tool layer.

If Rob asks to use one of these apps and Penny has not loaded its tool schema yet, first use tool discovery for that app, then proceed only if the needed action is available.

## Core Life OS Stack

- GitHub.
- Google Drive.
- Todoist.
- Google Calendar.
- Gmail.
- Google Contacts.
- Indeed.
- AccuWeather.
- Dropbox.

## Situation-Specific / Future-Use Apps

- Booking.com: lodging, attractions, rental cars.
- CALL-E: delegated phone calls when Rob wants an AI call made or a business contacted.
- Canva: visual assets, social posts, presentation/design work.
- DealPilot: coupons/deals for online shopping.
- Dupe: finding cheaper lookalikes for products.
- Insight Timer: meditations, sleep tracks, spiritual talks, breathwork.
- Meetup: local/social/community events.
- Simple World Clock: current time/time zones.
- Spotify: music and podcast recommendations.
- Tarot: spiritual/divination-style reflection, if Rob wants that framing.
- Tubi: free movie/show recommendations or trivia.
- Uber: ride fare estimates in the United States.

These apps should not be treated as part of the daily operating system unless they serve an active project.

## GitHub

Primary role:
Durable long-term memory and audit trail.

Can do:
- Read repository files.
- Create Markdown files.
- Update files with commits.
- Preserve history.
- Search files.
- Use issues/PRs if a more formal workflow becomes useful.

Use for:
- Boot files.
- Session handoffs.
- Operating rules.
- Active projects.
- Open loops.
- Strategy/implementation workflow files.
- Long-term personal-assistant memory.

Current Life OS relevance:
GitHub is being promoted as the preferred source of truth for durable memory as of 2026-07-02.

## Google Drive

Primary role:
Operational workspace.

Can do:
- Search Drive files.
- List folders.
- Create Google Docs, Sheets, and Slides.
- Edit Docs and Sheets.
- Fetch/read Docs, Sheets, Slides, and some files.
- Export files.
- Get file metadata.
- Create folders.
- Move/rename files when connector safety checks allow it.

Known limitations:
- Raw Markdown creation is not clean through the connector.
- Some folder moves/copies can be blocked by safety checks.
- Link integrity matters more than perfect folder placement.
- Long-running chats may experience connector invocation degradation.
- Explicit `@Google Drive` invocation may help wake or route the connector before a fresh chat is needed.
- Repeated blocked or failed operations may correlate with connector unavailability in the current chat. Mechanism unknown; treat safety-triggering payloads as operationally risky.
- RPR should be preferred over direct connector writes for critical structured records when reliability matters more than automation.

Use for:
- Working documents.
- Checkbook Register.
- Finance trackers.
- Job-search artifacts.
- PDFs/generated files.
- Google Docs and Sheets that Rob will open/edit directly.

## Todoist

Primary role:
Action/reminder engine.

Use for:
- Daily recovery anchors.
- Weekly Life OS reviews.
- Project pushes.
- Calls and deadlines.
- Small actionable next steps.

Do not use for:
- Storing full context.
- Replacing GitHub/Drive project files.

## Google Calendar

Primary role:
Time-based commitments.

Use for:
- Interviews.
- Appointments.
- Meetings.
- Phone calls with exact scheduled times.
- Focus blocks.

Rule:
Calendar is for events that happen at a time. Todoist is for actions. GitHub/Drive are for context.

## Gmail

Primary role:
Email communications and email-based evidence.

Use for:
- Job search emails.
- Application confirmations.
- Benefits/caregiver correspondence.
- Drafting emails for Rob to review.
- Organizing important communications.

Rule:
Draft unless Rob explicitly asks to send now.

Limitation:
Not all communications live in Gmail. Interview logistics or last-minute links may arrive by SMS/text message and require Rob to share them directly.

## Google Contacts

Primary role:
Find saved contact details.

Use for:
- Finding email addresses or phone numbers before emailing, inviting, or calling.

## Indeed

Primary role:
Job search and employment research.

Use for:
- Finding jobs near Rob.
- Remote or entry-level searches.
- Interview/company research.
- Salary or company culture checks.

Current Life OS relevance:
- Job Search project.
- Wendy's interview preparation if company/job research is useful.
- Future marketing, social media, customer service, or entry-level job searches.

## AccuWeather

Primary role:
Weather-sensitive planning.

Use for:
- Planning errands, calls, appointments, bus trips, cleanup days, yard work, or recovery meetings.
- Checking weather before Marqueto house cleanup logistics.
- Transportation planning.

## Booking.com

Primary role:
Travel/lodging logistics.

Use for:
- Emergency lodging search.
- Future travel planning.
- Finding stays near appointments, interviews, recovery events, or family needs.
- Rental car checks if transportation planning ever requires it.

Current Life OS relevance:
Situational only. Not active unless housing/travel/transportation needs arise.

## Dropbox

Primary role:
Backup/archive and legacy file access.

Use for:
- Old Life OS archive.
- Backup/reference copies.
- Recovering files if Dropbox was used earlier.
- Discovery or metadata checks for manually uploaded files.

Rule:
Dropbox is not the main Life OS workspace. GitHub and Google Drive now carry primary memory/workspace roles.

Do not rely on Dropbox connector reads/writes as the only path for maintaining critical structured records. Use RPR when reliability matters.

## SMS / Phone Messages

Primary role:
External communication channel not directly visible to Penny unless Rob shares the content.

Use for:
- Interview logistics received by text.
- Last-minute Zoom links or recruiter updates.
- Calls or texts that need manual summary into Life OS.

Rule:
When Gmail lacks expected interview details, check whether the missing evidence may be in SMS or phone messages before assuming the email search failed.

## Situation-Specific Use Cases

### Caregiver Income Project

Best tools:
- Web/current research if public policy facts are needed.
- GitHub for durable findings and project state.
- Google Drive for working project documents.
- Todoist for next actions and calls.
- Gmail for correspondence.
- Calendar for scheduled calls/appointments.
- Contacts if Marqueto/contact records are saved.
- RPR for structured records that need reliable editing or may trigger connector safety.

### Cleanup Project

Best tools:
- Web/current research for local cleanup providers.
- AccuWeather for cleanup/weather planning.
- Todoist for calls.
- Drive for quotes and call logs.
- GitHub for durable state/open loops.
- Calendar if a pickup/estimate is scheduled.
- RPR for critical structured trackers if connector reliability becomes a problem.

### Job Search

Best tools:
- Indeed for job searches and company research.
- Gmail for job emails.
- Drive for resumes, cover letters, and application tracker.
- Todoist for application/interview tasks.
- Calendar for interviews.
- SMS/phone messages for texted interview logistics.
- GitHub for durable job-search project status.
- RPR for critical application trackers if connector reliability becomes a problem.

### Finance & Benefits

Best tools:
- Drive/Sheets for trackers.
- Gmail for benefit notices or financial emails if Rob asks.
- Todoist for deadlines and paperwork tasks.
- Calendar for appointments.
- GitHub for durable finance/benefits project state.
- RPR for structured records where reliability and privacy are more important than automation.

### Recovery Logistics

Best tools:
- Todoist for daily/weekly anchors.
- Calendar for scheduled meetings or calls.
- Drive for recovery working files.
- GitHub for durable recovery logistics state.
- AccuWeather for transportation/weather planning.

### Housing / Emergency Logistics

Best tools:
- Booking.com for lodging if needed.
- AccuWeather for travel/weather.
- Calendar for appointments.
- Todoist for immediate actions.
- Drive for housing notes.
- GitHub for durable state.
- RPR for critical structured records if connector reliability becomes a problem.

## Future Penny Startup Note

When booting Life OS, read this file after Boot Log, Session Handoff, Active Projects, and Open Loops if the user asks about available tools, integrations, connector troubleshooting, or which app to use.

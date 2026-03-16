---
description: "Personal OS / Digital Twin — orchestrates screenpipe intelligence, vault knowledge, and external services into briefings, decisions, and autonomous actions."
---

# Command Center

**The Command Center turns your vault into a digital twin — a system that knows what you know, reasons with your priorities, and acts on your behalf.**

## When to Use

- **Session start**: Generate a morning/session briefing
- **"What should I focus on?"**: Priority analysis
- **"What was I doing N hours ago?"**: Screenpipe activity query
- **"Prepare for meeting with X"**: Meeting context prep
- **"Should I accept/do X?"**: Decision engine
- **"Triage stale items"**: Staleness sweep
- **"Draft a reply to X"**: High-risk draft (approval required)
- **Any dendron-add/query/generate pattern**: Pass through to existing skill

## Three-Tier Memory System

| Tier | File | Purpose | Refresh |
|------|------|---------|---------|
| **Working Memory** | `notes/_working-memory.md` | Hot index: today's focus, calendar, inbox, recent people, live tasks. | Every session |
| **Context Model** | `memory/command-center.md` | Medium-term: follow-ups, momentum, collaborator state, decision patterns. | End of each session |
| **Vault** | `notes/*.md` | Long-term: person profiles, projects, topic notes, journals. | When data arrives |

**Always read in this order**: Working Memory → Context Model → Vault (as needed).

## Source Sync Matrix

Each data source has a defined cadence, output destinations, and cache key to avoid redundant fetches.

| Source | Cadence | Cache Key | Short-term Output | Long-term Output |
|--------|---------|-----------|-------------------|-----------------|
| **Calendar** | Every session | `_working-memory.md` header: `Calendar (synced HH:MM)` | Today's events + 7-day preview | Update `user.*.md` with last-meeting dates |
| **Email** | Every session | `_working-memory.md` header: `Email (synced YYYY-MM-DD)` | Inbox triage (Needs Action / Scheduled / Tracking) | Update `user.*.md` with new interaction context, new follow-ups → `command-center.md` |
| **Screenpipe** | Every session | `.cache/cc-screenpipe-YYYY-MM-DD-*.json` | Last 4–6 hours activity table | Daily journal entries, people interaction dates in `user.*.md` |

### Sync Rules

1. **Check cache before fetching.** If a source's cache key shows it was synced today (or within 1 hour for calendar), skip re-fetch. The user can say "refresh" to force.
2. **Short-term writes go to `_working-memory.md`.** This file is the single pane of glass for "what's active right now."
3. **Long-term writes go to vault notes.** When a source reveals a new person interaction, update the relevant `user.*.md` with the date and context. When a source reveals a follow-up, add it to `command-center.md`.
4. **People are the connective tissue.** Every source can surface people interactions. ALL of them should flow into the person's `user.*.md` note — not just the source that created the note originally.
5. **Incremental by default.** Never reprocess unchanged data. Email uses date cache. Screenpipe uses preprocessor cache. Calendar is always live (it's cheap).

---

## Session-Start Briefing

### Step 1: Check Cache

Read `.cache/cc-briefing-YYYY-MM-DD.json` in the vault directory. If it exists and is <1 hour old, present the cached briefing with: "Cached from {time}. Say 'refresh' for live data." Then skip to Step 4.

### Step 1.5: Launch Sync Pipeline (background)

Invoke the `/sync` skill in background mode. This dispatches calendar, email, and screenpipe adapters in parallel. Manifests are applied by the vault-updater as they arrive.
The briefing agents (Step 2) run concurrently using cached state — they don't wait for sync.

### Step 2: Dispatch 5 Parallel Agents (with sync pipeline running in background)

Send a **single message with 5 Agent tool calls** for maximum parallelism. Use the prompt templates below.

#### Agent 1: Calendar Agent (foreground)

```
You are the Calendar Agent for {{USER_NAME}}'s command center briefing.

**Task**: Get today's and next 7 days' events from Google Calendar.

**Optimization**: If the sync pipeline has already run this session (check for a fresh
`.cache/sync-state/calendar-manifest-*.json` file from today), read the manifest's working
memory changes instead of calling gcal_list_events again. Only call the API if no fresh
manifest exists.

**Steps**:
1. Call gcal_list_events for today and next 7 days
2. For each meeting, check if there's a matching vault note:
   - Look for meet.YYYY.MM.DD.md files
   - Look for user.*.md files matching attendee names
3. Flag meetings that have NO vault prep (new contacts, no past meetings)

**Output format** (markdown):
## Today's Events
- [time] [event name] — [attendees if any] — [vault links if found]

## Next 7 Days
- [date] [time] [event] — [notes]

## Needs Prep
- [events with unknown attendees or no past meeting notes]

**Constraints**:
- If calendar MCP is unavailable, output: "Calendar: unavailable (MCP not connected)"
- Never fabricate events
- Keep output concise
```

#### Agent 2: Continuity Agent (foreground)

```
You are the Continuity Agent for {{USER_NAME}}'s command center briefing.

**Task**: Determine what {{USER_NAME}} was working on and what's unfinished.

**Steps**:
1. Read notes/_working-memory.md (if it exists)
2. Read memory/command-center.md (context model)
3. Find the most recent daily.journal.*.md file and read its "State & Open Questions" and "Tasks" sections
4. Extract:
   - Current focus areas
   - Uncompleted tasks (- [ ] items)
   - Open questions from last session
   - Carry-forward items

**Output format** (markdown):
## Last Session
- Date: [date]
- Focus: [what was being worked on]

## Carry-Forward
- [unfinished tasks with source links]
- [open questions]

## Current Focus
- Primary: [main thing]
- Secondary: [other active items]

**Constraints**:
- Read REAL files, don't guess content
- If _working-memory.md doesn't exist, rely on daily journal
- Quote specific tasks verbatim from source files
```

#### Agent 3: Staleness Agent (foreground)

```
You are the Staleness Agent for {{USER_NAME}}'s command center briefing.

**Task**: Find overdue tasks, stale projects, and forgotten follow-ups.

**Steps**:
1. Grep for "- [ ]" across recent daily.journal.*.md and meet.*.md files
2. For each unchecked task, calculate age (days since the file date)
3. Check proj.*.md files — flag any not updated in >30 days
4. Check meeting action items (meet.*.md) — flag follow-ups >7 days old

**Thresholds**:
- Tasks >14 days: "Needs Triage"
- Meeting follow-ups >7 days: "Overdue Follow-Up"
- Projects >30 days no update: "Stale Project"

**Output format** (markdown):
## Overdue Follow-Ups (>7 days)
- [task] — from [source file] — [age] days old

## Tasks Needing Triage (>14 days)
- [task] — from [source file]

## Stale Projects
- [project] — last updated [date]

**Constraints**:
- Only report items with REAL dates from filenames/timestamps
- Max 10 items per category
- Sort by age (oldest first)
```

#### Agent 4: Screenpipe Agent (foreground)

```
You are the Screenpipe Agent for {{USER_NAME}}'s command center briefing.

**Task**: Summarize recent activity from screenpipe data.

**Steps**:
1. Check for preprocessed cache files at notes/.cache/cc-screenpipe-YYYY-MM-DD-*.json
2. If cache exists, read and summarize sessions
3. If no cache, try running: python3 scripts/preprocess_screenpipe.py --date [today] --stats-only
4. If preprocessor fails, try the screenpipe MCP search-content tool for the last 2 hours
5. Summarize: what apps were used, what was being worked on, any notable interactions

**Output format** (markdown):
## Recent Activity
| Time Range | Activity | App | Duration |
|------------|----------|-----|----------|
| [times] | [what] | [app] | [min] |

## Key Observations
- [what's being actively worked on]
- [notable people interactions]

**Constraints**:
- If screenpipe is unavailable, output: "Screenpipe: unavailable"
- Summarize, don't dump raw data
- Focus on the last 4-6 hours
```

#### Agent 5: Insight Agent (background)

```
You are the Insight Agent for {{USER_NAME}}'s command center briefing.

**Task**: Find 0-2 non-obvious connections across the vault that are relevant NOW.

**Steps**:
1. Read notes/_index.by-person.md, notes/_index.by-project.md, notes/_index.by-topic.md
2. Cross-reference: are there people connected to multiple active projects?
3. Check: are there topic notes relevant to current work that haven't been referenced recently?
4. Look for: deadline convergences, people who should be connected, resources relevant to active projects

**Rules**:
- MAX 2 insights. Zero is fine if nothing is genuinely interesting.
- Each insight must connect at least 2 vault entities
- Never force connections

**Output format** (markdown):
## Connections
- [Insight with specific vault links and reasoning]

OR

## Connections
(No non-obvious connections found today.)
```

### Step 3: Compose Briefing

After all foreground agents return, compose the briefing:

```markdown
# {Greeting}, {{USER_NAME}}. {DayOfWeek}, {Month} {Day}

## Right Now
- [Calendar: today's events, linked to vault notes]
- [Screenpipe: what you were just doing, if data exists]
- [Continuity: carry-forward from last session]
- [Blockers: anything explicitly flagged]

## This Week
- [Upcoming meetings/deadlines, next 7 days]
- [Overdue follow-ups with age and source links]
- [Open meeting action items >7 days]

## Strategic View
- [Project momentum table from context model]
- [Key deadlines approaching]
- [Stale items needing triage (max 3)]

## Suggested Actions (max 5, ordered by urgency)
- [Each with reasoning: "Because X deadline is in 3 days..."]

## Connections (only if Insight Agent returned something)
- [Cross-entity insights, 0-2 max]
```

**Deduplication**: If multiple agents surface the same item, show it once in the most relevant section.

### Step 4: Cache & Update

1. Write briefing JSON to `.cache/cc-briefing-YYYY-MM-DD.json`
2. Update `memory/command-center.md` with session date and any new follow-ups discovered
3. Update `_working-memory.md` with standardized sync headers and new data:

```markdown
## Source Sync Status
| Source | Last Synced | Status |
|--------|------------|--------|
| Calendar | YYYY-MM-DD HH:MM | ok |
| Email | YYYY-MM-DD | ok |
| Screenpipe | YYYY-MM-DD HH:MM | ok / unavailable |
```

4. **Long-term writeback**: Handled by vault-updater via sync manifests. No manual writeback needed here.

---

## Screenpipe Intelligence Pipeline

**Handled by the `screenpipe-sync` adapter.** See `skills/sync/screenpipe-sync/SKILL.md`.

The screenpipe-sync adapter runs as part of the `/sync` pipeline at session start. It consumes preprocessed screenpipe data and produces a manifest that the vault-updater applies.

---

## Reactive Command Routing

When the user asks something, match to the appropriate handler:

| Pattern | Route | Risk |
|---------|-------|------|
| "What should I focus on?" | Priority analysis: context model + calendar + deadlines | Read-only |
| "What was I doing N hours ago?" | Query preprocessed screenpipe cache for that time window | Read-only |
| "What did I discuss with X?" | Invoke `dendron-query` with person intent | Read-only |
| "Draft a reply to X's email" | Read Gmail via MCP, draft in user's voice, **present for approval** | High-risk |
| "Update [project] status" | Edit proj.*.md frontmatter/content | Low-risk (auto) |
| "Mark X as done" | Find `- [ ]` in source note, change to `- [x]` | Low-risk (auto) |
| "Schedule follow-up with X" | `gcal_create_event` + meeting stub, **ask first** | High-risk |
| "Prepare for meeting with X" | Person profile + past meetings + recent screenpipe + calendar | Read-only |
| "Summarize my week/month" | Invoke `dendron-generate` with date range | Read-only |
| "Triage stale items" | Show staleness results, accept batch decisions | Mixed |
| "Should I accept [invitation/talk]?" | Decision engine (below) | Read-only |
| dendron-add/query/generate patterns | Pass through to existing skill | Varies |

---

## Decision Engine

When asked "Should I...?", "What should I prioritize?", or similar:

1. **Gather context**: Read relevant vault notes, calendar, screenpipe activity, context model
2. **Apply user's priorities**: From their priorities file, stated goals, decision patterns in context model
3. **Reason transparently**: Show the factors considered, not just the conclusion
4. **Present as recommendation**: "I'd recommend X because [reasons]. But consider Y if [condition]."
5. **Never fabricate**: If data is missing, say so explicitly

### Decision factors to weigh:
- Calendar load (next 7 days)
- Active deadlines (submissions, deliverables, applications)
- Project momentum (from context model)
- Energy patterns (how many consecutive days on same task?)
- Stated priorities (from priorities file and recent decisions)

---

## Meeting Context Prep

When a meeting is detected or "prepare for meeting with X" is requested:

1. **Identify attendees** → look up `user.*.md` profiles
2. **Find past meetings** → `meet.*.md` with same attendees
3. **Extract open threads** → unresolved `- [ ]` items from past meetings
4. **Check recent activity** → screenpipe data for work related to meeting topics
5. **Compose prep brief**: who they are, last interaction, open items, relevant recent work

Dispatch 3 parallel agents: (Person lookup, Past meetings, Recent activity).

---

## Autonomy Tiers

| Tier | Actions | Behavior |
|------|---------|----------|
| **Auto** | Update timestamps, mark tasks done, update context model, cache management, add progress notes | Execute silently, log in context model |
| **Draft & Present** | Draft emails, create calendar events, archive projects, send messages, create new notes | Show draft, wait for approval |
| **Read-only** | Queries, summaries, briefings, decision analysis, meeting prep | Always safe, no confirmation needed |

---

## Auto-Decay Thresholds

| Item Type | Threshold | Action |
|-----------|-----------|--------|
| Unchecked tasks (`- [ ]`) | >14 days | Surface in briefing "Needs Triage" |
| Meeting follow-ups | >7 days no completion evidence | Surface as "Overdue Follow-Up" |
| Project notes | No update >30 days | Flag for status review |
| Dismissed items | After user-set delay (default 14 days) | Re-surface once, then archive |

---

## Working Memory Management

### Update Triggers
- After screenpipe analysis completes
- After briefing composition
- When user explicitly changes focus
- At session end (auto-update)

### Daily Rollover
At end of day (or next morning's first session):
1. Read current `_working-memory.md`
2. Summarize key items into daily journal if not already captured
3. Reset working memory for new day, carrying over unresolved items

### Working Memory Template

```markdown
---
id: [existing-id]
title: Working Memory
desc: 'Hot index of current state — auto-updated by command center'
updated: [timestamp]
created: [existing-created]
---

## Current Focus
- **Primary**: [main task/project]
- **Secondary**: [other active items]
- **Context**: [brief description of where things stand]

## Today's Activity (from screenpipe)
| Time | Activity | Duration | Key Detail |
|------|----------|----------|------------|

## Live Tasks
- [ ] [task with source link]

## People Interacted With Today
- **[Name]**: [context] ([vault link])

## Recent Decisions
- [decision with date]

## Insights
- [observation or realization]
```

---

## Context Model Management

The context model (`memory/command-center.md`) persists across sessions.

### Auto-update (low-risk):
- Session date and focus
- Momentum scores (from vault timestamps + screenpipe)
- Collaborator last-contact dates
- Completed follow-ups

### Ask first:
- Priority changes
- Decision pattern updates
- Permanent suppressions
- Archiving projects

### Pattern Learning
After each decision recommendation:
- If the user accepts → reinforce the pattern
- If the user overrides → note the exception
- Patterns are descriptive ("tends to"), not prescriptive ("always")

---

## Integration with Existing Skills

| Skill | How Command Center Uses It |
|-------|---------------------------|
| `dendron-add` | Route content additions |
| `dendron-query` | Delegate person/project/topic queries |
| `dendron-generate` | Delegate report/summary generation |
| `detect-people` | Call when screenpipe surfaces unknown people |
| `screenpipe-query` | Ad-hoc screenpipe queries beyond preprocessed cache |
| `screenpipe-daily-journal` | Daily journal generation (complementary) |

## External Services (via MCP)

| Service | Tools | Used For |
|---------|-------|----------|
| Google Calendar | `gcal_list_events`, `gcal_create_event`, etc. | Events, scheduling, meeting prep |
| Gmail | `gmail_search_messages`, `gmail_read_message`, `gmail_create_draft` | Email context, follow-ups, drafts |
| Screenpipe | `search-content`, `export-video` + `screenpipe://context` | Real-time activity, transcripts |

## Vault Data Sources

| Source | Query Method | Used For |
|--------|-------------|---------|
| `daily.journal.*.md` | Read latest, grep tasks | Continuity, task tracking |
| `meet.*.md` | Grep action items | Follow-up tracking, meeting prep |
| `proj.*.md` | Read frontmatter timestamps | Momentum scoring |
| `user.*.md` | Read profiles | People context |
| `_index.by-*.md` | Read directly | Cross-entity insights |
| Priorities file | Read | Strategic priorities |

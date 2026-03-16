# Daily Journal Generator

Generate high signal-to-noise daily journal entries from screenpipe recordings using a **two-step process**: a script extracts raw data, then the agent formats it into the final journal.

## Key Principles

- Optimize for future retrieval value, not completeness
- Compress continuous work sessions into single entries
- Only include audio quotes with actual content (skip noise/testing)
- Only embed screenshots that are irreconstructible (skip terminal/code)
- State & Open Questions first (what you'll actually need when resuming work)
- Notes section contains valuable synthesis (make it prominent)

## NON-NEGOTIABLE Requirements

Every journal MUST have:

1. **Screenshots**: At least 1-3 keyframes extracted and embedded. Zero-screenshot journals are REJECTED.
2. **People Detection**: Every person mentioned in audio/OCR must be linked. Create entries for new people via the `detect-people` skill.
3. **Synthesized Content**: Timeline entries must contain human-readable synthesis. Raw OCR dumps are REJECTED. If OCR is garbled, describe what was happening based on context clues (app names, timestamps).
4. **Meeting Detection**: Any Zoom/Teams/Meet participant list in OCR = a meeting happened. Identify it, extract participants, link people. Substantial meetings (>1 hour) get separate meeting notes.
5. **Correct Timeline Ordering**: Day runs 6 AM to 6 AM next day. Morning first, late night last.

## Meeting Notes vs Daily Journal

When audio indicates a substantial meeting (>1 hour, rich content):

1. **Create a separate meeting note** with factual, topic-based organization (action items, topic sections, direct quotes as blockquotes)
2. **Reference it in the daily journal** timeline with a brief summary and link
3. Keep timeline entry brief -- full content lives in the meeting note

## Architecture

```
+-------------------------------------------------------------+
| STEP 1: Script (Data Extraction)                            |
| - Query screenpipe OCR/audio data                           |
| - Output: Raw JSON with hourly buckets                      |
+----------------------------+--------------------------------+
                             |
                             v
+-------------------------------------------------------------+
| STEP 2: Agent (Analysis & Formatting)                       |
| - Read raw JSON                                             |
| - Detect people (invoke detect-people skill)                |
| - Analyze content, group by work session                    |
| - Identify key moments, extract keyframes                   |
| - Write formatted journal                                   |
+-------------------------------------------------------------+
```

**Why two steps?**
- Script = lightweight, fast, no AI needed
- Agent = intelligent analysis with full context -- understands which moments matter, creates people entries, selects keyframes based on content value

## Timezone Configuration

> **Set your local timezone.** Screenpipe outputs UTC timestamps (Z suffix). All human-readable times in the journal must be converted to local time. Update the config with your offset (e.g., `America/Los_Angeles` = UTC-8/UTC-7).

## Quick Start

```bash
# Step 1: Extract raw data
bash scripts/extract_raw_data.sh 2026-03-14

# Step 2: Ask the agent to format
# "Format the raw journal data for 2026-03-14 into a journal following the daily-journal skill template"
```

## Raw Data Format

The script outputs structured JSON to `.cache/journal_raw_YYYY_MM_DD.json`:

```json
{
  "date": "2026-03-14",
  "day_boundaries": {"start": "2026-03-14T06:00:00-05:00", "end": "2026-03-15T06:00:00-05:00"},
  "total_items": 1200,
  "hourly_data": {
    "9": {
      "ocr": [{"text": "...", "timestamp": "...", "activity": "..."}],
      "audio": [{"text": "...", "timestamp": "..."}],
      "activities": {"Coding - Python": 8, "Email": 3}
    }
  },
  "summary_stats": {"total_hours_active": 8, "top_activities": {"Coding": 40}}
}
```

## Journal Template

```markdown
---
id: <23-char-lowercase-alphanumeric>
title: 'YYYY.MM.DD'
desc: 'Brief description naming actual projects/activities'
updated: <unix-ms>
created: <unix-ms>
---

## Day Summary

2-3 sentences covering main activities and people involved. Name specific projects.

## State & Open Questions

**Project A (with Collaborator)**
- Status: Current state
- Blocker: What's blocking (if anything)
- Next: What needs to happen next

**Project B**
- Status: Where things stand
- Decision: Key decision made today

## Tasks

### Inferred from Today

- [ ] Specific actionable task
- [ ] Follow up with [[Person|user.person]] about X

### Completed Today

- [x] Specific accomplishment
- [x] Meeting with [[Person|user.person]] about X

## Timeline

<!-- Use activity-type cards: dev, research, meeting, email, general -->
<!-- Group by work sessions and context switches, not time-of-day labels -->
<!-- Embed screenshots OUTSIDE HTML divs (markdown images don't render inside) -->
<!-- Use HTML formatting inside divs: <strong>, <em>, <a href="...">, <p> -->

<div class="timeline-container">
  <div class="timeline-line"></div>
  <div class="timeline-item">
    <div class="timeline-dot dot-meeting"></div>
    <div class="timeline-time">9:00 AM - 10:30 AM</div>
    <div class="timeline-card card-meeting">
      <div class="timeline-title">Meeting Title</div>
      <div class="timeline-content">
        <p>Summary with <a href="user.person.md">Person Name</a>.</p>
      </div>
    </div>
  </div>
</div>

![Screenshot description](assets/journal_YYYY-MM-DD_moment_1.png)

<div class="timeline-container">
  <div class="timeline-line"></div>
  <div class="timeline-item">
    <div class="timeline-dot dot-dev"></div>
    <div class="timeline-time">11:00 AM - 1:00 PM</div>
    <div class="timeline-card card-dev">
      <div class="timeline-title">Development Session</div>
      <div class="timeline-content">
        <p>Built X feature. <strong>Blocker</strong>: Missing API docs.</p>
      </div>
    </div>
  </div>
</div>

## Notes

Patterns, meta-observations, collaboration dynamics, technical insights, strategic context.
This section is the highest-value synthesis -- not a restatement of the timeline.
```

## Agent Workflow

When invoked, the agent should:

1. **Run data extraction** to get raw JSON
2. **Detect people** -- search audio/OCR for names, invoke `detect-people` skill for new entries
3. **Read raw JSON** -- sample key hours, understand activity patterns
4. **Format journal** -- Day Summary, State, Tasks, Timeline, Notes
5. **Identify key moments** needing screenshots (meetings, debugging, decisions)
6. **Extract keyframes** at specific timestamps from raw JSON
7. **Embed screenshots/videos** in timeline (images outside HTML divs)
8. **Write formatted journal** to `daily.journal.YYYY.MM.DD.md`

## Validation Checklist

Before marking complete, verify:

- [ ] Screenshots embedded (at least 1 keyframe)
- [ ] People detected and linked (all names from audio/OCR)
- [ ] Meetings identified (Zoom/Teams/Meet participant lists)
- [ ] Timeline ordering correct (6 AM top, late night bottom)
- [ ] Content synthesized (no raw OCR dumps)
- [ ] Audio quotes meaningful (decisions/ideas only, no noise)
- [ ] Notes section has synthesis (not restating timeline)

**If any item fails, fix it before writing the journal file.**

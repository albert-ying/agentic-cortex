---
description: "Sync Google Calendar events into vault manifest. Runs at session start."
---

# Calendar Sync Adapter

Pulls events from Google Calendar, diffs against snapshot, produces a manifest
of vault note updates.

## When to Use

Called by the `/sync` router. Not invoked directly.

## Process

### 1. Pull Events

Call `gcal_list_events`:
- Range: 7 days ago to 14 days ahead
- Include: event title, start/end time, attendees (names + emails), description, location

### 2. Load Snapshot

Read `.cache/sync-state/calendar-snapshot.json`. If missing, treat all events as new.

Snapshot format:
```json
{
  "synced_at": "2026-03-12T10:00:00Z",
  "events": {
    "<event_id>": {
      "title": "...",
      "start": "...",
      "attendees": ["..."],
      "status": "confirmed"
    }
  }
}
```

### 3. Diff

Compare current events against snapshot:
- **New events**: event ID not in snapshot
- **Changed events**: event ID exists but title/time/attendees differ
- **Cancelled events**: event ID in snapshot but not in current pull (or status=cancelled)

### 4. Match Against Vault Index

Load `.cache/sync-state/vault-index.json`.

For each new/changed event:
1. Extract keywords from: event title, attendee names, description text
2. Match against vault index entries using keyword overlap
3. For each attendee name, check for `type: "person"` matches
4. Read the full content of top candidate notes (up to 10 per event)
5. Decide which notes need updating and what sections to change

### 5. Generate Manifest

For each matched note, emit a change entry:

**Person notes** (`user.*.md`):
- Action: `rewrite_section`, section: `## Current Status`
- Content: Update with upcoming/recent meeting info
- Confidence: 0.9+ (calendar data is high-fidelity)

**Meeting notes** (`meet.YYYY.MM.DD.md`):
- Action: `create_note` if the meeting doesn't have a note yet and is today/tomorrow
- Frontmatter: `{title: "Meeting Title", desc: "With [attendees]"}`
- Content: Stub with attendee list and agenda from event description
- Confidence: 0.85

**Project/other notes**:
- Action: `rewrite_section` or `append` to relevant status/activity sections
- Confidence: 0.8+ if event title clearly matches project keywords

**Working memory**:
- Action: `rewrite_section`, section: `## Today's Calendar`
- Content: Today's events formatted as time/event/attendees/vault-links
- Confidence: 1.0

### 6. Save Manifest and Update Snapshot

Write manifest to `.cache/sync-state/calendar-manifest-<timestamp>.json`.
Update snapshot with current event state.

## Output

The manifest JSON file path, printed to stdout.

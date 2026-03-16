---
description: "Sync Gmail messages into vault manifest. Runs at session start."
---

# Email Sync Adapter

Pulls recent emails from Gmail, diffs against snapshot, produces a manifest
of vault note updates.

## When to Use

Called by the `/sync` router. Not invoked directly.

## Process

### 1. Pull Emails

Two queries:
1. `gmail_search_messages(query="in:inbox -category:promotions -category:social", maxResults=25)` — active inbox
2. `gmail_search_messages(query="in:sent newer_than:7d", maxResults=25)` — recent sent

For high-signal threads (starred, from known collaborators, with action items), call
`gmail_read_message` to get full thread content.

### 2. Load Snapshot

Read `.cache/sync-state/email-snapshot.json`. If missing, treat all emails as new.

Snapshot format:
```json
{
  "synced_at": "2026-03-12T10:00:00Z",
  "threads": {
    "<thread_id>": {
      "subject": "...",
      "last_message_id": "...",
      "participants": ["..."],
      "summary": "...",
      "starred": false
    }
  }
}
```

### 3. Diff

- **New threads**: thread ID not in snapshot
- **Updated threads**: thread ID exists but last_message_id differs (new replies)
- **Newly starred**: starred status changed

### 4. Match Against Vault Index

Load `.cache/sync-state/vault-index.json`.

For each new/updated thread:
1. Extract keywords from: subject line, sender name, recipient names, email body
2. Match against vault index using keyword overlap
3. For person names (From/To/CC), check `type: "person"` matches
4. Read full content of top candidate notes
5. Determine which notes need updating

### 5. Generate Manifest

**Person notes** (`user.*.md`):
- Action: `rewrite_section`, section: `## Current Status`
- Content: Latest interaction context from email thread
- Evidence: subject, date, direction (sent/received)
- Confidence: 0.9+ for known contacts, 0.75 for ambiguous name matches

**Project notes** (`proj.*.md`, `personal.grant.*.md`, etc.):
- Action: `rewrite_section` on status/progress sections
- Content: Status updates derived from email content
- Confidence: 0.85+ if subject/body clearly references the project

**Working memory** (`_working-memory.md`):
- Action: `rewrite_section`, section: `## Email Inbox — Active Items (synced YYYY-MM-DD)`
- Content: Triaged inbox — "### Needs Action", "### Scheduled", "### Tracking"
- Each item: checkbox, subject summary, sender, priority, vault link if person exists
- Confidence: 1.0

**Context model follow-ups**:
- For emails with detected action items or deadlines, emit changes targeting
  the relevant notes rather than context model directly (the vault-updater
  handles cross-note synthesis)

### 6. Save Manifest and Update Snapshot

Write manifest to `.cache/sync-state/email-manifest-<timestamp>.json`.
Update snapshot with current thread state.

## Triage Logic

Priority assignment for inbox items:
- **HIGH**: Starred emails, deadlines within 7 days, emails from important contacts awaiting response
- **MEDIUM**: Project-related emails, invitations, requests from known contacts
- **LOW**: FYI, newsletters that made it to inbox, tracking items

If the vault index includes a `tier` field on person notes, use it to boost priority
for high-tier contacts. This is optional — the adapter works without tier data.

## Output

The manifest JSON file path, printed to stdout.

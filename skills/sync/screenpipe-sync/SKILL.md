---
description: "Sync screenpipe activity data into vault manifest. Runs in background after briefing."
---

# Screenpipe Sync Adapter

Reads preprocessed screenpipe data, diffs against snapshot, produces a manifest
of vault note updates.

## When to Use

Called by the `/sync` router. Runs in background. Not invoked directly.

## Process

### 1. Load Preprocessed Data

Read hourly cache files from `.cache/cc-screenpipe-YYYY-MM-DD-*.json` for the last 24 hours.

If no cache exists for today, run the preprocessor:
```bash
python3 scripts/preprocess_screenpipe.py --date today
```

If preprocessor fails, fall back to screenpipe MCP `search-content` for last 2 hours.

### 2. Load Snapshot

Read `.cache/sync-state/screenpipe-snapshot.json`. If missing, treat all data as new.

Snapshot format:
```json
{
  "synced_at": "2026-03-12T10:00:00Z",
  "last_processed_hour": "2026-03-12T09"
}
```

### 3. Diff

Only process hours after `last_processed_hour`. For each new hour:
- Extract sessions (app, window, duration, key_content)
- Extract audio segments (transcriptions)
- Extract entities (people, projects, DOIs, URLs) from the preprocessor output

### 4. Match Against Vault Index

Load `.cache/sync-state/vault-index.json`.

For each session/entity:
1. Match app names and window titles against project keywords
2. Match detected people names against person notes
3. Match OCR text content against vault keywords
4. Read full content of top candidate notes
5. Determine what needs updating

### 5. Generate Manifest

**Project notes** (`proj.*.md`, `sci.*.md`):
- Action: `rewrite_section`, section: `## Current Status`
- Content: Activity summary ("3.5h on ColabFold, ran structure predictions for SOD1 variants")
- Evidence: screenpipe sessions with timestamps
- Confidence: 0.85 for clear app/window matches, 0.65 for OCR-based inference

**Person notes** (`user.*.md`):
- Action: `rewrite_section`, section: `## Current Status`
- Content: Interaction detected (Zoom call, chat window, email window with their name)
- Evidence: screenpipe session with app/window details
- Confidence: 0.8 for video call detection, 0.7 for chat/email window inference

**Tool notes** (`sci.tools.*.md`, `tool.*.md`):
- Action: `append`, section: `## Usage Log` (or create it)
- Content: Usage session detected with duration
- Confidence: 0.75

**Working memory** (`_working-memory.md`):
- Action: `rewrite_section`, section: `## Today's Activity (from screenpipe)`
- Content: Activity table (Time | Activity | Duration | Key Detail)
- Confidence: 1.0

### 6. Save Manifest and Update Snapshot

Write manifest to `.cache/sync-state/screenpipe-manifest-<timestamp>.json`.
Update snapshot with last processed hour.

## Output

The manifest JSON file path, printed to stdout.

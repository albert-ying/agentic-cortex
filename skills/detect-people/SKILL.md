# Detect People

Create user entries for people detected in screenpipe data. Uses AI judgment to filter false positives.

## Usage

```bash
# Run candidate extraction
python3 scripts/extract_candidate_names.py --date 2026-03-14

# Then validate candidates and create entries (agent step)
```

## 4-Step Process

### 1. Extract candidates

```bash
python3 scripts/extract_candidate_names.py --date YYYY-MM-DD
```

Returns JSON with OCR/audio candidates and existing user slugs.

### 2. Validate with AI judgment

For each candidate, determine if it's a real person:

- **Create entry** -- real person with professional context
- **Link to existing** -- audio name matches existing user phonetically
- **Skip** -- UI element, device name, OCR artifact

**Skip rules** -- these are NOT people:
- UI elements: "App Store", "Enhanced Context", "System Preferences"
- Device names: "HyperX SoloCast", "MacBook Pro"
- OCR artifacts: "Starting VideoCapture", "Screenshot Taken"
- Generic labels: "Unknown User", "Admin Panel"

**When in doubt, skip.** A missed person can be added later; a false entry pollutes the vault.

### 3. Create entries with web search

For each validated person:

1. Web search: `name + "professor"` OR `name + "researcher"` OR `name + institution`
2. Extract: institution, role, email (if public), bio summary
3. Create entry with ALL fields filled -- never use placeholders like "[To be filled]"

**If web search finds nothing**: skip creating the entry (likely false positive).

**Generate a 23-character lowercase alphanumeric node ID** for each entry:

```python
import random, string, time
node_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(23))
timestamp_ms = int(time.time() * 1000)
```

**Entry template** (`user.<name-slug>.md`):

```markdown
---
id: <23-char-lowercase-alphanumeric>
title: Full Name
desc: 'One-line role/institution'
updated: <unix-ms>
created: <unix-ms>
---

## Contact Info

- Email: actual-email@example.com
- Institution: University / Company
- Web: https://profile-url

## Role & Expertise

Title and role description.

Brief research or professional summary.

## Context

**How we connected**: Detected from screenpipe journal

**Date**: YYYY-MM-DD

**Context**: Description of how they appeared (meeting, email, mention)

## Notes

Any relevant observations from the detection context.
```

### 4. Return detected people as JSON

Return results for the calling skill (e.g., daily-journal) to use for linking:

```json
{
  "people": [
    {"name": "Sarah Kim", "slug": "sarah-kim", "status": "existing"},
    {"name": "David Lee", "slug": "david-lee", "status": "created"}
  ],
  "summary": {
    "created": 1,
    "linked": 1,
    "skipped": 35
  }
}
```

Brief text summary:
- Created: N entries (list names)
- Linked: N audio names to existing users
- Skipped: N false positives (total only)

---

**Key Principle**: When in doubt, skip. All created entries must be fully populated with real information from web search. No placeholders.

**Auto-run**: This skill is automatically called during the `daily-journal` workflow.

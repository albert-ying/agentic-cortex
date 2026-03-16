#!/usr/bin/env python3
"""Build a JSON index of all vault notes for the sync pipeline to match against.

Scans .md files in a Dendron vault, extracts metadata (title, type, keywords,
tier) from frontmatter and body text, and writes a structured index to
.cache/sync-state/vault-index.json.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Map filename prefixes to semantic types
PREFIX_TYPE_MAP = {
    "user.": "person",
    "proj.": "project",
    "meet.": "meeting",
    "daily.": "journal",
    "sci.": "science",
    "bib.": "bibliography",
    "lang.": "language",
    "tool.": "tool",
    "tags.": "tag",
    "task.": "task",
    "scratch.": "scratch",
    "personal.": "personal",
    "course.": "course",
    "plan.": "plan",
    "prompt.": "prompt",
    "report.": "report",
    "recipes.": "recipe",
    "template.": "template",
    "tutorial.": "tutorial",
    "_index.": "index",
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TITLE_RE = re.compile(r"^title:\s*['\"]?(.+?)['\"]?\s*$", re.MULTILINE)
TIER_RE = re.compile(r"^tier:\s*(.+?)\s*$", re.MULTILINE)


def infer_type(filename: str) -> str:
    """Infer note type from the filename prefix."""
    for prefix, note_type in PREFIX_TYPE_MAP.items():
        if filename.startswith(prefix):
            return note_type
    return "other"


def extract_keywords(title: str | None, body: str) -> list[str]:
    """Extract deduplicated lowercase keywords from title and first 200 chars of body."""
    raw = ""
    if title:
        raw += title + " "
    raw += body[:200]
    # Split on whitespace, strip punctuation, lowercase, deduplicate
    words = re.findall(r"[a-zA-Z0-9\-]+", raw.lower())
    seen = set()
    keywords = []
    for w in words:
        if w not in seen and len(w) > 1:
            seen.add(w)
            keywords.append(w)
    return keywords


def parse_note(filepath: Path) -> dict:
    """Parse a single .md file and return its index entry."""
    filename = filepath.stem
    text = filepath.read_text(encoding="utf-8", errors="replace")

    title = None
    tier = None
    body = text

    fm_match = FRONTMATTER_RE.match(text)
    if fm_match:
        frontmatter = fm_match.group(1)
        body = text[fm_match.end():]
        title_match = TITLE_RE.search(frontmatter)
        if title_match:
            title = title_match.group(1)
        tier_match = TIER_RE.search(frontmatter)
        if tier_match:
            tier = tier_match.group(1)

    return {
        "filename": filename,
        "title": title,
        "type": infer_type(filename),
        "keywords": extract_keywords(title, body),
        "tier": tier,
    }


def build_index(vault_path: Path) -> dict:
    """Scan all .md files and build the full index."""
    notes = []
    for md_file in sorted(vault_path.glob("*.md")):
        if md_file.is_file():
            notes.append(parse_note(md_file))
    return {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "notes": notes,
    }


def main():
    parser = argparse.ArgumentParser(description="Build vault note index for sync pipeline.")
    parser.add_argument("--vault-path", default=".", help="Path to vault directory (default: cwd)")
    args = parser.parse_args()

    vault = Path(args.vault_path).resolve()
    if not vault.is_dir():
        print(f"Error: {vault} is not a directory", file=sys.stderr)
        sys.exit(1)

    out_dir = vault / ".cache" / "sync-state"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "vault-index.json"

    index = build_index(vault)
    out_file.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Indexed {len(index['notes'])} notes -> {out_file}")


if __name__ == "__main__":
    main()

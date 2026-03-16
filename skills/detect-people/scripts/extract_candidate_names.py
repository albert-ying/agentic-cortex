#!/usr/bin/env python3
"""
Extract candidate person names from screenpipe cache files and cross-reference
with existing user entries. Outputs JSON for AI agent validation.

Usage: python3 extract_candidate_names.py --date 2026-03-14
"""

import argparse
import json
import re
import sys
from pathlib import Path

NAME_PATTERN = re.compile(r"\b([A-Z][a-z]+) ([A-Z][a-z]+)\b")


def extract_names_from_text(text, source_label):
    """Extract capitalized two-word name candidates with surrounding context."""
    candidates = {}
    for match in NAME_PATTERN.finditer(text):
        name = match.group(0)
        start = max(0, match.start() - 60)
        end = min(len(text), match.end() + 60)
        context = text[start:end].replace("\n", " ").strip()
        if name not in candidates:
            candidates[name] = {"name": name, "source": source_label, "context": context, "count": 1}
        else:
            candidates[name]["count"] += 1
    return candidates


def load_screenpipe_cache(date_str):
    """Load all hourly screenpipe cache files for the given date."""
    cache_dir = Path.cwd() / ".cache"
    pattern = f"cc-screenpipe-{date_str}-*.json"
    ocr_text = []
    audio_text = []

    for path in sorted(cache_dir.glob(pattern)):
        try:
            data = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        for item in data if isinstance(data, list) else data.get("data", []):
            item_type = item.get("type", "")
            content = item.get("content", {})
            if item_type == "OCR":
                ocr_text.append(content.get("text", ""))
            elif item_type == "Audio":
                audio_text.append(content.get("transcription", ""))

    return "\n".join(ocr_text), "\n".join(audio_text)


def find_existing_users():
    """Find existing user.*.md files in the current directory."""
    slugs = []
    for user_file in Path.cwd().glob("user.*.md"):
        slug = user_file.stem.replace("user.", "", 1)
        if slug and slug != "md":
            slugs.append(slug)
    return sorted(slugs)


def main():
    parser = argparse.ArgumentParser(description="Extract candidate names from screenpipe data")
    parser.add_argument("--date", required=True, help="Date to process (YYYY-MM-DD)")
    args = parser.parse_args()

    ocr_text, audio_text = load_screenpipe_cache(args.date)
    ocr_candidates = extract_names_from_text(ocr_text, "ocr")
    audio_candidates = extract_names_from_text(audio_text, "audio")

    # Merge, preferring audio source when both exist
    all_candidates = {}
    for name, info in ocr_candidates.items():
        all_candidates[name] = info
    for name, info in audio_candidates.items():
        all_candidates[name] = info  # audio overwrites ocr

    candidates_list = sorted(all_candidates.values(), key=lambda x: x["count"], reverse=True)
    existing = find_existing_users()

    output = {
        "date": args.date,
        "candidates": candidates_list,
        "existing_users": existing,
    }
    json.dump(output, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Preprocess screenpipe data into hourly JSON cache files.

Queries the local screenpipe API for OCR and audio data for a given date,
groups results by hour, and writes per-hour cache files to
.cache/cc-screenpipe-YYYY-MM-DD-HH.json.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

SCREENPIPE_BASE = "http://localhost:3030"
CACHE_DIR = ".cache"


def fetch_search(content_type: str, start: str, end: str, limit: int = 100) -> list:
    """Query screenpipe /search endpoint. Returns empty list on failure."""
    params = urlencode({
        "content_type": content_type,
        "start_time": start,
        "end_time": end,
        "limit": limit,
    })
    url = f"{SCREENPIPE_BASE}/search?{params}"
    try:
        with urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("data", [])
    except (URLError, OSError, json.JSONDecodeError) as exc:
        print(f"Warning: screenpipe query failed ({content_type}): {exc}", file=sys.stderr)
        return []


def parse_timestamp(ts: str) -> datetime | None:
    """Parse an ISO timestamp string to datetime, tolerating common formats."""
    for fmt in ("%Y-%m-%dT%H:%M:%S%.fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(ts.rstrip("Z").split(".")[0], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
    return None


def group_by_hour(items: list, key_fn) -> dict[int, list]:
    """Group items into hour buckets (0-23) using key_fn to extract timestamp."""
    buckets = {h: [] for h in range(24)}
    for item in items:
        ts = key_fn(item)
        if ts:
            dt = parse_timestamp(ts)
            if dt:
                buckets[dt.hour].append(item)
    return buckets


def extract_ocr_ts(item: dict) -> str | None:
    """Extract timestamp from an OCR search result."""
    content = item.get("content", {})
    return content.get("timestamp") or item.get("timestamp")


def extract_audio_ts(item: dict) -> str | None:
    """Extract timestamp from an audio search result."""
    content = item.get("content", {})
    return content.get("timestamp") or item.get("timestamp")


def build_sessions(ocr_items: list) -> list[dict]:
    """Convert raw OCR items into session summaries."""
    # Group by app+window to approximate sessions
    app_groups: dict[tuple[str, str], list] = {}
    for item in ocr_items:
        content = item.get("content", {})
        app = content.get("app_name", "Unknown")
        window = content.get("window_name", "")
        key = (app, window)
        app_groups.setdefault(key, []).append(content)

    sessions = []
    for (app, window), entries in app_groups.items():
        # Approximate duration from entry count (each entry ~30s of capture)
        duration_min = max(1, len(entries) * 30 // 60)
        # Key content: first 200 chars from the first entry's text
        text_parts = []
        for e in entries:
            t = e.get("text", "")
            if t:
                text_parts.append(t)
        key_content = " ".join(text_parts)[:200].strip()
        sessions.append({
            "app": app,
            "window": window,
            "duration_min": duration_min,
            "key_content": key_content,
        })
    return sessions


def build_audio(audio_items: list) -> list[dict]:
    """Convert raw audio items into audio summaries."""
    results = []
    for item in audio_items:
        content = item.get("content", {})
        ts = content.get("timestamp") or item.get("timestamp", "")
        dt = parse_timestamp(ts) if ts else None
        time_str = dt.strftime("%H:%M") if dt else ""
        text = content.get("transcription", "") or content.get("text", "")
        duration_sec = content.get("duration", 30)
        if text.strip():
            results.append({
                "time": time_str,
                "text": text.strip()[:500],
                "duration_sec": duration_sec,
            })
    return results


def process_date(date_str: str, cache_dir: str, stats_only: bool = False):
    """Fetch, group, and write (or print) hourly data for a given date."""
    start = f"{date_str}T00:00:00Z"
    end = f"{date_str}T23:59:59Z"

    ocr_data = fetch_search("ocr", start, end)
    audio_data = fetch_search("audio", start, end)

    ocr_by_hour = group_by_hour(ocr_data, extract_ocr_ts)
    audio_by_hour = group_by_hour(audio_data, extract_audio_ts)

    os.makedirs(cache_dir, exist_ok=True)

    total_sessions = 0
    total_audio = 0

    for hour in range(24):
        sessions = build_sessions(ocr_by_hour[hour])
        audio = build_audio(audio_by_hour[hour])
        total_sessions += len(sessions)
        total_audio += len(audio)

        hourly = {
            "date": date_str,
            "hour": hour,
            "sessions": sessions,
            "audio": audio,
        }

        if stats_only:
            if sessions or audio:
                print(f"  Hour {hour:02d}: {len(sessions)} sessions, {len(audio)} audio segments")
        else:
            out_path = os.path.join(cache_dir, f"cc-screenpipe-{date_str}-{hour:02d}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(hourly, f, indent=2, ensure_ascii=False)
                f.write("\n")

    if stats_only:
        print(f"\nSummary for {date_str}:")
        print(f"  Total sessions: {total_sessions}")
        print(f"  Total audio segments: {total_audio}")
        print(f"  OCR items fetched: {len(ocr_data)}")
        print(f"  Audio items fetched: {len(audio_data)}")
    else:
        print(f"Wrote 24 hourly cache files for {date_str} -> {cache_dir}/")
        print(f"  {total_sessions} sessions, {total_audio} audio segments")


def main():
    parser = argparse.ArgumentParser(description="Preprocess screenpipe data into hourly cache.")
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Date to process (YYYY-MM-DD, default: today)",
    )
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Print summary stats instead of writing files",
    )
    parser.add_argument(
        "--cache-dir",
        default=CACHE_DIR,
        help=f"Cache directory (default: {CACHE_DIR})",
    )
    args = parser.parse_args()

    # Validate date format
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"Error: invalid date format '{args.date}', expected YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)

    process_date(args.date, args.cache_dir, args.stats_only)


if __name__ == "__main__":
    main()

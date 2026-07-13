#!/usr/bin/env python3
"""Altool lesson event store CLI.

Source of truth:
  ~/.altool/events.jsonl

Derived artifacts:
  ~/.altool/lesson.index.json
  ~/.altool/lesson.md

Use ALTOOL_HOME to override ~/.altool in tests.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


KST = timezone(timedelta(hours=9))
EVENT_TYPES = {
    "code_error",
    "fix",
    "gap",
    "verification",
}


def altool_home() -> Path:
    override = os.environ.get("ALTOOL_HOME")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".altool"


def paths() -> dict[str, Path]:
    root = altool_home()
    return {
        "root": root,
        "events": root / "events.jsonl",
        "index": root / "lesson.index.json",
        "lesson": root / "lesson.md",
    }


def now_iso() -> str:
    return datetime.now(KST).replace(microsecond=0).isoformat()


def tokenize(value: Any) -> list[str]:
    text = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    return sorted(set(t.lower() for t in re.findall(r"[A-Za-z0-9_.:/\\\-\[\]가-힣]+", text)))


def load_events() -> list[dict[str, Any]]:
    event_path = paths()["events"]
    if not event_path.exists():
        return []
    events: list[dict[str, Any]] = []
    with event_path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSONL at {event_path}:{lineno}: {exc}") from exc
            if isinstance(event, dict):
                events.append(event)
    return events


def next_event_id(events: list[dict[str, Any]]) -> str:
    max_num = 0
    for event in events:
        raw_id = str(event.get("id", ""))
        match = re.fullmatch(r"E-(\d+)", raw_id)
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"E-{max_num + 1:05d}"


def read_payload(json_path: str | None, inline_json: str | None) -> dict[str, Any]:
    if json_path and inline_json:
        raise SystemExit("Use only one of --json-file or --json.")
    if json_path:
        text = sys.stdin.read() if json_path == "-" else Path(json_path).read_text(encoding="utf-8")
        payload = json.loads(text)
    elif inline_json:
        payload = json.loads(inline_json)
    else:
        raise SystemExit("append requires --json-file PATH or --json JSON.")
    if not isinstance(payload, dict):
        raise SystemExit("append payload must be a JSON object.")
    return payload


def normalize_event(payload: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    event = dict(payload)
    event_type = event.get("type")
    if event_type not in EVENT_TYPES:
        allowed = ", ".join(sorted(EVENT_TYPES))
        raise SystemExit(f"event.type is required and must be one of: {allowed}")
    event.setdefault("id", next_event_id(events))
    event.setdefault("timestamp", now_iso())
    event.setdefault("schemaVersion", 1)
    for list_field in ("tags", "files", "relatedEventIds", "verification"):
        if list_field in event and event[list_field] is None:
            event[list_field] = []
        if list_field in event and not isinstance(event[list_field], list):
            event[list_field] = [event[list_field]]
    return event


def build_index(events: list[dict[str, Any]]) -> dict[str, Any]:
    entries = []
    for event in events:
        if event.get("type") not in EVENT_TYPES:
            continue
        searchable = {
            "type": event.get("type"),
            "project": event.get("project"),
            "feature": event.get("feature"),
            "phase": event.get("phase"),
            "tags": event.get("tags", []),
            "files": event.get("files", []),
            "summary": event.get("summary"),
            "symptom": event.get("symptom"),
            "cause": event.get("cause"),
            "attempt": event.get("attempt"),
            "change": event.get("change"),
            "preventionRule": event.get("preventionRule"),
            "recurrenceRisk": event.get("recurrenceRisk"),
            "recurrenceScope": event.get("recurrenceScope"),
            "keywords": event.get("keywords", []),
        }
        entries.append(
            {
                "id": event.get("id"),
                "type": event.get("type"),
                "timestamp": event.get("timestamp"),
                "project": event.get("project"),
                "feature": event.get("feature"),
                "phase": event.get("phase"),
                "tags": event.get("tags", []),
                "files": event.get("files", []),
                "summary": event.get("summary") or event.get("symptom") or event.get("change") or "",
                "preventionRule": event.get("preventionRule", ""),
                "recurrenceRisk": event.get("recurrenceRisk", ""),
                "recurrenceScope": event.get("recurrenceScope", ""),
                "tokens": tokenize(searchable),
            }
        )
    return {
        "schemaVersion": 1,
        "generatedAt": now_iso(),
        "source": "events.jsonl",
        "entries": entries,
    }


def save_index(index: dict[str, Any]) -> None:
    index_path = paths()["index"]
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_lessons(events: list[dict[str, Any]]) -> str:
    promotable = [
        e
        for e in events
        if e.get("type") in EVENT_TYPES
        and (
            e.get("type") in {"code_error", "fix", "gap"}
            or e.get("promoteToLesson") is True
            or str(e.get("recurrenceRisk", "")).lower() in {"medium", "high"}
        )
    ]
    lines = [
        "# Altool Lesson Notes",
        "",
        "> Generated from `~/.altool/events.jsonl`. Do not treat this file as the source of truth.",
        "",
    ]
    if not promotable:
        lines.extend(["아직 승격된 lesson이 없습니다.", ""])
        return "\n".join(lines)
    for idx, event in enumerate(promotable, start=1):
        date = str(event.get("timestamp", ""))[:10] or "unknown-date"
        tags = ", ".join(str(t) for t in event.get("tags", [])) or "untagged"
        lines.append(f"## L-{idx:05d} | {date} | {tags} | event:{event.get('id')}")
        lines.append(f"- **유형**: {event.get('type')}")
        if event.get("summary"):
            lines.append(f"- **요약**: {event.get('summary')}")
        if event.get("symptom"):
            lines.append(f"- **증상**: {event.get('symptom')}")
        if event.get("cause"):
            lines.append(f"- **원인**: {event.get('cause')}")
        if event.get("change") or event.get("resolution"):
            lines.append(f"- **해결**: {event.get('change') or event.get('resolution')}")
        if event.get("preventionRule"):
            lines.append(f"- **예방 규칙**: {event.get('preventionRule')}")
        if event.get("recurrenceRisk") or event.get("recurrenceScope"):
            lines.append(
                f"- **재발성**: risk={event.get('recurrenceRisk', 'unknown')}, "
                f"scope={event.get('recurrenceScope', 'unknown')}"
            )
        files = event.get("files") or []
        if files:
            lines.append(f"- **관련 파일**: {', '.join(str(f) for f in files)}")
        lines.append("")
    return "\n".join(lines)


def write_lessons(events: list[dict[str, Any]]) -> None:
    lesson_path = paths()["lesson"]
    lesson_path.parent.mkdir(parents=True, exist_ok=True)
    lesson_path.write_text(render_lessons(events), encoding="utf-8")


def append_event(args: argparse.Namespace) -> None:
    p = paths()
    p["root"].mkdir(parents=True, exist_ok=True)
    events = load_events()
    event = normalize_event(read_payload(args.json_file, args.json), events)
    with p["events"].open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
    events.append(event)
    save_index(build_index(events))
    write_lessons(events)
    print(f"[al:lesson] event recorded - {event['id']} ({event['type']})")


def rebuild_index(_: argparse.Namespace) -> None:
    events = load_events()
    index = build_index(events)
    save_index(index)
    print(f"[al:lesson] index rebuilt - {len(index.get('entries', []))} active events")


def render_lessons_cmd(_: argparse.Namespace) -> None:
    events = load_events()
    write_lessons(events)
    print(f"[al:lesson] lesson.md rendered - {paths()['lesson']}")


def load_index() -> dict[str, Any]:
    index_path = paths()["index"]
    if not index_path.exists():
        events = load_events()
        index = build_index(events)
        save_index(index)
        return index
    return json.loads(index_path.read_text(encoding="utf-8"))


def search(args: argparse.Namespace) -> None:
    index = load_index()
    query_tokens = tokenize(args.query)
    entries = []
    for entry in index.get("entries", []):
        tokens = set(entry.get("tokens", []))
        score = sum(3 if token in tokens else 0 for token in query_tokens)
        text = json.dumps(entry, ensure_ascii=False).lower()
        score += sum(1 for token in query_tokens if token in text)
        if score:
            item = dict(entry)
            item["score"] = score
            item.pop("tokens", None)
            entries.append(item)
    entries.sort(key=lambda item: (-item["score"], str(item.get("timestamp", "")), str(item.get("id", ""))))
    entries = entries[: args.limit]
    if args.format == "json":
        print(json.dumps(entries, ensure_ascii=False, indent=2))
        return
    if not entries:
        print("[al:lesson] no related lessons")
        return
    for entry in entries:
        rule = entry.get("preventionRule")
        suffix = f" | rule: {rule}" if rule else ""
        print(f"{entry.get('id')} [{entry.get('type')}] score={entry.get('score')} {entry.get('summary')}{suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Altool lesson event CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    append_parser = sub.add_parser("append", help="append an event to events.jsonl")
    append_parser.add_argument("--json-file", help="event JSON file path, or '-' for stdin")
    append_parser.add_argument("--json", help="inline event JSON")
    append_parser.set_defaults(func=append_event)

    search_parser = sub.add_parser("search", help="search lesson index")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--limit", type=int, default=5)
    search_parser.add_argument("--format", choices=("text", "json"), default="text")
    search_parser.set_defaults(func=search)

    rebuild_parser = sub.add_parser("rebuild-index", help="rebuild lesson.index.json from events.jsonl")
    rebuild_parser.set_defaults(func=rebuild_index)

    render_parser = sub.add_parser("render-lessons", help="render lesson.md from events.jsonl")
    render_parser.set_defaults(func=render_lessons_cmd)

    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

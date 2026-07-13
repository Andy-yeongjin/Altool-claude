#!/usr/bin/env python3
"""Freedom radio CLI.

Append-only helper for `.altool/freedom/inbox.jsonl` and `outbox.jsonl`.
This script is not the Freedom engine. It is the communication channel used
while a long-running Freedom loop keeps working.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


KST = timezone(timedelta(hours=9))
FREEDOM_DIR = Path(".altool") / "freedom"
INBOX = FREEDOM_DIR / "inbox.jsonl"
OUTBOX = FREEDOM_DIR / "outbox.jsonl"
STATE = FREEDOM_DIR / "state.json"
JOURNAL = FREEDOM_DIR / "journal.md"

INBOX_TYPES = {"say", "ask", "pause", "resume", "stop"}
OUTBOX_TYPES = {"ack", "answer", "progress", "warning", "stop"}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def now_iso() -> str:
    return datetime.now(KST).replace(microsecond=0).isoformat()


def ensure_files() -> None:
    FREEDOM_DIR.mkdir(parents=True, exist_ok=True)
    for path in (INBOX, OUTBOX):
        if not path.exists():
            path.write_text("", encoding="utf-8")
    if not JOURNAL.exists():
        JOURNAL.write_text("# Freedom Journal\n\n", encoding="utf-8")
    if not STATE.exists():
        write_state(
            {
                "schemaVersion": 1,
                "goal": None,
                "status": "idle",
                "loop": 0,
                "loopBudget": 1,
                "loopsCompleted": 0,
                "currentAction": None,
                "constraints": [],
                "createdAt": now_iso(),
                "updatedAt": now_iso(),
            }
        )


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    ensure_files()
    events: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"FAIL: invalid JSONL at {path}:{line_no}: {exc}") from exc
        if not isinstance(item, dict):
            raise SystemExit(f"FAIL: JSONL item must be object at {path}:{line_no}")
        events.append(item)
    return events


def append_jsonl(path: Path, event: dict[str, Any]) -> None:
    ensure_files()
    with path.open("a", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")


@contextmanager
def file_lock(path: Path, timeout: float = 10.0):
    ensure_files()
    lock_path = path.with_suffix(path.suffix + ".lock")
    start = time.monotonic()
    handle: int | None = None
    while handle is None:
        try:
            handle = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(handle, str(os.getpid()).encode("ascii", errors="ignore"))
        except FileExistsError:
            if time.monotonic() - start > timeout:
                raise SystemExit(f"FAIL: could not acquire lock: {lock_path}")
            time.sleep(0.05)
    try:
        yield
    finally:
        if handle is not None:
            os.close(handle)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def next_id(prefix: str, path: Path) -> str:
    events = read_jsonl(path)
    max_num = 0
    for event in events:
        raw_id = str(event.get("id", ""))
        if raw_id.startswith(prefix + "-"):
            try:
                max_num = max(max_num, int(raw_id.split("-", 1)[1]))
            except ValueError:
                continue
    return f"{prefix}-{max_num + 1:05d}"


def append_numbered_event(prefix: str, path: Path, event: dict[str, Any]) -> dict[str, Any]:
    with file_lock(path):
        event["id"] = next_id(prefix, path)
        append_jsonl(path, event)
    return event


def write_state(state: dict[str, Any]) -> None:
    FREEDOM_DIR.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_state() -> dict[str, Any]:
    ensure_files()
    try:
        data = json.loads(STATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"FAIL: invalid state JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("FAIL: state JSON must be an object")
    changed = False
    defaults = {
        "loopBudget": 1,
        "loopsCompleted": 0,
    }
    for key, value in defaults.items():
        if key not in data:
            data[key] = value
            changed = True
    if changed:
        data["updatedAt"] = now_iso()
        write_state(data)
    return data


def update_state(**updates: Any) -> dict[str, Any]:
    state = read_state()
    state.update(updates)
    state["updatedAt"] = now_iso()
    write_state(state)
    return state


def append_journal(text: str) -> None:
    ensure_files()
    with JOURNAL.open("a", encoding="utf-8", newline="\n") as file:
        file.write(f"- {now_iso()} {text}\n")


def append_inbox(event_type: str, text: str) -> dict[str, Any]:
    if event_type not in INBOX_TYPES:
        raise SystemExit(f"FAIL: unsupported inbox type: {event_type}")
    event = {
        "type": event_type,
        "text": text,
        "createdAt": now_iso(),
    }
    append_numbered_event("I", INBOX, event)
    if event_type == "pause":
        update_state(status="pausing")
    elif event_type == "resume":
        update_state(status="running")
    elif event_type == "stop":
        update_state(status="stopping")
    print(json.dumps(event, ensure_ascii=False))
    return event


def append_outbox(event_type: str, text: str, reply_to: str | None = None) -> dict[str, Any]:
    if event_type not in OUTBOX_TYPES:
        raise SystemExit(f"FAIL: unsupported outbox type: {event_type}")
    event = {
        "type": event_type,
        "text": text,
        "createdAt": now_iso(),
    }
    if reply_to:
        event["replyTo"] = reply_to
    append_numbered_event("O", OUTBOX, event)
    if event_type == "stop":
        update_state(status="stopped")
    print(json.dumps(event, ensure_ascii=False))
    return event


def pending_events() -> list[dict[str, Any]]:
    inbox = read_jsonl(INBOX)
    outbox = read_jsonl(OUTBOX)
    replied = {str(item.get("replyTo")) for item in outbox if item.get("replyTo")}
    return [item for item in inbox if str(item.get("id")) not in replied]


def init_cmd(args: argparse.Namespace) -> int:
    ensure_files()
    state = read_state()
    if args.loops < 1:
        raise SystemExit("FAIL: --loops must be 1 or greater")
    state["loopBudget"] = args.loops
    state["loopsCompleted"] = 0
    state["loop"] = 0
    state["currentAction"] = None
    if args.goal:
        state["goal"] = args.goal
        state["status"] = "running"
        state["updatedAt"] = now_iso()
        write_state(state)
        append_outbox("progress", f"Freedom 목표를 설정했습니다: {args.goal} (루프 {args.loops}회)")
    else:
        state["updatedAt"] = now_iso()
        write_state(state)
        print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def inbox_cmd(args: argparse.Namespace) -> int:
    text = args.text or ""
    return 0 if append_inbox(args.type, text) else 1


def out_cmd(args: argparse.Namespace) -> int:
    return 0 if append_outbox(args.type, args.text, args.reply_to) else 1


def pending_cmd(_: argparse.Namespace) -> int:
    events = pending_events()
    print(json.dumps(events, ensure_ascii=False, indent=2))
    return 0


def outbox_cmd(args: argparse.Namespace) -> int:
    events = read_jsonl(OUTBOX)
    if args.limit:
        events = events[-args.limit :]
    print(json.dumps(events, ensure_ascii=False, indent=2))
    return 0


def tail_cmd(args: argparse.Namespace) -> int:
    inbox = [{"channel": "inbox", **event} for event in read_jsonl(INBOX)]
    outbox = [{"channel": "outbox", **event} for event in read_jsonl(OUTBOX)]
    events = sorted(inbox + outbox, key=lambda item: str(item.get("createdAt", "")))
    if args.limit:
        events = events[-args.limit :]
    for event in events:
        print(json.dumps(event, ensure_ascii=False))
    return 0


def state_cmd(_: argparse.Namespace) -> int:
    print(json.dumps(read_state(), ensure_ascii=False, indent=2))
    return 0


def cycle_cmd(args: argparse.Namespace) -> int:
    loop = args.loop
    if loop < 1:
        raise SystemExit("FAIL: --loop must be 1 or greater")
    if args.phase == "start":
        update_state(status="running", loop=loop, currentAction=None)
        append_journal(f"cycle {loop} start")
        append_outbox("progress", f"루프 {loop} 시작")
        return 0

    state = read_state()
    completed = max(int(state.get("loopsCompleted", 0)), loop)
    status = "completed" if completed >= int(state.get("loopBudget", completed)) else "running"
    update_state(status=status, loop=loop, loopsCompleted=completed, currentAction=None)
    summary = args.summary or f"루프 {loop} 완료"
    append_journal(f"cycle {loop} done: {summary}")
    append_outbox("progress", summary)
    return 0


def action_cmd(args: argparse.Namespace) -> int:
    loop = args.loop
    if loop < 1:
        raise SystemExit("FAIL: --loop must be 1 or greater")
    if args.phase == "start":
        update_state(status="running", loop=loop, currentAction=args.action)
        append_journal(f"cycle {loop} action start: {args.action}")
        append_outbox("progress", f"루프 {loop} {args.action} 시작")
        return 0

    update_state(status="running", loop=loop, currentAction=None)
    summary = args.summary or f"루프 {loop} {args.action} 완료"
    append_journal(f"cycle {loop} action done: {args.action} - {summary}")
    append_outbox("progress", summary)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Freedom radio inbox/outbox helper")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create freedom files and optionally set a goal")
    init.add_argument("goal", nargs="?", help="Freedom goal")
    init.add_argument("--loops", type=int, default=1, help="number of Freedom loops to run")
    init.set_defaults(func=init_cmd)

    for event_type in ("say", "ask", "pause", "resume", "stop"):
        cmd = sub.add_parser(event_type, help=f"append {event_type} event to inbox")
        cmd.add_argument("text", nargs="?", default="")
        cmd.set_defaults(func=inbox_cmd, type=event_type)

    out = sub.add_parser("out", help="append an AI event to outbox")
    out.add_argument("--type", choices=sorted(OUTBOX_TYPES), required=True)
    out.add_argument("--text", required=True)
    out.add_argument("--reply-to")
    out.set_defaults(func=out_cmd)

    pending = sub.add_parser("pending", help="show inbox events without outbox replyTo")
    pending.set_defaults(func=pending_cmd)

    outbox = sub.add_parser("outbox", help="show outbox events")
    outbox.add_argument("--limit", type=int, default=20)
    outbox.set_defaults(func=outbox_cmd)

    tail = sub.add_parser("tail", help="show combined inbox/outbox timeline")
    tail.add_argument("--limit", type=int, default=40)
    tail.set_defaults(func=tail_cmd)

    state = sub.add_parser("state", help="show freedom state")
    state.set_defaults(func=state_cmd)

    cycle = sub.add_parser("cycle", help="mark a Freedom cycle start/done")
    cycle.add_argument("phase", choices=("start", "done"))
    cycle.add_argument("--loop", type=int, required=True)
    cycle.add_argument("--summary", default="")
    cycle.set_defaults(func=cycle_cmd)

    action = sub.add_parser("action", help="mark a Freedom action start/done")
    action.add_argument("phase", choices=("start", "done"))
    action.add_argument("action")
    action.add_argument("--loop", type=int, required=True)
    action.add_argument("--summary", default="")
    action.set_defaults(func=action_cmd)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

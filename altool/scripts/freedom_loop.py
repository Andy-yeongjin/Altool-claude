#!/usr/bin/env python3
"""Bounded Freedom control-plane smoke runner.

Runs a finite control-plane tick budget and checks the radio inbox before each tick.
This runner is intentionally small: it validates the Freedom control plane
(state, inbox/outbox, loop accounting, step check) while the agent-facing
`altool/steps/freedom.md` remains the source of truth for real development work.
Ticks are not real Freedom development cycles.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import radio


KST = timezone(timedelta(hours=9))
CHECKS_DIR = Path(".altool") / "checks"
JOURNAL = Path(".altool") / "freedom" / "journal.md"
CHECK_PATH = CHECKS_DIR / "freedom.freedom.json"
ACTION_SEQUENCE = ["research", "plan", "spec", "run", "analyze", "fix", "browser", "report"]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def now_iso() -> str:
    return datetime.now(KST).replace(microsecond=0).isoformat()


def append_journal(text: str) -> None:
    radio.ensure_files()
    with JOURNAL.open("a", encoding="utf-8", newline="\n") as file:
        file.write(f"- {now_iso()} {text}\n")


def write_check(evidence: dict[str, list[str]], lesson_reason: str) -> None:
    CHECKS_DIR.mkdir(parents=True, exist_ok=True)

    def done_or_skipped(key: str, skipped_reason: str) -> dict[str, Any]:
        items = evidence.get(key, [])
        if items:
            return {"status": "done", "evidence": items}
        return {"status": "skipped", "reason": skipped_reason}

    checks: dict[str, dict[str, Any]] = {
        "inputs.loaded": {"status": "done", "evidence": evidence.get("inputs.loaded", [])},
        "lesson.search": {
            "status": "skipped",
            "reason": "control-plane smoke runner only; real implementation actions run lesson search in their own step",
        },
        "event.capture": {
            "status": "skipped",
            "reason": "control-plane smoke runner only; no code error or implementation gap",
        },
        "verification": {"status": "done", "evidence": evidence.get("verification", [])},
        "state.updated": {"status": "done", "evidence": evidence.get("state.updated", [])},
        "docs.synced": {
            "status": "skipped",
            "reason": "control-plane smoke runner only; no feature docs are produced",
        },
        "document.status": {
            "status": "skipped",
            "reason": "control-plane smoke runner only; no document status is changed",
        },
        "artifacts.created": {"status": "done", "evidence": evidence.get("artifacts.created", [])},
        "inbox.watch": {"status": "done", "evidence": evidence.get("inbox.watch", [])},
        "research.required": {
            "status": "skipped",
            "reason": "control-plane smoke runner only; real /altool freedom cycles must run research first",
        },
        "cycle.state": done_or_skipped("cycle.state", "stopped before any control-plane cycle started"),
        "action.state": done_or_skipped("action.state", "stopped before any control-plane action started"),
        "report.required": {
            "status": "skipped",
            "reason": "control-plane smoke runner only; real implementation cycles require report before cycle completion",
        },
        "outbox.updated": {"status": "done", "evidence": evidence.get("outbox.updated", [])},
        "action.selected": done_or_skipped("action.selected", "stopped before action selection"),
        "lesson.capture": {"status": "skipped", "reason": lesson_reason},
        "loop.progress": done_or_skipped("loop.progress", "stopped before loop progress was written"),
        "visual.reference_comparison": {
            "status": "skipped",
            "reason": "control-plane smoke runner only; no browser action",
        },
        "visual.css_custom_properties": {
            "status": "skipped",
            "reason": "control-plane smoke runner only; no browser action",
        },
        "server.cleanup": {
            "status": "skipped",
            "reason": "control-plane smoke runner only; no browser server",
        },
    }
    data = {
        "schemaVersion": 1,
        "feature": "freedom",
        "step": "freedom",
        "checks": checks,
    }
    CHECK_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_check() -> tuple[bool, str]:
    check_script = Path("altool") / "scripts" / "check.py"
    result = subprocess.run(
        [sys.executable, str(check_script), "validate", "--json", str(CHECK_PATH)],
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def process_pending(evidence: dict[str, list[str]]) -> bool:
    pending = radio.pending_events()
    evidence.setdefault("inbox.watch", []).append(f"pending={len(pending)}")
    if not pending:
        return True

    state = radio.read_state()
    constraints = state.get("constraints")
    if not isinstance(constraints, list):
        constraints = []

    for event in pending:
        event_id = str(event.get("id", ""))
        event_type = str(event.get("type", ""))
        text = str(event.get("text", ""))
        if event_type == "stop":
            radio.append_outbox("stop", "중단 요청을 확인했습니다. Freedom control-plane smoke run을 종료합니다.", event_id)
            radio.update_state(status="stopped", currentAction=None)
            append_journal(f"stop 처리: {event_id} {text}")
            evidence.setdefault("outbox.updated", []).append(f"stop replyTo={event_id}")
            return False
        if event_type == "pause":
            radio.append_outbox("ack", "일시정지 요청을 확인했습니다. 남은 control-plane tick은 보류합니다.", event_id)
            radio.update_state(status="paused", currentAction=None)
            append_journal(f"pause 처리: {event_id} {text}")
            evidence.setdefault("outbox.updated", []).append(f"pause ack replyTo={event_id}")
            return False
        if event_type == "resume":
            radio.append_outbox("ack", "재개 요청을 확인했습니다. 다음 control-plane tick부터 계속 진행합니다.", event_id)
            radio.update_state(status="running")
            append_journal(f"resume 처리: {event_id} {text}")
            evidence.setdefault("outbox.updated", []).append(f"resume ack replyTo={event_id}")
            continue
        if event_type == "ask":
            state = radio.read_state()
            answer = (
                f"현재 control-plane tick {state.get('loopsCompleted', 0)}/{state.get('loopBudget', 1)} 완료, "
                f"현재 action은 {state.get('currentAction') or '대기'}입니다."
            )
            radio.append_outbox("answer", answer, event_id)
            append_journal(f"ask 답변: {event_id} {text}")
            evidence.setdefault("outbox.updated", []).append(f"answer replyTo={event_id}")
            continue
        if event_type == "say":
            constraints.append(text)
            radio.update_state(constraints=constraints)
            radio.append_outbox("ack", f"반영했습니다: {text}", event_id)
            append_journal(f"say 반영: {event_id} {text}")
            evidence.setdefault("outbox.updated", []).append(f"ack replyTo={event_id}")
            evidence.setdefault("state.updated", []).append("constraints updated")
            continue

        radio.append_outbox("warning", f"지원하지 않는 inbox type입니다: {event_type}", event_id)
        evidence.setdefault("outbox.updated", []).append(f"warning replyTo={event_id}")
    return True


def select_action(loop_number: int) -> str:
    return ACTION_SEQUENCE[(loop_number - 1) % len(ACTION_SEQUENCE)]


def run_loop(args: argparse.Namespace) -> int:
    radio.ensure_files()
    goal = " ".join(args.goal).strip() if isinstance(args.goal, list) else str(args.goal or "").strip()
    if goal:
        radio.update_state(
            goal=goal,
            loopBudget=args.loops,
            loopsCompleted=0,
            loop=0,
            status="running",
            currentAction=None,
        )
        radio.append_outbox("progress", f"Freedom control-plane smoke run을 시작합니다: {goal} (ticks: {args.loops})")
    else:
        state = radio.read_state()
        if not state.get("goal"):
            raise SystemExit("FAIL: goal is required for first Freedom loop run")
        radio.update_state(loopBudget=args.loops, loopsCompleted=0, loop=0, status="running")
        radio.append_outbox("progress", f"Freedom control-plane smoke run을 재시작합니다. ticks: {args.loops}")

    evidence: dict[str, list[str]] = {
        "inputs.loaded": ["radio state and inbox/outbox files loaded", "check.py validator loaded"],
        "inbox.watch": [],
        "outbox.updated": ["control-plane smoke start progress"],
        "state.updated": ["loopBudget initialized", "loopsCompleted reset"],
        "artifacts.created": [
            ".altool/freedom/state.json",
            ".altool/freedom/inbox.jsonl",
            ".altool/freedom/outbox.jsonl",
            ".altool/freedom/journal.md",
            ".altool/checks/freedom.freedom.json",
        ],
        "cycle.state": [],
        "action.state": [],
        "action.selected": [],
        "verification": [],
        "loop.progress": [],
    }

    for loop_number in range(1, args.loops + 1):
        if not process_pending(evidence):
            evidence.setdefault("verification", []).append(f"control tick {loop_number} stopped by radio")
            break

        action = select_action(loop_number)
        radio.update_state(
            status="running",
            loop=loop_number,
            currentAction=action,
        )
        evidence.setdefault("state.updated", []).append(f"controlTick={loop_number} currentAction={action}")
        evidence.setdefault("cycle.state", []).append(f"loop={loop_number}")
        evidence.setdefault("action.state", []).append(f"currentAction={action}")
        evidence.setdefault("action.selected", []).append(f"control tick {loop_number}: {action}")
        append_journal(f"control tick {loop_number}/{args.loops}: action={action}")
        radio.append_outbox("progress", f"control tick {loop_number}/{args.loops}: {action} action을 선택했습니다.")
        evidence.setdefault("outbox.updated", []).append(f"control tick {loop_number} progress")
        evidence.setdefault("loop.progress", []).append(f"journal control tick {loop_number}")

        time.sleep(args.interval)

        state = radio.read_state()
        completed = int(state.get("loopsCompleted", 0)) + 1
        radio.update_state(loopsCompleted=completed, currentAction=None)
        evidence.setdefault("state.updated", []).append(f"loopsCompleted={completed}")
        evidence.setdefault("action.state", []).append("currentAction cleared")

    final_state = radio.read_state()
    if final_state.get("status") == "running":
        radio.update_state(status="completed", currentAction=None)
        radio.append_outbox(
            "progress",
            f"Freedom control-plane smoke run 완료: {final_state.get('loopsCompleted', 0)}/{final_state.get('loopBudget', args.loops)}",
        )
        evidence.setdefault("outbox.updated", []).append("control-plane smoke completed progress")

    evidence.setdefault("verification", []).append("bounded control-plane smoke run finished")
    write_check(evidence, "freedom control-plane smoke run; no project code error or implementation gap")
    valid, output = validate_check()
    print(output)
    return 0 if valid else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a bounded Freedom control-plane smoke run")
    parser.add_argument("goal", nargs="*", help="Freedom goal")
    parser.add_argument("--loops", type=int, default=1, help="loop budget")
    parser.add_argument("--interval", type=float, default=1.0, help="seconds between loops")
    args = parser.parse_args()
    if args.loops < 1:
        raise SystemExit("FAIL: --loops must be 1 or greater")
    return run_loop(args)


if __name__ == "__main__":
    raise SystemExit(main())

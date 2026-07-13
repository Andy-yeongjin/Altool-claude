#!/usr/bin/env python3
"""Altool Step Check validator.

Validates .altool/checks/{feature}.{step}.json files.
The validator checks structure only. Agents use the failure messages to
complete missing work, update the check JSON, and validate again.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


VALID_STATUSES = {"done", "skipped", "failed"}
RESEARCH_READINESS = {"ready", "partial", "not-ready"}
COMMON_REQUIRED = [
    "inputs.loaded",
    "lesson.search",
    "event.capture",
    "verification",
    "state.updated",
    "docs.synced",
    "document.status",
    "artifacts.created",
]

RESEARCH_REQUIRED = COMMON_REQUIRED + [
    "research.source_mix",
    "research.source_quality",
    "research.freshness",
    "research.duplicate_review",
    "research.evidence_map",
    "research.visual_capture",
    "research.design_system",
    "research.design_tokens",
    "research.screen_recipe",
    "research.component_extraction",
    "research.capture_map",
    "research.plan_readiness",
    "research.next_queries",
]

BROWSER_REQUIRED = COMMON_REQUIRED + [
    "visual.reference_comparison",
    "visual.css_custom_properties",
    "server.cleanup",
]

FREEDOM_REQUIRED = COMMON_REQUIRED + [
    "inbox.watch",
    "research.required",
    "cycle.state",
    "action.state",
    "report.required",
    "outbox.updated",
    "action.selected",
    "lesson.capture",
    "loop.progress",
    "visual.reference_comparison",
    "visual.css_custom_properties",
    "server.cleanup",
]

STEP_REQUIRED: dict[str, list[str]] = {
    "setup": COMMON_REQUIRED,
    "guide": COMMON_REQUIRED,
    "research": RESEARCH_REQUIRED,
    "freedom": FREEDOM_REQUIRED,
    "design_source": COMMON_REQUIRED,
    "lesson": COMMON_REQUIRED,
    "plan": COMMON_REQUIRED,
    "spec": COMMON_REQUIRED,
    "run": COMMON_REQUIRED,
    "analyze": COMMON_REQUIRED,
    "fix": COMMON_REQUIRED,
    "report": COMMON_REQUIRED,
    "status": COMMON_REQUIRED,
    "browser": BROWSER_REQUIRED,
}

OPTIONAL_STEP = "oneshot"


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def has_nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and any(str(item).strip() for item in value)


def check_label(step: str, item: str) -> str:
    return item if item.startswith(f"{step}.") else f"{step}.{item}"


def get_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def validate_research_quality(data: dict[str, Any], failures: list[str]) -> None:
    quality = data.get("quality")
    if not isinstance(quality, dict):
        fail("research.quality: root.quality object is required for research step", failures)
        return

    score = get_number(quality.get("score"))
    if score is None or not 0 <= score <= 100:
        fail("research.quality.score: must be a number between 0 and 100", failures)

    readiness = quality.get("planReadiness")
    if readiness not in RESEARCH_READINESS:
        fail("research.quality.planReadiness: must be ready, partial, or not-ready", failures)

    source_count = get_number(quality.get("sourceCount"))
    if source_count is None or source_count < 8:
        fail("research.quality.sourceCount: must be at least 8", failures)

    source_mix = quality.get("sourceMix")
    if not isinstance(source_mix, dict):
        fail("research.quality.sourceMix: must be an object", failures)
    else:
        minimums = {
            "actualService": 3,
            "researchOrOfficial": 3,
            "userVoice": 1,
        }
        for key, minimum in minimums.items():
            value = get_number(source_mix.get(key))
            if value is None or value < minimum:
                fail(f"research.quality.sourceMix.{key}: must be at least {minimum}", failures)

    next_query_count = get_number(quality.get("nextQueryCount"))
    if next_query_count is None or next_query_count < 3:
        fail("research.quality.nextQueryCount: must be at least 3", failures)

    if score is not None:
        if score < 70:
            fail("research.quality.score: below 70 requires research rework before completion", failures)
        if score < 80 and readiness == "ready":
            fail("research.quality.planReadiness: qualityScore below 80 cannot be ready", failures)


def validate_check(data: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if data.get("schemaVersion") != 1:
        fail("root.schemaVersion must be 1", failures)

    feature = data.get("feature")
    if not isinstance(feature, str) or not feature.strip():
        fail("root.feature is required", failures)

    step = data.get("step")
    if not isinstance(step, str) or not step.strip():
        fail("root.step is required", failures)
        step = ""

    checks = data.get("checks")
    if not isinstance(checks, dict):
        fail("root.checks must be an object", failures)
        return failures

    if step == "research":
        validate_research_quality(data, failures)

    if step == OPTIONAL_STEP:
        children = data.get("children")
        if not isinstance(children, list) or not children:
            fail("oneshot.children must be a non-empty list", failures)
    else:
        required = STEP_REQUIRED.get(str(step), COMMON_REQUIRED)
        for item in required:
            if item not in checks:
                fail(f"{check_label(str(step), item)}: missing required check", failures)

    for item, check in checks.items():
        label = check_label(str(step), str(item))
        if not isinstance(check, dict):
            fail(f"{label}: check must be an object", failures)
            continue
        status = check.get("status")
        if status not in VALID_STATUSES:
            fail(f"{label}: status must be one of done, skipped, failed", failures)
            continue
        if status == "done" and not has_nonempty_list(check.get("evidence")):
            fail(f"{label}: status=done requires non-empty evidence list", failures)
        if status in {"skipped", "failed"}:
            reason = check.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                fail(f"{label}: status={status} requires reason", failures)

    return failures


def load_json(path: str) -> dict[str, Any]:
    try:
        text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
        data = json.loads(text)
    except Exception as exc:  # noqa: BLE001 - CLI should return friendly failures
        raise SystemExit(f"FAIL: could not read JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("FAIL: check JSON must be an object")
    return data


def validate_cmd(args: argparse.Namespace) -> int:
    data = load_json(args.json)
    failures = validate_check(data)
    if args.format == "json":
        print(
            json.dumps(
                {
                    "valid": not failures,
                    "feature": data.get("feature"),
                    "step": data.get("step"),
                    "failures": failures,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif failures:
        print("FAIL Step Check validation")
        for failure in failures:
            print(f"- {failure}")
    else:
        print(f"PASS Step Check: {data.get('feature')}.{data.get('step')}")
    return 1 if failures else 0


def owner_check_for_doc(doc: Path, root: Path) -> Path | None:
    try:
        rel = doc.relative_to(root)
    except ValueError:
        rel = doc
    parts = rel.parts
    if len(parts) < 2 or parts[0] != "docs":
        return None

    checks_dir = root / ".altool" / "checks"
    name = doc.name

    if len(parts) >= 3 and parts[1] == "00-research" and name.endswith(".research.md"):
        match = re.match(r"^(R-\d+)", name)
        if match:
            return checks_dir / f"{match.group(1)}.research.json"
        return None

    suffix_map = {
        ".plan.md": "plan",
        ".spec.md": "spec",
        ".analyze.md": "analyze",
        ".fix.md": "fix",
        ".browser.md": "browser",
        ".report.md": "report",
    }
    for suffix, step in suffix_map.items():
        if name.endswith(suffix):
            feature = name[: -len(suffix)]
            return checks_dir / f"{feature}.{step}.json"
    return None


def iter_altool_docs(root: Path) -> list[Path]:
    docs_dir = root / "docs"
    if not docs_dir.exists():
        return []
    return sorted(
        path
        for path in docs_dir.rglob("*.md")
        if owner_check_for_doc(path, root) is not None
    )


def audit_docs_cmd(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    failures: list[str] = []
    audited = 0
    tolerance = float(args.tolerance)

    for doc in iter_altool_docs(root):
        check_path = owner_check_for_doc(doc, root)
        if check_path is None:
            continue
        audited += 1
        display_doc = doc.relative_to(root)
        display_check = check_path.relative_to(root)
        if not check_path.exists():
            failures.append(f"{display_doc}: missing owner check {display_check}")
            continue
        doc_mtime = doc.stat().st_mtime
        check_mtime = check_path.stat().st_mtime
        if doc_mtime > check_mtime + tolerance:
            failures.append(f"{display_doc}: owner check is stale ({display_check})")

    if args.format == "json":
        print(
            json.dumps(
                {
                    "valid": not failures,
                    "audited": audited,
                    "failures": failures,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif failures:
        print("FAIL Altool document/check audit")
        for failure in failures:
            print(f"- {failure}")
    else:
        print(f"PASS Altool document/check audit: {audited} docs")
    return 1 if failures else 0


CSS_EXTENSIONS = {".css", ".scss", ".sass", ".less"}
CSS_EXCLUDE_DIRS = {
    ".git",
    ".next",
    ".nuxt",
    ".output",
    ".turbo",
    ".vite",
    "coverage",
    "dist",
    "build",
    "node_modules",
    "playwright-report",
    "test-results",
}


def iter_css_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in CSS_EXTENSIONS:
            continue
        try:
            rel_parts = path.relative_to(root).parts
        except ValueError:
            rel_parts = path.parts
        if any(part in CSS_EXCLUDE_DIRS for part in rel_parts):
            continue
        files.append(path)
    return sorted(files)


def css_vars_cmd(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    files = iter_css_files(root)
    definitions: dict[str, list[str]] = {}
    references: list[tuple[str, str, int]] = []
    failures: list[str] = []

    define_pattern = re.compile(r"(^|[{\s;])(--[A-Za-z0-9_-]+)\s*:", re.MULTILINE)
    var_pattern = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)")

    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="ignore")
        rel = str(path.relative_to(root))
        for match in define_pattern.finditer(text):
            definitions.setdefault(match.group(2), []).append(rel)
        for line_no, line in enumerate(text.splitlines(), start=1):
            for match in var_pattern.finditer(line):
                references.append((match.group(1), rel, line_no))

    for name, rel, line_no in references:
        if name not in definitions:
            failures.append(f"{rel}:{line_no}: {name} is referenced with var() but never defined")

    if args.format == "json":
        print(
            json.dumps(
                {
                    "valid": not failures,
                    "files": len(files),
                    "definitions": len(definitions),
                    "references": len(references),
                    "failures": failures,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif failures:
        print("FAIL CSS custom property validation")
        for failure in failures:
            print(f"- {failure}")
    else:
        print(
            "PASS CSS custom property validation: "
            f"{len(files)} files, {len(definitions)} definitions, {len(references)} references"
        )
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Altool Step Check JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate a step check JSON file")
    validate.add_argument("--json", required=True, help="check JSON path, or '-' for stdin")
    validate.add_argument("--format", choices=("text", "json"), default="text")
    validate.set_defaults(func=validate_cmd)

    audit = sub.add_parser("audit-docs", help="verify Altool docs are not newer than their owner Step Check")
    audit.add_argument("--root", default=".", help="project root to audit")
    audit.add_argument("--tolerance", type=float, default=0.5, help="mtime tolerance in seconds")
    audit.add_argument("--format", choices=("text", "json"), default="text")
    audit.set_defaults(func=audit_docs_cmd)

    css_vars = sub.add_parser("css-vars", help="verify CSS var() references have matching custom property definitions")
    css_vars.add_argument("--root", default=".", help="project root to scan")
    css_vars.add_argument("--format", choices=("text", "json"), default="text")
    css_vars.set_defaults(func=css_vars_cmd)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Validate gate cards in .gameworkflow.

Usage:
    python check_gates.py <project-dir> [--json] [--strict]

Checks:
- state.md exists and contains "Current module" / "Preset" (or Chinese equivalents)
- every gates/*.md has five sections: 已定 / 待定 / 风险 / 下一步验证 / 签字
- 已定 has at least 3 bullets
- every 待定 bullet says when it will be decided
- 签字 contains A-level sign-off
--strict turns warnings into errors.

Exit: 0 pass, 1 errors, 2 bad path.
Console output is ASCII-only; user-facing text stays inside the files.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = [
    ("## 已定", "frozen decisions"),
    ("## 待定", "open questions"),
    ("## 风险", "risks"),
    ("## 下一步验证", "next verification"),
    ("## 签字", "sign-off"),
]
WHEN_WORDS = ("何时定", "决定时间", "冻结前", "之前", "待定时间", "下周", "本周", "before")
STATE_KEYS = ("当前模块", "顺序预设", "Current module", "Preset")


def split_sections(text: str) -> dict:
    sections, current = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line.strip()
            sections[current] = []
        elif current:
            sections[current].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def bullets(block: str) -> list:
    return [ln.strip() for ln in block.splitlines()
            if ln.strip().startswith(("-", "*", "[ ]", "[x]"))]


def check_gate(path: Path) -> tuple[list, list]:
    errors, warnings = [], []
    text = path.read_text(encoding="utf-8")
    name = path.name

    secs = split_sections(text)
    for head, label in REQUIRED:
        if head not in secs:
            errors.append("%s: missing section '%s'" % (name, label))

    for head, label in REQUIRED:
        if head in secs and not secs[head].strip():
            errors.append("%s: section '%s' is empty" % (name, label))

    done = bullets(secs.get("## 已定", ""))
    if len(done) < 3:
        warnings.append("%s: only %d frozen decisions (want >= 3)" % (name, len(done)))

    for idx, item in enumerate(bullets(secs.get("## 待定", "")), 1):
        if not any(w in item for w in WHEN_WORDS):
            warnings.append("%s: open question #%d has no 'when'" % (name, idx))

    sign = secs.get("## 签字", "")
    if sign and "A 级" not in sign and "A-level" not in sign:
        errors.append("%s: sign-off has no A-level line" % name)

    return errors, warnings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate gate cards")
    ap.add_argument("project", help="game project root containing .gameworkflow")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args(argv)

    root = Path(args.project).expanduser().resolve()
    wf = root / ".gameworkflow"
    if not wf.exists():
        msg = "[ERROR] %s not found; run init_workflow.py first" % wf
        print(json.dumps({"ok": False, "error": msg}) if args.json else msg)
        return 2

    errors, warnings = [], []
    state = wf / "state.md"
    if not state.exists():
        errors.append("missing state.md")
    else:
        st = state.read_text(encoding="utf-8")
        if not any(k in st for k in STATE_KEYS):
            errors.append("state.md: no current-module / preset field")

    gates = sorted(p for p in (wf / "gates").glob("*.md")
                   if p.name.lower() != "readme.md")
    if not gates:
        warnings.append("gates/ has no cards yet (normal at the start)")
    for g in gates:
        e, w = check_gate(g)
        errors.extend(e)
        warnings.extend(w)

    if args.strict:
        errors = errors + ["(strict) " + w for w in warnings]
        warnings = []

    result = {
        "ok": not errors,
        "gates": [g.name for g in gates],
        "errors": errors,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Checking: %s" % wf)
        print("Gate cards: %d (%s)" % (len(gates), ", ".join(g.name for g in gates) or "none"))
        for w in warnings:
            print("[WARN] " + w)
        for e in errors:
            print("[ERROR] " + e)
        print("Result: %s" % ("PASS" if not errors else "FAIL (%d errors)" % len(errors)))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())


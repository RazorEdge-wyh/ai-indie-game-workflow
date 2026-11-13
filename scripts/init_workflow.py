#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Initialize a .gameworkflow directory in a game project.

Usage:
    python init_workflow.py <project-dir> [--preset narrative|gameplay|experience|multiplayer]
    python init_workflow.py <project-dir> --force

Creates only missing files; never overwrites existing state.md unless --force.
Console output is ASCII-only so it stays readable in any terminal/codepage.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PRESETS = {
    "narrative": ("narrative-driven", "G0 -> N -> A -> L -> C -> P -> T? -> V -> M -> R"),
    "gameplay": ("gameplay-driven", "G0 -> C -> A -> L -> P -> N? -> V -> M -> R"),
    "experience": ("experience-driven", "G0 -> A -> N -> L -> P -> C -> V -> M -> R"),
    "multiplayer": ("multiplayer-driven", "G0 -> C -> T -> A -> L -> P -> N? -> V -> M -> R"),
}

STATE = """# Project state

- Project: <one-line concept>
- Genre: <co-op horror / match-3 / narrative adventure ...>
- Team size: <1>
- Hours per week: <20>
- Preset: {preset_name}
- Module order: {order}
- Current module: G0 seed
- Last frozen: none
- Next open question: <can this one-liner reject a bad request?>
- Next external playtest: <date / target players>
- Notes: <story is human-written; other constraints>

## Progress

| Module | Status | Frozen on | File |
|---|---|---|---|
| G0 seed | in progress | - | gates/G0.md |
"""

DECISIONS = """# A-level decision log

Only A-level decisions (theme, core loop, endings, art direction, scope, release bar, cuts).
B-level: one line in the freeze card. C-level: not logged, weekly audit.

| Date | Module | Decision | Why | Decided by |
|---|---|---|---|---|
"""

LEDGER = """# AI asset ledger

| Asset | Tool/model | Prompt notes | Date | Human edits | License | Needs disclosure |
|---|---|---|---|---|---|---|
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Initialize .gameworkflow")
    ap.add_argument("project", help="game project root")
    ap.add_argument("--preset", default="narrative", choices=sorted(PRESETS))
    ap.add_argument("--force", action="store_true", help="overwrite existing state.md")
    args = ap.parse_args(argv)

    root = Path(args.project).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print("[ERROR] project directory not found: %s" % root)
        return 2

    wf = root / ".gameworkflow"
    for sub in ("gates", "changes", "playtests"):
        (wf / sub).mkdir(parents=True, exist_ok=True)

    preset_name, order = PRESETS[args.preset]
    created = []

    state = wf / "state.md"
    if args.force or not state.exists():
        state.write_text(STATE.format(preset_name=preset_name, order=order), encoding="utf-8")
        created.append("state.md")

    decisions = wf / "decisions.md"
    if not decisions.exists():
        decisions.write_text(DECISIONS, encoding="utf-8")
        created.append("decisions.md")

    ledger = wf / "ledger.md"
    if not ledger.exists():
        ledger.write_text(LEDGER, encoding="utf-8")
        created.append("ledger.md")

    print("Initialized: %s" % wf)
    print("Preset: %s (%s)" % (preset_name, order))
    print("Created: %s" % (", ".join(created) if created else "nothing (already exists)"))
    print("")
    print("Next:")
    print("1. Fill state.md: one-line concept + team size")
    print("2. Start at G0: run the two-player review, ask 3-5 questions")
    print("3. After the human answers, write gates/G0.md with the five sections")
    print("4. Run: python check_gates.py .")
    return 0


if __name__ == "__main__":
    sys.exit(main())

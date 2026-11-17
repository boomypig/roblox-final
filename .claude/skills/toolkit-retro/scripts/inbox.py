#!/usr/bin/env python3
"""Read and close entries in the lessons inbox that session.py fills at each session boundary.

    inbox.py list                                     # every open lesson, with a stable id
    inbox.py done L1a2b3c4d --owner roblox-code --edit <path> --test <path>   # one edit made
    inbox.py skip L1a2b3c4d --reason "<why no toolkit change>"                # a game's own debt
    inbox.py check                                    # the gate: every closed lesson is backed

WHY THIS EXISTS. Lessons were written down and then nothing happened to them, or a lesson was
"addressed" by an edit nobody could find later. The inbox is a plain file session.py appends to;
this script gives each line an id, moves a lesson out only with the edit and the test that
answer it, and keeps the record in private/lessons-done.md so the next retro can see what was
done and why. A lesson that is a game's own debt (not a toolkit defect) is closed with a reason
instead of an edit.

Both files are in the toolkit's private/ folder (ROBLOX_FINAL_PRIVATE overrides it); a missing
inbox means there is nothing to do.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from datetime import date
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[4]
PRIVATE = Path(os.environ.get("ROBLOX_FINAL_PRIVATE") or TOOLKIT / "private").expanduser()
INBOX = PRIVATE / "lessons-inbox.md"
DONE = PRIVATE / "lessons-done.md"
HEAD = re.compile(r"^## (.+)$")


def lessons() -> list[dict]:
    if not INBOX.exists():
        return []
    out, head = [], ""
    for line in INBOX.read_text(encoding="utf-8").splitlines():
        m = HEAD.match(line)
        if m:
            head = m.group(1)
        elif line.startswith("- ") and head:
            lid = "L" + hashlib.sha1(f"{head}\n{line}".encode()).hexdigest()[:8]
            out.append({"id": lid, "head": head, "text": line[2:]})
    return out


def remove(lesson: dict) -> None:
    lines = INBOX.read_text(encoding="utf-8").splitlines()
    out, head, dropped = [], "", False
    for line in lines:
        m = HEAD.match(line)
        if m:
            head = m.group(1)
        if not dropped and head == lesson["head"] and line == f"- {lesson['text']}":
            dropped = True
            continue
        out.append(line)
    text = "\n".join(out) + "\n"
    text = re.sub(r"^## [^\n]+\n\n(?=## |\Z)", "", text, flags=re.M)  # a heading with no lessons left
    INBOX.write_text(text, encoding="utf-8")


def record(lesson: dict, fields: dict) -> None:
    new = not DONE.exists()
    with DONE.open("a", encoding="utf-8") as fh:
        if new:
            fh.write("# Lessons done\n\nWritten by toolkit-retro's inbox.py. One entry per closed lesson.\n")
        fh.write(f"\n## {lesson['id']} ({date.today().isoformat()})\n\n- lesson: {lesson['text']}\n"
                 f"- from: {lesson['head']}\n")
        for k, v in fields.items():
            fh.write(f"- {k}: {v}\n")


def find(lid: str) -> dict:
    for le in lessons():
        if le["id"] == lid:
            return le
    raise SystemExit(f"no open lesson {lid}; run `inbox.py list`")


def cmd_list(a) -> int:
    ls = lessons()
    if not ls:
        print(f"no open lessons ({INBOX} {'is empty' if INBOX.exists() else 'does not exist'})")
        return 0
    head = None
    for le in ls:
        if le["head"] != head:
            head = le["head"]
            print(f"\n{head}")
        print(f"  {le['id']}  {le['text']}")
    print(f"\n{len(ls)} open lesson(s)")
    return 0


def cmd_done(a) -> int:
    le = find(a.id)
    missing = [p for p in (a.edit, a.test) if not (TOOLKIT / p).exists()]
    if missing:
        raise SystemExit(f"not in the toolkit: {', '.join(missing)}. A lesson closes on an edit and a test that exist.")
    record(le, {"owner": a.owner, "edit": a.edit, "test": a.test})
    remove(le)
    print(f"closed {le['id']}: {a.edit}, proven by {a.test}")
    return 0


def cmd_skip(a) -> int:
    le = find(a.id)
    if len(a.reason.split()) < 4:
        raise SystemExit("say why in a sentence: what makes this the game's own debt and not a toolkit defect")
    record(le, {"no toolkit change": a.reason})
    remove(le)
    print(f"closed {le['id']} without a toolkit change: {a.reason}")
    return 0


def cmd_check(a) -> int:
    bad = []
    if DONE.exists():
        for block in re.split(r"\n(?=## L)", DONE.read_text(encoding="utf-8")):
            m = re.match(r"## (L\w+)", block)
            if not m or "- no toolkit change:" in block:
                continue
            for field in ("edit", "test"):
                f = re.search(rf"^- {field}: (.+)$", block, re.M)
                if not f:
                    bad.append(f"{m.group(1)}: no {field}")
                elif not (TOOLKIT / f.group(1).strip()).exists():
                    bad.append(f"{m.group(1)}: {field} {f.group(1).strip()} no longer exists")
    for b in bad:
        print(f"FAIL  {b}")
    print(f"{len(lessons())} open lesson(s); {len(bad)} closed lesson(s) without a backing edit or test")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").set_defaults(func=cmd_list)
    p = sub.add_parser("done"); p.add_argument("id"); p.add_argument("--owner", required=True)
    p.add_argument("--edit", required=True, help="toolkit path of the one edit"); p.add_argument("--test", required=True)
    p.set_defaults(func=cmd_done)
    p = sub.add_parser("skip"); p.add_argument("id"); p.add_argument("--reason", required=True); p.set_defaults(func=cmd_skip)
    sub.add_parser("check").set_defaults(func=cmd_check)
    a = ap.parse_args(argv)
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Gate a mechanic spec: can /build implement it and the reviewer check it?

    check_spec.py <spec file>                     # the spec-writer's gate (a draft may pass)
    check_spec.py <spec file> --require-approved  # /build's precondition

WHY THIS EXISTS. /build implements exactly what a spec says and the reviewer scores the result
against its acceptance criteria. A spec with no checkable criteria passes review by default,
and a spec built while still a draft is a design nobody approved. Both look fine until a
playtest. The other failure is quieter: an unclear point that was neither asked nor written
down, so the builder guessed and nobody knew a guess was made. The operating policy says such
points are decided and marked `**Assumption:**`; this gate checks the spec has the places to
hold them and no template text left where a decision should be.

Checks:
  1. a `Status:` line (idea | draft | approved | built); with --require-approved it must be
     approved or built
  2. every section of the template is present and none is empty:
     Player experience, Rules, Technical notes, Acceptance criteria, Out of scope
  3. at least one acceptance criterion, each a checkbox with text
  4. Technical notes say what the server decides and what the client does
  5. no template placeholder or bare template line is left
  6. an Open questions section exists (it may be empty: open points belong under Assumption)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SECTIONS = ["Player experience", "Rules", "Technical notes", "Acceptance criteria", "Out of scope"]
STATUS = re.compile(r"^Status:\s*(idea|draft|approved|built)\b", re.M)
PLACEHOLDER = re.compile(r"<[A-Za-z][^<>\n]{2,}>")
TEMPLATE_LINES = {"What it feels like, in 2–3 sentences.", "What it feels like, in 2-3 sentences."}


def section(text: str, title: str) -> str | None:
    m = re.search(r"^## " + re.escape(title) + r"[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def filled(body: str) -> list[str]:
    out = []
    for ln in body.splitlines():
        s = ln.strip()
        if not s or s in TEMPLATE_LINES:
            continue
        s = re.sub(r"^[-*]\s*(\[[ xX]\])?\s*", "", s)
        if s and not re.fullmatch(r"[A-Za-z /()]+:", s):  # "Server vs client:" with nothing after it
            out.append(s)
    return out


def check(text: str, require_approved: bool) -> list[str]:
    fails: list[str] = []
    m = STATUS.search(text)
    if not m:
        fails.append("no `Status: idea | draft | approved | built` line")
    elif require_approved and m.group(1) not in ("approved", "built"):
        fails.append(f"Status is {m.group(1)}; nothing is built from a spec the user has not approved")

    for title in SECTIONS:
        body = section(text, title)
        if body is None:
            fails.append(f"section `{title}` is missing")
        elif not filled(body):
            fails.append(f"section `{title}` is empty")

    criteria = section(text, "Acceptance criteria") or ""
    boxes = re.findall(r"^\s*-\s*\[[ xX]\]\s*(.*)$", criteria, re.M)
    if not [b for b in boxes if b.strip()]:
        fails.append("Acceptance criteria: no checkbox with text; the reviewer has nothing to check")
    for b in boxes:
        if not b.strip():
            fails.append("Acceptance criteria: an empty checkbox")

    tech = section(text, "Technical notes") or ""
    sv = re.search(r"Server vs client:[ \t]*(.*)", tech)
    if sv is not None and not sv.group(1).strip():
        fails.append("Technical notes: `Server vs client:` is blank; say what the server decides")

    for i, ln in enumerate(text.splitlines(), 1):
        ph = PLACEHOLDER.search(re.sub(r"<!--.*?-->", "", ln))
        if ph:
            fails.append(f"line {i}: template placeholder left in: {ph.group(0)[:40]}")

    if section(text, "Open questions") is None:
        fails.append("section `Open questions` is missing (leave it empty when every point was decided)")
    return fails


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    path = Path(args[0])
    if not path.is_file():
        print(f"FAIL  {path}: no such file")
        return 1
    fails = check(path.read_text(encoding="utf-8"), "--require-approved" in argv)
    for f in fails[:30]:
        print(f"FAIL  {f}")
    if len(fails) > 30:
        print(f"... and {len(fails) - 30} more")
    print(f"check_spec: {'PASS' if not fails else 'FAIL'} ({len(fails)} problems) {path.name}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

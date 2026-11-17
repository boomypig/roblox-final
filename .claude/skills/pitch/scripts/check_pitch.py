#!/usr/bin/env python3
"""Gate a /pitch file: is it the five scored pitches the skill promises, with honest evidence?

    check_pitch.py <pitch file>          # exit 1 on any FAIL
    check_pitch.py <pitch file> --quiet  # only the summary line

WHY THIS EXISTS. A pitch file is read once, by someone choosing what to spend weeks on, and the
ways it goes wrong are invisible in a skim: a total that is not the sum of its five scores (so
the summary table ranks the pitches wrongly), a trend number with no date (so nobody can tell
it is stale), a judgment that reads like a fact because `(inferred)` was left off, a pitch
missing its risks. The skill's rules say all of this; nothing checked it.

Checks:
  1. frontmatter has title, type: pitches, constraints, trends-report
  2. exactly five pitches, numbered 1 to 5
  3. every pitch has all ten fields
  4. every score is 1 to 5 and every total is the sum of its five scores
  5. the summary table lists all five, highest total first, with the same totals
  6. the closing sections exist, and the prototype pick is marked (inferred)
  7. every (data ...) citation carries a date
  8. nothing claims a pitch will succeed
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

FIELDS = ["Genre + themes", "Core loop", "Unique spin", "Reference games", "Why now",
          "Target audience", "Monetization", "Solo-dev scope", "Risks", "Scores"]
FRONTMATTER = ["title", "type", "constraints", "trends-report"]
PROMISE = re.compile(r"\b(will succeed|guaranteed|sure to (?:hit|succeed|work)|can't fail|cannot fail|will be a hit)\b", re.I)
DATA = re.compile(r"\(data\b([^)]*)\)")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
ROW = re.compile(r"^\|(.+)\|\s*$")


def cells(line: str) -> list[str]:
    m = ROW.match(line)
    return [c.strip() for c in m.group(1).split("|")] if m else []


def numbers(row: list[str]) -> list[float]:
    out = []
    for c in row:
        m = re.fullmatch(r"\**\s*(\d+(?:\.\d+)?)\s*(?:/\s*\d+)?\s*\**", c)
        if m:
            out.append(float(m.group(1)))
    return out


def check(text: str) -> list[str]:
    fails: list[str] = []
    lines = text.splitlines()

    # 1. frontmatter
    fm = {}
    if lines and lines[0].strip() == "---":
        for ln in lines[1:]:
            if ln.strip() == "---":
                break
            if ":" in ln:
                k, _, v = ln.partition(":")
                fm[k.strip()] = v.strip()
    for key in FRONTMATTER:
        if not fm.get(key):
            fails.append(f"frontmatter: `{key}` is missing or empty")
    if fm.get("type") and fm["type"] != "pitches":
        fails.append(f"frontmatter: type is `{fm['type']}`, expected `pitches`")

    # 2. five pitches
    heads = [(i, re.match(r"^## (\d+)\.\s+(.+)", ln)) for i, ln in enumerate(lines)]
    heads = [(i, int(m.group(1)), m.group(2)) for i, m in heads if m]
    nums = [n for _, n, _ in heads]
    if nums != [1, 2, 3, 4, 5]:
        fails.append(f"pitches: found headings numbered {nums or 'none'}, expected 1 to 5")

    # 3, 4. fields and scores per pitch
    totals: dict[int, float] = {}
    for idx, (start, n, title) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else next(
            (j for j in range(start + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
        body = lines[start:end]
        joined = "\n".join(body)
        for field in FIELDS:
            if not re.search(r"\*\*" + re.escape(field) + r":?\*\*", joined):
                fails.append(f"pitch {n}: field `{field}` is missing")
        scored = [numbers(cells(ln)) for ln in body if ROW.match(ln)]
        scored = [r for r in scored if len(r) == 6]
        if not scored:
            fails.append(f"pitch {n}: no score row with five scores and a total")
            continue
        *five, total = scored[0]
        for s in five:
            if not 1 <= s <= 5:
                fails.append(f"pitch {n}: score {s:g} is outside 1 to 5")
        if abs(sum(five) - total) > 1e-9:
            fails.append(f"pitch {n}: total {total:g} is not the sum of its scores ({sum(five):g})")
        totals[n] = total

    # 5. summary table
    tail_start = heads[-1][0] if heads else 0
    summary_at = next((i for i in range(tail_start, len(lines))
                       if re.match(r"^#{2,3} .*summary", lines[i], re.I) or re.match(r"^\*\*Summary", lines[i], re.I)), None)
    if summary_at is None:
        fails.append("summary table: no `Summary` heading after the pitches")
    else:
        rows = []
        for ln in lines[summary_at:]:
            if ln.startswith("## ") and rows:
                break
            ns = numbers(cells(ln))
            if len(ns) >= 6:
                rows.append(ns[-1])
        if len(rows) != 5:
            fails.append(f"summary table: {len(rows)} scored rows, expected 5")
        else:
            if rows != sorted(rows, reverse=True):
                fails.append(f"summary table: totals {[f'{r:g}' for r in rows]} are not sorted highest first")
            if totals and sorted(rows) != sorted(totals.values()):
                fails.append("summary table: totals differ from the totals in the pitches "
                             f"({sorted(f'{r:g}' for r in rows)} vs {sorted(f'{t:g}' for t in totals.values())})")

    # 6. closing sections
    low = text.lower()
    proto = re.search(r"what i'd prototype first.*", text, re.I)
    if not proto:
        fails.append("closing: no `What I'd prototype first and why` section")
    else:
        section = text[proto.start():proto.start() + 1500]
        if "(inferred)" not in section:
            fails.append("closing: the prototype pick is a judgment and must be marked (inferred)")
    if "what would change these scores" not in low:
        fails.append("closing: no `What would change these scores` section")

    # 7, 8. evidence
    for i, ln in enumerate(lines, 1):
        for m in DATA.finditer(ln):
            if not DATE.search(m.group(1)):
                fails.append(f"line {i}: `(data{m.group(1)})` has no date; cite the report date")
        m = PROMISE.search(ln)
        if m and "never" not in ln.lower() and "not " not in ln.lower():
            fails.append(f"line {i}: `{m.group(0)}` claims an outcome; no pitch may be promised to succeed")
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
    fails = check(path.read_text(encoding="utf-8"))
    if "--quiet" not in argv:
        for f in fails[:30]:
            print(f"FAIL  {f}")
        if len(fails) > 30:
            print(f"... and {len(fails) - 30} more")
    print(f"check_pitch: {'PASS' if not fails else 'FAIL'} ({len(fails)} problems) {path.name}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

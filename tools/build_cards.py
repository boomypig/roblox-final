#!/usr/bin/env python3
"""Build the agent cards: one file per agent carrying, word for word, every section it must act on.

    python3 tools/build_cards.py           # rewrite every card
    python3 tools/build_cards.py --check   # exit 1 if a card is missing, stale, or drops an item

WHY THIS EXISTS. The map-builder read about 24,000 tokens of reference before every run (three
files of 20 KB each, plus its own instructions), and the reviewer read the whole quality bar
and the whole roblox-code skill to find the sections it scores against. Most of that is
background the agent never acts on. A hand-written summary would be cheaper and would drop
things. So a card is generated: each section an agent acts on is copied verbatim from its
source with the file, heading and lines it came from, a coverage table counts the items
(checklist lines, bullets, table rows) in source and card, and each source section's hash is
recorded, so `--check` fails when a source changes and its card does not. The agent opens the
full reference only when a check fails, at the section the card names.

Run when editing the toolkit (and in CI via tests/test_cards.py), never during a game build.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SK = ".claude/skills"

# Each card: where it is written, what it says first, and the source sections it carries.
CARDS = {
    "map-builder": {
        "path": f"{SK}/roblox-map/references/builder-card.md",
        "title": "Map-builder card",
        "intro": """Everything the map-builder agent acts on during a run, copied word for word from the three
roblox-map references, with the place each part came from. Read this instead of the three full
files. Open a full reference only when a check fails or an item here is not enough to act on,
and then only the section named in that part's header.

Still read, every run: the map's state file, the approved art direction and map brief, the
genre file (`vault/genres/<genre>.md`) for dressing and props, and only the reference images
the brief links for the zone being built. The Luau checks are
`.claude/skills/roblox-map/scripts/luau/map_checks.lua`.""",
        "sections": [
            (f"{SK}/roblox-map/references/studio-mcp.md", "## `execute_luau`: rules that keep Studio alive"),
            (f"{SK}/roblox-map/references/studio-mcp.md", "## Vetting Creator Store assets"),
            (f"{SK}/roblox-map/references/studio-mcp.md", "## Common build bugs"),
            (f"{SK}/roblox-map/references/studio-mcp.md", "## Checklist for agents"),
            (f"{SK}/roblox-map/references/visual-quality.md", '## "Does this look default?" checklist'),
            (f"{SK}/roblox-map/references/visual-quality.md", "## Checklist for agents"),
            (f"{SK}/roblox-map/references/performance-and-devices.md", "## Budget table"),
            (f"{SK}/roblox-map/references/performance-and-devices.md", "## Checklist for agents"),
        ],
    },
    "reviewer": {
        "path": f"{SK}/build/references/reviewer-card.md",
        "title": "Reviewer card",
        "intro": """Everything the reviewer agent scores and checks against, copied word for word from the quality
bar, the roblox-code skill and its security reference, with the place each part came from.
Read this instead of the full files. Open a full reference only to cite it or when an item
here is not enough to judge, and then only the section named in that part's header.

Where the game keeps its remotes, pure rules and tunables is the game's own
`design/layout.json` when it exists. Read it first and check each rule below against those
paths; the rules name the roblox-code scaffold's defaults (`Net.luau`, `Core/`, `Config/`),
which apply only when there is no layout file.""",
        "sections": [
            (f"{SK}/build/references/quality-bar.md", "## How to review with it"),
            (f"{SK}/build/references/quality-bar.md", "## Why does it feel lackluster?"),
            *[(f"{SK}/build/references/quality-bar.md", f"## {x}.") for x in "ABCDEFGHIJKLM"],
            (f"{SK}/build/references/quality-bar.md", "## Genre checklists"),
            (f"{SK}/roblox-code/SKILL.md", "## The five standing rules"),
            (f"{SK}/roblox-code/SKILL.md", "## Server authority"),
            (f"{SK}/roblox-code/SKILL.md", "## The traps that cost real days"),
            (f"{SK}/roblox-code/SKILL.md", "## Anti-patterns"),
            (f"{SK}/roblox-code/references/security.md", "## Review checklist for any RemoteEvent handler"),
            (f"{SK}/roblox-code/references/security.md", "## Checklist for agents"),
        ],
    },
}

def heading_level(line: str) -> int:
    m = re.match(r"^(#+) ", line)
    return len(m.group(1)) if m else 0


def extract(path: str, heading: str) -> tuple[str, str, int, int]:
    """(full heading line, body, first line, last line) of the section whose heading starts with
    `heading`, up to the next heading of the same or a higher level. Fences are respected."""
    lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
    level = heading_level(heading)
    start = next((i for i, ln in enumerate(lines) if ln.startswith(heading)), None)
    if start is None:
        raise SystemExit(f"{path}: no heading starting with {heading!r}")
    end, fenced = len(lines), False
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("```"):
            fenced = not fenced
        if not fenced and 0 < heading_level(lines[i]) <= level:
            end = i
            break
    body = "\n".join(lines[start + 1:end]).strip("\n")
    return lines[start], body, start + 1, end


def items(text: str) -> int:
    """Checklist lines, bullets, numbered items and table body rows: the things an agent acts on.
    Lines inside code fences are not counted; a table's first row is its header."""
    count, fenced, in_table = 0, False, False
    for ln in text.splitlines():
        if ln.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if ln.startswith("|"):
            if re.match(r"^\|[\s:|-]+\|\s*$", ln):
                continue
            if in_table:
                count += 1
            in_table = True
            continue
        in_table = False
        if re.match(r"^(?:[-*] |\d+\. |\*\*\d+\. )", ln):
            count += 1
    return count


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def render(name: str) -> str:
    card = CARDS[name]
    parts, rows, built = [], [], []
    for n, (path, heading) in enumerate(card["sections"], 1):
        full, body, first, last = extract(path, heading)
        title = re.sub(r"^#+\s*", "", full)
        built.append(f"  - {path} | {title} | sha256:{digest(body)}")
        rows.append(f"| {n} | `{path}` | {title} | {first}-{last} | {items(body)} |")
        demoted = re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", body, flags=re.M)
        parts.append(f"## {n}. {title}\n\nSource: `{path}`, lines {first}-{last}.\n\n{demoted}\n")
    head = [
        "---",
        f"title: {card['title']}",
        "generated-by: python3 tools/build_cards.py (never hand-edit; rerun after editing a source)",
        "built-from:",
        *built,
        "---",
        "",
        f"# {card['title']}",
        "",
        card["intro"],
        "",
        "## Coverage",
        "",
        "Every section below is copied whole. Items are checklist lines, bullets, numbered items",
        "and table rows; the card holds the same count as its source (tests/test_cards.py).",
        "",
        "| # | Source | Section | Lines | Items |",
        "|---|---|---|---|---|",
        *rows,
        "",
    ]
    return "\n".join(head) + "\n" + "\n".join(parts)


def check(name: str) -> list[str]:
    path = ROOT / CARDS[name]["path"]
    if not path.exists():
        return [f"{CARDS[name]['path']} is missing; run python3 tools/build_cards.py"]
    if path.read_text(encoding="utf-8") != render(name):
        return [f"{CARDS[name]['path']} is stale: a source section changed; run python3 tools/build_cards.py"]
    return []


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="report stale or missing cards; write nothing")
    a = ap.parse_args(argv)
    problems = []
    for name, card in CARDS.items():
        if a.check:
            problems += check(name)
        else:
            (ROOT / card["path"]).write_text(render(name), encoding="utf-8")
            print(f"wrote {card['path']}")
    for p in problems:
        print(f"FAIL  {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

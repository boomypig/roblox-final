#!/usr/bin/env python3
"""Print map_checks.lua with a map's own parameters, ready to paste into execute_luau.

    map_checks.py --state docs/design/maps/harbor.state.md        # params from the state file
    map_checks.py --state <file> --only inventory                 # just the inventory
    map_checks.py                                                 # the defaults in the .lua

WHY THIS EXISTS. map_checks.lua takes its numbers (lane width, refuge distance, hiding-spot
size) from a PARAMS block, and those numbers belong to one map's brief. Hand-editing the block
before each run is how a check ends up running on the previous map's numbers, or on the
defaults, while reporting PASS. The map's state file holds the block; this splices it in and
refuses a block that is not a `local PARAMS = { ... }` table.

The map-builder agent has no shell: it does the same substitution itself (copy the state
file's block between the PARAMS markers). This script is for people, the smoke test and CI.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LUA = HERE / "luau" / "map_checks.lua"
BEGIN, END = "-- PARAMS BEGIN", "-- PARAMS END"
CHECKS = ("inventory", "properties", "lanes", "refuge", "hiding")
BLOCK = re.compile(r"^## Check parameters\s*$.*?^```lua\s*$\n(.*?)^```\s*$", re.M | re.S)


def params_from_state(text: str) -> str:
    m = BLOCK.search(text)
    if not m:
        raise SystemExit("the state file has no '## Check parameters' section with a ```lua block")
    block = m.group(1).strip()
    if not re.match(r"^local PARAMS\s*=\s*\{", block) or not block.endswith("}"):
        raise SystemExit("the Check parameters block must be one `local PARAMS = { ... }` table")
    if block.count("{") != block.count("}"):
        raise SystemExit("the Check parameters block has unbalanced braces")
    return block


def only(block: str, names: list[str]) -> str:
    unknown = [n for n in names if n not in CHECKS]
    if unknown:
        raise SystemExit(f"unknown check(s): {', '.join(unknown)}; checks are {', '.join(CHECKS)}")
    flags = ", ".join(f"{c} = {'true' if c in names else 'false'}" for c in CHECKS)
    out, n = re.subn(r"checks\s*=\s*\{[^}]*\}", f"checks = {{ {flags} }}", block, count=1)
    if n != 1:
        raise SystemExit("the PARAMS block has no `checks = { ... }` entry to narrow")
    return out


def split(lua: str) -> tuple[str, str, str]:
    """(before, current params block, after), where the markers are whole lines."""
    m = re.search(rf"^{re.escape(BEGIN)}\s*$\n(.*?)^{re.escape(END)}\s*$", lua, re.M | re.S)
    if not m:
        raise SystemExit(f"{LUA} has no '{BEGIN}' ... '{END}' lines")
    return lua[:m.start()], m.group(1).strip(), lua[m.end():]


def emit(block: str | None) -> str:
    head, current, tail = split(LUA.read_text(encoding="utf-8"))
    return f"{head}{BEGIN}\n{block if block is not None else current}\n{END}{tail}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--state", type=Path, help="the map's state file (docs/design/maps/<name>.state.md)")
    ap.add_argument("--only", help="comma-separated checks to run: " + ", ".join(CHECKS))
    a = ap.parse_args(argv)
    block = params_from_state(a.state.read_text(encoding="utf-8")) if a.state else None
    if a.only:
        if block is None:
            block = split(LUA.read_text(encoding="utf-8"))[1]
        block = only(block, [s.strip() for s in a.only.split(",") if s.strip()])
    sys.stdout.write(emit(block))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Load a game's layout map, design/layout.json, with the scaffold's values as defaults.

    layout.py show  --dir <game>    # the layout every reader uses, defaults filled in
    layout.py check --dir <game>    # exit 1 if the file is malformed or names a missing path

WHY THIS EXISTS. check.py, /build and the reviewer assumed every game was laid out like the
scaffold: Knit, a Net.luau of remotes, a Core/ folder of pure rules, a Config/ folder, Wally
packages and a tests/ folder. A game made before the toolkit kept the same things elsewhere
(plain modules, remotes created per service, one Config.luau, pure modules loose in
src/shared, no packages, no tests), so check.py failed on folders the game never had and the
reviewer judged code against paths that did not exist. The layout map says where things are;
this module is the one reader. The schema is references/layout.md.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

# The roblox-code scaffold (new_project.py). A game with no layout.json is read as this.
DEFAULT: dict = {
    "version": 1,
    "framework": "knit",
    "boot": {"server": "src/server/init.server.luau", "client": "src/client/init.client.luau"},
    "services": "src/server/Services",
    "controllers": "src/client/Controllers",
    "remotes": {"style": "net-module", "where": "src/shared/Net.luau"},
    "config": "src/shared/Config",
    "pure": ["src/shared/Core"],
    "tests": "tests",
    "packages": "wally",
    "toolchain": "aftman.toml",
    "lint": ["src"],
    "format": ["src", "lune"],
    "map": {"source": "prover", "spec": "design/map.json"},
    "adopted": False,
    "notes": [],
}

CHOICES = {
    "framework": {"knit", "modules"},
    "packages": {"wally", "none"},
    "toolchain": {"aftman.toml", "rokit.toml"},
}


def path_of(root: Path) -> Path:
    return root / "design" / "layout.json"


def load(root: Path) -> tuple[dict, bool]:
    """(layout with defaults filled in, whether design/layout.json exists)."""
    out = copy.deepcopy(DEFAULT)
    p = path_of(root)
    if not p.exists():
        return out, False
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("design/layout.json is not a JSON object")
    for key, value in data.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = {**out[key], **value}
        else:
            out[key] = value
    return out, True


def problems(layout: dict, root: Path) -> list[str]:
    """What is wrong with a layout: unknown values, and paths that do not exist."""
    out: list[str] = []
    for key, allowed in CHOICES.items():
        if layout.get(key) not in allowed:
            out.append(f"{key} is {layout.get(key)!r}; expected one of {sorted(allowed)}")
    style = layout["remotes"].get("style")
    if style not in ("net-module", "per-service"):
        out.append(f"remotes.style is {style!r}; expected 'net-module' or 'per-service'")
    files = [layout["boot"].get("server"), layout["boot"].get("client"), layout["services"],
             layout["controllers"], layout["config"], *layout.get("pure", [])]
    if style == "net-module":
        files.append(layout["remotes"].get("where"))
    if layout.get("tests"):
        files.append(layout["tests"])
    m = layout.get("map") or {}
    if m.get("source") == "studio" and m.get("brief"):
        files.append(m["brief"])
    if layout["toolchain"] and not (root / layout["toolchain"]).exists():
        out.append(f"toolchain {layout['toolchain']} does not exist")
    for rel in files:
        if rel and not (root / rel).exists():
            out.append(f"{rel} does not exist")
    return out


def existing(root: Path, paths: list[str]) -> list[str]:
    return [p for p in paths if (root / p).exists()]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("cmd", choices=["show", "check"])
    ap.add_argument("--dir", default=".")
    a = ap.parse_args(argv)
    root = Path(a.dir).expanduser().resolve()
    try:
        layout, found = load(root)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL  design/layout.json: {exc}")
        return 1
    if a.cmd == "show":
        print(json.dumps(layout, indent=2))
        if not found:
            print("(no design/layout.json: the scaffold's layout is assumed)", file=sys.stderr)
        return 0
    bad = problems(layout, root)
    for b in bad:
        print(f"FAIL  {b}")
    if not bad:
        print("layout ok" + ("" if found else " (no design/layout.json: scaffold defaults)"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

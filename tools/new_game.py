#!/usr/bin/env python3
"""Make a complete new game repo next to roblox-final in one command.

    python3 ~/roblox-final/tools/new_game.py "Small Hours"            # -> ~/small-hours
    python3 ~/roblox-final/tools/new_game.py "Small Hours" --dir ~/games/small-hours

What it writes, each from the one place that owns it:

1. The code scaffold: roblox-code's `scripts/new_project.py` (Rojo, Knit, Net, Config, one pure
   Core module with a spec, the Lune runner, pinned tools). Green on all four gates once the
   tools and packages are installed, before any game code exists.
2. The build contract: create-roblox-game's `scripts/new_game.py` (`design/game.json`, one stub
   spec per stage, `BUILD.md`). It is full of TODO markers on purpose: `validate.py` fails until
   section 1 fills them.
3. The layout map, `design/layout.json`: the scaffold's layout (roblox-code
   `scripts/layout.py`), read by check.py, /build and the reviewer.
4. The starter (`starter/`): CLAUDE.md (a task -> file list; status lives in HANDOFF.md),
   docs, `.claude/settings.json` (read access to the toolkit and the Stop hook that runs
   create-roblox-game's `scripts/session.py`), `.mcp.json`, and the first HANDOFF.md.
   Files the scaffold already wrote are kept; `.gitignore` lines are merged.
5. The map state template (roblox-map `references/map-state.template.md`) as
   `docs/design/maps/_template.state.md`, and the folders the briefs and backups expect.

Then `git init`. The old command, create-roblox-game's `scripts/new_game.py`, forwards here.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # roblox-final
SKILLS = ROOT / ".claude" / "skills"
SCAFFOLD = SKILLS / "roblox-code" / "scripts" / "new_project.py"
STARTER = ROOT / "starter"
MAP_STATE = SKILLS / "roblox-map" / "references" / "map-state.template.md"
SKIP = {"README.md", ".gitignore"}                     # the starter's own readme; .gitignore is merged
FILLED = {"CLAUDE.md", "HANDOFF.md"}                   # files whose <Game name> and <made on> are filled
EXTRA_DIRS = ["docs/images/ref", "docs/design/maps", "maps"]

def _load(name: str, path: Path):
    """Import a skill's script by path: this file shares the name new_game.py with one of them."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


contract = _load("crg_contract", SKILLS / "create-roblox-game" / "scripts" / "new_game.py")  # the contract's owner
layout_map = _load("rc_layout", SKILLS / "roblox-code" / "scripts" / "layout.py")  # the layout map's owner


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "new-game"


def overlay(dst: Path, title: str) -> list[str]:
    kept = []
    for src in sorted(STARTER.rglob("*")):
        rel = src.relative_to(STARTER)
        if src.is_dir() or rel.as_posix() in SKIP:
            continue
        out = dst / rel
        if out.exists():
            kept.append(rel.as_posix())
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        if rel.as_posix() in FILLED:
            text = src.read_text(encoding="utf-8")
            text = text.replace("<Game name>", title).replace("<made on>", date.today().isoformat())
            out.write_text(text, encoding="utf-8", newline="\n")
        else:
            shutil.copy2(src, out)
    return kept


def merge_gitignore(dst: Path) -> None:
    target = dst / ".gitignore"
    have = target.read_text(encoding="utf-8").splitlines() if target.exists() else []
    add = [ln for ln in (STARTER / ".gitignore").read_text(encoding="utf-8").splitlines()
           if ln.strip() and not ln.startswith("#") and ln not in have]
    if add:
        head = "# From the toolkit starter: place files, session state, Windows metadata"
        text = "\n".join(have).rstrip("\n") + "\n\n" + head + "\n" + "\n".join(add) + "\n"
        target.write_text(text.lstrip("\n"), encoding="utf-8")


def make(title: str, dst: Path, force: bool = False, quiet: bool = False) -> int:
    cmd = [sys.executable, str(SCAFFOLD), title, "--dir", str(dst)] + (["--force"] if force else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout + r.stderr, file=sys.stderr)
        print("scaffold failed; nothing else was written", file=sys.stderr)
        return 1

    contract.write_contract(dst, title)
    layout_path = layout_map.path_of(dst)
    layout_path.write_text(json.dumps(layout_map.DEFAULT, indent=2) + "\n", encoding="utf-8")
    kept = overlay(dst, title)
    merge_gitignore(dst)
    for d in EXTRA_DIRS:
        (dst / d).mkdir(parents=True, exist_ok=True)
    state = dst / "docs" / "design" / "maps" / "_template.state.md"
    if not state.exists():
        shutil.copy2(MAP_STATE, state)
    for d in EXTRA_DIRS:
        if not any((dst / d).iterdir()):
            (dst / d / ".gitkeep").touch()
    if not (dst / ".git").exists() and shutil.which("git"):
        subprocess.run(["git", "init", "-q", "-b", "main", str(dst)], check=False)

    if quiet:
        return 0
    rel = "../roblox-final" if dst.parent == ROOT.parent else str(ROOT)
    print(f"made {title} at {dst}" + (f" (kept the scaffold's {', '.join(kept)})" if kept else ""))
    if dst.parent != ROOT.parent:
        print(f"note: the game is not next to roblox-final, so edit .claude/settings.json and "
              f"CLAUDE.md to point at {ROOT} instead of ../roblox-final")
    print("\nnext:")
    print(f"  cd {dst}")
    print("  rokit install   # reads aftman.toml: rojo, wally, selene, stylua, lune")
    print("  wally install")
    print(f"  python3 {rel}/.claude/skills/roblox-code/scripts/check.py   # 4 gates green")
    print(f"  claude --add-dir {rel}")
    print('  then: "complete the research and plan stage" (create-roblox-game, section 1)')
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("title", help='game title, e.g. "Small Hours"')
    ap.add_argument("--dir", type=Path, help="game folder (default: a sibling of roblox-final)")
    ap.add_argument("--force", action="store_true", help="write into a non-empty folder")
    a = ap.parse_args(argv)
    dst = (a.dir or ROOT.parent / slug(a.title)).expanduser().resolve()
    return make(a.title, dst, a.force)


if __name__ == "__main__":
    raise SystemExit(main())

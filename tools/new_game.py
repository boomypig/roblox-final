#!/usr/bin/env python3
"""Make a new game repo next to roblox-final, ready for the whole workflow.

    python3 ~/roblox-final/tools/new_game.py "Small Hours"            # -> ~/small-hours
    python3 ~/roblox-final/tools/new_game.py "Small Hours" --dir ~/games/small-hours

Two halves, one command, so a new game never gets only one of them:

1. create-roblox-game's new_game.py: the roblox-code scaffold (Rojo + Knit + Net + Core +
   Lune tests, green on all four gates), design/game.json (the build contract) and BUILD.md.
2. roblox-final/starter/: CLAUDE.md, docs/ (workflow, pitch, glossary, decisions, spec and
   reference templates), .claude/settings.json (read access to ../roblox-final) and .mcp.json.
   Files the scaffold already wrote are kept; .gitignore lines are merged, not replaced.

Then it makes the folders the briefs and map backups expect and runs `git init`.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # roblox-final
SCAFFOLD = ROOT / ".claude" / "skills" / "create-roblox-game" / "scripts" / "new_game.py"
STARTER = ROOT / "starter"
SKIP = {"README.md", ".gitignore"}                     # starter's own readme; .gitignore is merged
EXTRA_DIRS = ["docs/images/ref", "docs/design/maps", "maps"]


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "new-game"


def overlay(dst: Path) -> list[str]:
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
        shutil.copy2(src, out)
    return kept


def merge_gitignore(dst: Path) -> None:
    target = dst / ".gitignore"
    have = target.read_text(encoding="utf-8").splitlines() if target.exists() else []
    add = [ln for ln in (STARTER / ".gitignore").read_text(encoding="utf-8").splitlines()
           if ln.strip() and not ln.startswith("#") and ln not in have]
    if add:
        head = "# Studio place files (back maps up as .rbxm instead) and Windows metadata"
        text = "\n".join(have).rstrip("\n") + "\n\n" + head + "\n" + "\n".join(add) + "\n"
        target.write_text(text.lstrip("\n"), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("title", help='game title, e.g. "Small Hours"')
    ap.add_argument("--dir", type=Path, help="game folder (default: a sibling of roblox-final)")
    ap.add_argument("--force", action="store_true", help="write into a non-empty folder")
    a = ap.parse_args()

    dst = (a.dir or ROOT.parent / slug(a.title)).expanduser().resolve()
    cmd = [sys.executable, str(SCAFFOLD), a.title, "--dir", str(dst)] + (["--force"] if a.force else [])
    if subprocess.run(cmd).returncode != 0:
        print("scaffold failed; nothing from starter/ was copied", file=sys.stderr)
        return 1

    kept = overlay(dst)
    merge_gitignore(dst)
    for d in EXTRA_DIRS:
        (dst / d).mkdir(parents=True, exist_ok=True)
        keep = dst / d / ".gitkeep"
        if not any((dst / d).iterdir()):
            keep.touch()
    if not (dst / ".git").exists() and shutil.which("git"):
        subprocess.run(["git", "init", "-q", "-b", "main", str(dst)])

    rel = "../roblox-final" if dst.parent == ROOT.parent else str(ROOT)
    print(f"\nstarter docs added to {dst}" + (f" (kept the scaffold's {', '.join(kept)})" if kept else ""))
    if dst.parent != ROOT.parent:
        print(f"note: the game is not next to roblox-final, so edit .claude/settings.json and "
              f"CLAUDE.md to point at {ROOT} instead of ../roblox-final")
    print("\nnext:")
    print(f"  cd {dst}")
    print("  rokit install   # or: aftman install   (pinned rojo, wally, selene, stylua, lune)")
    print("  wally install")
    print("  python3 ~/roblox-final/.claude/skills/roblox-code/scripts/check.py   # 4 gates green")
    print(f"  claude --add-dir {rel}")
    print('  then: "complete the research and plan stage" (create-roblox-game, section 1)')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Rewrite a game repo's references to toolkit paths that moved.

    python3 ~/roblox-final/tools/migrate_game.py <game dir>           # show what would change
    python3 ~/roblox-final/tools/migrate_game.py <game dir> --write   # apply it

WHY THIS EXISTS. A game repo's CLAUDE.md, docs and handoffs name toolkit files by path
(`../roblox-final/vault/fundamentals/quality-bar.md`, `~/roblox-final/goals.md`). When the
toolkit moved its private notes into private/ and its build references into the owning skills,
every such path in an existing game went dead, and a dead path in a game's CLAUDE.md is read
by every session of that game. This script rewrites them. It is run by the game's owner inside
that game; it never touches the toolkit, never deletes a file, and changes nothing without
--write.

Only references that carry the toolkit's folder name (`roblox-final/...`) or a full vault path
(`vault/fundamentals/quality-bar.md`) are rewritten. A bare `goals.md` or `workflow.md` could be
the game's own file, so those are listed for you to check by hand.

The table below is the single list of moves. docs/migration.md shows the same list and
tests/test_migration.py keeps the two equal.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SK = ".claude/skills"
# old path -> new path, both relative to the toolkit root. A trailing "/" moves a folder.
MOVES: list[tuple[str, str]] = [
    ("goals.md", "private/goals.md"),
    ("pitches/", "private/pitches/"),
    ("docs/history/", "private/history/"),
    ("vault/trends/", "private/trends/"),
    ("vault/case-studies/", "private/case-studies/"),
    ("tools/trends/data/", "private/trends/data/"),
    ("vault/fundamentals/quality-bar.md", f"{SK}/build/references/quality-bar.md"),
    ("vault/fundamentals/security-and-anti-exploit.md", f"{SK}/roblox-code/references/security.md"),
    ("vault/fundamentals/ui-ux.md", f"{SK}/roblox-ui/references/ui-ux.md"),
    ("vault/fundamentals/game-feel.md", f"{SK}/roblox-vfx/references/game-feel.md"),
    ("vault/fundamentals/visual-quality.md", f"{SK}/roblox-map/references/visual-quality.md"),
    ("vault/fundamentals/performance-and-devices.md", f"{SK}/roblox-map/references/performance-and-devices.md"),
    ("vault/fundamentals/building-with-studio-mcp.md", f"{SK}/roblox-map/references/studio-mcp.md"),
]
# Files a game used to carry that the toolkit now owns. Reported, never deleted.
SUPERSEDED = {
    "docs/workflow.md": "the one workflow doc is the toolkit's docs/workflow.md; point CLAUDE.md at "
                        "../roblox-final/docs/workflow.md and remove this copy when you are ready",
}
BARE = [
    (re.compile(r"(?<![\w/.-])goals\.md"), "bare `goals.md`: the toolkit's is now private/goals.md"),
    (re.compile(r"(?<![\w/-])quality-bar\.md"), "bare `quality-bar.md`: now build/references/quality-bar.md in the toolkit"),
]
TEXT = {".md", ".json", ".py", ".toml", ".txt", ".sh", ".yaml", ".yml", ".luau", ".lua"}
SKIP_DIRS = {".git", "Packages", "ServerPackages", "node_modules", "work", "build-runs", "__pycache__", ".venv"}
TOOLKIT = r"roblox-final/"


def rewrite(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Return the new text and the (old, new) pairs applied."""
    applied: list[tuple[str, str]] = []
    for old, new in MOVES:
        prefixed = re.compile(r"(" + TOOLKIT + r")" + re.escape(old) + (r"" if old.endswith("/") else r"(?![\w-])"))
        if prefixed.search(text):
            text = prefixed.sub(lambda m, new=new: m.group(1) + new, text)
            applied.append((old, new))
        if old.startswith("vault/fundamentals/"):
            bare = re.compile(r"(?<![\w/.-])" + re.escape(old) + r"(?![\w-])")
            if bare.search(text):
                text = bare.sub(new, text)
                applied.append((old, new))
    return text, applied


def files(game: Path):
    for p in sorted(game.rglob("*")):
        if p.is_file() and p.suffix.lower() in TEXT and not (set(p.relative_to(game).parts) & SKIP_DIRS):
            yield p


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("game", type=Path, help="the game repo to migrate")
    ap.add_argument("--write", action="store_true", help="apply the changes (default: only show them)")
    a = ap.parse_args(argv)

    game = a.game.expanduser().resolve()
    if not game.is_dir():
        print(f"{game} is not a folder")
        return 2
    if (game / ".claude" / "skills" / "create-roblox-game").exists() and (game / "vault").exists():
        print(f"{game} is the toolkit itself; this script migrates game repos")
        return 2

    changed, by_hand = 0, []
    for p in files(game):
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = p.relative_to(game).as_posix()
        new_text, applied = rewrite(text)
        if applied:
            changed += 1
            for old, new in applied:
                print(f"{'rewrote' if a.write else 'would rewrite'}  {rel}: {old} -> {new}")
            if a.write:
                p.write_text(new_text, encoding="utf-8")
        for n, line in enumerate(new_text.splitlines(), 1):
            if "private/" in line or "references/" in line:
                continue
            for pattern, why in BARE:
                if pattern.search(line):
                    by_hand.append(f"{rel}:{n}: {why}")
    for rel, why in SUPERSEDED.items():
        if (game / rel).exists():
            by_hand.append(f"{rel}: {why}")

    for item in by_hand[:30]:
        print(f"check by hand  {item}")
    if len(by_hand) > 30:
        print(f"... and {len(by_hand) - 30} more to check by hand")
    verb = "rewrote" if a.write else "would rewrite"
    print(f"migrate_game: {verb} {changed} file(s); {len(by_hand)} item(s) to check by hand"
          + ("" if a.write or not changed else "; run again with --write to apply"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

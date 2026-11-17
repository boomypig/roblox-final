#!/usr/bin/env python3
"""Rewrite a game repo's references to toolkit paths that moved.

    python3 ~/roblox-final/tools/migrate_game.py <game dir>           # show what would change
    python3 ~/roblox-final/tools/migrate_game.py <game dir> --write   # apply it

WHY THIS EXISTS. A game repo's CLAUDE.md, docs and handoffs name toolkit files by path: a
vault fundamentals file, the goals file. When the toolkit moved its private notes into
private/ and its build references into the owning skills, every such path in an existing game
went dead, and a dead path in a game's CLAUDE.md is read by every session of that game. This
script rewrites them. It is run by the game's owner inside that game; it never touches the
toolkit, never deletes a file, and changes nothing without --write.

Only references that carry the toolkit's folder name (`roblox-final/...`) or a full vault
fundamentals path are rewritten. A bare file name (the goals file, the quality bar,
`workflow.md`) could be the game's own file, so those are listed for you to check by hand.

The single list of moves is the table in docs/migration.md, "Rewritten by the script"; this
script reads it, so the old paths are written down in one place only. The new private/ paths
may not exist in a game's toolkit checkout: a rewrite changes text only, and each skill says
what it does when a private file is missing.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TOOLKIT_ROOT = Path(__file__).resolve().parents[1]
MIGRATION_DOC = TOOLKIT_ROOT / "docs" / "migration.md"


def load_moves(doc: Path = MIGRATION_DOC) -> list[tuple[str, str]]:
    """The (old, new) rows of docs/migration.md's "Rewritten by the script" table, both relative
    to the toolkit root. A trailing "/" moves a folder."""
    text = doc.read_text(encoding="utf-8")
    section = text.split("## Rewritten by the script", 1)[1].split("\n## ", 1)[0]
    rows = re.findall(r"^\| `([^`]+)` \| `([^`]+)` \|", section, re.M)
    if not rows:
        raise SystemExit(f"{doc}: no rows under 'Rewritten by the script'")
    return rows


MOVES: list[tuple[str, str]] = load_moves()
# Files a game used to carry that the toolkit now owns. Reported, never deleted.
SUPERSEDED = {
    "docs/workflow.md": "the one workflow doc is the toolkit's docs/workflow.md; point CLAUDE.md at "
                        "../roblox-final/docs/workflow.md and remove this copy when you are ready",
}


def bare_checks(moves: list[tuple[str, str]]) -> list[tuple[re.Pattern, str]]:
    """A bare file name from a moved file (the goals file, the quality bar) that may be the
    game's own file: reported, never rewritten. Only the root goals file and the quality bar
    are common enough as bare names to be worth a report."""
    out = []
    for old, new in moves:
        name = old.rsplit("/", 1)[-1]
        if old == name or name == "quality-bar.md":
            out.append((re.compile(r"(?<![\w/.-])" + re.escape(name)),
                        f"bare `{name}`: the toolkit's is now {new}"))
    return out


BARE = bare_checks(MOVES)
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

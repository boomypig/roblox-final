"""Existing games keep working: every moved path is listed, and migrate_game.py rewrites it.

Defect this exists for: a game repo names toolkit files by path. Moving goals, pitches, trend
reports, case studies and seven build references left those paths dead in every existing game.
docs/migration.md lists each move and tools/migrate_game.py reads that list and applies it in a
game; this test keeps the list, the script and the disk in agreement.

The old paths are written down only in docs/migration.md, so this test builds its sample game
from that table. The new private/ paths may not exist in a clone; the script rewrites text only.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import migrate_game  # noqa: E402

SCRIPT = ROOT / "tools" / "migrate_game.py"
TK = "../roblox-final/"


def move(stem: str) -> tuple[str, str]:
    """The one (old, new) row whose old path's last part, without extension, is `stem`."""
    rows = [r for r in migrate_game.MOVES if r[0].rstrip("/").rsplit("/", 1)[-1].split(".")[0] == stem]
    assert len(rows) == 1, f"{stem}: {rows}"
    return rows[0]


QUALITY = move("quality-bar")
SECURITY = move("security-and-anti-exploit")
PERF = move("performance-and-devices")
GOALS = move("goals")
PITCHES = move("pitches")
TRENDS = move("trends")
CASES = move("case-studies")
TRACKER = move("data")
FUNDAMENTALS = QUALITY[0].rsplit("/", 1)[0]  # the folder seven references left
STAYS = f"{FUNDAMENTALS}/metadata-thumbnails-icons.md"  # a fundamentals file that did not move

OLD_GAME_CLAUDE = f"""# Test game
- Quality bar: {TK}{QUALITY[0]}
- Security: ~/roblox-final/{SECURITY[0]} for remotes
- Phone first ({GOALS[0]})
- docs/pitch.md from {TK}{PITCHES[0]}first-idea.md
- Market: {TK}{TRENDS[0]}latest.md and {TK}{CASES[0]}doors.md
- Index: {TK}vault/INDEX.md
- Budgets: {PERF[0]}
- Stays: {STAYS}
"""


class Migration(unittest.TestCase):
    def test_moves_come_from_the_doc_table(self):
        doc = (ROOT / "docs" / "migration.md").read_text(encoding="utf-8")
        section = doc.split("## Rewritten by the script", 1)[1].split("## Not rewritten", 1)[0]
        rows = re.findall(r"^\| `([^`]+)` \| `([^`]+)` \|", section, re.M)
        self.assertEqual(len(rows), 13, "goals, pitches, history, trends, case studies, tracker data, seven references")
        self.assertEqual(rows, migrate_game.MOVES)
        self.assertNotIn("MOVES: list[tuple[str, str]] = [", SCRIPT.read_text(encoding="utf-8"),
                         "the script must read the table, not keep a second copy")

    def test_old_paths_are_gone_and_public_new_paths_exist(self):
        for old, new in migrate_game.MOVES:
            # the tracker's old data folder is still gitignored, so an old checkout may keep it
            self.assertFalse((ROOT / old).exists() and old != TRACKER[0], f"{old} still exists")
            if not new.startswith("private/"):
                self.assertTrue((ROOT / new).exists(), f"{new} does not exist")

    def test_index_path_is_still_valid(self):
        self.assertTrue((ROOT / "vault" / "INDEX.md").is_file())

    def test_dry_run_changes_nothing_and_write_rewrites(self):
        with tempfile.TemporaryDirectory() as d:
            game = Path(d) / "old-game"
            (game / "docs").mkdir(parents=True)
            (game / "CLAUDE.md").write_text(OLD_GAME_CLAUDE, encoding="utf-8")
            (game / "docs" / "workflow.md").write_text("# Workflow\n", encoding="utf-8")

            dry = subprocess.run([sys.executable, str(SCRIPT), str(game)], capture_output=True, text=True)
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertIn("would rewrite", dry.stdout)
            self.assertEqual((game / "CLAUDE.md").read_text(encoding="utf-8"), OLD_GAME_CLAUDE)

            wet = subprocess.run([sys.executable, str(SCRIPT), str(game), "--write"], capture_output=True, text=True)
            self.assertEqual(wet.returncode, 0, wet.stderr)
            new = (game / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertIn(f"{TK}.claude/skills/build/references/quality-bar.md", new)
            self.assertIn("~/roblox-final/.claude/skills/roblox-code/references/security.md", new)
            self.assertIn(f"{TK}{PITCHES[1]}first-idea.md", new)
            self.assertIn(f"{TK}{TRENDS[1]}latest.md", new)
            self.assertIn(f"{TK}{CASES[1]}doors.md", new)
            self.assertIn(f"{TK}vault/INDEX.md", new)
            self.assertIn(".claude/skills/roblox-map/references/performance-and-devices.md", new)
            self.assertIn(STAYS, new)
            self.assertNotIn(QUALITY[0], new)
            # ambiguous things are reported, not touched
            self.assertIn(f"({GOALS[0]})", new)
            self.assertIn("check by hand", wet.stdout)
            self.assertIn("docs/workflow.md", wet.stdout)
            self.assertTrue((game / "docs" / "workflow.md").exists(), "the script must never delete a file")

            again = subprocess.run([sys.executable, str(SCRIPT), str(game), "--write"], capture_output=True, text=True)
            self.assertIn("rewrote 0 file(s)", again.stdout, "a second run must find nothing left to rewrite")

    def test_refuses_to_run_on_the_toolkit(self):
        r = subprocess.run([sys.executable, str(SCRIPT), str(ROOT)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("toolkit itself", r.stdout)

    def test_no_tracked_file_names_an_old_path(self):
        out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-co", "--exclude-standard"],
                             capture_output=True, text=True)
        if out.returncode != 0:
            self.skipTest("not a git checkout")
        # The files tests/test_public_tree.py already allows to name old paths, and nothing else.
        allowed = {"docs/migration.md", "CHANGELOG.md", "docs/decisions.md", ".gitignore"}
        olds = [old for old, _ in migrate_game.MOVES if old.startswith(FUNDAMENTALS + "/")]
        hits = []
        for rel in filter(None, out.stdout.splitlines()):
            p = ROOT / rel
            if rel in allowed or not p.is_file():
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            hits += [f"{rel}: {old}" for old in olds if old in text]
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()

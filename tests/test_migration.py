"""Existing games keep working: every moved path is listed, and migrate_game.py rewrites it.

Defect this exists for: a game repo names toolkit files by path. Moving goals, pitches, trend
reports, case studies and seven build references left those paths dead in every existing game.
docs/migration.md lists each move; tools/migrate_game.py applies them in a game; this test
keeps the list, the script and the disk in agreement.

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

OLD_GAME_CLAUDE = """# Test game
- Quality bar: ../roblox-final/vault/fundamentals/quality-bar.md
- Security: ~/roblox-final/vault/fundamentals/security-and-anti-exploit.md for remotes
- Phone first (goals.md)
- docs/pitch.md from ../roblox-final/pitches/2026-01-01.md
- Market: ../roblox-final/vault/trends/latest.md and ../roblox-final/vault/case-studies/doors.md
- Index: ../roblox-final/vault/INDEX.md
- Budgets: vault/fundamentals/performance-and-devices.md
- Stays: vault/fundamentals/metadata-thumbnails-icons.md
"""


class Migration(unittest.TestCase):
    def test_doc_table_equals_the_script(self):
        doc = (ROOT / "docs" / "migration.md").read_text(encoding="utf-8")
        section = doc.split("## Rewritten by the script", 1)[1].split("## Not rewritten", 1)[0]
        rows = re.findall(r"^\| `([^`]+)` \| `([^`]+)` \|", section, re.M)
        self.assertEqual(rows, migrate_game.MOVES)

    def test_old_paths_are_gone_and_public_new_paths_exist(self):
        for old, new in migrate_game.MOVES:
            self.assertFalse((ROOT / old).exists() and not old.startswith("tools/trends/data"),
                             f"{old} still exists")
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
            self.assertIn("../roblox-final/.claude/skills/build/references/quality-bar.md", new)
            self.assertIn("~/roblox-final/.claude/skills/roblox-code/references/security.md", new)
            self.assertIn("../roblox-final/private/pitches/2026-01-01.md", new)
            self.assertIn("../roblox-final/private/trends/latest.md", new)
            self.assertIn("../roblox-final/private/case-studies/doors.md", new)
            self.assertIn("../roblox-final/vault/INDEX.md", new)
            self.assertIn(".claude/skills/roblox-map/references/performance-and-devices.md", new)
            self.assertIn("vault/fundamentals/metadata-thumbnails-icons.md", new)
            self.assertNotIn("vault/fundamentals/quality-bar.md", new)
            # ambiguous things are reported, not touched
            self.assertIn("(goals.md)", new)
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
        allowed = {"docs/migration.md", "tools/migrate_game.py", "tests/test_migration.py", "tests/test_public_tree.py",
                   "CHANGELOG.md", "docs/decisions.md", "docs/vault-readers.md", "docs/redundancy-map.md", ".gitignore"}
        olds = [old for old, _ in migrate_game.MOVES if old.startswith("vault/fundamentals/")]
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

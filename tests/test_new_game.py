"""One new_game.py makes a complete game; the starter points at skill rules and explains its gaps.

Defects this exists for:
- There were two new_game.py. create-roblox-game's made a game with no CLAUDE.md, docs,
  session hook or layout map; the toolkit's depended on it. A game got half its setup.
- The game's CLAUDE.md loaded the whole research index and kept status ("Current milestone")
  that went stale; status belongs in HANDOFF.md.
- Starter docs restated the roblox-code rules and left `<...>` placeholders nobody was told to
  fill.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW_GAME = ROOT / "tools" / "new_game.py"
ALIAS = ROOT / ".claude" / "skills" / "create-roblox-game" / "scripts" / "new_game.py"
PROMISED = ["CLAUDE.md", "HANDOFF.md", ".claude/settings.json", ".mcp.json", ".gitignore",
            "design/game.json", "design/layout.json", "design/map.json", "BUILD.md",
            "docs/design/maps/_template.state.md", "docs/tech/architecture.md",
            "docs/tech/conventions.md", "default.project.json", "src/shared/Net.luau",
            "tests/Health.spec.luau", "lune/test.luau"]

sys.path.insert(0, str(ROOT / "tools"))
import smoke  # noqa: E402  the placeholder rule is smoke.py's, used here on its own


def make(script: Path, tmp: str, title: str = "Small Hours") -> tuple[subprocess.CompletedProcess, Path]:
    game = Path(tmp) / "game"
    p = subprocess.run([sys.executable, str(script), title, "--dir", str(game)], capture_output=True, text=True)
    return p, game


class NewGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.proc, cls.game = make(NEW_GAME, cls.tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_one_command_makes_every_part(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)
        missing = [p for p in PROMISED if not (self.game / p).exists()]
        self.assertEqual(missing, [])

    def test_the_old_command_makes_the_same_game(self):
        with tempfile.TemporaryDirectory() as tmp:
            p, game = make(ALIAS, tmp)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertEqual([x for x in PROMISED if not (game / x).exists()], [])

    def test_layout_map_is_the_scaffold_layout(self):
        lay = json.loads((self.game / "design" / "layout.json").read_text(encoding="utf-8"))
        self.assertEqual(lay["remotes"], {"style": "net-module", "where": "src/shared/Net.luau"})
        self.assertEqual(lay["pure"], ["src/shared/Core"])
        for rel in [lay["config"], lay["services"], lay["controllers"], lay["tests"], *lay["boot"].values()]:
            self.assertTrue((self.game / rel).exists(), rel)

    def test_settings_carry_the_stop_hook(self):
        s = json.loads((self.game / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertIn("../roblox-final", s["permissions"]["additionalDirectories"])
        cmd = s["hooks"]["Stop"][0]["hooks"][0]["command"]
        self.assertIn("create-roblox-game/scripts/session.py stop", cmd)

    def test_claude_md_is_a_task_list_and_status_lives_in_handoff(self):
        text = (self.game / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("# Small Hours", text)
        self.assertIn("Status lives in HANDOFF.md", text)
        self.assertIn("## Task -> file", text)
        self.assertNotIn("Current milestone", text)
        self.assertNotIn("read INDEX first", text)

    def test_no_placeholder_is_left_unexplained(self):
        self.assertEqual(smoke.placeholders(self.game), [])

    def test_starter_points_at_rules_instead_of_restating_them(self):
        arch = (self.game / "docs" / "tech" / "architecture.md").read_text(encoding="utf-8")
        self.assertIn("design/layout.json", arch)
        self.assertIn("references/layout.md", arch)
        self.assertNotIn("Every value from a client is a request", arch)
        self.assertNotIn("src/shared/Net.luau     the ONLY gameplay transport", arch)

    def test_handoff_starts_filled(self):
        text = (self.game / "HANDOFF.md").read_text(encoding="utf-8")
        self.assertFalse(re.search(r"^TODO", text, re.M))
        self.assertIn("Small Hours", text)
        self.assertNotIn("<made on>", text)

    def test_session_state_is_gitignored(self):
        self.assertIn(".claude/session/", (self.game / ".gitignore").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

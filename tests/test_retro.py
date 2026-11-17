"""The lessons loop closes: session.py writes the inbox, /toolkit-retro empties it with backed edits.

Defects this exists for:
- Lessons were written down and nothing happened to them, or a lesson was "addressed" by an
  edit nobody could find later. Each lesson now leaves the inbox only with the edit and the
  test that answer it, or a stated reason it is the game's own debt.
- The retro must run only when the user asks: a model invoking it mid-build would edit the
  toolkit during a game.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INBOX_PY = ROOT / ".claude" / "skills" / "toolkit-retro" / "scripts" / "inbox.py"
SKILL = ROOT / ".claude" / "skills" / "toolkit-retro" / "SKILL.md"
SESSION = ROOT / ".claude" / "skills" / "create-roblox-game" / "scripts" / "session.py"


class Retro(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.private = Path(self.tmp.name) / "private"
        self.env = {**os.environ, "ROBLOX_FINAL_PRIVATE": str(self.private)}
        self.env.pop("CLAUDE_PROJECT_DIR", None)
        game = Path(self.tmp.name) / "game"
        (game / "design").mkdir(parents=True)
        (game / "design" / "game.json").write_text("{}", encoding="utf-8")
        (game / "HANDOFF.md").write_text("# H\n\n## Debts\n- The coin mesh is a placeholder.\n", encoding="utf-8")
        self.run_py(SESSION, "log", "--gate", "roblox-code check.py", "--note", "failed: selene", "--dir", str(game))
        self.run_py(SESSION, "mark", "build", "--what", "coins", "--at", "0", "--dir", str(game))
        self.run_py(SESSION, "stop", "--dir", str(game))  # the handoff is newer than at=0: consumed

    def tearDown(self):
        self.tmp.cleanup()

    def run_py(self, script, *args) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True,
                              env=self.env, input="{}")

    def ids(self) -> list[str]:
        return re.findall(r"^\s+(L[0-9a-f]{8})\s", self.run_py(INBOX_PY, "list").stdout, re.M)

    def test_session_lessons_are_listed_with_ids(self):
        out = self.run_py(INBOX_PY, "list").stdout
        self.assertIn("gate failure: roblox-code check.py: failed: selene", out)
        self.assertIn("handoff debt: The coin mesh is a placeholder.", out)
        self.assertEqual(len(self.ids()), 2)

    def test_done_needs_an_edit_and_a_test_that_exist(self):
        first = self.ids()[0]
        p = self.run_py(INBOX_PY, "done", first, "--owner", "roblox-code", "--edit", "no/such.py",
                        "--test", "tests/test_code_check.py")
        self.assertNotEqual(p.returncode, 0)
        p = self.run_py(INBOX_PY, "done", first, "--owner", "roblox-code",
                        "--edit", ".claude/skills/roblox-code/scripts/check.py", "--test", "tests/test_code_check.py")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertNotIn(first, self.ids())
        done = (self.private / "lessons-done.md").read_text(encoding="utf-8")
        self.assertIn("- edit: .claude/skills/roblox-code/scripts/check.py", done)
        self.assertEqual(self.run_py(INBOX_PY, "check").returncode, 0)

    def test_skip_needs_a_reason_and_empties_the_inbox(self):
        for lid in self.ids():
            self.assertNotEqual(self.run_py(INBOX_PY, "skip", lid, "--reason", "game debt").returncode, 0)
            p = self.run_py(INBOX_PY, "skip", lid, "--reason", "the game's own backlog, no toolkit gap")
            self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(self.ids(), [])
        self.assertNotIn("## ", (self.private / "lessons-inbox.md").read_text(encoding="utf-8").split("\n", 3)[-1])

    def test_check_fails_when_a_recorded_edit_is_gone(self):
        self.private.mkdir(exist_ok=True)
        (self.private / "lessons-done.md").write_text(
            "# Lessons done\n\n## L00000000 (2026-11-17)\n\n- lesson: x\n- owner: y\n"
            "- edit: tools/gone.py\n- test: tests/test_gone.py\n", encoding="utf-8")
        p = self.run_py(INBOX_PY, "check")
        self.assertEqual(p.returncode, 1)
        self.assertIn("tools/gone.py no longer exists", p.stdout)

    def test_the_skill_runs_only_when_asked(self):
        head = SKILL.read_text(encoding="utf-8").split("---", 2)[1]
        self.assertIn("disable-model-invocation: true", head)
        body = SKILL.read_text(encoding="utf-8")
        for part in ("## Rules", "## Steps", "## Gate", "## References", "## Traps"):
            self.assertIn(part, body)


if __name__ == "__main__":
    unittest.main()

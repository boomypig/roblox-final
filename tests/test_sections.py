"""create-roblox-game: resume is read-only, and scaffold markers match on the start only.

Defects this exists for:
1. `section.py resume` wrote an implied approval into design/sections.json. Asking where a game
   stands signed off a section. Now resume writes nothing and prints `approve N --implied`,
   which writes the same record (gate change 1).
2. validate.py rejected any string containing "TODO", so a game titled "TODO List Tycoon"
   could never pass section 1; `section.py close` did the same for any HANDOFF line mentioning
   "TODO:". Every scaffold marker starts with TODO, so only the start is matched, and the
   report shows the first 40 characters of the value.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude" / "skills" / "create-roblox-game" / "scripts"
SECTION = SCRIPTS / "section.py"
sys.path.insert(0, str(SCRIPTS))
import new_game  # noqa: E402
import validate  # noqa: E402


class ResumeIsReadOnly(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.game = Path(self.tmp.name) / "tycoon"
        (self.game / "design").mkdir(parents=True)
        (self.game / "design" / "game.json").write_text(json.dumps({"title": "Tycoon"}), encoding="utf-8")
        self.state = self.game / "design" / "sections.json"
        self.state.write_text(json.dumps({"ledger": None, "closed": {"1": "2026-11-17T10:00:00+00:00"}}, indent=2) + "\n",
                              encoding="utf-8")
        self.env = {**os.environ, "ROBLOX_GAMES_HOME": self.tmp.name}

    def tearDown(self):
        self.tmp.cleanup()

    def section(self, *args):
        return subprocess.run([sys.executable, str(SECTION), *args], capture_output=True, text=True, env=self.env)

    def test_resume_writes_nothing(self):
        before = self.state.read_bytes()
        r = self.section("resume", "--dir", str(self.game))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.state.read_bytes(), before, "resume changed design/sections.json")

    def test_resume_prints_the_command_that_records_the_approval(self):
        r = self.section("resume", "--dir", str(self.game))
        self.assertIn("approve 1 --implied", r.stdout)

    def test_approve_implied_writes_the_record_resume_used_to_write(self):
        r = self.section("approve", "1", "--implied", "--dir", str(self.game))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        approved = json.loads(self.state.read_text(encoding="utf-8"))["approved"]["1"]
        self.assertTrue(approved.endswith(" (implied by continuing)"), approved)

    def test_plain_approve_is_unchanged(self):
        self.section("approve", "1", "--dir", str(self.game))
        approved = json.loads(self.state.read_text(encoding="utf-8"))["approved"]["1"]
        self.assertNotIn("implied", approved)

    def test_no_prompt_once_approved(self):
        self.section("approve", "1", "--dir", str(self.game))
        r = self.section("resume", "--dir", str(self.game))
        self.assertNotIn("--implied", r.stdout)

    def test_skill_doc_matches(self):
        text = (SCRIPTS.parent / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("a `resume` after an unapproved\nclose records the approval", text)
        self.assertIn("approve N --implied", text)


class Markers(unittest.TestCase):
    def test_every_scaffold_marker_is_still_caught(self):
        # game.json and every stage stub new_game.py writes
        total = 0
        for name, data in [("game.json", new_game.GAME), *new_game.STUBS.items()]:
            hits = validate.find_todos(data, name)
            expected = json.dumps(data).count('"TODO')  # every marker is a string starting TODO
            self.assertEqual(len(hits), expected, f"{name}: " + "\n".join(hits))
            total += expected
        self.assertGreater(total, 15)

    def test_a_real_value_that_contains_or_starts_with_the_word_passes(self):
        data = {"title": "TODO List Tycoon", "pitch": "Check off a giant TODO list before night falls",
                "systems": [{"name": "TodoService", "owns": "the TODO board"}]}
        self.assertEqual(validate.find_todos(data, "game.json"), [])

    def test_report_shows_the_first_40_characters(self):
        hits = validate.find_todos({"pitch": "TODO: one sentence. What the player does, and what is at stake."}, "game.json")
        self.assertEqual(len(hits), 1)
        self.assertIn("'TODO: one sentence. What the player does...'", hits[0])  # 40 characters, then ...

    def test_marker_keys_are_caught(self):
        hits = validate.find_todos({"config": {"TODOTunable": 0}}, "game.json")
        self.assertEqual(len(hits), 1)
        self.assertIn("(key)", hits[0])

    def test_handoff_lines_match_on_the_start_only(self):
        import section
        text = "## Done this section\nFixed the TODO: label in the TODO List Tycoon shop.\n" \
               "TODO: what was built and what verified it (a gate, a measured number).\n"
        todos = section.handoff_todos(text)
        self.assertEqual(todos, ["'TODO: what was built and what verified i...'"])  # 40 characters


if __name__ == "__main__":
    unittest.main()

"""session.py: the Stop hook acts only at a session boundary, and keeps lessons.

Defects this exists for:
- A map pass or a /build ended with no handoff, and the next session started cold: it re-toured
  Studio and re-derived decisions. Nothing refused to end the session without one.
- Lessons from failures (gate failures, stalls, fallbacks, debts) lived only in the transcript
  of the session that hit them.
The hook must never interrupt inside a section, must let a stuck session go after a few tries,
and must be cheap.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude" / "skills" / "create-roblox-game" / "scripts"
SESSION = SCRIPTS / "session.py"
SECTION = SCRIPTS / "section.py"

STATE_ROW = """# Map state: harbor

## Pass log

| Date | Zone | Pass | Built (paths) | Checks (RESULT, failures) | Judgment calls | Left for the user |
|---|---|---|---|---|---|---|
| 2026-11-17 | pier | greybox | Workspace.Harbor.Layout | RESULT: PASS | none | none |

## Run in progress

{running}
"""


class Session(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.game = base / "game"
        (self.game / "design").mkdir(parents=True)
        (self.game / "design" / "game.json").write_text('{"title": "T"}', encoding="utf-8")
        self.private = base / "private"
        self.env = {**os.environ, "ROBLOX_FINAL_PRIVATE": str(self.private)}
        self.env.pop("CLAUDE_PROJECT_DIR", None)
        hf = self.game / "HANDOFF.md"
        hf.write_text("<!-- handoff: start -->\n# HANDOFF\n\n## Debts\n- None.\n", encoding="utf-8")
        old = time.time() - 60
        os.utime(hf, (old, old))

    def tearDown(self):
        self.tmp.cleanup()

    def py(self, script: Path, *args: str, stdin: str = "{}") -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(script), *args], input=stdin, capture_output=True,
                              text=True, env=self.env)

    def stop(self) -> str:
        p = self.py(SESSION, "stop", "--dir", str(self.game))
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout.strip()

    def fill_handoff(self, debts: str = "- None."):
        self.py(SECTION, "handoff", "--light", "build", "--what", "coins", "--dir", str(self.game))
        hf = self.game / "HANDOFF.md"
        text = hf.read_text(encoding="utf-8").replace(
            "TODO: fallbacks, judgment calls the user should review, and failures left open, or 'None'.", debts)
        hf.write_text("\n".join("Filled." if ln.startswith("TODO") else ln for ln in text.splitlines()) + "\n",
                      encoding="utf-8")

    def test_no_boundary_is_silent(self):
        self.assertEqual(self.stop(), "")

    def test_not_a_game_is_silent(self):
        p = self.py(SESSION, "stop", "--dir", self.tmp.name)
        self.assertEqual((p.returncode, p.stdout), (0, ""))

    def test_build_boundary_blocks_until_the_handoff_is_filled(self):
        self.py(SESSION, "mark", "build", "--what", "coins", "--dir", str(self.game))
        out = json.loads(self.stop())
        self.assertEqual(out["decision"], "block")
        self.assertIn("handoff --light build", out["reason"])
        self.py(SECTION, "handoff", "--light", "build", "--what", "coins", "--dir", str(self.game))
        self.assertIn("fill the remaining TODO lines", json.loads(self.stop())["reason"])
        self.fill_handoff()
        self.assertEqual(self.stop(), "")
        self.assertEqual(self.stop(), "", "a consumed boundary does not block again")

    def test_inside_a_section_only_the_section_boundary_counts(self):
        (self.game / "design" / "sections.json").write_text('{"ledger": null, "closed": {"1": "x"}}',
                                                             encoding="utf-8")
        self.py(SESSION, "mark", "build", "--what", "coins", "--dir", str(self.game))
        self.assertEqual(self.stop(), "", "a /build inside a section must not interrupt it")

    def test_a_finished_map_pass_is_a_boundary(self):
        maps = self.game / "docs" / "design" / "maps"
        maps.mkdir(parents=True)
        state = maps / "harbor.state.md"
        state.write_text(STATE_ROW.format(running="- pier deck: Workspace.Harbor.Layout.Deck RESULT: PASS"),
                         encoding="utf-8")
        self.assertEqual(self.stop(), "", "a run still in progress is not a boundary")
        state.write_text(STATE_ROW.format(running="- (none)"), encoding="utf-8")
        out = json.loads(self.stop())
        self.assertIn("handoff --light map", out["reason"])
        self.assertIn("harbor", out["reason"])

    def test_after_max_blocks_it_lets_go_and_records_a_debt(self):
        self.py(SESSION, "mark", "build", "--what", "coins", "--dir", str(self.game))
        for _ in range(3):
            self.assertIn("block", self.stop())
        self.assertEqual(self.stop(), "")
        inbox = (self.private / "lessons-inbox.md").read_text(encoding="utf-8")
        self.assertIn("handoff debt: the session stopped after a build boundary", inbox)

    def test_lessons_collect_gate_failures_ledger_events_and_debts(self):
        runs = self.game / "build-runs" / "r"
        runs.mkdir(parents=True)
        (runs / "meta.json").write_text("{}", encoding="utf-8")
        now = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
        (runs / "events.jsonl").write_text(
            json.dumps({"kind": "fallback", "stage": "animation", "note": "Tier 1 clip", "ts": now}) + "\n" +
            json.dumps({"kind": "end", "stage": "sfx", "status": "failed", "ts": now}) + "\n", encoding="utf-8")
        (self.game / "design" / "sections.json").write_text(json.dumps({"ledger": str(runs), "closed": {}}),
                                                             encoding="utf-8")
        self.py(SESSION, "log", "--gate", "roblox-code check.py", "--note", "failed: selene", "--dir", str(self.game))
        self.py(SESSION, "mark", "section", "--what", "4", "--dir", str(self.game))
        self.fill_handoff(debts="- The UI icons are placeholders.")
        self.assertEqual(self.stop(), "")
        inbox = (self.private / "lessons-inbox.md").read_text(encoding="utf-8")
        for line in ("gate failure: roblox-code check.py: failed: selene", "fallback (animation): Tier 1 clip",
                     "stage sfx ended failed", "handoff debt: The UI icons are placeholders."):
            self.assertIn(line, inbox)

    def test_section_close_marks_the_boundary_and_a_failed_close_is_logged(self):
        p = self.py(SECTION, "close", "1", "--dir", str(self.game))
        self.assertEqual(p.returncode, 1)
        log = (self.game / ".claude" / "session" / "log.jsonl").read_text(encoding="utf-8")
        self.assertIn("section.py close 1", log)
        src = SECTION.read_text(encoding="utf-8")
        self.assertIn('session.mark(root, "section", str(n), at=hf.stat().st_mtime)', src)

    def test_the_hook_is_fast(self):
        self.py(SESSION, "mark", "build", "--what", "coins", "--dir", str(self.game))
        times = []
        for _ in range(5):
            t = time.perf_counter()
            self.stop()
            times.append((time.perf_counter() - t) * 1000)
        times.sort()
        self.assertLess(times[2], 100, f"median {times[2]:.0f} ms")


if __name__ == "__main__":
    unittest.main()

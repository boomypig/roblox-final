"""adopt.py takes on an existing game as it is; the gates read its layout; section 1 accepts it.

Defects this exists for:
- The toolkit assumed every game came from its scaffold. A real game made before it (plain
  modules booted from Main.server.luau, remotes created by each service under
  ReplicatedStorage.Remotes, one Config.luau, pure modules loose in src/shared, no Wally,
  rokit.toml, no tests, a map built by hand in Studio) had no layout map, so check.py and the
  reviewer judged it against folders it did not have.
- Section 1 could never close for such a game: its research and design were done before the
  toolkit, so the ledger stages could not be bracketed (gate change 2 accepts `adopted`).
- Adoption must never reformat or move the game's code.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / ".claude" / "skills"
ADOPT = SK / "create-roblox-game" / "scripts" / "adopt.py"
SECTION = SK / "create-roblox-game" / "scripts" / "section.py"
RUN_LOG = SK / "roblox-build-orchestrator" / "scripts" / "run_log.py"
CHECK = SK / "roblox-code" / "scripts" / "check.py"
FIXTURE = ROOT / "tests" / "fixtures" / "adopted-game"
TOOL_OK = "#!/bin/sh\necho \"$0 $@\" >> \"$(dirname \"$0\")/calls.log\"\nexit 0\n"


def tree_hash(d: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(d.rglob("*")):
        if p.is_file():
            h.update(p.relative_to(d).as_posix().encode() + p.read_bytes())
    return h.hexdigest()


class Adopt(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.game = Path(self.tmp.name) / "harbor-rush"
        shutil.copytree(FIXTURE, self.game)

    def tearDown(self):
        self.tmp.cleanup()

    def py(self, *args, env=None) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True,
                              env=env or os.environ)

    def adopt_write(self):
        p = self.py(ADOPT, "--dir", self.game, "--write")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        return json.loads((self.game / "design" / "layout.json").read_text(encoding="utf-8"))

    def test_read_only_by_default(self):
        before = tree_hash(self.game)
        p = self.py(ADOPT, "--dir", self.game)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("read-only: nothing was written", p.stdout)
        self.assertEqual(tree_hash(self.game), before)

    def test_layout_matches_the_adopted_shape(self):
        lay = self.adopt_write()
        self.assertEqual(lay["framework"], "modules")
        self.assertEqual(lay["boot"]["server"], "src/server/Main.server.luau")
        self.assertEqual(lay["remotes"], {"style": "per-service", "where": "ReplicatedStorage.Remotes"})
        self.assertEqual(lay["config"], "src/shared/Config.luau")
        self.assertEqual(lay["pure"], ["src/shared/RoundTimer.luau", "src/shared/Scoring.luau"])
        self.assertIsNone(lay["tests"])
        self.assertEqual((lay["packages"], lay["toolchain"]), ("none", "rokit.toml"))
        self.assertEqual(lay["map"], {"source": "studio", "brief": "docs/design/maps/harbor.md"})
        self.assertTrue(lay["adopted"])

    def test_code_is_never_touched_and_existing_files_never_overwritten(self):
        src, pitch = tree_hash(self.game / "src"), (self.game / "docs" / "pitch.md").read_text(encoding="utf-8")
        self.adopt_write()
        self.assertEqual(tree_hash(self.game / "src"), src)
        self.assertEqual((self.game / "docs" / "pitch.md").read_text(encoding="utf-8"), pitch)
        self.assertFalse((self.game / "tests").exists())

    def test_contract_skeleton_comes_from_the_docs(self):
        self.adopt_write()
        game = json.loads((self.game / "design" / "game.json").read_text(encoding="utf-8"))
        self.assertEqual(game["title"], "Harbor Rush")
        self.assertTrue(game["pitch"].startswith("Race around a busy harbor"))
        self.assertEqual(len(game["core_loop"]), 3)
        self.assertEqual(game["out_of_scope"], ["trading", "pets", "a second map"])
        self.assertEqual(game["config"]["RoundSeconds"], 120)
        owns = {s["name"]: s["owns"] for s in game["systems"]}
        self.assertTrue(owns["RoundService"].startswith("the round state"))
        self.assertTrue(owns["HudController"].startswith("TODO"), "no 'owns' comment: left for section 1")

    def test_adoption_gives_the_starter_and_hook(self):
        self.adopt_write()
        for rel in ("CLAUDE.md", "HANDOFF.md", ".claude/settings.json", "docs/tech/layout.md",
                    "docs/design/maps/_template.state.md"):
            self.assertTrue((self.game / rel).exists(), rel)
        self.assertIn("# Harbor Rush", (self.game / "CLAUDE.md").read_text(encoding="utf-8"))

    @unittest.skipIf(os.name == "nt", "stand-in tools are shell scripts")
    def test_check_reads_the_layout(self):
        self.adopt_write()
        b = Path(self.tmp.name) / "bin"
        b.mkdir()
        for name in ("rojo", "lune", "selene", "stylua"):
            (b / name).write_text(TOOL_OK, encoding="utf-8")
            (b / name).chmod(0o755)
        (self.game / "tests").mkdir()
        (self.game / "tests" / "Old.spec.luau").write_text("return {}", encoding="utf-8")
        env = {**os.environ, "PATH": f"{b}{os.pathsep}/usr/bin{os.pathsep}/bin"}
        p = self.py(CHECK, "--dir", self.game, env=env)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("layout.json says this game has no tests yet", p.stdout)
        calls = (b / "calls.log").read_text(encoding="utf-8")
        self.assertNotIn("lune", calls)
        self.assertRegex(calls, r"stylua --check src\n")

    def test_section_1_accepts_adopted_ledger_stages_and_later_sections_do_not(self):
        self.adopt_write()
        runs = self.game / "build-runs"
        self.py(RUN_LOG, "init", "--dir", runs, "--run", "harbor")
        for stage in ("market-research", "design-spec", "code"):
            p = self.py(RUN_LOG, "end", "--dir", runs, "--run", "harbor", "--stage", stage, "--status", "adopted")
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        sys.path.insert(0, str(SECTION.parent))
        import section
        ends = section.ledger_ends(runs / "harbor")
        self.assertEqual(ends["market-research"], "adopted")
        p = self.py(SECTION, "handoff", "1", "--dir", self.game, "--ledger", runs / "harbor")
        self.assertEqual(p.returncode, 0, p.stderr)
        p = self.py(SECTION, "close", "1", "--dir", self.game)
        self.assertNotIn("ledger stage", p.stdout, "section 1 must accept adopted stages")
        self.assertIn("validate.py is not green", p.stdout, "validate.py must still be required")
        state = {"ledger": str(runs / "harbor"), "closed": {"1": "x"}}
        (self.game / "design" / "sections.json").write_text(json.dumps(state), encoding="utf-8")
        p = self.py(SECTION, "close", "2", "--dir", self.game)
        self.assertIn("only section 1 accepts --status adopted", p.stdout)


if __name__ == "__main__":
    unittest.main()

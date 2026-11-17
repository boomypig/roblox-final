"""roblox-code's check.py: the two defects it was fixed for.

1. It refused any project without Packages/, even one with no wally.toml (a game that uses no
   Wally packages). Packages/ is required only when wally.toml exists.
2. A rokit shim for a tool the game has not pinned prints "Failed to find tool ... in any
   project manifest file" and exits 0, so the gate passed with the tool never run. It must be
   a FAIL that names the tool to add to rokit.toml.

The tools are stand-in scripts on PATH, so the test runs anywhere (CI has no rokit).

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / ".claude" / "skills" / "roblox-code" / "scripts" / "check.py"
PROJECT = '{"name": "Fixture", "tree": {"$className": "DataModel"}}'
SHIM_UNPINNED = """#!/bin/sh
echo "ERROR Failed to find tool '{name}' in any project manifest file."
echo "Add the tool to a project using 'rokit add' before running it."
exit 0
"""
TOOL_OK = """#!/bin/sh
echo "{name} ok"
exit 0
"""


@unittest.skipIf(os.name == "nt", "stand-in tools are shell scripts")
class CodeCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.game = base / "game"
        (self.game / "src").mkdir(parents=True)
        (self.game / "default.project.json").write_text(PROJECT, encoding="utf-8")
        self.bin = base / "bin"
        self.bin.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def tool(self, name: str, body: str):
        p = self.bin / name
        p.write_text(body.replace("{name}", name), encoding="utf-8")
        p.chmod(p.stat().st_mode | stat.S_IEXEC)

    def check(self) -> subprocess.CompletedProcess:
        env = {**os.environ, "PATH": f"{self.bin}{os.pathsep}/usr/bin{os.pathsep}/bin"}
        return subprocess.run([sys.executable, str(CHECK), "--dir", str(self.game)],
                              capture_output=True, text=True, env=env)

    def test_no_wally_toml_needs_no_packages(self):
        for name in ("rojo", "selene", "stylua"):
            self.tool(name, TOOL_OK)
        r = self.check()
        self.assertNotIn("Packages/ is missing", r.stdout)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("all gates green", r.stdout)

    def test_wally_toml_without_packages_still_fails(self):
        (self.game / "wally.toml").write_text('[package]\nname = "x/y"\n', encoding="utf-8")
        for name in ("rojo", "selene", "stylua"):
            self.tool(name, TOOL_OK)
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("Packages/ is missing", r.stdout)
        self.assertIn("wally install", r.stdout)

    def test_unpinned_shim_fails_and_names_the_tool(self):
        (self.game / "rokit.toml").write_text('[tools]\nrojo = "rojo-rbx/rojo@7.4.4"\n', encoding="utf-8")
        self.tool("rojo", TOOL_OK)
        self.tool("selene", SHIM_UNPINNED)
        self.tool("stylua", TOOL_OK)
        r = self.check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("FAIL", r.stdout)
        self.assertIn("Add selene to rokit.toml", r.stdout)
        self.assertIn("rokit add Kampfkarren/selene", r.stdout)

    def test_unpinned_rojo_stops_the_build_with_the_name(self):
        self.tool("rojo", SHIM_UNPINNED)
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("Add rojo to rokit.toml", r.stdout)

    def test_aftman_only_project_is_told_aftman_toml(self):
        (self.game / "aftman.toml").write_text("[tools]\n", encoding="utf-8")
        self.tool("rojo", TOOL_OK)
        self.tool("selene", TOOL_OK)
        self.tool("stylua", SHIM_UNPINNED)
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("Add stylua to aftman.toml", r.stdout)


if __name__ == "__main__":
    unittest.main()

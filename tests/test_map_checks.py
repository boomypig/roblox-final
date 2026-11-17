"""The map-builder's Luau checks and the map state file.

Defect this exists for: the map-builder judged a pass from screenshots and prose, so default
grey Plastic, decoration players walk into, hiding spots an avatar does not fit, lanes narrower
than a player and floor with no refuge in reach were found only in playtests. map_checks.lua
measures them in Studio; these tests keep it runnable where no Studio is connected: one
grey rule shared with verify_build.lua, never a yield, failures capped at 30, every check
parameterised, and the source compiling under Luau when Lune is installed.

What these tests cannot prove is the numbers on a real place: that needs Studio (listed as
unverified until a run against a connected Studio).

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / ".claude" / "skills" / "roblox-map"
LUA = MAP / "scripts" / "luau" / "map_checks.lua"
VERIFY_BUILD = MAP / "scripts" / "luau" / "verify_build.lua"
EMIT = MAP / "scripts" / "map_checks.py"
TEMPLATE = MAP / "references" / "map-state.template.md"
sys.path.insert(0, str(MAP / "scripts"))
import map_checks  # noqa: E402


def code_only(lua: str) -> str:
    return "\n".join(ln.split("--", 1)[0] for ln in lua.splitlines())


def lune() -> str | None:
    """A Lune binary that really runs (a rokit shim with no pin prints an error and exits 0)."""
    candidates = [os.environ.get("LUNE_BIN"), shutil.which("lune")]
    candidates += sorted(glob.glob(str(Path.home() / ".rokit/tool-storage/lune-org/lune/*/lune")))
    for c in filter(None, candidates):
        r = subprocess.run([c, "--version"], capture_output=True, text=True)
        if r.returncode == 0 and "Failed to find tool" not in r.stdout + r.stderr:
            return c
    return None


class Source(unittest.TestCase):
    lua = LUA.read_text(encoding="utf-8")

    def test_default_grey_is_the_one_verify_build_uses(self):
        rule = re.compile(r"Color3\.fromRGB\((\d+),\s*(\d+),\s*(\d+)\)")
        mine = re.search(r"DEFAULT_GREY = " + rule.pattern, self.lua)
        theirs = re.search(r"DEFAULT = " + rule.pattern, VERIFY_BUILD.read_text(encoding="utf-8"))
        self.assertIsNotNone(mine)
        self.assertIsNotNone(theirs)
        self.assertEqual(mine.groups(), theirs.groups())
        self.assertIn("visible(p) and p.Color == DEFAULT_GREY", self.lua)
        self.assertIn("return p.Transparency < 1", self.lua)  # the same invisible-marker exemption

    def test_never_yields(self):
        code = code_only(self.lua)
        for call in ("task.wait", "wait(", "task.delay", "task.defer", "task.spawn", ":Wait("):
            self.assertNotIn(call, code)

    def test_failures_are_one_line_each_and_capped_at_30(self):
        self.assertRegex(self.lua, r"failLines = 30")
        self.assertIn("if #failLines < (PARAMS.failLines or 30)", self.lua)
        self.assertIn("more failures", self.lua)

    def test_every_requested_check_is_there(self):
        for check in ("inventory", "properties", "lanes", "refuge", "hiding"):
            self.assertRegex(self.lua, rf"if PARAMS\.checks\.{check}")
        self.assertIn("workspace:Raycast", self.lua)  # hiding sizes and lane widths are measured by raycast
        self.assertIn("Enum.Material.Plastic", self.lua)
        self.assertIn("PARAMS.surfaceAttribute", self.lua)
        self.assertIn("PARAMS.collideAttribute", self.lua)

    def test_template_params_equal_the_lua_defaults(self):
        block = map_checks.params_from_state(TEMPLATE.read_text(encoding="utf-8"))
        current = map_checks.split(self.lua)[1]
        self.assertEqual(block, current)

    @unittest.skipIf(lune() is None, "Lune is not installed (CI has none)")
    def test_compiles_as_luau(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "checks.lua"
            src.write_text(map_checks.emit(None), encoding="utf-8")
            runner = Path(d) / "compile.luau"
            runner.write_text(
                'local luau = require("@lune/luau")\nlocal fs = require("@lune/fs")\n'
                f'local ok, err = pcall(luau.compile, fs.readFile("{src.as_posix()}"))\n'
                'print(if ok then "COMPILES" else "SYNTAX ERROR " .. tostring(err))\n', encoding="utf-8")
            r = subprocess.run([lune(), "run", str(runner)], capture_output=True, text=True)
            self.assertIn("COMPILES", r.stdout, r.stdout + r.stderr)


class Emitter(unittest.TestCase):
    def state(self, params: str) -> str:
        return TEMPLATE.read_text(encoding="utf-8").replace(
            map_checks.params_from_state(TEMPLATE.read_text(encoding="utf-8")), params)

    def test_state_params_are_spliced_in(self):
        params = 'local PARAMS = {\n\tmap = "Harbor",\n\tchecks = { inventory = true, properties = true, lanes = true, refuge = true, hiding = true },\n\tlane = { minWidth = 8, height = 3 },\n}'
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "harbor.state.md"
            p.write_text(self.state(params), encoding="utf-8")
            r = subprocess.run([sys.executable, str(EMIT), "--state", str(p)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('map = "Harbor"', r.stdout)
        self.assertIn("minWidth = 8", r.stdout)
        self.assertEqual(r.stdout.count("local PARAMS ="), 1)
        self.assertIn("RESULT:", r.stdout)

    def test_only_narrows_the_checks(self):
        r = subprocess.run([sys.executable, str(EMIT), "--only", "inventory"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("checks = { inventory = true, properties = false, lanes = false, refuge = false, hiding = false }", r.stdout)

    def test_bad_params_are_refused(self):
        with self.assertRaises(SystemExit):
            map_checks.params_from_state("## Check parameters\n\n```lua\nPARAMS = 1\n```\n")
        with self.assertRaises(SystemExit):
            map_checks.params_from_state("no section here")
        with self.assertRaises(SystemExit):
            map_checks.only("local PARAMS = { checks = { inventory = true } }", ["nonsense"])


class StateFile(unittest.TestCase):
    text = TEMPLATE.read_text(encoding="utf-8")

    def test_has_every_section_the_agent_reads_and_writes(self):
        for heading in ("## Folders and counts", "## Check parameters", "## Pass log", "## Run in progress"):
            self.assertIn(heading, self.text)

    def test_the_agent_may_write_only_this_file(self):
        agent = (ROOT / ".claude" / "agents" / "map-builder.md").read_text(encoding="utf-8")
        tools = re.search(r"^tools:\s*(.*)$", agent, re.M).group(1)
        self.assertIn("Write", tools)
        self.assertIn("Edit", tools)
        self.assertRegex(agent, r"Write and Edit are for .*\.state\.md.* only")
        self.assertIn("map_checks.lua", agent)
        self.assertIn("builder-card.md", agent)


if __name__ == "__main__":
    unittest.main()

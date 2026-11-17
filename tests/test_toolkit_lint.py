"""tools/toolkit_lint.py catches each kind of decay it names, and fails only on new findings.

Defect this exists for: the toolkit decayed between sessions in five ways nothing checked:
a rule copied into a second file and then drifting, a path or line reference to something
that moved, an agent card older than its sources, a script no test runs, and a private path
or name in a tracked file.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("toolkit_lint", ROOT / "tools" / "toolkit_lint.py")
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)

RULE = "Every tunable a designer might change lives in the config module and never inline in a service."


class ToolkitLint(unittest.TestCase):
    def test_the_repo_has_no_new_findings(self):
        p = subprocess.run([sys.executable, str(ROOT / "tools" / "toolkit_lint.py")], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-2000:])

    def test_a_rule_in_two_files_is_found(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "vault") as tmp:
            a, b = Path(tmp) / "a.md", Path(tmp) / "b.md"
            a.write_text(f"# A\n\n{RULE}\n", encoding="utf-8")
            b.write_text(f"# B\n\nSome text first. {RULE}\n", encoding="utf-8")
            found = lint.check_dup([a, b])
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0][0], "dup")

    def test_a_dead_path_and_a_line_past_the_end_are_found(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "vault") as tmp:
            doc = Path(tmp) / "doc.md"
            doc.write_text("See `tools/no_such_tool.py` and `tools/new_game.py`, and tools/new_game.py:99999.\n",
                           encoding="utf-8")
            found = lint.check_path([doc])
        details = [f[2] for f in found]
        self.assertTrue(any("tools/no_such_tool.py" in d for d in details), details)
        self.assertTrue(any("past the end" in d for d in details), details)
        self.assertFalse(any("names tools/new_game.py" in d for d in details), details)

    def test_an_untested_script_is_found_and_a_run_one_is_not(self):
        lonely, runner = ROOT / "tools" / "_lint_probe_lonely.py", ROOT / "tools" / "_lint_probe_runner.py"
        fake_test = ROOT / "tests" / "_lint_probe_test.py"
        texts = {lonely: '"""Nothing runs this."""', runner: '"""Run by the fake test."""',
                 fake_test: "subprocess.run(['_lint_probe_runner.py'])"}
        real = lint.text_of
        lint.text_of = lambda p: texts.get(p, "") if p in texts else real(p)
        try:
            found = {Path(f[1]).name for f in lint.check_untested(list(texts))}
        finally:
            lint.text_of = real
        self.assertEqual(found, {"_lint_probe_lonely.py"})

    def test_private_data_is_found_and_never_baselined(self):
        home = "/" + "home/somebody/notes"  # built at run time: this file is linted too
        with tempfile.TemporaryDirectory(dir=ROOT / "vault") as tmp:
            doc = Path(tmp) / "doc.md"
            doc.write_text(f"Open {home} for the notes.\n", encoding="utf-8")
            found = lint.check_private([doc])
        self.assertTrue(any("machine path" in f[2] for f in found), found)
        self.assertNotIn("private |", lint.BASELINE.read_text(encoding="utf-8"))

    def test_cards_are_checked(self):
        self.assertEqual(lint.check_card(), [])


if __name__ == "__main__":
    unittest.main()

"""Everything that reads private/ still works when private/ does not exist.

Defect this exists for: goals, pitches, trend reports, the tracker database and the case
studies moved out of the tracked tree. A fresh clone has none of them, so every reader has to
say what is missing and carry on instead of crashing or pointing at nothing.

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
TRENDS = ROOT / "tools" / "trends"

# Words that show a file tells its reader what to do when the private file is not there.
FALLBACK = re.compile(
    r"missing|may not exist|when it exists|when present|if it exists|when you keep one|"
    r"created (?:as|on|when)|creates? (?:it|the folder|that folder)|not (?:yet )?available|no database yet",
    re.I,
)
PRIVATE_SLOT = re.compile(r"private/(?:goals\.md|pitches|trends|case-studies)")
# The vault's rule sits in vault/INDEX.md, which every vault reader loads first; the genre,
# pattern and fundamentals files only cite the report as a data source.
COVERED_BY_INDEX = re.compile(r"^vault/(?:genres|patterns|fundamentals)/")
NOT_READERS = {
    "tests/test_public_tree.py", "tests/test_private_optional.py",
    "tools/trends/trends/config.py",    # creates the folder (asserted below)
    "tools/trends/trends/__main__.py",  # help text; behaviour asserted below
    "tools/trends/themes.yaml",         # a comment about where to find an id
    "tools/toolkit_lint.py",
}


def python_with_tracker_deps() -> str | None:
    for exe in (TRENDS / ".venv" / "bin" / "python", Path(sys.executable)):
        if exe.exists() and subprocess.run([str(exe), "-c", "import yaml, requests"],
                                           capture_output=True).returncode == 0:
            return str(exe)
    return None


class WithoutPrivate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.private = Path(self.tmp.name) / "no-private-here"
        self.env = {**os.environ, "ROBLOX_FINAL_PRIVATE": str(self.private)}

    def tearDown(self):
        self.tmp.cleanup()

    def run_py(self, exe, *args, cwd=ROOT):
        return subprocess.run([exe, *args], cwd=cwd, env=self.env, capture_output=True, text=True)

    def test_vault_lint_passes_and_says_what_was_skipped(self):
        r = self.run_py(sys.executable, "tools/vault_lint.py")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("private/case-studies/ is missing", r.stdout)
        self.assertNotIn("Traceback", r.stderr)

    def test_vault_has_no_links_into_private(self):
        hits = []
        for p in (ROOT / "vault").rglob("*.md"):
            for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if re.search(r"\]\((?:\.\./)*private/", line):
                    hits.append(f"{p.relative_to(ROOT)}:{n}")
        self.assertEqual(hits, [], "a clone without private/ would show these as dead links")

    def test_tracker_without_data_explains_and_creates_its_folder(self):
        exe = python_with_tracker_deps()
        if exe is None:
            self.skipTest("tracker dependencies (requests, PyYAML) not installed")
        look = self.run_py(exe, "-m", "trends", "lookup", "anything", cwd=TRENDS)
        self.assertEqual(look.returncode, 1)
        self.assertIn("No stored game", look.stderr)
        self.assertNotIn("Traceback", look.stderr)
        self.assertTrue((self.private / "trends" / "data" / "trends.db").exists(),
                        "the tracker should create private/trends/data on first run")
        rep = self.run_py(exe, "-m", "trends", "report", cwd=TRENDS)
        self.assertEqual(rep.returncode, 1)
        self.assertIn("No snapshots yet", rep.stderr)
        self.assertNotIn("Traceback", rep.stderr)

    def test_report_is_written_under_private(self):
        exe = python_with_tracker_deps()
        if exe is None:
            self.skipTest("tracker dependencies (requests, PyYAML) not installed")
        code = ("from trends import config; "
                "print(config.DEFAULT_REPORT_DIR); print(config.DEFAULT_DB); print(config.CACHE_DIR)")
        r = self.run_py(exe, "-c", code, cwd=TRENDS)
        self.assertEqual(r.returncode, 0, r.stderr)
        for line in r.stdout.split():
            self.assertTrue(line.startswith(str(self.private)), f"{line} is outside private/")
        self.assertFalse((ROOT / "vault" / "trends").exists(), "reports must not be written into the vault")

    def test_scheduled_runner_logs_under_private(self):
        text = (TRENDS / "run.sh").read_text(encoding="utf-8")
        self.assertIn("ROBLOX_FINAL_PRIVATE", text)
        self.assertNotRegex(text, r">>\s*data/")

    def test_goals_template_ships(self):
        t = (ROOT / "goals.template.md").read_text(encoding="utf-8")
        self.assertIn("private/goals.md", t)
        self.assertIn("TBD", t)


class ReadersSayWhatToDo(unittest.TestCase):
    """Coverage: every tracked file that names a private slot also says what happens without it."""

    def test_each_reader_states_a_fallback(self):
        out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-co", "--exclude-standard"],
                             capture_output=True, text=True)
        if out.returncode != 0:
            self.skipTest("not a git checkout")
        silent, readers = [], 0
        for rel in filter(None, out.stdout.splitlines()):
            p = ROOT / rel
            if rel in NOT_READERS or COVERED_BY_INDEX.match(rel) or not p.is_file():
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if PRIVATE_SLOT.search(text):
                readers += 1
                if not FALLBACK.search(text):
                    silent.append(rel)
        self.assertGreater(readers, 8, "expected the known readers to be found")
        self.assertEqual(silent, [], "these name a private file without saying what to do when it is missing")

    def test_vault_index_carries_the_rule_for_vault_files(self):
        t = (ROOT / "vault" / "INDEX.md").read_text(encoding="utf-8")
        self.assertIn("If it is missing", t)
        self.assertRegex(t, r"If `private/case-studies/` is missing")


if __name__ == "__main__":
    unittest.main()

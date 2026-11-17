"""A visitor's first pages never link to a file that is not in the tree.

Defect this exists for: README, CLAUDE.md and docs/ name files by relative link, and files
moved (into private/, into the skills). A dead link is the first broken thing a visitor meets.
Links into private/ are skipped: that folder may not exist in a clone, and its readers say so.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
FIRST_PAGES = ("README.md", "NOTICE.md", "CLAUDE.md", "CONTRIBUTING.md", "CHANGELOG.md")


class DocLinks(unittest.TestCase):
    maxDiff = None

    def test_top_level_doc_links_resolve(self):
        pages = [ROOT / n for n in FIRST_PAGES if (ROOT / n).exists()]
        pages += sorted((ROOT / "docs").glob("*.md"))
        dead = []
        for page in pages:
            for n, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
                for target in LINK.findall(line):
                    if re.match(r"[a-z]+:", target) or target.startswith("private/"):
                        continue
                    if not (page.parent / target).exists():
                        dead.append(f"{page.relative_to(ROOT).as_posix()}:{n}: {target}")
        self.assertEqual(dead, [])


if __name__ == "__main__":
    unittest.main()

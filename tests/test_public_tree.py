"""The tracked tree is public: no personal names, emails or machine paths, and no stale paths.

Defect this exists for: the toolkit grew on one machine, so its docs carried the owner's name,
home folder and notes, and pointed at files (goals, pitches, trend reports, case studies) that
now live in private/. A fresh clone must not show any of that or point at a path that is gone.

Run: python3 -m unittest discover -s tests -v

Literal names are not written here (that would put them in the tracked tree). Generic patterns
catch emails and home folders. For your own name, handle or email, list them one per line in
private/identity.txt; when that file exists, every term in it is also searched for.
"""
from __future__ import annotations

import os
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path(os.environ.get("ROBLOX_FINAL_PRIVATE") or ROOT / "private").expanduser()
BINARY = {".ttf", ".png", ".jpg", ".jpeg", ".gif", ".blend", ".rbxm", ".rbxl", ".db", ".ogg", ".mp3", ".wav", ".fbx", ".glb"}

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[a-z]{2,}")
EMAIL_OK = re.compile(r"noreply@|@example\.(com|org)$|^git@github\.com$|@users\.noreply\.github\.com$")
HOME = re.compile(r"(?:/home/|/Users/|/mnt/c/Users/|C:[\\/]+Users[\\/]+)([A-Za-z0-9._<>$-]+)")
HOME_OK = {"<you>", "<user>", "<name>", "you", "user", "runner", "$USER", "USERNAME", "<username>", "name"}
# The two folders the toolkit was assembled from, and the wording that told that story.
SEAM = re.compile(r"(?:~|\.\.)/roblox-studio\b|\broblox-ai-skills\b|\broblox-workflow\b|Merged on 20\d\d-")
# Paths that moved to private/. Each is fine only with private/ in front of it.
MOVED = [
    (re.compile(r"(?<![\w/.-])goals\.md"), "goals.md is private/goals.md (template: goals.template.md)"),
    (re.compile(r"(?<![\w/-])pitches/"), "pitches/ is private/pitches/"),
    (re.compile(r"vault/trends\b"), "trend reports are in private/trends/"),
    (re.compile(r"vault/case-studies\b|\]\([^)]*case-studies/"), "case studies are private; cite as (case study: <slug>)"),
    (re.compile(r"docs/history\b"), "docs/history/ is private/history/"),
    (re.compile(r"tools/trends/data\b"), "tracker data is in private/trends/data/"),
]
# A tracked file may name a private slot (private/goals.md) but never one specific private file.
SPECIFIC_PRIVATE = re.compile(
    r"private/(?:pitches/\d{4}-|trends/history/\d{4}-|history/[\w-]+\.md|notes/[\w-]+\.md|archive/[\w-]+)")
SELF = {"tests/test_public_tree.py", "tools/toolkit_lint.py"}  # these files define the patterns
# Files whose job is to name old paths: the move list, its script and test, and the evidence.
OLD_PATH_DOCS = {"docs/migration.md", "tools/migrate_game.py", "tests/test_migration.py",
                 "docs/vault-readers.md", "docs/redundancy-map.md"}
MOVED_OK = {
    ".gitignore",          # still ignores the old data folder so an old checkout stays clean
    "docs/migration.md",   # lists old -> new paths on purpose
    "CHANGELOG.md",        # says what moved
    "docs/decisions.md",   # says why it moved
} | OLD_PATH_DOCS


def tracked() -> list[Path]:
    """Files git would publish: tracked plus not-yet-added, never ignored ones."""
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-co", "--exclude-standard"],
                             capture_output=True, text=True, check=True).stdout.splitlines()
        files = [ROOT / f for f in out if f]
    except (OSError, subprocess.CalledProcessError):
        files = [p for p in ROOT.rglob("*") if ".git" not in p.parts and "private" not in p.parts]
    return [p for p in files if p.is_file() and p.suffix.lower() not in BINARY]


def lines(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return
    for n, line in enumerate(text.splitlines(), 1):
        yield n, line


class PublicTree(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.files = tracked()
        cls.rel = {p: p.relative_to(ROOT).as_posix() for p in cls.files}

    def scan(self, check) -> list[str]:
        hits = []
        for p in self.files:
            rel = self.rel[p]
            if rel in SELF:
                continue
            for n, line in lines(p):
                msg = check(rel, line)
                if msg:
                    hits.append(f"{rel}:{n}: {msg}")
        return hits

    def test_no_email_addresses(self):
        def check(rel, line):
            for m in EMAIL.finditer(line):
                if not EMAIL_OK.search(m.group(0)) and "@" not in rel:
                    return f"email address {m.group(0)}"
        self.assertEqual(self.scan(check), [])

    def test_no_home_folders(self):
        def check(rel, line):
            for m in HOME.finditer(line):
                if m.group(1) not in HOME_OK:
                    return f"machine path {m.group(0)} (write ~ or /home/<you>)"
        self.assertEqual(self.scan(check), [])

    def test_no_trace_of_the_two_source_folders(self):
        self.assertEqual(self.scan(lambda rel, line: "names an old source folder" if SEAM.search(line) else None), [])

    def test_no_stale_paths_to_moved_files(self):
        def check(rel, line):
            if rel in MOVED_OK:
                return None
            for pattern, why in MOVED:
                if pattern.search(line):
                    return why
        self.assertEqual(self.scan(check), [])

    def test_no_reference_to_one_specific_private_file(self):
        def check(rel, line):
            m = SPECIFIC_PRIVATE.search(line)
            if m and rel not in MOVED_OK:
                return f"points at a specific private file ({m.group(0)})"
        self.assertEqual(self.scan(check), [])

    def test_top_level_doc_links_resolve(self):
        """A visitor's first pages (README, NOTICE, CLAUDE, CONTRIBUTING, CHANGELOG, docs/) never
        link to a file that is not in the tree: a dead link is the first broken thing a visitor
        meets."""
        link = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
        pages = [ROOT / n for n in ("README.md", "NOTICE.md", "CLAUDE.md", "CONTRIBUTING.md", "CHANGELOG.md")]
        pages += sorted((ROOT / "docs").glob("*.md"))
        dead = []
        for page in pages:
            for n, line in lines(page):
                for target in link.findall(line):
                    if re.match(r"[a-z]+:", target) or target.startswith("private/"):
                        continue
                    if not (page.parent / target).exists():
                        dead.append(f"{page.relative_to(ROOT).as_posix()}:{n}: {target}")
        self.assertEqual(dead, [])

    def test_private_is_ignored_and_untracked(self):
        out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "private"], capture_output=True, text=True)
        if out.returncode != 0:
            self.skipTest("not a git checkout")
        self.assertEqual(out.stdout.strip(), "", "files under private/ are tracked")
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("private/", ignore)

    def test_identity_terms_when_listed(self):
        terms_file = PRIVATE / "identity.txt"
        if not terms_file.exists():
            self.skipTest("private/identity.txt not present (expected on a fresh clone and in CI)")
        terms = [t.strip().lower() for t in terms_file.read_text(encoding="utf-8").splitlines()
                 if t.strip() and not t.startswith("#")]
        # The public repository's own address is the one place an owner handle may appear.
        allowed = re.compile(r"github\.com/[\w-]+/roblox-final")

        def check(rel, line):
            low = allowed.sub("", line.lower())
            for term in terms:
                if re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", low):
                    return "contains a term from private/identity.txt"
        self.assertEqual(self.scan(check), [])


if __name__ == "__main__":
    unittest.main()

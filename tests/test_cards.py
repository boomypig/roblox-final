"""Agent cards carry every item of every section they claim, and are rebuilt when a source changes.

Defect this exists for: the map-builder read about 24,000 tokens of reference before every run,
and the reviewer read the whole quality bar and roblox-code skill. A card is cheaper only if
it drops nothing an agent acts on. This is the coverage proof: for each carried section, every
item line of the source appears, word for word, in the card; the counts in the card's coverage
table match; the sections the task named are all carried; and a card older than its source
fails.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_cards  # noqa: E402



class Cards(unittest.TestCase):
    def test_cards_are_current(self):
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "build_cards.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_every_source_item_is_in_its_card_word_for_word(self):
        for name, card in build_cards.CARDS.items():
            text = (ROOT / card["path"]).read_text(encoding="utf-8")
            missing = []
            for path, heading in card["sections"]:
                _, body, first, _ = build_cards.extract(path, heading)
                for offset, line in enumerate(body.splitlines()):
                    # every line, not only list items: prose rules count too; headings are demoted
                    if line.strip() and not line.startswith("#") and line not in text:
                        missing.append(f"{path}:{first + 1 + offset}: {line.strip()[:70]}")
            self.assertEqual(missing, [], f"{name} card drops items")

    def test_coverage_table_counts_match_the_sources(self):
        for name, card in build_cards.CARDS.items():
            text = (ROOT / card["path"]).read_text(encoding="utf-8")
            rows = re.findall(r"^\| (\d+) \| `([^`]+)` \| .* \| (\d+)-(\d+) \| (\d+) \|$", text, re.M)
            self.assertEqual(len(rows), len(card["sections"]), name)
            for (n, path, _, _, count), (spath, heading) in zip(rows, card["sections"]):
                self.assertEqual(path, spath)
                _, body, _, _ = build_cards.extract(spath, heading)
                self.assertEqual(int(count), build_cards.items(body), f"{name} section {n}")
                self.assertTrue(body.strip(), f"{name} section {n} carries nothing")

    def test_builder_card_carries_what_the_task_named(self):
        sections = build_cards.CARDS["map-builder"]["sections"]
        refs = {f".claude/skills/roblox-map/references/{f}" for f in
                ("studio-mcp.md", "visual-quality.md", "performance-and-devices.md")}
        # every agent checklist in the three source files
        for ref in refs:
            self.assertIn((ref, "## Checklist for agents"), sections, ref)
        self.assertIn((".claude/skills/roblox-map/references/visual-quality.md",
                       '## "Does this look default?" checklist'), sections)
        self.assertIn((".claude/skills/roblox-map/references/performance-and-devices.md", "## Budget table"), sections)
        self.assertIn((".claude/skills/roblox-map/references/studio-mcp.md", "## Common build bugs"), sections)

    def test_reviewer_card_scores_every_quality_bar_area(self):
        qb = (ROOT / ".claude/skills/build/references/quality-bar.md").read_text(encoding="utf-8")
        areas = re.findall(r"^## ([A-Z])\. ", qb, re.M)
        card = (ROOT / build_cards.CARDS["reviewer"]["path"]).read_text(encoding="utf-8")
        for a in areas:
            self.assertRegex(card, rf"(?m)^## \d+\. {a}\. ", f"area {a} missing from the reviewer card")
        self.assertIn("design/layout.json", card)

    def test_card_is_smaller_than_what_it_replaces(self):
        builder = (ROOT / build_cards.CARDS["map-builder"]["path"]).stat().st_size
        sources = sum((ROOT / f".claude/skills/roblox-map/references/{f}").stat().st_size
                      for f in ("studio-mcp.md", "visual-quality.md", "performance-and-devices.md"))
        self.assertLess(builder, sources / 2)

    def test_a_changed_source_makes_the_card_stale(self):
        path, heading = build_cards.CARDS["map-builder"]["sections"][0]
        src = ROOT / path
        original = src.read_text(encoding="utf-8")
        try:
            src.write_text(original.replace(heading, heading + "\n- an item added after the card was built", 1),
                           encoding="utf-8")
            self.assertTrue(build_cards.check("map-builder"))
        finally:
            src.write_text(original, encoding="utf-8")
        self.assertEqual(build_cards.check("map-builder"), [])


if __name__ == "__main__":
    unittest.main()

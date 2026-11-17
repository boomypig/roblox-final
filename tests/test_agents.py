"""The reviewer and spec-writer read what the task says, and every agent can run its own gate.

Defects this exists for:
- The reviewer read the whole quality bar and roblox-code skill, and assumed every game keeps
  its remotes in Net.luau and its pure rules in Core/. A game laid out otherwise was reviewed
  against folders it does not have.
- The spec-writer was told to run check_spec.py with no Bash tool, so its own gate could not run.
- An agent told to read a card it does not name, or a file that does not exist, fails silently.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AG = ROOT / ".claude" / "agents"


def tools(name: str) -> set[str]:
    text = (AG / f"{name}.md").read_text(encoding="utf-8")
    line = re.search(r"^tools:\s*(.*)$", text, re.M).group(1)
    return {t.strip() for t in line.split(",")}


class Agents(unittest.TestCase):
    def test_reviewer_reads_the_card_and_the_layout_map(self):
        text = (AG / "reviewer.md").read_text(encoding="utf-8")
        self.assertIn("reviewer-card.md", text)
        self.assertIn("design/layout.json", text)
        self.assertLess(text.index("design/layout.json"), text.index("reviewer-card.md"),
                        "the layout map is read before the rules that use its paths")
        self.assertNotIn("remotes not declared in Net.luau", text)
        self.assertNotIn('"standing rules" and "traps" sections of', text)

    def test_spec_writer_uses_the_short_index_and_decisions_in_full(self):
        text = (AG / "spec-writer.md").read_text(encoding="utf-8")
        self.assertIn("docs/decisions.md in full", text)
        self.assertIn("vault/INDEX.md", text)
        self.assertIn("only when a name is not enough", text)

    def test_every_agent_that_runs_a_command_has_bash(self):
        for p in AG.glob("*.md"):
            text = p.read_text(encoding="utf-8")
            body = text.split("---", 2)[2]
            runs = re.search(r"\bpython3? [^\n`]*\.py\b", body) and re.search(r"\b(Run|run) (the gate|`python|the gates)", body)
            if runs:
                self.assertIn("Bash", tools(p.stem), f"{p.name} is told to run a script but has no Bash")

    def test_files_an_agent_is_told_to_read_exist(self):
        missing = []
        for p in AG.glob("*.md"):
            for ref in re.findall(r"\.\./roblox-final/([\w./-]+\.(?:md|lua|py|json))", p.read_text(encoding="utf-8")):
                if "<" in ref:
                    continue
                if not (ROOT / ref).exists():
                    missing.append(f"{p.name}: {ref}")
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()

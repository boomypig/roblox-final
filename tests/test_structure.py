"""Every skill and agent has the same shape, and docs/structure.md describes what is on disk.

Defect this exists for: half the toolkit had rules, references, scripts with a stated reason,
traps and a gate; the other half was a page of prose with none of them, so its output could
not be checked and its lessons had nowhere to go. The coverage table in docs/structure.md is
the proof that the shape holds; this test keeps the table true.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / ".claude" / "skills"
AG = ROOT / ".claude" / "agents"
STRUCTURE = (ROOT / "docs" / "structure.md").read_text(encoding="utf-8")


def rows(first_header: str) -> dict[str, list[str]]:
    out, on = {}, False
    for line in STRUCTURE.splitlines():
        if line.startswith(f"| {first_header} |"):
            on = True
            continue
        if on:
            if not line.startswith("|"):
                on = False
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not re.fullmatch(r"[-: ]+", cells[0]):
                out[cells[0].strip("`")] = cells[1:]
    return out


SKILL_ROWS = rows("Skill")
AGENT_ROWS = rows("Agent")


class Shape(unittest.TestCase):
    def test_every_skill_and_agent_has_a_row(self):
        skills = sorted(p.parent.name for p in SK.glob("*/SKILL.md"))
        agents = sorted(p.stem for p in AG.glob("*.md"))
        self.assertEqual(sorted(SKILL_ROWS), skills)
        self.assertEqual(sorted(AGENT_ROWS), agents)

    def test_no_cell_is_empty(self):
        for name, cells in {**SKILL_ROWS, **AGENT_ROWS}.items():
            self.assertTrue(all(cells), f"{name} has an empty part in docs/structure.md")

    def test_cited_headings_and_files_exist(self):
        missing = []
        for name, cells in SKILL_ROWS.items():
            skill = SK / name
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            for cell in cells:
                for heading in re.findall(r'"([^"]+)"', cell):
                    if not re.search(r"^#{1,4} .*" + re.escape(heading), text, re.M):
                        missing.append(f"{name}: no heading containing {heading!r} in SKILL.md")
                for path in re.findall(r"`((?:references|scripts|templates|sim)/[^`]*)`", cell):
                    if not (skill / path).exists():
                        missing.append(f"{name}: {path} does not exist")
                for script in re.findall(r"`([a-z_]+\.(?:py|lua))`", cell):
                    if not list(SK.rglob(script)):
                        missing.append(f"{name}: {script} does not exist in any skill")
        self.assertEqual(missing, [])

    def test_every_python_script_says_why_it_exists(self):
        silent = []
        for p in sorted(SK.glob("*/scripts/*.py")) + sorted((ROOT / "tools").glob("*.py")):
            doc = ast.get_docstring(ast.parse(p.read_text(encoding="utf-8")))
            if not doc or len(doc.split()) < 8:
                silent.append(p.relative_to(ROOT).as_posix())
        self.assertEqual(silent, [])

    def test_design_side_skills_have_all_five_parts(self):
        for name, gate in (("pitch", "check_pitch.py"), ("art-brief", "check_brief.py"), ("build", "check_spec.py")):
            text = (SK / name / "SKILL.md").read_text(encoding="utf-8")
            for heading in ("## Rules", "## Gate", "## References", "## Traps"):
                self.assertIn(heading, text, f"{name}/SKILL.md has no {heading}")
            self.assertTrue((SK / name / "scripts" / gate).exists())
            self.assertIn(gate, text)

    def test_agents_are_thin_and_name_their_owner(self):
        for name, cells in AGENT_ROWS.items():
            owner = cells[0].strip("`")
            self.assertTrue((SK / owner / "SKILL.md").exists(), f"{name}: owner {owner} is not a skill")
            text = (AG / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn(owner, text, f"{name} does not name its owning skill {owner}")

    def test_an_agent_holds_no_reference_of_its_own(self):
        extra = [p.relative_to(ROOT).as_posix() for p in AG.rglob("*") if p.is_file() and p.parent != AG]
        self.assertEqual(extra, [], "agent knowledge belongs in the owning skill's references/")


if __name__ == "__main__":
    unittest.main()

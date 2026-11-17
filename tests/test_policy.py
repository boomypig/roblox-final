"""One operating policy, one workflow doc, one shape for every skill and agent.

Defect this exists for: the build skills said "the run does not stop" and "never offer
options" while the design skills, agents and starter said "ask instead of guessing" and stopped
to ask; there were three workflow docs describing two ways to build. A visitor could tell the
toolkit came from two sources, and an agent could find a line telling it to do either thing.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / ".claude" / "skills"
AG = ROOT / ".claude" / "agents"

# Wording that tells an agent to stop and ask, or to hand the choice back, inside a task.
CONTRADICTS = [
    (re.compile(r"instead of guessing", re.I), "tells the agent to ask rather than decide"),
    (re.compile(r"ask before (writing|building|drafting|starting)", re.I), "asks mid-task"),
    (re.compile(r"return up to \d+ questions", re.I), "stops to return questions instead of drafting"),
    (re.compile(r"ask up to \d+ questions", re.I), "asks questions mid-task"),
    (re.compile(r"AskUserQuestion"), "asks through a tool mid-task"),
    (re.compile(r"\(empty = ask", re.I), "asks instead of deciding a default"),
    (re.compile(r"offer to (write|do|run|build)", re.I), "offers instead of deciding"),
    (re.compile(r"offers? (the user )?(a choice|options)|present options|which (one )?would you (like|prefer)", re.I),
     "offers options"),
    (re.compile(r"confirm (you read|with the user|before drafting)", re.I), "waits for a confirmation mid-task"),
    (re.compile(r"stop and (ask|tell me)", re.I), "stops to ask"),
    (re.compile(r"ask first", re.I), "asks first"),
]
# Lines that state the rule the pattern would otherwise flag.
NEGATED = re.compile(r"never|do not|don't|doesn't|not ask|no questions|can't ask|cannot ask|without asking", re.I)
# Machine setup is the case the policy names: only the user knows their paths and keys.
SETUP = SK / "roblox-skills-setup" / "SKILL.md"

DESIGN_SIDE = [
    SK / "pitch" / "SKILL.md", SK / "art-brief" / "SKILL.md", SK / "build" / "SKILL.md",
    AG / "spec-writer.md", AG / "map-builder.md", AG / "reviewer.md",
]


def governed_files() -> list[Path]:
    files = list(AG.glob("*.md")) + list(SK.glob("*/SKILL.md"))
    files += [p for p in (ROOT / "starter").rglob("*.md")]
    files += [ROOT / "CLAUDE.md", ROOT / "README.md"]
    return [p for p in files if p != SETUP]


class OnePolicy(unittest.TestCase):
    def test_no_line_contradicts_the_policy(self):
        hits = []
        for p in governed_files():
            for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if NEGATED.search(line):
                    continue
                for pattern, why in CONTRADICTS:
                    if pattern.search(line):
                        hits.append(f"{p.relative_to(ROOT).as_posix()}:{n}: {why}: {line.strip()[:90]}")
        self.assertEqual(hits, [])

    def test_policy_has_one_owner(self):
        text = (ROOT / "docs" / "workflow.md").read_text(encoding="utf-8")
        self.assertIn("## Operating policy", text)
        for phrase in ("You approve once", "Inside a task nobody stops to ask", "logged as assumptions",
                       "Never offer options", "The gate is the only stopping point", "The only asks"):
            self.assertIn(phrase, text)
        owners = [p for p in governed_files() if "## Operating policy" in p.read_text(encoding="utf-8")]
        self.assertEqual(owners, [], "the policy is restated outside docs/workflow.md")

    def test_design_side_items_point_at_the_policy(self):
        for p in DESIGN_SIDE:
            text = p.read_text(encoding="utf-8")
            self.assertRegex(text, r"docs/workflow\.md", f"{p.name} does not point at the operating policy")

    def test_front_door_points_at_the_policy(self):
        text = (SK / "create-roblox-game" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("docs/workflow.md", text)
        self.assertNotIn("wired to the rest of the toolkit", text)

    def test_setup_is_the_named_exception(self):
        policy = (ROOT / "docs" / "workflow.md").read_text(encoding="utf-8")
        self.assertIn("machine paths and keys", policy)
        self.assertIn("Ask, do not assume", SETUP.read_text(encoding="utf-8"))


class OneWorkflow(unittest.TestCase):
    def test_there_is_one_workflow_doc(self):
        docs = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("workflow.md")
                if ".git" not in p.parts and "private" not in p.parts]
        self.assertEqual(docs, ["docs/workflow.md"])

    def test_every_skill_and_agent_has_a_place_in_it(self):
        text = (ROOT / "docs" / "workflow.md").read_text(encoding="utf-8")
        names = [p.parent.name for p in SK.glob("*/SKILL.md")] + [p.stem for p in AG.glob("*.md")]
        missing = []
        for name in names:
            if name.startswith("roblox-asset-"):
                short = "-" + name.rsplit("-", 1)[1]
                if name in text or f"`{short}`" in text or "roblox-asset-*" in text:
                    continue
            if f"`{name}`" not in text:
                missing.append(name)
        self.assertEqual(missing, [])

    def test_every_step_names_a_gate(self):
        text = (ROOT / "docs" / "workflow.md").read_text(encoding="utf-8")
        rows = [ln for ln in text.splitlines() if ln.startswith("| **")]
        self.assertGreaterEqual(len(rows), 13)
        for row in rows:
            cells = [c.strip() for c in row.strip("|").split("|")]
            self.assertEqual(len(cells), 5, row[:60])
            self.assertTrue(all(cells), f"empty cell in: {row[:60]}")

    def test_gate_scripts_named_in_the_path_exist(self):
        text = (ROOT / "docs" / "workflow.md").read_text(encoding="utf-8")
        for script in ("check_pitch.py", "check_brief.py", "check_spec.py", "check.py", "validate.py",
                       "verify_wired.py", "section.py", "new_game.py"):
            self.assertIn(script, text)
            self.assertTrue(list(ROOT.rglob(script)), f"{script} is named in the workflow but does not exist")


if __name__ == "__main__":
    unittest.main()

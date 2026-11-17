"""The gates on the design-side outputs: a pitch file, a brief, a mechanic spec.

Defect this exists for: the pitch, brief and spec steps ended on "the user reads it", with no
check a script could run. An unfinished template, a total that is not the sum of its scores or
a spec with no acceptance criteria all looked done. Each gate must fail its own template (an
unfilled doc is not a finished one) and pass a complete example.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / ".claude" / "skills"
CHECK_PITCH = SK / "pitch" / "scripts" / "check_pitch.py"
CHECK_BRIEF = SK / "art-brief" / "scripts" / "check_brief.py"
CHECK_SPEC = SK / "build" / "scripts" / "check_spec.py"


def run(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True)


def pitch_block(n: int, scores: tuple[int, int, int, int, int], total: int | None = None) -> str:
    total = sum(scores) if total is None else total
    return f"""## {n}. Working title {n} — a hook

- **Genre + themes:** tycoon; themes: build
- **Core loop:** place, earn, upgrade
- **Unique spin:** the player trades shifts with a friend
- **Reference games:** two charted tycoons; learn pacing, do not copy names
- **Why now:** 12 games on the theme, 40,000 players (data, 2026-11-01)
- **Target audience:** 9 to 13, phone first, all ages
- **Monetization:** one pass, cosmetics
- **Solo-dev scope:** MVP in 3 weeks
- **Risks:** saturation; scope; retention
- **Scores:**

| Trend momentum | Saturation (inverse) | Uniqueness | Solo feasibility | Retention potential | Total /25 |
|---|---|---|---|---|---|
| {scores[0]} | {scores[1]} | {scores[2]} | {scores[3]} | {scores[4]} | {total} |

One line per score.
"""


def pitch_file(blocks: list[str], totals: list[int], data_cite: str = "(data, 2026-11-01)") -> str:
    rows = "\n".join(f"| Working title {i + 1} | 3 | 3 | 3 | 3 | 3 | {t} |" for i, t in enumerate(totals))
    return f"""---
title: Game pitches — 2026-11-02
type: pitches
constraints: "goals file defaults"
trends-report: 2026-11-01, 12 snapshots, 9 days
---

## Context
Constraints used, and the assumptions made. Charts were read {data_cite}.

{''.join(blocks)}
## Summary

| Pitch | Trend | Saturation | Uniqueness | Feasibility | Retention | Total |
|---|---|---|---|---|---|---|
{rows}

## What I'd prototype first and why `(inferred)`
Pitch 1, with a one-week greybox test.

## What would change these scores
More trend history.
"""


GOOD_BLOCKS = [pitch_block(i, (5 - (i > 2), 4, 4, 4, 4 - (i > 4))) for i in range(1, 6)]
GOOD_TOTALS = [21, 21, 20, 20, 19]


class PitchGate(unittest.TestCase):
    def check(self, text: str):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "2026-11-02.md"
            p.write_text(text, encoding="utf-8")
            return run(CHECK_PITCH, str(p))

    def test_complete_file_passes(self):
        r = self.check(pitch_file(GOOD_BLOCKS, GOOD_TOTALS))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_total_that_is_not_the_sum_fails(self):
        blocks = GOOD_BLOCKS[:4] + [pitch_block(5, (4, 4, 4, 4, 3), total=23)]
        r = self.check(pitch_file(blocks, [23, 21, 21, 20, 20]))
        self.assertEqual(r.returncode, 1)
        self.assertIn("not the sum", r.stdout)

    def test_undated_data_citation_fails(self):
        r = self.check(pitch_file(GOOD_BLOCKS, GOOD_TOTALS, data_cite="(data)"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("has no date", r.stdout)

    def test_four_pitches_fail(self):
        r = self.check(pitch_file(GOOD_BLOCKS[:4], GOOD_TOTALS[:4]))
        self.assertEqual(r.returncode, 1)
        self.assertIn("expected 1 to 5", r.stdout)

    def test_unsorted_summary_fails(self):
        r = self.check(pitch_file(GOOD_BLOCKS, [19, 21, 21, 20, 20]))
        self.assertEqual(r.returncode, 1)
        self.assertIn("not sorted", r.stdout)

    def test_promise_of_success_fails(self):
        text = pitch_file(GOOD_BLOCKS, GOOD_TOTALS).replace("a one-week greybox test", "it is guaranteed to chart")
        r = self.check(text)
        self.assertEqual(r.returncode, 1)
        self.assertIn("claims an outcome", r.stdout)

    def test_missing_field_fails(self):
        text = pitch_file(GOOD_BLOCKS, GOOD_TOTALS).replace("- **Risks:** saturation; scope; retention\n", "", 1)
        r = self.check(text)
        self.assertEqual(r.returncode, 1)
        self.assertIn("field `Risks` is missing", r.stdout)


ART = """# Art direction
Status: draft

## In the user's words
> "Warm and small, like a village at dusk."

## References
| Image | Take from it | Leave out |
|---|---|---|
| [ref-1.png](../images/ref/ref-1.png) | Rounded roofs, warm windows | The logo on the sign |

## Style in one line
Chunky rounded cottages, soft shadows, warm accents.

## Lighting
- Preset: Golden hour (roblox-map `references/visual-quality.md`)
- Set by hand in Studio Properties (not scriptable): `LightingStyle` = Soft,
  `PrioritizeLightingQuality` = true
- Sky: clear, low sun

## Palette
| Role | Name | RGB | Used on |
|---|---|---|---|
| Ground light | Sand | 226, 205, 160 | paths |
| Ground mid | Grass | 120, 170, 90 | lawns |
| Ground dark | Soil | 88, 70, 52 | beds |
| Support 1 | Plaster | 236, 224, 200 | walls |
| Support 2 | Roof | 150, 74, 60 | roofs |
| Accent (interactables, rewards) | Lantern | 255, 196, 64 | doors, pickups |
| Danger (hazards only) | Ember | 220, 40, 40 | hazards |

## Materials
| Surface | `Enum.Material` | Palette role | Notes |
|---|---|---|---|
| Main ground | Grass | Ground mid | |
| Paths | Cobblestone | Ground light | |

## Not this
- No neon, no flat grey Plastic.

## Assumptions
- **Assumption:** dusk rather than night, so the path stays readable.

## Open questions
-
"""

MAP = """# Map: Harbor
Status: approved
Art direction: [art-direction.md](../art-direction.md)

## In the user's words
> "A small harbor you can read from the spawn."

## References
| Image | Take from it | Leave out |
|---|---|---|
| [harbor-sketch.png](../../images/ref/harbor-sketch.png) | Layout | |

## Layout
- Overall size: 240 × 180 studs, height range 0 to 40
- Spawn: the quay, facing the lighthouse
- Main path: quay to market to lighthouse, 16 studs wide

## Zones
| # | Zone | Purpose | Size (studs) | Landmark | Hue | Notes |
|---|---|---|---|---|---|---|
| 1 | Quay | spawn | 60 × 40 | crane | sand | |

## Gameplay geometry (`Layout`)
| Element | Size / spacing (studs) | Tag | Notes |
|---|---|---|---|
| Main path | 16 wide | Path | |

## Dressing
- Zone 1: crates, nets, lamp posts

## Check views
| View | Camera at → looking at | Must show |
|---|---|---|
| Spawn | 0, 12, -40 → 0, 8, 60 | the crane and the path |
| Top-down | 0, 300, 0 → 0, 0, 0 | the layout |

## Budgets
From roblox-map `references/performance-and-devices.md`: 6,000 parts, 4 shadow lights.

## Not this
- No modern cars.

## Assumptions
-

## Open questions
-
"""


class BriefGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.game = Path(self.tmp.name)
        (self.game / "docs" / "images" / "ref").mkdir(parents=True)
        (self.game / "docs" / "design" / "maps").mkdir(parents=True)
        (self.game / "docs" / "images" / "ref" / "ref-1.png").write_bytes(b"png")
        (self.game / "docs" / "images" / "ref" / "harbor-sketch.png").write_bytes(b"png")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel: str, text: str) -> Path:
        p = self.game / rel
        p.write_text(text, encoding="utf-8")
        return p

    def test_every_template_fails_its_own_gate(self):
        for name in ("art-direction.md", "map-brief.md", "ui-brief.md"):
            text = (SK / "art-brief" / "templates" / name).read_text(encoding="utf-8")
            p = self.write("docs/design/" + name, text)
            r = run(CHECK_BRIEF, str(p))
            self.assertEqual(r.returncode, 1, f"{name} passed unfilled:\n{r.stdout}")
            self.assertIn("placeholder", r.stdout)

    def test_complete_art_direction_passes(self):
        r = run(CHECK_BRIEF, str(self.write("docs/design/art-direction.md", ART)))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_complete_map_brief_passes(self):
        r = run(CHECK_BRIEF, str(self.write("docs/design/maps/harbor.md", MAP)), "--require-approved")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_palette_without_rgb_fails(self):
        r = run(CHECK_BRIEF, str(self.write("docs/design/art-direction.md", ART.replace("255, 196, 64", "warm yellow"))))
        self.assertEqual(r.returncode, 1)
        self.assertIn("has no RGB value", r.stdout)

    def test_missing_reference_image_fails(self):
        (self.game / "docs" / "images" / "ref" / "ref-1.png").unlink()
        r = run(CHECK_BRIEF, str(self.write("docs/design/art-direction.md", ART)))
        self.assertEqual(r.returncode, 1)
        self.assertIn("not on disk", r.stdout)

    def test_check_view_without_coordinates_fails(self):
        text = MAP.replace("0, 300, 0 → 0, 0, 0", "above the map")
        r = run(CHECK_BRIEF, str(self.write("docs/design/maps/harbor.md", text)))
        self.assertEqual(r.returncode, 1)
        self.assertIn("camera position", r.stdout)

    def test_draft_fails_when_approval_is_required(self):
        r = run(CHECK_BRIEF, str(self.write("docs/design/art-direction.md", ART)), "--require-approved")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Status is draft", r.stdout)


SPEC = """# Checkpoints
Status: approved

## Player experience
Touching a flag saves your place. Falling puts you back at the last flag within a second.

## Rules
- A checkpoint counts once per player per run.
- **Assumption:** checkpoints reset when the round ends.

## Technical notes
- Server vs client: the server detects the touch and owns the stage number; the client only shows it.
- Where it lives (paths, tags): parts tagged `Checkpoint`.
- Data saved: nothing.

## Acceptance criteria
- [ ] Touching flag 3 then falling respawns the player at flag 3.
- [ ] A second touch of the same flag changes nothing.

## Out of scope
- Saving progress between sessions.

## Open questions
-
"""


class SpecGate(unittest.TestCase):
    def check(self, text: str, *args: str):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "checkpoints.md"
            p.write_text(text, encoding="utf-8")
            return run(CHECK_SPEC, str(p), *args)

    def test_template_fails_its_own_gate(self):
        text = (ROOT / "starter" / "docs" / "design" / "mechanics" / "_template.md").read_text(encoding="utf-8")
        r = self.check(text)
        self.assertEqual(r.returncode, 1, r.stdout)

    def test_complete_spec_passes(self):
        r = self.check(SPEC, "--require-approved")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_draft_is_refused_for_build(self):
        r = self.check(SPEC.replace("Status: approved", "Status: draft"), "--require-approved")
        self.assertEqual(r.returncode, 1)
        self.assertIn("has not approved", r.stdout)

    def test_draft_passes_the_writer_gate(self):
        r = self.check(SPEC.replace("Status: approved", "Status: draft"))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_no_acceptance_criteria_fails(self):
        text = SPEC.replace("- [ ] Touching flag 3 then falling respawns the player at flag 3.\n", "").replace(
            "- [ ] A second touch of the same flag changes nothing.\n", "")
        r = self.check(text)
        self.assertEqual(r.returncode, 1)
        self.assertIn("Acceptance criteria", r.stdout)

    def test_blank_server_vs_client_fails(self):
        r = self.check(SPEC.replace(
            "the server detects the touch and owns the stage number; the client only shows it.", ""))
        self.assertEqual(r.returncode, 1)
        self.assertIn("Server vs client", r.stdout)


if __name__ == "__main__":
    unittest.main()

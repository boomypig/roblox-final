"""Tagging, analysis and report rendering on a small synthetic history."""

from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from trends import analysis, db, report, tagging

LATEST = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)

# universe_id: (name, created, {days_before_latest: players}, up-and-coming on latest run?)
GAMES = {
    1: ("Steal a Thing", "2026-09-01T00:00:00Z", {8: 1000, 7: 2000, 1: 8000, 0: 9000}, False),
    2: ("Steal a Fish [UPDATE]", "2026-10-01T00:00:00Z", {3: 3000, 2: 3000, 1: 3000, 0: 3000}, True),
    3: ("Big Old Roleplay", "2018-05-01T00:00:00Z", {d: 100_000 for d in range(1, 9)} | {0: 90_000}, False),
    4: ("Steal Tycoon", "2026-10-10T00:00:00Z", {2: 2500, 1: 2500, 0: 2500}, True),
    5: ("Tiny Obby", "2020-01-01T00:00:00Z", {d: 50 for d in range(9)}, False),
    6: ("Steal the Event Hub", "2026-10-15T00:00:00Z", {1: 50_000, 0: 50_000}, True),  # Roblox-run
}
OFFICIAL = {6}


def build_db(days: int = 9) -> tuple:
    conn = db.connect(":memory:")
    for back in reversed(range(days)):
        taken = LATEST - timedelta(days=back)
        stamp = taken.isoformat().replace("+00:00", "Z")
        run_id = db.start_run(conn, stamp)
        with conn:
            rank = 0
            for uid, (name, created, players, rising) in GAMES.items():
                if back not in players:
                    continue
                db.upsert_game(conn, {"universe_id": uid, "name": name, "root_place_id": uid * 10, "created": created,
                                      "genre_l1": "Simulation" if "Steal" in name else "Roleplay & Avatar Sim",
                                      "description": "",
                                      "creator_name": "Roblox Presents" if uid in OFFICIAL else "Some Studio"}, stamp)
                db.insert_snapshot(conn, run_id, stamp, {"universe_id": uid, "name": name, "playing": players[back],
                                                         "visits": 1_000_000 + players[back] * (9 - back) * 10,
                                                         "up_votes": 90, "down_votes": 10})
                rank += 1
                db.insert_placement(conn, run_id, uid, "top-playing-now", rank, False)
                if rising and back == 0:
                    db.insert_placement(conn, run_id, uid, "up-and-coming", rank, False)
        db.finish_run(conn, run_id, stamp, "ok", 2, len(GAMES), 10, [])
    themes, manual = tagging.load_themes()
    tagging.retag_all(conn, themes, manual)
    return conn, themes


class Tagging(unittest.TestCase):
    def test_keyword_rules(self):
        self.assertTrue(tagging.keyword_pattern("egg").search("hatch eggs now"))
        self.assertFalse(tagging.keyword_pattern("egg").search("eggplant"))
        self.assertTrue(tagging.keyword_pattern("fish*").search("fishing rod"))
        self.assertTrue(tagging.keyword_pattern("tower defense").search("anime tower   defense"))
        self.assertTrue(tagging.keyword_pattern("+1").search("+1 speed every second"))
        self.assertFalse(tagging.keyword_pattern("rob").search("roblox"))

    def test_split_name(self):
        self.assertEqual(tagging.split_name("Steal An Egg [🎃 EVENT] (UPD 3)"), ("Steal An Egg", ["🎃 EVENT", "UPD 3"]))
        self.assertEqual(tagging.split_name("[NEW]"), ("[NEW]", ["NEW"]))

    def test_brackets_dont_create_themes(self):
        themes, _ = tagging.load_themes()
        self.assertNotIn("racing-cars", tagging.themes_for("Obby [CAR EVENT]", "", themes))

    def test_include_labels_matches_bracket_text(self):
        themes, _ = tagging.load_themes()
        self.assertIn("anomaly", tagging.themes_for("Sell Fries! [Anomaly]", "", themes))
        self.assertIn("cooking-food", tagging.themes_for("Sell Fries! [Anomaly]", "", themes))

    def test_description_opt_in_excludes_and_regex(self):
        spec = {"themes": {"speed": ["speed"],
                           "egg": {"keywords": ["egg"], "exclude": ["easter egg"], "description": True},
                           "verb-a": {"regex": ["^[^a-z0-9]*[a-z]+ (?:a|an) [a-z]"]}}}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "themes.yaml"
            path.write_text(yaml.safe_dump(spec), encoding="utf-8")
            themes, manual = tagging.load_themes(path)
        self.assertEqual(manual, {})
        self.assertEqual(tagging.themes_for("Obby", "gain speed fast", themes), [])  # names only by default
        self.assertEqual(tagging.themes_for("Speed Race", "", themes), ["speed"])
        self.assertEqual(tagging.themes_for("Hunt", "hatch an egg", themes), ["egg"])  # description opted in
        self.assertEqual(tagging.themes_for("Hunt", "find the easter egg", themes), [])
        self.assertEqual(tagging.themes_for("🪵 Chop A Forest [CH2]", "", themes), ["verb-a"])

    def test_bad_regex(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "themes.yaml"
            path.write_text("themes:\n  broken:\n    regex: ['(']\n", encoding="utf-8")
            with self.assertRaises(tagging.ThemeFileError):
                tagging.load_themes(path)

    def test_bad_theme_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "themes.yaml"
            path.write_text("themes:\n  broken: {}\n", encoding="utf-8")
            with self.assertRaises(tagging.ThemeFileError):
                tagging.load_themes(path)


class AnalysisWithHistory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn, themes = build_db()
        cls.a = analysis.analyze(cls.conn, themes)

    def test_history(self):
        self.assertEqual(len(self.a.history.runs), 9)
        self.assertEqual(len(self.a.history.days), 9)

    def test_risers(self):
        r1, r7 = self.a.risers_1d, self.a.risers_7d
        self.assertEqual(r1.baseline.taken_at, LATEST - timedelta(days=1))
        self.assertEqual(r1.rows[0].game.universe_id, 1)
        self.assertAlmostEqual(r1.rows[0].pct, 12.5)
        self.assertEqual(r7.rows[0].game.universe_id, 1)
        self.assertAlmostEqual(r7.rows[0].pct, 350.0)
        self.assertNotIn(5, [c.game.universe_id for c in r1.rows])  # under the player floor
        self.assertIn(2, [g.universe_id for g in r7.entered])  # absent 7 days ago

    def test_breakouts_and_waves(self):
        self.assertEqual([g.universe_id for g in self.a.breakouts], [1, 2, 4])  # Roblox-run game 6 left out
        steal = [w for w in self.a.waves if w.theme == "steal"]
        self.assertEqual(len(steal), 1)
        self.assertEqual(sorted(g.universe_id for g in steal[0].games), [1, 2, 4])

    def test_official_games_flagged(self):
        hub = next(g for g in self.a.games if g.universe_id == 6)
        self.assertTrue(hub.official)
        self.assertIn("_(Roblox event)_", report.game_link(hub))

    def test_labels_and_names(self):
        fish = next(g for g in self.a.games if g.universe_id == 2)
        self.assertEqual(fish.name, "Steal a Fish")
        self.assertEqual(fish.labels, ["UPDATE"])
        self.assertIn("fish", fish.themes)

    def test_genre_share_change(self):
        sim = next(s for s in self.a.genres_l1 if s.genre == "Simulation")
        self.assertIsNotNone(sim.prev_share)
        self.assertGreater(sim.share, sim.prev_share)

    def test_report_renders(self):
        text = report.render(self.a)
        front = yaml.safe_load(text.split("---")[1])
        self.assertEqual(front["type"], "trends")
        self.assertEqual(front["snapshot-count"], 9)
        for heading in ("## Top 25", "## Risers — 1 day", "## New breakouts", "## Genre share", "## Themes",
                        "## Forming clone waves", "## Saturation estimate", "## What this means `(inferred)`", "## Sources"):
            self.assertIn(heading, text)
        self.assertIn("**steal**: 3 rising games", text)
        self.assertNotIn("Not enough history yet: needs a snapshot", text)

    def test_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            latest, dated = report.write(self.a, Path(tmp))
            self.assertEqual(latest.read_text(encoding="utf-8"), dated.read_text(encoding="utf-8"))
            self.assertEqual(dated.name, "2026-10-20.md")


class AnalysisSingleSnapshot(unittest.TestCase):
    def test_marks_missing_history(self):
        conn, themes = build_db(days=1)
        a = analysis.analyze(conn, themes)
        self.assertIsNone(a.risers_1d.baseline)
        self.assertIsNone(a.visit_growth.baseline)
        text = report.render(a)
        self.assertIn("Not enough history yet", text)
        self.assertIn("Single day of data", text)

    def test_empty_database(self):
        self.assertIsNone(analysis.analyze(db.connect(":memory:")))


if __name__ == "__main__":
    unittest.main()

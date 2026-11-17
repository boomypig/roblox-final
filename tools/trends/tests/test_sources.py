"""Parsers against trimmed real responses (captured 2026-10-22) and against broken shapes."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from trends.net import Client, FetchError
from trends.sources import explore, games, rolimons

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class ExploreParsing(unittest.TestCase):
    def test_get_sorts_page(self):
        sorts, token, problems = explore.parse_sorts_page(load("get_sorts.json"))
        self.assertEqual(problems, [])
        self.assertTrue(token)
        game_sorts = [s for s in sorts if s.holds_games]
        self.assertTrue(game_sorts)
        first = game_sorts[0].games[0]
        self.assertIsInstance(first.universe_id, int)
        self.assertEqual(first.rank, 1)
        self.assertIsInstance(first.player_count, int)

    def test_filters_sort_has_no_games(self):
        sorts, _, _ = explore.parse_sorts_page(load("get_sorts.json"))
        filters = [s for s in sorts if not s.holds_games]
        self.assertTrue(all(s.games == [] for s in filters))

    def test_get_sort_content(self):
        sort, problems = explore.parse_sort_content(load("get_sort_content.json"), "up-and-coming")
        self.assertEqual(problems, [])
        self.assertEqual(sort.sort_id, "up-and-coming")
        self.assertEqual(len(sort.games), 3)

    def test_bad_shapes_are_skipped_not_raised(self):
        payload = {
            "sorts": [
                "not a dict",
                {"contentType": "Games"},  # no sortId
                {"sortId": "x", "contentType": "Games", "games": [{"name": "no id"}, {"universeId": "42", "name": "ok"}]},
                {"sortId": "y", "contentType": "Games", "games": "oops"},
            ]
        }
        sorts, token, problems = explore.parse_sorts_page(payload)
        self.assertIsNone(token)
        self.assertEqual([s.sort_id for s in sorts], ["x", "y"])
        self.assertEqual([g.universe_id for g in sorts[0].games], [42])
        self.assertEqual(sorts[0].games[0].rank, 2)  # rank keeps its chart position
        self.assertEqual(len(problems), 4)

    def test_unexpected_top_level(self):
        sorts, token, problems = explore.parse_sorts_page({"error": "nope"})
        self.assertEqual((sorts, token), ([], None))
        self.assertTrue(problems)


class GamesParsing(unittest.TestCase):
    def test_details(self):
        details, problems = games.parse_details(load("games.json"))
        self.assertEqual(problems, [])
        d = details[0]
        self.assertIsInstance(d.playing, int)
        self.assertIsInstance(d.visits, int)
        self.assertTrue(d.created.startswith("20"))
        self.assertIsNotNone(d.genre_l1)
        self.assertIsNotNone(d.creator_name)

    def test_votes(self):
        votes, problems = games.parse_votes(load("votes.json"))
        self.assertEqual(problems, [])
        up, down = next(iter(votes.values()))
        self.assertIsInstance(up, int)
        self.assertIsInstance(down, int)

    def test_details_bad_rows(self):
        details, problems = games.parse_details({"data": [{"id": "abc"}, None, {"id": 7, "name": "Seven", "creator": "x"}]})
        self.assertEqual([d.universe_id for d in details], [7])
        self.assertIsNone(details[0].creator_name)
        self.assertEqual(len(problems), 2)

    def test_details_wrong_envelope(self):
        details, problems = games.parse_details([])
        self.assertEqual(details, [])
        self.assertTrue(problems)


class RolimonsParsing(unittest.TestCase):
    def test_gamelist(self):
        payload = {"success": True, "games": {"1818": ["Crossroads", 16, "url"], "x": ["Bad", 1], "5": ["No count"]}}
        rows, problems = rolimons.parse_gamelist(payload)
        self.assertEqual([(r.place_id, r.playing) for r in rows], [(1818, 16)])
        self.assertEqual(len(problems), 1)


class FakeResponse:
    def __init__(self, status: int, body=None, headers=None):
        self.status_code = status
        self._body = body
        self.headers = headers or {}
        self.text = json.dumps(body) if body is not None else "not json"

    def json(self):
        if self._body is None:
            raise ValueError("no json")
        return self._body


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.headers = {}
        self.calls = 0

    def get(self, url, params=None, timeout=None):
        self.calls += 1
        return self.responses.pop(0)


class ClientRetries(unittest.TestCase):
    def client(self, responses):
        self.sleeps: list[float] = []
        return Client(delay=0, max_retries=2, session=FakeSession(responses), sleep=self.sleeps.append)

    def test_retries_then_succeeds(self):
        c = self.client([FakeResponse(503, {}), FakeResponse(429, {}, {"Retry-After": "3"}), FakeResponse(200, {"ok": 1})])
        self.assertEqual(c.get_json("u"), {"ok": 1})
        self.assertEqual(c.requests_made, 3)
        self.assertIn(3.0, self.sleeps)  # Retry-After honored

    def test_gives_up(self):
        c = self.client([FakeResponse(500, {})] * 3)
        with self.assertRaises(FetchError):
            c.get_json("u")

    def test_client_error_is_not_retried(self):
        c = self.client([FakeResponse(400, {"errors": []}), FakeResponse(200, {})])
        with self.assertRaises(FetchError):
            c.get_json("u")
        self.assertEqual(c.requests_made, 1)

    def test_non_json_body(self):
        c = self.client([FakeResponse(200, None)])
        with self.assertRaises(FetchError):
            c.get_json("u")


if __name__ == "__main__":
    unittest.main()

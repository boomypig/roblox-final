"""`doctor`: check that every data source answers and still parses into the shape the tracker expects."""

from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass
from pathlib import Path

from . import config, db, tagging
from .net import Client, FetchError
from .sources import explore, games, rolimons

# Long-lived universes used as probes (Murder Mystery 2, Brookhaven RP); any public game works.
PROBE_UNIVERSE_IDS = [66654135, 1686885941]


@dataclass
class Check:
    name: str
    status: str  # PASS | WARN | FAIL | SKIP
    detail: str


def run_checks(client: Client, db_path: Path, use_rolimons: bool = config.USE_ROLIMONS) -> list[Check]:
    checks: list[Check] = []
    session_id = str(uuid.uuid4())

    try:
        payload = client.get_json(
            config.EXPLORE_SORTS_URL,
            {"sessionId": session_id, "device": config.EXPLORE_DEVICE, "country": config.EXPLORE_COUNTRY},
        )
        sorts, token, problems = explore.parse_sorts_page(payload)
        game_sorts = [s for s in sorts if s.holds_games]
        filled = sum(1 for s in game_sorts if s.games)
        if not game_sorts:
            checks.append(Check("explore get-sorts", "FAIL", "no game charts in the first page; " + "; ".join(problems[:3])))
        else:
            status = "WARN" if problems or filled == 0 else "PASS"
            detail = f"{len(sorts)} sorts on page 1 ({filled} with games), next page token: {'yes' if token else 'no'}"
            if problems:
                detail += f"; {len(problems)} parse problems, e.g. {problems[0]}"
            checks.append(Check("explore get-sorts", status, detail))
    except FetchError as exc:
        checks.append(Check("explore get-sorts", "FAIL", str(exc)))

    sort, problems = explore.fetch_sort_content(client, session_id, "top-playing-now")
    if sort is None or not sort.games:
        checks.append(Check("explore get-sort-content", "FAIL", "; ".join(problems[:3]) or "no games returned"))
    else:
        top = sort.games[0]
        checks.append(Check(
            "explore get-sort-content", "WARN" if problems else "PASS",
            f"top-playing-now: {len(sort.games)} games; #1 {top.name} ({top.player_count} players)",
        ))

    details, problems = games.fetch_details(client, PROBE_UNIVERSE_IDS)
    required = ("playing", "visits", "created", "genre_l1")
    incomplete = [d.name for d in details.values() if any(getattr(d, f) is None for f in required)]
    if len(details) != len(PROBE_UNIVERSE_IDS):
        checks.append(Check("games v1/games", "FAIL", f"{len(details)}/{len(PROBE_UNIVERSE_IDS)} games parsed; " + "; ".join(problems[:2])))
    elif incomplete:
        checks.append(Check("games v1/games", "WARN", f"missing {', '.join(required)} for: {', '.join(incomplete)}"))
    else:
        d = next(iter(details.values()))
        checks.append(Check("games v1/games", "PASS", f"{d.name}: {d.playing} playing, genre {d.genre_l1}/{d.genre_l2}"))

    votes, problems = games.fetch_votes(client, PROBE_UNIVERSE_IDS)
    if len(votes) != len(PROBE_UNIVERSE_IDS) or any(v[0] is None for v in votes.values()):
        checks.append(Check("games v1/games/votes", "FAIL", f"{len(votes)} parsed; " + "; ".join(problems[:2])))
    else:
        checks.append(Check("games v1/games/votes", "PASS", f"{len(votes)} games with up/down votes"))

    if use_rolimons:
        rows, problems = rolimons.fetch_gamelist(client)
        status = "PASS" if rows and not problems else ("WARN" if rows else "FAIL")
        checks.append(Check("rolimons gamelist", status, f"{len(rows)} games; " + "; ".join(problems[:2])))
    else:
        checks.append(Check("rolimons gamelist", "SKIP", "disabled (config.USE_ROLIMONS = False)"))

    try:
        themes, manual = tagging.load_themes()
        checks.append(Check("themes.yaml", "PASS", f"{len(themes)} themes, {len(manual)} manual entries"))
    except tagging.ThemeFileError as exc:
        checks.append(Check("themes.yaml", "FAIL", str(exc)))

    try:
        conn = db.connect(db_path)
        runs = conn.execute("SELECT COUNT(*) FROM runs WHERE status IN ('ok', 'partial')").fetchone()[0]
        conn.close()
        checks.append(Check("database", "PASS", f"{db_path} ({runs} usable runs)"))
    except sqlite3.Error as exc:
        checks.append(Check("database", "FAIL", f"{db_path}: {exc}"))
    return checks


def format_checks(checks: list[Check]) -> str:
    width = max(len(c.name) for c in checks)
    return "\n".join(f"{c.status:<4}  {c.name:<{width}}  {c.detail}" for c in checks)

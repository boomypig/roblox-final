"""`collect`: one snapshot of every chart plus details and votes for each charted game."""

from __future__ import annotations

import logging
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from . import config, db, tagging
from .net import Client
from .sources import explore, games, rolimons

log = logging.getLogger(__name__)


@dataclass
class CollectResult:
    run_id: int
    status: str
    sorts: int
    games: int
    requests: int
    problems: list[str] = field(default_factory=list)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def collect(conn: sqlite3.Connection, client: Client, use_rolimons: bool = config.USE_ROLIMONS) -> CollectResult:
    taken_at = utc_now()
    run_id = db.start_run(conn, taken_at)
    problems: list[str] = []

    sorts, sort_problems = explore.fetch_all_sorts(client, str(uuid.uuid4()))
    problems += sort_problems
    game_sorts = [s for s in sorts if s.holds_games and s.games]
    chart_rows: dict[int, explore.ChartGame] = {}
    for sort in game_sorts:
        for game in sort.games:
            chart_rows.setdefault(game.universe_id, game)
    log.info("charts: %d sorts, %d unique games", len(game_sorts), len(chart_rows))

    if not chart_rows:
        problems.append("no games collected from any chart")
        db.finish_run(conn, run_id, utc_now(), "failed", len(game_sorts), 0, client.requests_made, problems)
        return CollectResult(run_id, "failed", len(game_sorts), 0, client.requests_made, problems)

    ids = list(chart_rows)
    details, detail_problems = games.fetch_details(client, ids)
    votes, vote_problems = games.fetch_votes(client, ids)
    problems += detail_problems + vote_problems
    missing = len(ids) - len(details)
    if missing:
        problems.append(f"{missing} games have no details; their chart player counts are stored instead")

    with conn:
        for sort in game_sorts:
            db.upsert_sort(conn, sort.sort_id, sort.display_name, taken_at)
        for uid, chart in chart_rows.items():
            detail = details.get(uid)
            up, down = votes.get(uid, (chart.up_votes, chart.down_votes))
            db.upsert_game(conn, _game_row(chart, detail), taken_at)
            db.insert_snapshot(
                conn,
                run_id,
                taken_at,
                {
                    "universe_id": uid,
                    "name": detail.name if detail else chart.name,
                    "playing": detail.playing if detail and detail.playing is not None else chart.player_count,
                    "visits": detail.visits if detail else None,
                    "favorites": detail.favorites if detail else None,
                    "up_votes": up,
                    "down_votes": down,
                },
            )
        for sort in game_sorts:
            for game in sort.games:
                db.insert_placement(conn, run_id, game.universe_id, sort.sort_id, game.rank, game.is_sponsored)

    if use_rolimons:
        rows, rol_problems = rolimons.fetch_gamelist(client)
        problems += rol_problems
        with conn:
            conn.executemany(
                "INSERT OR REPLACE INTO rolimons_counts (run_id, place_id, name, playing) VALUES (?, ?, ?, ?)",
                [(run_id, g.place_id, g.name, g.playing) for g in rows],
            )

    try:
        themes, manual = tagging.load_themes()
        tagging.retag_all(conn, themes, manual)
    except tagging.ThemeFileError as exc:
        problems.append(f"themes.yaml: {exc}")

    status = "partial" if problems else "ok"
    db.finish_run(conn, run_id, utc_now(), status, len(game_sorts), len(chart_rows), client.requests_made, problems)
    for p in problems:
        log.warning(p)
    return CollectResult(run_id, status, len(game_sorts), len(chart_rows), client.requests_made, problems)


def _game_row(chart: explore.ChartGame, detail: games.GameDetail | None) -> dict:
    if detail is None:
        return {
            "universe_id": chart.universe_id,
            "name": chart.name,
            "root_place_id": chart.root_place_id,
            "genre_l1": chart.genre_l1,
        }
    return {
        "universe_id": detail.universe_id,
        "name": detail.name,
        "root_place_id": detail.root_place_id or chart.root_place_id,
        "description": detail.description,
        "creator_id": detail.creator_id,
        "creator_name": detail.creator_name,
        "creator_type": detail.creator_type,
        "created": detail.created,
        "updated": detail.updated,
        "genre_l1": detail.genre_l1 or chart.genre_l1,
        "genre_l2": detail.genre_l2,
        "max_players": detail.max_players,
    }

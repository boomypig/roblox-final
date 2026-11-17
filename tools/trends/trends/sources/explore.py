"""Charts from the explore API: get-sorts (every chart, paged) and get-sort-content (one chart)."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from .. import config
from ..net import Client, FetchError
from .common import to_bool, to_int, to_str

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ChartGame:
    universe_id: int
    rank: int  # 1-based position in the chart, sponsored slots included
    name: str
    root_place_id: int | None = None
    player_count: int | None = None
    up_votes: int | None = None
    down_votes: int | None = None
    is_sponsored: bool = False
    genre_l1: str | None = None
    content_maturity: str | None = None


@dataclass
class Sort:
    sort_id: str
    display_name: str
    content_type: str
    games: list[ChartGame] = field(default_factory=list)

    @property
    def holds_games(self) -> bool:
        return self.content_type.lower() == "games"


def parse_chart_game(raw: Any, rank: int) -> ChartGame | None:
    if not isinstance(raw, dict):
        return None
    universe_id = to_int(raw.get("universeId"))
    if universe_id is None:
        return None
    return ChartGame(
        universe_id=universe_id,
        rank=rank,
        name=to_str(raw.get("name")) or f"universe {universe_id}",
        root_place_id=to_int(raw.get("rootPlaceId")),
        player_count=to_int(raw.get("playerCount")),
        up_votes=to_int(raw.get("totalUpVotes")),
        down_votes=to_int(raw.get("totalDownVotes")),
        is_sponsored=to_bool(raw.get("isSponsored")),
        genre_l1=to_str(raw.get("genreL1")),
        content_maturity=to_str(raw.get("contentMaturity")),
    )


def parse_sort(raw: Any, problems: list[str]) -> Sort | None:
    if not isinstance(raw, dict):
        problems.append("get-sorts: skipped a sort that isn't an object")
        return None
    sort_id = to_str(raw.get("sortId")) or to_str(raw.get("id"))
    if sort_id is None:
        problems.append("get-sorts: skipped a sort with no sortId")
        return None
    sort = Sort(
        sort_id=sort_id,
        display_name=to_str(raw.get("sortDisplayName")) or sort_id,
        content_type=to_str(raw.get("contentType")) or "",
    )
    if sort.holds_games:
        sort.games = _parse_games_list(raw.get("games"), sort_id, problems)
    return sort


def parse_sorts_page(payload: Any) -> tuple[list[Sort], str | None, list[str]]:
    problems: list[str] = []
    if not isinstance(payload, dict) or not isinstance(payload.get("sorts"), list):
        return [], None, ["get-sorts: response has no 'sorts' list"]
    sorts = [s for s in (parse_sort(raw, problems) for raw in payload["sorts"]) if s is not None]
    return sorts, to_str(payload.get("nextSortsPageToken")), problems


def parse_sort_content(payload: Any, sort_id: str) -> tuple[Sort | None, list[str]]:
    problems: list[str] = []
    if not isinstance(payload, dict):
        return None, [f"get-sort-content {sort_id}: response isn't an object"]
    sort = Sort(
        sort_id=to_str(payload.get("sortId")) or sort_id,
        display_name=to_str(payload.get("sortDisplayName")) or sort_id,
        content_type=to_str(payload.get("contentType")) or "Games",
    )
    sort.games = _parse_games_list(payload.get("games"), sort_id, problems)
    return sort, problems


def _parse_games_list(raw_games: Any, sort_id: str, problems: list[str]) -> list[ChartGame]:
    if raw_games is None:
        return []
    if not isinstance(raw_games, list):
        problems.append(f"{sort_id}: 'games' isn't a list")
        return []
    games = []
    for rank, raw in enumerate(raw_games, start=1):
        game = parse_chart_game(raw, rank)
        if game is None:
            problems.append(f"{sort_id}: skipped rank {rank} (unexpected shape)")
        else:
            games.append(game)
    return games


def fetch_all_sorts(client: Client, session_id: str) -> tuple[list[Sort], list[str]]:
    """Every chart from get-sorts, following page tokens; empty game charts are filled from get-sort-content."""
    sorts: list[Sort] = []
    problems: list[str] = []
    token: str | None = None
    for page in range(config.MAX_SORT_PAGES):
        params = {"sessionId": session_id, "device": config.EXPLORE_DEVICE, "country": config.EXPLORE_COUNTRY}
        if token:
            params["sortsPageToken"] = token
        try:
            payload = client.get_json(config.EXPLORE_SORTS_URL, params)
        except FetchError as exc:
            problems.append(f"get-sorts page {page + 1}: {exc}")
            break
        page_sorts, token, page_problems = parse_sorts_page(payload)
        sorts.extend(page_sorts)
        problems.extend(page_problems)
        if not token:
            break
    else:
        problems.append(f"get-sorts: stopped after {config.MAX_SORT_PAGES} pages; raise MAX_SORT_PAGES if charts are missing")

    for i, sort in enumerate(sorts):
        if sort.holds_games and not sort.games:
            filled, fill_problems = fetch_sort_content(client, session_id, sort.sort_id)
            problems.extend(fill_problems)
            if filled is not None and filled.games:
                sorts[i] = filled
    return sorts, problems


def fetch_sort_content(client: Client, session_id: str, sort_id: str) -> tuple[Sort | None, list[str]]:
    try:
        payload = client.get_json(config.EXPLORE_SORT_CONTENT_URL, {"sessionId": session_id, "sortId": sort_id})
    except FetchError as exc:
        return None, [f"get-sort-content {sort_id}: {exc}"]
    return parse_sort_content(payload, sort_id)

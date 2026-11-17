"""Game details and votes from games.roblox.com, batched."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .. import config
from ..net import Client, FetchError
from .common import chunks, to_int, to_str


@dataclass(frozen=True)
class GameDetail:
    universe_id: int
    name: str
    root_place_id: int | None = None
    description: str = ""
    creator_id: int | None = None
    creator_name: str | None = None
    creator_type: str | None = None
    created: str | None = None
    updated: str | None = None
    playing: int | None = None
    visits: int | None = None
    favorites: int | None = None
    max_players: int | None = None
    genre_l1: str | None = None
    genre_l2: str | None = None


def parse_detail(raw: Any) -> GameDetail | None:
    if not isinstance(raw, dict):
        return None
    universe_id = to_int(raw.get("id"))
    if universe_id is None:
        return None
    creator = raw.get("creator") if isinstance(raw.get("creator"), dict) else {}
    return GameDetail(
        universe_id=universe_id,
        name=to_str(raw.get("name")) or f"universe {universe_id}",
        root_place_id=to_int(raw.get("rootPlaceId")),
        description=raw.get("description") if isinstance(raw.get("description"), str) else "",
        creator_id=to_int(creator.get("id")),
        creator_name=to_str(creator.get("name")),
        creator_type=to_str(creator.get("type")),
        created=to_str(raw.get("created")),
        updated=to_str(raw.get("updated")),
        playing=to_int(raw.get("playing")),
        visits=to_int(raw.get("visits")),
        favorites=to_int(raw.get("favoritedCount")),
        max_players=to_int(raw.get("maxPlayers")),
        genre_l1=to_str(raw.get("genre_l1")),
        genre_l2=to_str(raw.get("genre_l2")),
    )


def parse_details(payload: Any) -> tuple[list[GameDetail], list[str]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        return [], ["v1/games: response has no 'data' list"]
    details, problems = [], []
    for raw in payload["data"]:
        detail = parse_detail(raw)
        if detail is None:
            problems.append("v1/games: skipped an entry with an unexpected shape")
        else:
            details.append(detail)
    return details, problems


def parse_votes(payload: Any) -> tuple[dict[int, tuple[int | None, int | None]], list[str]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        return {}, ["v1/games/votes: response has no 'data' list"]
    votes, problems = {}, []
    for raw in payload["data"]:
        universe_id = to_int(raw.get("id")) if isinstance(raw, dict) else None
        if universe_id is None:
            problems.append("v1/games/votes: skipped an entry with an unexpected shape")
            continue
        votes[universe_id] = (to_int(raw.get("upVotes")), to_int(raw.get("downVotes")))
    return votes, problems


def fetch_details(client: Client, universe_ids: list[int]) -> tuple[dict[int, GameDetail], list[str]]:
    details: dict[int, GameDetail] = {}
    problems: list[str] = []
    for batch in chunks(universe_ids, config.GAMES_BATCH_SIZE):
        try:
            payload = client.get_json(config.GAMES_URL, {"universeIds": ",".join(map(str, batch))})
        except FetchError as exc:
            problems.append(f"v1/games batch of {len(batch)}: {exc}")
            continue
        parsed, batch_problems = parse_details(payload)
        problems.extend(batch_problems)
        details.update({d.universe_id: d for d in parsed})
    return details, problems


def fetch_votes(client: Client, universe_ids: list[int]) -> tuple[dict[int, tuple[int | None, int | None]], list[str]]:
    votes: dict[int, tuple[int | None, int | None]] = {}
    problems: list[str] = []
    for batch in chunks(universe_ids, config.VOTES_BATCH_SIZE):
        try:
            payload = client.get_json(config.VOTES_URL, {"universeIds": ",".join(map(str, batch))})
        except FetchError as exc:
            problems.append(f"v1/games/votes batch of {len(batch)}: {exc}")
            continue
        parsed, batch_problems = parse_votes(payload)
        problems.extend(batch_problems)
        votes.update(parsed)
    return votes, problems

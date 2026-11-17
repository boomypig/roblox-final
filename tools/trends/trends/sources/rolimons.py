"""Rolimons game list (third-party): ~7–8K games with live player counts. Off unless config.USE_ROLIMONS."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .. import config
from ..net import Client, FetchError
from .common import to_int, to_str


@dataclass(frozen=True)
class RolimonsGame:
    place_id: int
    name: str
    playing: int


def parse_gamelist(payload: Any) -> tuple[list[RolimonsGame], list[str]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("games"), dict):
        return [], ["rolimons: response has no 'games' object"]
    games, skipped = [], 0
    for key, row in payload["games"].items():
        place_id = to_int(key)
        if place_id is None or not isinstance(row, list) or len(row) < 2:
            skipped += 1
            continue
        name, playing = to_str(row[0]), to_int(row[1])
        if name is None or playing is None:
            skipped += 1
            continue
        games.append(RolimonsGame(place_id, name, playing))
    problems = [f"rolimons: skipped {skipped} rows with an unexpected shape"] if skipped else []
    return games, problems


def fetch_gamelist(client: Client) -> tuple[list[RolimonsGame], list[str]]:
    try:
        payload = client.get_json(config.ROLIMONS_GAMELIST_URL)
    except FetchError as exc:
        return [], [f"rolimons: {exc}"]
    return parse_gamelist(payload)

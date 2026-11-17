"""SQLite storage. Schema changes go in MIGRATIONS; PRAGMA user_version tracks which have run."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

MIGRATIONS: dict[int, str] = {
    1: """
    CREATE TABLE runs (
        id INTEGER PRIMARY KEY,
        started_at TEXT NOT NULL,          -- UTC, ISO 8601 with Z
        finished_at TEXT,
        status TEXT NOT NULL DEFAULT 'running',  -- running | ok | partial | failed
        sorts_seen INTEGER,
        games_seen INTEGER,
        requests_made INTEGER,
        problems TEXT                      -- JSON list of strings
    );
    CREATE TABLE games (
        universe_id INTEGER PRIMARY KEY,
        root_place_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        creator_id INTEGER,
        creator_name TEXT,
        creator_type TEXT,
        created TEXT,
        updated TEXT,
        genre_l1 TEXT,
        genre_l2 TEXT,
        max_players INTEGER,
        first_seen TEXT NOT NULL,
        last_seen TEXT NOT NULL
    );
    -- One row per game per run. Placements hold chart ranks, so stats aren't repeated per chart.
    CREATE TABLE snapshots (
        run_id INTEGER NOT NULL REFERENCES runs(id),
        universe_id INTEGER NOT NULL REFERENCES games(universe_id),
        taken_at TEXT NOT NULL,
        name TEXT,                         -- names change with [UPDATE]/[EVENT] tags
        playing INTEGER,
        visits INTEGER,
        favorites INTEGER,
        up_votes INTEGER,
        down_votes INTEGER,
        PRIMARY KEY (run_id, universe_id)
    );
    CREATE TABLE placements (
        run_id INTEGER NOT NULL REFERENCES runs(id),
        universe_id INTEGER NOT NULL,
        sort_id TEXT NOT NULL,
        rank INTEGER NOT NULL,
        is_sponsored INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (run_id, sort_id, universe_id)
    );
    CREATE TABLE sorts (
        sort_id TEXT PRIMARY KEY,
        display_name TEXT,
        first_seen TEXT NOT NULL,
        last_seen TEXT NOT NULL
    );
    CREATE TABLE tags (
        universe_id INTEGER NOT NULL,
        tag TEXT NOT NULL,
        source TEXT NOT NULL CHECK (source IN ('keyword', 'roblox-genre', 'manual')),
        PRIMARY KEY (universe_id, tag, source)
    );
    CREATE TABLE rolimons_counts (
        run_id INTEGER NOT NULL REFERENCES runs(id),
        place_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        playing INTEGER NOT NULL,
        PRIMARY KEY (run_id, place_id)
    );
    CREATE INDEX snapshots_by_game ON snapshots (universe_id, taken_at);
    CREATE INDEX placements_by_sort ON placements (sort_id, run_id);
    -- The flat shape from the original spec: one row per chart appearance.
    CREATE VIEW snapshot_rows AS
        SELECT s.taken_at, s.universe_id, p.sort_id, p.rank, s.playing, s.visits, s.up_votes, s.down_votes
        FROM snapshots s LEFT JOIN placements p ON p.run_id = s.run_id AND p.universe_id = s.universe_id;
    """,
}


def connect(path: Path | str) -> sqlite3.Connection:
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    migrate(conn)
    return conn


def migrate(conn: sqlite3.Connection) -> None:
    current = conn.execute("PRAGMA user_version").fetchone()[0]
    for version in sorted(v for v in MIGRATIONS if v > current):
        with conn:
            conn.executescript(MIGRATIONS[version])
            conn.execute(f"PRAGMA user_version = {version}")


def start_run(conn: sqlite3.Connection, started_at: str) -> int:
    with conn:
        cur = conn.execute("INSERT INTO runs (started_at) VALUES (?)", (started_at,))
    return int(cur.lastrowid)


def finish_run(
    conn: sqlite3.Connection,
    run_id: int,
    finished_at: str,
    status: str,
    sorts_seen: int,
    games_seen: int,
    requests_made: int,
    problems: list[str],
) -> None:
    with conn:
        conn.execute(
            "UPDATE runs SET finished_at=?, status=?, sorts_seen=?, games_seen=?, requests_made=?, problems=? WHERE id=?",
            (finished_at, status, sorts_seen, games_seen, requests_made, json.dumps(problems), run_id),
        )


def upsert_game(conn: sqlite3.Connection, row: dict, seen_at: str) -> None:
    """row keys: universe_id, name, and any of the optional game columns. Missing values keep old ones."""
    conn.execute(
        """
        INSERT INTO games (universe_id, root_place_id, name, description, creator_id, creator_name, creator_type,
                           created, updated, genre_l1, genre_l2, max_players, first_seen, last_seen)
        VALUES (:universe_id, :root_place_id, :name, :description, :creator_id, :creator_name, :creator_type,
                :created, :updated, :genre_l1, :genre_l2, :max_players, :seen_at, :seen_at)
        ON CONFLICT (universe_id) DO UPDATE SET
            root_place_id = COALESCE(excluded.root_place_id, root_place_id),
            name = excluded.name,
            description = COALESCE(excluded.description, description),
            creator_id = COALESCE(excluded.creator_id, creator_id),
            creator_name = COALESCE(excluded.creator_name, creator_name),
            creator_type = COALESCE(excluded.creator_type, creator_type),
            created = COALESCE(excluded.created, created),
            updated = COALESCE(excluded.updated, updated),
            genre_l1 = COALESCE(excluded.genre_l1, genre_l1),
            genre_l2 = COALESCE(excluded.genre_l2, genre_l2),
            max_players = COALESCE(excluded.max_players, max_players),
            last_seen = excluded.last_seen
        """,
        {
            "root_place_id": None,
            "description": None,
            "creator_id": None,
            "creator_name": None,
            "creator_type": None,
            "created": None,
            "updated": None,
            "genre_l1": None,
            "genre_l2": None,
            "max_players": None,
            **row,
            "seen_at": seen_at,
        },
    )


def insert_snapshot(conn: sqlite3.Connection, run_id: int, taken_at: str, row: dict) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO snapshots
            (run_id, universe_id, taken_at, name, playing, visits, favorites, up_votes, down_votes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            row["universe_id"],
            taken_at,
            row.get("name"),
            row.get("playing"),
            row.get("visits"),
            row.get("favorites"),
            row.get("up_votes"),
            row.get("down_votes"),
        ),
    )


def insert_placement(conn: sqlite3.Connection, run_id: int, universe_id: int, sort_id: str, rank: int, sponsored: bool) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO placements (run_id, universe_id, sort_id, rank, is_sponsored) VALUES (?, ?, ?, ?, ?)",
        (run_id, universe_id, sort_id, rank, int(sponsored)),
    )


def upsert_sort(conn: sqlite3.Connection, sort_id: str, display_name: str, seen_at: str) -> None:
    conn.execute(
        """
        INSERT INTO sorts (sort_id, display_name, first_seen, last_seen) VALUES (?, ?, ?, ?)
        ON CONFLICT (sort_id) DO UPDATE SET display_name = excluded.display_name, last_seen = excluded.last_seen
        """,
        (sort_id, display_name, seen_at, seen_at),
    )


def replace_tags(conn: sqlite3.Connection, source: str, rows: list[tuple[int, str]]) -> None:
    """Rewrite every tag from one source, so edits to themes.yaml apply to old games too."""
    with conn:
        conn.execute("DELETE FROM tags WHERE source = ?", (source,))
        conn.executemany(
            "INSERT OR IGNORE INTO tags (universe_id, tag, source) VALUES (?, ?, ?)",
            [(uid, tag, source) for uid, tag in rows],
        )

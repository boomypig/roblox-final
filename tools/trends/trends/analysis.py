"""Turns stored snapshots into the numbers the report shows. No I/O besides reading the database."""

from __future__ import annotations

import sqlite3
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from . import config, tagging


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


@dataclass(frozen=True)
class Run:
    id: int
    taken_at: datetime


@dataclass
class History:
    runs: list[Run]

    @property
    def latest(self) -> Run | None:
        return self.runs[-1] if self.runs else None

    @property
    def days(self) -> list[str]:
        return sorted({r.taken_at.date().isoformat() for r in self.runs})

    @property
    def span_hours(self) -> float:
        if len(self.runs) < 2:
            return 0.0
        return (self.runs[-1].taken_at - self.runs[0].taken_at).total_seconds() / 3600

    def run_near(self, target: datetime, tolerance_hours: float) -> Run | None:
        candidates = [r for r in self.runs[:-1] if abs((r.taken_at - target).total_seconds()) <= tolerance_hours * 3600]
        return min(candidates, key=lambda r: abs((r.taken_at - target).total_seconds()), default=None)


@dataclass
class GameRow:
    universe_id: int
    name: str  # display name with [UPDATE]-style labels stripped
    labels: list[str]
    root_place_id: int | None
    playing: int
    visits: int | None
    favorites: int | None
    up_votes: int | None
    down_votes: int | None
    genre_l1: str | None
    genre_l2: str | None
    created: datetime | None
    updated: datetime | None
    themes: list[str] = field(default_factory=list)
    sorts: dict[str, int] = field(default_factory=dict)
    creator_name: str | None = None

    @property
    def official(self) -> bool:
        return self.creator_name in config.OFFICIAL_CREATORS

    @property
    def like_pct(self) -> float | None:
        if self.up_votes is None or self.down_votes is None or self.up_votes + self.down_votes == 0:
            return None
        return 100 * self.up_votes / (self.up_votes + self.down_votes)

    def age_days(self, now: datetime) -> int | None:
        return (now - self.created).days if self.created else None


@dataclass
class Change:
    game: GameRow
    before: int
    after: int

    @property
    def delta(self) -> int:
        return self.after - self.before

    @property
    def pct(self) -> float:
        return 100 * (self.after - self.before) / self.before


@dataclass
class Risers:
    label: str
    baseline: Run | None
    rows: list[Change]
    entered: list[GameRow]  # above the floor now, absent from the baseline snapshot
    note: str | None = None


@dataclass
class VisitGrowth:
    game: GameRow
    per_day: float
    pct_per_day: float


@dataclass
class VisitGrowthResult:
    baseline: Run | None
    rows: list[VisitGrowth]
    note: str | None = None


@dataclass
class GenreShare:
    genre: str
    players: int
    share: float
    games: int
    prev_share: float | None = None


@dataclass
class ThemeStat:
    theme: str
    games: int
    players: int
    per_game: float
    median: float
    top_game: str
    top_share: float
    in_top100: int
    rising: int
    prev_players: int | None = None
    all_games: int | None = None  # from Rolimons, when enabled
    all_players: int | None = None
    saturation: str = ""

    @property
    def change_pct(self) -> float | None:
        if not self.prev_players:
            return None
        return 100 * (self.players - self.prev_players) / self.prev_players


@dataclass
class Wave:
    theme: str
    games: list[GameRow]
    newest: datetime | None
    oldest: datetime | None

    @property
    def players(self) -> int:
        return sum(g.playing for g in self.games)


@dataclass
class Analysis:
    history: History
    now: datetime
    games: list[GameRow]  # latest run, sorted by players
    sorts_seen: list[str]
    top: list[GameRow]
    risers_1d: Risers
    risers_7d: Risers
    visit_growth: VisitGrowthResult
    breakouts: list[GameRow]
    genres_l1: list[GenreShare]
    genres_l2: list[GenreShare]
    genre_baseline: Run | None
    themes: list[ThemeStat]
    theme_baseline: Run | None
    waves: list[Wave]
    labelled: list[GameRow]
    rolimons_used: bool
    sources: list[str]


def load_history(conn: sqlite3.Connection) -> History:
    rows = conn.execute(
        """
        SELECT r.id, r.started_at FROM runs r
        WHERE r.status IN ('ok', 'partial') AND EXISTS (SELECT 1 FROM snapshots s WHERE s.run_id = r.id)
        ORDER BY r.started_at
        """
    ).fetchall()
    return History([Run(r["id"], parse_time(r["started_at"])) for r in rows if parse_time(r["started_at"])])


def load_games(conn: sqlite3.Connection, run_id: int) -> list[GameRow]:
    themes: dict[int, set[str]] = defaultdict(set)
    for r in conn.execute("SELECT universe_id, tag FROM tags WHERE source IN ('keyword', 'manual')"):
        themes[r["universe_id"]].add(r["tag"])
    sorts: dict[int, dict[str, int]] = defaultdict(dict)
    for r in conn.execute("SELECT universe_id, sort_id, rank FROM placements WHERE run_id = ? AND is_sponsored = 0", (run_id,)):
        sorts[r["universe_id"]][r["sort_id"]] = r["rank"]
    rows = conn.execute(
        """
        SELECT s.universe_id, COALESCE(s.name, g.name) AS name, s.playing, s.visits, s.favorites, s.up_votes,
               s.down_votes, g.root_place_id, g.genre_l1, g.genre_l2, g.created, g.updated, g.creator_name
        FROM snapshots s JOIN games g ON g.universe_id = s.universe_id
        WHERE s.run_id = ? AND s.playing IS NOT NULL
        """,
        (run_id,),
    ).fetchall()
    games = []
    for r in rows:
        clean, labels = tagging.split_name(r["name"])
        games.append(
            GameRow(
                universe_id=r["universe_id"],
                name=clean,
                labels=labels,
                root_place_id=r["root_place_id"],
                playing=r["playing"],
                visits=r["visits"],
                favorites=r["favorites"],
                up_votes=r["up_votes"],
                down_votes=r["down_votes"],
                genre_l1=r["genre_l1"],
                genre_l2=r["genre_l2"],
                created=parse_time(r["created"]),
                updated=parse_time(r["updated"]),
                themes=sorted(themes.get(r["universe_id"], ())),
                sorts=sorts.get(r["universe_id"], {}),
                creator_name=r["creator_name"],
            )
        )
    return sorted(games, key=lambda g: g.playing, reverse=True)


def risers(conn: sqlite3.Connection, history: History, now_games: list[GameRow], hours: float, label: str) -> Risers:
    latest = history.latest
    baseline = history.run_near(latest.taken_at - timedelta(hours=hours), config.RISER_TOLERANCE_HOURS) if latest else None
    if baseline is None:
        days = hours / 24
        return Risers(
            label, None, [], [],
            note=f"Not enough history yet: needs a snapshot from about {days:g} day{'s' if days != 1 else ''} "
            f"(±{config.RISER_TOLERANCE_HOURS:g} h) before the latest one.",
        )
    before = {r["universe_id"]: r["playing"] for r in conn.execute(
        "SELECT universe_id, playing FROM snapshots WHERE run_id = ? AND playing IS NOT NULL", (baseline.id,))}
    eligible = [g for g in now_games if g.playing >= config.RISER_MIN_PLAYERS]
    changes = [Change(g, before[g.universe_id], g.playing) for g in eligible if before.get(g.universe_id, 0) > 0]
    changes.sort(key=lambda c: c.pct, reverse=True)
    entered = [g for g in eligible if g.universe_id not in before][:10]
    return Risers(label, baseline, changes[: config.RISERS_SHOWN], entered)


def visit_growth(conn: sqlite3.Connection, history: History, now_games: list[GameRow]) -> VisitGrowthResult:
    latest = history.latest
    if latest is None:
        return VisitGrowthResult(None, [], "No snapshots yet.")
    baseline = history.run_near(latest.taken_at - timedelta(hours=24), config.RISER_TOLERANCE_HOURS)
    if baseline is None:
        older = [r for r in history.runs[:-1]
                 if (latest.taken_at - r.taken_at).total_seconds() >= config.VISIT_GROWTH_MIN_HOURS * 3600]
        baseline = older[-1] if older else None
    if baseline is None:
        return VisitGrowthResult(
            None, [], f"Not enough history yet: needs two snapshots at least {config.VISIT_GROWTH_MIN_HOURS:g} h apart."
        )
    hours = (latest.taken_at - baseline.taken_at).total_seconds() / 3600
    before = {r["universe_id"]: r["visits"] for r in conn.execute(
        "SELECT universe_id, visits FROM snapshots WHERE run_id = ? AND visits IS NOT NULL", (baseline.id,))}
    rows = []
    for g in now_games:
        then = before.get(g.universe_id)
        if g.visits is None or not then or g.visits < then:
            continue
        per_day = (g.visits - then) * 24 / hours
        rows.append(VisitGrowth(g, per_day, 100 * per_day / then))
    rows.sort(key=lambda v: v.per_day, reverse=True)
    return VisitGrowthResult(baseline, rows[:15])


def breakouts(now_games: list[GameRow], now: datetime) -> list[GameRow]:
    found = [
        g for g in now_games
        if not g.official and g.created and (now - g.created).days <= config.BREAKOUT_MAX_AGE_DAYS
        and g.playing >= config.BREAKOUT_MIN_PLAYERS
    ]
    return found[:20]


def genre_share(now_games: list[GameRow], base_games: list[GameRow] | None, level: str) -> list[GenreShare]:
    def totals(games: list[GameRow]) -> tuple[dict[str, int], dict[str, int], int]:
        players: dict[str, int] = defaultdict(int)
        counts: dict[str, int] = defaultdict(int)
        for g in games:
            key = (g.genre_l1 if level == "l1" else g.genre_l2) or "Unknown"
            players[key] += g.playing
            counts[key] += 1
        return players, counts, sum(players.values()) or 1

    players, counts, total = totals(now_games)
    prev = None
    if base_games is not None:
        base_players, _, base_total = totals(base_games)
        prev = {k: 100 * v / base_total for k, v in base_players.items()}
    shares = [
        GenreShare(k, v, 100 * v / total, counts[k], (prev.get(k, 0.0) if prev is not None else None))
        for k, v in players.items()
    ]
    return sorted(shares, key=lambda s: s.players, reverse=True)


def theme_stats(
    now_games: list[GameRow], base_games: list[GameRow] | None, rising_ids: set[int],
    rolimons: dict[str, tuple[int, int]] | None,
) -> list[ThemeStat]:
    by_theme: dict[str, list[GameRow]] = defaultdict(list)
    for g in now_games:
        for t in g.themes:
            by_theme[t].append(g)
    base_players: dict[str, int] = defaultdict(int)
    for g in base_games or []:
        for t in g.themes:
            base_players[t] += g.playing
    top100 = {g.universe_id for g in now_games[:100]}
    stats = []
    for theme, games in by_theme.items():
        players = sum(g.playing for g in games)
        leader = max(games, key=lambda g: g.playing)
        stat = ThemeStat(
            theme=theme,
            games=len(games),
            players=players,
            per_game=players / len(games),
            median=statistics.median(g.playing for g in games),
            top_game=leader.name,
            top_share=100 * leader.playing / players if players else 0.0,
            in_top100=sum(g.universe_id in top100 for g in games),
            rising=sum(g.universe_id in rising_ids for g in games),
            prev_players=base_players.get(theme) if base_games is not None else None,
        )
        if rolimons and theme in rolimons:
            stat.all_games, stat.all_players = rolimons[theme]
        stats.append(stat)
    _label_saturation(stats, now_games)
    return sorted(stats, key=lambda s: s.players, reverse=True)


def _label_saturation(stats: list[ThemeStat], now_games: list[GameRow]) -> None:
    """Rough labels (inferred). Charts only cover the top few hundred games, so 'crowded' undercounts the long tail."""
    if not stats or not now_games:
        return
    game_median = statistics.median(g.playing for g in now_games)
    per_game_median = statistics.median(s.per_game for s in stats)
    for s in stats:
        if s.games < 3:
            s.saturation = "too few games to judge"
        elif s.top_share >= 60:
            s.saturation = "one game dominates"
        elif s.games >= 15 and s.median <= game_median:
            s.saturation = "crowded"
        elif s.games <= 6 and s.per_game >= 2 * per_game_median:
            s.saturation = "few games, high demand"
        else:
            s.saturation = "mixed"


def rising_set(now_games: list[GameRow], risers_1d: Risers, risers_7d: Risers, found_breakouts: list[GameRow]) -> set[int]:
    ids = {g.universe_id for g in now_games if any(s in g.sorts for s in config.RISING_SORT_IDS)}
    ids |= {g.universe_id for g in found_breakouts}
    for r in (risers_1d, risers_7d):
        ids |= {c.game.universe_id for c in r.rows if c.pct >= 20}
    return ids


def clone_waves(now_games: list[GameRow], rising_ids: set[int]) -> list[Wave]:
    members: dict[str, list[GameRow]] = defaultdict(list)
    for g in now_games:
        if g.universe_id in rising_ids and not g.official:
            for t in g.themes:
                members[t].append(g)
    waves = []
    for theme, games in members.items():
        if len(games) >= config.CLONE_WAVE_MIN_GAMES:
            dates = [g.created for g in games if g.created]
            waves.append(Wave(theme, games, max(dates, default=None), min(dates, default=None)))
    return sorted(waves, key=lambda w: (len(w.games), w.players), reverse=True)


def rolimons_theme_counts(conn: sqlite3.Connection, run_id: int, themes: list[tagging.Theme]) -> dict[str, tuple[int, int]] | None:
    rows = conn.execute("SELECT name, playing FROM rolimons_counts WHERE run_id = ?", (run_id,)).fetchall()
    if not rows:
        return None
    counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for r in rows:
        for t in tagging.themes_for(r["name"], "", themes):
            counts[t][0] += 1
            counts[t][1] += r["playing"]
    return {k: (v[0], v[1]) for k, v in counts.items()}


def analyze(conn: sqlite3.Connection, themes: list[tagging.Theme] | None = None) -> Analysis | None:
    history = load_history(conn)
    latest = history.latest
    if latest is None:
        return None
    now = latest.taken_at
    now_games = load_games(conn, latest.id)
    sorts_seen = [r["sort_id"] for r in conn.execute(
        "SELECT DISTINCT sort_id FROM placements WHERE run_id = ? ORDER BY sort_id", (latest.id,))]

    r1 = risers(conn, history, now_games, 24, "1 day")
    r7 = risers(conn, history, now_games, 24 * 7, "7 days")
    found_breakouts = breakouts(now_games, now)
    rising_ids = rising_set(now_games, r1, r7, found_breakouts)

    # Genre and theme changes compare with ~1 day earlier when possible, else the oldest snapshot ≥ 6 h back.
    base_run = history.run_near(now - timedelta(hours=24), config.RISER_TOLERANCE_HOURS)
    if base_run is None:
        older = [r for r in history.runs[:-1] if (now - r.taken_at).total_seconds() >= config.VISIT_GROWTH_MIN_HOURS * 3600]
        base_run = older[0] if older else None
    base_games = load_games(conn, base_run.id) if base_run else None

    rolimons = rolimons_theme_counts(conn, latest.id, themes) if themes else None
    sources = ["explore-api get-sorts", "games.roblox.com v1/games", "games.roblox.com v1/games/votes"]
    if rolimons:
        sources.append("Rolimons gamelist")

    return Analysis(
        history=history,
        now=now,
        games=now_games,
        sorts_seen=sorts_seen,
        top=now_games[: config.TOP_N],
        risers_1d=r1,
        risers_7d=r7,
        visit_growth=visit_growth(conn, history, now_games),
        breakouts=found_breakouts,
        genres_l1=genre_share(now_games, base_games, "l1"),
        genres_l2=genre_share(now_games, base_games, "l2"),
        genre_baseline=base_run,
        themes=theme_stats(now_games, base_games, rising_ids, rolimons),
        theme_baseline=base_run,
        waves=clone_waves(now_games, rising_ids),
        labelled=[g for g in now_games if g.labels][:20],
        rolimons_used=rolimons is not None,
        sources=sources,
    )

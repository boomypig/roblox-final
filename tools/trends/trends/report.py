"""`report`: render the analysis as <report dir>/latest.md plus a dated copy in <report dir>/history/.

The report dir defaults to private/trends (config.DEFAULT_REPORT_DIR) and is created when missing."""

from __future__ import annotations

import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path

from . import config
from .analysis import Analysis, GameRow, Risers

READ_WHEN = "Choosing a game idea, judging saturation, or citing what's popular now."


def fmt_n(n: float | int | None) -> str:
    if n is None:
        return "–"
    n = float(n)
    sign = "-" if n < 0 else ""
    n = abs(n)
    if n >= 1e9:
        return f"{sign}{n / 1e9:.2f}B"
    if n >= 1e6:
        return f"{sign}{n / 1e6:.2f}M"
    if n >= 1e4:
        return f"{sign}{n / 1e3:.0f}K"
    if n >= 1e3:
        return f"{sign}{n / 1e3:.1f}K"
    return f"{sign}{n:.0f}"


def fmt_pct(p: float | None, signed: bool = False) -> str:
    if p is None:
        return "–"
    return f"{p:+.0f}%" if signed else f"{p:.0f}%"


def cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def game_link(g: GameRow) -> str:
    name = cell(g.name).replace("[", "(").replace("]", ")")
    link = f"[{name}]({config.GAME_PAGE_URL.format(place_id=g.root_place_id)})" if g.root_place_id else name
    return f"{link} _(Roblox event)_" if g.official else link


def themes_cell(g: GameRow) -> str:
    return ", ".join(g.themes) if g.themes else "–"


def genre_cell(g: GameRow) -> str:
    return " / ".join(x for x in (g.genre_l1, g.genre_l2) if x) or "–"


def age_cell(g: GameRow, now: datetime) -> str:
    days = g.age_days(now)
    return "–" if days is None else (f"{days} d" if days < 365 else f"{days / 365:.1f} y")


def render(a: Analysis) -> str:
    date = a.now.date().isoformat()
    h = a.history
    out: list[str] = []
    add = out.append

    add("---")
    add(f"title: Roblox trends — {date}")
    add("type: trends")
    add(f"read-when: {READ_WHEN}")
    add(f"last-researched: {date}")
    add(f"date: {date}")
    add(f"generated-at: {a.now.isoformat().replace('+00:00', 'Z')}")
    add("data-sources: [" + ", ".join(a.sources) + "]")
    add(f"snapshot-count: {len(h.runs)}")
    add(f"days-of-history: {len(h.days)}")
    add("generated-by: tools/trends (python -m trends report); do not hand-edit")
    add("---")
    add("")
    add(f"# Roblox trends — {date}")
    add("")
    add(
        f"Generated from **{len(h.runs)} snapshot{'s' if len(h.runs) != 1 else ''}** over **{len(h.days)} "
        f"day{'s' if len(h.days) != 1 else ''}** ({h.runs[0].taken_at:%Y-%m-%d %H:%M} → {h.runs[-1].taken_at:%Y-%m-%d %H:%M} UTC). "
        f"The latest snapshot covers {len(a.games)} games from {len(a.sorts_seen)} Roblox charts. "
        "Every number is tracker output, i.e. `(data)`, except lines labeled `(inferred)`."
    )
    add("")
    if len(h.days) < 8:
        add(
            f"> **Not enough history yet** for every section: 1-day risers need 2 days of snapshots and 7-day risers "
            f"need 8. This report has {len(h.days)}. Sections that can't be computed say so."
        )
        add("")

    _top(a, add)
    _risers(a.risers_1d, add)
    _risers(a.risers_7d, add)
    _visits(a, add)
    _breakouts(a, add)
    _genres(a, add)
    _themes(a, add)
    _theme_moves(a, add)
    _waves(a, add)
    _saturation(a, add)
    _labels(a, add)
    _meaning(a, add)
    _method(a, add)
    return "\n".join(out) + "\n"


def _top(a: Analysis, add) -> None:
    add(f"## Top {config.TOP_N} by current players")
    add("")
    add("| # | Game | Players | Visits | Like % | Roblox genre | Themes | Age | Updated |")
    add("|---|---|---|---|---|---|---|---|---|")
    for i, g in enumerate(a.top, 1):
        updated = g.updated.date().isoformat() if g.updated else "–"
        add(
            f"| {i} | {game_link(g)} | {fmt_n(g.playing)} | {fmt_n(g.visits)} | {fmt_pct(g.like_pct)} | "
            f"{genre_cell(g)} | {themes_cell(g)} | {age_cell(g, a.now)} | {updated} |"
        )
    add("")


def _risers(r: Risers, add) -> None:
    add(f"## Risers — {r.label}")
    add("")
    if r.baseline is None:
        add(f"_{r.note}_")
        add("")
        return
    add(
        f"Players now vs. the snapshot at {r.baseline.taken_at:%Y-%m-%d %H:%M} UTC (same time of day), "
        f"games with at least {fmt_n(config.RISER_MIN_PLAYERS)} players now."
    )
    add("")
    if r.rows:
        add("| Game | Then | Now | Change | Themes |")
        add("|---|---|---|---|---|")
        for c in r.rows:
            add(f"| {game_link(c.game)} | {fmt_n(c.before)} | {fmt_n(c.after)} | {fmt_pct(c.pct, True)} | {themes_cell(c.game)} |")
    else:
        add("_No games above the floor in both snapshots._")
    add("")
    if r.entered:
        add("Entered the charts since then: " + "; ".join(f"{game_link(g)} ({fmt_n(g.playing)})" for g in r.entered) + ".")
        add("")


def _visits(a: Analysis, add) -> None:
    v = a.visit_growth
    add("## Fastest visit growth")
    add("")
    if v.baseline is None:
        add(f"_{v.note}_")
        add("")
        return
    add(
        f"Visits gained per day since {v.baseline.taken_at:%Y-%m-%d %H:%M} UTC. Visits don't swing with time of day, "
        "so this is the steadier growth signal."
    )
    add("")
    add("| Game | Visits/day | Growth/day | Players | Themes |")
    add("|---|---|---|---|---|")
    for row in v.rows:
        add(f"| {game_link(row.game)} | {fmt_n(row.per_day)} | {row.pct_per_day:.2f}% | {fmt_n(row.game.playing)} | {themes_cell(row.game)} |")
    add("")


def _breakouts(a: Analysis, add) -> None:
    add(f"## New breakouts (created in the last {config.BREAKOUT_MAX_AGE_DAYS} days)")
    add("")
    if not a.breakouts:
        add(f"_No charted game under {config.BREAKOUT_MAX_AGE_DAYS} days old has {fmt_n(config.BREAKOUT_MIN_PLAYERS)}+ players._")
        add("")
        return
    add("| Game | Players | Created | Age | Roblox genre | Themes | Charts |")
    add("|---|---|---|---|---|---|---|")
    for g in a.breakouts:
        charts = ", ".join(sorted(g.sorts)[:3]) + ("…" if len(g.sorts) > 3 else "")
        add(
            f"| {game_link(g)} | {fmt_n(g.playing)} | {g.created.date().isoformat()} | {age_cell(g, a.now)} | "
            f"{genre_cell(g)} | {themes_cell(g)} | {charts or '–'} |"
        )
    add("")


def _genres(a: Analysis, add) -> None:
    add("## Genre share (Roblox's own genre fields)")
    add("")
    base = a.genre_baseline
    add(
        "Share of players across all charted games. "
        + (f"Change is vs. {base.taken_at:%Y-%m-%d %H:%M} UTC." if base else "_Change: not enough history yet._")
    )
    add("")
    add("| Genre (genre_l1) | Players | Share | Change (pts) | Games |")
    add("|---|---|---|---|---|")
    for s in a.genres_l1:
        delta = f"{s.share - s.prev_share:+.1f}" if s.prev_share is not None else "–"
        add(f"| {cell(s.genre)} | {fmt_n(s.players)} | {s.share:.1f}% | {delta} | {s.games} |")
    add("")
    add("Top subgenres (genre_l2):")
    add("")
    add("| Subgenre | Players | Share | Change (pts) | Games |")
    add("|---|---|---|---|---|")
    for s in a.genres_l2[:15]:
        delta = f"{s.share - s.prev_share:+.1f}" if s.prev_share is not None else "–"
        add(f"| {cell(s.genre)} | {fmt_n(s.players)} | {s.share:.1f}% | {delta} | {s.games} |")
    add("")


def _themes(a: Analysis, add) -> None:
    add("## Themes")
    add("")
    add(
        "Keyword themes from `tools/trends/themes.yaml` (matched on names; a few themes also check descriptions) "
        "plus manual tags. A game can carry several. "
        "\"Rising\" counts games on Up-and-Coming, new breakouts, or +20% risers."
    )
    add("")
    extra = " | All games (Rolimons) | All players (Rolimons)" if a.rolimons_used else ""
    add(f"| Theme | Games | Players | Per game | Median | Biggest game (share) | In top 100 | Rising | Change{extra} |")
    add("|---|---|---|---|---|---|---|---|---|" + ("---|---|" if a.rolimons_used else ""))
    for t in a.themes:
        row = (
            f"| {t.theme} | {t.games} | {fmt_n(t.players)} | {fmt_n(t.per_game)} | {fmt_n(t.median)} | "
            f"{cell(t.top_game)} ({t.top_share:.0f}%) | {t.in_top100} | {t.rising} | {fmt_pct(t.change_pct, True)} |"
        )
        if a.rolimons_used:
            row += f" {t.all_games if t.all_games is not None else '–'} | {fmt_n(t.all_players)} |"
        add(row)
    add("")


def _theme_moves(a: Analysis, add) -> None:
    add("## Rising and falling themes")
    add("")
    movers = [t for t in a.themes if t.change_pct is not None and t.players >= config.THEME_MIN_PLAYERS_FOR_CHANGE]
    if a.theme_baseline is None or not movers:
        add("_Not enough history yet: needs two snapshots at least 6 hours apart._")
        add("")
        return
    movers.sort(key=lambda t: t.change_pct, reverse=True)
    add(f"Total players per theme vs. {a.theme_baseline.taken_at:%Y-%m-%d %H:%M} UTC (themes with {fmt_n(config.THEME_MIN_PLAYERS_FOR_CHANGE)}+ players).")
    add("")
    rising = [t for t in movers if t.change_pct > 0][:6]
    add("Rising: " + (", ".join(f"`{t.theme}` {fmt_pct(t.change_pct, True)}" for t in rising) or "none."))
    add("")
    falling = [t for t in reversed(movers) if t.change_pct < 0][:6]
    add("Falling: " + (", ".join(f"`{t.theme}` {fmt_pct(t.change_pct, True)}" for t in falling) or "none."))
    add("")


def _waves(a: Analysis, add) -> None:
    add("## Forming clone waves")
    add("")
    add(
        f"A theme shared by {config.CLONE_WAVE_MIN_GAMES}+ rising games (Up-and-Coming chart, new breakouts, "
        "or +20% risers). The creation dates show how fresh the wave is."
    )
    add("")
    if not a.waves:
        add("_None this time._")
        add("")
        return
    for w in a.waves[:10]:
        span = ""
        if w.oldest and w.newest:
            span = f"; created {w.oldest.date().isoformat()} → {w.newest.date().isoformat()}"
        names = ", ".join(game_link(g) for g in sorted(w.games, key=lambda g: g.playing, reverse=True)[:6])
        add(f"- **{w.theme}**: {len(w.games)} rising games, {fmt_n(w.players)} players{span}. {names}")
    add("")


def _saturation(a: Analysis, add) -> None:
    add("## Saturation estimate")
    add("")
    add(
        "Games per theme vs. players per theme, from charted games only "
        + ("plus Rolimons' wider list. " if a.rolimons_used else "(Rolimons is off, so the long tail of small games is invisible). ")
        + "Labels are rough rules, `(inferred)`: _one game dominates_ = the biggest game holds 60%+ of the theme's players; "
        "_crowded_ = 15+ games with a median at or below the median charted game; _few games, high demand_ = 6 or fewer "
        "games averaging 2× the typical theme."
    )
    add("")
    groups = ("few games, high demand", "one game dominates", "crowded", "mixed")
    for label in groups:
        themes = [t for t in a.themes if t.saturation == label]
        if themes:
            add(f"- **{label}**: " + ", ".join(f"`{t.theme}` ({t.games} games, {fmt_n(t.per_game)}/game)" for t in themes[:12]))
    add("")


def _labels(a: Analysis, add) -> None:
    add("## Update and event labels in game names")
    add("")
    if not a.labelled:
        add("_No bracketed labels in charted names right now._")
        add("")
        return
    counts = Counter(word for g in a.games for label in g.labels for word in label.casefold().split() if word.isalpha())
    common = ", ".join(f"{w} ({n})" for w, n in counts.most_common(8))
    add(f"{sum(1 for g in a.games if g.labels)} charted games carry a bracketed label. Most common words: {common}.")
    add("")
    for g in a.labelled[:12]:
        add(f"- {game_link(g)}: {cell(', '.join(g.labels))} ({fmt_n(g.playing)} players)")
    add("")


def _meaning(a: Analysis, add) -> None:
    add("## What this means `(inferred)`")
    add("")
    add("Written by rules from the numbers above, nothing else. Treat each line as a lead to check, not a conclusion.")
    add("")
    lines: list[str] = []
    if len(a.history.days) < 2:
        lines.append(
            "Single day of data: \"rising\" here rests on Roblox's Up-and-Coming chart and creation dates, "
            "not on our own history. Re-read after a week of daily snapshots."
        )
    top_players = sum(g.playing for g in a.top) or 1
    theme_counter = Counter(t for g in a.top for t in g.themes)
    for theme, n in theme_counter.most_common(3):
        held = sum(g.playing for g in a.top if theme in g.themes)
        lines.append(f"`{theme}` appears in {n} of the top {len(a.top)} games, holding {100 * held / top_players:.0f}% of top-{len(a.top)} players.")
    for w in a.waves[:3]:
        if w.newest is None:
            continue
        newest_age = (a.now - w.newest).days
        stage = "still being joined (newest entry under 30 days old)" if newest_age <= 30 else "older (no new entries in 30+ days)"
        lines.append(f"Clone wave `{w.theme}`: {len(w.games)} rising games; {stage}.")
    gaps = [t for t in a.themes if t.saturation == "few games, high demand"]
    if gaps:
        lines.append("Few games but high players per game: " + ", ".join(f"`{t.theme}`" for t in gaps[:5]) + ". Possible gaps, or one-hit themes; check the games before acting.")
    crowded = [t for t in a.themes if t.saturation == "crowded"]
    if crowded:
        lines.append("Crowded (many games, typical game small): " + ", ".join(f"`{t.theme}`" for t in crowded[:5]) + ". A new entry here needs a strong spin.")
    if a.breakouts:
        newest = min(a.breakouts, key=lambda g: g.age_days(a.now) or 0)
        lines.append(
            f"Youngest breakout: {newest.name}, {age_cell(newest, a.now)} old with {fmt_n(newest.playing)} players "
            f"({genre_cell(newest)})."
        )
        ages = [g.age_days(a.now) for g in a.breakouts if g.age_days(a.now) is not None]
        genres = Counter(g.genre_l2 or g.genre_l1 or "Unknown" for g in a.breakouts).most_common(2)
        lines.append(
            f"{len(a.breakouts)} games under {config.BREAKOUT_MAX_AGE_DAYS} days old have {fmt_n(config.BREAKOUT_MIN_PLAYERS)}+ players "
            f"(median age {statistics.median(ages):.0f} days); most common genres: "
            + ", ".join(f"{g} ({n})" for g, n in genres) + ". New games can still break out."
        )
    if a.genre_baseline is not None:
        movers = sorted((s for s in a.genres_l1 if s.prev_share is not None), key=lambda s: s.share - s.prev_share)
        if movers:
            up, down = movers[-1], movers[0]
            lines.append(f"Genre share moved most: {up.genre} {up.share - up.prev_share:+.1f} pts, {down.genre} {down.share - down.prev_share:+.1f} pts.")
    if a.risers_1d.rows:
        r = a.risers_1d.rows[0]
        lines.append(f"Biggest 1-day riser: {r.game.name} ({fmt_pct(r.pct, True)} to {fmt_n(r.after)} players).")
    for line in lines:
        add(f"- {line} `(inferred)`")
    add("")


def _method(a: Analysis, add) -> None:
    add("## Method and caveats")
    add("")
    add(f"- Charts tracked ({len(a.sorts_seen)}): " + ", ".join(f"`{s}`" for s in a.sorts_seen) + ".")
    add("- Players = concurrent players from `games.roblox.com/v1/games` at snapshot time; they swing by hour and weekday, so risers compare snapshots taken at the same time of day.")
    add("- Sponsored chart slots are ignored for ranks. Charts list only the top few hundred games; small games are invisible unless Rolimons is enabled.")
    add("- Themes are keyword matches; a wrong tag is fixed by editing `tools/trends/themes.yaml` (exclude list or manual tags).")
    add("- Endpoints are unofficial and can change; `python -m trends doctor` checks them.")
    add("")
    add("## Sources")
    add("")
    add("1. https://apis.roblox.com/explore-api/v1/get-sorts — every chart and its games (unofficial)")
    add("2. https://apis.roblox.com/explore-api/v1/get-sort-content — one chart (unofficial)")
    add("3. https://games.roblox.com/v1/games — players, visits, favorites, created/updated, genre fields")
    add("4. https://games.roblox.com/v1/games/votes — up/down votes")
    if a.rolimons_used:
        add("5. https://api.rolimons.com/games/v1/gamelist — wider game list (third-party)")


def write(a: Analysis, trends_dir: Path) -> tuple[Path, Path]:
    text = render(a)
    history_dir = trends_dir / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    latest = trends_dir / "latest.md"
    dated = history_dir / f"{a.now.date().isoformat()}.md"
    latest.write_text(text, encoding="utf-8")
    dated.write_text(text, encoding="utf-8")
    return latest, dated

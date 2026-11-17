"""CLI: python -m trends collect | report | doctor"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from . import analysis, config, db, doctor, report, tagging
from .collect import collect
from .net import Client


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m trends", description="Roblox trend tracker")
    parser.add_argument("--db", type=Path, default=config.DEFAULT_DB, help=f"SQLite file (default {config.DEFAULT_DB})")
    parser.add_argument("-v", "--verbose", action="store_true", help="debug logging")
    sub = parser.add_subparsers(dest="command", required=True)

    p_collect = sub.add_parser("collect", help="take a snapshot of every chart")
    p_collect.add_argument("--cache", action="store_true", help="reuse cached responses (development only)")
    p_collect.add_argument("--rolimons", action="store_true", help="also fetch Rolimons for this run")

    p_report = sub.add_parser("report", help="write private/trends/latest.md and a dated copy in history/")
    p_report.add_argument("--out", type=Path, default=None,
                          help=f"report folder (default {config.DEFAULT_REPORT_DIR}; created if missing)")
    p_report.add_argument("--vault", type=Path, default=None,
                          help="deprecated: same as --out VAULT/trends (where reports went before they moved to private/)")
    p_report.add_argument("--stdout", action="store_true", help="print the report instead of writing files")

    p_doctor = sub.add_parser("doctor", help="check every data source")
    p_doctor.add_argument("--rolimons", action="store_true", help="also check Rolimons")

    p_lookup = sub.add_parser("lookup", help="show stored stats for games whose name contains TEXT")
    p_lookup.add_argument("text", help="case-insensitive name fragment, e.g. 'tower of hell'")
    p_lookup.add_argument("--limit", type=int, default=5)

    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.command == "doctor":
        checks = doctor.run_checks(Client(), args.db, use_rolimons=args.rolimons or config.USE_ROLIMONS)
        print(doctor.format_checks(checks))
        return 1 if any(c.status == "FAIL" for c in checks) else 0

    conn = db.connect(args.db)
    try:
        if args.command == "lookup":
            return lookup(conn, args.text, args.limit)
        if args.command == "collect":
            client = Client(cache_dir=config.CACHE_DIR if args.cache else None)
            result = collect(conn, client, use_rolimons=args.rolimons or config.USE_ROLIMONS)
            print(
                f"run {result.run_id}: {result.status} — {result.sorts} charts, {result.games} games, "
                f"{result.requests} requests, {len(result.problems)} problems"
            )
            return 1 if result.status == "failed" else 0

        themes, manual = tagging.load_themes()
        tagging.retag_all(conn, themes, manual)  # so themes.yaml edits show up without a new collect
        result = analysis.analyze(conn, themes)
        if result is None:
            print("No snapshots yet. Run `python -m trends collect` first.", file=sys.stderr)
            return 1
        if args.stdout:
            print(report.render(result))
        else:
            out_dir = args.out or (args.vault / "trends" if args.vault else config.DEFAULT_REPORT_DIR)
            latest, dated = report.write(result, out_dir)
            print(f"wrote {latest} and {dated}")
        return 0
    finally:
        conn.close()


def lookup(conn, text: str, limit: int) -> int:
    """Latest stored stats per matching game, biggest first, for citing in vault files as (data)."""
    rows = conn.execute(
        """
        SELECT g.universe_id, g.root_place_id, g.name, g.creator_name, g.created, g.updated, g.genre_l1, g.genre_l2,
               g.max_players, s.taken_at, s.playing, s.visits, s.favorites, s.up_votes, s.down_votes
        FROM games g
        JOIN snapshots s ON s.universe_id = g.universe_id
        WHERE s.taken_at = (SELECT MAX(taken_at) FROM snapshots WHERE universe_id = g.universe_id)
          AND g.name LIKE ? COLLATE NOCASE
        ORDER BY s.playing DESC LIMIT ?
        """,
        (f"%{text}%", limit),
    ).fetchall()
    if not rows:
        print(f"No stored game name contains '{text}'. Only charted games are stored.", file=sys.stderr)
        return 1
    for r in rows:
        tags = [t["tag"] for t in conn.execute(
            "SELECT DISTINCT tag FROM tags WHERE universe_id = ? AND source IN ('keyword', 'manual') ORDER BY tag",
            (r["universe_id"],))]
        charts = [f"{p['sort_id']}#{p['rank']}" for p in conn.execute(
            "SELECT p.sort_id, p.rank FROM placements p JOIN runs ru ON ru.id = p.run_id "
            "WHERE p.universe_id = ? AND ru.started_at = ? ORDER BY p.rank", (r["universe_id"], r["taken_at"]))]
        votes = (r["up_votes"] or 0) + (r["down_votes"] or 0)
        like = f"{100 * r['up_votes'] / votes:.0f}%" if votes else "–"
        print(
            f"{r['name']}\n  universe {r['universe_id']}, place {r['root_place_id']}, by {r['creator_name']}\n"
            f"  snapshot {r['taken_at']}: {r['playing']} playing, {r['visits']} visits, {r['favorites']} favorites, "
            f"{like} likes\n  created {r['created']}, updated {r['updated']}, max {r['max_players']} per server\n"
            f"  genre {r['genre_l1']} / {r['genre_l2']}; themes: {', '.join(tags) or '–'}\n"
            f"  charts: {', '.join(charts) or '–'}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())

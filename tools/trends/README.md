# Roblox trend tracker

Collects what's on Roblox's charts several times a day, keeps the history in SQLite, and writes
a trends report. `/pitch` and section 1 of `create-roblox-game` read that report.

The code is public; what it collects is yours. The database, the cache, the scheduled-run log
and the reports all go under the toolkit's `private/` folder, which git ignores and the tracker
creates on its first run:

| What | Where |
|---|---|
| Report | `private/trends/latest.md`, plus a dated copy in `private/trends/history/` |
| Database, cache, log | `private/trends/data/` (`trends.db`, `cache/`, `scheduled.log`) |

Set `ROBLOX_FINAL_PRIVATE` to keep that folder somewhere else. With no database yet, `report`
and `lookup` say so and exit 1; nothing crashes.

It answers: what's popular now, what's rising, which genres and themes are growing or shrinking,
which clone waves are forming, and how crowded each theme is. Risers need history: 1-day risers
need 2 days of snapshots and 7-day risers need 8. Until then the report says
"not enough history yet".

## Setup (WSL, Python 3.11+)

```bash
cd ~/roblox-final/tools/trends
uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt
# or: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Dependencies: `requests`, `PyYAML`. Everything else is the standard library.

## Usage

Run from `tools/trends/`:

| Command | What it does |
|---|---|
| `.venv/bin/python -m trends doctor` | Hits every data source, checks the response shape, checks themes.yaml and the database. Exit code 1 if anything FAILs. Run it first whenever something looks off. |
| `.venv/bin/python -m trends collect` | One snapshot: every chart, then details and votes for every charted game (~880 games, ~36 requests, ~1.5 min). |
| `.venv/bin/python -m trends report` | Re-tags every game from themes.yaml, analyzes the history, writes the report. `--stdout` prints instead. |
| `.venv/bin/python -m trends lookup "tower of hell"` | Latest stored stats for games whose name contains the text: players, visits, favorites, likes, created/updated, genre, themes, chart ranks. Handy when citing a game as `(data)`. |
| `.venv/bin/python -m unittest discover -s tests` | Tests (parsers on real captured responses, analysis on synthetic history). |

Options: `--db PATH` (default `private/trends/data/trends.db`), `report --out DIR` (default
`private/trends`), `-v` for debug logs, `collect --cache` reuses cached responses (development
only), `--rolimons` adds Rolimons for one run. The client's User-Agent names the tool only; set
`TRENDS_CONTACT` to add a URL or address where you can be reached.

## Themes

`themes.yaml` maps theme names to keywords. Add a theme by copying a block. Keywords match whole
words in the game's **name** (`egg` matches eggs, `fish*` matches fishing). A theme can opt into
description matching with `description: true`, but only use that for words that rarely appear in
unrelated descriptions; "fight", "survive" and "war" tagged half the charts when descriptions
were on for everything. `regex:` runs on the lowercased name (used for the "Verb a Noun" title
wave). `manual:` adds tags by universeId for games whose names carry no keyword.

`report` re-tags every stored game, so edits apply to the whole history.

## Data sources

All are public and unauthenticated. Roblox's endpoints are **unofficial**: undocumented, can change
without notice, and rate-limited. Responses carry `x-terms-message: Terms apply https://rblx.co/TOU`.

| Source | Endpoint | Status (2026-10-22) |
|---|---|---|
| Charts | `apis.roblox.com/explore-api/v1/get-sorts?sessionId=<uuid>&device=computer&country=all` | Works. Paged via `nextSortsPageToken` → `sortsPageToken` (5 pages, 28 sorts: 26 game charts, a filters row, a songs chart). Each sort already includes its games, so no per-chart calls are needed. |
| One chart | `apis.roblox.com/explore-api/v1/get-sort-content?sessionId=<uuid>&sortId=<id>` | Works. Only used if a chart comes back empty from get-sorts. |
| Game details | `games.roblox.com/v1/games?universeIds=<ids>` | Works. **Max 50 ids per call** (51+ returns 400 "Too many universe IDs"). Gives playing, visits, favoritedCount, created/updated, `genre_l1`/`genre_l2`, creator, description. |
| Votes | `games.roblox.com/v1/games/votes?universeIds=<ids>` | Works. 100 ids per call. |
| Rolimons | `api.rolimons.com/games/v1/gamelist` | Works (7,823 games as `[name, playing, thumbnail]`, keyed by place id). **Off** (`config.USE_ROLIMONS = False`): no published terms of use or API policy were found for it (no terms page at rolimons.com/terms on 2026-10-22). Ask Rolimons before turning it on. |

Rate limits: `games.roblox.com` advertised `x-ratelimit-limit: 200, 200;w=60`, but `/v1/games`
still returned 429 after ~25 calls at 1 request/s. The client waits 1.5 s between requests,
retries 429/5xx with exponential backoff (4, 8, 16, 32 s, honoring `Retry-After`), and logs and
skips any batch that still fails. Parsers skip malformed rows and record a "problem" on the run
instead of crashing.

Known blind spots:
- Charts are fetched as an anonymous session. Roblox may leave 16+-only games out of charts for
  unauthenticated viewers (unverified, 2026-10-24); only 5 of 880 charted games were 16+.
- Only charted games are stored. A big game that's on no chart that day (Jujutsu Shenanigans on
  2026-10-22) is invisible until it charts again.
- `created` is the place creation date, which can be years before public release (Natural
  Disaster Survival, Pet Simulator 99), so ages for old games are overstated.
- One snapshot is one moment: weekday evenings and Saturday nights differ by 2× or more.
- `/v1/games` field `createVipServersAllowed` reads `false` for every top game, even ones that
  sell private servers, so it seems to describe the anonymous caller. The tracker doesn't store
  it; don't cite it.

The available charts change over time. The report lists the ones seen in the latest snapshot.
If one you care about disappears, check `sorts` in the database (`first_seen`/`last_seen`).

## Database (`private/trends/data/trends.db`, not in git)

| Table | Contents |
|---|---|
| `runs` | One row per collect: times, status (ok / partial / failed), counts, problems (JSON) |
| `games` | universe_id, root_place_id, name, description, creator, created, updated, genre_l1, genre_l2, max_players, first/last seen |
| `snapshots` | One row per game per run: name at the time, playing, visits, favorites, up/down votes |
| `placements` | Which chart each game was in that run, rank, sponsored flag |
| `tags` | universe_id, tag, source (`keyword` / `roblox-genre` / `manual`) |
| `sorts` | Every chart id seen, with first/last seen |
| `rolimons_counts` | Rolimons rows per run (empty while Rolimons is off) |
| `snapshot_rows` (view) | The flat shape from the original spec: one row per chart appearance |

Stats live in `snapshots` once per run instead of once per chart (a game was in 1.7 charts on
average on 2026-10-22), and `placements` holds the ranks. Schema changes go in `db.MIGRATIONS`.

## How the analysis works

- **Players** are concurrent players at snapshot time. They swing by hour and weekday, so risers
  compare against the snapshot closest to exactly 24 h / 7 d earlier (±4 h), i.e. the same time
  of day.
- **Risers** only include games with 1,000+ players now. Games above the floor that weren't in
  the baseline snapshot are listed as "entered the charts".
- **Visit growth** (visits/day) doesn't depend on time of day, so it's the steadier growth signal.
- **Breakouts**: created in the last 90 days with 2,000+ players. Works from the first snapshot.
- **Clone waves**: a theme shared by 3+ "rising" games (on Up-and-Coming, new breakouts, or +20%
  risers). Creation dates show whether the wave is still being joined.
- **Saturation**: games per theme vs players per theme, with rough labels. Charts only show the
  top few hundred games, so the long tail is invisible without Rolimons.
- Thresholds live in `trends/config.py`.

## Scheduling (collect every 6 h, report daily)

WSL stops after a short idle timeout once no Windows terminal or process is using it, so cron
inside WSL only fires while WSL happens to be running. **Windows Task Scheduler is the reliable option**: it starts WSL
for each run. `run.sh` wraps the commands and appends output to
`private/trends/data/scheduled.log`.

In **PowerShell** (normal user, no admin needed):

```powershell
schtasks /Create /TN "roblox-trends-collect" /SC HOURLY /MO 6 /ST 00:15 /F /TR "wsl.exe -d <distro> -- /home/<you>/roblox-final/tools/trends/run.sh collect"
schtasks /Create /TN "roblox-trends-report" /SC DAILY /ST 00:45 /F /TR "wsl.exe -d <distro> -- /home/<you>/roblox-final/tools/trends/run.sh report"
```

`<distro>` is the name `wsl -l` prints (for example `Ubuntu`); `/home/<you>` is what `echo $HOME`
prints inside WSL. Task Scheduler needs the absolute path.

- Check them: `schtasks /Query /TN roblox-trends-collect /V /FO LIST`
- Run one now: `schtasks /Run /TN roblox-trends-collect`
- Remove them: `schtasks /Delete /TN roblox-trends-collect /F` (same for `-report`)
- A console window flashes for each run. To hide it, open Task Scheduler → the task →
  Properties → "Run whether user is logged on or not" (asks for your Windows password).
- Runs are skipped while the PC sleeps. Task Scheduler → Settings → "Run task as soon as possible
  after a scheduled start is missed" catches up after wake.

**Alternative, cron inside WSL** (only runs while WSL is up):

```bash
crontab -e
# add:
15 */6 * * * $HOME/roblox-final/tools/trends/run.sh collect
45 0 * * *   $HOME/roblox-final/tools/trends/run.sh report
```

Check `private/trends/data/scheduled.log` after the first scheduled run. The report's risers start meaning
something after about a week of snapshots.

## Files

```
tools/trends/
  README.md  requirements.txt  themes.yaml  run.sh
  trends/
    __main__.py   CLI
    config.py     paths, endpoints, pacing, thresholds
    net.py        HTTP client: timeouts, retries, backoff, pacing, optional cache
    sources/      explore.py (charts), games.py (details, votes), rolimons.py
    db.py         schema, migrations, writes
    collect.py    one snapshot
    tagging.py    themes.yaml → tags
    analysis.py   risers, breakouts, genre share, themes, waves, saturation
    report.py     markdown report
    doctor.py     source checks
  tests/          unittest + fixtures captured from the real endpoints
private/trends/   latest.md, history/, data/ (trends.db, cache, scheduled.log); outside git
```

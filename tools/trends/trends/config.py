"""Paths, endpoints, request pacing, and analysis thresholds. Change behavior here, not in code."""

from __future__ import annotations

import os
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parents[1]  # tools/trends
REPO_DIR = TOOL_DIR.parents[1]
# The database and the reports are the user's own data, so they live outside the tracked tree:
# in private/ (gitignored), which the tracker creates on its first run. Set ROBLOX_FINAL_PRIVATE
# to keep that folder somewhere else.
PRIVATE_DIR = Path(os.environ.get("ROBLOX_FINAL_PRIVATE") or REPO_DIR / "private").expanduser()
DATA_DIR = PRIVATE_DIR / "trends" / "data"
DEFAULT_DB = DATA_DIR / "trends.db"
DEFAULT_REPORT_DIR = PRIVATE_DIR / "trends"  # latest.md, plus history/<date>.md
THEMES_FILE = TOOL_DIR / "themes.yaml"
CACHE_DIR = DATA_DIR / "cache"

# Unofficial Roblox web endpoints (undocumented; verified 2026-10-22).
EXPLORE_SORTS_URL = "https://apis.roblox.com/explore-api/v1/get-sorts"
EXPLORE_SORT_CONTENT_URL = "https://apis.roblox.com/explore-api/v1/get-sort-content"
GAMES_URL = "https://games.roblox.com/v1/games"
VOTES_URL = "https://games.roblox.com/v1/games/votes"
ROLIMONS_GAMELIST_URL = "https://api.rolimons.com/games/v1/gamelist"
GAME_PAGE_URL = "https://www.roblox.com/games/{place_id}"

EXPLORE_DEVICE = "computer"
EXPLORE_COUNTRY = "all"
MAX_SORT_PAGES = 20  # get-sorts returned 5 pages on 2026-10-22

# Third-party; stays off until its terms are checked (see README).
USE_ROLIMONS = False

# Says what the client is. Set TRENDS_CONTACT (a URL or address) to add a way to reach you;
# nothing personal is sent unless you set it.
USER_AGENT = "roblox-final-trends/0.1 (personal research)" + (
    f" +{os.environ['TRENDS_CONTACT']}" if os.environ.get("TRENDS_CONTACT") else ""
)
TIMEOUT_SECONDS = 20.0
MAX_RETRIES = 4
BACKOFF_BASE_SECONDS = 4.0  # 4, 8, 16, 32 s
MAX_RETRY_AFTER_SECONDS = 60.0
# games.roblox.com advertises 200 requests / 60 s, but v1/games returned 429 after ~25 calls at
# 1 req/s on 2026-10-22, so stay slower than that. A full collect is ~36 requests.
POLITE_DELAY_SECONDS = 1.5

GAMES_BATCH_SIZE = 50  # /v1/games rejects more than 50 ids ("Too many universe IDs")
VOTES_BATCH_SIZE = 100

# Analysis
TOP_N = 25
RISER_MIN_PLAYERS = 1_000  # ignore tiny games whose % swings are noise
RISER_TOLERANCE_HOURS = 4.0  # baseline snapshot must be this close to exactly 1 d / 7 d earlier
RISERS_SHOWN = 20
VISIT_GROWTH_MIN_HOURS = 6.0
BREAKOUT_MAX_AGE_DAYS = 90
BREAKOUT_MIN_PLAYERS = 2_000
CLONE_WAVE_MIN_GAMES = 3
RISING_SORT_IDS = ("up-and-coming",)  # Roblox's own "rising" chart feeds clone-wave detection
# Roblox-run events (e.g. "The Hollow", Halloween 2026) chart high but aren't games a dev can compete
# with; they're flagged in the top table and left out of breakouts and clone waves.
OFFICIAL_CREATORS = ("Roblox", "Roblox Presents")
THEME_MIN_PLAYERS_FOR_CHANGE = 5_000
DESCRIPTION_CHARS_FOR_THEMES = 400  # descriptions get keyword-stuffed further down

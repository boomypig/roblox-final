#!/usr/bin/env bash
# Entry point for scheduled runs (Windows Task Scheduler -> wsl.exe -> this script).
# Usage: run.sh collect | run.sh report | run.sh both
# Output is appended to <private>/trends/data/scheduled.log, beside the database.
# <private> is the toolkit's private/ folder, or $ROBLOX_FINAL_PRIVATE when set.
set -uo pipefail
cd "$(dirname "$0")"
DATA="${ROBLOX_FINAL_PRIVATE:-../../private}/trends/data"
mkdir -p "$DATA"
LOG="$DATA/scheduled.log"
PY=.venv/bin/python
[ -x "$PY" ] || PY=python3

status=0
for cmd in $( [ "${1:-collect}" = both ] && echo "collect report" || echo "${1:-collect}" ); do
    echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) $cmd" >> "$LOG"
    "$PY" -m trends "$cmd" >> "$LOG" 2>&1 || status=$?
done
exit $status

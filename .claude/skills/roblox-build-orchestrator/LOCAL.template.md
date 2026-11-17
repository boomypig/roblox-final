# LOCAL.md for roblox-build-orchestrator

Copy this file to `LOCAL.md` and fill it in. `LOCAL.md` is yours and is never shared.

This skill needs almost nothing machine-specific. Optional settings:

- Run ledger folder (where `run_log.py` keeps each run; default is `./build-runs`
  under the folder you run it from, or pass `--dir`):
- Agents folder: nothing to set. The workers live in `~/roblox-final/.claude/agents` and load
  when roblox-final is in the session.

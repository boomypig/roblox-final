<!-- handoff: start -->
# HANDOFF: <Game name>, new game

Made on <made on> by `tools/new_game.py`. Nothing has been built yet. Each session replaces
this file at its end (`section.py handoff N` for a section, `section.py handoff --light build`
or `--light map` for one /build or one map pass); earlier ones are kept in `design/handoffs/`.

## Where things are

- `design/game.json`: the build contract, full of TODO markers until section 1 fills it.
- `design/layout.json`: where each kind of code lives (the roblox-code scaffold's layout).
- `src/`, `tests/`: the scaffold. One example service, controller, pure module and spec.
- `docs/`: pitch, glossary, decisions, backlog, ideas, and the spec and map-state templates.

## Done

- The scaffold, the contract skeleton, the starter docs and the session hook are in place.

## Unproven

- The four code gates on this machine: run them once the tools are installed (next step).
- `validate.py` fails on purpose until section 1 fills every TODO in `design/game.json`.

## Debts

- None.

## Next: first step

1. Install the pinned tools and packages, then run the gates (all four should be green):
   `rokit install` (reads aftman.toml), `wally install`,
   `python3 ../roblox-final/.claude/skills/roblox-code/scripts/check.py`.
2. Start a session with `claude --add-dir ../roblox-final` and say "complete the research and
   plan stage" (create-roblox-game, section 1).

# Moved paths

Every toolkit path that moved, old to new. `vault/INDEX.md` did not move and still lists
everything. A game repo that names an old path is fixed by its owner with:

```bash
python3 ~/roblox-final/tools/migrate_game.py <game dir>           # shows what would change
python3 ~/roblox-final/tools/migrate_game.py <game dir> --write   # applies it
```

The script rewrites references only. It never deletes a file, never touches the toolkit, and
lists anything ambiguous (a bare `goals.md`, the game's own `docs/workflow.md`) for you to
check by hand.

## Rewritten by the script

Paths are relative to the toolkit root. This table is the same list as `MOVES` in
`tools/migrate_game.py`; a test keeps them equal.

| Old | New | Why |
|---|---|---|
| `goals.md` | `private/goals.md` | personal; template is `goals.template.md` |
| `pitches/` | `private/pitches/` | personal |
| `docs/history/` | `private/history/` | personal planning notes |
| `vault/trends/` | `private/trends/` | generated from your own data |
| `vault/case-studies/` | `private/case-studies/` | personal research notes; cited as `(case study: <slug>)` |
| `tools/trends/data/` | `private/trends/data/` | the tracker's database, cache and log |
| `vault/fundamentals/quality-bar.md` | `.claude/skills/build/references/quality-bar.md` | read by `/build` and the reviewer |
| `vault/fundamentals/security-and-anti-exploit.md` | `.claude/skills/roblox-code/references/security.md` | read when writing a remote handler |
| `vault/fundamentals/ui-ux.md` | `.claude/skills/roblox-ui/references/ui-ux.md` | read when building UI |
| `vault/fundamentals/game-feel.md` | `.claude/skills/roblox-vfx/references/game-feel.md` | read when adding feedback to an action |
| `vault/fundamentals/visual-quality.md` | `.claude/skills/roblox-map/references/visual-quality.md` | read when setting the look or dressing a map |
| `vault/fundamentals/performance-and-devices.md` | `.claude/skills/roblox-map/references/performance-and-devices.md` | read when budgeting a map |
| `vault/fundamentals/building-with-studio-mcp.md` | `.claude/skills/roblox-map/references/studio-mcp.md` | read when building in Studio |

## Not rewritten: check by hand

| Old | Now | What to do |
|---|---|---|
| the game's own `docs/workflow.md` | the toolkit's `docs/workflow.md` is the one workflow doc | point the game's `CLAUDE.md` at `../roblox-final/docs/workflow.md`; remove the game's copy when ready |
| the game's `docs/tech/conventions.md` restating code rules | the rules are owned by `roblox-code` | keep only the game's own conventions; see `starter/docs/tech/conventions.md` |
| `vault/INDEX.md` rows with a full read-when line | `vault/CATALOG.md` | `INDEX.md` is now the short form; nothing to change in a game |
| links to a case study file | `(case study: <slug>)` | the file is in `private/case-studies/` when you keep case studies |
| `tools/trends` `report --vault DIR` | `report --out DIR` | `--vault` still works |
| `create-roblox-game/scripts/new_game.py "<Title>" --dir <dir>` | `tools/new_game.py "<Title>" [--dir <dir>]` | the old command still works: it forwards, and now makes the whole game |
| a game made before the layout map, the Stop hook and `HANDOFF.md` | `create-roblox-game/scripts/adopt.py --dir <game>` | run it read-only to see what it would add, then `--write`: it adds `design/layout.json`, the hook and any missing starter file, and changes no existing file. A game with no layout file is read with the scaffold's layout, so nothing breaks before you do |

## Unchanged

Every skill and agent name, every `/command`, `tools/new_game.py`, `tools/vault_lint.py`,
`tools/vault_apicheck.py`, `vault/INDEX.md`, `vault/CONTRIBUTING.md`, the `vault/genres/` and
`vault/patterns/` files, and the ten fundamentals that stayed in `vault/fundamentals/`.

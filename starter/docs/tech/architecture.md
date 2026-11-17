# Architecture

Where this game's code lives is `design/layout.json`, not this page: the boot scripts, the
services and controllers, where remotes are declared, the config, the pure-rule modules, the
tests, the packages and the tool manifest. Its fields are explained in the roblox-code skill
(`../roblox-final/.claude/skills/roblox-code/references/layout.md`), and `check.py`, `/build`
and the reviewer all read it. A new game starts with the roblox-code scaffold's layout; change
the file, not this page, when the code moves.

The code rules (server authority, one transport, pure logic, every tunable in config,
cosmetics never break gameplay) are the roblox-code skill's and are not restated here
(`docs/tech/conventions.md` says where each one is written).

This page holds what only this game knows. Fill each part in when the game decides it.

## Rojo

`default.project.json` maps the folders in `design/layout.json` into the place. Rojo owns
only those folders; map geometry, inserted assets and anything built in Studio belong to the
place file. Runtime children created inside a Rojo-managed folder are deleted on the next
connect (roblox-code `references/traps.md`).

## Services

Each service owns one piece of state and says so here (and in `design/game.json` "systems").

- <fill in at section 2: one line per service: its name, and the state it owns.>

## Maps

`design/layout.json` "map" says where the layout comes from: the roblox-map prover
(`design/map.json`) or a map built by hand in Studio from a brief. Either way, gameplay parts
sit in a `Layout` folder (tagged) and decoration in `Dressing`; the map-builder agent keeps
`docs/design/maps/<name>.state.md`. Code finds gameplay parts through CollectionService tags
or one path module, never FindFirstChild chains spread across services.

## Running a playtest

The steps are roblox-code's (`SKILL.md`, "When Studio is finally involved"): the four gates
green, the place open, `rojo serve` connected, Play, and the BUILD stamp in Output. Use two
clients for anything with hits, rounds or trading.

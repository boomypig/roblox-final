# Conventions
Full rules and traps: the roblox-code skill (`references/patterns.md`, `references/traps.md`).

## Code
- `--!strict` at the top of every new script.
- Disk is the source of truth. Edit files and let Rojo sync; never edit scripts in Studio or
  write script source over MCP.
- Knit Services (server) and Controllers (client). Knit is lifecycle only; gameplay remotes
  go through `src/shared/Net.luau`.
- Pure rules go in `src/shared/Core/` and take plain numbers (x, y, z), not Vector3/CFrame,
  so Lune can test them. Build the Vector3 at the edge.
- Every tunable lives in `src/shared/Config/`. No magic numbers in services.
- `task.wait/spawn/delay/defer`, never `wait/spawn/delay`.
- Never a bare `pcall`: capture the error and `warn` it.
- CollectionService tags for behaviors (e.g. "KillBrick"), not name matching.

## Style
- PascalCase for modules, services and instances; camelCase for locals and functions.
- Comments explain *why*, not *what*. Keep functions small; prefer early returns.
- StyLua formats, Selene lints. `check.py --fix` lets StyLua rewrite.

## Done means
- `check.py` green on all four gates (rojo build, lune test, selene, stylua).
- The BUILD stamp shows in Output on Play.
- Every generated asset is loaded by a line of shipping code (no orphaned assets).
- The reviewer agent has checked it against the spec and the vault quality bar.

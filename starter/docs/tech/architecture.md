# Architecture
Fill in the `<...>` parts per game. The layout comes from the roblox-code scaffold
(`~/roblox-final/.claude/skills/roblox-code`); the client/server rules come from the first game.

## Rojo mapping (default.project.json)
- src/server → ServerScriptService.Server (Knit Services: game rules, validation, data)
- src/client → StarterPlayerScripts.Client (Knit Controllers: UI, effects, input, camera)
- src/shared → ReplicatedStorage.Shared (Net, Config, Core)
- Packages → ReplicatedStorage.Packages (Knit, Promise, Signal, Trove from `wally install`)

Rojo owns only these folders. Workspace and Lighting get properties only, so map geometry,
inserted assets and anything built in Studio belong to the place file. **Never create
runtime children inside a Rojo-managed folder that must survive**: the next Rojo connect
deletes them (roblox-code traps). Map dressing lives in Studio, or in an `.rbxmx` that Rojo
serves, never in code that builds it at runtime.

## Layout
```
src/shared/Core/        pure Luau rules, no Instances, tested headless by tests/*.spec.luau
src/shared/Config/      every tunable (speeds, timings, prices). A balance pass is a data edit
src/shared/Net.luau     the ONLY gameplay transport: plain RemoteEvents, every name declared here
src/server/Services/    server-authoritative Knit Services
src/client/Controllers/ Knit Controllers: input, camera, UI, effects
tests/                  *.spec.luau, run with `lune run test`
design/                 game.json (the build contract) and one spec per asset stage
docs/                   pitch, specs, briefs, glossary, decisions
```

## Services
Each service owns one piece of state and says so here.
- <Service>: <what it owns>

## Maps
- The proven gameplay layout comes from the roblox-map skill (`design/map.json` → prover →
  `build.lua` or `.rbxmx`). The map-builder agent dresses it in Studio from the approved map
  brief. Two folders under the map root: `Layout` (gameplay, tagged) and `Dressing`
  (decoration, no collision unless the brief says so).
- Code finds gameplay parts through CollectionService tags or one path module (e.g.
  MapLayout), not FindFirstChild chains spread across services.

## Client ↔ server
- The client never reports progress, currency or results. The server detects and decides.
- Every value from a client is a request: check type, then range, then ownership.
- The server publishes state as attributes (on a ReplicatedStorage folder and on each Player);
  clients only read them. Times are `Workspace:GetServerTimeNow()` values.
- Cosmetics never break gameplay: effects resolve async, fail inert, each one pcall-isolated.
- Each gameplay service carries a debug trace behind an attribute flag
  (`workspace:GetAttribute("<Game>Debug")`) that prints why an action was refused.

## Running a playtest
1. `rokit install` (reads aftman.toml) or `aftman install`, then `wally install`.
2. `python3 ~/roblox-final/.claude/skills/roblox-code/scripts/check.py`: all four gates green.
3. Open the saved place in Studio, `rojo serve`, click Connect in the plugin, accept the prompt.
4. Press Play and look for the BUILD stamp line in Output. No stamp = Studio isn't running
   your code. Use two clients (Test tab) for anything with hits, rounds or trading.

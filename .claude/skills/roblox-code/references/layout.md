# The layout map: `design/layout.json`

Where one game keeps its code. The roblox-code rules name the scaffold's folders (`Core/`,
`Config/`, `Net.luau`, Knit services); a game that was not made by the scaffold keeps the same
things somewhere else. `design/layout.json` says where, so every reader checks the rules
against the game's real paths instead of folders it does not have.

Readers: `scripts/check.py` (which tools, which folders), `/build` (where new code goes), the
`reviewer` agent (what each rule is checked against). Writers: `tools/new_game.py` writes the
scaffold's map; `create-roblox-game/scripts/adopt.py --write` writes one for an existing game.
`scripts/layout.py` loads it, fills defaults and checks every path exists.

A game with no `design/layout.json` is read as the scaffold's layout (the defaults below).

## Fields

| Field | Scaffold value | What it says |
|---|---|---|
| `version` | `1` | Schema version. |
| `framework` | `"knit"` | `"knit"`: Knit services and controllers. `"modules"`: plain ModuleScripts that the boot script requires and calls `Init` then `Start` on. |
| `boot.server`, `boot.client` | `src/server/init.server.luau`, `src/client/init.client.luau` | The one entry script per side. With `"modules"`, it lists the modules it boots. |
| `services` | `src/server/Services` | Server-authoritative modules, one piece of state each. |
| `controllers` | `src/client/Controllers` | Client modules: input, camera, UI, effects. |
| `remotes.style` | `"net-module"` | `"net-module"`: every remote is declared in one module. `"per-service"`: each service creates its own remotes in one shared folder. |
| `remotes.where` | `src/shared/Net.luau` | The module (`net-module`), or the Instance path the services create their remotes under (`per-service`, e.g. `ReplicatedStorage.Remotes`). |
| `config` | `src/shared/Config` | Every tunable: a folder, or one module file. |
| `pure` | `["src/shared/Core"]` | Folders or files holding pure rules (no Instances, no services, no yielding). |
| `tests` | `"tests"` | Folder of `*.spec.luau` run by `lune run test`; `null` when the game has no tests yet. |
| `packages` | `"wally"` | `"wally"` (needs `wally install` and `Packages/`) or `"none"`. |
| `toolchain` | `"aftman.toml"` | The manifest that pins the tools (`rokit.toml` or `aftman.toml`; rokit reads both). |
| `lint` | `["src"]` | What selene checks. |
| `format` | `["src", "lune"]` | What stylua checks (paths that do not exist are dropped). |
| `map.source` | `"prover"` | `"prover"`: the layout comes from roblox-map (`map.spec`). `"studio"`: built by hand in Studio from a brief (`map.brief`). |
| `map.spec` / `map.brief` | `design/map.json` | The roblox-map spec, or the approved map brief. |
| `adopted` | `false` | `true` when `adopt.py` wrote the file for a game made before the toolkit. |
| `notes` | `[]` | Lines a reader must know, e.g. "(inferred) Scoring.luau is pure: no Instance or service use". |

## How each rule maps

| roblox-code rule (`SKILL.md`) | Check it against |
|---|---|
| 2. Pure logic lives in `src/shared/Core/` | every path in `pure` |
| 3. One `Net.luau` of plain RemoteEvents | `remotes`: with `per-service`, each remote is created in exactly one service, under `remotes.where`, and every handler validates its input |
| 5. Every tunable in `src/shared/Config/` | `config` |
| Knit lifecycle (services, controllers) | `framework`, `boot`, `services`, `controllers` |
| The four gates | `check.py` reads `tests`, `packages`, `toolchain`, `lint`, `format` |

A layout that differs from the scaffold is not a defect. Moving an adopted game onto the
scaffold's layout is a refactor the user asks for, never part of adoption
(`create-roblox-game/references/adopt.md`).

## Example: an adopted game

```json
{
  "version": 1,
  "framework": "modules",
  "boot": {"server": "src/server/Main.server.luau", "client": "src/client/Main.client.luau"},
  "services": "src/server/Services",
  "controllers": "src/client/Controllers",
  "remotes": {"style": "per-service", "where": "ReplicatedStorage.Remotes"},
  "config": "src/shared/Config.luau",
  "pure": ["src/shared/RoundTimer.luau", "src/shared/Scoring.luau"],
  "tests": null,
  "packages": "none",
  "toolchain": "rokit.toml",
  "lint": ["src"],
  "format": ["src"],
  "map": {"source": "studio", "brief": "docs/design/maps/harbor.md"},
  "adopted": true,
  "notes": ["(inferred) Scoring.luau is pure: no Instance, service or yield"]
}
```

## Sources

- The scaffold: `scripts/new_project.py` (the default values above).
- The adopted shape: the fixture `tests/fixtures/adopted-game/`, built from a real game made
  before the toolkit (plain modules booted from `Main.server.luau`, remotes created by each
  service under `ReplicatedStorage.Remotes`, one `Config.luau`, pure modules loose in
  `src/shared`, no Wally, `rokit.toml`, no tests, a map built by hand in Studio).

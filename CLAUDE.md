# roblox-final — the Roblox game-making toolkit

## What this is
A toolkit for making Roblox games with Claude Code. It holds no game code: each game is its own repo
next to this folder (`~/<game>`), and loads this one with `claude --add-dir ../roblox-final`.

## Layout
- `.claude/skills/`: every skill (table below). `.claude/agents/`: every agent.
- `vault/`: researched design knowledge (genres, fundamentals, patterns). Index: `vault/INDEX.md`.
- `tools/trends/`: Roblox chart tracker. `tools/new_game.py`: new game repo.
  `tools/vault_lint.py`, `tools/vault_apicheck.py`: vault checks. `tests/`: toolkit tests.
- `starter/`: docs copied into every new game by `tools/new_game.py`.
- `docs/workflow.md`: the whole flow, from idea to published game. `docs/decisions.md`: why the
  toolkit is built the way it is; log every toolkit decision there.
- `goals.template.md`: template for `private/goals.md`.

## private/ (the user's own notes; gitignored; may not exist)
| Path | What | When it is missing |
|---|---|---|
| `private/goals.md` | Goals and constraints every pitch and design is judged against | Copy `goals.template.md` there, say so, ask once whether to fill it in; otherwise use the template's defaults as stated assumptions |
| `private/pitches/` | `/pitch` output | Create it when writing a pitch |
| `private/trends/latest.md`, `history/`, `data/` | Generated trend reports and the tracker database | Say so; run `collect` and `report`, or continue without market numbers |
| `private/case-studies/` | Case studies of named games, cited in the vault as `(case study: <slug>)` | Skip; the genre file's "Top examples" has the summary |
| `private/lessons-inbox.md`, `toolkit-handoff.md`, `upstream-changes.md`, `archive/`, `history/` | Toolkit maintenance notes | Create when first needed |

Never stop or fail because a `private/` file is absent, never write a path to a specific
private file (a dated pitch, a note) into a tracked file, and never commit anything from
`private/` to the toolkit repo.

## Which tool for what
| Need | Use |
|---|---|
| Ideas for the next game | `/pitch [constraints]` (goals file + vault + trends report) |
| Start a game repo | `python3 ~/roblox-final/tools/new_game.py "<Title>"` |
| Build a game, section by section | `create-roblox-game` ("complete the research and plan stage", "continue with the development of <game>") |
| Time, log and fan out a build | `roblox-build-orchestrator` (+ the `roblox-asset-*` workers) |
| The look: art direction, map brief, UI brief | `/art-brief art \| map <name> \| ui` |
| A mechanic spec | `spec-writer` agent |
| Implement a spec | `/build <spec>` (follows `roblox-code`, runs its four gates) |
| Code rules, scaffold, gates, traps | `roblox-code` |
| A provably playable map layout | `roblox-map` |
| Dress a map in Studio from a brief | `map-builder` agent, one zone or pass per run |
| UI from a JSON spec | `roblox-ui` |
| Meshes / textures | `roblox-3d-model` / `roblox-texture-gen` |
| Animation / VFX / SFX | `roblox-animation` / `roblox-vfx` / `roblox-sfx` |
| Check work | `reviewer` agent (spec, rules, gates, vault quality bar) |
| First-time machine setup | `roblox-skills-setup` (writes each skill's personal `LOCAL.md`) |

## Running tools
- Python, Rojo, Wally, Lune, Selene, StyLua and the trends venv live in **WSL** (Ubuntu). From a
  Windows shell, run them through `wsl.exe -e bash -lc '<command>'`. Skill docs give script
  paths as `~/roblox-final/.claude/skills/<skill>/scripts/...`, which is a WSL path.
- Trends: `cd ~/roblox-final/tools/trends && .venv/bin/python -m trends collect | report |
  doctor | lookup "<name>"` (tools/trends/README.md). Reports and data go to `private/trends/`.
- Studio MCP: the built-in server, tools `mcp__Roblox_Studio__*`. One MCP server and one Rojo
  connection at a time.

## How to use the vault
- Load `vault/INDEX.md` first, then only the files whose read-when line matches the task.
  Don't load whole folders.
- Quality bar for any build: `vault/fundamentals/quality-bar.md`.
- Writing or editing vault files: follow `vault/CONTRIBUTING.md` (frontmatter, claim tags,
  dated numbers, Sources list, 100–400 lines). Run `python3 tools/vault_lint.py` after.
- Never hand-edit `private/trends/latest.md` or `private/trends/history/`; they're generated.

## Editing this toolkit
- A script written during a game that the next game would need goes into the owning skill's
  `scripts/`, takes paths as arguments, and says in its docstring what defect it exists for
  (create-roblox-game "A TOOL YOU WRITE DURING A RUN BELONGS TO THE SKILL").
- A lesson about design goes in the vault; a lesson about a tool goes in that skill's traps.
- `LOCAL.md` files are personal (gitignored). Templates are `LOCAL.template.md`.
- Agents load at session start: restart the session after editing one.

## Hard rules
- Describe other games' designs; never copy their assets, names, or content.
- Never claim a pitch will succeed. Mark inferences `(inferred)`.
- Never commit API keys or tokens; skills read keys from environment variables
  (`ROBLOX_API_KEY`, `HF_TOKEN`). The tracker uses only public, unauthenticated endpoints.
- Kaggle is off for every stage (its terms ban this use; see `roblox-3d-model`).

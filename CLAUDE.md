# roblox-final — the Roblox game-making toolkit

## What this is
A toolkit for making Roblox games with Claude Code. It holds no game code: each game is its own
repo next to this folder (`~/<game>`), and loads this one with `claude --add-dir ../roblox-final`.

## Layout
- `.claude/skills/`: every skill (table below). `.claude/agents/`: every agent.
- `vault/`: researched design knowledge (genres, fundamentals, patterns). Index: `vault/INDEX.md`.
- `tools/trends/`: Roblox chart tracker. `tools/new_game.py`: new game repo.
  `tools/vault_lint.py`, `tools/vault_apicheck.py`: vault checks. `tests/`: toolkit tests.
- `starter/`: docs copied into every new game by `tools/new_game.py`.
- `docs/workflow.md`: the one path from idea to published game, and the operating policy every
  skill and agent follows. `docs/structure.md`: the five parts every skill and agent has.
  `docs/decisions.md`: why the toolkit is built the way it is; log every toolkit decision there.
  `docs/migration.md`: every moved path, old to new. `docs/redundancy-map.md`,
  `docs/vault-readers.md`: which file owns each rule, and which step reads each research file.
- `goals.template.md`: template for `private/goals.md`.

## private/ (the user's own notes; gitignored; may not exist)
| Path | What | When it is missing |
|---|---|---|
| `private/goals.md` | Goals and constraints every pitch and design is judged against | Copy `goals.template.md` there, say so, ask once whether to fill it in; otherwise use the template's defaults as stated assumptions |
| `private/pitches/` | `/pitch` output | Create it when writing a pitch |
| `private/trends/latest.md`, `history/`, `data/` | Generated trend reports and the tracker database | Say so; run `collect` and `report`, or continue without market numbers |
| `private/case-studies/` | Case studies of named games, cited in the vault as `(case study: <slug>)` | Skip; the genre file's "Top examples" has the summary |
| `private/lessons-inbox.md`, `lessons-done.md` | Lessons each game's Stop hook appends; what `/toolkit-retro` closed | `session.py` creates the inbox; `inbox.py` the record |
| `private/toolkit-handoff.md`, `upstream-changes.md`, `archive/`, `history/` | Toolkit maintenance notes | Create when first needed |

Never stop or fail because a `private/` file is absent, never write a path to a specific
private file (a dated pitch, a note) into a tracked file, and never commit anything from
`private/` to the toolkit repo.

## Which tool for what
| Need | Use |
|---|---|
| Ideas for the next game | `/pitch [constraints]` (goals file + vault + trends report) |
| Start a game repo | `python3 ~/roblox-final/tools/new_game.py "<Title>"` |
| Take on a game made before the toolkit | `create-roblox-game/scripts/adopt.py --dir <game>` (read-only; `--write`), `references/adopt.md` |
| End a /build or map pass outside a section | `section.py handoff --light build\|map` (the game's Stop hook asks for it) |
| Prove the toolkit end to end | `python3 tools/smoke.py` (CI runs it with `--wally`) |
| Build a game, section by section | `create-roblox-game` ("complete the research and plan stage", "continue with the development of <game>") |
| Time, log and fan out a build | `roblox-build-orchestrator` (+ the `roblox-asset-*` workers) |
| The look: art direction, map brief, UI brief | `/art-brief art \| map <name> \| ui` |
| A mechanic spec | `spec-writer` agent (gate: `build/scripts/check_spec.py`) |
| Implement a spec | `/build <spec>` (follows `roblox-code`, runs its four gates) |
| Code rules, scaffold, gates, traps | `roblox-code` |
| A provably playable map layout | `roblox-map` |
| Dress a map in Studio from a brief | `map-builder` agent, one zone or pass per run |
| UI from a JSON spec | `roblox-ui` |
| Meshes / textures | `roblox-3d-model` / `roblox-texture-gen` |
| Animation / VFX / SFX | `roblox-animation` / `roblox-vfx` / `roblox-sfx` |
| Check work | `reviewer` agent (spec, rules, gates, vault quality bar) |
| First-time machine setup | `roblox-skills-setup` (writes each skill's personal `LOCAL.md`) |
| Turn game lessons into toolkit edits | `/toolkit-retro` (reads `private/lessons-inbox.md`; only when the user asks) |

## Running tools
- Python, Rojo, Wally, Lune, Selene, StyLua and the trends venv live in **WSL** (Ubuntu). From a
  Windows shell, run them through `wsl.exe -e bash -lc '<command>'`. Skill docs give script
  paths as `~/roblox-final/.claude/skills/<skill>/scripts/...`, which is a WSL path.
- Trends: `cd ~/roblox-final/tools/trends && .venv/bin/python -m trends collect | report |
  doctor | lookup "<name>"` (tools/trends/README.md). Reports and data go to `private/trends/`.
- Studio MCP: the built-in server, tools `mcp__Roblox_Studio__*`. Some skill passages use an
  older server's tool names; `create-roblox-game/references/mcp.md` ("Tool names") maps them.
  One MCP server and one Rojo connection at a time.

## How to use the vault
- Load `vault/INDEX.md` first (the short index), then only the files whose name matches the
  task. `vault/CATALOG.md` has each file's full read-when line; open it only when a name is not
  enough. Don't load whole folders. Build references (quality bar, security, UI, game feel,
  visual quality, performance, Studio MCP) live in the owning skill's `references/`.
- Quality bar for any build: `.claude/skills/build/references/quality-bar.md`.
- Writing or editing vault files: follow `vault/CONTRIBUTING.md` (frontmatter, claim tags,
  dated numbers, Sources list, 100–400 lines). The same rules cover the build references the
  catalog lists. Run `python3 tools/vault_lint.py` after.
- Never hand-edit `private/trends/latest.md` or `private/trends/history/`; they're generated.

## Editing this toolkit
- Operating policy: `docs/workflow.md`. Decide, log the reason in `docs/decisions.md`, continue.
- Every change needs proof: `python3 -m unittest discover -s tests`, `python3 tools/vault_lint.py`,
  `python3 tools/toolkit_lint.py` and `python3 tools/smoke.py` must pass, and a new rule or script comes with a test that fails
  without it.
- When an existing test fails, change the work until it passes; never loosen the test (an
  allowlist entry, a weaker assertion, a skip) to fit the change. A new check goes in a new
  test, not in an existing test file. If a test itself is wrong, say why and ask the user
  before editing it.
- One owner per rule (`docs/redundancy-map.md`). A skill or agent has five parts
  (`docs/structure.md`); an agent holds no knowledge of its own.
- After editing a section an agent card carries, run `python3 tools/build_cards.py` (the tests
  fail on a stale card).
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

# roblox-final

A toolkit for making Roblox games with [Claude Code](https://claude.com/claude-code): researched
design knowledge, a market-trends tracker, pitch scoring, and a build pipeline that takes a
game from an idea to a published place (code, maps, UI, 3D models, textures, animation, VFX,
sound, assembly, playtest, publish). Every stage ends in a gate a script can check, so the
work is proven on disk before Roblox Studio sees it.

It holds no game code. Each game is its own repo next to this folder and loads the toolkit
with `claude --add-dir ../roblox-final`.

> **About the research.** The design library (`vault/`) describes how other Roblox games are
> designed: their loops, pacing, monetization and what makes them stick. It never copies their
> assets, names or content, and nothing built with this toolkit should either.

## Requirements

| Need | For | Notes |
|---|---|---|
| Claude Code | everything | terminal or desktop app |
| Python 3.11+ | every script | standard library only, except the trends tracker (`requests`, `PyYAML`) |
| [Rokit](https://github.com/rojo-rbx/rokit) or Aftman | code | installs the pinned Rojo, Wally, Lune, Selene and StyLua for each game |
| Roblox Studio with its built-in MCP server | assembly, maps, playtest | one Studio connection at a time |
| Blender 4.x | 3D models, animation | optional |
| A Hugging Face token (`HF_TOKEN`) | generated meshes | optional; Kaggle is never used |
| A Roblox Open Cloud key (`ROBLOX_API_KEY`) | permanent asset uploads, publish | optional; assets still work inside a Studio session without it |

The tested setup is Windows with WSL (Ubuntu): Studio runs on Windows, every tool runs in
WSL. Keys are read from environment variables and are never written to a file.

## Quick start

```bash
git clone https://github.com/boomypig/roblox-final.git ~/roblox-final
cd ~/roblox-final
claude                                  # then type: /roblox-skills-setup
```

`/roblox-skills-setup` checks the machine, tells you what is missing, and writes each skill's
personal `LOCAL.md` (your folders and tool paths; gitignored). The skill docs give script paths
as `~/roblox-final/...`, so clone it there or expect to adjust them.

Then make a game:

```bash
mkdir -p private && cp goals.template.md private/goals.md   # optional: your goals and constraints
claude                                  # /pitch            -> five scored ideas in private/pitches/
python3 tools/new_game.py "My Game"     # -> ~/my-game, next to the toolkit, green on all gates
cd ~/my-game && rokit install && wally install
claude --add-dir ../roblox-final        # "complete the research and plan stage"
```

A game you made before the toolkit is adopted, not remade:
`python3 .claude/skills/create-roblox-game/scripts/adopt.py --dir <game>` shows what it found
(where the game keeps its services, remotes, config and pure rules); `--write` adds the layout
map, the build contract and the starter files without touching the code.

## How a game gets built

One section per session. You approve a section, clear the chat, and the next session resumes
from the game's `HANDOFF.md`. A Stop hook in every game refuses to end a session at its
boundary (a closed section, a finished map pass, a passing /build) until `HANDOFF.md` is
written, and appends what went wrong to your lessons inbox. The full path, with what each step
reads, writes and is gated by, is [docs/workflow.md](docs/workflow.md).

| Step | What you say or run | What ends it |
|---|---|---|
| Choose | `/pitch [constraints]` | five scored pitches; you pick one |
| 1 Research and design | "complete the research and plan stage" | `design/game.json` passes `validate.py` |
| The look | `/art-brief art`, `map <name>`, `ui` | you set each brief to `Status: approved` |
| 2 Code and a playable loop | "complete the code stage" | four code gates green; the loop is played on grey parts |
| 3 World and visuals | "complete the art stage" | proven map layout, meshes, UI on disk |
| 4 Motion and sound | "complete the sound stage" | animation, VFX and SFX verified |
| 5 Assembly and playtest | "complete the playtest stage" | wiring gate, two-player playtest, review against the quality bar |
| 6 Publish | "complete the publish stage" | published, live-server check |
| After launch | spec → `/build <spec>` → reviewer | four code gates green, acceptance criteria met |

## Layout

| Path | What |
|---|---|
| `.claude/skills/` | 15 skills: `create-roblox-game` (the front door), `roblox-build-orchestrator`, `pitch`, `art-brief`, `build`, `roblox-code`, `roblox-map`, `roblox-ui`, `roblox-3d-model`, `roblox-texture-gen`, `roblox-animation`, `roblox-vfx`, `roblox-sfx`, `roblox-skills-setup`, `toolkit-retro` (turns the lessons games leave into tested toolkit edits, only when you ask) |
| `.claude/agents/` | 10 agents: `spec-writer`, `map-builder`, `reviewer`, `roblox-market-scout`, and the `roblox-asset-*` workers (map, mesh, ui, anim, vfx, sfx) |
| `vault/` | The design library: genres, fundamentals, mechanic patterns. Start at `vault/INDEX.md`. Knowledge a build step uses lives in that skill's `references/` |
| `tools/` | `new_game.py`, `smoke.py` (the end-to-end proof), `toolkit_lint.py`, `migrate_game.py`, `build_cards.py`, the trends tracker (`tools/trends/`), vault lint and API checks |
| `starter/` | Docs every new game repo starts with |
| `docs/` | `workflow.md` (the one path and the operating policy), `structure.md` (the shape of a skill and an agent), `decisions.md`, `migration.md` (moved paths), `redundancy-map.md`, `vault-readers.md` |
| `tests/` | The toolkit's own tests |
| `goals.template.md` | Template for your goals file |
| `private/` | **Yours, never in git:** goals, pitches, trend reports and data, case studies, notes. Created as you use the toolkit; everything works without it |
| `CLAUDE.md` | The guide Claude reads when working in this folder |

## Checks

```bash
python3 -m unittest discover -s tests -v                                   # toolkit tests
python3 tools/vault_lint.py                                                # design library rules
python3 tools/build_cards.py --check                                       # agent cards are current
python3 tools/toolkit_lint.py                                              # duplicated rules, dead paths, untested scripts, private data
python3 tools/smoke.py                                                     # a new game, every gate, every command, the hooks, adoption
cd tools/trends && python3 -m unittest discover -s tests                   # tracker tests
```

The same commands run in GitHub Actions on every push. `smoke.py` needs Rojo, Lune, Selene and
StyLua installed (it finds rokit's copies, or set `ROBLOX_TOOLS_BIN` to a folder holding them);
CI also installs Wally and runs it with `--wally`.

## Notices

- Fonts in `.claude/skills/roblox-ui/references/fonts` are Fredoka, under the SIL Open Font
  License 1.1.
- Third-party tools and models the skills call (Blender, Rojo, Hugging Face models, Roblox
  services) have their own terms. `roblox-3d-model/references/licences.md` lists the model
  licences.
- See [NOTICE.md](NOTICE.md) for the full list. Changes are in [CHANGELOG.md](CHANGELOG.md);
  how to contribute is in [CONTRIBUTING.md](CONTRIBUTING.md).

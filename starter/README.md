# Starter docs for a new game repo

`tools/new_game.py` copies this folder into every new game, on top of the roblox-code scaffold
and the create-roblox-game contract, and `adopt.py` copies the files an existing game lacks.
You don't copy it by hand:

```bash
python3 ~/roblox-final/tools/new_game.py "My Game"      # makes ~/my-game next to roblox-final
```

These files are the parts of a game repo that proved worth keeping from one game to the next:
the spec-first workflow, the Studio MCP setup, and the doc templates. They become the game's
own and change with it. The vault, skills and agents stay in roblox-final and are read from
there.

## Loading the shared skills and agents

`.claude/settings.json` gives the game repo read access to `../roblox-final` (the vault). That
alone doesn't load skills or agents. Adding the folder to the session does:

- **Terminal:** `claude --add-dir ../roblox-final`
- **Desktop app:** **+** next to the prompt box → **Add folder** → roblox-final. Type `/` and
  check that `/art-brief` and `/create-roblox-game` are listed.

Agents in an added folder load when the session starts, so restart after editing one. If the
game repo defines a skill with the same name, its own wins and the shared one becomes
`/roblox-final:<name>`.

## What's here

| File | What it's for |
|---|---|
| `CLAUDE.md` | Project brief: a task -> file list, the stack, the hard rules. Holds no status: that is `HANDOFF.md`. Points at the toolkit's `docs/workflow.md`, the one workflow doc |
| `HANDOFF.md` | The first handoff: what was made and the first step. Every session replaces it at its end |
| `.claude/settings.json` | Read access to `../roblox-final`, and the Stop hook (`create-roblox-game/scripts/session.py stop`) that refuses to end a session at a boundary without an up-to-date `HANDOFF.md`. From Windows it runs through `wsl.exe` |
| `.mcp.json` | Studio MCP for Claude Code run inside WSL. The desktop app already has the Studio MCP without it |
| `.gitignore` | Merged into the scaffold's: keeps place files and the hook's session state out of git |
| `docs/pitch.md`, `decisions.md`, `glossary.md`, `ideas.md`, `backlog.md` | Empty formats that worked |
| `docs/tech/architecture.md`, `conventions.md` | What only this game knows (its services, its map source) and its own conventions. Where code lives is `design/layout.json`; the code rules are the `roblox-code` skill's and are not restated |
| `docs/design/mechanics/_template.md` | Spec template with acceptance criteria |
| `docs/research/reference-games/_template.md` | Notes on a game you played |

The scaffold provides `default.project.json`, `aftman.toml` (rokit reads it too), `wally.toml`,
the `src/` layout and `tests/`; create-roblox-game provides `design/game.json` and `BUILD.md`;
roblox-code's `layout.py` provides `design/layout.json`; roblox-map provides
`docs/design/maps/_template.state.md`. Every `<fill in ...>` names the step that fills it.

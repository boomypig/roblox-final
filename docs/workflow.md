# From idea to published game

The whole flow, and which tool does each step. A game repo gets a shorter copy of the build
half in `docs/workflow.md` (from `starter/`).

```
 goals ────┐
 vault/ ───┼─> /pitch ──> pick one ──> tools/new_game.py ──> section 1: research + design
 trends ───┘                                                   (design/game.json, docs/pitch.md)
                                                                        │
                 /art-brief art, map, ui  <─────────────────────────────┘  (you approve the look)
                                                                        │
   section 2: code + greybox, PLAY the loop on grey parts (roblox-code, roblox-map blockout)
   section 3: world + visuals (roblox-map, roblox-3d-model, roblox-texture-gen, roblox-ui,
              map-builder dresses in Studio from the brief)
   section 4: motion + sound (roblox-animation, roblox-vfx, roblox-sfx)
   section 5: assembly + two-player playtest + reviewer vs vault quality bar
   section 6: publish
                                                                        │
   after launch: idea → spec-writer → approve → /build → reviewer → playtest → close out
```

## 0. Once per machine
1. Open roblox-final in Claude Code and run `roblox-skills-setup`. It checks Python, Rojo,
   Wally, Lune, Selene, StyLua, Blender and the Studio MCP, and writes each skill's `LOCAL.md`.
2. Trends tracker venv:
   `cd ~/roblox-final/tools/trends && uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt`
   (or `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`).
3. Optional: schedule the tracker (tools/trends/README.md, "Scheduling"). Risers need a week of
   snapshots.

## 1. Choose the game (in roblox-final)
- Keep `private/goals.md` current (copy `goals.template.md` the first time): answer its `TBD`s
  when you can; they change every score.
- Refresh market data if `private/trends/latest.md` is missing or more than 3 days old:
  `.venv/bin/python -m trends collect && .venv/bin/python -m trends report`.
- `/pitch [constraints]` writes five scored pitches to `private/pitches/`. Pick one.

## 2. Build it (in the game repo)
```bash
python3 ~/roblox-final/tools/new_game.py "<Title>"     # ~/<title>, next to roblox-final
cd ~/<title> && rokit install && wally install
python3 ~/roblox-final/.claude/skills/roblox-code/scripts/check.py
claude --add-dir ../roblox-final
```
Then one section per session: "complete the research and plan stage", approve, clear the
chat, "continue with the development of <title>", and so on through section 6. Save reference
images to `docs/images/ref/` and run `/art-brief` between sections 1 and 3.

## 3. Grow it
The spec loop in the game's `docs/workflow.md`: ideas → spec (spec-writer) → approve →
`/build` or map-builder → reviewer → playtest → close out.

## 4. Feed the toolkit
- A reusable script → the owning skill's `scripts/`.
- A design lesson or a game you studied → the vault (`vault/CONTRIBUTING.md`).
- What you learned about yourself as a builder → `private/goals.md` ("Lessons").

# Conventions

The code rules are not restated here. They are owned by the `roblox-code` skill in the toolkit
(`../roblox-final/.claude/skills/roblox-code/`) and apply to every line of this game:

| Rule | Where it is written |
|---|---|
| The five standing rules (disk is the source of truth; pure logic in Core; one transport; cosmetics never break gameplay; every tunable in Config) | `SKILL.md`, "The five standing rules" |
| Server authority, and how each remote is validated | `SKILL.md`, "Server authority"; `references/security.md` |
| Service, controller, remote and spec patterns | `references/patterns.md` |
| Traps (`pcall`, `wait`, Rojo connections, runtime children) | `SKILL.md`, "The traps that cost real days"; `references/traps.md` |
| What "done" means for a build | `../roblox-final/.claude/skills/build/references/quality-bar.md` |

Where this game's code lives (which folder holds services, config, remotes, pure rules) is in
docs/tech/architecture.md.

## This game's own conventions

Only what the skill does not decide. Add to this list as the game settles them.

- PascalCase for modules, services and instances; camelCase for locals and functions.
- Comments explain why, not what.
- CollectionService tags name behaviors, and every tag is in docs/glossary.md.

## Done means

- `python3 ~/roblox-final/.claude/skills/roblox-code/scripts/check.py` is green on all four
  gates (rojo build, lune test, selene, stylua). `check.py --fix` lets StyLua rewrite.
- The BUILD stamp shows in Output on Play.
- Every generated asset is loaded by a line of shipping code
  (`create-roblox-game/scripts/verify_wired.py`).
- The reviewer agent has checked it against the spec and the quality bar.

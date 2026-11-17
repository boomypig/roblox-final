# The shape of a skill and an agent

Every skill and agent has the same five parts. A new one is not finished until each part
exists; `tests/test_structure.py` checks this table against the files.

| Part | What it is | Where it lives |
|---|---|---|
| **Rules** | What must always hold, stated once | The skill's `SKILL.md`. An agent states only how the operating policy applies to it and names its owning skill |
| **References** | The knowledge a step reads, each with its sources and dates | The owning skill's `references/` |
| **Scripts** | What can be run instead of reasoned about. Each script's docstring names the defect it exists for | The owning skill's `scripts/` |
| **Traps** | Failures that happened, with where they were seen. Never invented | A traps section in `SKILL.md`, or `references/traps.md` |
| **Gate** | The test or check that ends the step | A script, named in `docs/workflow.md` |

An agent is a thin entry: its role, its tools, how the policy applies, and the skill that owns
its references, scripts, traps and gate. Agents hold no knowledge of their own, so a fact is
never in an agent and a skill at once.

## Coverage

One row per skill. "Traps" and "Gate" name the heading or file that holds them.

| Skill | Rules | References | Scripts | Traps | Gate |
|---|---|---|---|---|---|
| `pitch` | SKILL.md "Rules" | SKILL.md "References" | `scripts/check_pitch.py` | SKILL.md "Traps" | `check_pitch.py` |
| `art-brief` | SKILL.md "Rules" | SKILL.md "References", `templates/` | `scripts/check_brief.py` | SKILL.md "Traps" | `check_brief.py` |
| `build` | SKILL.md "Rules" | `references/quality-bar.md` | `scripts/check_spec.py` | SKILL.md "Traps" | `check_spec.py`, then roblox-code `check.py` |
| `create-roblox-game` | SKILL.md "THE RUN DOES NOT STOP UNTIL THE GAME IS COMPLETE", "The rules that make a run finish" | `references/` (pipeline, game-plan, mcp, recovery) | `scripts/` (12) | `references/recovery.md`; the trap line of each stage in `references/pipeline.md` | `section.py close N`, `validate.py`, `verify_wired.py` |
| `roblox-build-orchestrator` | SKILL.md "The rule that decides the architecture" | `references/` (stage-briefs, write-boundary) | `scripts/run_log.py` | `references/write-boundary.md` | `run_log.py` debts gate |
| `roblox-code` | SKILL.md "The five standing rules" | `references/` (patterns, traps, security) | `scripts/` (check, new_project, json_to_luau) | SKILL.md "The traps that cost real days", `references/traps.md` | `check.py` (rojo build, lune test, selene, stylua) |
| `roblox-map` | SKILL.md "THE TWO RULES THAT MATTER MOST FOR LOOKS" | `references/` (studio-mcp, visual-quality, performance-and-devices, and its own) | `scripts/` | SKILL.md "Traps, all measured", "Known gaps" | `prove.py`, `verify_build.lua` |
| `roblox-ui` | SKILL.md | `references/` (ui-ux, ui-recipes, theme) | `scripts/` | SKILL.md "Iterate on `verify_ui.py`, not on the mockup" | `verify_ui.py`, `verify_labels.py` |
| `roblox-3d-model` | SKILL.md | `references/` (traps, licences, routes) | `scripts/` | `references/traps.md` | SKILL.md "Verify before believing", "Mesh verification scripts" |
| `roblox-texture-gen` | SKILL.md | SKILL.md | `scripts/` | SKILL.md | SKILL.md "5. Verify" |
| `roblox-animation` | SKILL.md "Read this first: the trap that wastes the most time" | `references/` | `scripts/` | `references/traps.md` | SKILL.md "3. Render and verify" |
| `roblox-vfx` | SKILL.md "RULE ZERO: no shortcuts, ever" | `references/` (game-feel and its own) | `scripts/`, `sim/` | SKILL.md "RULE ZERO: no shortcuts, ever" | SKILL.md "The verify loop" |
| `roblox-sfx` | SKILL.md "The rule that shapes everything" | SKILL.md | `scripts/` | SKILL.md "Traps" | SKILL.md "The three gates" |
| `roblox-skills-setup` | SKILL.md "Rules" | SKILL.md | `scripts/check_setup.py` | SKILL.md "Step 4: the VFX library (explain this, it surprises people)" | SKILL.md "Step 5: smoke test" |

| Agent | Owning skill | Gate it ends on |
|---|---|---|
| `spec-writer` | `build` | `build/scripts/check_spec.py` |
| `reviewer` | `build` | none of its own; it reports on `check.py`, `validate.py`, `verify_wired.py` |
| `map-builder` | `roblox-map` | the builder's Luau checks and the brief's check views |
| `roblox-asset-map` | `roblox-map` | `prove.py` report |
| `roblox-asset-mesh` | `roblox-3d-model` | its manifest |
| `roblox-asset-ui` | `roblox-ui` | `verify_ui.py` |
| `roblox-asset-anim` | `roblox-animation` | its verification renders |
| `roblox-asset-vfx` | `roblox-vfx` | its manifest |
| `roblox-asset-sfx` | `roblox-build-orchestrator` | its manifest with a licence per file |
| `roblox-market-scout` | `roblox-build-orchestrator` | its findings file with sources |

## Names

Names follow how a thing is started, and no existing name changed:

- Commands the user types are short verbs: `/pitch`, `/art-brief`, `/build`.
- Skills Claude loads for a domain are `roblox-<domain>`; `create-roblox-game` is the front door.
- Agents the user asks for by role are role names: `spec-writer`, `map-builder`, `reviewer`.
- Workers the orchestrator spawns are `roblox-asset-<domain>` and `roblox-market-scout`.

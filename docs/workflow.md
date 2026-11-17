# From idea to published game

The one path a game takes through this toolkit: where each skill and agent sits in it, what it
reads, what it writes, and the gate that ends it. There is no second way to build. A game repo
does not carry its own copy of this file; its `CLAUDE.md` points here.

## Operating policy

One policy for every skill and agent. A skill or agent states only how the policy applies to
it; this section owns the wording.

1. **You approve once, in writing.** A pitch you pick, a brief or spec you set to
   `Status: approved`, a section you approve after its gate passes. Nothing is built from a
   draft, and an approved doc is not reopened by the thing building from it.
2. **Inside a task nobody stops to ask.** A task is one section, one `/build`, one map pass,
   one brief or spec draft, one pitch run. When a detail is open, take the option closest to
   the approved doc and keep going.
3. **Open details are logged as assumptions, where the next reader will see them:**
   `**Assumption:**` in a draft brief or spec; "judgment calls" in an agent's report;
   `docs/decisions.md` in the game for a call that outlives the task; the run ledger
   (`run_log.py event`) during a build.
4. **Never offer options.** Choosing between them is the work. Decide, and say why.
5. **The gate is the only stopping point.** A task ends when its gate passes (table below). It
   does not pause earlier to summarise or check in, and it does not start the next task after.
6. **The only asks.** Ask, once, only when:
   - an action cannot be undone or leaves this machine (deleting something someone built,
     publishing, uploading, spending);
   - only you can know the answer (your goals, your reference images, machine paths and keys
     during setup);
   - it is purely mechanical and nothing of the agent's can reach it (pressing Play, clicking
     Publish, approving a tool call, restarting a stuck MCP server, saving a pasted image).

   An agent that cannot ask (a subagent) leaves the thing alone and puts it in its report. It
   stops early only when approved docs contradict each other or the same step fails twice.

A missing precondition is not a question: a spec that is not approved, a `private/` file that
does not exist, a tool that is not installed. Say what is missing, do what the step says to do
then, and continue or end.

## The path

```
 choose        /pitch ─────────────► you pick one
 start         tools/new_game.py ──► a game repo, green on every gate
               (an existing game: adopt.py ──► its layout map and contract, nothing moved)
 1 design      create-roblox-game ─► design/game.json            gate: validate.py
   the look    /art-brief ─────────► art direction, map, UI briefs     gate: you approve
 2 loop        roblox-code, roblox-map (blockout) ─► played on grey parts   gate: check.py
 3 world       roblox-map, roblox-3d-model, roblox-texture-gen, roblox-ui, map-builder
 4 motion      roblox-animation, roblox-vfx, roblox-sfx
 5 assembly    create-roblox-game, reviewer ─► wired, played by two clients
 6 publish     create-roblox-game ─► live
 change        spec-writer ► you approve ► /build or map-builder ► reviewer   (any time after 2)
```

Sections 1 to 6 are driven by `create-roblox-game`, one section per session; you approve each
and clear the chat. "Change" is the same path at the size of one feature: it is how a mechanic
is added or reworked once the loop exists, during the build or after launch.

| Step | Run by | Reads | Writes | Gate that ends it |
|---|---|---|---|---|
| **Choose** | `/pitch [constraints]` | `private/goals.md`, `vault/INDEX.md`, `private/trends/latest.md`, the shortlisted genre files | `private/pitches/<date>.md`: five scored pitches | `check_pitch.py` passes; you pick one |
| **Start** | `python3 tools/new_game.py "<Title>"` | `starter/`, the roblox-code scaffold, create-roblox-game's contract, roblox-map's state template | the game repo: code, contract, `design/layout.json`, docs, `CLAUDE.md`, the Stop hook, `HANDOFF.md` | the four code gates pass on the empty game; `validate.py` refuses it until section 1 fills the contract |
| **Adopt** (an existing game) | `create-roblox-game/scripts/adopt.py --dir <game>`, then `--write` (`references/adopt.md`) | the game's `default.project.json`, code, docs and tool manifest | `design/layout.json`, `docs/tech/layout.md`, the contract skeleton, the starter files it lacks; never `src/` or `tests/` | section 1 closes with its ledger stages ended `adopted`; `validate.py` green |
| **1 Research and design** | `create-roblox-game` ("complete the research and plan stage") | goals, the pitch, the vault, the trends report; web research for gaps (`roblox-market-scout` for fan-out) | `design/game.json` (core loop, plan, asset plan), `docs/pitch.md`, `HANDOFF.md` | `section.py close 1`: `validate.py` green, ledger stages bracketed |
| **The look** | `/art-brief art`, then `map <name>`, `ui` | reference images in `docs/images/ref/`, the pitch, roblox-map's `visual-quality.md` and `performance-and-devices.md`, roblox-ui's `ui-ux.md`, the genre file | `docs/design/art-direction.md`, `docs/design/maps/<name>.md`, `docs/design/ui.md` | `check_brief.py` passes; you set `Status: approved` (before section 3) |
| **2 Code and the playable loop** | `create-roblox-game` → `roblox-code`, `roblox-map` (blockout only) | `design/game.json`, roblox-code's rules | `src/`, `tests/`, a grey blockout in Studio | `section.py close 2`: `check.py` green (rojo build, lune test, selene, stylua); the loop was played |
| **3 World and visuals** | `create-roblox-game` → `roblox-map`, `roblox-3d-model`, `roblox-texture-gen`, `roblox-ui`; the `map-builder` agent dresses in Studio, one zone or pass per run | the approved briefs, `design/map.json`, the asset plan | proven layout (`report.json`, `plan.png`), meshes, UI; dressing in the place file; `docs/design/maps/<name>.state.md` | `section.py close 3`: map, meshes and ui stages `done` with artifacts on disk; each map pass ends on the builder's checks |
| **4 Motion and sound** | `create-roblox-game` → `roblox-animation`, `roblox-vfx`, `roblox-sfx` | the asset plan | animations, the VFX kit, the sound bank | `section.py close 4`: animation, vfx and sfx stages `done` with artifacts |
| **5 Assembly and playtest** | `create-roblox-game`; the `reviewer` agent | everything above | the assembled place, `HANDOVER.md` test matrix | `section.py close 5`: `validate.py --stage-gate`, `verify_wired.py` static and live, `HANDOVER.md`; reviewer findings fixed or listed as debts |
| **6 Publish** | `create-roblox-game` | `design/game.json` publish block | the published place | `section.py close 6`: publish ids recorded; audio and animation confirmed on a live server |
| **Change: spec** | the `spec-writer` agent | the idea, `docs/glossary.md`, `docs/decisions.md`, `vault/INDEX.md` and matching files | `docs/design/mechanics/<name>.md`, `Status: draft` | `check_spec.py` passes; you set `Status: approved` |
| **Change: build** | `/build <spec>` | the approved spec, `design/layout.json`, roblox-code's rules, the quality bar | code and tests, `HANDOFF.md` (short form) | `check.py` green; every acceptance criterion met or marked "needs playtest"; the handoff filled |
| **Change: map pass** | the `map-builder` agent | the approved map brief and art direction, the builder card, the map state file | geometry in Studio, the map state file; the session that ran it writes `HANDOFF.md` (short form) | the builder's Luau checks pass and the check views are captured; the handoff filled |
| **Change: review** | the `reviewer` agent | the diff, the spec or brief, the reviewer card | a report (read-only) | none of its own: it reports on the gates above |

A fan-out build (`roblox-build-orchestrator` with the `roblox-asset-*` workers) is the same
sections 3 and 4 with the asset stages run in parallel; every Studio write stays on one thread.

## Session boundaries

Every session starts cold, so each one ends at a boundary with `HANDOFF.md` written. There are
three: `section.py close N` passes (a section), one map-builder run reports (a map pass), or one
`/build` passes its gates (a build). Outside a section the last two write the short handoff,
`section.py handoff --light map|build`.

A game's `.claude/settings.json` runs `create-roblox-game/scripts/session.py stop` as a Stop
hook. With no boundary it does nothing, and inside a section only `close` counts, so it never
interrupts a section or a one-shot run. At a boundary it refuses to end the session until
`HANDOFF.md` is newer than the boundary and has no unfilled line, and after three refusals it
lets go and records a handoff debt. It adds no prompt and runs in about 20 ms (about 150 ms when
Claude Code runs on Windows and the hook crosses into WSL).

At each boundary it also appends the session's lessons to the toolkit's
`private/lessons-inbox.md`: gate failures, the ledger's stalls, fallbacks and interventions,
and the handoff's debts. That is a file append, never a model step.

## Where each skill and agent sits

| Name | Kind | Step | Started by |
|---|---|---|---|
| `pitch` | skill | Choose | you type `/pitch` |
| `create-roblox-game` | skill, the front door | 1 to 6 | "complete the … stage", "continue with the development of …", "approved" |
| `roblox-build-orchestrator` | skill | 3, 4 (fan-out) | `create-roblox-game`, or you ask for an orchestrated run |
| `roblox-market-scout` | agent | 1 | the orchestrator or section 1, for independent genre candidates |
| `art-brief` | skill | The look | you type `/art-brief art \| map <name> \| ui` |
| `roblox-code` | skill | 2, Change: build | `create-roblox-game`, `/build` |
| `roblox-map` | skill | 2 (blockout), 3 | `create-roblox-game`; `roblox-asset-map` in a fan-out |
| `map-builder` | agent | 3, Change: map pass | you or section 3 ask for one zone or one pass |
| `roblox-3d-model`, `roblox-texture-gen`, `roblox-ui` | skills | 3 | `create-roblox-game`; `roblox-asset-mesh`, `roblox-asset-ui` in a fan-out |
| `roblox-animation`, `roblox-vfx`, `roblox-sfx` | skills | 4 | `create-roblox-game`; `roblox-asset-anim`, `-vfx`, `-sfx` in a fan-out |
| `spec-writer` | agent | Change: spec | you ask for a spec draft |
| `build` | skill | Change: build | you type `/build <spec>` |
| `reviewer` | agent | 5, Change: review | section 5, or you ask after a build or a map pass |
| `roblox-skills-setup` | skill | once per machine | you type `/roblox-skills-setup` |

Names follow how a thing is started: commands you type are short verbs (`/pitch`, `/build`,
`/art-brief`); skills Claude loads for a domain are `roblox-<domain>`; agents you ask for by
role are role names; workers the orchestrator spawns are `roblox-asset-<domain>`.

## Once per machine

1. Open the toolkit in Claude Code and run `/roblox-skills-setup`. It checks Python, Rojo,
   Wally, Lune, Selene, StyLua, Blender and the Studio MCP, and writes each skill's `LOCAL.md`.
2. Trends tracker venv:
   `cd ~/roblox-final/tools/trends && uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt`
   (or `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`).
3. Optional: schedule the tracker (tools/trends/README.md, "Scheduling"). Risers need a week of
   snapshots.

## Choosing a game

- Keep `private/goals.md` current (copy `goals.template.md` the first time; `private/` is
  created as you use the toolkit): answer its `TBD`s when you can; they change every score.
- Refresh market data if `private/trends/latest.md` is missing or more than 3 days old:
  `.venv/bin/python -m trends collect && .venv/bin/python -m trends report`.
- `/pitch [constraints]` writes five scored pitches to `private/pitches/`. Pick one.

## Building it

```bash
python3 ~/roblox-final/tools/new_game.py "<Title>"     # ~/<title>, next to the toolkit
cd ~/<title> && rokit install && wally install
python3 ~/roblox-final/.claude/skills/roblox-code/scripts/check.py
claude --add-dir ../roblox-final
```

A game made before the toolkit is adopted instead of remade:
`python3 ~/roblox-final/.claude/skills/create-roblox-game/scripts/adopt.py --dir <game>` shows
what it found; `--write` adds the layout map, the contract skeleton and the starter files, and
never touches the code (`create-roblox-game/references/adopt.md`).

Then one section per session: "complete the research and plan stage", approve, clear the chat,
"continue with the development of <title>", and so on through section 6. Save reference images
to `docs/images/ref/` and run `/art-brief` between sections 1 and 3. Play the loop on grey
parts before any art is built: art on an unplayed loop gets rebuilt.

## Changing it

1. The idea goes in `docs/ideas.md`. It is not approved by being written down.
2. "Use the spec-writer agent to draft <name>." Edit the draft until it is right, then set
   `Status: approved`.
3. `/build <name>` for code; "use the map-builder agent to greybox zone 1 of
   docs/design/maps/<name>.md" for a map pass, one zone or one pass per run; an asset skill by
   name for one asset ("use roblox-ui to make a shop screen").
4. "Use the reviewer agent on these changes."
5. Playtest in Studio: `rojo serve`, Connect, Play, the BUILD stamp in Output, two clients for
   anything multiplayer.
6. Close out: the spec becomes `Status: built`, decisions go to `docs/decisions.md`, a finished
   map is saved to file and committed under `maps/`.

## Feeding the toolkit

- A script the next game would need goes in the owning skill's `scripts/`.
- A design lesson, or a game you studied, goes in the vault (`vault/CONTRIBUTING.md`); a case
  study of a named game goes in `private/case-studies/`.
- A lesson about a tool goes in that skill's traps.
- What you learned about yourself as a builder goes in `private/goals.md` ("Lessons").

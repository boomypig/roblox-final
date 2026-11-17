# <Game name>: project brief for AI assistants

<fill in at section 1: one or two lines on what the game is.> Full concept: docs/pitch.md.
Built with the toolkit in `../roblox-final` (skills, agents, research library). Start every
session with it added: `claude --add-dir ../roblox-final`.

**Status lives in HANDOFF.md, not here.** Read it first, in full: what was done last, what is
unproven, and the exact next step. This file holds only what does not change from session to
session. Every session ends at a boundary (a section closes, one map pass reports, or one
/build passes its gates) with HANDOFF.md written; the Stop hook in `.claude/settings.json`
refuses to end one without it.

## Task -> file

Load only the row for the task at hand.

| Task | Read |
|---|---|
| Know where the game stands | `HANDOFF.md` |
| Design research | `../roblox-final/vault/INDEX.md`, then only the files it names for the task |
| The concept, the build contract | `docs/pitch.md`; `design/game.json` (gate: `validate.py`) |
| A mechanic spec | `docs/design/mechanics/_template.md`; the spec-writer agent |
| Code | `design/layout.json` (where code lives), `docs/tech/conventions.md`, the `roblox-code` skill |
| The look | `docs/design/art-direction.md`, `docs/design/ui.md` (written with `/art-brief`) |
| A map | `docs/design/maps/<name>.md` (brief) and `<name>.state.md` (the map-builder's state) |
| Names | `docs/glossary.md` |
| Settled choices | `docs/decisions.md`; don't relitigate them |
| Review | the reviewer agent; `../roblox-final/.claude/skills/build/references/quality-bar.md` |
| The whole path, and the operating policy | `../roblox-final/docs/workflow.md` |

## Stack

- Luau, synced to Studio with Rojo (`default.project.json`); where each kind of code lives is
  `design/layout.json`. Tools pinned in the manifest it names; run them from WSL.
- Git owns code and `design/`. Studio (the place file) owns map dressing and inserted assets;
  back maps up as `.rbxm` at milestones.
- Gate before Studio: `python3 ../roblox-final/.claude/skills/roblox-code/scripts/check.py`.

## Hard rules

- The code rules are the `roblox-code` skill's five standing rules and its server-authority
  section; they are not restated here.
- Use the names in docs/glossary.md everywhere (code, comments, docs, Studio).
- Only build from specs and briefs marked `Status: approved`, and from a `design/game.json`
  that passes `validate.py`. docs/ideas.md is NOT approved.
- Inside a task, don't stop to ask: take the reading closest to the approved spec or brief and
  log it in docs/decisions.md as a judgment call. The only stopping point is the task's gate
  (`../roblox-final/docs/workflow.md`, "Operating policy").
- Phone layout first (most players are on mobile; `vault/fundamentals/audience.md`). Change this
  line if this game differs.
- Never commit API keys or tokens. Describe other games' designs; never copy their assets,
  names, or content.

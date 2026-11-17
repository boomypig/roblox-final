# <Game name> — project brief for AI assistants

## What this is
<One or two lines: the game, and what this stage is for.> Full concept: docs/pitch.md.
Built with the shared toolkit in `../roblox-final` (skills, agents, vault). Start every session
with it added: `claude --add-dir ../roblox-final`.

## Current milestone
<M1 — ...> (docs/backlog.md has the active task; HANDOFF.md has the current build section)

## Stack
- Luau, synced to Studio with Rojo (default.project.json). Knit for lifecycle, plain
  RemoteEvents through `src/shared/Net.luau` for gameplay. Layout: docs/tech/architecture.md.
- Toolchain pinned in aftman.toml (rojo, wally, selene, stylua, lune). Run tools from WSL.
- Git owns code and design/. Studio (the place file) owns map dressing and inserted assets;
  back maps up as .rbxm at milestones.
- Gate before Studio: `python3 ~/roblox-final/.claude/skills/roblox-code/scripts/check.py`.

## Hard rules
- The server is authoritative: never trust the client for progress, rewards, currency, or purchases.
- Disk is the source of truth for code: never edit scripts in Studio or over MCP.
- Use the names in docs/glossary.md everywhere (code, comments, docs, Studio).
- Only build from specs and briefs marked `Status: approved`, and from a `design/game.json`
  that passes `validate.py`. docs/ideas.md is NOT approved.
- Follow docs/tech/conventions.md. Never commit API keys or tokens.
- Inside a task, don't stop to ask: take the reading closest to the approved spec or brief and
  log it in docs/decisions.md as a judgment call. The only stopping point is the task's gate
  (../roblox-final/docs/workflow.md, "Operating policy").
- Phone layout first (most players are on mobile; vault/fundamentals/audience.md). Change this
  line if this game differs.
- Describe other games' designs; never copy their assets, names, or content.

## Where things are
- ../roblox-final/docs/workflow.md — the path from idea to published game, and the operating policy
- docs/pitch.md — the concept (from a `/pitch` file in ../roblox-final/private/pitches/ when it exists, or written here)
- design/game.json — the build contract every stage reads; BUILD.md — stage checklist
- docs/design/art-direction.md — the look (written with /art-brief)
- docs/design/maps/<name>.md — one brief per map; docs/design/ui.md — the UI brief
- docs/design/mechanics/ — mechanic specs (copy _template.md)
- docs/tech/ — architecture, conventions
- docs/decisions.md — settled choices and why; don't relitigate them
- docs/images/ref/ — reference images the briefs link to
- ../roblox-final/vault/INDEX.md — shared design vault; read INDEX first and load only what you
  need. Quality bar: ../roblox-final/.claude/skills/build/references/quality-bar.md

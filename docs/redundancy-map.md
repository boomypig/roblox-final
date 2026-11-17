# Redundancy map

Where the same rule or fact was written in more than one file, which file now owns it, and
what happened to the other copy. Line numbers are as of 2026-11-17. "Owner" is the file the
enforcing step reads; every other place points at it.

Status: **done** = consolidated; **phase 3** / **phase 4** = the copy is replaced by a piece of
work those phases deliver, named in the row.

## Workflow and policy

| Rule | Was written in | Owner now | Status |
|---|---|---|---|
| The path from idea to published game | `docs/workflow.md`; `starter/docs/workflow.md` (copied into every game); `starter/README.md`; `README.md` "Where it came from" | `docs/workflow.md` | **done**: the starter copy is removed, `starter/CLAUDE.md` points at the toolkit's doc, `README.md` keeps a summary table that links to it |
| Whether to stop and ask | "the run does not stop", "never offer options" in `create-roblox-game/SKILL.md`; "ask instead of guessing" in `starter/CLAUDE.md`; "ask before writing code" in `build/SKILL.md`; "return up to 5 questions" in `agents/spec-writer.md`; "ask up to 5 questions" in `art-brief/SKILL.md` | `docs/workflow.md`, "Operating policy" | **done**: each of those lines now applies the policy; `tests/test_policy.py` fails on a contradicting line |
| Which names start which thing | `CLAUDE.md` "Which tool for what"; `starter/docs/workflow.md` table; `README.md` | `docs/workflow.md`, "Where each skill and agent sits" | **done** |

## Studio MCP facts

| Fact | Was written in | Owner now | Status |
|---|---|---|---|
| How to enable the built-in server | `create-roblox-game/references/mcp.md:72`; the vault's Studio MCP file | `create-roblox-game/references/mcp.md:72` | **done**: `roblox-map/references/studio-mcp.md:20` points at it |
| Older tool names and their built-in equivalents | `create-roblox-game/SKILL.md` intro block; `CLAUDE.md` | `create-roblox-game/references/mcp.md:75` ("Tool names") | **done**: both now point at the table |
| The tool list | `create-roblox-game/references/mcp.md:55`; the vault file's "Tools for building" | `mcp.md:55` owns the surface; `studio-mcp.md` keeps only how each tool is used for building | **done**; the table is refreshed from the Creator Docs in phase 5 |
| How to build through it: batching, undo recordings, find-or-create, sources, asset vetting, captures, build bugs | the vault file; `agents/map-builder.md:47` (batching), `:51` (source order), `:58` (vetting), `:31` (Layout and Dressing) | `roblox-map/references/studio-mcp.md:54`, `:145`, `:194`, `:123` | file moved (**done**); the agent's restatement is replaced by the builder card in **phase 3** |
| One MCP server and one Rojo connection at a time | `mcp.md:118`; `pipeline.md:20`; `roblox-build-orchestrator/references/write-boundary.md:27`; `CLAUDE.md:60` | `write-boundary.md` (why) and `mcp.md:118` (the run rule) | left as is: the three build-skill passages are each read by a different step and none is required reading for another; `CLAUDE.md` keeps one line |

## Code rules

| Rule | Was written in | Owner now | Status |
|---|---|---|---|
| The five standing rules | `roblox-code/SKILL.md:37`; `starter/docs/tech/conventions.md` (rules 1, 2, 3, 5 restated); `starter/CLAUDE.md:19` "Hard rules" (rule 1) | `roblox-code/SKILL.md:37` | **done** for conventions.md, which now points at the skill and keeps only the game's own conventions. `starter/CLAUDE.md` keeps two one-line hard rules on purpose: it is loaded in every session of a game and the skill is not |
| `task.wait` not `wait`; never a bare `pcall` | `roblox-code/references/traps.md:69`; `starter/docs/tech/conventions.md`; `agents/reviewer.md:26` | `roblox-code/references/traps.md` | **done** for conventions.md; the reviewer's list is replaced by its card in **phase 3** |
| Client and server: every client value is a request | `roblox-code/SKILL.md` "Server authority"; `roblox-code/references/security.md`; `starter/docs/tech/architecture.md:41` | `roblox-code/references/security.md` | **phase 4**: architecture.md is rewritten around `design/layout.json` |
| Where code lives (Core, Config, Net, Services) | `roblox-code/references/patterns.md:7`; `starter/docs/tech/architecture.md:17`; `build/SKILL.md` step 4; `agents/reviewer.md:25` | `design/layout.json` in each game | **phase 4**: `/build`, the reviewer and `check.py` read the layout map instead of assuming one layout |
| How to run a playtest | `docs/workflow.md` "Changing it" 5; `starter/docs/tech/architecture.md:50` | `docs/workflow.md` | **phase 4**, with the architecture rewrite |

## Starting a game

| Thing | Was written in | Owner now | Status |
|---|---|---|---|
| Making a new game | `tools/new_game.py` (102 lines: calls the next one, then overlays `starter/`); `create-roblox-game/scripts/new_game.py` (210 lines: contract, `BUILD.md`, calls the next one); `roblox-code/scripts/new_project.py` (480 lines: the code scaffold) | one `new_game.py` in `create-roblox-game/scripts/`; `tools/new_game.py` stays as the same command | **phase 4**, with the rebuilt starter (hooks, `HANDOFF.md` template, map state template, `design/layout.json`). `new_project.py` is a different job (code only) and stays |

## Maps

| Thing | Was written in | Owner now | Status |
|---|---|---|---|
| Who builds what | `agents/map-builder.md` (builds in Studio); `roblox-map/SKILL.md` (proves a layout headlessly); `agents/roblox-asset-map.md` (runs roblox-map in a fan-out, never touches Studio) | `docs/workflow.md` step 3; each agent states its side | **done**: `map-builder` says it never moves a proven `Layout` part and that layout proof is roblox-map's; the three do not overlap in what they write |
| Default-grey and Plastic checks | `roblox-map/scripts/luau/verify_build.lua`; `agents/map-builder.md:36` ("No default gray Plastic") as prose | `verify_build.lua` | **phase 3**: the builder's Luau checks reuse its logic |
| "Does this look default?" checklist, budgets, build bugs | `roblox-map/references/visual-quality.md`, `performance-and-devices.md`, `studio-mcp.md` (read in full before every run, about 24,000 tokens) | the same three files | **phase 3**: one builder card carries every item with its source; the full file is opened only when a check fails |

## Review

| Check | Was written in | Owner now | Status |
|---|---|---|---|
| Stages marked done have artifacts; the contract is complete | `create-roblox-game/scripts/validate.py:13`; `agents/reviewer.md` (ran it and re-described it) | `validate.py` | **done**: the reviewer runs it and reports its first error |
| Generated assets and labels are used by shipping code | `create-roblox-game/scripts/verify_wired.py:21`; `agents/reviewer.md:29` ("Wiring", by eye) | `verify_wired.py` | **done**: the reviewer reports the script's output instead of re-deriving it |
| Code gates | `roblox-code/scripts/check.py`; `agents/reviewer.md:14`; `build/SKILL.md` step 5 | `check.py` | **done**: both run it; neither restates what it checks |
| Quality bar | `vault/fundamentals/quality-bar.md`; restated in part in `starter/docs/tech/conventions.md` "Done means" | `build/references/quality-bar.md` | **done** |

## Research index

| Thing | Was written in | Owner now | Status |
|---|---|---|---|
| The list of research files and when to read each | `vault/INDEX.md` (one long table, loaded first by five steps) | `vault/CATALOG.md` (full), `vault/INDEX.md` (short) | **done**: the lint fails if a catalogued file is not named in the short index |

# Workflow: building with AI

You decide; the AI drafts and builds; you test. Two modes, same tools:

- **Build the game (sections 1–6).** create-roblox-game takes the game from pitch to publish,
  one section per session, with `HANDOFF.md` carrying memory between sessions.
- **Grow the game (after launch, or one feature at a time).** The spec loop below.

Every session: `claude --add-dir ../roblox-final`.

## Build the game

| Section | Say | What happens | Shared tools it uses |
|---|---|---|---|
| 1 Research and design | "complete the research and plan stage" | Reads docs/pitch.md, the vault and the trends report, fills `design/game.json` (core loop, 23-section plan, asset plan) | vault, `/pitch` file, market-scout only for gaps |
| — The look | `/art-brief art`, then `/art-brief map <name>`, `/art-brief ui` | Turns your reference images into briefs with real values. You approve them | art-brief |
| 2 Code + playable loop | "complete the code stage" | roblox-code scaffold → systems → greybox map → **play the loop on grey parts** | roblox-code, roblox-map |
| 3 World and visuals | "complete the art stage" | Proven map layout, meshes + textures, UI; map-builder dresses from the brief | roblox-map, roblox-3d-model, roblox-texture-gen, roblox-ui, map-builder |
| 4 Motion and sound | "complete the sound stage" | Animation, VFX, SFX | roblox-animation, roblox-vfx, roblox-sfx |
| 5 Assembly + playtest | "complete the playtest stage" | Wiring gate, two-player playtest, HANDOVER.md test matrix | reviewer agent, vault quality bar |
| 6 Publish | "complete the publish stage" | Open Cloud publish, live-server check | create-roblox-game |

After each section: read the summary, say "approved", then clear the chat. Next session, say
"continue with the development of <game>" and it resumes from `HANDOFF.md`.

## Grow the game

1. **Idea → docs/ideas.md.** No commitment.
2. **Spec → docs/design/mechanics/<name>.md.** Copy `_template.md`, or "use the spec-writer
   agent to draft <name>". You edit it until it's right, then set `Status: approved`.
3. **Backlog → docs/backlog.md.** One task = one spec, one map pass, or one small change.
4. **Build.**
   - Code: `/build <spec name>`. Implements the spec, runs the four code gates, reports which
     acceptance criteria pass.
   - Map: "use the map-builder agent to greybox zone 1 of docs/design/maps/<name>.md". Playtest
     the greybox, then ask for the dressing pass. One zone or one pass per run.
   - Assets: call the skill by name ("use roblox-ui to make a shop screen").
5. **Review.** "use the reviewer agent on these changes": spec, rules, gates, vault quality bar.
6. **Playtest (you, in Studio).** `rojo serve` → Connect → Play, BUILD stamp in Output, two
   clients for anything multiplayer. Bugs: paste the exact Output error and what you did.
7. **Close out.** Spec → `Status: built`; decisions → decisions.md; finished map → Save to
   File → commit the .rbxm under maps/; commit and tick the backlog item.

## Rules of thumb
- Play the loop on grey parts before any art is built. Art on an unplayed loop gets rebuilt.
- Small tasks beat big ones. "Greybox zone 1" > "build the map".
- If the AI gets something wrong twice, the spec or brief is probably unclear: fix the doc.
- If you change your mind, update the doc first. Stale docs get followed confidently.
- Save the place to disk (File > Save to File) before a section and at the end of it.
- New session per task or section keeps context clean; the docs carry the memory.

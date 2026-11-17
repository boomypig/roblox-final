---
title: Escape and story obby
type: genre
read-when: Building an "escape the ___" or story obby with a named antagonist, themed rooms and chase set-pieces.
last-researched: 2026-10-22
---

# Escape and story obby

## In one line

A short, linear obby told as a story: you're trapped (prison, school, house, shop), a named
antagonist is on shift, and you escape through themed rooms that end in a chase and a payoff.
Theme, character and set-pieces carry it more than jump difficulty. Movement and checkpoint
rules come from [obby-classic](obby-classic.md); read that file for gaps and respawn.

## Core loop

- **Moment to moment:** easy-to-medium jumps and simple puzzles inside a themed room, with the
  antagonist visible, patrolling or taunting.
- **Run (15–30 min, inferred):** 10–20 rooms with a checkpoint each. The pace rises toward a
  chase where the antagonist pursues and the player sprints a scripted path. The ending is a
  confrontation, a cutscene, a badge and an "ESCAPED" screen.
- **Long term:** badges and hidden collectibles, skins/morphs, alternate modes and seasonal or
  sequel chapters. Barry's Prison Run has 9 badges and ran a LEGO mode with 10 collectibles in
  2025-04 (community, RoWatcher).

## Main verbs

Run, jump, hide/sneak, press a button or lever to open the next room, dodge a patrolling
character, sprint from a chase, find secrets.

## Why players come back

The first run is the product. Returns come from things the first run reveals but doesn't finish
(inferred):
- Badges and hidden items seen but not collected; show a "3/10 found" counter at the end.
- A faster time: an end-screen timer and a server best-time board.
- Skins or morphs earned by finishing, used on the next run.
- A new chapter or seasonal mode. Barry's Prison Run got a LEGO mode (2025-04), Roblox's "The
  Hatch" event (2025-07-02) and "The Takeover" (2025-09-12) (community, RoWatcher).

## What separates top games from clones

| Top games | Clones |
|---|---|
| One original antagonist with a clear personality, shown on the icon | A meme or celebrity character, or someone else's mascot |
| Each room has its own idea (laundry, cafeteria, vents) | 20 identical platform rooms with a prison skybox |
| A chase that is scripted, readable and fair | A chaser with random pathfinding that kills from off-screen |
| A satisfying ending: cutscene, badge, reward | The game just stops, or teleports you to the lobby |
| Difficulty a 9-year-old on a phone can finish | Precision jumps that block the story |

Barry's Prison Run spawned many reskins that keep the "Barry" format with a new guard; some
credit the original in their descriptions (community, Roblox game pages 2026-10). Only the
original is charted (data, 2026-10-22).

## Session shape

- **Typical session:** one full run, about 15–30 min (inferred). Dig to Escape states an average
  playtime of 30–60 min+ (official game description, 2026-10).
- **First 60 s:** an intro of 5–10 s at most (the antagonist, the goal, "escape!"), then control.
  First jump within 15 s; first room cleared within 60 s (inferred; see
  [first-time experience](../fundamentals/first-time-experience.md)).
- **First 10 min:** about a third of the rooms, one scripted scare or near-miss, and the first
  badge (inferred).
- **Day 7:** most players have finished. Retention depends on badges, skins, modes and the next
  chapter, so plan chapter 2 before launch (inferred; see [retention](../fundamentals/retention.md)).

## Social hooks

- Servers of about 12 run the story together. Barry's Prison Run caps servers at 12 (data,
  2026-10-22). Seeing others get caught is part of the fun (inferred).
- Co-op rooms: a lever one player holds while others pass; group buttons like Flood Escape 2's,
  which need several players at once (community, FE2 wiki).
- End-of-run screen with time and deaths that friends can compare (inferred).

## Monetization that works here

| Product | Notes (inferred unless tagged) |
|---|---|
| Skip room (developer product) | Same rules as [obby-classic](obby-classic.md#monetization-that-works-here): offer only after 5+ deaths or 60+ s stuck |
| Free skip via rewarded video ad | Roblox suggests ad rewards worth about R$3–10, placed "after losing a life" (official, 2026-10) |
| Skins / morphs (play as the guard, alternate outfits) | Story-friendly cosmetics; the best seller fits the theme |
| Speed / gravity coil passes | Make the run easier; fine in a solo story, label them |
| Radio / emote / effect passes | Cheap cosmetic extras |

- Don't sell power over other players (pushing, trapping) in a story obby: it ruins the run for
  the 11 others (inferred).
- Barry's Prison Run has 105.25M favorites from 4.75B visits, a 2.2% favorite-per-visit rate,
  against 0.04% for Tower of Hell (data, 2026-10-22). An in-game favorite prompt is the likely
  cause (inferred, unverified). Its like ratio is 61% (data, 2026-10-22). Don't trade likes for
  favorites by nagging.

## Common failure modes

- **Too hard for the audience.** Story players want to see the ending, not master jumps. Keep
  every jump in the Easy/Medium bands of [obby-classic](obby-classic.md#movement-tuning-and-jump-gap-math)
  (inferred).
- **Unfair chase:** a chaser faster than `WalkSpeed`, a catch radius bigger than the model, or
  pathfinding that cuts corners. Players can't learn it, so they blame the game (inferred).
- **Long cutscenes** that can't be skipped on a second run (inferred).
- **One-and-done** with nothing after the ending (inferred).
- **IP risk:** "Run from [meme person / brand mascot]" reskins (see What NOT to copy).
- **Horror overshoot:** strong jump scares in a game aimed at under-13s. Answer the Maturity &
  Compliance questionnaire honestly ([metadata](../fundamentals/metadata-thumbnails-icons.md)) and
  keep scares mild (inferred).

## Saturation & opportunity

Single snapshot (data, 2026-10-22).

- **Barry's Prison Run** is the only charted escape/story obby: 7,999 players, 4.75B visits,
  trending-in-obby-and-platformer #2, created 2022-02-02, updated 2026-10-14. RoWatcher reports a
  65K all-time peak in 2025-07 (community, unverified).
- `prison` theme: 2 games, 14K players, Barry's 57%. The other is Prison Life, which isn't an obby.
- The `escape` keyword theme (7 games, 61K) is mostly "+1 Speed ___ Escape" incremental games, not
  obbies. See [plus-one-stat](plus-one-stat.md).
- Roblox's **Survival / Escape** subgenre (8 games, 296K players) is chase horror: DOORS, Dandy's
  World, Dig to Escape (3,944 players, 98% likes, a prison dig-and-escape with a patrolling guard).
  The "escape a character" fantasy lives there at scale ([horror](horror.md)).
- Seasonal story obbies chart briefly: 20 Doors Till Midnight (20 Halloween levels, 2,530 players,
  created 2026-09-26) (data, 2026-10-22).
- Read (inferred): one 4-year-old leader and a quiet field. The opening is an original character
  plus a stronger second loop (co-op rooms, collectibles, a dig/stealth verb like Dig to Escape)
  or a seasonal one-off timed for an event, not another reskin of Barry's.

## Scope for a solo dev

**MVP (3–4 weeks, no artist; inferred):**
- 12 themed rooms built from primitives and built-in materials, with a checkpoint each.
- One antagonist: an R15 rig with original colors and props, a simple taunt animation, voice lines
  as on-screen text (no voice actor needed). Static or patrolling NPCs use an `AnimationController`
  where they don't need a `Humanoid` (official perf guidance, 2026-10).
- 2 set-pieces: a patrol room (avoid the sight cone) and a final chase on a fixed path.
- Ending: a 5–8 s cutscene, badge, "ESCAPED in mm:ss", a skin reward.
- Skip product, 3 skins, end-of-run favorite/like reminder shown once.

| Week | Build |
|---|---|
| 1 | Movement lock, checkpoints, rooms 1–4, antagonist model and taunt |
| 2 | Rooms 5–12, patrol room |
| 3 | Final chase, ending, badges, collectibles, skip, skins |
| 4 | Phone playtests of the full run, cutscene skip, icon/thumbnail with the antagonist, launch |

**Cut:** a lobby hub, currencies, multiple endings, voice acting, pets. **After launch:** a mode
or chapter every 3–4 weeks (inferred).

## Top examples

- Barry's Prison Run: escape a prison during a lazy guard's shift, first person by default with
  third person optional; 9 badges; LEGO mode and two Roblox events in 2025 (official game
  description; community, RoWatcher).
- Dig to Escape: prison escape as a dig-down survival game with a night-patrolling guard and chase
  music; 98% likes (data and official description, 2026-10-22).
- 20 Doors Till Midnight: seasonal 20-level Halloween story obby (data, 2026-10-22).
- For chase horror at scale see case study: doors.

## Build checklist for agents

### Do

- Use the obby movement lock and only Easy/Medium gap bands from
  [obby-classic](obby-classic.md#movement-tuning-and-jump-gap-math).
- Put a checkpoint at every room entrance; respawn in ≤ 1 s.
- Give control within 10 s of joining; make every cutscene skippable after the first view.
- Script chases on a fixed path. Chaser speed 12–14 studs/s against the player's 16, catch radius
  ≤ 3 studs, and 2–3 s of head start (inferred values; tune in playtests).
- Telegraph patrol sight cones on the floor (colored decal or beam) and use a sound cue before
  the antagonist turns.
- End with a payoff: cutscene ≤ 8 s, badge, time, unlock, and the "X/10 secrets found" counter.
- Make the antagonist original and put it on the icon and thumbnail.
- Grant skips and skins only in `MarketplaceService.ProcessReceipt`; validate room progress on the
  server as in obby-classic.
- Test the full run on a phone-sized viewport with Studio MCP; a new player must finish in
  ≤ 30 min.

### Don't

- Don't use real people, memes of real people, brand mascots or other games' characters (Barry
  included), names or room designs.
- Don't add precision jumps (> 80% of max gap) or 1-stud beams on the story path.
- Don't let a chaser use free pathfinding that can corner players unseen, or move faster than
  `WalkSpeed`.
- Don't sell items that let one player trap or fling others.
- Don't prompt for favorites or purchases more than once per run.
- Don't put strong gore or scares in a game whose maturity label says otherwise.

## Sources

1. https://www.roblox.com/games/8712817601 — Barry's Prison Run description: premise, first person by default (official game page)
2. https://rowatcher.com/games/3310460039 — Barry's peak (65K, 2025-07), badges, LEGO mode, Hatch and Takeover events (third-party tracker)
3. https://www.roblox.com/games/17681465299/MECH-BARRYS-PRISON-RUN — example reskin crediting the original
4. https://www.roblox.com/games/92122513197996 — Dig to Escape description: playtime, guard patrol, chase music
5. https://flood-escape-2.fandom.com/wiki/Buttons — group buttons requiring several players
6. https://create.roblox.com/docs/production/promotion/rewarded-video-ads — ad reward value and placement guidance
7. https://create.roblox.com/docs/reference/engine/classes/StarterPlayer — camera and movement defaults
8. .claude/skills/roblox-map/references/performance-and-devices.md — AnimationController for static NPCs (official guidance cited there)
9. private/trends/latest.md and its 2026-10-22 dated copy — players, visits, favorites, likes, server size, themes and subgenres (data)

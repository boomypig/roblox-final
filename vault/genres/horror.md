---
title: Horror
type: genre
read-when: Building chase, story, or co-op horror (monsters, darkness, scares, procedural rooms, revives).
last-researched: 2026-10-22
---

# Horror

## In one line

Co-op or solo runs through dark spaces where every threat announces itself with one clear cue
and is beaten with one clear counter. Fear comes from anticipation; the scare is the release.
Roblox has no "Horror" genre: list it as **Survival / Escape** (runs) or **Survival / 1 vs All**
(killer rounds) (data, 2026-10-22; see [metadata](../fundamentals/metadata-thumbnails-icons.md)).
Killer-vs-survivor rosters have their own file: [asymmetric-survival](asymmetric-survival.md).

## Core loop

- **Moment to moment (5–30 s):** move into an unknown space → read cues (light, sound, text)
  → act on one counter (hide, look, look away, freeze, run a route) → loot or progress → relief.
- **Session (10–25 min):** one run or chapter. Rooms or areas escalate, with a fixed
  set-piece at milestones (DOORS: rooms 50 and 100) (press, Destructoid 2025-04-28). Death
  returns you to a lobby in seconds with partial rewards.
- **Long-term (days–weeks):** soft currency → pre-run items or characters; badges; harder
  modes and modifiers; new floors, chapters or monsters as updates. DOORS added modifiers after
  beating the game (press, Wikipedia, 2023-08-26). Dandy's World sells progress in "Toons"
  with their own stats and abilities, plus collectible trinkets (data, game description
  2026-10-22).

## Main verbs

Open, explore, hide, listen, look/avoid looking, sprint, crouch, light (flashlight, lighter),
solve (keys, codes, levers), carry, revive, escape. Each threat should map to **one** verb
(inferred, from the DOORS roster in case study: doors).

## Why players come back

- **Mastery of a threat roster.** Each death teaches one rule; the next run goes further.
  DOORS tells players to "use each death as a lesson" (data, game description 2026-10-22).
- **Randomness inside fixed structure.** Random rooms and spawns, fixed milestones (inferred).
- **Friends.** Screaming together is the product; co-op makes fear fun for players who wouldn't
  play horror alone (inferred). DOORS gives a currency bonus per friend in the run (community,
  unverified).
- **Unlocks and lore.** Characters with abilities, cosmetics, hidden rooms, notes and secrets
  feed theories and videos (inferred).
- **Events.** DOORS joined Roblox's 2026 Halloween event The Hollow and sat at 184K players on
  its launch day (data, 2026-10-22).

## What separates top games from clones

- **Readable, fair threats.** Every lethal threat has a telegraph ≥2 s before it can kill and a
  counter the player has already seen (inferred). Unfair deaths read as bugs, not fear.
- **Tension/release pacing.** Quiet stretches, false alarms, and harmless scares between real
  ones. DOORS has pop-out monsters that do no or little damage (press, Destructoid 2025-04-28).
  A DevForum thread warns that overused jump scares desensitize players (community, 2021).
- **Sound carries the game.** Monsters are heard before seen; distinct audio per threat
  (inferred). Top games recommend headphones (data, DOORS description 2026-10-22).
- **Original, memorable monsters** with a strong silhouette and a single gimmick (blind,
  light-sensitive, mimic). The monster *is* the brand and the thumbnail (inferred).
- **Content cadence.** New floors, monsters and chapters, plus seasonal events (see
  case study: doors update table).
- Clones: free-model monsters, one map, spammed jump scares, too dark to see on a phone,
  a hit's names and title pattern (inferred).

## Session shape

- **Typical session:** Dandy's World averages 12.9 min per session over 7 days (community
  tracker Rotrends, read 2026-10-23, unverified). Aim for runs of 10–20 min with a natural
  stop at each floor or chapter (inferred).
- **First 60 seconds:** spawn in a lit lobby → party up or solo queue → in the run within
  30–60 s → first harmless scare or creepy cue by ~60–90 s. No long cutscene; bounce under
  60 s and 61–180 s both count against you (official, see
  [discovery](../fundamentals/discovery-algorithm.md)).
- **First 10 minutes:** meet 2–3 threats, die at least once to a fair one, see the death hint,
  re-queue in under 15 s, earn first currency, see one shop item worth saving for (inferred).
- **Day 7:** has beaten floor 1 or chapter 1, unlocked a harder mode or second character,
  chasing badges and the next floor (inferred).

## Social hooks

- Party queue (friends-only elevator or lobby pad) before each run (inferred; DOORS lobby
  elevators have a friends-only option per the wiki, community).
- Revive downed teammates; spectate the living after death so dead players stay engaged
  (inferred).
- Shared puzzles that need two people (one holds a light, one reads a code) (inferred).
- Clip moments: chase set-pieces and readable jump scares get shared (press: PCGamesN on DOORS
  being "too much for YouTubers", via Wikipedia).
- `SocialService:PromptGameInvite` after a run ends ("bring a friend for the next floor")
  (official API; see [discovery](../fundamentals/discovery-algorithm.md)).

## Monetization that works here

- **Revives / continues** at the moment of loss, with free sources (group join, codes) so
  it isn't pure pay-to-win (data: DOORS description 2026-10-22; inferred).
- **Cosmetics:** skins, emotes, death effects. Forsaken and Dandy's World sell skin and emote
  packs at 100–700 Robux; Violence District sells VIP at 599 (official game-pass API, read
  2026-10-23).
- **Soft-currency packs** for pre-run items or characters (community, DOORS wiki, unverified).
- **Small passes:** 99 Robux seasonal pass (DOORS "BUSTER PASS (HALLOWEEN '26)") (official
  API, read 2026-10-23).
- **Private servers** for friend groups and streamers (inferred). See
  [monetization](../fundamentals/monetization.md), [private-servers](../patterns/private-servers.md).
- Don't sell immunity, monster wallhacks or skip-the-run passes. They remove the fear that is
  the product (inferred).

## Maturity label: what horror content costs you

From Roblox's content-maturity rules (official, 2026-10):

| Content | Lowest label | Who can play |
|---|---|---|
| Any fear: jump scares, creepy NPCs, screaming, heavy breathing, ominous music | **Mild** ("mild fear-based content") | Kids 5–8, Select 9–15, 16+ (after evaluation) |
| Disfigured faces with realistic blood, realistic exposed tissue | Moderate | Select 9–15 and 16+ |
| Any realistic blood, even distant spatter | at least Moderate (light realistic) | Select and 16+ |
| Heavy realistic blood (pools, gushing, close spatter) | Restricted | ID-verified 18+ only |
| Graphic realistic death (dismemberment, impalement) | Restricted | 18+ |
| Off-screen implied violence (sounds only) | counts as mild | — |

- **Minimal allows no fear at all.** A horror game is Mild at best (official, 2026-10).
- A single realistic-consequence moment pushes violence to Moderate or higher (official).
- Frequency: "Repeated" applies if scary elements occur often, or a short burst packs many
  (official). Horror runs are Repeated.
- Unrated games are restricted for everyone; new games start in a **16+ trial** until they
  pass evaluation (250 highly engaged plays in 60 days) (official, 2026-10). See
  [discovery](../fundamentals/discovery-algorithm.md#audience-gating-kids-and-select) and
  [audience](../fundamentals/audience.md).
- **Target Mild** (inferred): stylized monsters, non-red or cartoon "ichor" instead of blood,
  deaths shown as a scream + cut to black or a ragdoll, no realistic wounds. You keep ages 5–15.
- Add a description warning for loud audio and flashing lights, as DOORS and Forsaken do (data,
  descriptions 2026-10-22).

## Darkness, light and sound

Engine facts (official, 2026-10):
- `Lighting.Technology` is deprecated. Use `Lighting.LightingStyle` (`Realistic` or `Soft`) and
  set `Lighting.PrioritizeLightingQuality = true` when shadows matter to the mood.
- `Lighting.Ambient` defaults to black (0,0,0); `OutdoorAmbient` to (127,127,127).
  `ExposureCompensation` ranges −5 to 5.
- `PointLight`/`SpotLight`/`SurfaceLight` `Range` is clamped to **120 studs**.
- Fog properties are hidden when `Lighting` contains an `Atmosphere`; use `Atmosphere.Density`,
  `Color`, `Haze` instead.
- Shadows switch off below graphics quality 4, so **never make a shadow a gameplay cue**
  ([performance](../../.claude/skills/roblox-map/references/performance-and-devices.md)).
- `Highlight` renders at most 255 at once per client.

Starting values for an indoor horror map (inferred, tune on a phone):

| Property | Value |
|---|---|
| `LightingStyle` | `Realistic` |
| `ClockTime` | 0 (or interiors with no sky exposure) |
| `Brightness` | 0–1 |
| `Ambient` / `OutdoorAmbient` | (10,10,15)–(25,25,35) / (20,20,30)–(40,40,55) |
| `ExposureCompensation` | −0.5 to −1 |
| `Atmosphere.Density` | 0.35–0.5, dark blue-grey `Color` |
| `ColorCorrectionEffect` | `Saturation` −0.2 to −0.4, `Contrast` 0.1–0.2 |
| Flashlight (`SpotLight` on the character) | `Range` 40–60, `Angle` 45–70, `Brightness` 1–2, `Shadows = true` on the local player's light only |
| Room lights (`PointLight`) | `Range` 12–20, `Shadows = false` on all but 1–2 key lights |

- Keep interactables readable without a flashlight: an emissive (`Neon`) accent or a
  `Highlight` within ~10 studs (inferred).
- Offer a client-side brightness slider (adjust a local `ColorCorrectionEffect.Brightness`);
  phone players at low screen brightness will quit otherwise (inferred).
- Flicker lights by toggling `Enabled` or tweening `Brightness` **on the client**; the server
  fires one event (official guidance on client-side tweens, see
  [performance](../../.claude/skills/roblox-map/references/performance-and-devices.md)).

Sound (official API names; values inferred):
- Positional sounds: parent `Sound` to a part or `Attachment` on the monster. Tune
  `RollOffMinDistance`/`RollOffMaxDistance` (e.g. 10/80 for footsteps) and `RollOffMode`
  (`Inverse`, `Linear`, `InverseTapered`, `LinearSquare`).
- `Sound.Volume` runs 0–10, default 0.5 (official). Route music, SFX and ambience through
  separate `SoundGroup`s and give each a volume slider.
- `SoundService.AmbientReverb` or `ReverbSoundEffect` for halls; `EqualizerSoundEffect` to muffle
  sound behind doors.
- Each threat gets a unique cue that plays ≥2 s before it can hurt anyone. Silence before a
  cue makes it land (inferred).

## Monster design and AI

- **One gimmick, one counter** per monster: blind/sound-tracking, light-sensitive, only moves
  when unseen, mimic, rusher that kills anyone not hidden (inferred, from the DOORS roster).
- **Speed vs player** (default `Humanoid.WalkSpeed` 16, official). Starting values (inferred):
  - Roaming stalker: 10–14 studs/s. A player who notices it can always walk away.
  - Hunting chase: 0.9–1.1× the player's sprint (sprint 20–22). Escape depends on route and
    counters, not raw speed.
  - Scripted chase set-piece: 1.05–1.15× sprint on a fixed route, 20–45 s long, with the
    correct path marked.
  - Rusher (passes through rooms): 60–120 studs/s, but only after a ≥2–3 s telegraph.
- **Pathfinding:** server `Script`, `PathfindingService:CreatePath({AgentRadius, AgentHeight,
  AgentCanJump, Costs})`, `Path:ComputeAsync`, `Path:GetWaypoints`, `Path.Blocked`. Limits:
  3,000-stud line-of-sight distance and a 20,000-node budget (official). Use
  `PathfindingModifier` (`PassThrough` for doors) and `Label` costs to keep monsters out of
  safe rooms (official).
- Recompute the path every 0.25–0.5 s while chasing; between recomputes, if
  `Workspace:Raycast` shows clear line of sight, move straight at the target (inferred).
  `Humanoid:MoveTo` times out after 8 s, so re-issue it (official).
- Call `SetNetworkOwner(nil)` on the monster's root so no client controls it (official, see
  [security](../../.claude/skills/roblox-code/references/security.md)).
- **Kills and hiding are server decisions:** check distance and the player's server-side
  `Hidden` state on the server at ~10 Hz. Never kill on client `Touched`, and never let the
  client declare itself hidden (official principle; implementation inferred).
- Validate hide prompts: `ProximityPrompt.Triggered` gets a server distance check, but
  re-check state and cooldown yourself (official).

## Procedural rooms for replay

- Build 15–30 room templates as `Model`s with `Entrance` and `Exit` attachments and a
  `PrimaryPart`. Chain them with `Model:PivotTo` so each entrance meets the previous exit
  (inferred; DOORS-style).
- Seed each run with `Random.new(seed)` and log the seed, so bugs reproduce (inferred).
- Before placing, test overlap with `Workspace:GetPartBoundsInBox` and an `OverlapParams`
  filter; reroll the template on a hit (inferred).
- Keep only ~3 rooms ahead and 1–2 behind; close doors behind the group and delete old rooms
  (inferred; protects phone memory, see [performance](../../.claude/skills/roblox-map/references/performance-and-devices.md)).
- Fixed set-pieces at milestones (e.g. room 25 and 50) and a guaranteed hiding spot within
  ~30 studs (≈2 s at WalkSpeed 16) of any point in rooms where a hide-threat can spawn
  (inferred).
- Spawn weights per threat rise with room number; never two lethal threats in the first 10
  rooms (inferred).

## Co-op revive

Starting values (inferred): downed state with crawl at WalkSpeed 4; bleed-out 30 s; revive
by holding a `ProximityPrompt` for 3–5 s within 8 studs; the reviver can't move; one free
team revive per floor plus paid self-revive. Dead players spectate living teammates and see the
death hint. Solo players get a checkpoint at each milestone instead of teammates.

## Common failure modes

- Too dark on phones and low graphics; players can't find the door and leave (inferred).
- Deaths without a telegraph, or monsters stuck on furniture (pathfinding agent too big,
  no `Path.Blocked` handling) (inferred).
- Jump-scare spam with max-volume stingers: desensitizes and drives players off (community).
- Long intro or story cutscene before control, which raises 0–60 s bounce (official signal).
- Free-model monsters and jump-scare kits carrying hidden scripts or another game's assets
  (inferred). Never insert models with scripts you haven't read.
- Realistic blood or gore that drops the game to Moderate/Restricted by accident (official
  rules).
- One map, no unlocks: nothing to return for after the first win (inferred).

## Saturation & opportunity

All (data, 2026-10-22) unless tagged:
- **Survival** is the #2 Roblox genre: 1.54M players, 21.9% share, 48 charted games.
  **Escape** subgenre: 296K across 8 games, 93% of it DOORS (184K) + Dandy's World (91K).
  **1 vs All**: 843K across 8 games, 80% of it Murder Mystery 2.
- **`horror` theme:** 27 games, 477K players, 18K per game but a **1.9K median**; DOORS holds
  39%. Labeled "mixed". Horror is in 4 of the top 25, with 11% of top-25 players (inferred line
  in the report).
- **Rising horror:** 3 games, 10.0K players (PINKIE PROMISE 4.9K, HUNTRESS 3.6K, Rust Blaster).
  Rust Blaster is a Halloween-tagged simulator, not horror, so the real wave is smaller.
- **Theme tagging is noisy** (inferred, from our own lookup): Piggy (19.8K), Evade (35.0K) and
  "he ate them. [HORROR]" (10.6K) aren't tagged `horror`; Anime Card Clash and Rust Blaster are.
- **Untracked mini-wave: "(Anomaly)" job sims in Survival.** Animal Hospital (Anomaly) 31.6K
  (created 2026-05-10), Sell Fries! [Anomaly] 30.1K, Clone Baby Care (Anomaly) 15.9K (created
  2026-10-09), Airport Security (Anomaly) 4.5K: ~82K combined. Spot-what-changed horror over a
  work-sim loop is cheap to build and needs no chase AI (inferred). See
  case study: sell-fries, [job-sims](job-sims.md).
- **Seasonality:** 20 charted titles carry a Halloween label and DOORS's peak sits on The
  Hollow's launch (data). Ship horror updates for October; expect quieter months (inferred).
- **Opportunity (inferred):** the median horror game is tiny, so a generic DOORS-like loses.
  Openings: (1) small-party (1–4) co-op runs with one novel monster gimmick; (2) anomaly or
  observation horror layered on a simple job loop; (3) Mild-rated "cute horror" with a
  character roster (Dandy's World's lane) for under-16s. Check [trend lifecycle](../fundamentals/trend-lifecycle.md).

## Scope for a solo dev

**MVP (6–8 weeks, one dev with Claude Code, no artist) (inferred):** lobby with a 1–4 player
party pad, a run of 30–50 rooms from 12–20 templates, 3 threats (one hide, one look/avoid, one
scripted chase), flashlight, hiding spots, death hint screen, a final set-piece escape, a soft
currency with a 4-item pre-run shop, a paid revive, saving, settings (brightness, volume).

| Week | Build |
|---|---|
| 1 | Room template format, seeded generator, lobby → run teleport (reserved server per party), [round-system](../patterns/round-system.md) |
| 2 | Lighting + sound pass, flashlight, hiding closets (server state), brightness slider |
| 3 | Threat 1 (rusher + hide) and the death/hint/requeue loop |
| 4 | Threat 2 (look/avoid) and threat 3 (pathfinding chaser + scripted chase set-piece) |
| 5 | Currency, shop, revive product (`ProcessReceipt`), [player-data](../patterns/player-data.md) |
| 6 | Phone test on a low-end Android, onboarding, metadata, maturity questionnaire |
| 7–8 | Second floor theme or 2 more threats; badges; event-ready Halloween dressing |

- **No artist:** built-in materials, `Neon` accents and darkness hide simple geometry; monsters
  as strong silhouettes (tall, thin, wrong proportions) with emissive eyes and great sound
  (inferred). Read [visual-quality](../../.claude/skills/roblox-map/references/visual-quality.md).
- **Cut:** multiple floors at launch, voiced story, cutscenes, 12-player runs, trading, admin
  panels, PvP (inferred).

## Top examples

- DOORS (case study: doors): co-op room-by-room runs, threat roster with counters;
  184K (data, 2026-10-22, event day).
- Dandy's World: Mild-style "mascot horror", team repairs machines to descend floors, roster
  of Toons with abilities; 91K (data, 2026-10-22). Peak ~620K after an October 2025 update
  (press, games.gg; unverified).
- Piggy: chapter-based story horror (community, unverified); 19.8K, 6 per server (data,
  2026-10-22).
- Evade: chase-survival with a 15-player server; 35.0K (data, 2026-10-22).
- Forsaken (case study: forsaken) and Flee the Facility: killer rounds, see
  [asymmetric-survival](asymmetric-survival.md).

## Build checklist for agents

### Do
- Give every lethal threat a unique cue (sound + light or text) ≥2 s before it can kill, and
  exactly one counter verb.
- Put at least one harmless scare or false alarm between real threats; cap real jump scares
  at ~1 per 3–5 min of play (inferred).
- Keep stalker speed ≤14 and chase speed within 0.9–1.15× player sprint; scripted chases 20–45 s.
- Make kills, hiding and revives server decisions with distance checks; `SetNetworkOwner(nil)`
  on monsters.
- Use `PathfindingService` with `Path.Blocked` handling and re-issue `MoveTo` before 8 s.
- Seed procedural runs with `Random.new(seed)`; guarantee a hiding spot within ~30 studs where a
  hide-threat can spawn.
- Set `LightingStyle`, ambient ≤(40,40,55), a flashlight `SpotLight` ≤60 range, and test on a
  phone at low graphics; ship a brightness slider and per-group volume sliders.
- Put the player in control within 30–60 s of joining; first cue by ~90 s.
- Answer the maturity questionnaire for the worst moment; target Mild (stylized, non-realistic
  blood); warn about loud audio and flashing lights in the description.
- Let dead players spectate and re-queue in under 15 s.

### Don't
- Don't use shadows, tiny audio, or pitch darkness as the only cue for anything lethal.
- Don't kill on client `Touched` or trust a client "I'm hidden" flag.
- Don't tween or flicker lights from the server every frame.
- Don't use realistic red blood or gore unless you accept losing under-16s.
- Don't sell immunity, monster ESP or run skips.
- Don't insert free-model monsters or jump-scare kits with unread scripts.
- Don't reuse another game's monster names, designs, sounds or a "DOORS"-like title and art.
- Don't play max-volume stingers more than once in a row, or flash the screen without a warning.

## Sources

1. private/trends/latest.md, `trends lookup` and the tracker DB — genre/theme numbers, players, server sizes, descriptions (data, 2026-10-22)
2. https://create.roblox.com/docs/production/promotion/content-maturity — fear, violence, blood definitions and label mapping
3. https://create.roblox.com/docs/reference/engine/classes/Lighting.md — Technology deprecated, LightingStyle, Ambient defaults, ExposureCompensation range, fog hidden with Atmosphere, 120-stud light range
4. https://create.roblox.com/docs/environment/lighting — LightingStyle, PrioritizeLightingQuality guidance
5. https://create.roblox.com/docs/characters/pathfinding — agent parameters, Blocked, modifiers, links, 3,000-stud and 20,000-node limits
6. https://create.roblox.com/docs/reference/engine/classes/Humanoid — WalkSpeed 16, MoveTo 8 s timeout
7. https://create.roblox.com/docs/reference/engine/classes/Sound — Volume range, positional sound rules
8. https://create.roblox.com/docs/reference/engine/classes/Highlight — 255 simultaneous highlights
9. https://www.destructoid.com/all-doors-entities-guide-how-to-survive/ — DOORS threat telegraphs and counters (2025-04-28)
10. https://en.wikipedia.org/wiki/Doors_(game) — DOORS history, modifiers, press reception
11. https://devforum.roblox.com/t/good-horror-game-design-tips/1464664 — jump-scare overuse (community opinion)
12. https://devforum.roblox.com/t/horror-lighting-help/2168646 — ambient and exposure tuning for dark scenes (community)
13. https://games.gg/news/roblox-top-games-october-2025/ — Dandy's World ~620K after an October 2025 update
14. https://rotrends.com/game/5569032992 — Dandy's World average session 12.9 min (third-party tracker)
15. https://games.gg/roblox/guides/roblox-the-hollow-2026/ — The Hollow event dates
16. https://apis.roblox.com/game-passes/v1/universes/{universeId}/game-passes — pass prices for DOORS, Forsaken, Dandy's World, Violence District (read 2026-10-23)

---
title: Battlegrounds (anime fighting)
type: genre
read-when: Building an anime fighting / battlegrounds game.
last-researched: 2026-10-22
---

# Battlegrounds (anime fighting)

## In one line

Drop-in free-for-all servers of 15–20 players where everyone picks a character with an M1
chain, four skills and an awakening, and fights for kills. Players come for combos and
spectacle; the developer keeps them by releasing new characters.

## Core loop

- **Moment to moment (1–10 s):** close distance with a dash → M1 chain → finisher (knockback,
  uppercut or downslam) → skill to extend → opponent blocks, counters or ragdoll-cancels → reset.
- **Session (15–40 min):** spawn → fight whoever is near → die → respawn in seconds → fill the
  awakening bar → awaken for about a minute → chase a kill streak → swap character (inferred).
- **Meta (days to months):** learn combos ("techs") for each character, unlock characters and
  emotes, return for each new character drop (inferred from both leaders' update patterns below).

## Main verbs

| Verb | Typical input (PC / both leaders) | Purpose |
|---|---|---|
| M1 | Left click, hold or tap | 4-hit chain; 4th hit knocks back, or becomes an uppercut while jumping and a downslam while falling |
| Skills 1–4 | 1–4 keys, mobile buttons, L1/L2/R1/R2 | Character kit: attacks, grabs, counters, mobility |
| Special | R (JJS) | Fifth utility move on some kits |
| Dash | Q; direction picks forward or side/back | Approach, escape, combo extension |
| Block | F, hold | Frontal guard; some moves pierce it or need a timed block |
| Ragdoll cancel / evasive | Q or side dash while ragdolled | Escape a combo; gated by a meter |
| Awaken | G when the bar is full | Ultimate moveset for a limited time |
| Run | Double-tap W | Map travel |
| Emote | B (emote wheel) | Taunts, clips; main cosmetic sink |

Sources: both games' Roblox pages (community, game pages, 2026-10-23) and the JJS wiki (community, 2026-10).

## Reference tuning: one leader's documented numbers

The Jujutsu Shenanigans (JJS) community wiki documents frame-level values. Use them as a
**starting point** that real players have tested, then tune (community, 2026-10):

| Mechanic | JJS value |
|---|---|
| M1 hitbox | 8×8×8-stud box in front of the attacker, active ~16 ms (one server frame) |
| M1 startup | 0.16–0.23 s, usually 0.2 s |
| M1 hit stun | ~0.75 s; attacker is pulled ~1 stud toward the target |
| M1 chain | 4 hits, 3+3+4+4 = 14 damage, then 2 s downtime |
| Blocked M1 | Double endlag for the attacker |
| Block arc | Under 180° in front; some moves only stopped by blocking before impact |
| Forward dash | ~25 studs, ends in a 4-damage jab; 6 s cooldown |
| Side/back dash | ~17.5 studs, steerable, usable during startup of M1s/skills; 2 s cooldown |
| After ragdoll | ~0.5 s immunity to melee stun |
| Evasive (ragdoll cancel) | 1 s i-frames; meter fills after ~77 damage taken or 200 dealt |
| Health regen | 1 HP/s, starting 1 s after the last hit |
| Awakening | Bar fills after ~286 damage dealt (lost on character swap); lasts about a minute; brief invulnerable intro that restores some health |
| Kit | 4 skills per finished character; tooltip tags (HOLD, USE TWICE, RAGDOLL, TARGET…) explain variants |

The Strongest Battlegrounds (TSB) follows the same shape: a 4-hit M1 whose last hit deals the
most damage, Q to dash and to escape ragdoll, F to block, G for ultimate (press, undated;
community, game page 2026-10-23). Its awakening also comes from a meter built in combat, and
most awakenings expire on a timer (guide site, 2026-06, unverified).

## Hitboxes and netcode

How hits are detected decides whether the game feels fair at 150–250 ms ping. Server-side
validation rules (range, state, cooldown) are in
[security](../../.claude/skills/roblox-code/references/security.md); don't duplicate them.

| Method | API | Verdict |
|---|---|---|
| Box overlap | `Workspace:GetPartBoundsInBox(cframe, size, overlapParams)` | **Default for melee.** Cheap, rotatable CFrame, no instance needed. Uses part bounding boxes, slightly loose on limbs (community, 2025-09). |
| Part overlap | `Workspace:GetPartsInPart(part, overlapParams)` | Exact shape, but needs a hitbox part per attack (community, 2025-09). |
| Radius | `Workspace:GetPartBoundsInRadius(position, radius, overlapParams)` | AoE slams, shockwaves (inferred). |
| Shapecasts | `Workspace:Blockcast`, `Workspace:Spherecast`, `Workspace:Shapecast` | Swept volume for fast lunges and projectiles. Each cast returns only the first hit, so AoE needs several, and cost grows with shape size and distance (official, 2023-05; community, 2025-09). |
| Raycasts | `Workspace:Raycast` | Precise for weapons; many rays per swing to cover volume (community, 2025-09). |
| Touched | `BasePart.Touched` | **Don't.** Unreliable timing, and an exploiter can fire or suppress it on parts they own (community, 2025-09; official, 2026-10). |

Filter with `OverlapParams.FilterType = Enum.RaycastFilterType.Include` on a folder of live
character models, and set `OverlapParams.MaxParts` to bound work (inferred).

**Where to detect.** Roblox's default character replication runs at roughly 20 Hz plus an
interpolation delay, so the attacker and the server disagree on where the target is
(community, 2026-06). At 200 ms ping, client-side box checks reached visibly farther than the
server's view (community, 2026-06). Pick one model and stick to it:

1. **Server detects (recommended start).** The client plays the windup animation immediately and
   sends the intent (`RequestMove(moveId)`). The server checks state and cooldown, waits the
   move's startup on its own clock, then runs the box at server positions. Add 1–2 studs of
   forgiveness to the box to offset lag (inferred). Simple and exploit-resistant.
2. **Client detects, server validates.** The client runs the box at its active frame and sends
   targets; the server re-checks distance with slack and rejects impossible hits. Feels better at
   high ping; costs more validation code (community consensus, 2023–2026).
3. **Custom replication** (for example the open-source Chrono library) replaces default physics
   replication to cut delay. The author says it is client-authoritative and needs your own
   movement checks (community, 2025). Only after the game proves itself.

Store each move as data, not code: startup, active, recovery, damage, stun, knockback,
hitbox size and offset, cooldown, blockable, tags. Both server and client read the same
ModuleScript (inferred). See [ability kits](../patterns/ability-kits.md).

If you opt into `Workspace.AuthorityMode = Server`, check its release limits first (including
the animation-track cap noted in the security file); battlegrounds stack many tracks (inferred).

## Why players come back

- **New characters.** JJS has run 13+ characters through Early Access (community, 2026-10);
  TSB added characters such as Tech Prodigy as Early Access in its 2024-12-21 update and later
  made it free (press, 2024-12 and 2026-05, unverified).
- **Skill expression.** Community "tech" lists for TSB name dozens of combo tricks (dash loops,
  M1 resets) and track which ones got patched (community, 2026-07).
- **Short, social fights.** Respawn in seconds, no match queue, friends in the same server (inferred).
- **Awards and visibility.** TSB's page cites "Best Fighting Experience" at the 2024 Innovation
  Awards; JJS's cites Best Action Experience 2026 (community, game pages, 2026-10-23).

## What separates top games from clones

- **Readable fights.** Every move has a visible windup, a clear active hit and punishable endlag.
  Clones skip endlag and windup, so fights become spam (inferred from JJS endlag rules).
- **Defense with a cost.** Block slows you and blocks no attacks of your own; blocked M1s punish
  the attacker; a meter-gated evasive lets a combo victim escape once (community, 2026-10).
- **Spectacle per second.** Map destruction (JJS's page cites "destruction inspired by combat
  mayhem"), ragdolls, screen shake, hit-stop, awakening intros (community, game page, 2026-10-23).
  See [game feel](../../.claude/skills/roblox-vfx/references/game-feel.md).
- **Movement depth.** Wall jumps limited by HP (3/2/1 at high/mid/low health), auto-vault while
  sprinting, roll on landing (community, 2026-10).
- **Anti-teaming.** JJS lists "Anti-Team" and "Anti-Run" mechanics; one documented effect is a
  burst that refills the evasive meter (community, 2026-10).
- **Build or sandbox modes.** JJS added a private-server Build Mode and a Skill Builder for
  player-made creations (community, 2026-10), which gives clip makers content.

## Session shape

- **First 60 s:** spawn straight into the live map with the free starter character; a 3-line
  control hint (M1, Q, F) and a dummy to hit. No menu wall (inferred; see
  [first-time experience](../fundamentals/first-time-experience.md)).
- **First 10 min:** land a full M1 chain, use all 4 skills, die and respawn, see someone awaken,
  fill your own bar once (inferred).
- **Typical session:** 15–40 min of continuous FFA (inferred).
- **Day 7:** has a main character, knows 2–3 combos, owns or wants an emote, waits for the next
  character (inferred).

## Social hooks

- FFA servers: TSB 15 players, JJS 20, the other charted kit fighters 15–20 (data, 2026-10-22;
  JJS via API 2026-10-23).
- Friends join the same server; private servers for 1v1 practice and combo labs. TSB sells
  "Private Servers+" (499 Robux); JJS gates Build Mode to private servers (data, API 2026-10-23;
  community, 2026-10).
- Emotes and kill effects are the bragging layer; clips of combos and ultimates drive YouTube
  and TikTok (inferred). See [social and virality](../fundamentals/social-and-virality.md).

## Monetization that works here

Game passes read from the Roblox API on 2026-10-23 (data):

| Game | Passes (Robux) |
|---|---|
| TSB | Private Servers+ 499, Early Access 299, VIP 299, Kill Sound 199, Awakening Outfit 99, Extra Emote Slots 99, Emote Second Page 99 |
| JJS | Early Access 345, More Emote Slots 175, More Build Saves 125, Custom Kill Sound 120, Awakening Outfits 115 |

- **Early Access is the anchor.** One permanent pass unlocks every unfinished character as it
  arrives (JJS wiki: "permanent", all future EA movesets) (community, 2026-10). It sells each new
  drop again without selling power forever, because characters go free later (inferred).
- **Cosmetics: emotes, kill sounds, awakening outfits, emote slots.** JJS says no pass other than
  Early Access affects battles (community, 2026-10).
- **Random rewards are disclosed.** TSB's page states equal odds and no duplicates for emote
  spins (community, game page, 2026-10-23). Disclose odds if you add any loot box.
- Add a cheap repeatable developer product (emote spin, cosmetic crate) for spend days
  (see [monetization](../fundamentals/monetization.md)).

## Common failure modes

- **Spam combat:** no endlag, no block punish, cooldowns under ~2 s on big moves (inferred).
- **Infinite combos:** no stun immunity after ragdoll, no evasive. Players quit after one
  unescapable death (inferred; both leaders added escapes).
- **Hitboxes that lie:** client-only detection with no checks, or `Touched`. Hit feels stolen at
  high ping or exploiters hit across the map (community, 2026-06).
- **Pay-to-win characters** that stay paid and stronger (inferred).
- **Ragdoll physics bugs:** flung characters, stuck-in-ground. Keep the target server-owned and
  reset state on a timer (inferred).
- **Effects that kill phones:** stacked particles from 15 players awakening at once (see
  [performance](../../.claude/skills/roblox-map/references/performance-and-devices.md)).
- **Teaming and spawn camping** in FFA with no counter-mechanic (inferred).
- **Copying a manga:** character names, signature moves and looks from a licensed franchise
  invite takedowns. Describe archetypes ("blind sorcerer", "cyborg") in your own art (inferred).

## Saturation & opportunity

- Roblox subgenre **Battlegrounds & Fighting: 44 charted games, 414K players, 5.9% share**
  (data, 2026-10-22). Theme `battlegrounds`: 6 games, 72K players, TSB holds 60% (data, 2026-10-22).
- **The subgenre field is broad.** Its biggest entries include a duel shooter (Murderers VS
  Sheriffs, 74K), a cat ring-out party brawler (Cat Battles, 46K, 17 days old, 10-player rounds,
  crates of cosmetic furs) and a chaser/crossing tag game (Huss Valley, 45K, 52 days old, 30
  players) (data, 2026-10-22; game pages 2026-10-23). **Neither new breakout is an anime kit
  fighter.**
- Anime kit fighters on the charts: TSB 43.6K, ABA 13.3K, Legends Battlegrounds 12.3K, Anime
  Ability Arena 8.4K, Ability Arena 7.4K, Superhero Arena 6.9K, Heroes Battlegrounds 5.1K,
  Ultimate Battlegrounds 2.0K, Shonen Unleashed 1.0K ≈ 100K across 9 games (data, 2026-10-22;
  grouping inferred).
- **Tracker gap:** JJS is not in the snapshot but had ~77K players on a direct API read
  (2026-10-23 04:51 UTC, data). Real kit-fighter demand is ~180K+, split between two leaders.
- Three 2026 kit fighters (created 2026-05 to 2026-09) hold 7–8K each at 88–93% likes (data,
  2026-10-22): a new entry can find a 5–10K niche, not the top (inferred).
- **Opportunity (inferred):** cheaper-to-animate spins on "fighting" are breaking out now: physics
  ring-outs, tag, duels. A kit fighter only makes sense with a clear twist (setting, a single
  mechanic like grabs or ring-outs, or a build/sandbox angle). See
  [trend lifecycle](../fundamentals/trend-lifecycle.md).

## Scope for a solo dev

**Animation is the bottleneck.** No animator means every attack is hand-keyed in the Animation
Editor or generated from video. Roblox's Live Animation Creator (Clip Editor, beta feature) turns
a stable-camera clip **under 15 s** into keyframes, **R15 only** (official, 2026-10). Both leaders
force R6 (data, API 2026-10-23), so video capture can't make R6 sets: pick R15 if you'll rely on it.

Animation budget for the MVP (inferred):

| Set | Clips |
|---|---|
| Shared: 4 M1s, uppercut, downslam, block, block-hit, 2–4 dashes, hit-react ×2, get-up, run | ~14 |
| Per character: 4 skills (windup + strike in one clip) + awaken intro + 1–2 awakened moves | ~6–8 |
| 2 characters total | ~26–30 clips at roughly 1–3 h each hand-keyed, or less with video capture: 40–80 h |

**MVP:** one 300×300-stud arena, FFA up to 16, 2 characters × (M1 chain + 4 skills + awakening),
dash, block, evasive, respawn, kill feed, streak leaderboard, emote wheel with 3 free emotes,
Early Access + emote-slot passes (inferred).

**Build order (one developer with Claude Code, inferred):**

1. **Week 1:** server combat state machine (Idle, Attacking, Stunned, Blocking, Ragdolled,
   Dashing, Awakened), move-data module, M1 chain with placeholder animations, hitbox debug view,
   damage and stun. Playtest with 2–4 clients through Studio MCP.
2. **Week 2:** dashes, knockback (`LinearVelocity` or `AssemblyLinearVelocity` on the server-owned
   root), ragdoll and get-up, evasive meter, block and endlag, respawn.
3. **Weeks 3–4:** character 1 kit, awakening, VFX/SFX, hit-stop, camera shake.
4. **Weeks 5–6:** character 2, character select, mobile buttons and console bindings.
5. **Week 7:** fake destruction (swap to pre-broken debris, reset after 20–30 s), data save,
   passes, emote wheel, analytics funnel.
6. **Week 8:** phone performance pass in a full server, balance, launch.

**Cut:** ranked, quests, story NPCs, trading, real-time fracture physics, more than 2 characters
at launch, cutscene ultimates longer than ~2 s, custom replication.

## Top examples

- The Strongest Battlegrounds (case study: the-strongest-battlegrounds): the genre
  leader since 2022; character-per-update cadence, Early Access pass, emote economy.
- Jujutsu Shenanigans (compared inside the TSB case study): solo-developer origin, documented
  frame data, Build Mode.
- [Anime RPG](anime-rpg.md) for the progression-heavy alternative; Blox Fruits (case study: blox-fruits).

## Build checklist for agents

### Do
- Keep all combat state, cooldowns, damage and stun on the server; clients send intents only.
- Define every move as data: startup, active, recovery, damage, stun, knockback, hitbox size and
  offset, cooldown, blockable, tags.
- M1: 4-hit chain, startup 0.15–0.25 s, ~0.75 s hit stun, ~1.5–2 s downtime after the 4th hit;
  4th hit varies by vertical state (knockback / uppercut / unblockable downslam).
- Melee hitbox: `GetPartBoundsInBox` in front of the attacker, 5–8 studs per side, filtered to
  character models, plus 1–2 studs of lag forgiveness when the server detects.
- Block: frontal 180° arc, slows movement, blocked hits add attacker endlag; at least one
  block-breaking option per kit.
- Dashes: forward 4–6 s cooldown, side/back ~2 s; side dash can cancel startup.
- Give an escape: 0.5 s stun immunity after ragdoll and a meter-gated evasive with ~1 s i-frames.
- Awakening from damage dealt (~250–300), lasting 45–60 s, reset on character swap.
- Servers of 12–20; respawn in ≤ 5 s near but not on top of the killer.
- Play windup animations and VFX on the client immediately; replicate results from the server.
- Cap simultaneous particles per player and scale bursts on low quality levels.
- Disclose odds for any random emote or cosmetic roll.

### Don't
- Don't use `Touched` for hit detection or trust client-sent damage, targets or positions without
  the checks in [security](../../.claude/skills/roblox-code/references/security.md).
- Don't ship moves with no windup or no endlag, or big moves under ~2 s cooldown.
- Don't allow a combo the victim can't escape.
- Don't sell characters that stay paid and stronger; Early Access should end in free release.
- Don't use franchise names, signature move names or likenesses.
- Don't plan more than 2 characters before the first one is fun in a 10-player playtest.
- Don't pick R6 and then plan on video-captured animations.

## Sources

1. https://jujutsu-shenanigans.fandom.com/wiki/Controls_%26_Mechanics — JJS M1, block, dash, ragdoll, evasive, awakening, regen, wall-jump values
2. https://jujutsu-shenanigans.fandom.com/wiki/Gamepasses — Early Access permanence, 13+ EA characters, "no gamepass other than Early Access affects battles"
3. https://jujutsu-shenanigans.fandom.com/wiki/Build_Mode — Build Mode in private servers, Skill Builder
4. https://www.roblox.com/games/9391468976 — JJS page: controls, destruction note, award; API read 2026-10-23 (77K players, 20 max, R6)
5. https://www.roblox.com/games/10449761463 — TSB page: controls, 2024 award, random emote odds disclosure
6. https://apis.roblox.com/game-passes/v1/universes/3808081382/game-passes — TSB pass names and prices (read 2026-10-23)
7. https://apis.roblox.com/game-passes/v1/universes/3508322461/game-passes — JJS pass names and prices (read 2026-10-23)
8. https://allthings.how/the-strongest-battlegrounds-character-roster-movesets-and-access-rules/ — TSB roster, awakening meter (updated 2026-06)
9. https://sportskeeda.com/roblox-news/the-strongest-battlegrounds-kj-update-patch-notes — KJ update 2024-12-21, Tech Prodigy Early Access (via search snippet)
10. https://bloxodes.com/wiki/the-strongest-battlegrounds/techniques — TSB tech catalog, patched techs
11. https://devforum.roblox.com/t/what-is-the-most-ideal-way-for-a-melee-system/3915571 — hitbox method trade-offs (2025-09)
12. https://devforum.roblox.com/t/help-with-server-client-hitbox-system/4687309 — 200 ms ping reach, ~20 Hz replication, server-side detection advice (2026-06)
13. https://devforum.roblox.com/t/introducing-shapecasts/2320655 — Blockcast/Spherecast/Shapecast, first-hit and cost notes (2023-05)
14. https://devforum.roblox.com/t/chrono-drop-in-custom-physics-replication-library/3873294 — custom replication, client-authoritative caveat
15. https://create.roblox.com/docs/reference/engine/classes/WorldRoot — GetPartBoundsInBox, GetPartsInPart, GetPartBoundsInRadius, casts
16. https://create.roblox.com/docs/animation/capture — Live Animation Creator: R15 only, < 15 s clips
17. private/trends/latest.md — subgenre and theme totals, server sizes, new breakouts (data, 2026-10-22)
18. https://sportskeeda.com/roblox-news/the-strongest-battlegrounds-a-beginner-s-guide — TSB 4-hit M1, final hit strongest (via search snippet)
19. https://www.roblox.com/games/130906410042392 and https://www.roblox.com/games/107535308163741 — Cat Battles (ring-out, 10 players, fur crates) and Huss Valley (chaser crossing game) descriptions, read 2026-10-23

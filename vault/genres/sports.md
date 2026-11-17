---
title: Sports
type: genre
read-when: Building a soccer, volleyball, basketball, or other sports game.
last-researched: 2026-10-22
---

# Sports

## In one line

Short team matches (2v2 to 6v6) around one shared ball. How the ball is networked decides
whether the game feels fair. Collectible "styles" and abilities give players the long-term goal,
and ranked play gives them a reason to keep improving (inferred from the games below).

## Core loop

- **Moment to moment:** get into position, receive, then pass, shoot or spike, then defend. Every
  touch of the ball is a timing or aim check with instant feedback (inferred).
- **Match:** timed, or first to N points. Illegal Soccer runs 4v4 on a timer, and its tutorial
  ends after 3 goals (press, 2026-09). Volleyball Legends is 6v6 with a timed serve power meter
  (official game description, 2026-10). Keep a match under ~8 minutes so a mobile session fits 1–2
  of them (inferred).
- **Session:** play matches, earn soft currency scaled by result, spend it on spins for styles or
  abilities, try the new pull in the next match (community, 2026).
- **Long term:** collect and upgrade styles, climb seasonal ranked Elo, buy cosmetics (emotes,
  goal effects, ball or car skins), and join clans or tournaments (inferred).

## Main verbs

| Sport | Verbs players expect |
|---|---|
| Soccer | sprint (stamina), dribble, pass, lob, charged shot, slide tackle, header, keeper dive. Illegal Soccer adds items from a pickup box: grappling hook, oil spill, jetpack, guns (press, 2026-09) |
| Volleyball | serve (click, then click again to set power), bump, set, spike with mid-air aim, block, dive (official game description, 2026-10) |
| Basketball | dribble, timing-meter shot, pass, block, steal (inferred) |
| Car soccer | drive, boost, jump; skins, wheels, decals and boosts as unlocks (official, Turbo Soccer description, 2026-10) |

Anime-sports hybrids add 3–5 hotkeyed skills per character or style. A Blue Lock-licensed soccer
game binds shot to M1, skills to 1–5, tackle and dash to Q, and dribble to E (official game
description, 2026-10).

## Why players come back

1. **Gacha styles that change stats.** Volleyball Legends styles set eight attributes (block,
   bump, dive, jump, serve, set, speed, spike) and roll at Common 62.5%, Rare 35%, Legendary 2%,
   Godly 0.5% and Secret 0.1%, from a pool of 32 styles (press, 2025-11). A new style each update
   gives a reason to log in (inferred).
2. **Abilities that reward timing.** Volleyball Legends abilities last only a few seconds, and a
   rarer one isn't always better. Examples: the next spike passes through blockers, or curves the
   way you tilt in the air (press, 2025-05).
3. **Ranked.** "Pickup game with friends OR … ranked match" is in Volleyball Legends' own
   description (official game description, 2026-10). Seasonal Elo resets are reported (community
   guides, 2026; unverified).
4. **A fixed update day.** Volleyball Legends promises weekly updates on Saturdays at 11:30am EST,
   and new codes usually arrive with them (official game description, 2026-10; community).
5. **Fandom.** Two of the highest-rated sports games are anime-inspired: Blue Lock: Rivals (97%)
   and Basketball: Zero (98%) (data, 2026-10-22).

## What separates top games from clones

### Ball netcode: pick one model before writing gameplay

| Model | How | Good | Bad |
|---|---|---|---|
| A. Server-owned physics | `ball:SetNetworkOwner(nil)` and the server applies `ApplyImpulse` or a `LinearVelocity` | Fair, hard to exploit | The kicker sees a full round trip before the ball moves; players commonly have ~100–200 ms (community, 2023-06) |
| B. Possession owner | The server calls `SetNetworkOwner(player)` for whoever has the ball and takes it back on release | Smooth for the holder | Each handover causes a visible hitch for others. Ownership drops to nil after unattaching (community, 2025-08). The owner can teleport the ball, so the server must validate it |
| C. Scripted trajectory | The ball is anchored. The server computes the path (origin, velocity, spin, gravity) and sends the parameters plus `workspace:GetServerTimeNow()`. Every client draws the same curve, and the server decides touches | Deterministic, cheap, same on every screen, can't be exploited by owning the ball | No free bounces unless you code them (inferred). Best for volleyball spikes, basketball shots, lobs |
| D. Server Authority | `Workspace.AuthorityMode = Server`. Game logic runs in `RunService:BindToSimulation`, and nearby objects are predicted and rolled back | Official answer for fair sports physics. Roblox ships a Soccer-Server-Authority-Template (official, 2026-07) | All gameplay code moves to the simulation model. Limits: 8 active animation tracks per Animator, 64 replicated attributes per instance, higher server CPU (official, 2026-07) |

- Default for a solo dev: **C** for volleyball and basketball, **A or D** for soccer. Use B only
  with server checks on ball speed and position (inferred).
- Whatever the model, play the kick sound, animation and VFX on the client the moment the input
  lands, before the server confirms. This hides the round trip (community, 2025-08; inferred).
- Never let two systems move the ball: a velocity set on a client while the server owns the ball
  fights the server (community, 2023-01).
- Prefer `LinearVelocity` over setting `AssemblyLinearVelocity` when you need curve or controlled
  drag (community, 2023-06).
- Server Authority setup and limits: [security](../../.claude/skills/roblox-code/references/security.md).
  Ownership basics: [performance](../../.claude/skills/roblox-map/references/performance-and-devices.md).

### Fairness under latency

- The server decides every contested touch (who reached the ball first, block versus spike) from
  server-side positions, with a few studs of slack (inferred). Mispredictions caused by other
  players are unavoidable even under Server Authority (official, 2026-10).
- Bias the matchmaker toward low ping. Custom matchmaking has a built-in Latency signal (max
  relevant difference 100 ms) and supports custom attributes such as Elo (official, 2026-10).
- Test every ball interaction in Studio's Network Simulator at 150 ms and 250 ms before calling it
  done (official tool; thresholds inferred).

### Progression without breaking competition

- Styles and abilities are the meta-loop, but a match must still be won by play. Keep the gap
  between the best and worst style on any attribute small, about 15–20% (inferred: no public
  numbers exist), and give abilities clear counters and cooldowns.
- Give rare styles new looks and new options (an ability, a curve) rather than a bigger number
  (inferred from the 2025-05 ability design above).

### Spectacle

- **Goal and point replays.** Illegal Soccer once ran with "[REPLAYS!]" in its title (community:
  RoWatcher title history, 2026). A cheap version: each client keeps a ring buffer of the ball and
  every `HumanoidRootPart` CFrame at 20 Hz for the last 8 s. On the server's `GoalScored` event,
  play it back on stand-in models while the camera orbits the scorer (community pattern, 2020/2023;
  numbers inferred).
- **Slow motion** only exists inside replays: play the buffer at 0.3–0.5× for the last 1.5 s
  before the goal. Don't try to slow live physics (inferred).
- Goal moment: hit-stop of 0.1 s, FOV kick, net shake, scorer banner, crowd sound. Recipes are in
  [game feel](../../.claude/skills/roblox-vfx/references/game-feel.md). Skip shake under `GuiService.ReducedMotionEnabled`.
- Per-style VFX on skill use is the cosmetic you sell (inferred).

### Mobile controls

- Volleyball Legends documents PC and console bindings only (click/RT, Q/LT, Ctrl/X) (official
  game description, 2026-10). Mobile needs its own layout. See [ui-ux](../../.claude/skills/roblox-ui/references/ui-ux.md).
- Use at most 3–4 action buttons arcing around the jump button, each ≥ 56 px. Show context
  buttons (Shoot only while you have the ball, Block only near the net) (inferred from ui-ux).
- Charge shots: hold the button and show a fill meter, then release. Aim from camera direction
  plus thumbstick, with light auto-aim toward the goal on touch only (inferred).
- Build buttons with `InputAction` and `UIButton` bindings so PC, gamepad and touch share one
  code path (official, 2026-10).

## Session shape

- **Typical session:** Volleyball Legends averages 12.97 minutes of play (community: Rolimons,
  read 2026-10-23).
- **First 60 s:** on the field with the ball within 30 s. A 3-goal or 3-point tutorial against
  bots, as Illegal Soccer does (press, 2026-09), then straight into a casual match.
- **First 10 min:** 2–3 casual matches, first currency, first free spin. Grant the spin before the
  first loss stings (inferred).
- **Day 7:** ranked unlocks (Volleyball Legends gates ranked at level 15; press, 2025;
  unverified), and the player is chasing one specific style or ability.

## Social hooks

- Party queue: friends always land on the same team (inferred).
- Free private servers with an admin panel let groups run leagues and scrims. Realistic Street
  Soccer advertises exactly this (official game description, 2026-10). See
  [private servers](../patterns/private-servers.md).
- Tournaments and seasonal events: Blue Lock: Rivals has run "World Tournament" titled updates
  (community: RoWatcher title history, 2026).
- Celebration emotes after goals. Volleyball Legends sells 2x emote slots (community: Rolimons,
  2026-10-22). More in [social and virality](../fundamentals/social-and-virality.md).

## Monetization that works here

- **Spins** for styles and abilities: Robux bundles of currency or lucky spins. A pity of 100 lucky
  spins for a Secret is reported (community guides, 2025; unverified). Check
  `PolicyService:GetPolicyInfoForPlayerAsync` → `ArePaidRandomItemsRestricted` and disclose paid
  random items ([metadata](../fundamentals/metadata-thumbnails-icons.md)).
- **Slots and convenience passes.** Volleyball Legends sells Spin Skipping (49 R$), VIP (399 R$)
  and 2x emote slots (150 R$). Its style-slot (4–18) and ability-slot (3–6) passes are now offsale
  (community: Rolimons, read 2026-10-23).
- **Premium bonus:** +10% currency for Premium players (official game description, 2026-10).
- **Cosmetics:** ball, car and goal-effect skins. Turbo Soccer lists skins, wheels, decals and
  boosts (official game description, 2026-10).
- **Free-to-progress option:** Illegal Soccer gives coins per match for daily-shop item rolls and
  needs no purchase to progress (press, 2026-09).
- Scale: RoWatcher estimates Volleyball Legends at ~$284K/month (community, undated, its own
  confidence 0.6; unverified).
- Details in [monetization](../fundamentals/monetization.md).

## Common failure modes

- Ball stutter or teleport on ownership changes. This is the single most reported sports bug on
  the DevForum (community, 2022–2025).
- Not enough players: a 6v6 game with 40 concurrent players runs a few broken matches. Ship 2v2 or
  3v3 first, or fill with AI. Realistic Street Soccer advertises AI goalkeepers (official game
  description, 2026-10; inferred).
- Leavers wreck ranked. Volleyball Legends halved the Elo loss when a teammate quits in the first
  15 rounds (community guide, 2025-06; unverified).
- Pay-to-win stat gaps in ranked (inferred).
- Unlicensed anime names: "Haikyuu Legends" was renamed Volleyball Legends in 2025-02 (press).
  Blue Lock IP is licensable through Roblox License Manager since 2025-07 (press). Use original
  names, or license.
- Me-too entries rate poorly: Become A Striker 66% and Bloxx League 78%, against 93–98% for the
  leaders (data, 2026-10-22).

## Saturation & opportunity

Single snapshot, so no growth claims.

- Sports & Racing: 272K players across 47 charted games (3.9% share). The Sports subgenre alone
  is 258K across 38 games (data, 2026-10-22).
- Soccer: 22 games, 182K players, 8.3K per game, median 3.8K. The leader, Illegal Soccer, holds
  only 25%, so the theme is "mixed" rather than dominated (data, 2026-10-22).
- Three rising soccer games, all created 2026-09-19 → 2026-10-04: Turbo Soccer (23K, 93%), Bloxx
  League (3.3K, 78%) and Become A Striker (2.9K, 66%) (data, 2026-10-22). Only the one with a
  distinct twist, car soccer, is large (inferred).
- Volleyball: Volleyball Legends (41K) dwarfs the next volleyball game, Volleyball Journey (1.2K)
  (data, 2026-10-22). One game dominates this sport.
- Basketball is split across mid-sized games: Basketball: Zero 7.3K, Basketball Legends 3.9K, NBA:
  Heroes 2.8K, Pixel Basketball 2.6K (data, 2026-10-22). No dominant leader is a possible opening
  (inferred).
- Twists that chart: chaos items (Illegal Soccer, 45K, 163 days old), vehicles (Turbo Soccer),
  ragdoll physics (Ragdoll Football 3.7K), anime licence (Blue Lock: Rivals 14K) (data,
  2026-10-22).
- Server sizes: Illegal Soccer 8, Blue Lock: Rivals 10, Volleyball Legends 12, Become A Striker 6
  (data, 2026-10-22).

## Scope for a solo dev

**MVP:** one sport, one 3v3 casual mode (2v2 fallback), one arena, a server-decided ball, 5–6
actions, AI fill for empty slots, one soft currency, 6–8 styles with a spin, a goal moment with a
simple replay. Ranked waits until there's enough concurrent players.

| Week | Build |
|---|---|
| 1 | Ball prototype in the chosen netcode model. Test at 150/250 ms in Network Simulator with 2 clients. Stop if it doesn't feel right |
| 2 | Actions with input buffering, stamina, possession rules, AI keeper or fill bot |
| 3 | Match state (lobby → match → results) with [round system](../patterns/round-system.md), teams, score UI, goal moment |
| 4 | Mobile and gamepad controls, FTE tutorial, HUD |
| 5 | Styles, spins, data saving ([player data](../patterns/player-data.md)), shop |
| 6 | Playtest with 6+ real players, replay polish, exploit checks |
| Later | Elo ranked with a season reset, private-server leagues, cosmetics |

- **Netcode is the main risk:** budget the whole first week for it.
- **Animation is the second risk.** Each verb needs one animation, and the user has no animator.
  Make 6–8 short animations in Studio's Animation Editor, or use stylized ragdoll, cartoon or
  vehicle avatars that need fewer (inferred).
- **Cut:** 11v11, realistic motion capture, a full-pose replay (record root and ball only),
  spectator mode, clans, custom physics engines.

## Top examples

- Volleyball Legends (case study: volleyball-legends): 6v6 volleyball with gacha styles
  and abilities, weekly updates, ranked.
- Illegal Soccer: 4v4 soccer with no rules and item boxes; 45K and 163 days old (data,
  2026-10-22); peaked at 82K in 2026-09 (community: RoWatcher).
- Blue Lock: Rivals: licensed anime soccer with character abilities; 5.01B visits (data,
  2026-10-22); peaked at 276K on 2025-09-13 (community: RoWatcher).
- Turbo Soccer: car soccer with customization; 23K at 33 days old (data, 2026-10-22).
- Realistic Street Soccer: futsal-sized pitch, AI keepers, free private servers; 24K (data,
  2026-10-22).

## Build checklist for agents

### Do

- Pick and document one ball netcode model (A–D) before writing actions.
- Have the server decide goals, points, touches and possession. Clients send intents
  (`RequestKick(dir, power)`) that are validated for range, cooldown, possession and a power clamp.
- Play kick, spike and shot feedback on the client immediately; reconcile from the server.
- Test every ball interaction at 150 ms and 250 ms simulated latency.
- Give the ball explicit `CustomPhysicalProperties` and a max speed the server enforces.
- Use reserved servers or custom matchmaking with a Latency signal for ranked.
- Ship a 2v2/3v3 mode or bots so matches start with 4 players online.
- Context-sensitive mobile buttons (≤ 4) built with `InputAction`.
- A goal or point moment with sound, hit-stop, banner and a short replay.
- Original style and ability names; disclose paid random items.

### Don't

- Don't let the ball's network owner decide where the ball is without server checks.
- Don't switch ball ownership every touch without testing the hitch at real ping.
- Don't let a paid style win ranked matches by stats alone.
- Don't start with 11v11 or 6v6 when concurrent players are low.
- Don't use anime character or team names you haven't licensed.
- Don't put more than 4 permanent action buttons on a phone screen.
- Don't slow live physics for slow motion; slow the replay.

## Sources

1. https://www.roblox.com/games/73956553001240 — Volleyball Legends description: 6v6, ranked, controls, weekly Saturday updates, Premium +10% (read via tracker 2026-10-22)
2. https://www.pockettactics.com/volleyball-legends-styles — style attributes, rarity odds, 32 styles (2025-11-14)
3. https://www.escapistmagazine.com/volleyball-legends-abilities-tier-list/ — abilities: duration, examples, rarity vs power (2025-05-26)
4. https://www.rolimons.com/game/73956553001240 — game passes and prices, peaks, average playtime (third-party tracker, read 2026-10-23)
5. https://rowatcher.com/games/6931042565/upd-volleyball-legends — revenue estimate, peak (third-party tracker)
6. https://www.pcgamesn.com/volleyball-legends/codes — Haikyuu Legends renamed in 2025-02
7. https://allthings.how/illegal-soccer-on-roblox-how-to-play-controls-and-item-boxes/ — Illegal Soccer teams, controls, items, coins (2026-09-06)
8. https://rowatcher.com/games/10155360168/replays-illegal-soccer — Illegal Soccer peak 82K (2026-09), replays title
9. https://rowatcher.com/games/6325068386/sendou-blue-lock-rivals — Blue Lock: Rivals peak 276K (2025-09-13)
10. https://www.anitrendz.com/news/2025/07/16/kodansha-partners-with-roblox-on-new-licensing-initiative-will-bring-blue-lock-and-tensura-to-licenses-catalog — Blue Lock in License Manager (2025-07-16)
11. http://www.pocketgamer.biz/roblox-opens-license-manager-to-all-eligible-ip-holders-throughself-serve-system/ — Blue Lock: Rivals past 4B visits (2025-11-13)
12. https://devforum.roblox.com/t/soccer-ball-latency/2088353 — server ownership latency, custom replication (2022-12)
13. https://devforum.roblox.com/t/soccer-ball-system-has-a-short-delay-before-applying-velocity-on-other-clients-screen/3874644 — ownership handover hitch (2025-08)
14. https://devforum.roblox.com/t/2403339 — LinearVelocity over AssemblyLinearVelocity for kicks (2023-06)
15. https://create.roblox.com/docs/projects/server-authority — prediction, rollback, BindToSimulation, SetPredictionMode
16. https://devforum.roblox.com/t/full-release-ship-fair-and-competitive-games-with-server-authority/4727993 — Soccer/Racing templates, limits (2026-07-09)
17. https://create.roblox.com/docs/matchmaking/attributes-and-signals — Latency signal, custom Elo attributes
18. https://devforum.roblox.com/t/vpf-replay-module/523112 — replay recording and smooth slow playback (2020)
19. https://devforum.roblox.com/t/how-would-i-go-about-creating-a-var-system-for-roblox-tps/2278552 — CFrame ring-buffer replays (2023)
20. https://roonby.com/2025/06/21/volleyball-legends-update-24-guide-new-codes-more/ — leaver Elo rule (2025-06; unverified)
21. private/trends/latest.md and tools/trends lookups — all (data, 2026-10-22) numbers
22. https://devforum.roblox.com/t/2441924 — ~100–200 ms typical player lag, ownership-switch teleports (2023-06)

---
title: Round-based races and survival
type: genre
read-when: Building a lobby → round → results game (speed-run races, disaster survival, deathruns, flood escapes, quick duels), or fixing one that feels flat.
last-researched: 2026-10-22
---

# Round-based races and survival

## In one line

Short shared rounds (1–4 min) on rotating maps, with everyone back in the lobby between them.
The round is the content and the spectacle, and the gaps between rounds are where these games
win or lose players. Implementation (phases, timers, voting, spectate, cleanup) lives in
[round system](../patterns/round-system.md); this file covers design.

## Core loop

- **Moment to moment:** run, jump, dodge, survive a hazard, outpace others.
- **Round (1–4 min):** intermission and vote → load → 3-2-1 → play → results with rewards.
- **Session (15–30 min = 6–12 rounds, inferred):** a different map each round, daily missions,
  currency toward cosmetics or perks.
- **Long term:** levels, map unlocks, cosmetics, seasons, records per map.

## Variants and what each teaches

| Variant | Example (facts) | Lesson for us |
|---|---|---|
| Disaster survival | Natural Disaster Survival: released 2011-12-04, 13 disasters, random map + disaster each round, warning banner that says how to survive ("Flash Flood! Seek higher ground!"), lobby tower overlooking the island so dead players watch the round (community, wiki). 6,887 players, 91% likes (data, 2026-10-22). | A warning plus a hint turns randomness into a decision. Dead players watching survivors is free content. |
| Deathrun (runners vs one killer) | Deathrun: 15 s intermission in an activity lobby; the killer triggers traps whose buttons recharge 7–30 s; 3–5 checkpoints per map, one every 2–4 traps; "The Hand" appears ~30 s in, kills anyone who hasn't moved, then sweeps the course; dead runners become ghosts who respawn at their last checkpoint and still collect coins (community, wiki). | Anti-stall pressure, a role swap, and keeping the dead playing. |
| Flood escape (co-op parkour vs rising liquid) | Flood Escape 2: buttons must all be pressed to escape, group buttons need several players; map voting with cooldowns and "pre-votes" that grow on the least-played map until it's picked; 150+ community maps in 6 difficulty tiers; rescue NPCs worth 100 XP (community, wiki). | Co-op objectives inside a race; voting that forces rotation; user-made maps as content. |
| Speed-run race | Speed Run 4: dozens of levels, each with its own song and look, a visible timer, stars that unlock "forbidden" levels (official game description, 2026-10). 810 players, 74% likes, created 2014 (data, 2026-10-22). | Per-level identity and personal-best timers; the format alone is small today. |
| Elimination minigames | Squid Game X 12,917, Ink Game 9,780, DON'T GET ELIMINATED 3,922, Death Order: Simon Says 2,268 (data, 2026-10-22) | Rounds where the rule changes each time; big servers (Death Order allows 100). |
| Quick duels | Murderers VS Sheriffs 74,329 players; MVSD (1v1 to 4v4 duels) 7,775 (data, 2026-10-22) | Rounds under a minute with skill expression; see [shooter](shooter.md) and [social deduction](social-deduction.md). |

## Main verbs

Run, jump, survive, vote, spectate, press buttons (co-op), trigger traps (killer role), and race
the clock or each other.

## Why players come back

- **Variety per round:** a new map and/or hazard each time. NDS crosses 13 disasters with its map
  list (community, wiki). Variety is the whole content budget (inferred).
- **Records:** best time per map, survival streaks. NDS has a server leaderboard of survivals
  (community, wiki).
- **Daily missions:** Deathrun gives tickets for missions such as "activate X checkpoints" or "win
  X games", spent on a prize wheel (community, wiki).
- **Seasons:** Deathrun ran at least 9 themed seasons, each with a map, a currency and a premium
  track, 2019-10 to 2021-12 (community, wiki; its page says 9 but lists 10).
- **Friends in the same lobby:** rounds are a natural party activity (inferred; see
  [social and virality](../fundamentals/social-and-virality.md)).

## What separates top games from clones

| Top games | Clones |
|---|---|
| Downtime is playable: lobby obby, fishing, spleef, coins from a sprinkler, spectate (Deathrun lobby, community wiki) | A gray box with "Intermission: 20" |
| Dead players stay in the round as ghosts or watchers who still earn something | Death means 2 minutes watching a countdown |
| Each map has a set-piece and a name players vote for | Maps are reskins of one layout |
| Hazards announced with a counter-action | Random deaths with no warning |
| Rewards for progress (checkpoints, buttons, survival time), not just winning | Winner-takes-all; 90% of players earn nothing |
| Anti-stall pressure (The Hand, rising flood) | Rounds stall while one player hides |
| Voting that guarantees rotation | The same favorite map 5 times in a row |

## Pacing and dead time

Use the tuning ranges in [round system](../patterns/round-system.md#tuning-ranges-inferred-unless-tagged);
the headline numbers (inferred there):
- **About 30 s downtime per round** (results + intermission + load + countdown), under 25% of
  the cycle.
- **Intermission 10–15 s** without a vote, 15–20 s with one; cut to 5 s when everyone has voted.
  Deathrun uses 15 s (community, wiki).
- **Finish window** after the first finisher: `clamp(0.5 × winnerTime, 20, 60)` s; end at once when
  everyone is done or out.
- **Round cap** at about 2× the median finish time from playtests.

**While dead or finished (inferred unless tagged):**
1. **Keep playing:** respawn as a ghost at the last checkpoint who can't affect the race but can
   still collect coins (Deathrun's model, community wiki). Or send them to a lobby mini-course
   with a timer.
2. **Watch:** a spectate button that cycles alive players, with the round's music playing
   quietly, as in FE2 (community, wiki). NDS places its lobby so the arena is visible (community,
   wiki).
3. **Predict:** a free pick of "who wins / who survives" for a small bonus. It costs nothing and
   gives dead players a stake (inferred).
4. **Vote early:** open the next-map vote to finished or dead players right away (inferred).

## Map rotation and voting

- Three options per vote, never the last map. One vote per player (round-system rules).
- Force rotation: FE2 adds growing "pre-votes" to the least-played map until it's picked, and
  locks recently played maps (community, wiki). A simpler equivalent: weight each option by rounds
  since it was played.
- Paid influence stays small: Deathrun's VIP doubles a vote; NDS sells a pass to vote among 3 maps
  (community, wiki). Never let one payer decide every map (inferred).
- Show each map's name, image, difficulty and best time on the vote card; FE2's intermission
  screen shows name, difficulty, creator and button count (community, wiki).

## Rewards per round

Compute on the server at Results (see [round system](../patterns/round-system.md#rewards-per-round)).
Starting values (inferred):

| Event | Reward share |
|---|---|
| Participation (moved > 50 studs or survived > 20 s) | 20% |
| Each checkpoint / button / survival milestone | 40% split across them |
| Finishing or surviving | 25% |
| Placement bonus (top 3) | 15% |
| First win of the day | ×2 on that round |

- References: FE2 pays 10 XP per button, 20 per group button and 100 per rescue (community, wiki);
  Deathrun pays coins for checkpoints, finishing, kills and lobby fishing (community, wiki).
- Show the breakdown on the results screen with the next goal ("120 coins to the next trail").

## Fixing a flat speed-run race (the user's prototype)

His loop: Lobby → Intermission (20 s) → Map → race with 3–4 lives → Results (5 s), with a 45 s
finish window (task brief, 2026-10). Likely causes and changes (all inferred):

| Symptom | Fix |
|---|---|
| Lives knock the weakest players out of a race, leaving them idle | Replace lives with checkpoints plus a time cost (respawn in 1–2 s at the last checkpoint). Keep lives only for a "hardcore" mode or a survival variant. |
| Racers never interact | Add one shared element per map: a shortcut button that opens for everyone, a hazard the leader triggers, or a group button. |
| Every map feels the same | Give each map one set-piece and its own music; name it on the vote card. |
| 20 s idle intermission, 45 s fixed finish window | 10–15 s playable intermission; `clamp(0.5 × winnerTime, 20, 60)` window. |
| Only the winner is rewarded | Pay per checkpoint plus placement (table above). |
| No reason to play round 6 | Per-map best times, daily missions ("finish 3 maps under par"), and a cosmetic track. |
| No spectacle | A chaser or rising hazard behind the pack (Deathrun's Hand, FE2's flood) that ends stalls and creates near misses. |

## Session shape

- **Typical session:** 15–30 min, 6–12 rounds (inferred).
- **First 60 s:** if a round is running, the joiner gets the lobby course and a clear "next round
  in 0:42" banner; if not, the round starts with 1 player (never "waiting for 2"; round-system).
  First round within 60 s of joining (inferred; see
  [first-time experience](../fundamentals/first-time-experience.md)).
- **First 10 min:** 3–5 rounds, a first reward screen, a first vote, a first cosmetic within reach.
- **Day 7:** map records, missions, season progress (inferred; see
  [retention](../fundamentals/retention.md)).

## Social hooks

Shared spectacle (everyone sees the disaster), placement callouts in chat, co-op buttons, a
killer/runner role swap, voting, ghosts helping as spotters, private servers with round control.
NDS sells round control for private servers (community, wiki).

## Monetization that works here

| Product | Example (community, wiki unless tagged) | Notes |
|---|---|---|
| Currency/XP boost passes | Deathrun Coin Boost +20% R$300, XP Boost +20% R$300 | Safe; doesn't change outcomes |
| Role chance | Deathrun Killer chance +20% R$600 | Fine when roles are fun both ways |
| VIP | Deathrun R$1,200: double vote, cape, chat color | Status plus small influence |
| Season pass | Deathrun Season Gold R$400 | Needs live ops |
| Server-wide spectacle product | NDS Weather Machine R$75 per extra disaster | One buyer creates a moment for all |
| Survival tools | NDS Green Balloon (higher jump, slower fall), Red Apple (+15 HP, 5.5 s cooldown) | Mild pay-to-win; keep effects small |
| Extra life / revive | Rewarded video ad worth about R$3–10, "after losing a life" (official, 2026-10) | Free path for everyone |

Don't sell speed in a race against other players, or checkpoint skips in a competitive round
(inferred). See [monetization](../fundamentals/monetization.md).

## Common failure modes

- Downtime above about 30 s per round; nothing to do in the lobby.
- Eliminated players idle for the rest of the round.
- Rounds that wait for one straggler or a leaver (round-system cleanup rules).
- One map repeated because voting has no rotation rule.
- Random, unannounced deaths (disasters without warning).
- Winner-takes-all rewards.
- Requiring 2+ players to start (solo players leave).
- Map loads that freeze the client: stream maps and pre-stream spawn areas
  ([performance](../fundamentals/performance-and-devices.md)).

## Saturation & opportunity

Single snapshot (data, 2026-10-22); no growth claims.

- Survival is 21.9% of charted players (48 games, 1.54M), but almost all of it is 1-vs-All and
  horror: Murder Mystery 2 675K, DOORS 184K, Flee the Facility 80K.
- `disaster` theme: 3 games, 14K players: What If Disasters 7,251 (created 2026-10-05; 25
  disasters, 9 maps), NDS 6,887 (15 years old), Survive The Disasters 2 at 49.
- Speed-run races: Speed Run 4 (810) is the only charted one. Flood Escape 2 and Deathrun are not
  charted on 2026-10-22.
- Elimination minigame rounds: Squid Game X 12.9K, Ink Game 9.8K, DON'T GET ELIMINATED 3.9K,
  Death Order 2.3K.
- Read (inferred): a plain speed-run race is a small slot. Players are in round games with
  spectacle (disasters, giant chasers), roles (killer vs runners, murderer vs sheriff) or
  changing rules. A new disaster game just reached 7K in 17 days, so spectacle-first survival
  rounds still break out. For the user's race, add a spectacle or a role, not more maps of the same.

## Scope for a solo dev

**MVP (4 weeks; inferred):**
- Round system from [round system](../patterns/round-system.md), with solo start and a
  playable lobby (a 60-second practice course).
- 5 maps, each with one set-piece; checkpoints with 1–2 s respawn; ghost or spectate on death.
- One spectacle or role mechanic (rising hazard behind the pack, a hunter, or random events
  announced with a counter-hint).
- 3-option vote with a rotation rule; results with a reward breakdown; per-map best times.
- 2 boost passes, 5 cosmetics, rewarded-ad revive once eligible.

| Week | Build |
|---|---|
| 1 | Round loop, lobby course, 2 maps, checkpoints, results |
| 2 | Spectacle/role mechanic, ghost/spectate, vote and rotation |
| 3 | 3 more maps, rewards, data, missions, products |
| 4 | Phone test of a full 20-min session, downtime measurement, thumbnails, launch |

**Cut:** seasons, community maps, a killer-role shop, ranked play, private-server controls.
**After launch:** 1–2 maps every 2 weeks; a themed event map monthly (inferred).

## Top examples

- Natural Disaster Survival: random map × disaster, warning hints, watch from the lobby tower
  (community, wiki; data 2026-10-22).
- Deathrun: killer vs runners, The Hand, ghosts, activity lobby, seasons (community, wiki).
- Flood Escape 2: co-op buttons, rising flood, rotation-forcing votes, community maps
  (community, wiki).
- Speed Run 4: per-level songs and timers (official description).
- Murder Mystery 2 (case study: murder-mystery-2): hidden-role rounds at scale.
- Tower of Hell (case study: tower-of-hell): a timer-only round with no lobby at all.

## Build checklist for agents

### Do

- Use the phase loop and cleanup from [round system](../patterns/round-system.md); start rounds
  with 1 player for races and survival.
- Keep total downtime per round ≤ 30 s and intermission 10–15 s (15–20 s with a vote); log idle
  seconds per player in analytics.
- Make the lobby playable: a practice course plus visible next-round timer and last round's top 3.
- Give dead or finished players a ghost run, spectate (`CameraSubject` + `AddReplicationFocus`) and
  the next vote within 2 s of death or finish.
- In races, use checkpoints and 1–2 s respawns instead of lives.
- Add anti-stall pressure: a hazard that starts moving 20–30 s into the round, or a shrinking
  finish window.
- Announce every random hazard with its counter ("seek higher ground") 3–5 s before it hits.
- Pay rewards per checkpoint/milestone plus placement, and show the breakdown.
- Rotate maps: 3 options, exclude the last map, weight by rounds since played.
- Give each map a name, a set-piece and its own music.

### Don't

- Don't make a solo player wait for a second player.
- Don't leave eliminated players with only a countdown.
- Don't reward only the winner, or reward AFK players.
- Don't sell speed, checkpoint skips or vote control that decides outcomes for others.
- Don't let one leaver or straggler hold a round open.
- Don't ship more than 2 maps that share a layout.
- Don't copy maps, disaster names, characters or UI from NDS, Deathrun, FE2 or Speed Run 4.

## Sources

1. https://natural-disaster-survival.fandom.com/wiki/Changelogs — NDS creation 2008, release 2011-12-04, update history
2. https://natural-disaster-survival.fandom.com/wiki/Disasters — 13 disasters and warning texts
3. https://natural-disaster-survival.fandom.com/wiki/Disaster_Warning — warning banner behavior
4. https://natural-disaster-survival.fandom.com/wiki/Lobby — lobby tower overlooks the round
5. https://natural-disaster-survival.fandom.com/wiki/Gamepasses — Green Balloon, Red Apple, Yellow Compass vote pass, Weather Machine R$75
6. https://natural-disaster-survival.fandom.com/wiki/Round_Control — private-server map/disaster control
7. https://deathrun.fandom.com/wiki/Lobby — 15 s intermission, lobby activities, spectator mode
8. https://deathrun.fandom.com/wiki/The_Hand — anti-stall entity, ~30 s spawn
9. https://deathrun.fandom.com/wiki/Ghosts — dead runners as ghosts, rules
10. https://deathrun.fandom.com/wiki/Checkpoints — 3–5 per map, every 2–4 traps, rewards
11. https://deathrun.fandom.com/wiki/Traps — trap states, 7–30 s recharge
12. https://deathrun.fandom.com/wiki/Gamepasses — pass prices and effects
13. https://deathrun.fandom.com/wiki/Tickets — daily missions
14. https://deathrun.fandom.com/wiki/Seasons — seasons 2019-10 to 2021-12
15. https://flood-escape-2.fandom.com/wiki/Map_Voting — pre-votes, cooldowns, vote stacking
16. https://flood-escape-2.fandom.com/wiki/Buttons — buttons, group buttons, XP values
17. https://flood-escape-2.fandom.com/wiki/Rescue_Missions — rescue NPCs, 100 XP
18. https://flood-escape-2.fandom.com/wiki/Spectate — spectate from lobby or round
19. https://flood-escape-2.fandom.com/wiki/Intermission — intermission screen contents
20. https://flood-escape-2.fandom.com/wiki/Difficulty — 6 difficulty tiers
21. https://www.roblox.com/games/183364845 — Speed Run 4 description (official game page)
22. https://create.roblox.com/docs/production/promotion/rewarded-video-ads — reward value and placement guidance
23. ../patterns/round-system.md — phase timings, voting, spectate, rewards implementation
24. private/trends/latest.md and its 2026-10-22 dated copy — players, genres, themes, game descriptions (data)

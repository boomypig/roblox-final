---
title: Asymmetric survival
type: genre
read-when: Building killer-vs-survivors rounds with character rosters, ability kits, objectives, or killer rotation.
last-researched: 2026-10-22
---

# Asymmetric survival

## In one line

One powerful killer hunts a team of weaker survivors on a small map for a few minutes;
survivors win by working objectives and outlasting the clock, the killer by eliminating them.
Rosters of characters with ability kits are the long-term meta. List it as **Survival /
1 vs All** (data, 2026-10-22; see [metadata](../fundamentals/metadata-thumbnails-icons.md)).
Co-op PvE horror runs live in [horror](horror.md); hidden-role rounds in
[social-deduction](social-deduction.md).

## Core loop

- **Moment to moment (5–45 s):** survivor: work an objective (repair, hack) → hear or see the
  killer → break line of sight, use a stun or escape ability → heal or rescue → back to work.
  Killer: patrol → find → chase → down → pressure the next objective.
- **Round (3–8 min, inferred):** role assignment → short spawn grace → objectives cut the
  clock → last-survivor endgame → results with rewards. Forsaken survivors win by surviving
  "until the timer hits 0" (data, game description 2026-10-22); repairs take time off the
  clock (community guides, unverified amounts).
- **Session:** 5–10 rounds in the same server, rotating killer turns (inferred).
- **Meta (weeks):** soft currency → buy survivors and killers; XP per character; skins and
  emotes; events with their own currency. Forsaken: 9 killers and 12 survivors by 2026-10-02,
  bought from a shop, one free starter (press, PocketGamer 2026-10-02).

## Main verbs

Survivor: repair, hack, hide, sprint, stun, block, heal, rescue, distract, escape.
Killer: track, chase, trap, ambush, down, use ultimate, defend objectives.

## Why players come back

- **Role rotation:** every few rounds you get the power fantasy of being the killer (inferred).
  Forsaken picks the player with the highest Malice, a meter built by doing survivor objectives
  (press, AllThingsHow 2026-09-02).
- **Roster mastery:** each character is a new way to play with its own XP track (press,
  AllThingsHow 2026-09-02).
- **Short, bounded rounds** that fit a few minutes of free time (inferred).
- **Friends:** survivor co-op plus bragging rights; Forsaken gives up to 20% extra XP with
  friends (press, AllThingsHow 2026-09-02).
- **Retention evidence:** Forsaken is Top Revisited #22 while #21 by players (data, 2026-10-22).

## What separates top games from clones

- **Distinct kits with counterplay.** Every killer power has a visible tell and a survivor
  answer; every survivor stun has a cooldown the killer can read (inferred).
- **Objectives that create risk.** Forsaken's generators have 4 stages and a skill check, and a
  failed check alerts the killer (press, AllThingsHow 2026-09; Bluestacks 2025-07). Work makes
  noise; noise starts chases (inferred).
- **Scarce chase-breakers.** Violence District calls its pallets "a scarce and limited resource
  to stun the killer" (data, game description 2026-10-22). Limited stuns make chases readable
  and finite (inferred).
- **Fair role selection and anti-AFK design** (below).
- **Continuous balance patches.** One Forsaken update changed eight killers at once (community
  tracker RoWatcher, unverified). Top games log win rates and patch often (inferred).
- **Original characters.** Clones reuse film killers or another game's cast and take on IP and
  discovery risk (inferred; see [trend lifecycle](../fundamentals/trend-lifecycle.md)).

## Role balance and ratios

Observed in our snapshot (server size from the tracker, data 2026-10-22):

| Game | Max per server | Killer : survivors | Players |
|---|---|---|---|
| Flee the Facility | 5 | 1 : 4 | 79.9K |
| Violence District | 6 | 1 : 5 (description: "5 survivors … against a killer") | 21.8K |
| Forsaken | 9 | 1 : 8 (press: "8 Survivors vs. 1 Killer") | 47.3K |
| Murder Mystery 2 | 12 | 1 murderer + 1 sheriff : 10 innocents (community) | 675K |
| Dead by Daylight (PC reference) | — | 1 : 4 (community) | — |

Rules (inferred, starting values to tune with telemetry):
- **1:4 to 1:5** when the game is about chases: each survivor gets chased several times per round.
- **1:6 to 1:8** only if survivors have team abilities (heals, shields, stuns) and win on a timer.
  Forsaken's 1:8 works with kits and a clock.
- Above 1:8, add a second killer. Forsaken announced a "Double Trouble" mode for v4.0.5
  (community tracker RoWatcher, unverified).
- **Scale the round to the survivor count:** fewer survivors → shorter timer and fewer
  objectives, so a 1v2 at low CCU is still playable.
- **Targets:** each killer's win rate 40–60%; each survivor's survival rate 35–60%; median
  chase 20–45 s; time to first chase under 60 s.
- **Speeds** (default `Humanoid.WalkSpeed` 16, official): survivors walk 16 and sprint 22–26 on
  stamina; killer base 1.0–1.1× survivor sprint, with lunges or dashes for bursts and slow-down
  when attacking. The killer catches a survivor in the open; survivors survive by looping
  obstacles, stuns and line-of-sight breaks.
- **Stuns:** 1.5–3 s; one stun per survivor per 30–60 s; brief killer immunity after a stun so
  stuns can't chain.
- **Downs and eliminations:** 2–3 hits to down or eliminate; a rescue window so one mistake
  isn't instant loss.

## Objectives

| Type | How it works | Seen in |
|---|---|---|
| Repair stations | Multi-stage progress with skill checks; failure alerts killer | Forsaken generators, 4 stages (press, AllThingsHow 2026-09-02) |
| Hack → exit | Hack N computers, then open exits and leave | Flee the Facility "unlock the exits" (data, description) |
| Timer survival | Live until 0; objectives shorten the clock | Forsaken (data, description) |
| Task lists | Several small tasks across the map | Forsaken objectives, Among Us-like (community) |

Rules (inferred): 1 objective per survivor + 1–2 spare; spread them so the killer can't guard
two at once; 15–30 s solo work time per stage; stacking survivors speeds work but splits the
reward (Forsaken splits shared generator XP, press, AllThingsHow); after the last survivor
remains, switch to an endgame with a short clock and reveal both positions (community guides
on Forsaken's last-survivor phase, unverified).

## Abilities per character

See [ability-kits](../patterns/ability-kits.md). Starting shape (inferred):
- **Survivor:** 1 passive + 2 actives. Cooldowns 20–60 s. Roles: support (heal), defense (stun
  or block), mobility (dash, speed), information (reveal killer), objective (faster repair).
  Forsaken guides group survivors this way (community).
- **Killer:** 1 passive + 3 actives + an ultimate charged by a meter. Each killer has one
  identity: trapper (traps, trails), summoner (turns eliminated players into minions), trickster
  (fake objectives) (press, PocketGamer 2026; community guides).
- Every active has a sound and visual tell visible to the other side.
- Server-authoritative: cooldowns, hit checks and stuns run on the server
  ([security](../fundamentals/security-and-anti-exploit.md)). Never trust a client "I stunned
  the killer".

## Unlock economy

- One free survivor and one free killer at start (Forsaken's starter survivor is free, press,
  PocketGamer 2026-10-02).
- Soft currency per round, more for wins and objective work. Forsaken's Summer Games event
  paid 160 Tix for a killer win and 80 for a survivor win, 45 XP per elimination and 15 XP per
  generator stage (press, AllThingsHow 2026-09-02).
- Characters sold for soft currency, not Robux only (press, PocketGamer 2026-10-02). First
  purchase within ~5 rounds; later characters 15–30 rounds (inferred).
- XP per character, cosmetic rewards at character levels (inferred; Forsaken tracks XP per
  character, press).
- Robux: VIP (599 Robux in both Forsaken and Violence District, 1.25× XP in Forsaken), skin
  packs 349, emote packs 149–199 (official game-pass API, read 2026-10-23; AllThingsHow).
  Rotating limited packs: Forsaken has 7 off-sale passes (official API, 2026-10-23).
- Event currencies with tiers that unlock in any order (press, AllThingsHow 2026-09-02).

## Matchmaking and round flow

See [round-system](../patterns/round-system.md). Rules (inferred):
- Rounds run inside one server: lobby/intermission 15–30 s → role reveal 5 s → spawn grace
  10–15 s (killer held back) → round → results 10 s.
- **Minimum players to start: 2.** Below the target ratio, shorten the timer and remove
  objectives. A fresh game at low CCU will rarely fill a 9-player server.
- **Killer selection:** a meter (Malice-style) raised by survivor objective work and reset on
  becoming killer; never the same killer twice in a row unless they're alone.
- Parties stay on the same side. Mid-round joiners spectate and get the next round.
- Server size = max ratio + 0 spare (Forsaken 9, Flee the Facility 5, data); spares would
  have to sit out.
- Cross-server party queues later: `TeleportService:ReserveServerAsync` /
  `TeleportService:TeleportAsync` and `MemoryStoreService` (official APIs). Not for v1.

## Toxicity and AFK handling

Rules (inferred unless tagged):
- **No rewards without activity:** Forsaken gives no idle or offline XP (press, AllThingsHow).
  Pay for objective progress, chases survived and rescues, not for time alive.
- **AFK killer:** no movement for 20–30 s after spawn → swap the role to the next-highest meter.
- **AFK survivor:** no input for 60 s → mark AFK, exclude from rewards and from the killer
  meter; `Player.Idled` fires after ~2 minutes of no input (official, unverified timing).
- **Tunneling** (chasing only the just-rescued survivor): 5–10 s protection after a rescue.
- **Camping** (guarding a downed survivor): rescue progress speeds up while the killer is near.
- **Teaming** (killer cooperating with survivors): reward the killer only for eliminations and
  pressure; publish rules. Flee the Facility links its game rules from the description (data).
- **Chat:** `TextChatService` only; post-round taunts via emotes. Avoid player votekicks,
  which become bullying tools.
- **Exploits:** server checks on speed and hits; `Players:BanAsync` with an appeal path
  ([security](../fundamentals/security-and-anti-exploit.md)).

## Session shape

- **First 60 seconds:** join → lobby with a playable area → first round within 30 s, as a
  survivor with a starter character → objective marker on screen (inferred). See
  [first-time experience](../fundamentals/first-time-experience.md).
- **First 10 minutes:** 2–3 rounds, one killer turn if the server is small, first character
  affordable (inferred).
- **Day 7:** 2–3 characters owned, a favorite killer, a cosmetic goal, daily objectives
  (Forsaken has daily objectives, press, AllThingsHow) (inferred).

## Social hooks

Party queue that keeps friends together, friend XP bonus (Forsaken up to 20%, press),
spectate teammates, emotes, rescue moments for clips, `SocialService:PromptGameInvite` after a
win (official API), private servers for friend lobbies ([private-servers](../patterns/private-servers.md)).

## Monetization that works here

Cosmetics (skins, emotes, death effects), VIP XP boost, timed XP boosts (Forsaken: 3-hour boost,
press), event currency bundles, private servers. Avoid selling characters for Robux only or
stat-boosting skins: paid power in a PvP role game reads as pay-to-win (inferred). See
[monetization](../fundamentals/monetization.md).

## Common failure modes

- Servers never fill: a 1:8 design at 50 CCU means empty rounds (inferred).
- One dominant killer or survivor kit and no telemetry to see it (inferred).
- Killer queue starvation: some players never get a killer turn and leave (inferred).
- Endless chases: no stun limits or line-of-sight breaks, or a killer too slow to ever catch
  anyone (inferred).
- Building on another IP: Outcome Memories states its characters belong to SEGA (data, game
  description 2026-10-22); this invites takedowns ([metadata](../fundamentals/metadata-thumbnails-icons.md)).
- Moderate or Restricted gore by accident; see the maturity table in [horror](horror.md).
- Flashing and loud audio without a warning (Forsaken and DOORS warn, data).

## Saturation & opportunity

All (data, 2026-10-22) unless tagged:
- **1 vs All:** 843K players across 8 games, 12.0% of all charted players, but Murder Mystery 2
  holds 675K. The other 7 share ~168K: Flee the Facility 79.9K, Forsaken 47.3K, Violence
  District 21.8K, Outcome Memories 8.7K, 3008 5.9K, Hide From The Hulk 3.8K, Daybreak 383.
- **`killer-survivor` theme:** 3 games, 803K, "one game dominates" (MM2 84%); **0 rising**.
  The tagger misses Violence District, Outcome Memories and Daybreak, so the real asymmetric
  field is larger than the theme shows (inferred, from our lookup).
- Small asym games exist in the long tail: JUST ONE MORE ASYM 468, Daybreak 383 (data).
- Peaks: Forsaken 138K+ (community tracker, unverified); Violence District ~168K on 2026-05-16
  (community tracker RoWatcher, unverified).
- **Opportunity (inferred):** no new asym breakout in our data; the leaders are 1–9 years old.
  A new entry needs a twist that changes what players *do*: a novel objective (build, carry,
  ritual), a PvE killer for low-CCU servers, a 2-killer format, or a Mild-rated "cute" roster
  for under-16s. Expect slow growth: rosters take time.

## Scope for a solo dev

**MVP (7–9 weeks, one dev with Claude Code, no artist) (inferred):** 6-player server (1:5),
one map, 1 killer + 4 survivors with kits (1 passive + 2 actives each, killer 3 + ultimate),
repair objective with skill check, timer win, Malice-style selection, scaling for 2–6 players,
soft currency, shop, XP per character, saving, AFK handling, win-rate logging.

| Week | Build |
|---|---|
| 1 | Round state machine, roles, spawn grace, timer scaling ([round-system](../patterns/round-system.md)) |
| 2 | Map greybox with loops, objectives with skill checks, line-of-sight breaks |
| 3 | Killer base kit: chase speed, hits, downs, eliminations (server-side) |
| 4 | 4 survivor kits and the killer's actives + ultimate meter ([ability-kits](../patterns/ability-kits.md)) |
| 5 | Selection meter, AFK rules, spectate, results screen |
| 6 | Currency, shop, XP per character, [player-data](../patterns/player-data.md), VIP and skin pass |
| 7 | Win-rate and chase-length analytics events ([analytics](../fundamentals/analytics.md)), balance pass |
| 8–9 | Phone test, onboarding, metadata, maturity questionnaire; second killer if time allows |

- **No artist:** characters as R15 rigs with simple accessories and strong color identity; one
  readable silhouette per killer; built-in materials (inferred).
- **Cut:** more than one map, lore cutscenes, trading, ranked queues, cross-server
  matchmaking, more than 6 characters at launch (inferred).

## Top examples

- Forsaken (case study: forsaken): 1:8 roster game with timer win and Malice
  selection; 47.3K (data, 2026-10-22).
- Flee the Facility: 1:4 beast vs survivors, hack and escape; 79.9K, 92% likes, 9 years old,
  last updated 2026-10-01 per its description (data, 2026-10-22).
- Violence District: Dead by Daylight-like 1:5 with scarce pallets; 21.8K (data, 2026-10-22).
- Murder Mystery 2 (case study: murder-mystery-2): hidden-role variant, 675K (data).
- Dandy's World: PvE roster variant, co-op Toons vs AI monsters; 91K (data, 2026-10-22).
  See [horror](horror.md).

## Build checklist for agents

### Do
- Start at a 1:4–1:5 ratio; go to 1:8 only with team kits and a timer win.
- Let a round start with 2 players and scale timer and objectives to the survivor count.
- Pick the killer with a meter raised by objective work; no repeat killer back to back.
- Give every ability a tell, a cooldown (20–60 s survivors) and a server-side check.
- Keep stuns 1.5–3 s with post-stun immunity; median chase 20–45 s.
- Log per-character win rate, round length and chase length from day one; patch outliers
  outside 40–60%.
- Pay rewards for objectives, rescues and chases, not idle time; swap AFK killers after 20–30 s.
- Sell cosmetics and XP boosts; sell characters for soft currency.
- Warn about flashing lights and loud audio; answer the maturity questionnaire for the worst
  kill animation.

### Don't
- Don't build a 9+ player ratio for a brand-new game that can't fill servers.
- Don't let the client decide hits, stuns, downs or objective progress.
- Don't sell stat boosts, exclusive killers for Robux only, or immunity.
- Don't use another game's or film's characters, names, maps or music.
- Don't add votekick or open taunt chat; use emotes.
- Don't ship more than 6 characters before telemetry shows the first ones are balanced.

## Sources

1. private/trends/latest.md, `trends lookup` and the tracker DB — 1 vs All and theme numbers, server sizes, descriptions (data, 2026-10-22)
2. https://www.pocketgamer.com/roblox/forsaken-tier-list — Forsaken roster 9 killers / 12 survivors, shop unlocks, free starter, kit types (2026-10-02)
3. https://allthings.how/roblox-forsaken-how-to-get-tix-and-xp-fast/ — Malice selection, generator stages, rewards, no idle XP, friend bonus, VIP, event tiers (2026-09-02)
4. https://www.bluestacks.com/blog/game-guides/roblox/rl-forsaken-beginners-guide-en.html — failed skill checks alert the killer (2025-07-08)
5. https://rowatcher.com/news/forsaken-s-floral-update-drives-the-survival-horror-hit-past-86k-players — 8 vs 1, peaks, balance patch scope, Double Trouble mode (third-party tracker)
6. https://rowatcher.com/games/6739698191 — Violence District peak ~168K on 2026-05-16 (third-party tracker)
7. https://apis.roblox.com/game-passes/v1/universes/{universeId}/game-passes — Forsaken and Violence District pass prices, read 2026-10-23
8. https://create.roblox.com/docs/reference/engine/classes/Humanoid — default WalkSpeed 16
9. https://create.roblox.com/docs/reference/engine/classes/Player — Idled event
10. https://create.roblox.com/docs/reference/engine/classes/TeleportService — reserved servers, TeleportAsync
11. https://create.roblox.com/docs/cloud-services/memory-stores — cross-server queues
12. https://www.ofzenandcomputing.com/best-strategies-to-win-as-survivor-in-forsaken-roblox/ — repairs cut the clock, last-survivor countdown (2026-04)

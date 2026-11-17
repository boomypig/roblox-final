---
title: Tower defense
type: genre
read-when: Building a tower defense game: unit placement, waves, upgrades, co-op matches, unit summons, or balancing new units against old content.
last-researched: 2026-10-24
---

# Tower defense

## In one line

Enemies walk a fixed path toward your base; you spend match cash to place and upgrade towers
(or summoned anime units) beside it, in co-op parties of up to 4, and win by surviving every
wave. Between matches you unlock or summon better units, which demands harder modes, which
demands better units.

Summons, banners and pity are covered in [gacha raid](gacha-raid.md) and
[rarity tiers](../patterns/rarity-tiers-and-eggs.md). Not repeated here.

## Core loop

- **Moment to moment (1–5 s):** read the incoming wave → place a tower on a valid spot →
  upgrade the one that's carrying → set targeting → collect cash from kills (inferred).
- **Match (10–20 min):** lobby pad → party of 1–4 → map and mode vote → 20–40 waves with a boss
  at the end or every 10th wave → rewards scaled by waves survived → back to the lobby. Tower
  Defense Simulator (TDS): Casual 25 waves in ~10 min, Fallen 40 waves in ~18 min (community, TDS
  wiki 2026-10).
- **Meta (weeks):** coins and XP unlock or summon towers, tower levels and skins, harder modes
  gated by player level (TDS: Intermediate at level 5, Molten 15, Fallen 30, Hardcore 50) (community,
  TDS wiki 2026-10).

## Main verbs

Place · upgrade · sell · set targeting · use ability · vote mode / skip wave · speed up ·
(between matches) unlock / summon · equip loadout · evolve · trait reroll.

## Why players come back

- **New units each update** and the modes that need them (inferred; both leaders ship per update).
- **Progression gates by mode:** each harder mode is a visible next goal (community, TDS level gates).
- **Co-op with friends** in short matches (inferred).
- **Rotating content:** Vanguards' challenges rotate every 30 min, 24 h and 7 days per player,
  capped at 20 completions a day, with doubled rewards on weekends; its boss event rotates weekly
  (community, Vanguards wiki 2026-10). TDS doubles XP Friday to Sunday (community, TDS wiki).
- **Long tails are possible:** TDS set its all-time peak of 159,824 on 2025-10-04, six years after
  it was created (community tracker, Rolimons; data for the 2019-06-05 creation date). Cause not
  checked (unverified).

## Reference numbers: what the leaders ship

**TDS (community, TDS wiki 2026-10):**

| Mechanic | Value |
|---|---|
| Starting cash | $500 (+$100 for joining the group) |
| Base health | 200 (Fallen) |
| Party | Solo, duo, trio or quad; matchmaking fills empty slots |
| Cash from kills | Split evenly: 100% solo, 50% each in duo, 33% trio, 25% quad, regardless of who dealt damage |
| Enemy HP scaling (Fallen) | +15% duo, +25% trio, +40% quad |
| End rewards | Scale with waves survived, plus a win bonus; e.g. Casual coins = 400 ÷ (1 + ((25 ÷ wave) − 1)^1.3) + 50 |
| Starter tower (Scout) | $125, 1 damage, 1 s fire rate, 12 range, footprint 1.5 |
| Scout upgrades | $50 / $375 / $1,350 / $2,200; level 2 adds hidden detection |
| Sell value | ~33% of cash spent ($125 → $41; $175 → $58) |
| Enemy counters | Towers list hidden, lead and flying detection; the right counter gates waves |
| Quests | 4 daily (2 active), 2 weekly (1 active); refills sold for 50 and 120 Robux |

**What the Scout's numbers show (inferred, arithmetic):** DPS per $1,000 spent goes 8.0 → 7.6 →
7.3 → 6.5 → 6.0 from level 0 to 4. Upgrades are slightly *worse* per cash but much better per
placement slot. Placement limits and footprints are what make upgrading the right call, so
ship them together.

**Vanguards (anime summon TD) mode list after ~2 years (community, Vanguards wiki 2026-10):**
Story (12 stages × 6 acts, Normal and Nightmare), Legend stages (11, with modifiers), Challenges
(5 rotating), Raids (4, 20 waves), Dungeons (30 waves with modifier cards that buff units or
enemies), Boss Events (30 waves, a boss every 10, traits disabled), Portals (20 waves, tiers),
Infinite, Rifts (up to 6 players), a roguelike mode with 30+ modifiers, PvP (Assault, Defense,
Ranked; traited and traitless), Sandbox. **Most modes are the same maps with modifiers:** cheap
content once the core works (inferred).

## The balance treadmill

1. Update adds units stronger than the last meta (inferred; summon TDs sell the newest unit).
2. Old modes become trivial, so the update also adds a harder mode or modifier tier (Nightmare,
   Legend, Infinite) (community, Vanguards modes).
3. Players without the new unit hit a wall, which sells summons (inferred).
4. Repeat. When a new game offers a fresh start, players leave together.

**The fade is steep for anime TDs (data, API 2026-10-24; community tracker, Rolimons):**

| Game | Peak | Now |
|---|---|---|
| Anime Defenders | 377,836 (2024-07-21) | 159 playing, 3.43B visits |
| Anime Last Stand | not checked | 50 playing, 1.08B visits |
| Anime Rangers X | not checked | 0 playing, title now starts "[OLD]" |
| Vanguards | 340,167 (2024-09-14) | 30,097 playing, 32 min average session |
| Toilet Tower Defense | not checked | 2,478 playing, 6.20B visits, title starts "[LEGACY]" (2026-10-22) |

Vanguards kept ~9% of its peak two years on; Anime Defenders kept under 0.1% (inferred,
arithmetic). Ways to slow the treadmill (inferred):
- **Equalizer modes** where traits or levels are disabled (Vanguards boss events, traitless PvP).
- **Counters over raw power:** element or attribute counters (hidden, flying, armored) make old
  units useful against specific waves.
- **Cap upgrades by mode** (e.g. Nightmare enemies scale with your best unit's level) instead of
  inflating base stats.
- **Ship modifiers, not only units:** a modifier tier is a week of content with no new art.

## What separates top games from clones

- **Readable maps:** one or two clear paths, distinct placement zones (ground vs cliff vs water),
  the path visibly marked (inferred).
- **Placement feel:** a ghost preview with range circle, red when invalid, snap to valid spots,
  rotate on mobile with a button (inferred; see [ui-ux](../../.claude/skills/roblox-ui/references/ui-ux.md)).
- **Enemy variety with counters:** hidden, flying, armored, splitting, healing, boss abilities that
  stun towers. Each one asks the loadout a question (community, TDS detection stats; inferred).
- **Co-op that shares, not competes:** even cash split and HP scaling (TDS above).
- **Pacing controls:** skip-wave vote, 2x speed, auto-skip setting (community, TDS settings; inferred).
- **Mode ladder:** easy enough for a new player to win the first match, hard enough that the top
  mode takes weeks (community, TDS level gates).

## Session shape

- **First 60 s:** spawn in a lobby with one obvious "PLAY" pad; teleport into a tutorial-easy match
  with 2 starter towers; first tower placed by second 45 (inferred; see
  [first-time experience](../fundamentals/first-time-experience.md)).
- **First 10 minutes:** win one short match (15–20 waves), unlock a third tower, see the next mode's
  level gate (inferred).
- **Typical session:** 13–32 min (TDS 12.9 min, Vanguards 32.3 min average; community tracker,
  Rolimons 2026-10-24). Summon TDs hold sessions longer than tower-unlock TDs (inferred).
- **Day 7:** a full loadout, a few towers upgraded or evolved, first hard-mode win with friends,
  weekly quest done (inferred).

## Social hooks

- **Parties of 4** from lobby pads or a party menu, with matchmaking fill (community, TDS).
- **Clutch moments:** a boss with low base HP left is clip material (inferred).
- **Co-op raids/rifts** for 4–6 (community, Vanguards).
- **PvP** as a later mode, never the first (Vanguards added it in Update 6, TDS runs a ranked
  PvP mode; community wikis 2026-10). TDS's PvP launch date wasn't checked (unverified).
- **Lobby showcase:** equipped units or tower skins visible in the lobby (inferred). See
  [social and virality](../fundamentals/social-and-virality.md).

## Monetization that works here

Game passes read from the Roblox API on 2026-10-24 (data):

| Game | Passes (Robux) |
|---|---|
| TDS | Towers sold directly: Hacker 2,249, Gatling Gun 1,949, Engineer 1,690, Pursuit 1,500, Mercenary Base 1,350, Warden 450, Saboteur 449, Cowboy 340, Turret 340, Mortar 300, Crook Boss 225; "limited time" towers 499–799; VIP 375; Sandbox Plus+ 7,999; custom music 85 |
| Vanguards | Shiny Hunter 1,299, Cosmetic Recolor 799, Display All Units 599, VIP 299, Extra Unit Storage 149; luck potions 99 and 199 (community, wiki) |

- **Two models.** Unlock TDs (TDS) sell towers outright; summon TDs (Vanguards) sell summon
  speed, luck, storage and cosmetics around a gem economy (data; community). TDS is top-earning
  #10 with 11K players; Vanguards #18 with 31.8K (data, 2026-10-22). Selling towers outright to a
  loyal audience earns well per player (inferred).
- **Paid towers are pay-to-win in co-op only.** Acceptable when every mode can be won with free
  towers (inferred). In PvP, keep paid units out or offer traitless queues.
- **"Limited time" must be true.** Under Roblox's honest-presentation rule, a countdown or limited
  label on an item that returns unchanged is not allowed (official, 2026-10; see
  [monetization](../fundamentals/monetization.md)).
- **Summons sold for Robux** carry the full paid-random-item rules
  ([monetization](../fundamentals/monetization.md#paid-random-items-eggs-crates-spins-luck-boosts-pity)).
- Cheap repeatables that fit: quest refills, 2x speed or 2x rewards for a match, revive base once
  (inferred).

## Common failure modes

- **Enemies as Humanoids with physics.** Hundreds of `Humanoid` NPCs using `MoveTo` choke the
  server; enemies push each other off the path (community, DevForum 2023-10).
- **Client-trusted placement or cash.** Exploiters place towers anywhere, for free, or report kills
  (see [security](../../.claude/skills/roblox-code/references/security.md)).
- **Unreadable waves:** no preview of the next wave's types; players lose to a hidden wave they
  couldn't see coming (inferred).
- **One mode only:** nothing to do after the first win (inferred).
- **Power creep with no equalizer** (treadmill above).
- **Franchise characters:** many anime TDs use recognizable characters under altered names
  (community, Vanguards unit names). Make original units.
- **Phone collapse** in late waves: 200 enemies × particles × 4 players' towers (inferred; see
  [performance](../../.claude/skills/roblox-map/references/performance-and-devices.md)).

## Saturation & opportunity

From the tracker (data, 2026-10-22, single snapshot):

- **Subgenre Tower Defense: 22 charted games, 116K players, 1.6% share.** Theme `tower-defense`:
  15 games, 55K, Cameraman Tower Defense the biggest at 27%. The theme keyword **misses the two
  anime summon TDs** (Vanguards 31.8K, Anime Adventures 14.8K), so the subgenre number is the one
  to use (data; inferred).

| Game | Players | Created | Note |
|---|---|---|---|
| Vanguards | 31.8K | 2024-01-28 | anime summon TD; 24 per server |
| Cameraman Tower Defense | 14.9K | 2026-08-26 | meme-themed; 99% likes; top-revisited #4; page says all assets are its own |
| Anime Adventures | 14.8K | 2021-12-21 | top-revisited #3 |
| Tower Defense Simulator | 11.3K (19.2K on 2026-10-24) | 2019-06-05 | top-earning #10; 50 per lobby server |
| Anime Mysterious | 8.7K | 2026-05-03 | anime TD |
| All Star Tower Defense | 6.3K | 2020-05-07 | |
| Candy Kingdom Defense | 3.7K | 2026-09-29 | up-and-coming #23 |
| Garden Tower Defense | 2.9K | 2025-05-14 | theme borrowed from the farming wave; 98% likes |

- **New entries do break out at a small scale:** four TDs created in 2026 hold 2.4K–14.9K (data).
- **Anime summon TD is a spent wave** for a newcomer: the 2024 leaders fell 99%+ and only one
  holds 30K (table above) (inferred).
- **Opportunity (inferred):** a co-op TD with an original, non-character theme (toys, plants,
  machines), short matches and modifier-driven modes. Themes from the current waves
  ([trend lifecycle](../fundamentals/trend-lifecycle.md)) can be borrowed as a skin, as Garden TD
  did, without copying names or assets.

## Scope for a solo dev

**TD is the most animation-light combat genre.** Towers can be part-built models that rotate to
the target (`CFrame.lookAt`) with a muzzle flash and a projectile; enemies can glide and bob along
the path. Characters as towers (anime units) need idle and attack clips per unit, which is the
expensive version (inferred). Pick turrets, plants or toys for an MVP.

**Architecture (community pattern, DevForum 2023-10; details inferred):**
- **Server:** each enemy is data `{id, kind, hp, speed, distance, flags}` advanced along the path
  by distance at a fixed tick. Position = point on the waypoint polyline at `distance`. No
  `Humanoid`, no physics, no `MoveTo`.
- **Client:** receives spawn (`id, kind, spawnTime`) and state events (hit, slowed, died) and
  renders its own model, computing position from the same path and time. Send batches; a
  `buffer` payload keeps them small (official API). Use `UnreliableRemoteEvent` for periodic
  position corrections only (official API).
- **Towers:** the server owns placement and attacks. Each tick a tower picks a target by mode
  (First, Last, Strongest, Closest) from enemies in range, applies damage and tells clients to
  draw the shot.
- **Placement validation (server):** owner has the cash; spot is in a placement zone, off the path
  by at least the footprint; no overlap with other towers (`Workspace:GetPartBoundsInRadius` or
  a grid); under the tower's placement limit; match not over.
- **Matches in their own place:** lobby + match place in one universe; send parties with
  `TeleportService:TeleportAsync` and `TeleportOptions.ShouldReserveServer = true` (official API).
  Teleports don't work in Studio playtests (official), so test the match place directly with a
  debug party.

**MVP (inferred):** lobby with party pads, 2 maps, 8 towers with 4 upgrade levels each, 6 enemy
types (normal, fast, armored, hidden, flying, boss), 3 modes (Easy 20 waves, Normal 30, Hard 40),
co-op up to 4, coins and XP, tower unlocks, daily quests, VIP + skins.

**Build order (one developer with Claude Code, inferred):**

| Week | Build |
|---|---|
| 1 | Path module, server enemy simulation, client renderer, wave table → spawner, base HP, win/lose |
| 2 | Placement ghost + server validation, targeting modes, attack tick, upgrade/sell, cash from kills |
| 3 | 8 towers, 6 enemy types with counters, 30 balanced waves (spreadsheet: wave HP vs best-case DPS), skip vote, 2x speed |
| 4 | Lobby, parties, reserved-server teleport, cash split, HP scaling by party size, rewards saved before teleport back |
| 5 | Unlocks, XP levels, mode gates, second map, daily quests, codes |
| 6 | Passes and skins, FTUE match, phone pass with 150+ enemies, analytics funnel, launch |

**Cut:** summons and banners, PvP, evolutions, traits, infinite mode, sandbox, more than 2 maps.
Add one modifier mode per update after launch.

## Top examples

- Tower Defense Simulator: the unlock-based reference since 2019; co-op rules, mode ladder,
  towers sold as passes (data; community).
- Vanguards: the anime summon reference; banners and pity in [gacha raid](gacha-raid.md).
- Anime Defenders: 2024 spike, near-zero by 2026 (data).
- Cameraman Tower Defense: 2026 meme-themed breakout (data).

## Build checklist for agents

### Do
- Simulate enemies as server data advanced by path distance; render them on the client.
- Validate every placement on the server: cash, zone, path clearance, footprint overlap, placement
  limit, match state.
- Give every tower a range circle in the ghost preview and a red invalid state.
- Ship placement limits with upgrades; check that the top upgrade beats two base towers per slot.
- Split kill cash evenly in co-op and scale enemy HP by party size (start at +15/25/40%).
- Pay partial rewards by waves survived.
- Show the next wave's enemy types before it starts.
- Add counters (hidden, flying, armored) so loadouts matter.
- Give boss waves a telegraphed ability (stun towers, speed burst) with a counter.
- Test late waves on a phone with 150+ enemies and 4 players' towers.
- Make each new mode a modifier on existing maps before building new maps.

### Don't
- Don't use `Humanoid:MoveTo` or physics for enemies, or let enemies collide with each other.
- Don't trust client-sent positions, kills, damage or cash.
- Don't sell towers that are required to win any mode.
- Don't label items "limited" if they return unchanged.
- Don't add a summon banner at launch; prove the match is fun first.
- Don't release units that obsolete everything without an equalizer mode.
- Don't use franchise character names, likenesses or signature moves.

## Sources

1. https://tds.fandom.com/wiki/Casual_Mode — 25 waves, ~10 min, $500 start, cash split per player, reward formula (wiki, read 2026-10-24)
2. https://tds.fandom.com/wiki/Fallen_Mode — 40 waves, ~18 min, 200 base HP, HP scaling 15/25/40%
3. https://tds.fandom.com/wiki/Gamemodes — mode list and level gates
4. https://tds.fandom.com/wiki/How_to_Play — parties of up to 4, matchmaking fill, quests and Robux refills, XP settings
5. https://tds.fandom.com/wiki/Scout — cost, stats, upgrade costs, sell values, hidden detection, footprint
6. https://animevanguards.fandom.com/wiki/Gamemodes — Vanguards mode list, challenge rotation and caps
7. https://animevanguards.fandom.com/wiki/Summon — luck potion prices, summon structure
8. https://apis.roblox.com/game-passes/v1/universes/1176784616/game-passes — TDS passes (read 2026-10-24)
9. https://apis.roblox.com/game-passes/v1/universes/5578556129/game-passes — Vanguards passes (read 2026-10-24)
10. https://games.roblox.com/v1/games?universeIds=5836869368,4509896324,6884266247 — Anime Defenders, Anime Last Stand, Anime Rangers X current numbers (read 2026-10-24)
11. https://www.rolimons.com/game/17017769292 — Anime Defenders peak 377,836 (2024-07-21)
12. https://www.rolimons.com/game/16146832113 — Vanguards peak 340,167 (2024-09-14), 32.25 min playtime
13. https://www.rolimons.com/game/3260590327 — TDS peak 159,824 (2025-10-04), 12.88 min playtime
14. https://devforum.roblox.com/t/tower-defense-enemy-system/2667346 — invisible server roots with client visuals, Humanoid state cost (2023-10)
15. https://create.roblox.com/docs/reference/engine/classes/TeleportService — TeleportAsync, TeleportOptions, no teleports in Studio
16. https://create.roblox.com/docs/reference/engine/classes/UnreliableRemoteEvent — unreliable remotes
17. https://create.roblox.com/docs/reference/engine/libraries/buffer — buffer payloads
18. private/trends/latest.md and tools/trends lookups — subgenre and theme totals, game rows (data, 2026-10-22)

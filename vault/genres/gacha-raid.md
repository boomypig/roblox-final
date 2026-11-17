---
title: Gacha raid (unit gacha + PvE fights)
type: genre
read-when: Building dice/unit/character gacha where rolled units fight raids, towers, bosses or dungeons (Anime Dice-likes, card battlers, summon-and-raid games).
last-researched: 2026-10-24
---

# Gacha raid (unit gacha + PvE fights)

## In one line

Roll or summon anime-style units, improve the keepers with more rolls (traits, grades, shinies),
and send a team into PvE content (tower floors, raids, boss rushes) whose rewards buy more rolls.
The roll is the dopamine; the fight is the gate that makes a rare unit matter.

Placement-based unit games are [tower defense](tower-defense.md). Rolls for cosmetic status only
are [RNG aura](rng-aura.md). Odds, pity and reveal rules live in
[rarity tiers and eggs](../patterns/rarity-tiers-and-eggs.md); this file doesn't repeat them.

## Shapes that ship (2026)

| Shape | Example | Who fights | Combat cost for a solo dev |
|---|---|---|---|
| Idle plot + auto-battle | Anime Dice (case study: anime-dice): roll dice → place units on a plot that earns cash offline → auto-resolved tower floors pay gems (community, 2026-09) | Units, automatically; can run hidden in the background | Low: stat simulation, a lunge tween, damage numbers |
| Summon + wave modes | Vanguards (renamed from Anime Vanguards): banners → story, raids, boss events, challenges (community, wiki 2026-10) | Units placed on a map | Medium: see [tower defense](tower-defense.md) |
| Action RPG + unit army | Arise Crossover: defeat an enemy, raise it as a "Shadow" ally; timed tower dungeon with 100 floors (press, Sportskeeda 2025; Deltia's via search snippet, unverified) | You and your units | High: player combat kit plus unit AI |
| Card battler | Anime Card Clash: roll cards, build a deck, story maps, infinite towers, nightmare modes, PvP ranking, "Secret Boss Raids" (data, game page 2026-10-22) | Cards | Low to medium; 2D card art is the cost |

## Core loop

- **Moment to moment (1–5 s):** roll → tiered reveal → keep, auto-sell or feed → (in battle)
  watch units fight, tap a skill or speed-up (inferred).
- **Session (20–40 min):** spend income on rolls and luck, reroll a keeper's trait or grade, push
  1–3 floors or one raid run, claim quests, rebirth when the multiplier is worth it (community,
  Anime Dice guides 2026-09; inferred). Anime Dice averages 32 min a session (community tracker,
  Rolimons 2026-10-24).
- **Meta (weeks):** complete the unit index, chase the top tier on the current banner, max a team
  for the newest tower or the weekly boss, return for the weekly update and its codes (community;
  inferred).

## Main verbs

Roll/summon · auto-roll · equip team · reroll trait · roll grade · fuse or evolve · place units
(plot or map) · start floor/raid · speed up / skip · collect offline income · rebirth · trade.

## Why players come back

- **Banners rotate.** Vanguards rotates featured units **every hour** and lets players pick the
  featured Mythic on a Selection banner once per 24 h (community, wiki 2026-10). There's always
  a "this hour" reason to check (inferred).
- **Weekly content on a fixed slot.** Anime Dice shipped Updates 4–8 one week apart (2026-09-12 to
  2026-10-11), each with a 3-day event and new codes (community, bloxodes 2026-10-24). Vanguards
  rotates its boss event weekly (community, wiki 2026-10).
- **Offline income** on a plot pays out on return ([idle and offline income](../patterns/idle-offline-income.md)).
- **Layered rerolls** give a bad day value: a mediocre unit can still roll a Z++ grade (50x
  income in Anime Dice, community 2026-09-14) (inferred).
- **Pity counters** turn a losing streak into a countdown (inferred; see rarity file).

## What separates top games from clones

1. **Banner structure, not one flat pool.** Vanguards' Special banner: the middle unit is a 50%
   share and the two side units 20% each of the featured rate (community, wiki 2026-10). Featured
   units make the same odds feel new every hour (inferred).
2. **Pity at ~2× expected pulls, shown in UI.** Vanguards: Legendary 4% with pity at 50 (expected
   25); Mythic 0.5% with pity at 400 (expected 200); top tier 0.005% with a **one-time** pity at
   20,000–25,000 summons (community, wiki 2026-10). That matches the rarity file's 2× rule.
3. **Luck boosts that can't break the top.** Vanguards' Robux luck potions (99 and 199 Robux,
   1 hour, stacking to +62.5%) raise Legendary and Mythic odds only; they **don't** touch Secret,
   Vanguard or shiny odds and don't reduce pity (community, wiki 2026-10).
4. **Independent variant rolls.** Shiny is a separate 1.5% roll on eligible units (3% with a
   1,299-Robux pass) (community, wiki 2026-10; data, API 2026-10-24). Anime Dice stacks traits,
   grades and mutations on one unit (community, 2026-09). More chase per model.
5. **Equalizer modes.** Vanguards' Boss Events **disable traits**, and its PvP offers traited and
   traitless variants (community, wiki 2026-10). A fair mode keeps unlucky players in co-op.
6. **Raid rewards that feed the roll.** Boss runs pay summon currency (200–250 gems per run) plus a
   2% chance of the boss as a unit with **pity at 75 runs** (community, wiki 2026-10). Anime Dice
   towers pay gems that buy grades (community, 2026-09-14).
7. **Auto-sell and storage tools.** Auto-sell by rarity (but never shinies or traited units) is
   standard in Vanguards (community, wiki 2026-10). Without it, inventory fills in a day (inferred).

## Raids and co-op: shapes that work

| Mode | Shape (reference) | Players |
|---|---|---|
| Tower floors | Floors in a row, each a fixed enemy team; difficulty settings; endless tower for the top (Anime Dice, community 2026-09) | Solo |
| Boss rush | 30 waves, a boss every 10th wave, stronger each time; Normal and Nightmare; weekly rotation (Vanguards, community 2026-10) | Solo or up to 4 |
| Island raid | 5 rooms in a row, clear all enemies to open the next, boss in the last; reward scales with progress (300–1,000 fragments); entry token bought with soft currency or a unit (Blox Fruits, community wiki 2026-10) | Up to 4 |
| Timed dungeon | 100 floors, 15-minute timer, each cleared floor adds time; portal opens hourly (Arise Crossover, press 2025 via search snippet, unverified) | Party |

Co-op rules (inferred unless tagged):
- **Each player gets their own drops.** Never make players compete for a shared loot roll.
- **Scale enemy HP with party size,** e.g. +15% / +25% / +40% for 2 / 3 / 4 players (Tower Defense
  Simulator's Fallen mode, community wiki 2026-10).
- **Pay partial rewards on failure,** scaled by how far the team got (Blox Fruits raids, community).
  A wipe still moves the meta forward.
- **Queue from a lobby pad, solo or party,** and fill empty slots with matchmaking. Run the raid in
  the same server for the MVP; move to reserved servers
  (`TeleportService:TeleportAsync` with `TeleportOptions.ShouldReserveServer = true`, official API)
  only when raids need their own map.
- Full encounter design: [boss fights and raids](../patterns/boss-fights-and-raids.md).

## Session shape

- **First 60 s:** spawn on your plot or in the lobby, the Roll/Summon button pulsing; first roll in
  ≤ 5 s; a guaranteed Rare in the first 10 rolls; place it and see income tick (inferred; FTUE pity
  as in [rng-aura](rng-aura.md)).
- **First 10 minutes:** ~50–150 rolls, first Epic, first die or luck upgrade, first floor cleared,
  first quest claimed, auto-roll shown (inferred).
- **Typical session:** 20–35 min (Anime Dice 32 min; Arise Crossover 19 min; community tracker,
  Rolimons 2026-10-24).
- **Day 7:** a team with one Legendary+, first rebirth done, a grade rolled at A or better, the
  weekly boss attempted with friends, trading unlocked (inferred).

## Social hooks

- **Small servers with visible plots** (Anime Dice: 9 per server, data 2026-10-22): neighbours see
  your best units and your rare-roll announcements (inferred).
- **Server and cross-server announcements** for top-tier pulls (pattern in rarity file).
- **Co-op raids up to 4** with party invites from the lobby (community, Vanguards and Blox Fruits).
- **Trading** gated behind play (Anime Dice: 1,000 rolls, community 2026-09-14) to slow alt farms.
  Paid-random outcomes need the trading policy checks in [trading](../patterns/trading.md).
- **Leaderboards** for tower floor and strongest team ([leaderboards](../patterns/leaderboards.md)).

## Monetization that works here

| Game | Passes (Robux) |
|---|---|
| Anime Dice | Double Roll 799, Ultra Luck 499, Roll Speed 349, More Traits 329, More Grades 299, VIP 249, Luck 199, More Cash 199 (data, API 2026-10-24) |
| Vanguards | Shiny Hunter 1,299, Cosmetic Recolor 799, Display All Units 599, VIP 299, Extra Unit Storage 149 (data, API 2026-10-24) |

- **Roll speed and roll count** sell best in a roll loop: Anime Dice's priciest pass doubles rolls
  (data). Vanguards' VIP cuts summon cost from 50 to 40 gems (community, wiki 2026-10).
- **Timed luck potions** for Robux are probability modifiers: state the multiplier and duration
  before purchase and show boosted odds while active (official, 2026-10).
- **Summon currency sold for Robux makes every summon a paid random item.** Then you need full
  odds in %, an "Info"/"Details" button, `PolicyService:GetPolicyInfoForPlayerAsync` gating on
  `ArePaidRandomItemsRestricted`, and paid-item trading checks (official, 2026-10). The safe MVP:
  rolls cost earn-only currency; Robux buys passes and convenience (inferred).
- Full rules: [monetization](../fundamentals/monetization.md#paid-random-items-eggs-crates-spins-luck-boosts-pity).

## Common failure modes

- **Power creep with nowhere to use it.** Units get stronger but the content is one tower; week 2
  has nothing to push (inferred).
- **Every update obsoletes the last banner.** Players stop pulling when today's Mythic is next
  week's filler. Keep old units useful in at least one mode (equalizer or element counters) (inferred).
- **Robux-only best units in a mode with rankings** (reviewer: reject; see monetization).
- **Inventory overflow** with no auto-sell, fuse or storage upgrade (inferred).
- **Client-side rolls or battle results.** Exploiters print units and auto-clear floors. Roll and
  simulate on the server ([security](../../.claude/skills/roblox-code/references/security.md)).
- **Spike, then rebuild.** Arise Crossover, built around a named manhwa hero (press, Player.One
  2025-03), peaked at 334,189 on 2025-04-06 (community tracker, Rolimons) and had 380 players on
  2026-10-22, retitled "ARISE 1.0 [STATUS: IN DEV]" with a page saying a team is being assembled
  for an "official 1.0" version (data, 2026-10-22). Content and systems didn't hold players for
  18 months, and borrowed IP adds takedown risk (inferred).

## Saturation & opportunity

From the tracker (data, 2026-10-22, single snapshot; no growth claims):

| Theme | Games | Players | Per game | Median | Leader (share) | Note |
|---|---|---|---|---|---|---|
| `anime` | 41 | 361K | 8.8K | 3.0K | Blox Fruits 34% | "mixed"; spans RPGs, TDs, fighters, incrementals |
| `dice` | 1 | 69K | 69K | 69K | Anime Dice 100% | the only dice game charted |
| `raid-boss` | 3 | 129K | 43K | 4.3K | Blox Fruits 95% | |
| `card` | 3 | 10.0K | 3.3K | 3.7K | Anime Card Clash 46% | |
| `gacha` | 1 | 11K | 11K | 11K | Gacha Online 100% | **a roleplay dress-up game, not unit gacha** (keyword false positive) |

- **Anime Dice is the only unit-gacha game in the top 25:** #17, 68.6K, 99% likes, 68 days old
  (data, 2026-10-22); 74.3K on 2026-10-24 (data, API).
- **2026 anime hybrids are breaking out in Simulation, not RPG:** Anime Dice (2026-08, 69K), My
  Anime Mine (2026-08, 10.4K, tycoon/mining), Anime Astral Simulator (2026-07, 9.3K) (data,
  2026-10-22). The roll-and-idle layer is doing the work; the anime skin is the hook (inferred).
- **Spike risk is real:** Arise Crossover went from 334K to under 1K within 18 months (above).
- **Opportunity (inferred):** a unit gacha with **original characters** and a mode that uses the
  collection (auto tower + weekly co-op boss), cheaper to build than an action RPG. A direct Anime
  Dice clone joins a single-leader theme 10 weeks in; take the shape (roll → plot → auto-battle)
  and change the theme or the battle (see [trend lifecycle](../fundamentals/trend-lifecycle.md)).

## Scope for a solo dev

**The content cost is characters, not code.** No artist means each unit needs a look you can
make yourself. Options, cheapest first (inferred):
1. Rigs built with `Players:CreateHumanoidModelFromDescriptionAsync` from a `HumanoidDescription` of
   catalog accessories and colors (official API). Pick generic items, not franchise knock-offs.
2. Recolors + effects (`ParticleEmitter`, `Highlight`, `Trail`) per rarity tier on 4–5 base rigs.
3. Generated meshes (Studio MCP `generate_mesh`), checked for quality and style consistency.

Animation: share **one idle and one attack per archetype** (melee, ranged, caster) instead of per
unit; auto-battle needs no hitboxes (inferred). Compare the 26–30 clips a two-character
[battlegrounds](battlegrounds.md) MVP needs.

**MVP (inferred):** 20 units in 6 tiers, 8–10 dice or summon tiers, plot with 6–10 pedestals and
offline income, 1 trait reroll layer, a 30-floor auto-battle tower, rebirth, daily quests, codes,
passes (luck, roll speed, more storage).

**Build order (one developer with Claude Code, inferred):**

| Week | Build |
|---|---|
| 1 | Server roll service (integer weights, luck, pity), unit data module, inventory + ProfileStore save, tiered reveal, auto-roll on the server |
| 2 | Plot pedestals, income tick, offline income with welcome-back screen, upgrade lines and the die ladder ([upgrade trees](../patterns/upgrade-trees.md)) |
| 3 | Auto-battle: server stat simulation at a fixed tick (HP, ATK, attack speed, target rule), compact event stream to clients, tower floors 1–30 with a difficulty curve |
| 4 | Trait reroll, rebirth ([rebirth](../patterns/rebirth-prestige.md)), auto-sell and storage, index with rewards |
| 5 | 2–4 player co-op boss (same server, lobby pad), party HP scaling, per-player drops |
| 6 | Passes with odds UI and PolicyService gating, FTUE pity, quests, codes, analytics funnel, phone pass, launch |

**Cut:** trading, PvP, banners beyond one, evolutions, more than one tower, mutations, cutscenes,
reserved-server raids, weekly events (add after launch on a 2-week cadence).

## Top examples

- Anime Dice (case study: anime-dice): 2026 breakout; dice luck ladder, plot income,
  layered rerolls, auto-battle towers, weekly updates.
- Vanguards: banner, pity and boss-event reference (compared in [tower defense](tower-defense.md)).
- Blox Fruits (case study: blox-fruits): co-op island raids that unlock power for an action RPG.
- Arise Crossover: the unit-army action RPG spike of 2025 and its fade (above).

## Build checklist for agents

### Do
- Roll, simulate battles and grant rewards on the server; clients send intents and animate results.
- Keep one server-side odds table per banner/die; generate the displayed % from it with luck applied.
- Pity at ~2× expected pulls per tier, saved in the profile, shown as "guaranteed in N".
- Make luck boosts apply to a capped set of tiers; never let paid luck change the top tier or pity.
- Roll variants (shiny, trait, grade) as separate rolls with their own disclosed odds.
- Give every unit tier a use: auto-sell for currency, feed/fuse, or an equalizer mode.
- Run auto-battle as a fixed-tick stat simulation; send one compact event list per fight.
- Co-op: per-player drops, HP scaling by party size, partial rewards on failure.
- Price rolls in earn-only currency unless the full paid-random-item checklist is implemented.
- Gate trading behind real play (e.g. 1,000 rolls or level 10).
- Ship with auto-roll, skip-reveal and auto-sell from day 1.

### Don't
- Don't roll or decide battle outcomes on the client, or trust client-sent unit IDs or damage.
- Don't sell summon currency for Robux without odds %, Info/Details, PolicyService gating and
  paid-item trading checks.
- Don't make the strongest units Robux-only where they decide rankings or PvP.
- Don't let every update obsolete the previous banner's units.
- Don't use real anime character names, likenesses or signature looks; build original archetypes.
- Don't build per-unit animation sets for the MVP; share archetype clips.
- Don't launch with one flat pool and no mode that uses the collection.

## Sources

1. https://animevanguards.fandom.com/wiki/Summon — banner rotation, 50/20/20 featured split, rarity odds, pity counts, luck potion limits and prices, shiny chance, auto-sell (wiki, read 2026-10-24)
2. https://animevanguards.fandom.com/wiki/Boss_Events — 30 waves, boss every 10, solo or 4 players, weekly rotation, traits disabled, rewards, 2% boss unit with 75-run pity
3. https://animevanguards.fandom.com/wiki/Gamemodes — raids, dungeons, challenges, rifts, PvP traited/traitless
4. https://apis.roblox.com/game-passes/v1/universes/5578556129/game-passes — Vanguards passes (read 2026-10-24)
5. https://apis.roblox.com/game-passes/v1/universes/10708913337/game-passes — Anime Dice passes (read 2026-10-24)
6. https://allthings.how/roblox-anime-dice-guide-upgrade-priority-and-rebirth-timing/ — Anime Dice loop, grades, towers, trading gate (2026-09-14)
7. https://bloxodes.com/wiki/anime-dice — Anime Dice update cadence (2026-10-24)
8. https://blox-fruits.fandom.com/wiki/Raids — 5-island raids, 4-player cap, microchip entry, 300–1,000 fragments
9. https://tds.fandom.com/wiki/Fallen_Mode — party HP scaling 15/25/40%
10. https://www.sportskeeda.com/roblox-news/arise-crossover-a-beginner-s-guide — Arise Crossover shadow mechanic
11. https://deltiasgaming.com/?p=195184 — Arise Crossover Infernal Castle: 100 floors, 15-minute timer, hourly portal (search snippet only)
12. https://www.rolimons.com/game/87039211657390 — Arise peak 334,189 on 2025-04-06
13. https://www.rolimons.com/game/113290951185459 — Anime Dice average playtime 32 min
14. https://create.roblox.com/docs/production/monetization/paid-random-items — paid random item and probability modifier rules
15. https://create.roblox.com/docs/reference/engine/classes/Players — CreateHumanoidModelFromDescription
16. https://create.roblox.com/docs/reference/engine/classes/TeleportService — TeleportAsync, TeleportOptions.ShouldReserveServer
17. private/trends/latest.md and tools/trends lookups — theme stats, game numbers and descriptions (Anime Card Clash, Arise) (data, 2026-10-22)
18. https://www.player.one/roblox-arise-crossover-codes-march-2025-play-solo-leveling-sun-jin-woo-beat-monarchs-160151 — Arise Crossover's licensed-franchise theme (2025-03)

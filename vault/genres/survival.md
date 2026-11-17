---
title: Survival
type: genre
read-when: Building a co-op survival run (day/night cycle, gathering, crafting, a camp to defend, night threats, classes, "survive N days").
last-researched: 2026-10-24
---

# Survival

## In one line

A party of 1–5 friends spends the day gathering and crafting, then holds a safe zone through a
short, dangerous night, and repeats until a day count is reached. The camp is the shared
progress bar; classes unlocked between runs are the meta. The 2025–26 leader is
99 Nights in the Forest (case study: 99-nights-in-the-forest). List it as **Survival**
(99 Nights has no subgenre set, data 2026-10-22). Killer rounds live in
[asymmetric-survival](asymmetric-survival.md), room-by-room horror runs in [horror](horror.md),
and lobby → round disaster games in [round-based-races-and-survival](round-based-races-and-survival.md).

## Core loop

- **Moment to moment (5–60 s):** walk out from camp → chop, mine, loot a chest, hunt → carry the
  haul back → feed the fire or craft at the bench → eat, heal, repeat.
- **Day/night cycle (~4–5 min):** day is for gathering and exploring; night pulls everyone
  back to the light, where a stalker and raids test the defenses. 99 Nights runs 3-minute days
  and 90-second nights (community wiki, 2026-10).
- **Run (≈1–2 h for a full clear, inferred):** escalating fixed beats (first trader on day 2,
  first raid on day 4, a second monster from day 5) plus random events, ending in a finale
  at the target day. Rescuing the 4 missing kids and building beds raises 99 Nights' day
  multiplier to at most 9 days per night (community wiki, 2026-10), so skilled parties finish
  much faster than 99 × 4.5 min (≈7.4 h) (inferred).
- **Meta (weeks):** premium-ish soft currency earned at milestones, dungeons, daily quests and
  badges buys **classes**; each class levels up through its own task counts; seasonal events
  add limited classes and furniture (community wiki, 2026-10).

## Main verbs

Chop, mine, scavenge, carry, fuel, craft, build, cook, eat, hunt, fish, explore, light (torch,
flashlight), defend, revive, rescue, trade with an NPC, decorate.

## Why players come back

- **Shared camp growth.** Every log makes the fire bigger, the safe zone wider and the map larger
  (community wiki, 2026-10). Progress is visible and owned by the group (inferred).
- **Friends.** The description is one line: build a camp with friends (data, game description
  2026-10-22). Co-op days are a ranking signal ([social](../fundamentals/social-and-virality.md)).
- **Class collection.** 39 permanent and 7 limited classes by 2026-09-03 (community wiki).
  Each one changes the run (more logs, faster revives, a shield), so a new class is a reason to
  start another run (inferred).
- **Fresh runs.** Random biomes, chests and events inside a fixed day timeline (community wiki;
  inferred).
- **Weekly events.** 99 Nights holds a live "Update Party" sandbox each weekend before the update
  and ships updates every two weeks (official DevForum spotlight 2025-10-31; community wiki 2026-06).

## What separates top games from clones

- **One central object carries every system** (inferred). In 99 Nights the campfire is the safe
  zone, the map-size gate, the healing spot, the cooker and the flashlight charger (community
  wiki). Clones scatter these across five buildings and players lose the thread.
- **Night is short and readable.** A 1:2 night:day ratio keeps tension high without making
  players sit in camp for minutes (inferred from 90 s / 180 s).
- **An unkillable stalker plus killable raiders.** The 99 Nights deer can't be damaged, only
  stunned by a flashlight, and is scared off by the fire; cultist raids can be fought and can
  enter camp (community wiki). One threat teaches "stay in the light", the other gives combat.
- **Tone for all ages.** The developers chose a tone that "wouldn't alienate younger players"
  over pure horror (official DevForum spotlight 2025-10-31). See the maturity table in
  [horror](horror.md).
- **Fast, live iteration.** Jam → 3-month build → push to thousands of players until something
  breaks → fix (official DevForum spotlight). Clones ship once and stall.
- **Clones:** a copied deer-like mascot, "N Nights/Days in the X" titles, no reason to revisit
  after one clear (inferred; 100 Days at Sea credits 99 Nights in its description, data
  2026-10-22).

## Day/night design

Starting values (inferred unless tagged):

| Setting | Value |
|---|---|
| Day | 150–210 s (99 Nights: 180 s, community wiki) |
| Night | 60–100 s (99 Nights: 90 s, community wiki) |
| Dusk warning | 15 s: sky shift + sound + HUD "Night in 15" |
| First night | Safe or near-safe (99 Nights' stalker doesn't hunt night 1, community wiki) |
| Escalation | A new threat or event every 2–4 days; fixed days for the first 10, random after |
| Finale | Target day 30–50 for a v1 (not 99): a full run must fit one evening |

- Server owns the clock: publish `Phase`, `DayNumber` and `PhaseEndsAt`
  (`Workspace:GetServerTimeNow()` + duration) as attributes. Clients tween `Lighting.ClockTime`
  locally from those values. The reference marks `ClockTime` as not replicated (official), and
  a client tween is smooth and costs no bandwidth (inferred).
- Night lighting: reuse the dark-map values and the brightness slider in [horror](horror.md).
  Keep the camp and resource silhouettes readable at night on a phone (inferred).

## The camp: safe zone and base building

- **Safe zone radius grows with camp level.** 99 Nights has fire levels 1–6, each needing more
  fuel; each level widens the safe zone and the explorable map, and rain and snow drain it
  faster (community wiki, 2026-10). A starting curve (inferred): radius 25 → 40 → 60 → 80 studs;
  fuel cost ×2–3 per level.
- **Fuel drains constantly.** If it hits zero, the stalker spawns at 100% and can enter camp, and
  regen stops (community wiki). A fail state the whole party can see coming (inferred).
- **Scale costs by party size.** 99 Nights raises fuel requirements for larger parties
  (community wiki). Use `cost × (1 + 0.3 × (players − 1))` as a start (inferred).
- **Crafting bench tiers** unlock defenses, beds, traps, storage (community wiki). Keep a
  v1 bench to 3 tiers and 12–20 recipes (inferred).
- **Placement:** grid-snapped, server-validated, inside the camp radius only; cap placed objects
  per run (e.g. 150) for phones (inferred). See
  [base-defense-and-stealing](../patterns/base-defense-and-stealing.md) for defense structures.
- **Safe zone rules on the server:** distance from the fire < radius and fire lit → no stalker
  damage. Monsters target only players outside it (inferred).

## Resources and crafting

- **3–5 raw resources** for v1: wood (fuel + build), scrap (tools), food (hunger), one rare
  (gems or ore) for upgrades (inferred; 99 Nights uses logs, coal, fuel cans, scrap, meat).
- **Carry limit forces trips.** 99 Nights uses a sack with slots; the Scavenger class adds +2
  (community wiki). Trips create the "out and back" rhythm (inferred).
- **Carry as counts, not physics, for v1.** Store the haul in a server inventory and deposit with
  a `ProximityPrompt` at the fire or bench. Physically dragged parts are network-owned by the
  client and easy to exploit (inferred; see [inventory](../patterns/inventory.md),
  [security](../fundamentals/security-and-anti-exploit.md)).
- **Gather validation:** server checks distance (≤ 10 studs) to a tagged node
  (`CollectionService:GetTagged("Tree")`), tool equipped, and a hit cooldown (≥ 0.3 s); node HP
  and drops live on the server (inferred).
- **Regrowth:** 99 Nights lets players plant saplings (community wiki). Respawn nodes or
  allow planting so a long run doesn't strip the map (inferred).
- **Hunger** is the clock inside the day: 99 Nights' Camper class cuts hunger drain 10%
  (community wiki). Drain so a player eats ~2× per cycle (inferred).

## The night threat

- **Stalker (unkillable):** spawns on a random outside player at night; speed rises the longer it
  chases (99 Nights' deer: 35+ walk speed, community wiki); a flashlight stuns it with shorter
  stuns each time; it flees the safe zone and at dawn (community wiki). Use the chase numbers and
  pathfinding rules in [horror](horror.md#monster-design-and-ai).
- **Raids (killable):** a wave of fighters walks into camp on fixed nights (99 Nights: from day
  4, every 4 days, community wiki). Size waves to party size and camp level (inferred).
- **Wildlife (day danger):** wolves, bears; killing a quota drops a key in 99 Nights (press,
  Wikipedia). Day danger keeps gathering from being chores (inferred).
- **Biome bosses** later: one per biome, with its own loot (community wiki; see
  [boss-fights-and-raids](../patterns/boss-fights-and-raids.md)).
- Server rules: `SetNetworkOwner(nil)` on every enemy, damage decided on the server, the client
  only plays effects ([security](../fundamentals/security-and-anti-exploit.md)). The 99 Nights
  programmer predicts hits on the client and rolls back on server rejection (official DevForum
  spotlight); that rollback is hard to get right, so a solo dev should start server-only
  (inferred).

## Co-op roles and classes

- Classes are roles: Lumberjack (bonus logs), Medic (5× faster revives), Support (bond with a
  teammate, absorb damage), Brute (shield + taunt), Hunter, Cook, Fisherman, Base Defender
  (community wiki, 2026-10). Good parties mix them (inferred).
- **Shape (inferred):** 1 passive at level 1, 2 more perks at levels 2–3 unlocked by doing the
  role (99 Nights: e.g. "Logs burned 200", "Revive players 25", community wiki). Leveling by use
  teaches the role and keeps a bought class from being instant power.
- **Revive:** downed → bleed-out → teammate holds a prompt (values in [horror](horror.md#co-op-revive)).
  Solo players get a once-per-run self-revive item (inferred).
- See [ability-kits](../patterns/ability-kits.md) for cooldown and server-check rules.

## Session shape

- **First 60 seconds:** lobby → party pad (1–5) → teleport to a reserved run server → spawn at
  an unlit fire with a starter axe and a pointer to the nearest trees (inferred). Light the fire
  in the first minute.
- **First 10 minutes:** two cycles; first night is safe; first craft (a bench item) and first
  fire level-up; first stalker sighting at the edge of the light on night 2 (inferred).
- **Typical session:** one run, 45–120 min. Offer a mid-run save point or a short mode
  (inferred).
- **Day 7:** first or second class bought, first full clear with friends, chasing a badge or a
  harder mode. 99 Nights added a Hard Mode with more rewards in 2026-01 (community wiki).

## Social hooks

- Party pads that keep friends together; reserved run servers so strangers don't drop in
  (inferred; `TeleportService:ReserveServerAsync`, `TeleportAsync`, official).
- Role synergy (Support bonds with one teammate, community wiki) and revives (inferred).
- Base decorating: 99 Nights sells a Decorator Pass and furniture from events (official API
  2026-10-24; community wiki). A camp worth screenshotting (inferred).
- Live sandbox before updates where devs hand out items (official DevForum spotlight).
- Invite prompt after a night survived or a finale ([social](../fundamentals/social-and-virality.md)).

## Monetization that works here

- **Currency → classes.** 99 Nights sells diamonds (20 for 99 Robux up to large packs) that buy
  classes priced 10–600 diamonds (community wiki, unverified prices). Classes also come from free
  diamonds: milestones, a dungeon, daily quests (5 each), badges, codes (community wiki).
- **Level skips** for classes: 250 and 400 Robux (community wiki, unverified).
- **Convenience passes:** Decorator Pass 199 Robux (official API, read 2026-10-24).
- **Event shops** with event-only currency (candy, eggs) (community wiki).
- Rerolling a random class stock or talents with Robux-bought currency is a **paid random item**:
  odds disclosure and `PolicyService` rules apply ([monetization](../fundamentals/monetization.md#paid-random-items-eggs-crates-spins-luck-boosts-pity)).
- Don't sell "skip the night" or invincibility; the night is the product (inferred).

## Common failure modes

- **Run too long for the audience.** A 7-hour run with no save loses most parties (inferred).
- **Chores without danger.** Gathering with no day threats feels like a job sim (inferred).
- **Nights too long or too dark.** Players sit idle or can't see on phones (inferred).
- **Map too big for phones.** Thousands of trees with leaves; use streaming and low part counts.
  99 Nights' builder keeps part, vertex and instance counts low for mobile (official DevForum
  spotlight). See [performance](../fundamentals/performance-and-devices.md).
- **Client-trusted gathering or carrying:** teleporting logs, instant chopping (inferred).
- **Lost runs.** A server crash wipes an hour; save meta rewards at milestones (inferred).
- **Copying the hit's mascot and title** (inferred; see [trend lifecycle](../fundamentals/trend-lifecycle.md)).

## Saturation & opportunity

All (data, 2026-10-22) unless tagged:
- **Survival** genre: 1.54M players, 21.9% share, 48 games, but Murder Mystery 2 (675K), DOORS
  (184K) and Dandy's World (91K) make up most of it. Co-op "survive N days" games are a small
  slice: 99 Nights 122.7K, 7 Days Cat-Sitting 14.6K, Survive a Million Monkeys 11.9K, 100 Days
  at Sea 10.4K, A Long Flight 2.6K, 100 Waves Later 109.
- **`survival` theme:** 13 games, 205K, "mixed", 99 Nights holds 60%. **`forest` theme:** 3
  games, 148K, "one game dominates" (99 Nights 83%); 🪵 Chop A Forest (22.1K, 31 days old) is an
  incremental sim, not survival.
- **The leader is past its peak:** 122.7K on 2026-10-22 (Thursday 22:46 UTC) and 214K on
  2026-10-25 (Saturday 03:24 UTC) (data), vs a 14M peak (official DevForum spotlight
  2025-10-31) and a 270K weekly average in 2026-08 (press, StudioKrew 2026-08-20, unverified).
  Still top 10 by players and #30 top-earning (data, 2026-10-22). The two snapshots differ in
  time of day, so read the gap as daily swing, not growth (inferred).
- **Spin-offs work at small scale:** 100 Days at Sea moves the loop to a raft at sea and holds
  10.4K with 97% likes (data); Survive a Million Monkeys pairs classes with horde waves (data).
- **Opportunity (inferred):** a new setting plus one changed rule beats a re-skin: a moving base
  (raft, train, caravan), a shorter run (20–40 days, 45 min), or a Mild-rated cozy version for
  under-13s. Roblox's Survival genre is large, but the co-op crafting lane has one leader and a
  few 10K followers. Check [trend lifecycle](../fundamentals/trend-lifecycle.md).

## Scope for a solo dev

**MVP (7–9 weeks, one dev with Claude Code, no artist) (inferred):** lobby with party pads (1–4),
reserved run server, one forest biome, a camp object with 4 levels and a growing safe zone,
day/night cycle with a 30-day finale, 3 resources, a 3-tier bench with ~15 recipes, hunger,
one unkillable stalker, raids every 4 nights, wolves by day, revives, 4 classes bought with a
soft currency, saving, a settings menu (brightness, volume).

| Week | Build |
|---|---|
| 1 | Lobby pads → `TeleportAsync` with `ShouldReserveServer`; server clock attributes; client lighting tween |
| 2 | Resource nodes (tagged, server HP), sack inventory, deposit prompts, node respawn |
| 3 | Camp levels, fuel drain, safe-zone radius, map gate (fog or invisible wall per level) |
| 4 | Bench tiers, grid placement with server checks, beds/defenses |
| 5 | Stalker (pathfinding, flashlight stun), wolves, raids; downs and revives |
| 6 | Run end, rewards at milestones, currency, 4 classes with leveling ([player-data](../patterns/player-data.md)) |
| 7 | Phone test on low-end Android, streaming, part-count pass, onboarding, metadata |
| 8–9 | One random event per run, badges, daily quests, a currency pack and a decor pass |

- **No artist:** low-poly built-in parts for trees and rocks, one emissive fire, color-coded
  resources; the stalker as a tall silhouette with glowing eyes (inferred). 99 Nights had an
  extra artist and an animator (official DevForum spotlight), so budget your look accordingly.
- **Cut:** extra biomes, 99 days, fishing, cooking recipes, NPC traders, trading, decorating
  furniture, Hard Mode, physics carrying, client-side hit prediction (inferred).

## Top examples

- 99 Nights in the Forest (case study: 99-nights-in-the-forest): campfire-centered co-op
  run with classes; 122.7K (data, 2026-10-22).
- 100 Days at Sea: same loop on a raft at sea, harpoon gathering, islands; 10.4K, 97% likes,
  created 2025-11-14 (data, 2026-10-22).
- Survive a Million Monkeys: class picks and horde waves, guns and a leaderboard; 11.9K (data).
- A Long Flight: repair-a-plane survival in a desert, early access; 2.6K (data).
- DOORS (case study: doors): co-op runs without a base, for threat design.

## Build checklist for agents

### Do
- Put safe zone, healing, cooking and map gating on one camp object whose level everyone sees.
- Keep night ≤ half the day (e.g. 90 s vs 180 s); warn 15 s before dusk; make night 1 safe.
- Run the clock on the server (`Phase`, `DayNumber`, `PhaseEndsAt` attributes); tween
  `Lighting.ClockTime` on clients.
- Scale fuel and raid size by party size; let a solo player finish a run.
- Validate every gather, deposit, craft and placement on the server (distance, cooldown,
  ownership, inside camp radius).
- Give the stalker a counter (light) and a safe zone; make raiders killable.
- Level classes by doing the role; give each a perk that helps the party.
- Save meta rewards when earned (milestone days, dungeon), not only on leave.
- Use reserved servers for runs and a lobby place for parties.
- Test the night on a phone at low graphics; ship a brightness slider.

### Don't
- Don't make v1 runs longer than ~60 min without a save or a short mode.
- Don't carry resources as client-owned physics parts in v1.
- Don't let the client decide damage, hits, node HP or camp fuel.
- Don't sell night skips, invincibility, or classes only for Robux.
- Don't sell rerolls with Robux-bought currency without odds and `PolicyService` checks.
- Don't reuse 99 Nights names, its deer mascot, cultists, "Nights in the Forest" title pattern
  or thumbnails.
- Don't fill the map with high-part trees; keep the run under phone memory limits.

## Sources

1. private/trends/latest.md, `trends lookup` and the tracker DB — genre, theme and per-game numbers, server sizes, descriptions (data, 2026-10-22)
2. https://devforum.roblox.com/t/creator-spotlight-the-story-behind-99-nights-in-the-forest/4036940 — team, jam-to-3-month build, 14M peak, tone choice, client prediction, mobile part budgets, Update Party (official, 2025-10-31)
3. https://99-nights-in-the-forest.fandom.com/wiki/Days — 180 s day / 90 s night, day multiplier up to 9×, fixed-day timeline, milestone diamonds (community wiki, read via API 2026-10-24)
4. https://99-nights-in-the-forest.fandom.com/wiki/Campfire — fire levels 1–6, safe zone and map growth, fuel drain, party-size scaling, burn-out penalties
5. https://99-nights-in-the-forest.fandom.com/wiki/The_Deer — unkillable stalker, flashlight stun, speed ramp
6. https://99-nights-in-the-forest.fandom.com/wiki/Classes — class roster, prices, level tasks, Robux skips, class counts as of 2026-09-03
7. https://99-nights-in-the-forest.fandom.com/wiki/Diamonds — diamond sources and Robux packs
8. https://99-nights-in-the-forest.fandom.com/wiki/Update_Log — biweekly updates, 2026 events
9. https://99-nights-in-the-forest.fandom.com/wiki/Hard_Mode — Hard Mode added 2026-01
10. https://en.wikipedia.org/wiki/List_of_Roblox_games — 99 Nights gameplay summary, key from wolf/bear kills
11. https://studiokrew.com/blog/top-roblox-games-august-2026/ — 99 Nights 152.1K on 2026-08-20, 269.6K weekly average (third-party, unverified)
12. https://apis.roblox.com/game-passes/v1/universes/7326934954/game-passes — Decorator Pass 199, off-sale class passes (read 2026-10-24)
13. https://create.roblox.com/docs/reference/engine/classes/Lighting — ClockTime not replicated, Get/SetMinutesAfterMidnight
14. https://create.roblox.com/docs/reference/engine/classes/TeleportService — ReserveServerAsync, TeleportAsync; ReserveServer deprecated

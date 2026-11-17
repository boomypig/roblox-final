---
title: Pet and egg collection
type: genre
read-when: Building pet collection, eggs, or hatching as the main loop (team power, variants, index, trading, event pets).
last-researched: 2026-10-22
---

# Pet and egg collection

## In one line

Earn currency, spend it on eggs, hatch random pets whose stats boost how fast you earn, and
chase the rarest tier, variant and index entry. The pets are the progression, the trophy
and (once trading exists) the economy.

Mechanics live in patterns; this file is about the genre:
[rarity-tiers-and-eggs](../patterns/rarity-tiers-and-eggs.md) (odds, pity, luck, hatch
reveal, disclosure), [pets-companions](../patterns/pets-companions.md) (following, slots,
fusing, storage, visuals), [trading](../patterns/trading.md), [inventory](../patterns/inventory.md),
[rebirth-prestige](../patterns/rebirth-prestige.md), [upgrade-trees](../patterns/upgrade-trees.md).
The clicker/stat loop that usually feeds it is [simulator.md](simulator.md).

## Core loop

- **Moment-to-moment (2–5 s):** walk to an egg, press hatch, watch a 1–3 s reveal, see the
  pet and its tier color, equip it or auto-delete it.
- **Session (15–45 min):** earn currency (breakables, clicks, minigames) → hatch the zone's
  egg until a better pet drops → "Equip Best" → higher team power earns faster → unlock the
  next zone and its stronger egg → check the index and event egg.
- **Long-term (weeks):** finish index pages, collect variants (golden, rainbow, shiny,
  mythic), chase the size or secret tier (PS99 Huge/Titanic, BGSI Secrets), trade for missing
  pets, collect each event's limited pets.

The engine: each new zone's common pet should beat the last zone's best, so hatching never
stops being useful (inferred; see the 2–3x tier step in
[pets-companions](../patterns/pets-companions.md)).

## Main verbs

Hatch, equip (best), fuse/craft, upgrade variant, index, lock/delete, trade, show off.
Hatching alone is a slot machine; the other verbs give hatches a use (inferred).

## Why players come back

- **A chase that is visible and possible.** PS99 announces only Exotic and above
  (community, BIG Games API 2026-10-22). Rare hatches are public events, so others see them too.
- **Guaranteed routes beside the lottery.** Bubble Gum Simulator INFINITY (BGSI) reportedly
  gives a Shiny every 75th hatch with a mastery upgrade, and some Secret pets for milestones
  such as 10M eggs hatched (press, Sportskeeda 2025; unverified). Pity counters do the same
  ([rarity-tiers-and-eggs](../patterns/rarity-tiers-and-eggs.md#pity)).
- **Index rewards.** PS99 unlocks index rewards at its third rebirth (community, API
  2026-10-24). A page at 9/10 pets is a reason to return (inferred).
- **Events with limited pets** on a fixed cadence. PS99 updates on Saturdays at 17:00 GMT,
  when ready (press, Ginx 2025).
- **The market.** Once trading exists, prices move every day, and checking them is itself a
  session (inferred).

## What separates top games from clones

1. **Pets do visible work.** PS99 pets break coins and chests; Bee Swarm's bees gather pollen;
   Adopt Me pets grow through care tasks (community/press). In clones, pets are a multiplier
   number floating behind the player (inferred).
2. **Variants multiply the collection without new models.** PS99 eggs roll golden, shiny and
   rainbow chances separately from the pet roll (community, API 2026-10-22). BGSI reports
   Shiny at about 2.5% per hatch or crafted from 8–16 duplicates, and Mythic at 1% on
   Legendary+ for 1.75x stats (press, Sportskeeda 2025; unverified). For a solo dev with no
   artist this is the cheapest content there is (inferred).
3. **Duplicates have a use.** Fusing and crafting delete copies: Adopt Me needs 4 full-grown
   pets for a Neon and 4 Neons for a Mega Neon (press/wiki, 2026). That is a sink that props
   up trade values (inferred).
4. **Trading tools, not just a trade window.** PS99 gates its Trading Plaza behind the first
   rebirth and shows RAP, the average of the last 150 sales (community API 2026-10-24; press,
   Pocket Tactics 2025-05). Adopt Me requires a Trade License (a scam-spotting test) for pets
   above Rare, shows 30 days of trade history, and caps a trade window at 18 items (press,
   Wikipedia on 2020-11; community wiki).
5. **Scale and cadence that a solo dev can't match.** PS99 has 4 worlds (each a separate
   place), 279 zones, 951 egg configs and 3,277 pet configs (community, API 2026-10-24).
   Compete on a new verb or theme, not on content volume (inferred).

## Session shape

Targets are (inferred) from the loop and the odds worked example in
[rarity-tiers-and-eggs](../patterns/rarity-tiers-and-eggs.md#worked-example-a-launch-egg).

- **First 60 seconds:** a free starter pet or free first egg, the first hatch reveal within
  60 s, the pet visibly following and boosting the first earning action.
- **First 10 minutes:** 10–30 hatches, first Rare, a team of 3, the index panel opened once
  (prompt it), zone 2 egg visible with its price.
- **Session:** 15–45 minutes, ending on a zone unlock, rebirth or index page.
- **Day 7:** first Legendary, an index page done, the chase tier seen in someone else's
  announcement, trading unlocked if the game has it.

## Social hooks

- **Hatch announcements:** server chat for Epic+, cross-server for the chase tier (see
  [simulator.md](simulator.md#social-hooks) for APIs).
- **Pets as status:** big, glowing or rare pets following the player are the avatar flex
  of this genre (inferred). Size by tier is in
  [pets-companions](../patterns/pets-companions.md#visuals-without-an-artist).
- **Clans/teams:** PS99 unlocks clans at its second rebirth and has run clan battles since
  2023-12-16 (54 battles configured as of 2026-10-24; community, API).
- **Trading and gifting:** the strongest social glue in the genre and the biggest risk
  (see "Ethics" below and [trading](../patterns/trading.md)).
- **Co-op events:** a server-wide egg or boss everyone hatches from or fights (inferred).

## Monetization that works here

- **Passes:** more equipped pets, bigger storage, triple/octuple hatch, auto-hatch, luck.
  PS99 lists Lucky at 275 Robux, Huge Hunter at 3,250, and Super Drops and Double Stars at
  2,400 each (press, Screenwise 2026).
- **Robux eggs:** PS99 sells Exclusive egg bundles from 240 Robux for 2 eggs to 14,500 for
  169 (press, Screenwise 2026). Their odds put a Huge at 1.5% and 0.5% (community, API
  2026-10-22). A solo dev should skip Robux eggs at launch (see Checklist).
- **Boosts:** timed luck or hatch-speed potions sold as developer products (paid probability
  modifiers when bought with Robux; official).
- **Event passes** that add hatch speed or exclusive cosmetics for the event's length.
- **Scope trap:** an egg priced in any currency the player can buy with Robux is a paid
  random item (official). Default: eggs cost earn-only currency; Robux buys passes, boosts and
  direct-purchase items (inferred; same rule in the egg pattern).
- Purchase handling and pricing: [monetization](../fundamentals/monetization.md).

## Paid random items: rules and ethics for kids

Full policy: [monetization](../fundamentals/monetization.md#paid-random-items-eggs-crates-spins-luck-boosts-pity).
Genre-specific points:

- **Covered:** eggs, chests, wheels; luck boosts and pity; and combination items such as
  fusing that can fail or roll a random result, when any input is bought with Robux or
  Robux-bought currency (official, 2026-10).
- **Before purchase:** every outcome's odds as percentages summing to 100%, behind "Info" or
  "Details" if long; boosted odds shown live; once-only outcomes update the remaining odds
  (official).
- **Restricted players:** `PolicyService:GetPolicyInfoForPlayerAsync` →
  `ArePaidRandomItemsRestricted` (earnable path, fixed order, direct purchase at expected
  value, hide, block or exclude) and `IsPaidItemTradingAllowed` (no trading of paid items)
  (official). Under-18s in Brazil can't access paid random items (official, help center 2026).
- **Every outcome must benefit the player**; gambling, real or simulated, is banned
  (official, Community Standards).
- **What regulators and researchers flag:** a 2026 study of 15 popular Roblox games found
  misleading purchases in 14, including loot boxes, near-miss visuals, prompts after losses,
  false urgency and fake discounts (press, University of Sydney 2026-05-17).
- **Tradeable rare items get a real-money price.** Huge pets are listed for cash on eBay
  (observed in search results, 2026; unverified scale). Third-party gambling sites using
  Robux were the subject of a 2023 class action against Roblox (press, TechCrunch
  2023-08-18). Anything tradeable and scarce will attract both (inferred).
- **Trading scams hit young players:** parent guides describe outdated value lists,
  pressure, and last-second offer swaps in PS99's Trading Plaza (press, Screenwise 2026).

Reviewer rules (inferred unless tagged): every pet tier, including the chase tier, is
reachable without Robux; no Robux-only pet decides PvP or stealing outcomes; no near-miss
reveals; no purchase prompt right after a hatch; event pets are labelled with their real end
date and never "return" after a "last chance" (official honest-presentation rule).

## Common failure modes

- **Inflation of the chase tier.** PS99 has about 56M copies of normal Huge pets across 1,082
  species; its five most common Huges exist 1.0M–1.6M times each, while the rarest exist once
  (community, API `exists` 2026-10-24). The median normal Huge's RAP is about 58.5M diamonds
  and the median Titanic's about 6.8B (community, API `rap` 2026-10-24). When an event mints a
  million of a "rare" tier, the tier stops meaning rare, so the game needs a new tier above it
  (inferred: PS99 added Titanic and Gargantuan tiers, 370 and 83 pet configs).
- **No sinks.** Pets only enter the economy, storage bloats and trade values fall (inferred).
- **Duplication bugs.** One dupe in a trading game corrupts every price; trading needs
  atomic swaps and session locks first ([trading](../patterns/trading.md),
  [player-data](../patterns/player-data.md)).
- **Pets are cosmetic.** If team power doesn't change earning speed in a way the player can
  feel, hatching has no point beyond collecting (inferred).
- **Unskippable reveals.** A 5 s animation is fun 10 times and torture at 500 (inferred; see
  hatch pacing in the egg pattern).
- **Policy misses.** No odds UI, odds that don't sum to 100%, or paid eggs shown to restricted
  players. In Brazil, an undeclared or ungated paid-random game becomes unplayable for minors
  (official).
- **Storage full silently eats a paid hatch** (inferred; stop before charging).

## Saturation & opportunity

All numbers are one tracker snapshot, so they show size, not growth (data, 2026-10-22).

- **`pet` name theme: one game dominates.** 7 charted games, 252K players; Adopt Me! holds 72%.
  Median 8.8K (data).
- **`egg` name theme: one game dominates.** 8 games, 1.03M players; Steal An Egg (877K) holds
  85%. Its clone wave has 7 rising games created 2026-07-25 → 2026-10-04 and is still being
  joined (data).
- **The rising egg games are hybrids, not hatch sims:** Steal An Egg, Break and Steal an Egg,
  Fake an Egg and Climb For Animals Eggs (26.5K players, created 2026-09-06) all sit in Roblox's
  Tycoon subgenre (data). Eggs are the reward layer on a new verb (inferred).
- **Pet Simulator 99** had 38.0K players and ranked top-earning #11 (data). It is an incumbent
  with a three-year head start; see case study: pet-simulator-99.
- **Opportunity (inferred):** use eggs and pets as the collection layer of a game with a fresh
  verb (climb, steal, break, fish), or a pet game with a different relationship to pets (care,
  battling, breeding), not a straight PS99-style hatch sim. Read
  [trend-lifecycle](../fundamentals/trend-lifecycle.md) before joining the egg wave, and
  [steal-a-x](steal-a-x.md) if the hybrid involves stealing.

## Scope for a solo dev

Week counts are (inferred) for one developer with Rojo and Studio MCP playtests.

**MVP:** one earning action, 3 zones with one egg each (6 pets + 1 chase pet per egg, 5 tiers),
golden variant by deterministic fuse, index with page rewards, 3→6 team slots, Equip Best,
single + triple hatch, skippable reveal, odds billboards, earn-only egg currency, saving,
2 passes. No trading at launch.

| Week | Build |
|---|---|
| 1 | Session-locked data with pet inventory records ([inventory](../patterns/inventory.md)); earning action; HUD |
| 2 | Egg roll on the server with integer weights; odds billboard; hatch reveal; storage cap |
| 3 | Equip/Equip Best, client-rendered followers, team power → earnings; zones 2–3 |
| 4 | Fuse to golden, index and rewards, passes with `ProcessReceipt`, analytics events |
| 5 | Rare-hatch announcements, first limited event egg, mobile pass, launch |
| Later | Trading (only after 2+ weeks of clean saves and no dupes), rainbow tier, clans |

**Cut from v1:** trading, Robux eggs, enchants, multiple worlds, clans, pet levels, more than
18–21 pets per zone set. Pets from simple shapes or generated meshes; never copied designs.

## Top examples

- Pet Simulator 99 (case study: pet-simulator-99): the reference hatch-and-trade game
  at scale, and its controversies.
- Adopt Me! (case study: adopt-me): pets as care-and-trade, Neon fusing, trade licenses.
- Bubble Gum Simulator INFINITY (no case study): variant layers, milestone guarantees and weekly
  updates (press, 2025); 10.4K players, 97% likes (data, 2026-10-22).
- Steal An Egg (case study: steal-an-egg): eggs as the prize in a stealing game.

## Build checklist for agents

### Do

- Roll every hatch on the server with integer weights; display the normalized percentages,
  summing to 100%, on the egg before the player pays.
- Price the zone's basic egg at 1–5 minutes of that zone's expected income and its best egg at
  10–15 minutes (inferred; same targets as [simulator.md](simulator.md)).
- Make each zone's Common pet at least as strong as the previous zone's Legendary (inferred).
- Start with 3 equip slots; reach 6 by play; sell +1 to +3 by pass (inferred; matches the pets
  pattern).
- Fuse: 4–6 identical pets → golden, 4–6 golden → rainbow, 100% success, result shown before
  confirm (inferred; Adopt Me uses 4, BGSI reportedly 8–16).
- Index: a reward every 5–10 entries and a big one per completed page (inferred).
- Reveal ≤ 2.5 s for a single hatch, skippable after the first; multi-hatch reveals together.
- Add pity for any tier rarer than 1% in an egg players buy repeatedly; show the counter.
- Give every limited event pet a stated end date, and announce in advance whether it will
  ever return.
- Gate paid randomness and trading with `PolicyService`; treat a failed call as restricted.
- Before trading ships: atomic swaps, both-sides confirm with a short delay after any change,
  item lock, trade log, and a trade unlock requirement (rebirth, level or playtime).

### Don't

- Don't price eggs in a Robux-buyable currency without the full paid-random-items treatment.
- Don't sell Robux eggs or Robux-only chase pets at launch.
- Don't mint an "event Huge" with uncapped supply and still call it rare.
- Don't show near-miss reveals, prompt a purchase after a hatch, or run "last chance" eggs
  that come back.
- Don't let the client choose the egg result, the pets to fuse that it doesn't own, or the
  team it claims to have equipped.
- Don't copy PS99, Adopt Me or BGSI pet designs, names, tier names or UI art.

## Sources

1. https://www.roblox.com/games/8737899170 — Pet Simulator 99 (tracker snapshot 2026-10-22 in private/trends/latest.md)
2. https://www.roblox.com/games/107778070777162 — Steal An Egg (tracker snapshot 2026-10-22)
3. https://www.roblox.com/games/85738654635245 — Climb For Animals Eggs (tracker snapshot 2026-10-22)
4. https://www.roblox.com/games/85896571713843 — Bubble Gum Simulator INFINITY (tracker snapshot 2026-10-22)
5. https://ps99.biggamesapi.io/api/collection/Rebirths — PS99 rebirth unlocks: Trading Plaza, clans, index rewards (read 2026-10-24)
6. https://ps99.biggamesapi.io/api/exists — PS99 copies in existence per pet (read 2026-10-24)
7. https://ps99.biggamesapi.io/api/rap — PS99 recent average prices (read 2026-10-24)
8. https://ps99.biggamesapi.io/api/collection/Eggs — PS99 egg odds and variant chances (read 2026-10-22, via rarity pattern)
9. https://ps99.biggamesapi.io/api/collection/GuildBattles — PS99 clan battles since 2023-12-16 (read 2026-10-24)
10. https://www.pockettactics.com/pet-simulator-99/values — RAP = average of last 150 sales (2025-05-16)
11. https://www.ginx.tv/en/?p=58102 — PS99 Saturday 17:00 GMT update schedule (2025)
12. https://www.sportskeeda.com/roblox-news/how-get-first-secret-pet-bubble-gum-simulator-infinity — BGSI milestone-guaranteed Secrets (2025)
13. https://www.sportskeeda.com/roblox-news/how-get-mythic-dementor-bubble-gum-simulator-infinity — BGSI Mythic 1.75x stats (2025)
14. https://en.wikipedia.org/wiki/Adopt_Me! — Adopt Me trade licenses introduced 2020-11
15. https://adoptme.fandom.com/wiki/Trade_License — license test, 30-day history, scam reporting
16. https://screenwiseapp.com/media/pet-simulator-99-game — PS99 pass and Exclusive egg prices, Trading Plaza risks (2026)
17. https://create.roblox.com/docs/production/monetization/paid-random-items — scope incl. combination items, disclosure, restricted treatments
18. https://create.roblox.com/docs/reference/engine/classes/PolicyService — ArePaidRandomItemsRestricted, IsPaidItemTradingAllowed
19. https://about.roblox.com/community-standards — gambling ban, off-platform sales
20. https://en.help.roblox.com/hc/cs/articles/48706630819476-Brazil-Digital-ECA-Updates — Brazil under-18 paid random item block
21. https://www.sydney.edu.au/news-opinion/news/2026/05/17/inside-the-pay-to-play-world-of-roblox-targeting-children-.html — 14 of 15 games with misleading purchases
22. https://techcrunch.com/2023/08/18/roblox-children-gambling-class-action-lawsuit-robux/ — 2023 class action over Robux gambling sites
23. https://www.ebay.com/itm/296770771569 — example real-money listing of Roblox pet-game items (observed 2026)

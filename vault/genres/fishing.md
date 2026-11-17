---
title: Fishing
type: genre
read-when: Building a fishing game (Fisch / Fish It!-likes): casting, catch minigame, bestiary, rods, bait, zones, rarity.
last-researched: 2026-10-22
---

# Fishing

## In one line

Cast, wait for a bite, win a short catch minigame, and pull a random fish from a weighted table
shaped by your rod, bait, zone, weather and time of day; sell it, log it in a bestiary, and buy a
better rod to reach rarer fish in new zones. Two games hold the genre: Fish It! and Fisch, both
in the top 25 (data, 2026-10-22).

## Core loop

- **Moment to moment (10–20 s per fish):** charge and release a cast → wait for a bite (shake
  prompts can shorten it) → catch minigame → reveal fish, rarity, weight (community, Fisch wiki).
- **Session (15–30 min):** fill the backpack, sell at a merchant, buy bait or a rod upgrade,
  try a new spot or chase a weather/time window (inferred; Fish It!'s average session is
  reported at ~30 min, community 2025-12).
- **Meta (weeks):** rod ladder, new zones/islands, bestiary completion, ultra-rare "secret"
  fish, events (community, Fisch wiki; press-style blogs on Fish It!).

## Main verbs

Cast · wait/shake · reel · reveal · sell · log (bestiary) · upgrade rod · equip bait · travel ·
(enchant, appraise, trade in deeper games).

## Two reference designs

| | Fisch | Fish It! |
|---|---|---|
| Public launch | 2024-10-05 (created 2024-03-13) (community, Fisch wiki) | created 2024-10-21; broke out 2025-08 → 2025-12 (data; community) |
| Peak (Rolimons) | 1,273,618 on 2025-10-18 (community tracker) | 2,716,766 on 2025-12-07 (community tracker) |
| Now | 62,107 playing, 91% likes, 3.70M favorites (data, 2026-10-22) | 70,068 playing, 83% likes, 1.29M favorites (data, 2026-10-22) |
| Earning chart | top-earning #7 (data, 2026-10-22) | top-earning #73 (data, 2026-10-22) |
| Catch minigame | Hold to push a bar right, release to drift left; keep the fish inside it; progress +12%/s inside, −12%/s outside; input locked first 1.2 s; min ~8 s per reel at base stats (community, Fisch wiki) | Hold to charge cast with a luck meter ("perfect" boosts rare odds), then click rapidly to reel; near-impossible to fail (community guides, 2025) |
| Rarity display | Named tiers (Trash → Common → … → Mythical → Exotic → Secret, plus many event tiers); weight matters | "1 in X" odds on every fish, e.g. secret fish 1 in 750K–5M (community guides, unverified) |
| Automation | Manual | Built-in auto-fish unlocked by leveling (community, 2025) |
| Map | Islands across an ocean; boat needed to leave the start island (community, Fisch wiki) | Guided islands with labeled points of interest and quest prompts (community, 2025-12) |

Case study: fisch.

## Why players come back

- **Rarity chase with known odds.** Seeing "1 in 4,000,000" next to an empty bestiary slot is a
  long-term goal you can read at a glance (inferred from Fish It!'s display).
- **Bestiary slots.** Fisch's bestiary is a logbook of discovered fish and a secondary goal
  (community, Fisch wiki). Empty slots are hook #5 in
  [retention](../fundamentals/retention.md).
- **Time and weather windows.** Fisch's day lasts ~25–30 min; weather rolls per day/night;
  fish caught at the wrong time get −75% chance, preferred weather +35%, preferred season +20%,
  preferred bait +10% (community, Fisch wiki). "This fish only bites at night in rain" sends
  players back at specific times.
- **Rod ladder.** Each rod adds Luck, Control, Resilience or Lure Speed, and a rod's max weight
  limits which fish it can land at all (community, Fisch wiki). The next rod is always visible.
- **Events and admin luck.** Event weathers multiply luck (Fisch lists x7–x8 weathers and
  admin events from x2 upward) (community, Fisch wiki). See
  [server events](../patterns/server-events-admin-abuse.md).

## What separates top games from clones

1. **Clear, fast first catch.** Fish It! reached twice Fisch's peak with a near-automatic catch,
   auto-equipped gear and constant quest guidance (community, Max Power Gaming 2025-12-08;
   Rolimons).
2. **Readable odds.** "1 in X" beats tier names alone for kids (community, 2025-12; inferred).
3. **A skill layer for those who want it.** Fisch's bar minigame rewards a "perfect" catch
   (+10 coins, +50% XP) (community, Fisch wiki) and kept the higher like rating (91% vs 83%,
   data 2026-10-22). Offer both: forgiving default, optional skill bonus (inferred).
4. **Many modifiers on one roll.** Rod, bait, enchant, potion, weather, time, season, zone and
   event all feed the same weighted table (community, Fisch wiki). Each is a new thing to buy,
   craft or wait for, without new core code (inferred).
5. **Weekly updates with an event label.** Both games carried an event tag in their name on
   2026-10-22 (Fisch "FISCHFRIGHT", Fish It! "🎃UPD") (data).

## Session shape

- **Typical session:** ~30 min for Fish It!, helped by auto-fish (community, 2025-12).
- **First 60 seconds:** rod in hand on spawn, a dock 10 studs away, one tap-and-hold prompt,
  first fish within 20 s, rarity reveal, "sell" arrow (inferred).
- **First 10 minutes:** ~20–30 fish, first sale, first rod upgrade, first uncommon/rare reveal
  with a sound and color, bestiary opened once, second spot or zone unlocked (inferred).
- **Day 7:** third zone, bait choice matters, first legendary-tier fish, a night-only or
  weather-only fish targeted on purpose, auto-fish if offered (inferred).

## Social hooks

- **Shared spots:** 20-player servers in both leaders (data, 2026-10-22) put anglers side by
  side; rare catches announced to the server create "what did you catch?" moments (inferred).
- **Server-wide luck events** and admin events reward being online together (community, Fisch
  wiki).
- **Show-off:** hold up or display a rare catch; leaderboards for heaviest fish (inferred).
- **Trading** only after safe trades exist ([trading](../patterns/trading.md)). Fish It! has
  reports of bot accounts farming items for resale (community, 2025-12, unverified).

## Monetization that works here

- **Luck is the product.** Fisch sells server luck for Robux and had a 4x luck pass that drew
  "cash grab" complaints (community, Fisch wiki; Roonby 2026-02).
- **Rods and luck items are probability modifiers.** Roblox's paid-random-items rules cover
  "luck potions, special rods": state the numeric effect before purchase and update displayed
  odds while active. If a fish is bought or rolled with Robux, show % odds summing to 100%
  (official, 2026-10). Gate with `PolicyService:GetPolicyInfoForPlayerAsync()` →
  `ArePaidRandomItemsRestricted` (official, 2026-10). See
  [monetization](../fundamentals/monetization.md).
- **What we build (inferred):** cosmetic rods/boats/bobber trails, a bigger backpack, auto-sell,
  a fast-travel pass, a 2x XP pass, a timed personal luck potion with its exact multiplier shown,
  a private server.
- **What backfired:** Fisch's limited items had stock raised after selling out, which angered
  players; the player base fell and recovered only after the original developer took the game
  back and removed some monetization (community, Fisch wiki; Roonby 2026-02).

## Common failure modes

- **Minigame too hard on mobile.** A precise bar fails on touch; Fish It!'s forgiving reel
  widened the audience (community, 2025-12). Default to forgiving; test on a phone.
- **Long dead waits.** Bites over ~10 s with nothing to do. Use shake/tap prompts that shorten
  the wait (Fisch: 0.5–1.5 s per shake) (community, Fisch wiki).
- **Opaque luck.** "Luck +50%" with no visible effect. Show the odds change in the UI.
- **Client-decided catches.** If the client reports which fish it caught, exploiters print
  secret fish. The server rolls the fish (inferred; see
  [security](../../.claude/skills/roblox-code/references/security.md)).
- **AFK farming and bots.** Auto-fish invites multi-account farms and RMT (community,
  2025-12). Cap auto-fish yield, trade-lock fresh catches, log catches per hour (inferred).
  Roblox still kicks players idle for 20+ min ([retention](../fundamentals/retention.md)).
- **Monetization pivots after a sale.** See Fisch above.
- **Copying fish, NPC or island names** from either leader (see the case study).

## Saturation & opportunity

From the tracker (data, 2026-10-22, single snapshot, so no growth claims):

| Theme | Games | Players | Per game | Median | Leader share | In top 100 | Rising | Label |
|---|---|---|---|---|---|---|---|---|
| fish | 8 | 155K | 19K | 6.2K | Fish It! 45% | 2 | 1 | mixed |

| Game | Players | Created | Notes |
|---|---|---|---|
| Fish It! | 70K | 2024-10-21 | Simulation / Incremental Simulator |
| Fisch | 62K | 2024-03-13 | trending-in-simulation #1, top-earning #7 |
| Deep Fishing | 9.4K | 2026-07-18 | 97% likes, top-trending #55 |
| Heavyweight Fishing | 7.1K | 2025-08-04 | top-revisited #28 |
| Harpoon a Fish | 5.2K | 2026-08-28 | Up-and-Coming #55, "verb-a-noun" title |
| Be Fish | 551 | 2024-12-18 | |
| Cage Fishing | 99 | 2025-05-02 | |
| Titan Fishing | 34 | 2026-01-25 | |

- The theme median (6.2K) is about 4x the median charted game (1,544) (data, 2026-10-22): few
  games, each fairly large. No game holds 60%.
- Three newer games (Deep Fishing, Heavyweight Fishing, Harpoon a Fish) hold 5–9K each beside
  the two leaders (data, 2026-10-22). Room exists for a fishing game with a distinct twist
  (inferred).
- Twists visible in the data (names only, mechanics not researched): heavy-weight catches,
  depth/diving, harpoons (data). Other spins (inferred): co-op boat crews, fishing + base
  building, fishing + steal-a-x, a horror night-fishing mode.
- Fisch out-earns Fish It! on the earning chart with fewer players (data, 2026-10-22): depth
  monetizes better than breadth here (inferred).

## Scope for a solo dev

**MVP, about 4–5 weeks (inferred):**

| Week | Build |
|---|---|
| 1 | Cast (hold/release meter), water check by raycast, bite timer, forgiving catch minigame, server-side fish roll, backpack, sell NPC, save |
| 2 | Weighted fish table per zone, 25–35 fish in 6 tiers, luck math, rarity reveal (color, sound, `TweenService:Create` pop), bestiary UI |
| 3 | 3 rods, 2 baits, 2 zones + boat or teleport, day/night via `Lighting.ClockTime`, 2 weathers, "preferred conditions" |
| 4 | Server announcements for rare catches, quests for the first 10 min, passes/products with odds UI, analytics, mobile pass |
| 5 | Polish, optional skill bonus ("perfect catch"), launch |

Post-launch: a new zone or event every 1–2 weeks; auto-fish as a progression unlock; enchants.

**Cut from v1:** trading, enchant system, fish mutations/appraisal, ocean-scale map with
boat physics (teleport between islands instead), 100+ fish, custom fish models (use a few base
meshes recolored and resized; the rarity color and name do the work) (inferred).

**Server-authoritative flow (inferred):**
1. Client: `RequestCast(power)` → server checks rod equipped, cooldown, and that a raycast with
   `RaycastParams.IgnoreWater = false` from the cast point hits water (`RaycastResult.Material
   == Enum.Material.Water`) or a tagged fishing zone.
2. Server picks bite time, then **rolls the fish** from the zone table with all modifiers and
   stores `{fishId, weight, biteAt, deadline}` for that player.
3. Client plays the minigame for that fish's difficulty and sends `RequestReel(success)`.
4. Server accepts only if `now - biteAt` is between the minimum possible reel time and the
   deadline, then grants. Draw the line with a `Beam` between rod tip and bobber `Attachment`s.

## Tuning starting points (inferred, tune with analytics)

| Tier | Share of catches at 0 luck | Shown as |
|---|---|---|
| Common | 60% | 1 in 2 |
| Uncommon | 25% | 1 in 4 |
| Rare | 10% | 1 in 10 |
| Epic | 4% | 1 in 25 |
| Legendary | 0.9% | 1 in ~111 |
| Mythic | 0.1% | 1 in 1,000 |
| Secret (per fish) | 0.0002–0.002% | 1 in 50K–500K |

- Luck: multiply the weights of Rare and above by `(1 + luck)`, then renormalize; never let luck
  raise Commons. Cap any single fish at, say, 5% so luck can't flatten the table (Fisch also
  caps per-fish chance, community, Fisch wiki).
- Timings: bite wait 2–8 s base; each shake/tap −0.5 to −1.5 s; reel 3–6 s for casual fish,
  6–10 s for top tiers; perfect-cast window 10–15% of the meter; input lock ≤ 1 s.
- Backpack 20–30 fish at start so a sale happens every ~5 min.

## Top examples

- Fisch (case study: fisch): deep systems, skill minigame, bestiary, weather/season,
  the ownership-and-monetization cautionary tale.
- Fish It!: simplified, guided, "1 in X" odds and auto-fish; overtook Fisch in late 2025 (see
  the case study's comparison).
- Deep Fishing, Heavyweight Fishing, Harpoon a Fish: smaller 2025–2026 entrants (data).

## Build checklist for agents

### Do
- Roll the fish on the server at bite time; the client only plays the minigame.
- Reject reel results faster than the minimum reel time or after the deadline; rate-limit casts.
- Show odds as both "1 in X" and %, and update them live when luck, bait, weather or time
  change.
- Explain every luck source numerically before purchase; gate Robux random rolls with
  `ArePaidRandomItemsRestricted`.
- Default to a forgiving catch (≥ 90% success for at-level fish) and add an optional perfect
  bonus.
- Give each tier a distinct color and sound; give Legendary+ a server-wide announcement.
- Fill the bestiary with silhouettes and hints ("bites at night", "needs bait X").
- Make the first catch happen within 20 s of spawning, on mobile.
- Tie 2–3 fish per zone to time/weather windows and show the current conditions on the HUD.
- Log catches per hour per player and per tier to tune odds and catch farms.

### Don't
- Don't trust a client-sent fish ID, weight or rarity.
- Don't show "+X% luck" without showing what it does to the odds.
- Don't require pixel-precise input to land at-level fish.
- Don't sell limited items and then raise the stock, or invent scarcity.
- Don't make bite waits longer than ~10 s without an input to shorten them.
- Don't copy Fisch or Fish It! fish names, NPCs, islands, rod names or UI.
- Don't launch trading or auto-fish before catch-rate logging and session-locked saves exist.

## Sources

1. https://fischipedia.org/wiki/Fisch — Fisch developer, dates, Today's Picks, top CCU 2024-11-30, bestiary, day length, weather
2. https://fischipedia.org/wiki/Fishing — cast, shake, reel minigame numbers and formulas
3. https://fischipedia.org/wiki/Luck — luck rules, modifiers, server luck, caps
4. https://fischipedia.org/wiki/Rarity — rarity tier list
5. https://www.rolimons.com/game/16732694052 — Fisch peak 1,273,618 (2025-10-18)
6. https://www.rolimons.com/game/121864768012064 — Fish It! peak 2,716,766 (2025-12-07)
7. https://www.maxpowergaming.co/post/fish-it-how-a-simplified-copycat-became-one-of-roblox-s-biggest-hits — Fish It! vs Fisch design, growth, auto-fish, bot doubts (2025-12-08)
8. https://games.gg/news/fish-it-unexpected-rise-to-the-top-of-roblox/ — Fish It! growth and design (2025-12-11)
9. https://www.sportskeeda.com/roblox-news/fish-it-a-beginner-s-guide — Fish It! cast meter, rapid-click reel, auto-fish unlock
10. https://allthings.how/fish-it-rod-tier-list-and-how-to-get-every-rod/ — Fish It! rod luck stats (guide)
11. https://roonby.com/2026/02/13/is-do-big-still-developing-fisch-here-are-the-facts-so-far/ — Fisch monetization backlash, handback
12. https://create.roblox.com/docs/production/monetization/paid-random-items — odds disclosure, luck items, PolicyService flags
13. https://create.roblox.com/docs/reference/engine/datatypes/RaycastParams — IgnoreWater
14. private/trends/latest.md and tools/trends lookups — players, charts, theme stats (data, 2026-10-22)

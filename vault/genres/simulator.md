---
title: Simulator (clicker / stat)
type: genre
read-when: Building a clicker/stat simulator (click → sell → upgrade → unlock zone → rebirth).
last-researched: 2026-10-22
---

# Simulator (clicker / stat)

## In one line

Repeat one cheap action to grow a number, spend the number to grow it faster, unlock a zone
where it grows faster still, then reset (rebirth) for a permanent multiplier. The whole game
is pacing: the reviewer should check the tuning table before anything else.

Related genres: pet collection as the main loop is [pet-egg-collection.md](pet-egg-collection.md);
pure offline/idle play is [idle-incremental.md](idle-incremental.md); "+1 stat per second" is
[plus-one-stat.md](plus-one-stat.md); droppers and build-out is [tycoon.md](tycoon.md).

## Core loop

- **Moment-to-moment (1–5 s):** click/tap/swing → stat or currency goes up with a number pop,
  sound and a small scale punch. In pet-farming variants the player points pets at breakables
  and the pets do the hitting.
- **Session (10–40 min):** fill the stat or backpack → sell (if the variant has a sell step) →
  buy an upgrade or an egg → reach the next zone gate → hatch better pets there → hit the
  rebirth threshold → rebirth and replay the early zones much faster.
- **Long-term (days–weeks):** higher rebirth tiers, world 2+, pet index completion, bosses and
  leaderboards, limited-time event eggs.

| Variant | The action | What gates the next zone | Example (data, 2026-10-22) |
|---|---|---|---|
| Tap/click | Tap anywhere or a button | Currency cost | Tap Simulator REBORN, 35.6K players |
| Stat/strength | Lift, punch, swing; stat beats NPCs or obstacles | Stat threshold or NPC win | Arm Wrestle Simulator, 2.4K players (1.32B visits) |
| Collect-and-sell | Gather into a capped bag, walk to a sell pad | Bag size + currency | Bee Swarm Simulator (pollen → honey), 28.6K players |
| Breakables + pets | Pets break coins/chests in an area | Currency cost per area | Pet Simulator 99, 38.0K players |

Mechanics live in patterns: [rebirth-prestige](../patterns/rebirth-prestige.md),
[upgrade-trees](../patterns/upgrade-trees.md), [idle-offline-income](../patterns/idle-offline-income.md),
[rarity-tiers-and-eggs](../patterns/rarity-tiers-and-eggs.md), [pets-companions](../patterns/pets-companions.md),
[inventory](../patterns/inventory.md). This file is about how they combine in the genre.

## Main verbs

Click/tap, collect, sell, upgrade, hatch, equip, unlock (zone), rebirth, fight (boss/NPC),
and later trade. A clone has only the first five; top games add a second verb that the
clicking feeds (pets that break things, bees that gather, a boss to beat) (inferred).

## Why players come back

- **Visible next goal.** The next zone gate, egg and rebirth always show a progress bar or
  "X more to unlock" (inferred).
- **Rebirth replays the early game at power-fantasy speed.** Zones that took 10 minutes take 1;
  the second cycle should be shorter than the first (inferred; see
  [rebirth-prestige](../patterns/rebirth-prestige.md)).
- **Random hatches and an index to complete** (see [pet-egg-collection](pet-egg-collection.md)).
- **Offline or AFK income** gives a reason to return to a fuller bank
  ([idle-offline-income](../patterns/idle-offline-income.md)).
- **Dated reasons:** daily rewards, weekly updates, event eggs, codes
  ([daily-rewards-and-streaks](../patterns/daily-rewards-and-streaks.md),
  [live-ops](../fundamentals/live-ops-and-updates.md), [codes](../patterns/codes.md)).

## What separates top games from clones

1. **A second system the click feeds.** Pet Simulator 99's pets break coins; Bee Swarm's bees
   gather pollen in fields; plain "click to get clicks" is the clone baseline (inferred).
   DevForum posters said as early as 2020 that plain grind-and-gacha sims were fading and that
   hits blend in another genre (community, 2020-05).
2. **A theme you can name in three words**, not "X Clicker Simulator." The `clicker` name
   theme is 6 charted games with 3.8K players in total and a 296-player median (data,
   2026-10-22). The young breakouts in Incremental Simulator lead with a verb or hook instead:
   Chop A Forest, +1 Venom Evolution, Anime Dice (data, 2026-10-22).
3. **Longevity through identity and depth.** Bee Swarm Simulator was created 2018-03-21, last
   updated 2026-08-22, and still had 28.6K players and a 96% like rate (data, 2026-10-22).
   Its hook is a hive of distinct bees and fields with quests, not bigger numbers (inferred).
4. **Update cadence.** Bubble Gum Simulator INFINITY was reported to update about weekly,
   near the weekend (press, Sportskeeda 2025-05). Tap Simulator REBORN, PS99 and Arm Wrestle
   Simulator were all updated within 3 days of the snapshot (data, 2026-10-22).
5. **Feel.** Number pops, hatch reveals, rebirth fanfare and a clean mobile HUD are the
   product; see [game-feel](../../.claude/skills/roblox-vfx/references/game-feel.md) and [ui-ux](../../.claude/skills/roblox-ui/references/ui-ux.md).
6. **Small servers.** Max players per server: Bee Swarm 6, Arm Wrestle 9, Tap Simulator
   REBORN 10, PS99 10, BGSI 12 (data, 2026-10-22). Other players are scenery and status, not
   competition for resources (inferred).

## Session shape

No official session-length data exists for the genre; these targets are (inferred) from the
loop timing above and [retention.md](../fundamentals/retention.md).

- **First 60 seconds:** clicking within 5 s of spawn (no menu first); first number pop in the
  first second; first upgrade affordable by about 30 s; the first egg visible and priced so it
  is affordable within about 3 minutes.
- **First 10 minutes:** 3–5 upgrades bought, first pets hatched and equipped, zone 2 reached at
  about 8–12 minutes, the rebirth requirement shown on screen.
- **Session:** 15–40 minutes, ending on a rebirth or a zone unlock.
- **Day 7:** 5–20 rebirths, world 2 or the last zones of world 1, a team of rare/epic pets,
  chasing the index or a leaderboard spot.

## Social hooks

- **Rare-hatch announcements** to the server (chat system message via
  `TextChannel:DisplaySystemMessage`) and, for the rarest tiers, to all servers via
  `MessagingService:PublishAsync`. Batch them; MessagingService is rate-limited (official API).
- **Status on the avatar:** overhead rebirth count, equipped rare pets following the player.
- **Shared server moments:** a server-wide boss or event where every hit counts; a server luck
  boost one player buys for everyone (seen in RNG and pet games; unverified as a sales driver).
- **Leaderboards** for total stat and rebirths ([leaderboards](../patterns/leaderboards.md)).
- **Trading** only once the economy is stable ([trading](../patterns/trading.md)); it needs
  duplication-proof saves first.
- See [social-and-virality](../fundamentals/social-and-virality.md).

## Monetization that works here

The genre sells time and capacity well (see [monetization](../fundamentals/monetization.md)).

- **Auto-click / auto-farm pass.** Clicker Simulator sold a permanent Auto Click pass at 399
  Robux and timed boosts at 38–299 Robux (press, ~2022, unverified). PS99 lists Auto Farm at
  175 Robux (press, Screenwise 2026).
- **Multipliers:** 2x currency, 2x clicks, x2 rebirth rewards (Clicker Simulator sold one at
  349 Robux; press, ~2022, unverified).
- **Capacity:** more equipped pets, bigger backpack, sell-anywhere, teleport between zones.
- **Hatching speed and luck:** triple hatch, auto hatch, lucky pass (PS99 Lucky: 275 Robux;
  press, Screenwise 2026). Luck boosts are paid random items under Roblox rules (official).
- **Developer products:** 15–30 minute boosts, currency packs, exclusive eggs. Paid eggs need
  odds disclosure and `PolicyService` gating; see [pet-egg-collection](pet-egg-collection.md).
- **Don't sell zone access.** A zone you can only enter by paying splits the player base and
  reads as pay-to-progress (inferred).
- Fetch every displayed price with `MarketplaceService:GetProductInfoAsync` (official).

## Common failure modes

- **The wall at minute 20.** Costs grow exponentially but income grows linearly and rebirth is
  out of reach, so players stall and quit (inferred; idle-game math shows costs must be
  balanced against production; press, Game Developer 2016).
- **Number precision.** Luau numbers are 64-bit doubles: about 15 significant digits, max
  about 1.7e308 (official). `IntValue` is a 64-bit integer and caps near 9.2e18 (official).
  Past 1e15, small additions vanish; past 1e308 the value becomes `inf` and saves break.
- **Raw scientific notation in the HUD** (`1.2e+15`) instead of suffixes (K, M, B, T, Qa…).
- **Client-trusted clicks or sells.** An exploiter fires the click remote thousands of times a
  second, or sends a sell amount. See [security](../../.claude/skills/roblox-code/references/security.md).
- **Rebirth that feels like loss.** Wiping pets or passes on rebirth, or not showing the gain
  before the confirm button (inferred).
- **Non-atomic rebirth save.** Currency reset and multiplier gain saved in two writes, so a
  crash between them loses one (inferred; see [player-data](../patterns/player-data.md)).
- **Pets as physics parts on the server.** Dozens of following pets per server lag phones;
  render followers on each client from replicated data (inferred; see
  [performance](../../.claude/skills/roblox-map/references/performance-and-devices.md)).
- **Content treadmill.** Zone 4 is empty because a solo dev can't build zones as fast as the
  curve consumes them. Reuse zones with new multipliers rather than building more art (inferred).
- **Pass wall at launch:** 8+ passes and prompts before the player has felt the loop.
- **AFK assumptions.** Roblox disconnects idle clients after about 20 minutes (community,
  DevForum). An in-game auto-click doesn't count as input, so don't promise overnight farming
  in-session; use offline income instead.

## Saturation & opportunity

All numbers are one tracker snapshot, so they show size, not growth (data, 2026-10-22).

- **`simulator` name theme: crowded.** 33 charted games, 168K players, 5.1K per game, median
  1.1K. The biggest is PS99 with 23% of the theme. The theme matches the word "simulator" in
  the title, so it also includes job sims (Firefighting Sim, Welding Simulator) (data).
- **Incremental Simulator subgenre (Roblox's own field):** 73 games, 594K players, 8.4% of
  charted players. It holds 5 of the 20 games under 90 days old with 2K+ players (data).
- **Breakout proof:** Tap Simulator REBORN, created 2026-08-04, had 35.6K players, 12.6M
  visits, 95% likes, top-earning #13 and up-and-coming #18 (data). A plain tap sim can still
  break out, and it monetizes well (inferred).
- **`clicker` in the name** is tiny: 6 games, median 296 players (data).
- **Simulation genre overall:** 2.41M players, 34.3% of charted players, 256 games (data).
- **Opportunity (inferred):** the open slot is an incremental sim with a fresh verb and a
  nameable theme (chop, climb, dig, feed) plus a second system, not another "Clicker
  Simulator." Before choosing a theme, read [trend-lifecycle](../fundamentals/trend-lifecycle.md):
  the `egg` and `verb-a-noun-title` waves are still being joined (data, 2026-10-22).

## Scope for a solo dev

Week counts are (inferred) for one developer working from this vault, with Rojo and Studio
MCP playtests.

**MVP:** one action, one currency, one upgrade track (8–10 levels), 3 zones, 2 eggs with 5–6
pets each, 1 rebirth tier, saving, 2 passes + 1 developer product, a stat leaderboard.

| Week | Build |
|---|---|
| 1 | Data model and session-locked save ([player-data](../patterns/player-data.md)); click remote with server rate limit; HUD with number formatting; number-pop feel |
| 2 | Upgrade track, zones and gates from one tuning module; sell pad if the variant has one; playtest the first 10 minutes |
| 3 | Eggs, odds UI, hatch reveal, pet inventory and equip, client-rendered followers |
| 4 | Rebirth (atomic), passes and product with `ProcessReceipt`, daily reward, analytics funnel events |
| 5–6 | Boss or server event, pet index, mobile UI pass, icon/thumbnail, launch |

**Cut from v1:** trading, world 2, enchants/crafting/fusion, clans, quests, custom-modeled
pets (no artist: use simple part-built or generated shapes, never copied pet designs).

## Top examples

- Pet Simulator 99 (case study: pet-simulator-99): breakables + pets + trading at
  huge scale; study the loop, not the monetization.
- Bee Swarm Simulator (no case study): eight-year-old collect-and-sell sim kept alive by a
  distinct theme and deep systems (data, 2026-10-22).
- Tap Simulator REBORN (no case study): a 2026 tap-sim breakout; taps, eggs, rebirths, islands
  (official game page, 2026-10).
- +1 Speed Keyboard Escape (case study: plus-one-speed-keyboard-escape): the "+1 per
  second" cousin of the genre.

## Build checklist for agents

### Do

- Keep all currency, stats, pets and multipliers on the server. The click remote carries no
  amount; the server computes the gain.
- Rate-limit the click remote per player with a token bucket of about 15–20 clicks per second;
  drop extras silently (inferred: a fast human clicks about 10–14 per second).
- Put every cost and reward in one tuning module. Upgrade cost = `base * r^level` with `r`
  between 1.07 and 1.15 (AdVenture Capitalist used 1.07, Cookie Clicker 1.15; press, Game
  Developer 2016; community, arXiv 2018).
- Rebirth cost geometric (`S * R^rebirths`, `R` between 1.5 and 3; community, DevForum).
  Show "x1.5 → x2.0 coins" on the confirm screen.
- Pace (inferred): first upgrade ≤ 30 s; first egg ≤ 3 min; zone 2 at 8–12 min; first rebirth
  at 25–45 min; each of the first five rebirth cycles shorter than the one before.
- Zone k costs about 8–15 minutes of expected income in zone k−1. Reward per action in zone k
  is 2–5x zone k−1 (inferred).
- Egg price about 1–5 minutes of current-zone income for the zone's basic egg and 10–15
  minutes for its best egg (inferred).
- Pet slots: 3 equipped at start, 6–8 reachable by play, +1 to +3 by pass (inferred).
- Keep pets, passes and the index through rebirth. Reset only currency and upgrades.
- Save a rebirth as one `UpdateAsync` (or one ProfileStore change) that resets and grants
  together.
- Format numbers with suffixes up to 1e33 and scientific notation past that. Use
  `NumberValue` or `StringValue`, not `IntValue`, for leaderstats that can pass 9.2e18.
- Set max players per server between 6 and 12.
- Make the auto-click pass click no faster than an average manual player, and only while the
  player is in the server.

### Don't

- Don't title or pitch the game as only "Clicker Simulator" or "X Simulator" (data: `clicker`
  median 296 players).
- Don't sell zone access, ship more than 4 passes at launch, or prompt a purchase in the
  first 2 minutes.
- Don't let the client send currency amounts, sell values, zone IDs it has "reached," or hatch
  results.
- Don't let any cost curve pass 1e300 without a big-number type.
- Don't build trading, world 2 or fusion before the first two weeks of retention data.
- Don't copy another sim's pet models, zone names or UI art; BIG Games has filed DMCA
  takedowns against look-alike cube-pet games (press, Dexerto 2023-09-08).

## Sources

1. https://www.roblox.com/games/72858262610964 — Tap Simulator REBORN page: taps, eggs, rebirths, islands (tracker snapshot 2026-10-22 in private/trends/latest.md)
2. https://www.roblox.com/games/1537690962 — Bee Swarm Simulator (tracker snapshot 2026-10-22)
3. https://www.roblox.com/games/8737899170 — Pet Simulator 99 (tracker snapshot 2026-10-22)
4. https://www.roblox.com/games/13127800756 — Arm Wrestle Simulator (tracker snapshot 2026-10-22)
5. https://www.roblox.com/games/85896571713843 — Bubble Gum Simulator INFINITY (tracker snapshot 2026-10-22)
6. https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i — exponential costs vs linear production; 1.07 growth example
7. https://arxiv.org/abs/1808.07540 — Cookie Clicker analysis; cost growth 1.15
8. https://devforum.roblox.com/t/simulator-rebirth-formula/3162074 — geometric rebirth cost S·R^r
9. https://devforum.roblox.com/t/rebirths-math-problem/768366 — summing rebirth costs for multi-buy
10. https://devforum.roblox.com/t/why-are-simulator-type-of-games-popular-these-days/595075 — 2020 dev views: plain sims fading, blend genres
11. https://devforum.roblox.com/t/what-is-a-simulator/1632385 — community definition of the genre (2022)
12. https://devforum.roblox.com/t/bypassing-built-in-idle-timeout/2152352 — ~20-minute idle disconnect
13. https://create.roblox.com/docs/luau/numbers — double precision, ~15 digits, ±1.7e308, int64 range
14. https://progameguides.com/roblox/how-to-get-more-rebirths-in-clicker-simulator/ and https://progameguides.com/roblox/how-to-get-gems-fast-in-roblox-clicker-simulator/ — Clicker Simulator Auto Click 399 / boosts 38–299 / x2 Rebirth Gems 349 Robux (seen in search excerpts; pages returned 403; unverified)
15. https://screenwiseapp.com/media/pet-simulator-99-game — PS99 pass prices (Auto Farm, Lucky)
16. https://www.sportskeeda.com/roblox-news/when-next-bubble-gum-simulator-infinity-update-summer-festival-explored — BGSI weekly update cadence (2025)
17. https://www.dexerto.com/roblox/pet-simulator-x-creator-under-fire-for-hypocritical-dmca-on-roblox-games-2284798/ — BIG Games DMCA takedowns (2023-09-08)
18. https://create.roblox.com/docs/production/monetization/paid-random-items — luck boosts count as paid random items

---
title: Idle / incremental
type: genre
read-when: Building an idle/incremental game, a "Verb a Noun" collect-and-train game, or any offline-progress number-growth loop.
last-researched: 2026-10-22
---

# Idle / incremental

## In one line

The player does one simple action, buys things that do it for them, watches the numbers grow
faster and faster, and resets (prestige) for a permanent multiplier when growth slows. On Roblox
the format now mostly appears as **"Verb a Noun"** games (Chop A Forest, Ride a Dino, Feed A
Mosquito): a physical verb in a 3D world, a stat trained on a machine, creatures or tools that
earn, and zones gated by the stat (data, 2026-10-22).

## Core loop

**Three sub-types on the charts** (data, 2026-10-22; grouping inferred):

| Sub-type | Examples (players, 2026-10-22) | Shape |
|---|---|---|
| "Verb a Noun" collect-and-train | Ride a Dino 28.5K, Chop A Forest 22.1K, Feed A Mosquito 21.4K | Physical action in zones; stat machine; pen/base income; Roblox labels them Tycoon or Incremental Simulator |
| Pure incremental | Noob Incremental 4.4K, Idle Mafia Game 3.5K, Immortality Incremental 2.8K | Menu-driven; hundreds of upgrades; several prestige layers |
| Idle job/tycoon | Sell Lemons 25.5K ("earn 100% of your income offline") | Sell loop plus offline income. See [job-sims](job-sims.md) |

**Moment to moment (1–10 s):** perform the verb (chop, ride, feed, tap), see a number pop, and
collect. Chop A Forest: break trees, collect logs, sell them for coins (data, description
2026-10-22).

**Session (10–25 min):** buy the next tool, generator or creature; raise the trained stat;
reach the next zone; hit a milestone that multiplies output. Ride a Dino: jump onto
stampeding dinos, capture them, put them in a pen that earns, and train stamina on a machine.
One stamina upgrade tier costs $75B (community, Roonby 2026-10-20).

**Long term (days to weeks):** prestige or rebirth layers, new zones (Ride a Dino lists 9 eras
and 50+ species from Common to Divine), classes and gear (data, 2026-10-22). Noob Incremental
advertises "hundreds of Upgrades, dozens of Stats, multiple Prestige layers" (data, 2026-10-22).

## Main verbs

Act (one physical verb), collect, buy, upgrade, train (stat machine), unlock zone, prestige,
claim offline earnings, roll (RNG layers such as runes or auras), fuse.

## Why players come back

- **Something waits to be claimed.** Offline income is the genre's return hook. Feed A
  Mosquito's V3 update headline was "Added offline earnings" (data, 2026-10-22).
  [Retention](../fundamentals/retention.md) lists "something finishes while they're away" as a
  D1 hook (inferred).
- **Ladder climbing.** Each prestige makes the same ground faster, which Pecorella calls the
  core appeal of idle games (press, Kongregate 2017).
- **Bumpy pacing.** Milestone multipliers cause bursts of rapid buying between slow stretches.
  Vary reset patterns so progress feels uneven, not flat (press, Kongregate 2017).
- **A visible next zone or tier**, with its requirement on screen. (inferred)
- **Low skill, short sessions.** Works on phones and for young players. (inferred)
- **High revisit even when small.** Noob Incremental, with 4.4K players, ranks #17 on Roblox's
  top-revisited chart (data, 2026-10-22).

## What separates top games from clones

1. **A verb that feels good in 3D.** Trees fall, dinos stampede. Charted pure-menu incrementals
   top out at ~4K players while "Verb a Noun" games reach 20–30K (data, 2026-10-22).
   (inference from a single snapshot)
2. **A second system that unlocks after the first hour**: classes (Chop A Forest), auras (Ride a
   Dino), runes (Noob Incremental) (data; community). The first hour teaches one system; the
   second hour adds one more. (inferred)
3. **Labeled updates.** Leaders carry update tags in their names: [CH2], [V3], [UPD 5]
   (data, 2026-10-22). See [live-ops-and-updates](../fundamentals/live-ops-and-updates.md).
4. **Co-op that doesn't slow anyone down.** Chop A Forest: "SOLO & FRIEND RUNS SAVE", 18 per
   server (data, 2026-10-22).
5. **Tested math.** Cost curves, milestone multipliers and prestige formulas are tuned with a
   spreadsheet or simulation before launch (press, Kongregate 2016–2017).

## Session shape

- **Roblox kicks idle players.** `Player.Idled` fires after ~2 min idle and Roblox disconnects
  after 20 min idle (official, 2026-10). Progress that needs "stay in the server" doesn't work;
  offline income with a claim on return does. (inferred)
- **Target average session 15–25 min**, the range where Roblox D1 retention peaks (press,
  GameAnalytics 2025; see [retention](../fundamentals/retention.md)).
- **First 60 s (inferred targets):** first earn within 5 s of spawning, first purchase within
  30 s, and output visibly doubles by 60 s.
- **First 10 min (inferred targets):** 3–5 purchases, first milestone multiplier, second zone
  or tool visible with its price, offline earnings explained ("Your X earn while you're away").
- **First prestige (inferred target):** available after 30–60 min of total play, i.e. in the
  second or third session, so the first reset is the reason to come back.
- **Day 7 (inferred targets):** 2–5 prestiges, the second system unlocked, a long goal (a top
  zone or a full collection) visible.

## Social hooks

- **Group and like bonuses** are common: "+10% Rune Speed" for joining the group and liking
  (data, Noob Incremental description 2026-10-22).
- **Subscription perks**: +10% to +15% income for "Roblox Plus" members appears in descriptions
  (data, 2026-10-22; program terms unverified).
- **Co-op runs** that save for each player (Chop A Forest, data). Incremental Simulator games
  run larger servers than tycoons: median 10 vs 6 (data, 2026-10-22).
- **Leaderboards** of lifetime totals and prestige count. See
  [leaderboards](../patterns/leaderboards.md). (inferred)
- **Server-wide boosts** (a purchase or event that boosts everyone) turn spending into a social
  moment. (inferred)

## Monetization that works here

- **2× income pass.** The standard first pass in every income game (see
  [steal-a-x](steal-a-x.md) for dated prices).
- **Auto pass:** auto-collect, auto-buy or auto-train. Sells convenience, not new power.
  (inferred)
- **Bigger offline cap**, e.g. 2 h free → 8 h with a pass. (inferred)
- **Timed boosts** (2× for 15–30 min) at 25–50 R$: cheap and repeatable, which feeds the spend
  days discovery signal (official signal, 2026-10; prices inferred). See
  [discovery-algorithm](../fundamentals/discovery-algorithm.md).
- **Robux tools and classes.** Chop A Forest: top class 599 R$, Infinite Bag 149 R$, a 5-minute
  Trial Saw for 25 R$ (community, 2026-10, unverified).
- **Rewarded video ads** for a boost: `AdService:CreateAdRewardFromDevProductId`, then
  `AdService:ShowRewardedVideoAdAsync`. The reward arrives through
  `MarketplaceService.ProcessReceipt` with `Enum.ProductPurchaseChannel.AdReward` (official,
  2026-10). Player-started, rate-limited ads are exempt from the 2026-08-25 media-feed rule
  (official).
- See [monetization](../fundamentals/monetization.md) for pass versus product rules.

## Common failure modes

- **Walls.** Exponential costs with nothing else to do for 10+ minutes. Add a milestone, a new
  system or a prestige before every wall. (inferred, from Kongregate 2016)
- **AFK-in-server design.** Kicked at 20 min idle (official). Use offline income.
- **Number overflow.** Luau numbers are doubles: integers stay exact only to 2^53 (~9.0e15), and
  values overflow to infinity past ~1.8e308. Leaderstats break past these limits (community,
  DevForum "After 1e308 leaderstat game breaks"). `IntValue` is commonly described as a 64-bit
  integer (max ~9.2e18); its reference page doesn't state the range (unverified).
- **Uncapped offline income** breaks the economy and makes active play pointless. (inferred)
- **Prestige too early** (no felt gain) or **too late** (wall before it). (inferred)
- **Menu overload in minute one.** Show one currency and one button; unlock tabs as they matter.
  (inferred) See [first-time-experience](../fundamentals/first-time-experience.md).
- **Rewarded feeds.** Rewarding viewing of an autoplaying or scrolling media feed gets a game
  removed from Roblox Kids and Select (official, 2026-08-25).
- **Generic "clicker" or "idle" titles.** The `clicker` theme has 6 charted games, median 296
  players (data, 2026-10-22). Name the verb, not the genre. (inferred)

## Saturation & opportunity

All (data, 2026-10-22, single snapshot, so no growth claims):

| Theme / field | Games | Players | Median | Note |
|---|---|---|---|---|
| Roblox subgenre Incremental Simulator | 73 | 594K (8.4% of charted) | 2.4K | Includes Fish It!, Anime Dice, +1 games |
| `verb-a-noun-title` | 48 | 1.24M | 2.9K | 17 rising; Steal An Egg holds 71% |
| `plus-one` | 15 | 124K | 4.1K | 5 rising, all created 2026-09-18 → 10-05 |
| `idle` | 4 | 11K | 3.1K | "Idle"/"Incremental" in the title |
| `clicker` | 6 | 3.8K | 296 | Spent |

- Without Steal An Egg, the 47 other "Verb a Noun" games share ~363K players (data, calculated).
  The naming wave is still being joined: newest rising entry created 2026-10-10 (data).
- Rising "Verb a Noun" incrementals: Ride a Dino (created 2026-08-24, 98% likes), Fake an Egg
  (2026-10-04), Chop A Forest (2026-09-21, top-earning #49), Feed A Mosquito (2026-08-21, 80%
  likes), Create a Robot Fighter (2026-09-25, 72% likes) (data, 2026-10-22).
- Low like ratios (72–80%) on some entries suggest players notice thin clones. (inferred)
- Opportunity (inferred): a verb nobody has used, with its own satisfying 3D feedback, on the
  collect → pen income → stat machine → zone skeleton. The title pattern alone is not a spin.
  See [trend-lifecycle](../fundamentals/trend-lifecycle.md).

## Scope for a solo dev

A good fit: low art needs, mostly systems and UI, and the math can be tested in code. (inferred)

**MVP** (inferred)
- One verb with strong feedback (sound, particles, number pops). See
  [game-feel](../../.claude/skills/roblox-vfx/references/game-feel.md).
- One soft currency plus one prestige currency.
- 6–8 generators, tools or creature tiers; 3 zones gated by a trained stat.
- Upgrade tree of ~20 nodes ([upgrade-trees](../patterns/upgrade-trees.md)).
- One prestige layer ([rebirth-prestige](../patterns/rebirth-prestige.md)).
- Offline income with a cap and a "welcome back" claim screen
  ([idle-offline-income](../patterns/idle-offline-income.md)).
- Number formatting with suffixes; autosave ([player-data](../patterns/player-data.md)).
- 2 passes (2× income, auto) plus 2 timed boosts.

**Build order** (one developer with Claude Code; rough weeks, inferred)

| Week | Build |
|---|---|
| 1 | Verb, currency, generators, number formatting, save |
| 2 | Upgrades, stat machine, zones, offline income, prestige |
| 3 | Balance with a headless Luau simulation of 3 h of play; shop, passes, FTUE |
| 4 | Mobile UI, feedback polish, icon/thumbnail, launch |
| 5+ | Weekly: one zone or tier plus one event |

**Cut from v1:** second prestige layer, RNG layers (runes, auras), pets, trading, co-op runs,
classes. Add them as updates once D1 is known. (inferred)

## Top examples

- Steal An Egg (case study: steal-an-egg): idle pen income under a stealing loop;
  #1 on Roblox (data, 2026-10-22).
- +1 Speed Keyboard Escape (case study: plus-one-speed-keyboard-escape): the "+1 stat"
  cousin of this genre; 50K (data, 2026-10-22).
- Sell Fries! (case study: sell-fries): a small 2026 job-sim breakout with an idle
  sell loop.
- Chop A Forest, Ride a Dino, Feed A Mosquito: the 2026 "Verb a Noun" incrementals (data).
- Noob Incremental: the pure-incremental reference; small but highly revisited (data).

## Build checklist for agents

Numbers are starting values to tune unless tagged otherwise. (inferred)

### Do

- Cost of the next item = base × rate^owned, rate 1.07–1.15 (AdVenture Capitalist used 1.07;
  press, Kongregate 2016). Use the closed-form bulk-buy and max-affordable formulas, not loops.
- Production = base × owned × multipliers. Add ×2 milestones at 25, 50 and 100 owned
  (AdVenture Capitalist used ×2 at 25 and 50; press, Kongregate 2016).
- Prestige currency from lifetime earnings with a root, e.g. k × √(lifetime / threshold)
  (AdVenture Capitalist style: doubling needs ~3–4× the previous run; press, Kongregate 2017).
- Make the first prestige worth at least ×2 total output.
- Store `os.time()` on leave and on autosave. On join, pay offline income =
  rate × min(elapsed, cap) × 0.5–1.0, with a 2–8 h cap (Egg, Inc. capped offline at 2 h in
  2017; press, Kongregate 2017).
- Show a "while you were away" claim screen. Never auto-credit silently.
- Run the economy on the server at a fixed tick (e.g. 1 Hz) and let the client interpolate the
  display. (inferred)
- Format numbers with suffixes (K, M, B, T, Qa, Qi…) and switch to scientific notation past
  ~1e33.
- If values can pass ~1e300, use a big-number module (EternityNum, InfiniteMath, GammaNum;
  community) from day one. Switching later means touching every script (community, DevForum).
- Keep big totals in server data as numbers (or big-number tables) and show them through a
  formatted `StringValue` in leaderstats, not an `IntValue`.
- Simulate 3 h of play in a headless Luau script. Report time to the first purchase (≤ 30 s),
  first milestone (≤ 5 min), first prestige (30–60 min) and each zone.
- Save on `Players.PlayerRemoving` and in `game:BindToClose`, with session locking
  ([player-data](../patterns/player-data.md)).

### Don't

- Don't require players to stay in the server to progress (20-min idle kick, official).
- Don't leave offline income uncapped or at 100% with no active-play bonus.
- Don't reward watching any autoplaying or scrolling media feed (official, 2026-08-25).
- Don't show more than one currency and one primary button in the first minute.
- Don't put a wall (10+ min with no affordable purchase) before the first prestige.
- Don't trust client-sent amounts, tick counts or timestamps. The server owns time and income.
- Don't title the game "Idle ___" or "___ Clicker". Name the verb.
- Don't sell Robux skips for timers that gate the core loop; sell permanent speed instead.

## Sources

1. https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i — cost and production formulas, bulk-buy math, 1.07 rate, milestone ×2 (Pecorella, 2016)
2. https://www.gamedeveloper.com/design/the-math-of-idle-games-part-iii — prestige formulas, doubling ratios, Egg, Inc. 2 h offline cap, bumpy pacing (Pecorella, 2017)
3. https://create.roblox.com/docs/reference/engine/classes/AdService — rewarded video ad API names, ProcessReceipt AdReward channel
4. https://devforum.roblox.com/t/roblox-kids-and-select-new-restrictions-on-reward-driven-media-feeds/4829188 — media-feed reward rule and rewarded-ad exemption (2026-08-25)
5. https://create.roblox.com/docs/reference/engine/classes/Player — Idled event and 20-minute idle disconnect
6. https://devforum.roblox.com/t/after-1e308-leaderstat-game-breaks/3740242 — overflow past 1e308 in leaderstats
7. https://devforum.roblox.com/t/gammanum-up-to-100x-faster-than-eternitynum/3906397 — big-number modules (community)
8. https://devforum.roblox.com/t/dealing-with-large-numbers/4074545 — switching cost of big-number modules
9. https://roonby.com/2026/10/20/ride-a-dino-roblox-beginner-guide-fast-money-best-dinosaurs-stamina-and-fusion/amp/ — Ride a Dino loop, stamina machine costs (2026-10-20)
10. https://bloxodes.com/wiki/chop-a-forest/classes — Chop A Forest classes and Robux prices (community, unverified)
11. https://www.gameanalytics.com/reports/2025-roblox-report — retention by session length
12. private/trends/latest.md — themes, subgenres, players, server sizes, descriptions (data, 2026-10-22)

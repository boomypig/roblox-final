---
title: RNG aura
type: genre
read-when: Building a rolling/RNG aura game (Sol's RNG-likes): luck, "1 in X" rarities, reveals, auto-roll, biomes, potions.
last-researched: 2026-10-22
---

# RNG aura

## In one line

Press Roll (or let it auto-roll), get a random aura with a published "1 in X" rarity, equip the
rarest one so it glows around your avatar, and stack luck from passes, potions, gear and timed
biomes to chase rarer ones. Sol's RNG leads the theme; most charted RNG games now bolt the roll
onto another loop.

## Core loop

- **Moment to moment (1–3 s per roll):** roll → short spin animation through names → reveal
  with tier color and sound → keep or ignore (inferred; Sol's RNG sells a pass that skips the
  animation, community).
- **Session (20–60 min, often idle):** auto-roll while a biome or potion is active, collect
  map pickups, craft a potion or gear from duplicate auras, equip the best (community,
  bloxodes; inferred).
- **Meta (weeks):** collection completion, crafted luck gear, rare-biome hunting, the next
  "1 in a billion" chase; new auras each update (community; inferred).

## Main verbs

Roll · auto-roll · reveal · equip/show off · craft (consume duplicates) · drink potion · wait for
biome · collect pickups · (trade, fight, build in hybrids).

## How the leader works (Sol's RNG, community sources, unverified details)

| System | Behaviour |
|---|---|
| Auras | ~290–340 auras across tiers Basic, Epic, Unique, Legendary, Mythic, Exalted, Glorious, Transcendent, plus challenge and event auras; rarest cited at 1 in 3,000,000,000 (community, 2026-03) |
| Reveal | Cutscenes escalate with rarity; above 1 in ~100M the whole server is notified; above 1 in 1B auras get unique cutscenes with their own music (community, 2026-03) |
| Biomes | The server rolls for a biome every second: common ones at 1 in 500–750 per second lasting 2 min; rare ones 1 in 3,000–9,000 lasting ~10–11 min; the rarest natural biome 1 in 30,000 for 2 min. Only that biome's native auras get better odds (community, bloxodes) |
| Potions | Luck or roll-speed boosts, from 1-minute map pickups to 4-hour crafted brews; some one-roll potions add huge luck (community, bloxodes) |
| Gear | One per hand: right hand adds luck or roll speed, left hand changes the bonus-roll cooldown and multiplier; crafted from specific auras and materials (community, bloxodes) |
| Biome items | Pocket items that double a biome's spawn chance; runes that let biome auras roll without the biome (community, bloxodes) |
| Passes | VIP x1.2 final luck; VIP+ x1.2 (x1.3 with VIP) and auto-collect; skip-animation pass; merchant teleport; starter pack of potions and coins (community, bloxodes; prices not checked) |

Mean wait for a biome at `1 in N per second` is N seconds of server time: 1 in 500 → ~8 min,
1 in 30,000 → ~8.3 h (inferred, arithmetic). That pacing makes common biomes a session event
and rare biomes a "server hop and pray" event.

## Why players come back

- **The chase never ends.** Odds go up to "1 in billions", so there's always a rarer aura
  (community). Each update adds auras, biomes and gear (inferred).
- **Timed luck.** Biomes, potions and events are windows; being online inside one is the best
  use of time (inferred).
- **Visible status.** The equipped aura is worn on the avatar, so rarity is seen by everyone in
  the server (inferred).
- **Crafting turns duplicates into progress,** so bad rolls still count (community, bloxodes;
  inferred).
- **Daily / long-term:** Sol's RNG is #14 on top-revisited (data, 2026-10-22), a sign players
  return over many days.

## What separates top games from clones

1. **Reveal feel scales with rarity.** Common: instant. Rare: color, sound, screen flash. Very
   rare: server message. Ultra rare: cutscene and music (community for Sol's thresholds;
   inferred for the ladder). Flat reveals make rolling feel like spreadsheet work.
2. **Many luck sources, all visible.** Passes, potions, gear, biomes, events, each stated as a
   number (community). Players optimize stacks; that *is* the midgame (inferred).
3. **Auras look different, not just recolored.** Shape, motion and sound per aura (inferred).
4. **Systems around the roll:** crafting, biomes, merchants, challenge areas (community). A
   clone with only a Roll button has no week-2 goals (inferred).
5. **Regular "Eon"/era updates** with new auras; the game has run since 2023-12 (data) with a
   new event label in its title (data, 2026-10-22: "Radiant Forest").

## Session shape

- **Typical session:** long and partly idle; players leave auto-roll running (inferred).
  Roblox still disconnects players idle 20+ min, and `Player.Idled` fires after ~2 min
  ([retention](../fundamentals/retention.md), official 2026-10), so idle rolling inside the
  server is fragile.
- **First 60 seconds:** Roll button already pulsing; first roll within 5 s; a guaranteed
  uncommon or rare within the first 10 rolls (pity) so the reveal ladder shows itself; equip it
  (inferred).
- **First 10 minutes:** ~150–300 rolls, first rare reveal with sound, first potion pickup, first
  biome seen (tune common biomes so most new players see one), auto-roll unlocked or shown
  (inferred).
- **Day 7:** first crafted gear, a biome-native aura, a personal best rarity worth showing,
  collection % visible (inferred).

## Social hooks

- **Server and global announcements** of rare rolls: rarity is public status (community).
  Use `MessagingService:PublishAsync` for cross-server announcements of top-tier rolls
  (inferred), rate-limited.
- **Shared biomes:** the biome is server-wide, so everyone in the server benefits at once
  (community).
- **Showcase:** equipped aura on the avatar; a "rarest roll" leaderboard
  ([leaderboards](../patterns/leaderboards.md)).
- **Trading** is possible but raises dupes and policy issues: if an aura can come from Robux
  rolls, players with `IsPaidItemTradingAllowed` false must not be able to trade it (official,
  2026-10). See [trading](../patterns/trading.md).

## Monetization that works here

**Paid random item rules (official, Roblox creator docs, 2026-10). Reviewer: check every one.**
- Free rolls need no odds disclosure. Rolls bought with Robux, or with currency bought with
  Robux (keys, tickets, rerolls), must show every outcome and its odds **as percentages that
  sum to 100%**, before the spend.
- Luck boosts, pity systems and roll-boost items are "probability modifier" items. Their effect
  must be explained numerically before purchase, and displayed odds must update while they're
  active. Potions with random duration are "enhancement" items under the same rules.
- Too many outcomes for one screen: a pop-up labeled "Info" or "Details", visible before
  purchase. A bare (i) icon is not enough.
- Rounding: at least 4 decimal places past the first non-zero digit, with the disclaimer
  "Probabilities are rounded; total of displayed individual probabilities may not equal 100%."
  So 1 in 3,000,000,000 shows as `0.00000003333%`.
- If an outcome can only be obtained once per user, update that user's remaining odds.
- Call `PolicyService:GetPolicyInfoForPlayerAsync(player)` on the server. If
  `ArePaidRandomItemsRestricted` is true: offer a free earnable path, a fixed disclosed order, a
  direct purchase priced by expected value, hide it, block with a message, or move the user out
  of that area.
- If `IsPaidItemTradingAllowed` is false, that user must not trade paid-random outcomes.
- Full rules: [monetization](../fundamentals/monetization.md).

**"1 in X" display rules (inferred from the policy):**
- "1 in X" is the genre's language; keep it, but for anything touched by Robux also show the %.
- Show the *effective* odds for this player now (luck, biome, potion applied), with base odds
  in smaller text.
- Odds must be the true odds of your algorithm. With the common "check rarest first, first hit
  wins" roll, a common aura's true chance is lower than 1/N because rarer checks come first;
  compute the real distribution (exactly or by simulation) for the disclosure table.

**What we sell (inferred):** luck passes with a stated multiplier (genre norm x1.2, community),
a roll-speed pass, a skip-animation pass, timed luck potions with exact multiplier and duration,
extra aura storage, aura showcase cosmetics, private servers. All luck items go through the
disclosure and PolicyService checks above.

**Avoid:** selling Robux rolls directly as the main product (strictest rules, highest risk);
"limited-time luck" countdowns that restart; luck items with hidden effects.

## Common failure modes

- **Flat reveals.** Everything plays the same animation; rare rolls don't feel rare (inferred).
- **Luck inflation.** Stacked multipliers trivialize the table; Fisch-style per-item caps or
  diminishing returns help (inferred; see [fishing](fishing.md)).
- **Client-side RNG.** If the client rolls, exploiters print top auras. Roll only on the server
  with `Random.new()` held per server; never accept a client-reported result
  ([security](../../.claude/skills/roblox-code/references/security.md)).
- **Roll-remote spam.** Rate-limit `RequestRoll` to the roll cooldown; auto-roll runs on the
  server, not as a client spam loop (inferred).
- **Wrong odds on screen.** Showing 1/N when the algorithm gives something else breaks the
  "actual numerical odds" rule (official, 2026-10).
- **Viral spike, then nothing.** Slime RNG peaked at 1,309,649 on 2026-05-23 (community tracker,
  Rolimons) and has 296 players on 2026-10-22 (data), −99.98%. A roll loop alone doesn't hold
  players; see [trend-lifecycle](../fundamentals/trend-lifecycle.md).
- **Idle-only design.** Players kicked after 20 min idle lose their "session"; bank progress or
  make auto-roll survive rejoin (inferred).
- **Copying aura names, biome names or cutscenes** from Sol's RNG.

## Saturation & opportunity

From the tracker (data, 2026-10-22, single snapshot, so no growth claims):

| Theme | Games | Players | Per game | Median | Leader share | In top 100 | Rising |
|---|---|---|---|---|---|---|---|
| rng-aura | 12 | 50K | 4.2K | 1.4K | Sol's RNG 61% | 1 | 2 |

| Game | Players | Created | Genre | Hybrid of |
|---|---|---|---|---|
| Sol's RNG | 30.4K | 2023-12-03 | Simulation / Incremental Simulator | pure RNG |
| Roll A Stickman! | 7.7K | 2026-09-10 | Simulation / Incremental Simulator | RNG + characters (name) |
| Aura Dance Battles | 3.3K | 2026-08-30 | Party & Casual / Minigame | aura + party minigame |
| Roll a Barber RNG | 2.3K | 2026-09-29 | Simulation / Tycoon | RNG + job/tycoon; Up-and-Coming #50 |
| +1 Aura Per Click | 2.2K | 2026-04-22 | Simulation / Incremental Simulator | aura + "+1" clicker |
| Heroes RNG | 1.7K | 2026-05-11 | Simulation / Incremental Simulator | RNG + heroes |
| Build a base RNG | 1.1K | 2026-05-31 | Strategy / Tower Defense | RNG + base/TD |
| Slime RNG | 296 | 2026-02-25 | Simulation / Incremental Simulator | 537M visits, peak 1.31M (above) |

- The theme median (1.4K) is below the median charted game (1,544) (data, 2026-10-22): many
  small games. Sol's RNG holds 61% of the theme's players (data), which meets the report's
  "one game dominates" rule (60%+).
- Sol's RNG: 30,384 playing, 2.24B visits, 91% likes, top-revisited #14, top-earning #26
  (data, 2026-10-22); all-time peak 193,836 on 2024-05-12 (community tracker, Rolimons). A
  long-lived, moderately sized game, not a spike.
- Opportunity (inferred): a pure Sol's RNG clone fights a 3-year content backlog. The newer
  entries are RNG + another loop (job, tower defense, characters, clicker). Use the roll as the
  *reward engine* for a different verb, per spin #1 in
  [trend-lifecycle](../fundamentals/trend-lifecycle.md). See also
  [gacha-raid](gacha-raid.md) and [pet-egg-collection](pet-egg-collection.md).

## Scope for a solo dev

**MVP, about 3–4 weeks (inferred):**

| Week | Build |
|---|---|
| 1 | Server roll service (`Random.new()`, rarity table, luck), `RequestRoll` remote with cooldown, auto-roll toggle on the server, inventory + equip, ProfileStore save |
| 2 | 30–40 auras as `ParticleEmitter`/`Beam`/`Trail`/`Highlight` presets on the character, tiered reveal (UI tween, sound, flash), server announcements |
| 3 | 3–4 biomes (per-second roll, `Lighting`/`Atmosphere` changes), 2 potions, 1 crafting recipe using duplicates, collection UI with "1 in X" and effective odds |
| 4 | Passes/products with disclosure UI and PolicyService gating, rarest-roll leaderboard, FTUE pity, analytics, mobile pass |

Post-launch: 5–10 auras + 1 biome or gear per update, every 1–2 weeks.

**Cut from v1:** trading, cutscenes beyond one shared camera move, challenge zones, merchants,
runes, 100+ auras. Auras are code-built effects, so no artist is needed; budget particle counts
for phones (`ParticleEmitter.Rate` low on other players' auras;
[performance](../../.claude/skills/roblox-map/references/performance-and-devices.md)) (inferred).

## Tuning starting points (inferred, tune with analytics)

| Tier | Base odds | Reveal |
|---|---|---|
| Common | 1 in 2 – 1 in 10 | instant, soft tick |
| Uncommon | 1 in 16 – 1 in 100 | color + sound |
| Rare | 1 in 250 – 1 in 1,000 | color, sound, short flash (0.3 s) |
| Epic | 1 in 2,500 – 1 in 25,000 | 1–1.5 s build-up, server chat line |
| Legendary | 1 in 50K – 1 in 1M | 2–3 s sequence, server-wide banner |
| Mythic+ | 1 in 2M – 1 in 1B | skippable cutscene ≤ 6 s, cross-server message |

- Base roll cooldown 1–2 s; roll-speed upgrades cap at ~2x (inferred).
- Luck: per-aura chance = `min(1, luck / N)`, checked rarest first; cap total luck from
  purchases (e.g. x2 from all Robux items combined) so free players can still roll everything
  (inferred).
- Common biome: 1 in 400–600 per second, 2–3 min; rare biome: 1 in 10,000–30,000, 2–5 min;
  native auras x3–x10 during the biome (inferred, near the leader's scale).
- Pity for new players: a guaranteed Rare within the first 10 rolls; no paid pity at launch
  (paid pity is a regulated probability modifier, official 2026-10).

## Top examples

- Sol's RNG: the reference pure-RNG design; long-running, update-driven (data; community).
- Slime RNG: 1.31M peak (2026-05-23) to under 400 players in five months (community tracker;
  data). The cautionary spike.
- Roll a Barber RNG, Roll A Stickman!, Build a base RNG: 2026 hybrids (data).
- No case study yet; case study: anime-dice covers a related dice/roll loop.

## Build checklist for agents

### Do
- Roll on the server only; clamp `RequestRoll` to the cooldown with a per-player token bucket.
- Store the rarity table server-side; send clients display data only.
- Show base and effective odds per aura; show "1 in X" and % for anything Robux touches.
- Compute the true outcome distribution of your roll algorithm and use it in the odds table.
- State every luck item's multiplier and duration before purchase; update shown odds while
  active.
- Call `PolicyService:GetPolicyInfoForPlayerAsync` and apply a treatment when
  `ArePaidRandomItemsRestricted` is true; block trading of paid outcomes when
  `IsPaidItemTradingAllowed` is false.
- Escalate reveals by tier (table above) and let players skip anything over 2 s.
- Run auto-roll on the server and save results immediately so a kick or crash loses nothing.
- Announce top-tier rolls server-wide, and cross-server with `MessagingService` rate-limited.
- Give duplicates a use (crafting or conversion) from day 1.
- Simulate 10^7+ rolls offline to check the odds table and luck caps before launch.

### Don't
- Don't roll or decide rarity on the client, and don't trust client-sent aura IDs.
- Don't display 1/N when your algorithm's true odds differ.
- Don't use a bare (i) icon for odds, or show odds only after purchase.
- Don't sell luck without numbers, or let purchased luck flatten the table.
- Don't sell Robux rolls to policy-restricted users or let them trade paid outcomes.
- Don't ship a Roll button with no biome, crafting or collection goal behind it.
- Don't copy Sol's RNG aura, biome, NPC or item names, cutscenes or music.

## Sources

1. https://create.roblox.com/docs/production/monetization/paid-random-items — paid random item types, % odds, rounding, Info pop-up, luck modifiers, PolicyService flags, restricted-user treatments, trading
2. https://create.roblox.com/docs/reference/engine/classes/PolicyService — GetPolicyInfoForPlayerAsync fields
3. https://bloxodes.com/wiki/sols-rng/biomes — biome spawn chances and durations (community wiki)
4. https://bloxodes.com/wiki/sols-rng — potions, gear, lanterns, runes, passes, aura counts (community wiki)
5. https://allthings.how/sols-rng-aura-tier-list-every-rarity-and-drop-rate-ranked/ — aura tiers, announcement and cutscene thresholds (2026-03-20)
6. https://www.rolimons.com/game/15532962292 — Sol's RNG peak 193,836 (2024-05-12)
7. https://www.rolimons.com/game/92416421522960 — Slime RNG peak 1,309,649 (2026-05-23)
8. https://earnaldo.com/blog/slime-rng-vs-sols-rng — Slime RNG release and peak context
9. https://create.roblox.com/docs/reference/engine/classes/MessagingService — cross-server messages
10. ../fundamentals/retention.md — idle kick, Player.Idled
11. private/trends/latest.md and tools/trends lookups — theme stats, game numbers (data, 2026-10-22)

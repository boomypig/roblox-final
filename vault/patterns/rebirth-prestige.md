---
title: Rebirth and prestige
type: pattern
read-when: Adding rebirth/prestige resets and multipliers.
last-researched: 2026-10-22
---

# Rebirth and prestige

## What it is

The player gives up a run's progress (cash, upgrades, zone) and gets a permanent bonus that makes
the next run faster. Roblox games mostly use **fixed-price rebirths**: pay `cost(n)`, get rebirth
`n+1` and a bigger multiplier. Idle games mostly use **earn-based prestige**: reset any time and get
prestige currency computed from what the run earned. Both can stack into layers (rebirth → super
rebirth → ascension), where each layer resets everything below it.

## Why it works

- Early game is the most fun part of an incremental curve: purchases come every few seconds. A
  rebirth restores that pace at a higher multiplier, so the player re-climbs old ground fast and
  feels the bonus directly (inferred).
- Exponential costs eventually outrun polynomial production in any incremental game. A reset is
  how the designer lets the player escape that wall without adding infinite content
  (community, 2016-10).
- Prestige gain is usually made to grow much more slowly than earnings, so "go further this run"
  has diminishing returns and frequent resets win. That keeps the loop short and repeated
  (community, 2017-02).
- The rebirth count is a public status number and a long-term goal. Long-term goals such as
  rebirths are a D8–28 return reason, which now feeds Home recommendations (official guidance for
  long-term goals, 2026-10; the rebirth link is inferred). See
  [retention](../fundamentals/retention.md).

## Genres that use it

[Simulator](../genres/simulator.md), [tycoon](../genres/tycoon.md),
[idle/incremental](../genres/idle-incremental.md), [steal-a-x](../genres/steal-a-x.md),
[+1 stat](../genres/plus-one-stat.md), and progression layers in
[anime RPGs](../genres/anime-rpg.md). Rare in round-based, obby and social games, where there is
no accumulating economy to reset.

## Design rules

### What resets, what persists

Decide this per field before writing code. Put the answer in the design doc.

| Usually resets (the "run") | Usually persists | Decide case by case |
|---|---|---|
| Soft currency (cash, coins) | Rebirth count and its multiplier | Pets / units (kept in Pet Simulator 99, wiped in Steal a Brainrot; sources below) |
| Upgrades bought with soft currency | Premium currency (gems), Robux purchases | Zone / world unlocks (Pet Simulator 99 is reported to send players back to spawn, unverified) |
| Placed buildings, droppers, conveyors | Cosmetics, titles, badges, codes redeemed | Quest progress |
| Run-only stats (strength, speed) | Prestige-shop upgrades | Equipped tools |

- **Anything bought with Robux must persist.** Resetting a paid item is a refund request waiting to
  happen, and it breaks the receipt record in [player data](player-data.md) (inferred).
- **Real examples:**
  - **Miner's Haven** (tycoon, open source since 2019): money drops back to a small starting amount,
    normal items in inventory are cleared, placed items are destroyed, and a starter kit is
    handed out. The life counter, shards and a few item classes (rebirth-tier items) persist
    (community, 2019).
  - **Steal a Brainrot**: a guide says rebirth wipes cash and brainrots. The rewards are a cash
    multiplier, an extra base slot, +10 s of base-lock time, and a cash grant to start the next run
    (press, 2025-11).
  - **Pet Simulator 99**: rebirths are gated by reaching a zone (25, then 50) rather than a price.
    Rewards include feature unlocks (teleport, auto-hatch, clans) plus pet-strength boosts; coins and
    zone progress reset. Guides disagree on details (press, 2025–26, unverified).
- **A starting grant scaled to rebirth level** (Steal a Brainrot's cash bonus) skips the first
  trivial purchases of each run, so the re-climb starts at the interesting part (inferred).

### Two cost models

**A. Fixed-price rebirth (default for Roblox).** `cost(n) = C0 × g^n`, where `n` is rebirths already
done. The price is a visible number with a progress bar, which young players understand at a glance
(inferred).

**B. Earn-based prestige (idle games).** `gain = k × (E / E0)^α`, where `E` is lifetime or run
earnings. Earnings needed to double prestige gain = `2^(1/α)`. Formulas from shipped idle games
(community, 2017-02):

| Game | Prestige gain | Earnings needed to double prestige |
|---|---|---|
| Realm Grinder | `(√(1 + 8c/10¹²) − 1) / 2` on max currency | ~4× |
| AdVenture Capitalist | `150 × √(lifetime / 10¹⁵)` | ~3–4× |
| Cookie Clicker | `∛(lifetime / 10¹²)` | ~8× |
| Egg, Inc. | `(run / 10⁶)^0.14` per run | ~128× |

Lower `α` means flatter gains and more frequent resets. Use model B only for a true idle game whose
players read numbers; show the "prestige now: +N" preview at all times (inferred).

**A + overshoot reward (Miner's Haven).** Base price `25e18` ($25Qn). The price multiplies by
`(2⌊n/5⌋ + 1) × (1 + 100⌊n/25⌋) × (1 + 1000⌊n/500⌋)`, so it steps up every 5 and every 25 lives
rather than every life, and the whole term is raised to `1 + 0.00024n`. The price is capped at
2.5e181. Each 1000× of cash above the price skips one more life (up to 20), and every 2 skipped
lives give a shard (community, 2019). This turns surplus cash into value instead of waste.

### Multiplier curves: linear vs multiplicative

Effective grind for rebirth `k` ≈ `cost(k) / multiplier(k−1)`. Per rebirth, grind grows by `g` divided
by the multiplier's growth (inferred, follows from the formulas).

- **Linear** `m = 1 + a·n`: the multiplier's growth shrinks toward 1, so each rebirth costs nearly
  `g×` more grind than the last. Runs get long fast. Steal a Brainrot uses +1× per level (x1 at
  Rebirth 1 to x17 at Rebirth 17), with costs rising from $1M to about $500T by Rebirth 15, ~4× per
  level on average (press, 2025-11; average inferred). It relies on new brainrots and slots, not the
  multiplier alone, to carry the climb.
- **Multiplicative** `m = M^n`: grind grows by a constant `g/M` per rebirth. Set `g/M` between 1.1 and
  1.3 for slowly lengthening runs (inferred).

Worked example, `C0 = 10,000`, `g = 3` (inferred):

| Rebirth k | Cost | Linear m = 1+n: grind | Multiplicative m = 2.5ⁿ: grind |
|---|---|---|---|
| 1 | 10,000 | 10,000 | 10,000 |
| 2 | 30,000 | 15,000 | 12,000 |
| 3 | 90,000 | 30,000 | 14,400 |
| 4 | 270,000 | 67,500 | 17,280 |
| 5 | 810,000 | 162,000 | 20,736 |
| 6 | 2.43M | 405,000 | 24,883 |
| 7 | 7.29M | 1.04M | 29,860 |
| 8 | 21.9M | 2.73M | 35,832 |
| 9 | 65.6M | 7.29M | 42,998 |
| 10 | 197M | 19.7M | 51,598 |

The linear column is ~2,000× harder at rebirth 10. The multiplicative one is ~5×. Linear works only
if each rebirth also unlocks new content (zones, items, slots) that raises income on its own.
If in-run income grows with upgrades, real time grows more slowly than grind; playtest the times
(inferred).

### Time targets (inferred)

These come from the vault's session data: median session 15–25 min is the target and first
rewards must land before 3 minutes ([retention](../fundamentals/retention.md),
[discovery](../fundamentals/discovery-algorithm.md)). No source publishes rebirth timings.

| Milestone | Target active play | Why |
|---|---|---|
| Rebirth button and progress bar visible | ≤ 3 min | The goal exists before the bounce window closes |
| First rebirth | 8–15 min | Inside the first session, so the "faster second run" lands before they leave |
| Rebirths 2–5 | each 1.1–1.5× the previous | Rhythm without a wall |
| ~1 rebirth per session | days 2–7 | A session goal that fits the 60 min/day playtime cap |
| Second layer unlocks | day 3–7 | When single rebirths start to drag; a D8–28 goal |

### Multiple prestige layers

- Layer 2 costs a number of layer-1 rebirths (e.g., 10–25), resets rebirths **and** the run, and
  multiplies (not adds to) the layer-1 multiplier (inferred).
- Unlock a new layer when the grind ratio of layer 1 exceeds ~3× the first rebirth's time, not
  earlier. Players can't value a layer they never felt the need for (inferred).
- Give each layer a distinct reward type: layer 1 = income multiplier, layer 2 = new feature or
  zone, layer 3 = cosmetic or title (inferred; Pet Simulator 99's feature-unlock rebirths are a
  real example, unverified).
- Cap at 2–3 layers for a solo-dev game. Each layer adds a reset rule to test (inferred).

### UI that makes the trade obvious

- Rebirth panel shows three lists: **You lose** (cash 1.2M, 14 upgrades), **You keep** (pets, gems),
  **You gain** (income ×3 → ×4, +1 slot). Use exact numbers from replicated server values (inferred).
- Show progress toward the price as a bar and as "1.2M / 3M". Pulse the button when affordable
  (inferred). See [UI/UX](../fundamentals/ui-ux.md).
- First rebirth: show a one-time explainer and a confirm step. Later rebirths: a single press, and an
  optional auto-rebirth toggle once the player has rebirthed ~5 times (inferred).
- After the reset, show "income ×4 now" on the first earnings popups so the bonus is felt
  (inferred).
- Format numbers with suffixes; see [upgrade trees](upgrade-trees.md).

### Rebirth-skip products and fairness

- Grant every Robux rebirth product only inside `MarketplaceService.ProcessReceipt`, deduplicated by
  `PurchaseId` (official, 2026-10). See [monetization](../fundamentals/monetization.md).
- Prefer selling **speed** (2× cash for the run, auto-collect) over selling **rebirths**. A speed
  boost keeps the player in the loop; a bought rebirth skips the content they would play (inferred).
- If you sell rebirths, store `PaidRebirths` separately and rank leaderboards on earned rebirths or
  label paid ones. A buyable leaderboard drives off free players (inferred). See
  [leaderboards](leaderboards.md).
- Where rebirths affect other players (base lock time in steal games, PvP stats), don't sell them
  (inferred). See [base defense and stealing](base-defense-and-stealing.md).
- Never use fake urgency on rebirth offers (official, 2026-10; see retention anti-patterns).

## Implementation outline (server-authoritative)

- **Data model:** keep everything a rebirth wipes in one sub-table, `data.Run`, so the reset is one
  assignment from a template. Persistent fields sit at the top level: `Rebirths`, `Layer2`,
  `PaidRebirths`, `Gems`, `Pets`. Never save the multiplier; derive it from `Rebirths` in one
  shared function so it can't desync (inferred).
- **Remote:** one `RequestRebirth` RemoteEvent with no arguments (or a bulk count, validated as an
  integer 1–100). The server reads the price from its own data, never from the client. Run the
  full pipeline in [security](../fundamentals/security-and-anti-exploit.md): rate limit, loaded
  data, state checks.
- **Atomic step:** check price, then mutate, with no yield in between. Set a `Busy` flag during
  trades and pending purchases and refuse rebirths while it's set (inferred).
- **World cleanup:** destroy run-owned instances (plot buildings, droppers, tools) after the data
  change, then rebuild the starter state. See [conveyor and dropper economy](conveyor-dropper-economy.md).
- **Save right away** after a rebirth (ProfileStore `profile:Save()`), like a purchase. A crash
  must not undo it. See [player data](player-data.md).
- **Replicate:** set `Rebirths` and `Cash` as player attributes or leaderstats for the UI; the UI
  computes previews from those copies only.

```lua
--!strict
-- ServerScriptService/Rebirth: outline only, not drop-in
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local PlayerData = require(script.Parent.PlayerData) -- get(player): Data? (player-data.md)
local RateLimit = require(script.Parent.RateLimit)   -- token bucket per remote (security file)
local Economy = require(ReplicatedStorage.Shared.Economy) -- pure functions, safe to share

local RequestRebirth = ReplicatedStorage.Remotes.RequestRebirth :: RemoteEvent
local RebirthDone = ReplicatedStorage.Remotes.RebirthDone :: RemoteEvent

-- Economy.rebirthCost(n) = 10_000 * 3 ^ n ; Economy.multiplier(n) = 2.5 ^ n
local RUN_TEMPLATE = table.freeze({Cash = 0, Upgrades = {}, Zone = 1})

local function newRun()
	return {Cash = RUN_TEMPLATE.Cash, Upgrades = {}, Zone = RUN_TEMPLATE.Zone}
end

RequestRebirth.OnServerEvent:Connect(function(player: Player)
	if not RateLimit.take(player, "Rebirth") then return end
	local data = PlayerData.get(player)
	if not data or data.Busy then return end
	local price = Economy.rebirthCost(data.Rebirths)
	if not (data.Run.Cash >= price) then return end -- also false for NaN
	-- no yields between the check and the mutation
	data.Rebirths += 1
	data.Run = newRun()
	data.Run.Cash = Economy.startGrant(data.Rebirths) -- optional starting cash
	player:SetAttribute("Rebirths", data.Rebirths)
	PlayerData.saveSoon(player) -- ProfileStore: profile:Save()
	RebirthDone:FireClient(player, data.Rebirths)
	-- then: clear plot / tools for this player and respawn the starter kit
end)
```

## Common bugs and exploits

| Bug | Cause | Fix |
|---|---|---|
| Double rebirth for one price | Remote spam, or a yield between the price check and the reset | Rate limit; check and mutate in one synchronous block (official principle, 2026-10) |
| Free multiplier | Client sends its multiplier or rebirth count | Derive from server `Rebirths` only (official, 2026-10) |
| Rebirth undone after a crash | Saved only on the next autosave | Save immediately after the rebirth (inferred) |
| Field survives the reset | Reset code lists fields one by one and misses a new one | One `Run` sub-table replaced from a template (inferred) |
| Paid item wiped | Robux item stored inside `Run` | Robux grants live outside `Run`; reviewer checks the template (inferred) |
| Duplicate items across rebirth | Rebirth during a trade or an open purchase | `Busy` flag blocks rebirth (inferred) |
| `inf` cost or NaN cash | `g^n` overflows past ~1.8e308; NaN compares false | Cap `n`, check `math.isfinite`, or move to a big-number type ([upgrade trees](upgrade-trees.md)) |
| Lost surplus | Cash far above the price is wiped | Bulk rebirths, Miner's Haven-style skips, or show the waste in the confirm (community, 2019) |
| Leaderboard throttling | Writing `OrderedDataStore` on each rebirth | Write on leave and every few minutes ([player data](player-data.md)) |
| Auto-rebirth macros | Players script the button | Either offer an in-game auto toggle, or rate limit and treat it as allowed play. Miner's Haven's game page bans macro rebirthing (community, read 2026-10) |

## Checklist for agents

### Do
- Write the reset/persist table in the design doc before coding.
- Keep run state in one `Run` sub-table; derive multipliers from counts.
- Use `cost = C0 × g^n` with a multiplicative bonus and `g/M` of 1.1–1.3, or linear bonuses only
  if each rebirth also unlocks content.
- Target first rebirth at 8–15 min, visible from minute 3; playtest the times.
- Show lose/keep/gain with exact numbers and a progress bar.
- Save immediately after a rebirth; block it while trading or purchasing.
- Handle surplus cash (bulk rebirth or skips).

### Don't
- Don't reset anything bought with Robux.
- Don't accept a price, count or multiplier from the client.
- Don't sell rebirths that affect other players, or rank buyable rebirths without labeling them.
- Don't add a second prestige layer before the first one starts to drag.
- Don't let costs reach `inf`: plan the number range up front.

## Sources

1. https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i: exponential cost vs polynomial production, cost and bulk formulas (Pecorella, 2016-10)
2. https://www.gamedeveloper.com/design/the-math-of-idle-games-part-iii: prestige formulas for Realm Grinder, AdVenture Capitalist, Cookie Clicker, Egg, Inc.; earnings to double prestige (2017-02)
3. https://github.com/berezaa/minershaven: Miner's Haven source, Apache-2.0, released 2019
4. https://raw.githubusercontent.com/berezaa/minershaven/master/src/ReplicatedStorage/MoneyLib.lua: `RebornPrice`, `LifeSkips`, suffix table
5. https://raw.githubusercontent.com/berezaa/minershaven/master/src/ServerScriptService/Main/RebirthHandler.server.lua: what resets and persists, shards from skips
6. https://www.roblox.com/games/258258996/Miners-Haven-Sandbox-Tycoon: game rules banning macro rebirthing
7. https://beebom.com/steal-a-brainrot-rebirth-guide-levels-and-rewards/: Steal a Brainrot rebirth costs, multipliers, slots, lock time (updated 2025-11-24)
8. https://holdtoreset.com/pet-simulator-99-rebirth-system-explained/: Pet Simulator 99 zone-gated rebirths and rewards (unverified)
9. https://dungeonpath.com/posts/pet-simulator-99/rebirth-prestige-guide/: Pet Simulator 99 reset/keep table (unverified)
10. https://create.roblox.com/docs/production/analytics/retention: long-term goals as D30 hooks
11. https://create.roblox.com/docs/reference/engine/classes/MarketplaceService: ProcessReceipt for product grants

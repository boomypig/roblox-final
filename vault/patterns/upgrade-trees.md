---
title: Upgrade trees and cost curves
type: pattern
read-when: Adding upgrade paths, cost curves, or skill trees.
last-researched: 2026-10-22
---

# Upgrade trees and cost curves

## What it is

Upgrades turn currency into more earning power: buy a level, get more income, click power, speed
or storage. Costs grow exponentially per level while effects grow linearly or slowly, so each level
takes a bit longer than the last. Upgrades come as **linear lists** (one track per stat), **tiers**
(new generator types that cost ~10× more), or **branching trees** (prerequisites and choices).

## Why it works

- A constant stream of affordable next steps gives a goal every few seconds early on and every few
  minutes later (inferred).
- Exponential costs eventually outgrow any linear or polynomial production. That built-in slowdown is
  what lets one curve last hours instead of minutes, and what makes a
  [rebirth](rebirth-prestige.md) feel needed (community, 2016-10).
- Visible "almost affordable" prices keep players in the session for one more purchase (inferred).

## Genres that use it

[Simulator](../genres/simulator.md), [tycoon](../genres/tycoon.md),
[idle/incremental](../genres/idle-incremental.md), [+1 stat](../genres/plus-one-stat.md),
[job sims](../genres/job-sims.md), [tower defense](../genres/tower-defense.md) (tower upgrade paths),
[anime RPG](../genres/anime-rpg.md) and [battlegrounds](../genres/battlegrounds.md) (skill trees).

## Design rules

### Core formulas (community, 2016-10)

- Next level: `cost(k) = base × r^k`, where `k` is the number already owned.
- Production: `base_production × owned × multipliers`.
- Buying `n` at once: `base × r^k × (r^n − 1) / (r − 1)`.
- Most you can afford with cash `c`: `floor(log(c × (r − 1) / (base × r^k) + 1) / log(r))`.
- Milestones: the article's model doubles a generator's output at 25 and again at 50 owned.
  AdVenture Capitalist's first generator uses `r = 1.07`, base cost ~4, 1.67/s each.
- Cookie Clicker uses `r = 1.15` for every building, and 25% of the current price back on sale
  (community wiki). Each new building tier costs ~7–11× the last and produces ~5.5–10× more: costs
  15, 100, 1,100, 12,000, 130,000 for 0.1, 1, 8, 47, 260 per second (community wiki).

### Picking the growth rate

Cost of level L with `base = 10`, `cost = 10 × r^(L−1)`:

| Level | r = 1.07 | r = 1.15 | r = 1.25 |
|---|---|---|---|
| 1 | 10.0 | 10.0 | 10.0 |
| 2 | 10.7 | 11.5 | 12.5 |
| 3 | 11.4 | 13.2 | 15.6 |
| 4 | 12.3 | 15.2 | 19.5 |
| 5 | 13.1 | 17.5 | 24.4 |
| 6 | 14.0 | 20.1 | 30.5 |
| 7 | 15.0 | 23.1 | 38.1 |
| 8 | 16.1 | 26.6 | 47.7 |
| 9 | 17.2 | 30.6 | 59.6 |
| 10 | 18.4 | 35.2 | 74.5 |
| Sum of 1–10 | 138 | 203 | 333 |
| 25 | 50.7 | 286 | 2,118 |
| 50 | 275 | 9,431 | 560,510 |
| 100 | 8,118 | 10.2M | 39.3B |

With a linear effect of +1/s per level, the payback time of a level in seconds equals its cost.

Rules of thumb (inferred from the table and the shipped values above):
- **1.07–1.10** for main generators that players buy hundreds of.
- **1.12–1.20** for upgrade shops with tens of levels per stat.
- **1.5–3** for short tracks of 5–15 big upgrades (backpack size, new tool tier).
- **New tier ≈ 10× the cost, 5–8× the output** of the previous one, so a new tier is a step up in
  income but slightly worse per coin, and old tiers stay worth leveling.
- **Payback time** (`cost / Δincome`) should rise slowly: from seconds in minute 1 to a few minutes
  at the end of a run. When it passes ~5–10 minutes with nothing else to buy, the player needs a
  new tier, zone or rebirth (inferred).
- **Effect growth must stay below cost growth.** If an upgrade multiplies income by 1.1 per level
  and costs 1.08× more per level, it pays back faster each level and the curve runs away (inferred).

### Soft caps and hard caps (inferred)

- **Soft cap:** past a threshold `c`, an effect grows more slowly:
  `effect = x` if `x ≤ c`, else `c × (x / c)^p`, with `p` around 0.5. Use it for stacked
  multipliers that would otherwise explode (rebirth × pet × pass × event).
- **Saturating stats** (crit chance, cooldown cut, drop luck):
  `effect = max × (1 − e^(−k × level))`. The stat approaches `max` and never passes it.
- **Hard caps** where physics or fairness break: `Humanoid.WalkSpeed` high enough to skip map
  geometry or outrun streaming, percentages above 100%, cooldowns below the server tick.
- Show caps in the UI ("MAX" or "soft-capped: 50% effect"). Hidden caps read as bugs.

### Linear lists vs branching trees

| Use | When | Example |
|---|---|---|
| Linear list per stat | Simulators, tycoons, a young audience | Click power, walk speed, backpack |
| Tiers (new generators) | Idle and tycoon economies | Droppers 1–10 |
| Branching tree | Meaningfully different builds | Combat paths, tower upgrade paths, prestige shop |

- Show **3–5 affordable or nearly affordable choices** at a time. More at once slows young players
  down (inferred).
- A tree needs real trade-offs (playstyles). If every player buys every node, it's a list with
  extra UI; build the list (inferred).
- Prerequisites are data: `requires = {"speed_3"}`. Check them on the server.
- Offer a free or cheap respec on trees that lock choices (inferred).
- Prestige-shop nodes persist through rebirths; normal upgrades reset. See
  [rebirth and prestige](rebirth-prestige.md).

### Showing affordability

- Price text green when affordable and red when not; an "affordable" count badge on the shop
  button (inferred). See [UI/UX](../fundamentals/ui-ux.md).
- Show **time to afford**: `(cost − cash) / income` as "in 0:42" (inferred).
- Buy buttons ×1 / ×10 / Max, using the bulk and max-affordable formulas above. Show the bulk total
  before the click (inferred).
- Pop a short notice the first time a new tier becomes affordable (inferred).
- The client computes all of this from replicated cash and the shared config. It's display only.

### Big-number formatting

**Limits of Luau numbers (official, 2026-10):**
- Every number is a 64-bit double: range about ±1.7 × 10^308, about 15 significant digits.
- Integers above 2^53 (~9.0 × 10^15) aren't exact. Adding 1 to 10^17 does nothing, so per-click
  "+1" stops counting once balances pass ~9e15 (consequence inferred).
- `IntValue` holds a signed 64-bit integer, max 2^63 − 1 (~9.2 × 10^18). Leaderstats built on
  `IntValue` break first; use `NumberValue` or a `StringValue` with the formatted text.
- `OrderedDataStore` stores integers only (official, 2026-10). For huge stats, rank on
  `math.floor(math.log10(x) * 1000)` (inferred).
- Past ~1.8e308 a double becomes `inf`. A DevForum game broke at 1e308 in 2025, and replies pointed
  to big-number modules (community, 2025-06).

**Suffix format.** `string.format` supports `%d`, `%f`, `%e`, `%g` with width and precision, and no
thousands separator (official, 2026-10). Standard short scale: K (1e3), M, B, T, Qa (1e15), Qi, Sx,
Sp, Oc, No, Dc (1e33). Miner's Haven's open-source formatter has 61 suffixes and falls back to the
plain number past them (community, 2019). Past ~1e36, switch to `1.23e45`. Incremental players read
it fine, and long suffix lists don't (inferred).

```lua
--!strict
-- ReplicatedStorage/Shared/Format: outline only
local SUFFIXES = {"", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc"}

local function format(n: number): string
	if n ~= n then return "0" end                      -- NaN
	if n == math.huge then return "∞" end
	local sign = if n < 0 then "-" else ""
	n = math.abs(n)
	if n < 1000 then return sign .. tostring(math.floor(n)) end
	local tier = math.floor(math.log10(n) / 3)
	local m = math.floor(n / 10 ^ (tier * 3) * 100) / 100 -- truncate, never round up
	if m >= 1000 then m, tier = m / 1000, tier + 1 end   -- float edge at tier boundary
	if tier >= #SUFFIXES then return sign .. string.format("%.2e", n) end
	return sign .. (string.format("%.2f", m):gsub("%.?0+$", "")) .. SUFFIXES[tier + 1]
end

return format
```

- **Truncate balances, round prices up.** Rounding 999,999 up to "1M" next to a 1M price makes a
  player think they can afford it (inferred).
- Show full digits with separators below 1M in shop prices if space allows (inferred).

**When to switch to mantissa/exponent** (inferred unless noted):
- Stay on doubles if the design tops out below ~1e300. Plan the curve: `10 × 3^n` reaches 1e308 at
  `n ≈ 640`; layered rebirths can reset magnitudes instead.
- Switch when content past ~1e300 is planned. Store `{m: number, e: number}` with `1 ≤ m < 10`;
  multiply = multiply `m`, add `e`; add = align exponents, and ignore the smaller term when
  exponents differ by more than ~17.
- Community libraries: EternityNum, InfiniteMath, OmegaNum (community, 2025-06); GammaNum, which
  claims 30–100× faster than EternityNum (community, 2025); BigNumber, whose docs warn it isn't
  for per-frame math (community, 2025). Pick one at the start: retrofitting means changing every
  economy script (community, 2025-06).
- Save big numbers as a `{m, e}` table or a string. DataStores reject NaN ([player data](player-data.md));
  never save `inf` either (inferred).

## Implementation outline (server-authoritative)

- **Data:** `Upgrades: {[string]: number}` (upgrade ID → level) in the player's save. IDs are stable
  strings; renaming one needs a migration ([player data](player-data.md)).
- **Config:** one module with `base`, `r`, `maxLevel`, `requires`, `effect`. Formulas can live in a
  shared module so the UI matches. Exploiters can read it, but the server's copy is authoritative.
  Keep secret values (unpublished odds) server-only, as the
  [security](../fundamentals/security-and-anti-exploit.md) file says.
- **Derived stats:** compute income, click power and speed from levels in one function, and cache
  the result after each purchase. Never save derived stats.
- **Remote:** `RequestUpgrade(upgradeId: string, count: number)`. Run the validation pipeline: rate
  limit, types, integer count 1–100, known ID, prerequisites, level cap, server-computed cost.

```lua
--!strict
-- ServerScriptService/Upgrades: outline only, not drop-in
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local PlayerData = require(script.Parent.PlayerData)
local RateLimit = require(script.Parent.RateLimit)
local Config = require(ReplicatedStorage.Shared.UpgradeConfig) -- {[id]: {base, r, maxLevel, requires}}
local Stats = require(script.Parent.Stats)                        -- recompute(player, data)

local RequestUpgrade = ReplicatedStorage.Remotes.RequestUpgrade :: RemoteEvent

local function bulkCost(u, owned: number, n: number): number
	return u.base * u.r ^ owned * (u.r ^ n - 1) / (u.r - 1)
end

RequestUpgrade.OnServerEvent:Connect(function(player: Player, id: unknown, count: unknown)
	if not RateLimit.take(player, "Upgrade") then return end
	if typeof(id) ~= "string" or #id > 32 then return end
	if typeof(count) ~= "number" or count % 1 ~= 0 or count < 1 or count > 100 then return end
	local u = Config[id]
	local data = PlayerData.get(player)
	if not u or not data then return end
	for _, req in u.requires do
		if (data.Upgrades[req] or 0) < 1 then return end
	end
	local owned = data.Upgrades[id] or 0
	local n = math.min(count, u.maxLevel - owned)
	if n < 1 then return end
	local cost = bulkCost(u, owned, n)
	if not (math.isfinite(cost) and data.Cash >= cost) then return end -- NaN-safe
	data.Cash -= cost
	data.Upgrades[id] = owned + n
	Stats.recompute(player, data)
end)
```

## Common bugs and exploits

| Bug | Cause | Fix |
|---|---|---|
| Free purchase | `if cash < cost then return end` with `cost = NaN` passes, because NaN fails every comparison | Write `if not (cash >= cost)` and check `math.isfinite` (official NaN behavior, 2026-10) |
| Price from the client | Remote accepts a cost | Cost only from server config and server level (official, 2026-10) |
| Prerequisite skipped | Only the UI hides locked nodes | Check `requires` on the server |
| Negative or fractional count | No integer and range check | `count % 1 == 0`, clamp 1–100 |
| Runaway income | Effect growth ≥ cost growth, or stacked multipliers | Effect growth below cost growth; soft cap stacks (inferred) |
| "1000K" shown | Rounding carries over a tier boundary | Re-check the mantissa after rounding (inferred) |
| "Can afford" lies | UI rounds the balance up | Truncate balances, round prices up (inferred) |
| Leaderstat stuck or wrong | `IntValue` past 2^63 − 1, or `+1` lost above 2^53 | `NumberValue`/`StringValue`; big-number type if needed (official limits) |
| Save fails or corrupts | `inf` or NaN in data | Validate before save ([player data](player-data.md)) |
| Old saves break | Upgrade ID renamed | Stable IDs, migrations |

## Checklist for agents

### Do
- Use `cost = base × r^owned` with `r` from the table above; compute bulk and max with the closed
  forms.
- Keep effect growth below cost growth; soft-cap stacked multipliers.
- Show green/red prices, time to afford, ×1/×10/Max, and an affordable-count badge.
- Store levels by stable string ID; derive stats on the server.
- Format with suffixes; truncate balances; switch to e-notation past the suffix list.
- Decide doubles vs mantissa/exponent before writing the economy.

### Don't
- Don't accept costs, levels or effects from the client.
- Don't build a branching tree when every player buys every node.
- Don't hide caps.
- Don't use `IntValue` for currencies that can pass ~9.2e18.
- Don't compare with `<` alone where NaN can appear.

## Sources

1. https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i: cost, production, bulk and max-affordable formulas; AdVenture Capitalist 1.07, milestones (2016-10)
2. https://cookieclicker.wiki.gg/wiki/Building: 1.15 price growth, 25% sell-back, building costs and CpS
3. https://create.roblox.com/docs/luau/numbers: double precision, ±1.7e308, ~15 digits
4. https://create.roblox.com/docs/reference/engine/classes/IntValue.md: int64 range, precision loss above 2^53
5. https://create.roblox.com/docs/reference/engine/libraries/string.md: `string.format` specifiers, precision, no thousands separator
6. https://create.roblox.com/docs/scripting/security/client-server-boundary: NaN fails comparisons; `math.isfinite`
7. https://create.roblox.com/docs/reference/engine/classes/OrderedDataStore: integer-only values
8. https://raw.githubusercontent.com/berezaa/minershaven/master/src/ReplicatedStorage/MoneyLib.lua: Miner's Haven suffix table and formatter (2019)
9. https://devforum.roblox.com/t/how-do-i-shorten-this-numbers/741957: suffix formatting with `math.log10` and `string.format` (2020–2025)
10. https://devforum.roblox.com/t/after-1e308-leaderstat-game-breaks/3740242: game broke at 1e308; library suggestions (2025-06)
11. https://devforum.roblox.com/t/gammanum-up-to-100x-faster-than-eternitynum/3906397: GammaNum speed claim
12. https://devforum.roblox.com/t/bignumber-scalable-math-system-for-huge-numbers-in-roblox/4039476: mantissa/exponent module, per-frame warning
13. https://devforum.roblox.com/t/abhis-number-abbreviation-system/698058: truncating abbreviation

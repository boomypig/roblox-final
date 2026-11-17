---
title: Rarity tiers and eggs
type: pattern
read-when: Adding eggs, gacha rolls, rarity tiers, or odds.
last-researched: 2026-10-22
---

# Rarity tiers and eggs

## What it is

The player spends currency on a container (egg, crate, spin) and the **server** picks one outcome
from a weighted table. Outcomes are grouped into named, color-coded tiers. The client only plays
a reveal for a result the server has already decided and saved in memory. Pets that come out are
covered in [pets and companions](pets-companions.md); storing them in [inventory](inventory.md).

## Why it works

- Variable rewards: an unknown outcome on every hatch keeps the next hatch interesting long after
  the reward itself stops mattering (inferred).
- Tiers turn a number (0.2%) into a status symbol (an orange "Legendary" label) that other players
  can read at a glance (inferred).
- Rare hatches are social moments. A server-wide "X hatched a SECRET (0.01%)" makes everyone else
  want to hatch, and it's clip material (inferred; see
  [social and virality](../fundamentals/social-and-virality.md)).
- Collections give a long-term goal: "2 more to complete the set" (official guidance on goals,
  see [retention](../fundamentals/retention.md)).

## Genres that use it

[Pet and egg collection](../genres/pet-egg-collection.md), [simulator](../genres/simulator.md),
[RNG aura](../genres/rng-aura.md), [gacha raid](../genres/gacha-raid.md),
[tower defense](../genres/tower-defense.md) (unit summons), [steal-a-x](../genres/steal-a-x.md)
(Steal An Egg combines stealing with hatching, see
[trend lifecycle](../fundamentals/trend-lifecycle.md)), [fishing](../genres/fishing.md) (catch
rarity), [farming](../genres/farming-growing.md) (seed and pet rarity).

## Design rules

### Tier ladders in shipped games

| Game | Tiers, low → high | Source |
|---|---|---|
| Pet Simulator 99 | Basic `#9491A7`, Rare `#71FF3E`, Epic `#29E2FF`, Legendary `#FF8522`, Mythical `#FF2B64`, Exotic `#FF1DFB`, Divine `#FFEC58`, Superior `#C3FFFF`, Celestial `#BBC4FF`; off-ladder: Exclusive `#D24AFF`, Secret `#AD4FFF`, Event `#FFA032`. Only Exotic and above (plus Exclusive/Secret) are flagged `Announce = true`. | community: BIG Games public API, read 2026-10-22 |
| Adopt Me! | Common, Uncommon, Rare, Ultra-Rare, Legendary | press, 2026 guides |

Conventions a player already knows (inferred from the above and genre norms):
- Gray → green → blue/cyan → purple → orange/gold → red/pink → rainbow or animated gradient.
  Keep that order; players read color before text.
- Ship **5 tiers** at launch (Common, Uncommon, Rare, Epic, Legendary) plus one hidden chase tier
  (Mythic or Secret) added in the first big update. More tiers dilute meaning; fewer leave no
  chase (inferred).
- Off-ladder labels (Exclusive = from a Robux egg, Event = time-limited, Secret = hidden odds
  tier) are separate tags, not steps on the ladder (PS99 data shows this split; inferred).
- Always pair color with the tier name as text, so color-blind players can read it (inferred).
- Variants (Golden, Shiny, Rainbow) are a **second, independent roll** layered on the pet roll.
  PS99 eggs carry their own `goldChance`, `shinyChance` and `rainbowChance` fields
  (community, API 2026-10-22). This multiplies collection goals without new models.

### Odds ladders that ship

| Egg type | Weights per pet, common → rarest | Source |
|---|---|---|
| PS99 grind egg (coins) | 70 / 29 / 1 / 0.1 / 0.002, some add 0.00004 | community, API 2026-10-22 |
| PS99 Robux "Exclusive" egg | 50 / 35 / 13 / then Huge pets at 1.5 and 0.5 (one adds a Titanic at 0.05) | community, API 2026-10-22 |
| Adopt Me! Royal Egg (premium) | Common 0, Uncommon 25, Rare 37, Ultra-Rare 30, Legendary 8 | press, 2026 (several guides agree) |

What the data shows (inferred):
- Grind eggs: two filler outcomes take ~99%. Above that, each step is 10–50× rarer than the
  previous one. The top of the ladder is effectively a lottery that keeps whales and clips busy.
- Premium eggs drop the bottom tier and give the chase tier a ~2–8% chance. Paid eggs must feel
  much better per open than grind eggs.
- PS99's weights don't always sum to 100 (one egg sums to ~100.1, another uses `1` per pet).
  They are relative weights, so chance = weight / total. **Your displayed odds must be the
  normalized percentages** (official disclosure rule below).

### Worked example: a launch egg

Integer weights out of 1,000,000 (use integers so the displayed % is exact and sums to 100%):

| Tier | Weight | Chance | Expected hatches to first | 95% of players have one by |
|---|---|---|---|---|
| Common | 600,000 | 60% | 1.7 | 4 |
| Uncommon | 280,000 | 28% | 3.6 | 10 |
| Rare | 100,000 | 10% | 10 | 29 |
| Epic | 18,000 | 1.8% | 56 | 165 |
| Legendary | 2,000 | 0.2% | 500 | 1,497 |

- Math: chance of at least one in `n` hatches is `1 - (1 - p)^n`. At `p = 0.002`, 500 hatches give
  63%, 1,500 give 95%, and the unluckiest 1% of players need 2,300+ hatches (inferred: arithmetic).
- That long tail is why pity exists: a cap at 1,000 hatches catches the ~14% of players who'd
  otherwise wait longer, without changing the odds for anyone else (inferred).
- **Tune time, not odds.** Time to a tier = expected hatches × time per hatch. Time per hatch is
  set by egg price ÷ income per minute. Changing price later is invisible; changing displayed odds
  is not (inferred).
- Target pacing (inferred, test with [analytics](../fundamentals/analytics.md)): first Rare in the
  first 5 minutes, first Epic in session 1, first Legendary around day 2–4, chase tier as a
  multi-week goal. Each new zone's egg should make the last zone's Legendary the new Common-ish
  power level.

### Luck multipliers

- Apply luck to tiers at or above a threshold (e.g. Epic+), and take the extra weight from the most
  common outcome. Example: luck ×2 on the egg above → Common 58%, Epic 3.6%, Legendary 0.4%
  (inferred).
- Stack luck sources **additively** (+100% potion + 50% pass = ×2.5) and cap the total (e.g. ×3),
  or stacks run away fast. Clamp so the common tier never goes negative (inferred).
- If any luck source is bought with Robux, it's a paid "probability modifier": you must explain the
  boost numerically before purchase and show the player's **actual current odds** while it's
  active (official, 2026-10). So the odds UI always shows post-luck numbers.

### Pity

- Counter per player per egg (or per banner), saved in player data. Miss → +1. Hit the pity tier
  naturally or by pity → reset to 0. At the threshold, the roll is restricted to pity-tier entries
  (weighted among themselves) (inferred).
- Show the counter: "Legendary guaranteed in 37 hatches". A hidden pity has no retention value
  (inferred).
- Set the threshold at ~2× the expected hatches (1,000 for a 0.2% tier). Lower thresholds turn
  the tier into a fixed price (inferred).
- Soft pity (odds ramp after N) is fine but harder to disclose; for Robux eggs pity is a
  probability modifier and must be disclosed numerically (official, 2026-10).
- Real example: Anime Warriors 2 guarantees a Legendary at 500 spins and a Mythical at 10,000
  (press, guide; unverified).

### Hatch reveal pacing (client only; the server already decided)

Use [game feel](../../.claude/skills/roblox-vfx/references/game-feel.md)'s reveal row: egg shakes faster over 0.8–1.5 s,
white flash, rarity-colored burst, pet pops in with name in tier color. Common ≤ 1 s total,
Legendary 2–3 s, tap to skip.

- Show the **tier color first** (flash), then the pet. The color is the payoff; the pet confirms it
  (inferred).
- Scale spectacle with tier: Common = no screen shake, no sound sting beyond a pop; Legendary+ =
  dimmed screen, rays, fanfare, server announcement (inferred).
- Never fake a near miss (a wheel creeping past Legendary to stop on Common) (inferred; see below).
- Announce only the top 2–3 tiers server-wide (PS99 announces Exotic+, community 2026-10). Use
  `TextChannel:DisplaySystemMessage` on each client after the server fires the event (official API).

### Multi-hatch and auto-hatch

- Offer 1 / 3 / 8 at once (common genre ladder, inferred). Show multi results as a grid revealing
  together, with the rarest one highlighted last (inferred).
- Multi-hatch and auto-hatch are the classic game passes for this genre (inferred). Check passes
  on the server with `MarketplaceService:UserOwnsGamePassAsync` and store the unlocked max in
  session data.
- Auto-hatch: the client sends `SetAutoHatch(eggId, on)`; the **server** runs the loop at a fixed
  cadence and re-checks distance, currency and space each cycle. Stop on leave, on moving away,
  or when inventory is full (inferred).
- Offer an "auto-delete by tier" filter (e.g. skip Commons) applied on the server at hatch time,
  so auto-hatch doesn't fill storage with junk (inferred).

### Odds disclosure and country gating (paid random items)

Full rules: [monetization](../fundamentals/monetization.md#paid-random-items-eggs-crates-spins-luck-boosts-pity).
Egg-specific must-dos (official, 2026-10 unless tagged):
- **Scope trap:** an egg priced in a currency that can be bought with Robux *anywhere* in your game
  is a paid random item, even if most players earn that currency. Design default: price eggs in
  earn-only soft currency, and sell passes, boosts and direct items for Robux (inferred).
- Show every outcome's % before purchase, summing to 100%. Round long decimals to at least four
  digits past the first non-zero digit, with a "probabilities are rounded" disclaimer. Showing
  "1 in 500" is fine as extra text, never instead of the %.
- Odds billboard over the egg in the world, plus a button labelled "Info" or "Details" for long
  lists. A bare (i) icon doesn't count.
- If a player can win an outcome only once, update their remaining odds.
- Earn-only eggs (no Robux path) don't need disclosure. Show odds anyway: players expect it and it
  makes clips readable (inferred).
- Gate with `PolicyService:GetPolicyInfoForPlayerAsync(player)` (server, in `pcall`). If
  `ArePaidRandomItemsRestricted` is true: free/earnable path, disclosed fixed order, direct
  purchase priced at expected value, hide, block with a message, or keep them out of the area.
  Treat a failed call as restricted (inferred). Players under 18 in Brazil can't access paid
  random items (official, help center 2026).
- Whether a Robux luck potion applied to a free egg must also be blocked for restricted players
  isn't stated (unverified). Block it to be safe (inferred).
- Declare paid random items in the maturity questionnaire
  ([metadata](../fundamentals/metadata-thumbnails-icons.md#maturity--compliance-questionnaire)).
- Every outcome must benefit the player; no "nothing" result and no wagering (official, Community
  Standards via monetization file).

### What feels exploitative to kids (reviewer: reject these)

- Near-miss reveals, fake slowdowns, or showing the Legendary you "almost" got (inferred).
- A purchase prompt right after a bad hatch, or Robux eggs pushed before the free egg is tried
  (inferred).
- Chase pets that are only in Robux eggs and decide PvP or stealing outcomes (see monetization).
- Odds that differ from what's shown, hidden boosts, silent odds changes mid-event (official rule
  on actual odds; inferred on silence).
- Countdown "last chance" eggs that come back unchanged next week (official honest-presentation
  rule, 2026-10).
- Pity counters that reset on event end or logout without saying so up front (inferred).
- Currency packs sized so leftovers never buy a whole egg (inferred).

## Implementation outline (server-authoritative)

- **Config:** `ServerStorage/Config/Eggs` module: per egg `price`, `currency`, `pos`, ordered
  `entries {petId, tier, weight}` (most common first), `luckFromTier`, optional `pityTier`,
  `pityAt`. The server sends display odds (already luck-adjusted) to the client through a remote,
  so shown odds and rolled odds come from one table (inferred; see
  [security](../../.claude/skills/roblox-code/references/security.md#where-code-and-data-live)).
- **RNG:** one `Random.new()` per server. With no seed it uses an internal entropy source
  (official). `NextInteger(min, max)` is inclusive of both ends; `NextNumber()` is also inclusive
  of 0 and 1 (official), so prefer integer weights with `NextInteger(1, total)`.
- **Remotes:** `RequestHatch(eggId: string, count: number)` (C→S), `SetAutoHatch(eggId, on)`
  (C→S), `HatchResult(eggId, results)` (S→C), `GetEggOdds(eggId)` (C→S invoke, returns display
  table). Run the full [validation pipeline](../../.claude/skills/roblox-code/references/security.md#remote-validation-pipeline).
- **Data:** `Pity: {[eggId]: number}`, `Luck` sources with expiry timestamps, pets added through
  [inventory](inventory.md) with GUIDs.
- **Robux eggs:** roll inside `MarketplaceService.ProcessReceipt`, record the `PurchaseId` in the
  same save, return `PurchaseGranted` only after the save, then fire the reveal
  ([player data](player-data.md#related-systems)). Revealing before the save risks showing a
  Legendary that a crash rolls back (inferred).

```lua
--!strict
-- ServerScriptService/EggServer: outline only. Rate limiting and auto-hatch omitted.
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")
local PlayerData = require(script.Parent.PlayerData) -- get(p) -> Data?, canSave(p) -> boolean
local Inventory = require(script.Parent.Inventory)   -- addPet(player, data, petId, tier) -> string? (GUID)
local Eggs = require(ServerStorage.Config.Eggs)

type Entry = {petId: string, tier: number, weight: number} -- integer weights, most common first
type Egg = {price: number, pos: Vector3, entries: {Entry}, luckFromTier: number, pityTier: number?, pityAt: number?}

local RequestHatch = ReplicatedStorage.Remotes.RequestHatch :: RemoteEvent
local HatchResult = ReplicatedStorage.Remotes.HatchResult :: RemoteEvent
local rng = Random.new() -- once per server; never Random.new(os.time()) per call
local COUNTS = {[1] = true, [3] = true, [8] = true}
local lastHatch: {[Player]: number} = {}

local function weightsFor(egg: Egg, luck: number): {number}
	local w, extra = {}, 0
	for i, e in egg.entries do
		w[i] = if e.tier >= egg.luckFromTier then math.floor(e.weight * luck) else e.weight
		extra += w[i] - e.weight
	end
	w[1] = math.max(w[1] - extra, 0) -- keep the total fixed; luck cap keeps this positive
	return w
end

local function pick(egg: Egg, w: {number}, minTier: number): number
	local total = 0
	for i, x in w do if egg.entries[i].tier >= minTier then total += x end end
	local r = rng:NextInteger(1, total) -- inclusive
	for i, x in w do
		if egg.entries[i].tier >= minTier then
			r -= x
			if r <= 0 then return i end
		end
	end
	return #w
end

RequestHatch.OnServerEvent:Connect(function(player: Player, eggId: unknown, count: unknown)
	if typeof(eggId) ~= "string" or typeof(count) ~= "number" or not COUNTS[count] then return end
	local egg: Egg? = Eggs[eggId]
	local data = PlayerData.get(player)
	if not egg or not data or not PlayerData.canSave(player) or count > data.MaxHatch then return end
	local now = os.clock()
	if now - (lastHatch[player] or 0) < 1 then return end -- server cooldown ≈ shortest reveal
	local char = player.Character
	local root = if char then char:FindFirstChild("HumanoidRootPart") :: BasePart? else nil
	if not root or (root.Position - egg.pos).Magnitude > 12 then return end
	local cost = egg.price * count
	if data.Coins < cost or data.PetCount + count > data.PetCap then return end
	lastHatch[player] = now
	-- No yields below: charge, roll and grant happen as one step.
	data.Coins -= cost
	local w = weightsFor(egg, math.clamp(data.Luck, 1, 3))
	local results = {}
	for _ = 1, count do
		local pity = (data.Pity[eggId] or 0) + 1
		local forced = egg.pityAt ~= nil and egg.pityTier ~= nil and pity >= egg.pityAt
		local e = egg.entries[pick(egg, w, if forced then egg.pityTier :: number else 0)]
		data.Pity[eggId] = if egg.pityTier and e.tier >= egg.pityTier then 0 else pity
		local uid = Inventory.addPet(player, data, e.petId, e.tier)
		table.insert(results, {uid = uid, petId = e.petId, tier = e.tier, pity = forced})
	end
	HatchResult:FireClient(player, eggId, results) -- client animates; it never chose anything
end)
```

## Common bugs and exploits

| Bug | Cause | Fix |
|---|---|---|
| Client picks the pet | `math.random` in a LocalScript, server trusts the reported result | Server rolls; client only receives results (official principle) |
| Identical rolls | `Random.new(os.time())` per call: same seed within a second, same outcome | One `Random.new()` per server (official API; inferred bug) |
| Off-by-one weights | `NextNumber() * total` with `<` checks; `NextNumber` is inclusive of 1 | Integer weights + `NextInteger(1, total)`; fall back to the last entry (official API) |
| Shown odds ≠ real odds | Client config copy drifts, or luck isn't applied to the display | Server generates the display table from the roll table (inferred) |
| Double spend or free hatch | Handler yields between check and charge; two requests interleave | No yields between check, charge and grant (inferred) |
| Hatch with full inventory | Space checked after charging | Check `PetCount + count <= PetCap` before charging (inferred) |
| Auto-hatch spam | Client loop fires faster than reveals | Server cooldown per player; server-run auto loop (official rate-limit guidance) |
| Pity lost or duped | Pity stored in a separate key or only in memory | Pity lives in the same profile as pets and coins (inferred; see [player data](player-data.md)) |
| Robux egg re-roll | Receipt retried after a failed save rolls again | Dedup by `PurchaseId` in the same save (official) |
| Restricted player buys a paid egg | No PolicyService check, or a failed check treated as allowed | Check at join in `pcall`; failure = restricted (official + inferred) |

## Checklist for agents

- [ ] Tiers: 5 at launch + one chase tier; color order gray → green → blue → purple → gold → red → rainbow; name shown with color.
- [ ] Integer weights in one server-side table; displayed % generated from it, luck applied, sums to 100%.
- [ ] One `Random.new()` per server; `NextInteger(1, total)`; no client RNG.
- [ ] Hatch handler: types, allowed counts, distance, data loaded and saveable, currency, space, cooldown, then charge + roll + grant with no yields.
- [ ] Pity counter saved in the profile, shown in UI, threshold ~2× expected hatches.
- [ ] Luck sources additive and capped; Robux luck shows exact boosted odds.
- [ ] Reveal is client-only, tier color first, Common ≤ 1 s, Legendary 2–3 s, skippable; top tiers announced.
- [ ] Eggs priced in earn-only currency unless you implement full paid-random-item compliance.
- [ ] Paid eggs: odds before purchase, "Info"/"Details" button, PolicyService gate, roll in `ProcessReceipt` with `PurchaseId` dedup, questionnaire updated.
- [ ] No near misses, no post-loss purchase prompts, no fake urgency.

## Sources

1. https://create.roblox.com/docs/production/monetization/paid-random-items: scope (capsule, enhancement, combination, probability modifiers), % odds summing to 100, rounding disclaimer, Info/Details button, boosted odds, once-only outcomes, six treatments for restricted players, paid item trading
2. https://create.roblox.com/docs/reference/engine/classes/PolicyService.md: `GetPolicyInfoForPlayerAsync` keys, `pcall` requirement, client local-player only, 100 concurrent call limit
3. https://create.roblox.com/docs/reference/engine/datatypes/Random.md: entropy seed when omitted, `NextInteger` and `NextNumber` inclusive ranges, `Shuffle`, `Clone`
4. https://ps99.biggamesapi.io/api/collection/Rarity: Pet Simulator 99 tier names, numbers, colors, Announce flags (read 2026-10-22)
5. https://ps99.biggamesapi.io/api/collection/Eggs: Pet Simulator 99 egg weights, variant chance fields, Exclusive egg odds (read 2026-10-22)
6. https://www.sportskeeda.com/roblox-news/5-best-eggs-roblox-adopt-me: Adopt Me Royal Egg 8% Legendary, no Commons
7. https://allthings.how/adopt-me-royal-fairytale-egg-guide-pets-and-hatch-odds/: Adopt Me tier names and Royal Egg breakdown
8. https://deltiasgaming.com/?p=270167: Anime Warriors 2 pity thresholds (guide; unverified)
9. https://create.roblox.com/docs/reference/engine/classes/MarketplaceService: ProcessReceipt, UserOwnsGamePassAsync
10. https://create.roblox.com/docs/reference/engine/classes/TextChannel: DisplaySystemMessage for announcements

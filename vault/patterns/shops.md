---
title: Shops
type: pattern
read-when: Adding an in-game shop (soft or Robux currency).
last-researched: 2026-10-22
---

# Shops

## What it is

A place where players swap currency for items. There are two kinds, and they follow different
rules:

- **Soft-currency shops** sell for earned currency. The server validates and charges.
- **Robux shops** show developer products and passes. Roblox charges, and the server grants in
  the receipt handler.

Many soft shops **restock on a timer** with limited stock (Grow a Garden's seed stand). Some
make the shop a live event: Steal a Brainrot's item belt spawns weighted random items that
anyone can buy as they walk by. Receipts, pricing and honest-presentation rules live in
[monetization](../fundamentals/monetization.md). Card layout and modal rules live in
[UI/UX](../fundamentals/ui-ux.md). This file covers the shop systems themselves.

## Why it works

- **A shop turns earning into choosing.** Currency only matters if there's something to
  want, and a visible shelf of unaffordable items is a goal (inferred).
- **Restocks are appointments.** "New stock in 2:41" gives a reason to stay, or to come back,
  without punishing anyone for missing it, as long as the stock is fair (inferred).
- **Limited stock makes rare items feel found, not just bought.** Chancing on a rare seed in
  stock is a small RNG win each cycle (inferred).
- **Robux items in context sell better than a menu.** Roblox's "right item, right time" guide
  names pre-play shops (Doors' pre-run elevator shop), intermission offers (Dress to Impress),
  lobby displays, complementary items and UI cues (official, 2026-10).

## Genres that use it

Nearly all. Restocking soft shops are central to [farming-growing](../genres/farming-growing.md)
(Grow a Garden (case study: grow-a-garden)), [pet-egg](../genres/pet-egg-collection.md)
and [steal-a-x](../genres/steal-a-x.md). Upgrade shops drive [simulator](../genres/simulator.md)
and [tycoon](../genres/tycoon.md). Pre-run shops suit [horror](../genres/horror.md) runs and
[round-based](../genres/round-based-races-and-survival.md) games.

## Design rules

### Soft shop vs Robux shop

| | Soft-currency shop | Robux shop |
|---|---|---|
| Where | In the world (an NPC stand with a `ProximityPrompt`) and/or a HUD tab | HUD Shop button, plus Roblox's own Shop surface in the menu |
| Who charges | Your server, from saved currency | Roblox's purchase prompt; you grant in `ProcessReceipt` |
| Stock | Can restock and be limited | Should not be limited or timed unless it's real (honest-presentation rules) |
| Prices | Server catalog | Read live with `MarketplaceService:GetProductInfoAsync`, never hard-coded |
| Confirm | One tap; a confirm step only for expensive or rare buys | Roblox's prompt *is* the confirm. No extra guilt screen |

- Keep them visually distinct. Robux buttons get the Robux glyph and a different color, and
  never sit where a soft-currency button used to be. Accidental Robux spends by children are
  the worst shop bug you can ship (inferred).
- Don't hide prices behind a premium currency. If you sell gems for Robux, show what the gem
  item costs in Robux. A University of Sydney study flagged currency layers that hide real
  prices (press, 2026-05; see [monetization](../fundamentals/monetization.md)).
- Keep Roblox's Shop surface on (`Enum.CoreGuiType.ExperienceShop`), and turn on its global
  Shop button in Creator Hub. It's off by default, and Roblox recommends enabling it
  (official, 2026-10).
- **Listed vs unlisted products** (official, 2026-10):
  - A *listed* developer product appears in the Roblox Shop and may appear on the game page.
  - An *unlisted* one is purchasable only through your own prompts. Unlist items that make
    sense only in context, such as revives, restocks and trap refills.
  - Passes are always listed.

### Layout that converts without nagging

- Follow [UI/UX shop rules](../fundamentals/ui-ux.md): one Shop button, card = icon, name, one
  benefit line, price and one CTA, best value enlarged, no pop-up in the first 3 minutes, one
  modal at a time, "Not now" always visible.
- Soft shop order: affordable and new items first, then the next one to save for. Show "Need
  1,250 more" instead of a grey button. A goal reads better than a refusal (inferred).
- Put the restock countdown on the stand itself and in the open shop, so players learn the
  rhythm without opening a menu (inferred).
- Contextual Robux offers (official guide, 2026-10):
  - Offer them at natural pauses: before a run, at intermission, when out of a consumable.
  - Explain the benefit in one line, as Doors' pre-run shop does.
  - Limit how often complementary prompts appear, and bundle items instead of chaining prompts.
  - Allow for the "buy Robux" flow taking several seconds. If play can't pause, don't offer
    in-play.
- Log the funnel per shop open: opened → viewed item → prompted → granted, with
  `AnalyticsService:LogFunnelStepEvent`. Log each soft purchase with `LogEconomyEvent`
  (transaction type `Shop`) and each Robux grant with `IAP` or `ContextualPurchase` (official
  API; see [analytics](../fundamentals/analytics.md)).

### Restocking shops

| Reference | Cadence | Stock model |
|---|---|---|
| Grow a Garden seed shop | Every 5 min; Daily Deals every 24 h | Same stock on every server. A purchase counts only against the buyer's own stock. A Robux restock costs 79 Robux per purchase (community wiki, 2026-10) |
| Grow a Garden gear shop | Every 5 min | Same across servers; staple items are always in stock (community wiki, 2026-10) |
| Grow a Garden egg shop | Every 30 min | Has a Robux "refresh now" stand (community wiki, 2026-10) |
| Steal a Brainrot belt | Continuous spawns | Weighted random items per server. Another player can buy an item walking to its owner for 150% of its price. Rare spawns are announced (community wiki, 2026-10) |

- **Derive stock from the clock, not from messages.**
  - `cycle = math.floor(os.time() / PERIOD)` gives every server the same cycle number, and
    `os.time()` defaults to UTC (official).
  - Seed a generator from `cycle`, a per-shop salt and the catalog version. Every server then
    rolls the same stock with no DataStore, MessagingService or "leader" server.
  - DevForum developers use this time-bucket seed for global rotations (community, 2025).
  - That `Random.new(seed)` repeats the same sequence for the same seed and call order is
    community-established, not stated on the reference page (unverified). For a hard
    guarantee, write a small integer hash in Luau (inferred).
- **Roll in a fixed order** over an *array* sorted by item id. Draw the same number of values
  per item whatever the outcome, so changing one item's odds doesn't reshuffle every other item
  (inferred).
- **Catalog changes only at a cycle boundary.** Include a catalog version in the seed. After an
  update, old and new servers can disagree until old servers shut down, so use "Migrate to
  latest update" for shop changes (inferred).
- **Per-player stock is the safe default** (Grow a Garden's model): everyone sees the same
  shelf, and each player can buy up to the listed quantity. There's no cross-server
  contention and no "someone else bought it first." Store `{cycle, bought = {[id]: n}}` in
  the profile and reset it when the cycle changes (community model; rule inferred).
- **Truly shared limited stock** (one server or all servers compete) needs an atomic counter:
  server memory for one server, `MemoryStoreService` for all servers. That brings refunds on
  failure, races and angry kids. Skip it unless scarcity *is* the game (inferred; quotas in
  [player data](player-data.md)).
- **Cadence:** 5 min for the main shop (several restocks per 15–25 min session), 30–60 min for
  rare shelves, 24 h for daily deals (community reference; mapping inferred).
- Clients draw the countdown from `Workspace:GetServerTimeNow()`, not the device clock, which
  can be wrong (community, DevForum).
- **Rare in stock?** Say so: a server message at restock ("Golden seed in stock!") makes
  restocks a shared moment (inferred).

### Honest stock and timers

- Stock counts and countdowns must be true. No countdown that restarts for the same offer, no
  "only 2 left" unless it is, and no "daily deal" that never changes (official
  honest-presentation rules; see [monetization](../fundamentals/monetization.md)).
- **Paid instant restocks** (Grow a Garden's 79 Robux, community) skip a wait for Robux. Roblox
  says its players dislike Robux-skippable timers (official). A restock that rerolls random
  stock is also a random outcome bought with Robux, so treat it as a paid random item:
  disclose stock odds and check `PolicyService` (inferred). Default: don't sell restocks.

### Robux items in your shop

- **Price.** Read it on the client with `MarketplaceService:GetProductInfoAsync(id,
  Enum.InfoType.Product)` (or `.GamePass`), inside `pcall`, cached for the session.
  - Display `PriceInRobux`.
  - The reference sample also reads `UserBasePriceInRobux` ("Original Price") and
    `PriceDiscountDetails` (a Roblox Plus discount, with `Percent` and `AmountInRobux`). Use
    them for an honest struck-through price (official API, 2026-10).
  - `GetDeveloperProductsAsync()` lists all products (official).
  - Regional prices sit between 30% and 100% of your default, so hard-coded numbers will be
    wrong for many players (official, 2026-10).
- **Hard-coded prices:** Roblox's Dynamic Price Check tool finds them by previewing the game at
  pinned price levels for up to 5 test users (official, 2026-10).
- **Flow:**
  1. The button calls `MarketplaceService:PromptProductPurchase(player, id)`
     (`PromptGamePassPurchase` for passes).
  2. The grant happens only in the receipt handler, keyed on `PurchaseId`.
  3. The UI celebrates when the server reports the new state. `PromptProductPurchaseFinished`
     only means the prompt closed (official; full rules in
     [monetization](../fundamentals/monetization.md)).
- **Gifting** Robux items to other players needs `GetUsersPriceLevelsAsync` checks at join,
  uncached, so cheap regional purchases can't be farmed (official, 2026-10).

### Bundles and starter packs

- **Bundle:** one developer product whose grant function hands out several things, each
  listed on the card. Roblox suggests bundling instead of chaining complementary prompts
  (official guide).
- **Starter pack:** one per account.
  - Sell it as a pass (ownership stops a repeat purchase) with a saved `StarterClaimed` flag
    for its one-time contents.
  - Or sell it as an unlisted product, shown only while `StarterClaimed` is false.
  - If a second receipt still arrives, grant a fixed currency equivalent. Never drop it
    (inferred).
  - Price: 25–99 Robux ([monetization](../fundamentals/monetization.md) ladder).
  - Show it after the first reward, not on first load. Roblox notes a starter pack may not
    suit a first-time loading screen (official guide).
- Show bundle value in plain numbers ("1,000 coins + Speed Coil"), not "%-off" against a price
  that never existed (official honest-presentation rules).
- Roblox's Shop can also surface Robux packages that include your items (official, 2026-10).

### Refunds and mistakes

- **No refund API.** MarketplaceService has no method to refund a developer product, so make
  good in-game (inferred from the API reference, 2026-10).
- **Robux purchase support:**
  - Keep the last 100 receipts (`PurchaseId`, `ProductId`, time) in the profile, so you can
    verify claims and re-grant (inferred; see
    [player data](player-data.md)).
  - If a grant was missing, repair it with a data patch keyed by `PurchaseId`. Never ask for a
    second purchase.
- **Soft-currency mistakes:**
  - Offer an "Undo" toast for 10 s after any purchase over about 25% of the wallet.
  - Or allow a full-price sell-back until first use.
  - Confirm only for rare or expensive items (inferred).
- **Sold perks must keep working** across updates. Removing paid functionality without notice
  counts as a scam under the Community Standards (official; see
  [monetization](../fundamentals/monetization.md)).

## Implementation outline (server-authoritative)

- **Catalog:** a server-only ModuleScript in `ServerStorage` with ids, prices, odds, stock
  ranges and grant functions. Clients get a display copy.
  - Robux product ids can live in `ReplicatedStorage`; they aren't secret.
  - Soft prices and odds shown to the client are display only.
- **Remotes:**
  - `RequestBuy(shopId, itemId, cycle)` as a RemoteFunction returning `(ok, reason)`. It
    passes the [security](../fundamentals/security-and-anti-exploit.md) pipeline: token
    bucket, `typeof`, catalog lookup, range to the stand, data loaded, cost from the catalog.
  - The client sends the `cycle` it was showing. If the shop has restocked since, refuse with
    "restocked" so it buys what it showed.
- **State the client reads:**
  - `shop:SetAttribute("Cycle", cycle)` on each restock, or let the client compute it.
  - Per-player `bought` counts pushed after each purchase.

```lua
--!strict
-- ServerScriptService/SeedShop.server.lua: OUTLINE, not drop-in
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")
local PlayerData = require(script.Parent.PlayerData) -- session-locked, get() → nil until loaded

type Item = {id: string, price: number, chance: number, minQty: number, maxQty: number}
local CATALOG: {Item} = require(ServerStorage.SeedCatalog) -- ARRAY sorted by id
local BY_ID: {[string]: Item} = {}
for _, it in CATALOG do BY_ID[it.id] = it end
local PERIOD, SHOP_SALT, CATALOG_VERSION = 300, 41, 3 -- bump version only at a cycle boundary

local function cycleNow(): number return math.floor(os.time() / PERIOD) end

local cache: {[number]: {[string]: number}} = {}
local function stockFor(cycle: number): {[string]: number}
	local hit = cache[cycle]
	if hit then return hit end
	local rng = Random.new(cycle * 1009 + SHOP_SALT * 7919 + CATALOG_VERSION)
	local stock = {}
	for _, it in CATALOG do -- fixed order; same draws per item whatever the outcome
		local roll, qty = rng:NextNumber(), rng:NextInteger(it.minQty, it.maxQty)
		if roll < it.chance then stock[it.id] = qty end
	end
	table.clear(cache) -- keep only the current cycle
	cache[cycle] = stock
	return stock
end

local RequestBuy = ReplicatedStorage.Remotes.RequestBuy :: RemoteFunction
RequestBuy.OnServerInvoke = function(player: Player, itemId: unknown, shownCycle: unknown): (boolean, string?)
	-- 1) token bucket + stand-distance check from security-and-anti-exploit.md go here
	if typeof(itemId) ~= "string" or typeof(shownCycle) ~= "number" then return false, nil end
	local cycle = cycleNow()
	if shownCycle ~= cycle then return false, "restocked" end
	local item, data = BY_ID[itemId], PlayerData.get(player)
	if not item or not data then return false, nil end
	if data.Shop.cycle ~= cycle then data.Shop = {cycle = cycle, bought = {}} end
	local left = (stockFor(cycle)[itemId] or 0) - (data.Shop.bought[itemId] or 0)
	if left <= 0 then return false, "sold out" end
	if data.Coins < item.price then return false, "need coins" end
	data.Coins -= item.price -- price from the server catalog, never the client
	data.Shop.bought[itemId] = (data.Shop.bought[itemId] or 0) + 1
	data.Seeds[itemId] = (data.Seeds[itemId] or 0) + 1
	-- AnalyticsService:LogEconomyEvent(player, Enum.AnalyticsEconomyFlowType.Sink, "Coins",
	--   item.price, data.Coins, Enum.AnalyticsEconomyTransactionType.Shop.Name, itemId)
	return true, nil
end
```

Client side: compute `cycle` and the time to the next restock from
`Workspace:GetServerTimeNow()`. Show "Restocking…" for the first second of a new cycle so a
buy sent right at the boundary isn't wasted. Fetch Robux prices once per session with
`GetProductInfoAsync` in `pcall`, and show "…" until they load.

## Common bugs and exploits

| Bug or exploit | Fix |
|---|---|
| Client sends the price or quantity | Price and stock from the server catalog. Quantity integer-checked and capped |
| Buying at the restock boundary gets the wrong item | The client sends the `cycle` it displayed; the server refuses a mismatch |
| Servers show different stock | Seed from `floor(os.time()/PERIOD)` + salt + catalog version; roll an array in fixed order; never `pairs` a dictionary |
| Stock reshuffles when one item's odds change | Draw a fixed number of values per item whatever the outcome |
| Per-player limits reset by rejoining | Store `{cycle, bought}` in the saved profile, not in server memory |
| Countdown wrong on some devices | Use `Workspace:GetServerTimeNow()` on the client, not `os.time()`/`tick()` |
| Robux price wrong for regional players | `GetProductInfoAsync` at runtime; run the Dynamic Price Check tool before launch |
| Grant on prompt close | Grant only in `ProcessReceipt`/`BindReceiptHandler`; see [monetization](../fundamentals/monetization.md) |
| Starter pack bought twice | Pass-based, or a currency-equivalent fallback grant; never silently drop a receipt |
| Remote spam buying out stock or lagging the server | Token bucket per remote; bounded work per call |
| Buying from across the map with a fired remote | Server distance check to the stand, or allow remote buying on purpose (a HUD shop) |
| Fake urgency, flagged by reviewers or players | True stock counts, non-restarting timers, no permanent "sale" |

## Checklist for agents

- [ ] Soft shop and Robux shop are visibly distinct; Robux buttons never replace soft ones.
- [ ] Catalog, prices and odds on the server. `RequestBuy` validated per the security pipeline.
- [ ] Restock = `math.floor(os.time()/PERIOD)` seed, fixed-order roll, per-player bought counts
      saved by cycle. No cross-server messaging needed.
- [ ] Client countdown from `Workspace:GetServerTimeNow()`. Stock and timers are true.
- [ ] Robux prices from `GetProductInfoAsync` (`PriceInRobux`), never hard-coded. Dynamic Price
      Check run.
- [ ] Grants only in the receipt handler, keyed on `PurchaseId`; UI updates from server state.
- [ ] Starter pack once per account, shown after the first reward, priced 25–99 Robux.
- [ ] No paid restocks or Robux-skippable timers by default. If added, odds disclosed and
      `PolicyService` checked.
- [ ] Context-only products unlisted. `ExperienceShop` kept on and the global Shop button
      enabled.
- [ ] Undo or sell-back for soft-currency mistakes. A receipt log kept for support.
- [ ] Shop funnel and economy events logged.

## Sources

1. https://create.roblox.com/docs/production/game-design/contextual-purchases — "right item, right time", pre-play/in-play/lobby/complementary/UI types, buy-Robux delay, no stacked modals, bundling
2. https://create.roblox.com/docs/production/monetization/shop — Roblox Shop surface, listed vs unlisted products, Robux bundles, ExperienceShop, global Shop button off by default
3. https://create.roblox.com/docs/reference/engine/classes/MarketplaceService — GetProductInfoAsync fields (PriceInRobux, UserBasePriceInRobux, PriceDiscountDetails), GetDeveloperProductsAsync, PromptProductPurchase, GetProductInfo deprecated
4. https://create.roblox.com/docs/production/monetization/regional-pricing — display via GetProductInfoAsync/GetDeveloperProductsAsync, Dynamic Price Check, GetUsersPriceLevelsAsync uncached at join
5. https://create.roblox.com/docs/production/monetization/managed-pricing — 30–100% regional bounds
6. https://create.roblox.com/docs/production/monetization — honest presentation, Robux-skippable timers disliked
7. https://growagarden.fandom.com/wiki/Seed_Shop — 5-min global stock, per-player purchases, 24 h Daily Deals, 79-Robux restock
8. https://growagarden.fandom.com/wiki/Gear_Shop — same stock on all servers, 5-min refresh, staple items always stocked
9. https://growagarden.fandom.com/wiki/Pet_Eggs_(Shop) — 30-min egg restock, Robux refresh stand
10. https://stealabrainrot.fandom.com/wiki/Red_Carpet — weighted belt spawns, 150% rival purchase, rare-spawn announcements
11. https://devforum.roblox.com/t/recreate-something-globally/3774167 — time-bucket seeds so all servers roll the same result
12. https://devforum.roblox.com/t/whats-up-with-randomnew/2645384 — seeded Random repeats with the same call order
13. https://devforum.roblox.com/t/os-time-consistency/453603 — client clocks differ from the server
14. https://create.roblox.com/docs/reference/engine/libraries/os — os.time defaults to UTC
15. https://create.roblox.com/docs/reference/engine/datatypes/Random — Random.new, NextInteger, NextNumber
16. https://create.roblox.com/docs/reference/engine/classes/Workspace — GetServerTimeNow

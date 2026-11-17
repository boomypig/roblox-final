---
title: Monetization
type: fundamental
read-when: Adding any game pass, developer product, subscription, or purchase code.
last-researched: 2026-10-22
---

# Monetization

## In one line

Sell cheap, repeatable, honest convenience and expression. Grant every purchase on the server,
exactly once, keyed on `PurchaseId`. Gate restricted products with `PolicyService`. Robux per
user and spend days per user are ranking signals, so monetization is part of discovery, not
separate from it.

## What you can sell (state on 2026-10-22)

| Product | What it is | Creator share | Key limits |
|---|---|---|---|
| Pass | One-time purchase, permanent perk | 70% of Robux spent (official) | Promoted passes on sale must be priced 50–800 Robux (official). Cross-game pass sales disabled from 2026-05-30 (official). |
| Developer product | Repeatable purchase (currency, boosts, revives) | 70% of Robux spent (official) | 1 to 1,000,000,000 Robux. Cross-game product sales disabled from 2026-05-30 (official). Products sold from the game page's Store tab need a working receipt handler, or Roblox stops listing them there (official). |
| Subscription (Robux) | Monthly auto-renew | 70% every month, paid in Robux, ~5-day hold (official) | ≥49 Robux. Regional pricing is on and can't be turned off. Price change at most once per 60 days, with 30 days' notice for increases (official). |
| Subscription (local currency) | Monthly auto-renew at $2.99 / $4.99 / $7.99 / $9.99 / $14.99 | 70% in month 1, then 100%, paid in Robux, 30-day hold (official) | Buyer needs ID or phone verification. Not offered in 12 countries, including India, Indonesia, Japan and Türkiye. Price can't be changed (official). |
| Private server | Monthly Robux fee, or free | 70%: Roblox's Plus private-server example computes earnings as 70% of the price (official) | Can't be combined with paid access. Roblox Plus subscribers join paid ones free (official). See [private servers](../patterns/private-servers.md). |
| Paid access | One-time entry fee, in Robux or local currency | — | Mostly used for closed betas (official). It blocks private servers and kills free discovery (inferred). |
| Rewarded video ad | Player chooses to watch a 6–30 s ad for a dev-product reward | Earnings = EPM × impressions (official) | Viewers must be 13+. Reward can't be random or Robux (official). Details below. |
| Immersive ads | Image, video and portal ad units in 3D | Paid per impression or teleport, on the 25th of the following month (official) | Publisher 13+ with an approved questionnaire. Check `AreAdsAllowed` (official). |
| Robux transfers | Roblox Plus subscribers send 10–500 Robux to another user in your game | Your game gets 10%, the recipient 90%; DevEx-eligible (official) | `MarketplaceService:PromptRobuxTransferAsync` (server only) plus a receipt handler (official). This is the replacement for donation boards that sold other games' passes (official). |
| Avatar items sold in-game | Catalog items via inspect menu or avatar editor | Game owner 40%, item creator 30% (official) | Commission only. |
| Commerce products | Physical goods from a Shopify store | Not stated (unverified) | Creator 18+ and ID-verified; US buyers only, 13+ (18+ in Texas) (official). Skip for a solo launch (inferred). |

### Platform payouts you earn without selling anything

- **Creator Rewards** replaced Premium Payouts (engagement-based payouts) on 2025-07-24
  (official). Don't build anything around Premium playtime.
  - *Daily Engagement:* 5 Robux per Active Spender who plays ≥10 minutes that day, if yours
    is one of the first 3 experiences they launch that day. An Active Spender has ≥$9.99 in
    qualifying purchases in the last 60 days (official, 2026-10).
  - *Audience Expansion:* 35% of a new or reactivated user's first $100 in platform purchases
    over 60 days, when they arrive through your Share Link, direct link, or a search for your
    name. Your game must average ≥100 DAU, and you must be ID-verified (official, 2026-10).
  - Paid out as Earned Robux after a 60-day hold (official).
- **Roblox Plus** ($4.99/month) replaced Premium for new subscribers on 2026-04-30. Premium
  benefits changed on 2026-05-30 (official, DevForum 2026-04-10).
  - Plus members get 10% off in-game items, rising to 20% from the third consecutive month.
    Roblox pays the discount, so your per-sale earnings don't change (official).
  - Sign-up bonus: 250 Robux a month for each subscriber's first 3 paid months (max 750). It
    only counts if they signed up through `MarketplaceService:PromptRobloxSubscriptionPurchase`
    in your game (official, 2026-04).
  - Private servers: Plus members join paid private servers free. On each renewal you get up
    to 100 Robux per Plus member with ≥60 cumulative minutes in that server over 30 days,
    counted across their top 5 servers. Free servers don't qualify (official, 2026-04).
  - `PromptRobloxSubscriptionPurchaseFinished` only means they *tried*; confirm with
    `GetRobloxSubscriptionDetailsAsync`. `PromptPremiumPurchase` is deprecated (official API).

## DevEx and what a sale is worth

- Standard rate: **$0.0038 per Earned Robux** since 2025-09-05 ($114 per 30,000). Robux
  earned before then cash out at the legacy $0.0035 (official, 2026-10).
- Higher rate: **$0.0054** for Robux from developer products, passes, subscriptions and private
  servers bought by US players verified 18+, in eligible games (official, 2026-10). The game
  eligibility rules are on a separate page that wasn't checked (unverified).
- To cash out you need: age 13+, 30,000 Earned Robux, a verified email, and a W-9 or W-8 on
  file. One cash-out per calendar month (official).
- Worked example (inferred arithmetic): a 100-Robux pass nets 70 Robux, which is $0.27 at
  the standard rate. 1,000 sales of a 99-Robux product is about $263.
- Roblox's DevEx payments to creators were $1.50B in 2025, up 63% on 2024 (official, 10-K).

## Monetization is a discovery signal

- Recommended for You ranks games with two monetization signals in its "important" tier:
  **spend days per user** and **Robux spent per user**. Both are averages over users who
  arrived from that sort (official, 2026-10). Full signal list:
  [discovery algorithm](discovery-algorithm.md).
- Spend *days* rewards many small purchases on many days more than one big purchase
  (inferred). Ship a cheap, repeatable, useful product from launch day.
- The explore/expand phase widens distribution when a new cohort shows good engagement *and*
  monetization (official).
- Daily Engagement rewards pay you for returning Active Spenders, so retention is a revenue line
  too (inferred; see [retention](retention.md)).

## What to sell: what players pay for vs what feels exploitative

Roblox splits players into "tourists," who hop between games and want variety and instant
effects, and "locals," who make up the engaged base (official). Sell tourists cheap instant
items and locals long-term value (inferred).

**Players pay happily for** (community + inferred, consistent with Roblox's own guidance):
- Time-savers that don't lock content: 2x currency pass, auto-collect, faster walk, a bigger
  backpack.
- Expression: skins, trails, titles, name colors, emotes, base decorations.
- Capacity and convenience: extra pet, plot, loadout or inventory slots, teleports.
- Social value: a VIP lounge or tag, private servers, and gifting to friends (gifting needs
  a server check that the gift is allowed).
- A starter pack priced for a first purchase, sold once per account.
- Refills and consumables at natural breaks: revive, extra spin, boost for the next round.

**Feels exploitative, so a reviewer should reject it:**
- The best items obtainable *only* by paying, in a game where items decide PvP or stealing
  outcomes. Polygon criticized Steal a Brainrot for this (press, 2025-07-25; see
  [trend lifecycle](trend-lifecycle.md)).
- Appointment timers that you pay to skip. Roblox says these are unpopular with its users
  and work better on other platforms (official).
- False urgency and false discounts (banned; see "Honest presentation" below).
- Paid random items with low odds and no earnable path.
- Interrupting core play with purchase prompts, or prompts that appear before the player has
  any reason to want the item (inferred).

Roblox warns that users downvote games whose monetization they dislike (official). No
platform rule bans pay-to-win outright (none found, 2026-10). The penalties come from ratings,
retention, and press (inferred).

## Pricing (dated guidance)

- **Never hard-code displayed prices.** A player's price can be regional, a Plus discount,
  or a price-test variant. Fetch it with `MarketplaceService:GetProductInfoAsync(id,
  Enum.InfoType.Product)` or `Enum.InfoType.GamePass`, on the client (official, 2026-04 and
  2026-10). `GetProductInfo` without `Async` is deprecated, though older doc samples still use
  it (official API).
- **Managed pricing** combines regional pricing with price optimization. New games and new items
  are enrolled by default (official, 2026-10).
- **Regional pricing** sets prices at 30–100% of your default, based on purchasing power and
  local spending. Subscriptions and private servers are regionalized automatically (official).
  Regional prices for passes raised paying users by 22.4% in Brazil, 44.8% in the Philippines
  and 13.8% in Mexico (official, DevForum 2025-10-01).
- **Price optimization** needs about **60,000 transactions in the previous 30 days** to run
  (official, 2026-10). A new solo game won't qualify, so pick sensible prices by hand.
  - Tests last about 3 weeks and run automatically at least every 90 days.
  - New prices are applied only when they raise total revenue (official).
- **Trading or gifting** with regional prices: use `MarketplaceService:GetUsersPriceLevelsAsync`
  (levels 1–1000) so cheap regional items can't be farmed and resold (official).
- **Experiments** can A/B test price or shop layout through configs (14–60 day runs, up to 2
  variants). See [live ops](live-ops-and-updates.md) and the [analytics](analytics.md) file.
- **Starting price ladder** (inferred; no official numbers exist, so tune with data): first
  purchase 25–99 Robux; repeatable boosts 15–50; permanent perk passes 100–400; one prestige
  anchor at 500–1,500 that makes the rest look reasonable. Matches [discovery](discovery-algorithm.md).
- **Rewarded ad reward value:** worth about 3–10 Robux (official recommendation).

## Purchase handling (server-authoritative)

### Developer products: rules

1. **One handler.** Set `MarketplaceService.ProcessReceipt` once, in one server `Script`, for
   every product (official). Alternatively, use `MarketplaceService:BindReceiptHandler(
   Enum.ReceiptType.DeveloperProduct, handler, filter?)`:
   - A filtered handler only takes the product IDs in its list.
   - A catch-all (no filter) takes everything a filtered handler didn't claim.
   - Bound handlers take precedence. A receipt with no matching handler falls through to
     `ProcessReceipt`, so you can migrate one product at a time (official, API 2026-10).
2. **Use the right enum.** `ProcessReceipt` returns `Enum.ProductPurchaseDecision.PurchaseGranted`
   / `.NotProcessedYet`; bound handlers return `Enum.ReceiptDecision.Processed` / `.NotProcessedYet` (official).
3. **When receipts arrive:** after a purchase, and again whenever the buyer joins any server
   while the receipt is still unresolved (official).
   - No time-based retry and no timeout. Receipts arrive in no guaranteed order.
   - **The same receipt can run on two servers at once** if the player server-hops mid-grant.
   - Even after you return `PurchaseGranted`, the backend can fail to record it and deliver the
     receipt again (official).
4. **Idempotent grant keyed on `PurchaseId`.**
   - Store granted IDs *inside the player's session-locked save*, so the reward and the ID
     persist together in one write. The session lock stops two servers from both granting
     (inferred; see [player data](../patterns/player-data.md)).
   - The docs sample uses a separate `PurchaseHistory` store instead. That needs session
     locking to be safe across servers, which the docs themselves point out (official).
5. **Persist, then acknowledge.** Return granted/processed only after the save write
   succeeds.
6. **Return `NotProcessedYet` when** the buyer isn't on this server, their data isn't loaded
   or locked yet, the product ID is unknown (log it), or the save fails.
7. **Never grant from `PromptProductPurchaseFinished`.** It fires when the prompt closes, not
   when a payment succeeds (official).
8. **Always define a handler before selling.** Without one, receipts are auto-acknowledged and
   can never be recovered (official).
9. **Same path for ads and the Store tab.** `receiptInfo.ProductPurchaseChannel` says where the
   purchase came from: `InExperience`, `ExperienceDetailsPage`, `AdReward` or
   `CommerceProduct` (official API). Don't assume a shop UI is open.

```lua
--!strict
-- ServerScriptService/Receipts.server.lua: the ONLY script that touches receipts.
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")
local PlayerData = require(script.Parent.PlayerData) -- session-locked profiles (patterns/player-data.md)

-- Pure data mutations only: no yields, no remotes. Keyed by developer product ID.
local GRANTS: {[number]: (data: PlayerData.Data) -> ()} = {
	[1234567] = function(data) data.Coins += 1000 end,
	[1234568] = function(data) data.Boosts.Luck2x += 1 end,
}

local function handle(receipt: {[string]: any}): boolean
	local player = Players:GetPlayerByUserId(receipt.PlayerId)
	local profile = if player then PlayerData.getLoaded(player) else nil -- nil until loaded + locked
	local grant = GRANTS[receipt.ProductId]
	if not (player and profile and grant) then
		if not grant then warn("Unknown product", receipt.ProductId) end
		return false -- redelivered on the next purchase or join
	end
	local id = receipt.PurchaseId :: string
	if not profile.Data.PurchaseIds[id] then
		grant(profile.Data)
		profile.Data.PurchaseIds[id] = true -- same document as the reward: saved atomically
	end
	return PlayerData.saveNow(player, id) -- yields; true once a save containing id landed (ProfileStore: profile:Save(), then wait for profile.LastSavedData.PurchaseIds[id])
end

MarketplaceService.ProcessReceipt = function(receipt: {[string]: any}): Enum.ProductPurchaseDecision
	return if handle(receipt)
		then Enum.ProductPurchaseDecision.PurchaseGranted
		else Enum.ProductPurchaseDecision.NotProcessedYet
end
-- Newer equivalent (catch-all), returning Enum.ReceiptDecision.Processed / .NotProcessedYet:
-- MarketplaceService:BindReceiptHandler(Enum.ReceiptType.DeveloperProduct, function(r)
--   return if handle(r) then Enum.ReceiptDecision.Processed else Enum.ReceiptDecision.NotProcessedYet end)
```

If the save fails, the in-memory reward and its ID stay together; a redelivery skips the grant
and retries the save, so it's granted once either way. If you trim `PurchaseIds`, drop only
entries older than 30 days (inferred).

### Passes

- Check ownership on the server in `Players.PlayerAdded` with
  `MarketplaceService:UserOwnsGamePassAsync(player.UserId, passId)` inside `pcall`. Results are
  cached. The first check after a player joins a new server always reflects a purchase made
  earlier (official).
- After `MarketplaceService:PromptGamePassPurchase`, listen on the server to
  `PromptGamePassPurchaseFinished(player, gamePassId, wasPurchased)`. Grant immediately when
  `wasPurchased` is true and the ID matches. This event also refreshes the ownership cache
  (official).
- **Pitfall:** a pass bought *outside* the game (website or Store tab) during a session can take
  "several minutes" to show up in the cache (official). Re-check when the shop opens, or add a
  "Restore purchases" button that re-calls the API (inferred).
- **Pitfall:** a failed `pcall` means "unknown," not "doesn't own." Retry. Never strip perks or
  save `false` on an error (inferred).
- **Pitfall:** pass perks that give a one-time reward (for example, 5,000 coins on purchase) need
  their own saved "claimed" flag. Otherwise they pay out on every join (inferred).
- **Pitfall:** never trust a client remote saying "I bought it"; check on the server (official,
  [security](security-and-anti-exploit.md)). In group-owned games the creator doesn't
  automatically own the passes, so tests can return false (community).

### Subscriptions

- Prompt with `MarketplaceService:PromptSubscriptionPurchase(player, subscriptionId)`.
- Check `MarketplaceService:GetUserSubscriptionStatusAsync(player, subscriptionId)` on the server
  (`IsSubscribed`, `IsRenewing`), and react to `Players.UserSubscriptionStatusChanged` (official).
- Benefits must match on every platform and last the whole paid term. You can't quietly
  revoke them, or gate them behind social-media posts. Battle passes are allowed as
  subscriptions (official).
- To retire a subscription, take it off sale and cancel renewals. Deleting an active one
  refunds every subscriber, and you get 0 Robux (official).

### Rewarded video ads

- Docs eligibility: the creator is 13+ and ID-verified, and the game is public with ≥2,000
  unique visitors a month (official, 2026-10). An earlier DevForum post required ≥100K DAU
  (official, 2025-08). Trust the newer docs, but check Creator Hub > Monetization > Ads.
- Flow: the client checks `AdService:GetAdAvailabilityNowAsync(Enum.AdFormat.RewardedVideo)`
  right before showing the button; the server calls `AdService:CreateAdRewardFromDevProductId`
  then `AdService:ShowRewardedVideoAdAsync(player, reward, placementId?)`; the grant arrives
  through your normal receipt handler (official).
- Only users 13+ see ads. If availability isn't `IsAvailable`, hide the button (official).
- Show ads in safe spots, such as the lobby or after a level, and pause damage while one plays
  (official).
- Roblox expected rewarded video to be up to 3% of earnings in the first months (official,
  2025-07). It's a supplement, not a business model.

## Policy limits (current rules)

### Paid random items (eggs, crates, spins, luck boosts, pity)

- **Scope:** any random outcome bought with Robux, directly or through Robux-bought currency,
  keys, tickets or rerolls. That includes luck boosts and pity systems (official).
- **Odds disclosure:** every outcome with numerical odds as percentages summing to 100%, shown
  *before* purchase or before spending the paid currency. Overflow goes behind a button labelled
  "Info" or "Details" (a bare (i) icon isn't enough). Boosted odds show the player's actual
  odds; once-only items update the remaining odds (official).
- **Every outcome must benefit the player.** Gambling, simulated or real, is banned (official,
  Community Standards).
- **Country gating:**
  - Call `PolicyService:GetPolicyInfoForPlayerAsync(player)` in `pcall`.
  - If `ArePaidRandomItemsRestricted` is true, apply one of these: an earnable path, disclosed
    fixed order, direct purchase at expected value, hide, block, or keep the player out of the
    area (official).
  - If `IsPaidItemTradingAllowed` is false, block trading of paid items (official).
  - Treat a failed call as "restricted" (inferred).
- **Brazil:** players under 18 can't access paid random items. A game that declares them but
  doesn't use `PolicyService` becomes unplayable for those players (official, help center 2026).
- **Disclosure applies worldwide:** Roblox revised the policy for South Korea's law and applied
  it everywhere (press, TechTimes 2026-06-26).
- **More:** [rarity tiers and eggs](../patterns/rarity-tiers-and-eggs.md).

### Honest presentation (official monetization guidance, 2026-10)

- A discount isn't genuine if the item is always "on sale" for the same price.
- A discount isn't fair if it's so short it pressures a fast purchase.
- No false "almost sold out" or "only for a short time" claims.
- No countdowns that are inaccurate or restart for the same item. Example of a banned design: a
  24-hour "deal of the day" that appears on every login and never ends.
- For minors, swap pushy copy for neutral copy: "GET IT NOW" → "View Item", "LAST CHANCE, ACT
  NOW" → "See Price", "BUY BEFORE IT'S GONE!" → "Open Shop".
- Notifications must not use dark patterns: disguised ads, false time pressure, bait-and-switch
  rewards (official).

### Other platform rules

- **No** selling on-platform items through off-platform services, programmatic third-party ads
  or tracking, personalized ads for under-18s, or real-money-prize contests without Roblox's
  direct involvement (official, Community Standards).
- **Scam rule:** taking away paid functionality without proper notice counts as a scam
  (official). Keep sold perks working across updates.
- **Under-13 and young players:**
  - Parents can set monthly spending limits and spend alerts (official, help center).
  - Rewarded ads and personalized notifications are 13+ only (official).
  - Roblox Kids (5–8) and Select (9–15) accounts only see games that passed all-ages evaluation
    (official). See [discovery](discovery-algorithm.md) and [audience](audience.md).
  - Plus Robux transfers by under-18s need parental approval (official).
- **Restricted features:** gate subscriptions, commerce, ads, paid random items and trading with
  the matching `PolicyService` keys: `IsEligibleToPurchaseSubscription`,
  `IsEligibleToPurchaseCommerceProduct`, `AreAdsAllowed`, `ArePaidRandomItemsRestricted`,
  `IsPaidItemTradingAllowed` (official).

## Ethics for a young audience (reviewer rules)

A large share of players are children (inferred; see [audience](audience.md)). A University
of Sydney study of 15 top-earning games (played 2025-10 to 2026-02) documented 14 misleading
practices, including never-ending "daily discounts" and currency layers that hide real prices
(press, 2026-05). Brazil and South Korea already forced rule changes (above) (inferred).

- Show the Robux price on every buy button. Show the Robux cost next to soft-currency packs.
- One confirm step, using Roblox's own prompt. No custom "Are you sure you don't want it?" guilt
  screens.
- Free players must be able to finish the core loop and see all content. Paying makes it faster
  or prettier, not possible.
- In PvP or stealing games, paid power is capped or matched by an earnable equivalent.
- Lead with a value offer, not an upsell. Don't prompt purchases in the first 2 minutes or
  right after a loss (inferred).

## Checklist for agents

### Do
- Put exactly one receipt path in one server script (`ProcessReceipt` and/or
  `BindReceiptHandler`). Make it idempotent on `PurchaseId`, inside the session-locked save.
- Return `NotProcessedYet` / `ReceiptDecision.NotProcessedYet` when the player is missing, data
  isn't loaded, the product is unknown, or the save fails.
- Check pass ownership on the server at join and on `PromptGamePassPurchaseFinished`. Handle
  `pcall` failures as "unknown."
- Fetch every displayed price with `GetProductInfoAsync` on the client.
- Ship a cheap (25–99 Robux) repeatable or starter product at launch.
- Disclose odds and gate paid randomness and trading with `PolicyService`.
- Add a `PromptRobloxSubscriptionPurchase` entry point (for example, a Plus perk sign) if Plus
  perks fit the game.

### Don't
- Grant from `PromptProductPurchaseFinished`, from a client remote, or before the save
  succeeds.
- Hard-code prices, run fake sales, use restarting timers, or write pushy copy.
- Sell the best PvP power only for Robux, or sell randomness with no earnable path.
- Rely on Premium Payouts, which ended 2025-07-24, or on cross-game pass and product sales,
  which ended 2026-05-30.
- Plan around price optimization before the game has about 60,000 transactions a month.

## Related

- [Player data](../patterns/player-data.md): session locking, `PurchaseIds` field, saves
- [Security](security-and-anti-exploit.md): purchase spoofing
- [Shops](../patterns/shops.md), [private servers](../patterns/private-servers.md),
  [rarity tiers and eggs](../patterns/rarity-tiers-and-eggs.md), [trading](../patterns/trading.md)
- [Discovery](discovery-algorithm.md), [retention](retention.md), [audience](audience.md),
  [live ops](live-ops-and-updates.md)

## Sources

1. https://create.roblox.com/docs/production/monetization — product list, update cadence, honest-presentation rules, tourists/locals, appointment timers
2. https://create.roblox.com/docs/get-started/monetization — "You receive 70% of Robux spent" for passes and dev products
3. https://create.roblox.com/docs/production/monetization/developer-exchange — $0.0038 / $0.0054 / legacy $0.0035 rates, requirements
4. https://create.roblox.com/docs/creator-rewards — Daily Engagement and Audience Expansion rules, 60-day hold
5. https://devforum.roblox.com/t/introducing-roblox-plus/4567894 — Plus price, discount, sign-up bonus, private-server rewards, Premium changes
6. https://create.roblox.com/docs/production/monetization/subscriptions — subscription tiers, shares, holds, rules
7. https://create.roblox.com/docs/production/monetization/private-servers — Plus access, paid-access conflict
8. https://create.roblox.com/docs/production/monetization/developer-products — price range, Store tab, cross-game sales end 2026-05-30
9. https://create.roblox.com/docs/production/monetization/game-passes — pass flow, promoted pass price range
10. https://create.roblox.com/docs/reference/engine/classes/MarketplaceService — ProcessReceipt timing/limits, BindReceiptHandler, UserOwnsGamePassAsync caching, receipt fields
11. https://create.roblox.com/docs/production/monetization/managed-pricing — managed/regional pricing, 30–100% bounds
12. https://create.roblox.com/docs/production/monetization/price-optimization — 60,000-transaction threshold, test length
13. https://devforum.roblox.com/t/introducing-regional-pricing-for-developer-products/3971235 — regional pricing results (2025-10-01)
14. https://create.roblox.com/docs/production/promotion/rewarded-video-ads — rewarded ad rules, 3–10 Robux reward, eligibility
15. https://devforum.roblox.com/t/more-creators-can-now-use-rewarded-video-ads/3838678 — 2025 eligibility, 13+ viewers, "up to 3%" of earnings
16. https://create.roblox.com/docs/production/monetization/immersive-ads — ad formats, payout timing, eligibility
17. https://create.roblox.com/docs/production/monetization/robux-transfers — 10–500 Robux, 10% share
18. https://create.roblox.com/docs/production/monetization/commerce-products — commerce eligibility
19. https://create.roblox.com/docs/production/monetization/marketplace-fees-and-commissions — 40%/30% in-game avatar item split
20. https://create.roblox.com/docs/production/monetization/paid-random-items — odds disclosure, PolicyService treatments
21. https://create.roblox.com/docs/reference/engine/classes/PolicyService — policy keys
22. https://about.roblox.com/community-standards — gambling, scams, off-platform sales, ads, contests
23. https://en.help.roblox.com/hc/cs/articles/48706630819476-Brazil-Digital-ECA-Updates — Brazil under-18 paid random item block
24. https://www.techtimes.com/articles/319148/20260626/koreas-loot-box-rules-push-roblox-disclose-item-odds-worldwide.htm — worldwide odds revision (2026-06)
25. https://create.roblox.com/docs/discovery — spend days / Robux per user signals, explore/expand
26. https://www.sec.gov/Archives/edgar/data/1315098/000131509826000024/rblx-20251231.htm — 2025 DevEx fees $1.50B
27. https://www.sydney.edu.au/news-opinion/news/2026/05/17/inside-the-pay-to-play-world-of-roblox-targeting-children-.html — 2026 study of misleading monetization in 15 top games
28. https://create.roblox.com/docs/production/publishing/kids-and-select — Kids/Select account tiers

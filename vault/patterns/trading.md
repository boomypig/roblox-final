---
title: Trading
type: pattern
read-when: Adding player-to-player trading.
last-researched: 2026-10-22
---

# Trading

## What it is

Two players in the same server each put items into a shared trade window. Both accept, a short
countdown runs, both confirm a final summary, and the **server** swaps the items in one step and
saves both players at once. Gifting is a trade with one empty side and goes through the same
pipeline. This file builds on [player data](player-data.md) (session locks, immediate saves) and
[security](../fundamentals/security-and-anti-exploit.md) (validation, dupes); it doesn't repeat them.

## Why it works

- Trading gives every duplicate and every off-meta item a value, so hatching never feels wasted
  (inferred).
- It's a social reason to talk to strangers and bring friends, and a long-term goal ("trade up")
  that doesn't need new content (inferred).
- Scarcity becomes visible: an item is worth what someone will give for it (inferred).
- The cost: trading attracts scammers, dupers and off-platform sellers. A dupe can wreck the whole
  economy in a day (Grow a Garden disabled pet gifting over a dupe bug in 2025-06/07; press).
  Build the safety parts before the fun parts (inferred).

## Genres that use it

[Pet and egg collection](../genres/pet-egg-collection.md), [roleplay life sim](../genres/roleplay-life-sim.md)
(Adopt Me!), [farming](../genres/farming-growing.md) (Grow a Garden), [RNG aura](../genres/rng-aura.md),
[social deduction](../genres/social-deduction.md) (Murder Mystery-style knife and gun skins),
[shooter](../genres/shooter.md) (skins), [steal-a-x](../genres/steal-a-x.md).

## Design rules

### Ship trading late

- Launch without trading, or with gifting to friends only. Add full trading once the item
  economy, session locking and GUID-based items are proven (inferred). Every item that ever
  changes hands must be a unique record with a GUID ([inventory](inventory.md)).
- Same-server trades only. Cross-server or offline trades need `MemoryStoreService` escrow and
  are out of scope for a solo dev (inferred; see [player data](player-data.md#related-systems)).

### Request flow

| Step | Rule |
|---|---|
| Request | From the player list or a `ProximityPrompt` on the other player. Expires after ~20 s. One outgoing request at a time (inferred). |
| Settings | Each player chooses: everyone / friends only / nobody. Default to "everyone" only if your audience is mostly 13+ (inferred). |
| Decline | Blocks repeat requests from the same sender for ~60 s (inferred). |
| Open | Server creates the trade; both players can't start another, and the items they offer are **locked**: no equip, fuse, delete, sell or second trade (inferred). |
| Leave or die | Leaving, teleporting or a data error cancels the trade with nothing moved (inferred). |

### Two-phase confirm (stops the last-second swap)

The classic scam: put a valuable item in the window, then swap it for junk just before the other
player accepts (press, Adopt Me scam guides, 2026). Defend at the protocol level:

1. **Version counter.** Every change to either side increments `trade.version` and clears both
   players' accept and confirm flags. The client sends the version it is accepting; the server
   ignores an accept for an old version (inferred).
2. **Accept → countdown.** When both accept, run a 5 s countdown visible to both. Any change or
   un-accept cancels it (inferred numbers).
3. **Confirm screen.** After the countdown, show a read-only summary of both sides, then both
   confirm. Items can't be changed on this screen (inferred).
4. **Highlight changes.** Flash any slot that changed in the last 3 s, and show a "Trade changed"
   toast (inferred).

### Scam prevention

- **Show what's really there:** tier name and color, variant (Golden, Rainbow), level, and the
  item's real name. Never display a nickname alone; a pet renamed "Legendary Dragon" is a scam
  tool (inferred). Names still pass the text filter ([pets](pets-companions.md#naming)).
- **Imbalance warning:** compute a server-side score (e.g. sum of tier weights) and warn the
  player giving far more: "You're giving much more than you get." Warn, don't block (inferred).
- **No "give first":** the window only swaps simultaneously, and the UI says "Never trade outside
  the trade window" (inferred). Trust trades ("give me yours, I'll give mine later") are the
  standard scam (press, 2026).
- **Teach once:** Adopt Me! requires a "Trade License", a short quiz sorting trade scenarios into
  safe or scam, before trading top-tier pets; passing also unlocks 30 days of trade history and
  scam reporting (press/wiki, 2026). A 3-question quiz is cheap to build (inferred).
- **History:** keep the last 30 trades per player with the other user's ID, item GUIDs and time,
  for support and rollback (inferred).
- **Report button** on the trade screen; log the trade ID with the report (inferred).

### Cooldowns and gates

- Account age: `Player.AccountAge` (days, official API). Require ≥ 3–7 days, and/or ≥ 1 hour of
  play in your game, before trading, to stop fresh alts farming items (inferred thresholds).
- One open trade per player; ~10 s cooldown after a trade completes; cap trades per hour (e.g. 30)
  (inferred).
- Don't allow a new trade until both players' post-trade saves have succeeded. That stops rapid
  chains through a lagging server (inferred).
- Regional prices: if Robux-bought items are tradeable, check
  `MarketplaceService:GetUsersPriceLevelsAsync` so items bought cheaply in one region can't be
  farmed and resold (official; see [monetization](../fundamentals/monetization.md#pricing-dated-guidance)).
- Optional trade hold (e.g. 24 h) on items bought with Robux, to blunt chargeback fraud, which
  Roblox counts as fraud (official rule; hold inferred).

### Roblox rules (official, Community Standards and Creator Docs, 2026-10)

- **Paid item trading:** some users can't trade items bought with Robux, or with currency bought
  with Robux, under local law. If you offer trading, you **must** use `IsPaidItemTradingAllowed`
  from `PolicyService:GetPolicyInfoForPlayerAsync` so only eligible users can trade them.
- Being allowed to buy paid random items doesn't mean being allowed to trade them; both keys are
  separate (`ArePaidRandomItemsRestricted` vs `IsPaidItemTradingAllowed`).
- How to apply it (inferred): mark every item that came from Robux (directly, through
  Robux-bought currency, or from a paid egg) with `Paid = true`, and keep the flag through trades
  and fusing. If either player's `IsPaidItemTradingAllowed` is false, neither can offer or receive
  `Paid` items. Treat a failed policy call as false. Simplest of all: never let paid items be
  tradeable.
- **Real-money trading is banned:** off-platform, secondary-market deals for virtual content from
  games; third-party services that buy, sell or trade Robux; offering virtual content for Robux or
  other payment outside Roblox's systems. Don't build features that settle trades in Robux (e.g.
  "buy this pet from me through my game pass") (official rules; feature advice inferred).
- **No gambling with items:** "No real money, Robux, or in-game items of value may be exchanged"
  in connection with gambling, simulated or real. No coinflips, jackpots or wagers with
  tradeable items (official).
- **Disclose** paid item trading in the maturity questionnaire
  ([metadata](../fundamentals/metadata-thumbnails-icons.md#maturity--compliance-questionnaire)).

### Dupe postmortems

| Game | What happened | Lesson |
|---|---|---|
| Grow a Garden (2025) | Pet gifting disabled ~2025-06/07 over an "exploit/dupe bug", restored 2025-07-09; some accounts were trade-restricted or banned (press). A reported method used two clients and server lag so a transfer completed twice (press; unverified). | Gifting needs the same atomic, saved, rate-limited pipeline as trading. Keep a kill switch (inferred). |
| Pet Simulator X | A dupe let players create top pets "out of thin air". The fix reportedly rewrote the trading code, moved to a newer DataStore setup to fix a desync, banned top exploiters and reverted duped currency (press; unverified). | Dupes come from desync between memory and saves. Session locks plus GUIDs make them preventable and traceable (inferred). |
| Generic | Trade, then crash or leave before the save lands; the giver rejoins on stale data (official, Roblox docs). | Session-lock data and save both sides immediately ([player data](player-data.md#common-bugs-and-exploits)). |

**The hole that remains** (inferred): two players are two DataStore keys, and there's no
multi-key transaction. If the server dies after one save lands and before the other, one item can
exist twice. Mitigations, in order of cost:
1. Save both profiles in parallel right after the swap (shrinks the window to one round trip).
2. Keep every item's GUID unchanged through trades, and log `{TradeId, A, B, GUIDs, time}` to a
   `TradeLog` DataStore (one key per day or per trade). A dupe then shows as one GUID in two
   profiles and can be reversed.
3. Kill switch: a server-read config flag that disables trading or gifting instantly.
4. High-value economies only: two-phase commit. Write a `Trades/{TradeId}` record as `pending`,
   save both profiles with the items moved into an escrow field, mark the record `committed`, then
   release escrow on each profile. On load, a profile holding escrow reads the record and either
   completes or refunds.

## Implementation outline (server-authoritative)

- **State (server memory only):** `Trade {id: GUID, version, a: Side, b: Side, phase}` with
  `Side {player, uids, accepted, confirmed}`. Index trades by player.
- **Remotes (C→S):** `TradeRequest(userId)`, `TradeRespond(tradeId, accept)`,
  `TradeSetOffer(tradeId, uids)` (≤ 9 strings, each ≤ 38 chars), `TradeAccept(tradeId, version)`,
  `TradeConfirm(tradeId, version)`, `TradeCancel(tradeId)`. **(S→C):** `TradeState(snapshot)` to
  both players after every change. Token-bucket every remote.
- **On every `TradeSetOffer`:** types, ownership, not locked, not already offered elsewhere,
  `Paid` rules, then bump version and clear flags.
- **Execute** only from the final confirm, re-checking everything, with no yields until both
  inventories are updated. Use `profile:Save()` (ProfileStore) or your save function right after.

```lua
--!strict
-- ServerScriptService/TradeServer: execution step only, outline
local PlayerData = require(script.Parent.PlayerData) -- get(p), canSave(p), saveNow(p) -> boolean
local Policy = require(script.Parent.Policy)         -- paidTradeOK(p) -> boolean, cached at join

type Side = {player: Player, uids: {string}, confirmed: boolean}
type Trade = {id: string, version: number, a: Side, b: Side}

local function valid(give: Side, get: Side): boolean
	local from, to = PlayerData.get(give.player), PlayerData.get(get.player)
	if not from or not to or not PlayerData.canSave(give.player) then return false end
	if give.player.Parent == nil then return false end -- left mid-trade
	local seen: {[string]: boolean} = {}
	for _, uid in give.uids do
		local pet = from.Pets[uid]
		if not pet or seen[uid] or pet.Locked then return false end
		if pet.Paid and not (Policy.paidTradeOK(give.player) and Policy.paidTradeOK(get.player)) then
			return false
		end
		seen[uid] = true
	end
	return to.PetCount - #get.uids + #give.uids <= to.PetCap -- room after the swap
end

local function move(from: any, to: any, uids: {string})
	for _, uid in uids do
		local pet = from.Pets[uid]
		from.Pets[uid], from.PetCount = nil, from.PetCount - 1
		local i = table.find(from.Equipped, uid)
		if i then table.remove(from.Equipped, i) end
		to.Pets[uid], to.PetCount = pet, to.PetCount + 1 -- same GUID: the audit trail survives
	end
end

local function execute(t: Trade): boolean
	if not (t.a.confirmed and t.b.confirmed) then return false end
	if not valid(t.a, t.b) or not valid(t.b, t.a) then return false end
	local da, db = PlayerData.get(t.a.player) :: any, PlayerData.get(t.b.player) :: any
	-- No yields between the checks above and the end of these two moves.
	move(da, db, t.a.uids)
	move(db, da, t.b.uids)
	local entry = {Id = t.id, T = os.time(), A = t.a.player.UserId, B = t.b.player.UserId,
		FromA = t.a.uids, FromB = t.b.uids}
	for _, d in {da, db} do
		table.insert(d.TradeLog, entry)
		if #d.TradeLog > 30 then table.remove(d.TradeLog, 1) end
	end
	task.spawn(PlayerData.saveNow, t.a.player) -- both saves start now, in parallel
	task.spawn(PlayerData.saveNow, t.b.player)
	-- then: republish equipped pets, fire TradeState "done", write the TradeLog store entry
	return true
end
```

## Common bugs and exploits

| Bug | Cause | Fix |
|---|---|---|
| Last-second swap | Accept counted after the other side changed | Version counter; changes clear both flags; countdown; confirm screen (inferred) |
| Item in two trades | Offered items not locked | Lock offered items server-side until the trade ends (inferred) |
| Same item twice in one offer | Duplicate UIDs in the array | `seen` set on every offer and at execute (inferred) |
| Trade dupe on crash or leave | Only one side saved, or saved late | Session locks, immediate parallel saves, GUID log ([player data](player-data.md)) |
| Trade with unloaded data | Profile loading or `canSave = false` | Refuse unless both profiles are loaded and saveable (official principle) |
| Yield inside the swap | A DataStore or policy call between check and move lets state change | All lookups before; no yields during the move (inferred) |
| Overflowing inventory | Receiver's cap not checked | Check room after the swap on both sides (inferred) |
| Equipped pet traded away keeps boosting | `Equipped` not cleaned | Remove from `Equipped` in `move`, republish (inferred) |
| Gift spam / dupe | Gifting outside the trade pipeline | Gifts are trades with one empty side (inferred; Grow a Garden 2025, press) |
| Ineligible player gets a paid item | No `IsPaidItemTradingAllowed` check, or check only on the giver | Check both players for `Paid` items (official rule; both-sides check inferred) |
| Remote spam | `TradeSetOffer` fired 100×/s | Token bucket per remote ([security](../fundamentals/security-and-anti-exploit.md#rate-limiting)) |

## Checklist for agents

- [ ] Items are unique GUID records; GUIDs never change on trade.
- [ ] Same-server only; trade state lives only in server memory.
- [ ] Every change bumps `version` and clears accepts; accept/confirm carry the version.
- [ ] Accept → 5 s countdown → read-only confirm screen; any change cancels.
- [ ] Offered items locked; leaving cancels; no yields during the swap.
- [ ] Both profiles loaded, saveable, under capacity; both saved immediately in parallel.
- [ ] Trade logged with GUIDs (profile history of 30 + a `TradeLog` store); kill switch flag exists.
- [ ] `IsPaidItemTradingAllowed` checked for both players on `Paid` items; failure = not allowed.
- [ ] Account-age or playtime gate, request cooldowns, trade settings (everyone/friends/nobody).
- [ ] Real names, tier, variant shown; imbalance warning; "never trade outside the window" notice.
- [ ] No Robux settlement between players, no item gambling; questionnaire updated.

## Sources

1. https://about.roblox.com/community-standards: paid item trading and `IsPaidItemTradingAllowed` requirement, off-platform and Robux trading bans, gambling with items banned, chargeback fraud
2. https://create.roblox.com/docs/production/monetization/paid-random-items: `IsPaidItemTradingAllowed` meaning; ineligible users must not trade paid items
3. https://create.roblox.com/docs/reference/engine/classes/PolicyService.md: policy keys, `pcall`, server use
4. https://create.roblox.com/docs/scripting/security/client-server-boundary: trade dupes, atomic swap guidance
5. https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing: session locking, save after trades
6. https://create.roblox.com/docs/reference/engine/classes/Player: AccountAge
7. https://create.roblox.com/docs/reference/engine/classes/MarketplaceService: GetUsersPriceLevelsAsync
8. https://www.sportskeeda.com/roblox-news/why-pet-gifting-disabled-grow-garden: Grow a Garden gifting disabled over a dupe bug (2025)
9. https://ofzenandcomputing.com/why-pet-gifting-is-disabled-in-grow-a-garden/: reported lag/two-client dupe method, restoration 2025-07-09 (unverified)
10. https://gamerjournalist.com/pet-simulator-x-hell-update/: Pet Simulator X dupe patch, trading rewrite, reverted currency (unverified)
11. https://thenerdstash.com/how-to-get-a-trading-license-in-adopt-me/: Adopt Me Trade License quiz
12. https://progameguides.com/roblox/adopt-me-adds-methods-to-avoid-being-scammed/: Adopt Me anti-scam features
13. https://deltiasgaming.com/?p=224692: common trade scams (pressure, trust trades, last-second swaps)

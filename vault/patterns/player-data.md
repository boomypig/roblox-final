---
title: Player data
type: pattern
read-when: Saving anything: DataStores, session locking, data migration.
last-researched: 2026-10-22
---

# Player data

## What it is

Each player's save lives in one DataStore key. At join the server loads it into memory under a
session lock. Gameplay reads and writes only that in-memory copy. The server writes it back on a
timer, after purchases and trades, when the player leaves, and at shutdown. Default to
**ProfileStore**; hand-roll only with the same guarantees.

## Why it works

- Lost progress is the fastest way to lose a player for good. A bad save hurts players more than
  any missing feature (inferred).
- Dupes inflate the economy and destroy trade value. Session locking blocks the most common dupe
  class: leaving or crashing before a save lands, then loading stale data on another server
  (official, 2026-10).
- Buffering in memory keeps gameplay instant and DataStore traffic tiny. DataStore calls are web
  requests with rate limits (official, 2026-10).

## Genres that use it

All of them. The stakes are highest where items are tradeable or scarce:
[pet and egg collection](../genres/pet-egg-collection.md), [RNG aura](../genres/rng-aura.md),
[simulator](../genres/simulator.md), [tycoon](../genres/tycoon.md),
[steal-a-x](../genres/steal-a-x.md), and anything with [trading](trading.md).

## Design rules

### Current limits (official, read 2026-10-22)

| Limit | Value |
|---|---|
| Value per key | 4,194,304 characters of serialized JSON (~4 MB). Check size with `HttpService:JSONEncode()`. |
| Store name, key, scope | 50 characters each |
| User metadata per key | 300 characters total |
| Per-key throughput (rolling 60 s) | Read 25 MB/min, write 4 MB/min |
| Storage per experience | 500 MB + 1 MB × lifetime users. Counts the compressed latest version of each key only. Live since 2026-07-29; the base was 100 MB before. |
| Experience-wide requests/min (shared with Open Cloud) | Read 300 + 40×CCU, Write 300 + 20×CCU, List 300 + 2×CCU, Remove 300 + 40×CCU. Ordered stores use the same formulas. |
| Default per-server requests/min | Standard Read 60 + 40×players, Write 60 + 40×players, List 5 + 2×players, Remove 60 + 40×players. Ordered Write 30 + 5×players. New servers get a one-time startup burst. |
| `UpdateAsync` cost | One read plus one write |
| Request queue | 30 requests per queue. When a queue is full, calls fail with errors 301–306. |
| `GetAsync` cache | 4 s. Bypass with `DataStoreGetOptions.UseCache = false`. Cached reads don't count against limits. |
| Versions | The first write per key per UTC hour makes a version. Superseded versions expire 30 days after being overwritten. |
| `game:BindToClose` | Every bound function together gets 30 s before shutdown. They run in parallel. |
| Studio Run mode | Separate, possibly lower, static limits |

- Read budgets with `DataStoreService:GetRequestBudgetForRequestType(Enum.DataStoreRequestType.StandardWrite)`.
  Use the modern enum values `StandardRead`, `StandardWrite`, `StandardList`, `StandardRemove`
  and `Ordered*`. The legacy values (`GetAsync`, `SetIncrementAsync`, `UpdateAsync`, …) "should
  not be used" (official, 2026-10).
- `DataStoreService:SetRateLimitForRequestType(type, base, perPlayer)` caps one server's share of
  the experience budget (official, 2026-10).
- What happens past the storage cap isn't documented: the docs give only the formula
  (unverified). Treat the cap as hard.

### Tuning rules

- One store, such as `PlayerData`, and one key per player with a static pattern: `Player_{UserId}`.
  Never key by name or display name. Split keys only when access patterns differ, and keep data
  that must change together in the same key (official, 2026-10).
- Autosave every 180 s (Roblox sample) to 300 s (ProfileStore default), with a random first
  offset so servers don't write in sync (official, 2026-10; community, 2025-07). Also save right after
  every Robux purchase and every trade, and on leave and shutdown (official, 2026-10).
- The experience-wide write budget works out to ~20 writes per player per minute. Autosave plus
  event saves use well under 1, so budget trouble means you're saving per change (inferred from
  the formula).
- Keep a typical save under 100 KB and alert above 1 MB (inferred). Storage averages 1 MB per
  lifetime user, and keys max out at 4 MB. Cap every growing list: purchase IDs (ProfileStore's
  example keeps the last 100, community), logs, mail.
- Don't pre-compress. DataStores compress automatically, and storage is measured compressed
  (official, 2026-10).
- Store plain data only: strings (valid UTF-8), numbers, booleans, and arrays or dictionaries
  with string keys. No Instances, no `Vector3`/`CFrame`/`Color3` (serialize to arrays), no mixed
  or gapped arrays, no NaN (official, 2026-10; community, 2025).
- Put `SchemaVersion: number` at the top level of every save from day one (inferred).

## Implementation outline (server-authoritative)

### Default: ProfileStore (community)

- By loleris (MadStudio), Apache-2.0. It's the successor to ProfileService, and its profiles are
  backward-compatible with ProfileService saves. Wally `lm-loleris/profilestore` 1.0.3; last
  commit 2025-07-31 (community, 2025-07). DataStore2 is legacy and not for new games
  (official, 2026-10).
- Flow (community): `ProfileStore.New("PlayerStore", TEMPLATE)` →
  ``store:StartSessionAsync(`Player_{player.UserId}`, {Cancel = function() return player.Parent ~= Players end})``
  → if nil, kick ("rejoin") → `profile:AddUserId(player.UserId)` → `profile:Reconcile()` → run
  migrations → `profile.OnSessionEnd:Connect(kick)` → if the player already left,
  `profile:EndSession()`. On `PlayerRemoving`, call `profile:EndSession()`. ProfileStore handles
  `BindToClose` itself.
- Defaults in source (community, 2025-07): `AUTO_SAVE_PERIOD` 300 s. A waiting server steals a
  conflicting session after `SESSION_STEAL` 40 s; it uses MessagingService to ask the holder to
  release first. A lock silent for `ASSUME_DEAD` 630 s counts as a crashed server.
  `START_SESSION_TIMEOUT` is 120 s.
- Extras: `profile:Save()` saves now, e.g. after a trade. `profile.LastSavedData` lets
  `ProcessReceipt` wait until a `PurchaseId` is actually saved. `store:GetAsync(key)` reads
  offline profiles without locking (for admin tools). `store:VersionQuery()` rolls back.
  `store:MessageAsync()` sends gifts to offline players. `store.Mock:StartSessionAsync()` keeps Studio tests
  out of live data (community).
- Not for leaderboards or global state. The README says so (community).

### Hand-rolled: what Roblox's reference system does (official, 2026-10)

- **Lock in metadata.** Every read and write goes through `UpdateAsync`. The callback refuses to
  proceed if the key's metadata holds another server's `LockId` that is younger than the lock
  expiry. Otherwise it writes this server's GUID as the lock in the same call. A save also checks
  that this server's lock is still there. If not, the lock was taken, so stop saving and end the
  session.
- **Refresh the lock** on every autosave, and make the expiry several autosave intervals long.
- **Order requests per key.** Use a queue per key and retry with exponential backoff plus jitter
  inside the queue, so an old retry can't overwrite newer data. At shutdown, skip to the latest
  queued request.
- **Failed load means never save.** On load error, let the player continue on defaults with
  `canSave = false`, show a warning, and block purchases. Or kick. Never write that default data.
- **Callback rules:** `UpdateAsync` callbacks can't yield, may run more than once, and return
  `nil` to cancel. Return `keyInfo:GetUserIds()` and `keyInfo:GetMetadata()` unless you're
  changing them, or they're cleared (official, 2026-10).

### Luau sketch: session-locked load/save outline

```lua
--!strict
-- ServerScriptService/PlayerData: outline only (production: ProfileStore, or add per-key queues)
local DataStoreService = game:GetService("DataStoreService")
local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")

local STORE = DataStoreService:GetDataStore("PlayerData")
local SCHEMA, AUTOSAVE, LOCK_EXPIRY = 3, 180, 600 -- lock lasts >3 autosaves
local SERVER_ID = HttpService:GenerateGUID(false)

export type Data = {SchemaVersion: number, Coins: number, Items: {[string]: number}, PurchaseIds: {string}}
type Session = {data: Data, canSave: boolean}
local TEMPLATE: Data = {SchemaVersion = SCHEMA, Coins = 0, Items = {}, PurchaseIds = {}}
local MIGRATE: {[number]: (any) -> ()} = {
	[1] = function(d) d.Items = d.Inventory or {}; d.Inventory = nil end, -- v1→v2 rename
	[2] = function(d) d.PurchaseIds = {} end,                              -- v2→v3 new field
}
local sessions: {[Player]: Session} = {}

local function deepCopy(t: any): any
	if type(t) ~= "table" then return t end
	local c = {}
	for k, v in t do c[k] = deepCopy(v) end
	return c
end

local function tryLoad(player: Player): (string, any)
	local status, value = "error", nil
	local ok = pcall(function()
		STORE:UpdateAsync(`Player_{player.UserId}`, function(old: any, info: DataStoreKeyInfo?)
			local meta = if info then info:GetMetadata() else {}
			local lock = meta.Lock
			if lock and lock.Id ~= SERVER_ID and os.time() - lock.T < LOCK_EXPIRY then
				status = "locked"; return nil -- another server holds the session
			end
			if old and (old.SchemaVersion or 1) > SCHEMA then
				status = "newer"; return nil -- saved by a newer build: never downgrade
			end
			status, value = "ok", old
			meta.Lock = {Id = SERVER_ID, T = os.time()}
			return old or deepCopy(TEMPLATE), {player.UserId}, meta
		end)
	end)
	if not ok then return "error", nil end
	return status, value
end

local function save(player: Player, release: boolean)
	local s = sessions[player]
	if not s or not s.canSave then return end -- never write defaults over real data
	local ok, err = pcall(function()
		STORE:UpdateAsync(`Player_{player.UserId}`, function(_old: any, info: DataStoreKeyInfo?)
			local meta = if info then info:GetMetadata() else {}
			if not meta.Lock or meta.Lock.Id ~= SERVER_ID then
				s.canSave = false; return nil -- lock lost: stop writing
			end
			meta.Lock = if release then nil else {Id = SERVER_ID, T = os.time()}
			return s.data, {player.UserId}, meta
		end)
	end)
	if not ok then warn("save failed", player.UserId, err) end -- production: queued retry
end

local function onPlayerAdded(player: Player)
	for attempt = 1, 5 do
		local status, raw = tryLoad(player)
		if status == "ok" then
			local data = raw or deepCopy(TEMPLATE)
			for v = data.SchemaVersion or 1, SCHEMA - 1 do MIGRATE[v](data) end
			data.SchemaVersion = SCHEMA
			for k, v in TEMPLATE do if data[k] == nil then data[k] = deepCopy(v) end end -- reconcile
			sessions[player] = {data = data, canSave = true}
			if player.Parent ~= Players then save(player, true); sessions[player] = nil; return end
			task.spawn(function() -- staggered autosave
				task.wait(math.random() * AUTOSAVE)
				while sessions[player] do save(player, false); task.wait(AUTOSAVE) end
			end)
			return
		elseif status == "newer" then break end
		task.wait(math.min(8, 2 ^ attempt) * (0.5 + math.random())) -- backoff + jitter
	end
	if player.Parent ~= Players then return end
	sessions[player] = {data = deepCopy(TEMPLATE), canSave = false} -- play, never save
	-- tell the client: progress won't save; block purchases while canSave is false
end

Players.PlayerAdded:Connect(onPlayerAdded)
for _, p in Players:GetPlayers() do task.spawn(onPlayerAdded, p) end
Players.PlayerRemoving:Connect(function(p) save(p, true); sessions[p] = nil end)
game:BindToClose(function() -- engine allows 30 s total
	local pending = 0
	for p in sessions do
		pending += 1
		task.spawn(function() save(p, true); pending -= 1 end)
	end
	while pending > 0 do task.wait() end
end)

return {get = function(p: Player): Data? local s = sessions[p]; return s and s.data end}
```

Migrations run in order, one step per version, and each step only adds or renames fields; never
reuse a field name for a new meaning (inferred). Reconcile fills top-level gaps from the
template. Deep-reconcile only fixed-shape records, never dictionaries like `Items` (inferred).

### Related systems

- **Purchases:** grant inside `MarketplaceService.ProcessReceipt` (or `BindReceiptHandler`).
  Check the `PurchaseId` isn't already recorded, grant, record the `PurchaseId` in the same
  data, save, and return `PurchaseGranted` only after the save succeeds. Otherwise return
  `NotProcessedYet` (official, 2026-10). The callback can run on two servers at once if the
  player hops, which session locking makes safe (official, 2026-10). See
  [monetization](../fundamentals/monetization.md).
- **Trades:** apply both sides in server memory in one step, then save both profiles right away.
  Refuse the trade if either profile has `canSave = false` (official principle; details inferred).
  See [trading](trading.md).
- **Leaderboards:** use `OrderedDataStore`, which holds integers only. `GetSortedAsync` pages
  hold at most 100. The ordered write default is 30 + 5×players per server per minute, so write
  stats on leave and every few minutes, not per change. Cache the top-N on each server and refresh
  every 60 s or more (official limits 2026-10; cadence inferred). See [leaderboards](leaderboards.md).
- **Cross-server state:** `MemoryStoreService` (sorted maps, queues, hash maps) suits
  matchmaking, global events, live auctions and trade escrow, never the save of record. Quotas:
  memory 64 KB + 1.2 KB × users, requests 1,000 + 120 × CCU per minute, values ≤ 32 KB,
  expiration ≤ 3,888,000 s (45 days, also the default), ~30,000 request units/min per partition
  (official, 2026-10). `MessagingService` messages are ≤ 1 KB and best-effort, with 600 + 240 ×
  players sends per server per minute (official, 2026-10).
- **GDPR / right to erasure:** pass user IDs (`SetAsync` `userIds`, the third return of
  `UpdateAsync`, `profile:AddUserId`). Set up automated RTBF in Data Stores Manager: up to 100
  templates, using the case-sensitive `{UserId}` token in the store name, scope or key, e.g.
  `Player_{UserId}`. Templates only work with static key patterns (official, 2026-10). Otherwise,
  delete by hand within 30 days of the request (official, 2026-10). Include ordered stores and
  any external backend.
- **Studio:** turn on Game Settings → Security → Enable Studio Access to API Services to test
  saves. Studio writes go to the live stores, so use a separate test place or
  `store.Mock` (official, 2026-10; community, 2025-07).

## Common bugs and exploits

| Bug | Cause | Fix |
|---|---|---|
| Wiped progress | Load failed or timed out, the default data was used, and a later save overwrote the real save | `canSave = false` on any failed or partial load (official, 2026-10) |
| Saving before load finishes | A leave or autosave fires mid-load and writes the template | Save only sessions that finished loading. If the player left mid-load, write back the loaded data and release the lock as soon as the load completes (inferred) |
| Rejoin rollback / dupe | Server A's final save is slow (retries, throttling, a yield in `PlayerRemoving`, a lagging server), the player joins server B, which loads old data, then A's save lands and B overwrites it | Session lock in metadata via `UpdateAsync`, checked on every write (official, 2026-10) |
| Trade dupe | Trade, then leave or crash the server before the save lands | Save both profiles immediately after a trade, under session locks. Commit atomically (official, 2026-10) |
| Out-of-order retries | Naive `pcall` retry loop: an old retry overwrites a newer write | One queue per key, retries inside the queue (official, 2026-10) |
| Lost shutdown saves | Saves run one after another in `BindToClose`, or wait on throttled queues past 30 s | Save in parallel, skip stale queued requests, keep saves small (official, 2026-10) |
| Saving `nil` or garbage | Callback returns `nil` by accident, or data contains Instances, NaN or mixed tables | Validate the shape before save. `nil` cancels the write, which is safe but silent, so log it (official, 2026-10) |
| Metadata or user IDs wiped | `UpdateAsync` callback returns only the value | Return the value, user IDs and metadata every time (official, 2026-10) |
| Downgrade on rolling update | An old server loads a save written by a newer schema, then saves an older shape | Refuse to load when `SchemaVersion > SCHEMA` (inferred) |
| Double grant of Robux items | Grant happened but the save failed, so the receipt is re-sent | Record `PurchaseId` in the same save; return `PurchaseGranted` only after it saves (official, 2026-10) |
| Throttling | `SetAsync` per coin pickup, or an ordered-store write per change | Buffer in memory; save on a timer and at key events (official, 2026-10) |
| Studio corrupts live data | Testing against production stores | Test place, `store.Mock`, or skip saves when `RunService:IsStudio()` (official, 2026-10) |
| Key hits 4 MB | Unbounded inventories or logs | Cap lists; alert on `#HttpService:JSONEncode(data)` (inferred) |

## Checklist for agents

- [ ] ProfileStore, or a hand-rolled system with locks, ordered retries and the `canSave` rule.
- [ ] One key per player, `Player_{UserId}`, in a small fixed set of stores.
- [ ] `SchemaVersion` field, ordered migrations, template reconcile, no downgrade.
- [ ] Nothing saves unless the load succeeded; failed loads block purchases and trades.
- [ ] Autosave 180–300 s with jitter; save after purchases and trades, on leave, in `BindToClose`.
- [ ] `UpdateAsync` callbacks don't yield and always return user IDs and metadata.
- [ ] Receipts deduplicated by `PurchaseId` stored in the same save.
- [ ] Saved data is plain, valid UTF-8, size-capped, and has no Instances or userdata.
- [ ] Leaderboards in a separate `OrderedDataStore`, written sparingly.
- [ ] `{UserId}` RTBF template configured; user IDs attached to every write.
- [ ] Gameplay code reads data only through `get(player)` and handles `nil` (not loaded yet).

## Sources

1. https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits: size, throughput, storage, experience and server limits, queues, error codes, modern request types
2. https://devforum.roblox.com/t/unifying-data-stores-open-cloud-and-game-apis-and-increasing-storage-limits/4739240: 500 MB base, unified budgets, live 2026-07-29
3. https://create.roblox.com/docs/cloud-services/data-stores/best-practices: one key per player, key patterns, save triggers, retries, DataStore2 legacy, RTBF
4. https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing: session locking in metadata, ordered retries, `canSave`/errored-load rule, 180 s autosave, 30 s BindToClose, receipt flow
5. https://create.roblox.com/docs/cloud-services/data-stores/versioning-listing-and-caching: 4 s cache, UseCache, hourly versions, 30-day retention
6. https://create.roblox.com/docs/reference/engine/classes/GlobalDataStore: UpdateAsync callback rules, UTF-8 requirement
7. https://create.roblox.com/docs/reference/engine/enums/DataStoreRequestType: legacy vs modern enum values
8. https://create.roblox.com/docs/reference/engine/classes/DataModel: BindToClose 30 s, parallel callbacks
9. https://create.roblox.com/docs/reference/engine/classes/OrderedDataStore: integers only, page size ≤ 100
10. https://create.roblox.com/docs/cloud-services/memory-stores: memory and request quotas, 32 KB values, 45-day expiration
11. https://create.roblox.com/docs/reference/engine/classes/MessagingService: 1 KB, best-effort, send limits
12. https://create.roblox.com/docs/cloud-services/data-stores/right-to-be-forgotten: automated RTBF templates, `{UserId}` token, 100 templates
13. https://create.roblox.com/docs/reference/engine/classes/MarketplaceService: ProcessReceipt guarantees, BindReceiptHandler
14. https://devforum.roblox.com/t/profilestore/3190543: ProfileStore announcement (2024-10), successor to ProfileService, 300 s autosave
15. https://github.com/MadStudioRoblox/ProfileStore: source constants, version, README scope note
16. https://madstudioroblox.github.io/ProfileStore/api/: ProfileStore API (StartSessionAsync, Reconcile, Mock, GetAsync, VersionQuery, MessageAsync)

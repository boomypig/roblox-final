---
title: Leaderboards
type: pattern
read-when: Adding in-game or global leaderboards.
last-researched: 2026-10-22
---

# Leaderboards

## What it is

There are three layers, and each needs a different tool:

| Layer | Tool | Scope | Freshness |
|---|---|---|---|
| Session board (player list) | `leaderstats` Folder under each `Player` | This server | Instant |
| All-time global board | `OrderedDataStore`, plus Roblox's platform Friends/Global view | Every server, forever | Delayed by backend caching (official, 2026-10) |
| Daily, weekly or live event board | `MemoryStoreService` sorted map with expiration | Every server, short-lived | Seconds |

The player's profile (see [player-data](player-data.md)) stays the source of truth. Boards are
mirrors the server writes from it.

## Why it works

- A visible rank gives a reason to play one more round and something to show friends. The
  Friends view matters most for small games: a rank among friends is reachable, while global
  rank #1 isn't (inferred).
- Daily and weekly boards reset, so new and casual players can place, and every reset is a
  reason to return (inferred). See [retention](../fundamentals/retention.md).
- Lobby boards also show new players what "good" looks like, such as a best time to beat
  (inferred).

## Genres that use it

[Round-based races](../genres/round-based-races-and-survival.md) (wins, best times),
[obbies](../genres/obby-classic.md) (stage, completions), [tower obbies](../genres/obby-tower.md),
[simulators](../genres/simulator.md) and [+1 stat games](../genres/plus-one-stat.md) (stat
totals), [racing](../genres/racing-driving.md) (lap times), [tycoons](../genres/tycoon.md)
(cash), [battlegrounds](../genres/battlegrounds.md) (kills, streaks).

## Design rules

### Session board: `leaderstats` (official, 2026-10)

- Create a `Folder` named exactly `leaderstats` (all lowercase) under the `Player`, on the
  server. Any other name keeps the player off the board.
- Stats are value objects (`IntValue`, `NumberValue`, `StringValue`) with the stat name as
  `Name`. They appear in the order you add them.
- A child `BoolValue` named `IsPrimary` set to `true` puts a stat first and takes precedence
  over `Priority`. A child `NumberValue` named `Priority` orders the rest (higher first,
  default 0).
- Hide the list during menus or cutscenes with
  `StarterGui:SetCoreGuiEnabled(Enum.CoreGuiType.PlayerList, false)` from a client script.
- Show 1–3 stats, the ones players compare: `Wins`, `Stage`, `Best`. Currency balances are
  a weak stat (inferred).
- Fill values from the loaded profile and update them through one `setStat(player, name, v)`
  function that changes the profile first. Never read game state back from a leaderstat: it's
  a display (inferred).

### Platform Friends/Global leaderboards

- Roblox now renders persistent **Friends** and **Global** views in the player list. The
  **Here** view keeps showing session `leaderstats` (official, 2026-10).
- Setup: register an `OrderedDataStore` that holds one numeric score per player, keyed by user
  ID (for example `tostring(player.UserId)`), in Creator Hub, then mark it the active
  leaderboard. Your server writes the scores; the platform only reads them. Deactivating hides
  the board but keeps the data (official, 2026-10).
- One active persistent leaderboard per experience (official, 2026-10). The docs still say
  beta; the DevForum announcement (2026-08-26) was updated on 2026-09-16 to say "now fully
  released" (official, 2026-09). Re-check status before relying on it.
- Staff advice: points-based games should give every player a default score on join, or the
  Friends/Global tabs can render squished (official, 2026-08).
- Not documented: sort direction, daily/weekly windows, a rank API. Developers report cropped
  names and truncated large numbers (community, 2026-09). Use it for your one headline
  all-time stat, usually `Wins` or `MaxStage`, and build time-based boards yourself.

### All-time boards: `OrderedDataStore` (official, 2026-10)

- Values must be integers. `GetSortedAsync(ascending, pageSize, minValue?, maxValue?)` returns
  pages. The default page size is 50, the maximum is 100, and `minValue`/`maxValue` must be
  integers.
- No versioning, no metadata, and no `userIds` argument on `SetAsync`/`IncrementAsync`. Keys are
  ≤ 50 characters.
- Default per-server budgets (requests/min): **OrderedList (`GetSortedAsync`) 5 + 2 × players**,
  OrderedWrite 30 + 5 × players, OrderedRead 60 + 40 × players. Experience-wide OrderedList is
  300 + 2 × CCU, shared with Open Cloud. A throttled `GetSortedAsync` fails with code 305.
- The list budget is the tight one. A 10-player server gets 25 `GetSortedAsync` calls a minute.
  Roblox's leaderboard tutorial has every client ask the server every 3 s, and the server calls
  `GetSortedAsync` each time (official, 2026-10). Ten clients would make 200 calls a minute,
  8× the budget (inferred math). Don't copy that loop.
- **Cadence (inferred):** one refresh loop per server per board, every 60–120 s with random
  jitter, top 50–100, cached in memory. Write a player's value only when it changed: on leave
  and every 2–5 min. Use `SetAsync` with the profile's value. The profile is session-locked, so
  there's no race and no need for `UpdateAsync` (which costs a read and a write).
- Huge values (simulator stats past 2^53) can't be stored exactly. Rank by a scaled log, such as
  `math.floor(math.log10(v) * 1e6)`, and display the profile's real value (inferred).

### Fastest-time boards

- Store milliseconds as positive integers and read with `GetSortedAsync(true, 50, 1)`:
  ascending, with `minValue = 1` to skip zero or empty entries. No inversion is needed for your
  own boards (inferred from the API).
- Only for a board that must sort descending (the platform view's direction isn't documented),
  store `CAP - ms`, with `CAP = 3_600_000` (1 hour), so values stay positive. Whether ordered
  stores accept negative integers isn't documented (unverified), so don't store `-ms`.
- Write only on a new personal best, which the profile's `BestTimeMs` decides.
- Per-map time boards need one store (or key prefix) per map, and each needs its own erasure
  template (see GDPR). The 100-template cap is a limit on map count (official limit, 2026-10;
  consequence inferred).
- Only validated runs count: server-timed start to finish, every checkpoint in order (see
  [checkpoints-and-respawn](checkpoints-and-respawn.md)), no skip-stage tokens used.

### Daily, weekly and live boards: memory store sorted maps (official, 2026-10)

- `MemoryStoreService:GetSortedMap(name)`. Items have a key, a value and an optional sort key
  (a number or a string up to 128 characters). Numeric sort keys order first, then strings,
  then items without one. Ties break by key.
- `SetAsync(key, value, expiration, sortKey)`. The maximum expiration is 3,888,000 s (45 days).
  `UpdateAsync(key, transform, expiration)` passes `(oldValue, oldSortKey)` to the transform,
  which returns `(newValue, newSortKey)`, or `nil` to cancel.
- `GetRangeAsync(direction, count, lowerBound?, upperBound?)`. `count` is at most 200, and the
  call costs one request unit per item returned (an empty result costs 1).
- Quotas: 1,000 + 120 × CCU request units/min and 64 KB + 1.2 KB × users of memory per
  experience; throttling starts around 30,000 units/min on one partition; at most 1,000,000
  items and 100 MB per structure. Shard by user-ID digits if a single map gets hot.
- Studio has the same limits, but its memory store data is isolated from production.
- **Period names:** `Wins_D_` .. `os.date("!%Y%m%d")` (UTC day). For weeks, use
  `(os.time() - 345600) // 604800`, which counts Monday-00:00-UTC weeks from the Unix epoch
  (inferred math). Expire entries after period + 1 day (daily 172,800 s, weekly 691,200 s), so
  old boards clean themselves up (inferred).
- Keep the period counter in the profile (`DailyWins` plus the `DailyKey` it belongs to; reset
  when the key changes) and mirror it with `SetAsync` on change, throttled to once per 30–60 s
  per player (inferred).
- Reads: one loop per server every 15–30 s, top 50. Fifty servers polling 50 items every 15 s
  spend 10,000 units/min on one map, a third of the per-partition throttle point (inferred math
  from official numbers). Poll slower or shard as you grow.
- Publish the reset time (`EndsAt` in server time) so clients can show "resets in 5h 12m" (see
  [round-system](round-system.md) for the countdown pattern).

### Display: lobby boards

- One `Part` per board in the lobby with a `SurfaceGui` (`SizingMode = PixelsPerStud`, about
  50 pixels per stud, `LightInfluence = 0` for readable text). Rows are built by a LocalScript
  with a `UIListLayout` (inferred).
- The server publishes each board as a JSON string attribute (`Top`) on
  `ReplicatedStorage.Leaderboards.<Board>`: rank, user ID, display name, score. Clients
  re-render on `GetAttributeChangedSignal("Top")`, and again when the board part streams back
  in (local changes are lost on stream-out; see
  [performance-and-devices](../../.claude/skills/roblox-map/references/performance-and-devices.md)) (inferred).
- Resolve names on the server with `Players:GetNameFromUserIdAsync(userId)`, as the official
  tutorial does, wrapped in `pcall`, cached per server for its lifetime (official, 2026-10;
  caching inferred). Headshots: client `ImageLabel.Image =
  "rbxthumb://type=AvatarHeadShot&id=" .. id .. "&w=48&h=48"` (unverified format).
- Show three things: top 10 with the top 3 highlighted, the viewer's own value from their
  profile ("Your best: 41.32 s"), and the time until reset. Neither store can tell you a
  player's rank outside the pages you fetch, so don't promise "You are #4,812" (inferred).
- Format numbers on the client: `1.2M`, `41.32 s`. Keep the stored value raw.

### Anti-cheat for scores

- Scores come only from server state. No remote ever takes a score, time or win count
  (official principle, 2026-10; see [security](../../.claude/skills/roblox-code/references/security.md)).
- Sanity floors and caps: reject runs faster than a floor per map (for example 80% of the
  developer's best run, or route length ÷ max `WalkSpeed`), and wins per hour above what round
  length allows. Flag them for review instead of auto-banning (inferred).
- Moderation: a server-only admin command that calls `RemoveAsync` on the entry (an
  OrderedRemove request) and sets `BoardBanned = true` in the profile. Writes skip flagged
  players (inferred).
- Studio playtests write to live stores. Skip leaderboard writes when `RunService:IsStudio()`,
  or use a test place (official, 2026-10; see [player-data](player-data.md)).

### GDPR and right to erasure (official, 2026-10)

- Ordered stores take no `userIds`, so automated erasure depends on the key. Add an `ORDERED`
  key template in Data Stores Manager: store name, `key_pattern` such as `{UserId}` or
  `User_{UserId}`, scope `global`. The token is case-sensitive; up to 100 templates.
- Templates match static names only. A store whose name changes daily (`WinsDaily_20261022`)
  can't be matched by one template (inferred from the docs). Keep periodic boards in memory
  stores with expiry under 30 days, inside the 30-day deletion window (inferred).
- Never key boards by username: usernames change, and erasure templates need the user ID
  (official key-pattern rule; reason inferred).
- Cached top-N lists and attributes refresh on their own within minutes; nothing else to purge
  (inferred).

## Implementation outline (server-authoritative)

- `ServerScriptService/Leaderboards`: owns the board config, the dirty-flag write loop, the
  refresh loops and the name cache. It reads values through `PlayerData.get(player)`.
- `ReplicatedStorage.Leaderboards`: one Folder per board with `Top` (JSON string) and `EndsAt`
  attributes.
- No client→server remotes. Clients only render.
- The leave-flush must run before the profile is released. Have the PlayerData module call
  `Leaderboards.flush(player)` inside its own `PlayerRemoving` handler, rather than relying on
  the order of two separate connections (inferred).

### Luau sketch: all-time board mirror and refresh (outline)

```lua
--!strict
-- ServerScriptService/Leaderboards: outline only (one all-time board, wins)
local DataStoreService = game:GetService("DataStoreService")
local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local PlayerData = require(script.Parent.PlayerData) -- get(player) -> Data? (player-data.md)

local WINS = DataStoreService:GetOrderedDataStore("Wins") -- registered in Creator Hub
local OUT = ReplicatedStorage:WaitForChild("Leaderboards"):WaitForChild("Wins") :: Folder
local WRITE_EVERY, REFRESH_EVERY, TOP_N = 180, 90, 50
local written: {[Player]: number} = {} -- last value we wrote
local names: {[number]: string} = {}

local function flush(player: Player)
	local data = PlayerData.get(player)
	if not data or RunService:IsStudio() or data.BoardBanned then return end
	if written[player] == data.Wins then return end -- unchanged: no request
	local ok = pcall(function() WINS:SetAsync(tostring(player.UserId), data.Wins) end)
	if ok then written[player] = data.Wins end
end

local function nameOf(userId: number): string
	local cached = names[userId]
	if cached then return cached end
	local ok, name = pcall(function() return Players:GetNameFromUserIdAsync(userId) end)
	local resolved = if ok and typeof(name) == "string" then name else "?"
	names[userId] = resolved
	return resolved
end

local function refresh()
	local ok, pages = pcall(function() return WINS:GetSortedAsync(false, TOP_N, 1) end)
	if not ok then return end -- throttled (305) or down: keep the old cache
	local rows = {}
	for rank, entry in (pages :: DataStorePages):GetCurrentPage() do
		local id = tonumber(entry.key)
		if id then table.insert(rows, {r = rank, id = id, n = nameOf(id), v = entry.value}) end
	end
	OUT:SetAttribute("Top", HttpService:JSONEncode(rows))
end

Players.PlayerRemoving:Connect(function(p) flush(p); written[p] = nil end)
task.spawn(function()
	task.wait(math.random() * REFRESH_EVERY) -- desync servers
	while true do refresh(); task.wait(REFRESH_EVERY) end
end)
task.spawn(function()
	while true do
		task.wait(WRITE_EVERY)
		for _, p in Players:GetPlayers() do task.spawn(flush, p) end
	end
end)
```

A daily board is the same shape with `MemoryStoreService:GetSortedMap("Wins_D_" .. dayKey)`,
`SetAsync(tostring(userId), data.DailyWins, 172800, data.DailyWins)` on change, and
`GetRangeAsync(Enum.SortDirection.Descending, 50)`, whose items carry `key`, `value` and
`sortKey`.

## Common bugs and exploits

| Bug | Cause | Fix |
|---|---|---|
| Player missing from the player list | Folder named `Leaderstats` or created on the client | Exactly `leaderstats`, created on the server (official, 2026-10) |
| Global board throttled, empty for everyone | `GetSortedAsync` per client request or per player join | One cached refresh loop per server (official limits, 2026-10) |
| Ordered write throttling | Writing on every coin or win | Dirty flag; write on leave and every 2–5 min |
| Values rejected | Decimals in an ordered store | Integers only: ms for times, scaled ints for big stats (official, 2026-10) |
| Fastest-time board shows the slowest first | Descending read of raw ms | `GetSortedAsync(true, …, 1)` |
| Zero times top the board | Default 0 entries in an ascending board | `minValue = 1`; write only real runs |
| Board names show "?" or stall the refresh | Uncached, unprotected name lookups | `pcall`, cache per server |
| Daily board never resets, or resets at local midnight | Local-time keys or no expiry | UTC `os.date("!…")` keys; expiration set |
| Erasure request can't be met | Usernames in keys, or date-named ordered stores | `{UserId}` key template; periodic boards in memory stores |
| Studio test scores on the live board | Studio writes go to production | Skip writes in Studio (official, 2026-10) |
| Exploiter at #1 | A remote reported the score, or no plausibility floor | Server-derived scores, floors, review, `RemoveAsync` |
| Friends/Global tabs look broken | No default score for new players | Write a default on join (official, 2026-08) |

## Checklist for agents

- [ ] `leaderstats` created on the server, 1–3 stats, `IsPrimary` on the headline stat, values
      mirrored from the profile.
- [ ] One headline all-time stat in an `OrderedDataStore` keyed by `tostring(UserId)`, and
      registered as the platform leaderboard if the feature is available.
- [ ] Ordered writes only when changed, on leave and every 2–5 min; reads via one cached loop
      per server, every 60–120 s with jitter, ≤ 100 per page.
- [ ] Times stored as positive integer ms and read ascending with `minValue = 1`.
- [ ] Daily/weekly boards in memory store sorted maps with UTC period names and expiration.
- [ ] Lobby `SurfaceGui` boards rendered on the client from a server-published attribute.
- [ ] No remote accepts a score; plausibility floors; moderation removal path.
- [ ] `ORDERED` erasure templates for every leaderboard store; no usernames in keys.
- [ ] Leaderboard writes disabled in Studio.

## Sources

1. https://create.roblox.com/docs/players/leaderboards: `leaderstats` rules, `IsPrimary`/`Priority`, hiding the PlayerList, persistent Friends/Global setup and limits
2. https://devforum.roblox.com/t/beta-add-persistent-friends-and-global-leaderboards-easily/4832224: announcement (2026-08-26), "fully released" update (2026-09-16), default-score advice, one active board, reported display issues
3. https://create.roblox.com/docs/reference/engine/classes/OrderedDataStore: integers only, page size default 50 / max 100, no versioning, metadata or `userIds`
4. https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits: ordered per-server and experience-wide budgets, error 305, 50-character keys, integer min/max
5. https://create.roblox.com/docs/cloud-services/data-stores: ordered stores for persistent leaderboards, `GetSortedAsync` paging
6. https://create.roblox.com/docs/tutorials/use-case-tutorials/data-storage/create-leaderboard: tutorial (3 s client poll, `GetNameFromUserIdAsync`, caching delay, memory stores for instant updates)
7. https://create.roblox.com/docs/cloud-services/memory-stores: quotas, per-item request units, 1M items / 100 MB, partition throttling, sharding, Studio isolation
8. https://create.roblox.com/docs/cloud-services/memory-stores/sorted-map: sort-key ordering and ties, 128-character keys, 32 KB values, `UpdateAsync` retries, leaderboard example
9. https://create.roblox.com/docs/reference/engine/classes/MemoryStoreSortedMap: `GetRangeAsync` count ≤ 200, 45-day expiration, transform signature
10. https://create.roblox.com/docs/cloud-services/data-stores/right-to-be-forgotten: `ORDERED` key templates, static patterns, `{UserId}` token, 100 templates

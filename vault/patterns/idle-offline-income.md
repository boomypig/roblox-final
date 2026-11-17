---
title: Idle and offline income
type: pattern
read-when: Adding passive or offline income.
last-researched: 2026-10-22
---

# Idle and offline income

## What it is

Two related systems:
- **Passive income:** the server credits currency every tick from what the player owns
  (generators, droppers, brainrots, pets), with no click needed.
- **Offline income:** on join, the server computes what the player's setup would have earned since
  they left, applies a rate and a cap, and holds it for the player to claim on a "welcome back"
  screen.

Timers work the same way: a crop, egg or restock stores an absolute `ReadyAt` timestamp, so it
finishes whether or not the player is online.

## Why it works

- "Something finishes while they're away" is a core D1 return reason. Roblox guidance says timers
  should produce something, not block play (official, 2026-10). See
  [retention](../fundamentals/retention.md).
- **Play days** per user, over D1, D2–7 and D8–28, are a top Home recommendation signal. Playtime
  counts only up to **60 min per user per day** (official, 2026-10). Offline income buys return
  days, which count, rather than idle hours, which don't. See
  [discovery](../fundamentals/discovery-algorithm.md).
- A cap creates an appointment: "storage fills in 8 h" tells the player when to come back
  (inferred).
- Grow a Garden, the 2025 concurrency record-holder, lets crops keep growing while the player is
  offline (press, 2025).

## Genres that use it

[Idle/incremental](../genres/idle-incremental.md), [tycoon](../genres/tycoon.md),
[steal-a-x](../genres/steal-a-x.md) (brainrots that earn while away),
[farming/growing](../genres/farming-growing.md), [pet/egg collection](../genres/pet-egg-collection.md)
(hatch timers), [simulator](../genres/simulator.md).

## Design rules

### Real numbers from shipped games

| Game | Offline rate | Cap | Source |
|---|---|---|---|
| Cookie Clicker | 5% of production for 1 h after buying the first heavenly upgrade; drops to 0.5% after that. Upgrades reach 91% for 7 days 8 hours | see rate | community wiki |
| Egg, Inc. (now) | 50% with the standard permit, 100% with the paid pro permit | 1 h per silo; 2 silos (standard) or 10 (pro); research adds 6 min per level per silo, up to +2 h | community wiki |
| Egg, Inc. (2017) | n/a | 2 h | community, 2017-02 |
| Grow a Garden | Crops grow at full speed | none reported | press, 2025 |
| Sell Lemons (Roblox) | "100% of their income" offline | none stated | unverified SEO wiki |

In these games, the cap and the rate are progression rewards themselves: start stingy, then let
upgrades, prestige or a pass extend them (community wiki; the pattern is inferred).

### Recommended defaults (inferred)

| Parameter | Default | Range | Reason |
|---|---|---|---|
| Offline rate | 50% of online income | 25–100% | Playing should beat idling per hour, so sessions still matter |
| Base cap | 8 h | 2–12 h | Fills over a school day or a night; one claim per half-day |
| Cap with upgrades or pass | 24 h | ≤ 48 h | Supports a once-a-day player without paying for weeks away |
| Minimum time away for a payout | 5 min | 1–10 min | No popup on server hops or quick rejoins |
| Size of a full-cap payout | buys the next 1–3 meaningful upgrades | — | A reason to log in, not a skip past content |

**Worked example (inferred):** online income 1,000/s, rate 50%, cap 8 h.

| Time away | Credited time | Payout | Equal to active play |
|---|---|---|---|
| 3 min | 0 (below minimum) | 0 | — |
| 45 min | 45 min | 1.35M | 22.5 min |
| 3 h | 3 h | 5.4M | 1.5 h |
| 8 h | 8 h | 14.4M | 4 h |
| 3 days | 8 h (capped) | 14.4M | 4 h |

If costs grow 1.15× per level ([upgrade trees](upgrade-trees.md)), a 4-hour-equivalent payout buys
about `log(payout/cost)/log(1.15)` levels of one generator, typically 5–15. Check that number in
playtests; if it skips a whole zone, lower the rate or the cap (inferred).

### Offline income is a return reason, not an idle reason

- Roblox's `Player.Idled` fires after about 2 minutes without input, and idle players are
  disconnected after 20 minutes (official, 2026-10). Progress that requires staying in the server
  pushes players to auto-clickers and anti-AFK scripts (inferred).
- Never pay more for AFK-in-server than for offline. Otherwise players leave clients running
  overnight, which adds nothing past the 60-min playtime cap (inferred).
- Make the claim the start of a session: after claiming, show "You can now afford: X, Y" and the
  next goal (inferred). Bounce rate is measured on first sessions of new players only, so a short
  claim-and-leave visit from a returning player doesn't count as a bounce (official definition,
  2026-10; the conclusion is inferred).
- Pair a full cap with a notification. One personal Experience Notification per day, such as
  "your vault is full", is the allowed maximum (official, 2026-10). See
  [retention](../fundamentals/retention.md).
- Don't punish absence: no decay, no theft of offline earnings from players who are away (inferred;
  retention anti-patterns). For steal-a-x, see [base defense](base-defense-and-stealing.md).

### Welcome-back screen

- Show: time away (and "capped at 8 h" if it hit the cap), the amount, and a big **Claim** button.
  Show it after the loading screen, when the player can act (inferred).
- When the cap was hit, say so and point to the upgrade that raises it. That turns a loss into a
  goal (inferred).
- An optional "×2 claim" developer product is the standard idle upsell. Grant it only in
  `ProcessReceipt` (official, 2026-10). Keep it optional and never time-pressured (official,
  2026-10). See [monetization](../fundamentals/monetization.md).
- New players (no `LastSeen`) see no popup.

### Monetization levers (inferred unless noted)

- Game pass: offline rate 50% → 100% (Egg, Inc.'s paid permit doubles the offline rate and raises
  the silo count, community wiki).
- Upgrade tree or prestige shop nodes: +1 h cap per level.
- Don't sell a product that pays offline income on demand. It's a currency pack disguised as a
  timer.

## Implementation outline (server-authoritative)

### Time source

- `os.time()` returns seconds since the Unix epoch in UTC, read from **the device's local clock**
  (official, 2026-10). On the server that's Roblox's machine; on a client it's whatever the player
  set. Only ever read it on the server.
- `DateTime.now()` also uses the device's local clock (official, 2026-10). Same rule.
- `Workspace:GetServerTimeNow()` is for syncing client visuals with the server. The docs say it is
  "not suitable for things like timed rewards" (official, 2026-10).
- `DataStoreKeyInfo.UpdatedTime` is the key's last write time in milliseconds since epoch, recorded
  by Roblox (official, 2026-10). A hand-rolled loader gets it from `UpdateAsync`'s callback; it's
  an optional cross-check on `LastSeen`.
- Clock changes on the player's device have no effect, because no client time is ever read
  (inferred). Clamp negative elapsed time to 0 anyway: different servers' clocks can disagree by a
  little (inferred).

### Data and flow

- Save fields: `LastSeen: number` (server `os.time()`), `PendingOffline: number`, and timers as
  absolute `ReadyAt` timestamps (`os.time() + duration`), never as "seconds remaining".
- Update `LastSeen` **on every autosave** and on leave, not only on leave. If only the leave save
  wrote it and that save failed, the next join would pay the online time again (inferred).
- On load: compute the payout, move `LastSeen` to now, and add the payout to `PendingOffline` in the
  same in-memory step. The next save stores both, so a crash before claiming can't lose or double
  it (inferred).
- Compute income from the saved setup with **current** balance values, then cap. Never store an
  "income per second" the client could have influenced.
- Session locking ([player data](player-data.md)) guarantees two servers never run the same
  player, so offline time can't overlap online time elsewhere (official, 2026-10).
- Passive income while online: one server loop (e.g., every 1 s) credits all players from server
  state. Don't spawn a loop per player or per generator (inferred). See
  [conveyor and dropper economy](conveyor-dropper-economy.md).

```lua
--!strict
-- ServerScriptService/OfflineIncome: outline only, not drop-in
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local PlayerData = require(script.Parent.PlayerData)   -- player-data.md; calls onLoaded after load
local RateLimit = require(script.Parent.RateLimit)     -- token bucket (security file)
local Economy = require(ReplicatedStorage.Shared.Economy) -- incomePerSecond, offlineCap, offlineRate

local WelcomeBack = ReplicatedStorage.Remotes.WelcomeBack :: RemoteEvent
local ClaimOffline = ReplicatedStorage.Remotes.ClaimOffline :: RemoteEvent
local MIN_AWAY = 300

local OfflineIncome = {}

function OfflineIncome.onLoaded(player: Player, data: PlayerData.Data)
	local now = os.time() -- server clock only
	local last = data.LastSeen
	data.LastSeen = now
	if last == nil then return end -- first visit: no popup
	local away = math.clamp(now - last, 0, Economy.offlineCap(data)) -- seconds
	if away < MIN_AWAY then return end
	local amount = away * Economy.incomePerSecond(data) * Economy.offlineRate(data)
	if not math.isfinite(amount) or amount <= 0 then return end
	data.PendingOffline += amount
	WelcomeBack:FireClient(player, away, data.PendingOffline)
end

function OfflineIncome.beforeSave(data: PlayerData.Data) -- call from autosave and on leave
	data.LastSeen = os.time()
end

ClaimOffline.OnServerEvent:Connect(function(player: Player) -- no arguments accepted
	if not RateLimit.take(player, "ClaimOffline") then return end
	local data = PlayerData.get(player)
	if not data or data.PendingOffline <= 0 then return end
	data.Cash += data.PendingOffline
	data.PendingOffline = 0
end)

return OfflineIncome
```

Timers need no offline code: `isReady = os.time() >= plot.ReadyAt`. Send `ReadyAt` to the client
and let it count down with `Workspace:GetServerTimeNow()` for display only (official API; usage
inferred).

## Common bugs and exploits

| Bug or exploit | Cause | Fix |
|---|---|---|
| Infinite money by changing the device date | Client-sent timestamp, or client `os.time()`/`DateTime.now()` | Read time only on the server (official, 2026-10) |
| Online time paid again as offline | `LastSeen` written only on leave; that save failed | Write `LastSeen` on every autosave (inferred) |
| Payout lost or doubled on crash | Credited straight to cash before a save; or recomputed on next join | `PendingOffline` field, `LastSeen` moved in the same step (inferred) |
| Rejoin farming the popup | Each join pays something regardless of time away | Pay strictly by elapsed time, with a minimum away (inferred) |
| Economy-breaking payout after weeks away | No cap, or the cap is applied after multiplying | `math.clamp` elapsed time first (inferred) |
| Negative or NaN payout | Server clock skew; uninitialized `LastSeen` | Clamp at 0; `math.isfinite`; skip if `LastSeen` is nil (official for isfinite) |
| Timer resets when the player leaves | Saved "seconds remaining" | Save absolute `ReadyAt` (inferred) |
| Lag from per-generator loops | `while true` per dropper or per player | One server tick for all players (inferred) |
| Double-claim via remote spam | Claim handler yields before zeroing | Rate limit; credit and zero in one step (official principle, 2026-10) |
| Offline payout on data that failed to load | Ran before `canSave` was known | Run only after a successful load ([player data](player-data.md)) |

## Checklist for agents

### Do
- Compute offline time on the server with `os.time()` and saved `LastSeen`.
- Update `LastSeen` on every autosave and on leave.
- Apply `math.clamp(elapsed, 0, cap)` before multiplying; check `math.isfinite`.
- Hold the payout in `PendingOffline` until the player claims it.
- Store timers as absolute `ReadyAt` timestamps.
- Start at 50% rate and an 8 h cap; let upgrades or a pass raise them.
- After the claim, show what the player can now afford and the next goal.
- Use one server income tick for all players.

### Don't
- Don't read any time value from a client or from `GetServerTimeNow()` for rewards.
- Don't pay more for staying AFK in a server than for being offline.
- Don't let offline income skip whole zones or rebirths.
- Don't decay, steal or expire what accumulated while the player was away.
- Don't show the welcome-back popup to brand-new players or after short hops.

## Sources

1. https://create.roblox.com/docs/reference/engine/libraries/os.md: `os.time` is UTC epoch seconds from the device's local clock; `os.clock` monotonic
2. https://create.roblox.com/docs/reference/engine/datatypes/DateTime.md: `DateTime.now` uses the local clock; `UnixTimestamp` range
3. https://create.roblox.com/docs/reference/engine/classes/Workspace.md: `GetServerTimeNow` is for sync, "not suitable for things like timed rewards"
4. https://create.roblox.com/docs/reference/engine/classes/DataStoreKeyInfo.md: `UpdatedTime` in ms since epoch
5. https://create.roblox.com/docs/discovery: play days, 60-min/day playtime cap, bounce definition
6. https://create.roblox.com/docs/production/analytics/retention: timers that produce rewards as D1 hooks
7. https://create.roblox.com/docs/reference/engine/classes/Player.md: `Idled` and the 20-minute idle disconnect
8. https://create.roblox.com/docs/cloud-services/experience-notifications: one notification per user per day
9. https://cookieclicker.wiki.gg/wiki/Prestige: offline production 5% for 1 h, up to 91% for 7 d 8 h
10. https://egg-inc.fandom.com/wiki/Grain_Silo: 1 h per silo, permit silo counts and offline rates, Silo Capacity research
11. https://www.gamedeveloper.com/design/the-math-of-idle-games-part-iii: Egg, Inc. 2 h offline cap (2017-02)
12. https://esports.gg/news/roblox/grow-a-garden-breaks-blox-fruits-record-for-most-concurrent-users-on-roblox/: Grow a Garden crops grow offline (2025)
13. https://bloxinformer.com/wikis/sell-lemons/: Sell Lemons 100% offline income claim (unverified)
14. https://devforum.roblox.com/t/how-to-setup-a-time-counter-offline/3942628: community timestamp-on-leave pattern

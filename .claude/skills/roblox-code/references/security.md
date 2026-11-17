---
title: Security and anti-exploit
type: fundamental
read-when: Writing any RemoteEvent/RemoteFunction handler or server validation.
last-researched: 2026-10-22
---

# Security and anti-exploit

## In one line

The client is a hostile input device. It sends intents, the server checks every argument and
game rule, then decides and replicates. Anything the server doesn't check, an exploiter controls.

## What an exploiter controls

Assume a cheater can (official, 2026-10):
- Read and decompile every replicated LocalScript and ModuleScript, even ones that never run on
  the client. Secrets in `ReplicatedStorage` are public.
- Fire any `RemoteEvent`/`RemoteFunction` at any rate with any arguments. Only the first
  argument, the `Player`, is filled in by the engine and can't be faked.
- Own the physics of their character and nearby unanchored parts. They can move them anywhere,
  through walls and through the air, and the server can't verify the physics.
- Fire `Touched` on parts they own, and trigger `ProximityPrompt` and `ClickDetector` at any
  distance or rate.
- Change their local DataModel (WalkSpeed, GUIs, local values) without firing the events you
  expect.

The 64-bit Windows client has shipped Hyperion anti-tamper since 2023-05 (press). Exploit and
ban-evasion tools still circulate (community, 2025-06). Server checks are the only defence you
control (inferred).

## Where code and data live

- Game rules, prices, drop tables, reward amounts and admin lists go in `ServerScriptService` or
  `ServerStorage`. Clients get display copies only (official, 2026-10).
- Never `require` a module or load an asset by a name or path the client sent (official, 2026-10).
- Don't build generic remotes such as `SetValue(instance, value)`, `DeleteObject(path)` or
  `GiveCash(amount)`. Each remote names one player intent: `RequestBuy(itemId)`, `RequestSwing()`
  (official guidance; naming inferred).
- Use one remote per message type, and separate client→server from server→client remotes. Each
  handler then has one argument shape to validate and one rate limit (inferred).

## Remote validation pipeline

Run these checks in this order on every `OnServerEvent`/`OnServerInvoke`, and drop the call at
the first failure:

| # | Check | How | Tag |
|---|---|---|---|
| 1 | Rate | Per-player token bucket per remote (next section) | official, 2026-10 |
| 2 | Types | `typeof(x) == "number"`/`"string"`/`"Vector3"`/`"Instance"`. Use `typeof`, not `type`, for Roblox types. A table can pose as an Instance with fake `Name`/`ClassName` fields. | official, 2026-10 |
| 3 | Numbers | `math.isfinite(x)` rejects NaN and ±inf. NaN fails every `<`/`>` test, so it slips past range checks. For integers, check `x % 1 == 0`. Clamp to a range. | official, 2026-10 |
| 4 | Strings | Cap the length (`#s <= N`) and require `utf8.len(s) ~= nil` (valid UTF-8, which DataStores need). | official, 2026-10 |
| 5 | Tables | Prefer not to accept them. If you must, iterate every key and value, reject unknown keys and NaN keys, and cap the count. | official, 2026-10 |
| 6 | Instances | `inst:IsA("Model")` plus `inst:IsDescendantOf(expectedFolder)`. Better: accept a string ID and look it up on the server. | official, 2026-10 |
| 7 | Ownership | The item, plot, pet or tool belongs to this player in server data. | inferred |
| 8 | State | Data loaded, character exists, `Humanoid.Health > 0`, not stunned, in the right round or zone, permission checked against a server-set attribute | official, 2026-10 |
| 9 | Range | `(root.Position - target).Magnitude <= limit + slack`. Allow a few studs for latency. | official, 2026-10 |
| 10 | Cooldown and cost | Server-side timestamp per action. Price and currency come from server data, never from arguments. | official, 2026-10 |
| 11 | Act, then replicate | Mutate server state, then `FireClient`/`FireAllClients` the result. Never relay raw client input to other clients. | official, 2026-10 |

## Rate limiting

- The engine throttles client→server traffic at ~500 requests/s per client, shared by all
  RemoteEvents (UnreliableRemoteEvents have their own pool). Excess `RemoteEvent` calls are queued
  and processed later, so the throttle protects the engine, not your game logic (official, 2026-10).
- Give each remote its own per-player token bucket, with a capacity (burst) and a refill rate.
  Roblox's sample uses `TokenBucket.new(5, 10)`: a burst of 5, refilling one token every 2 s
  (official, 2026-10).
- Rate-limit everything a client can trigger: remotes, `Touched` handlers, `ProximityPrompt`,
  `ClickDetector`, `DragDetector` (official, 2026-10). Limit hardest the handlers that call
  DataStores, BadgeService or teleports, clone large models, grant currency, or update every
  client's GUI (official, 2026-10).
- Client-side cooldowns are UX only (official, 2026-10).
- Over budget: drop the call silently and count a strike. Act on repeated strikes, not on one
  (inferred: network bursts after lag spikes cause legitimate overruns).
- Clear buckets on `Players.PlayerRemoving` to avoid leaks (official, 2026-10).

## RemoteFunction pitfalls

- **Never `InvokeClient` from the server.** If the client never returns, the server thread waits
  forever. If the client errors or disconnects, the server call throws (official, 2026-10). An
  exploiter can hang any server logic waiting on it.
- To ask a client something, `FireClient` a request, accept the reply on a separate RemoteEvent,
  and time out after a few seconds (inferred).
- Client→server `InvokeServer` is fine for request/response flows such as "buy, then show the
  result". The handler must validate like any remote and should not yield for long (inferred).
- Arguments are copied: functions arrive as nil and metatables are stripped. Never accept
  client-built objects (official, 2026-10).

## Validated remote sketch

```lua
--!strict
-- ServerScriptService/ShopServer: outline, not drop-in
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Catalog = require(script.Parent.Catalog) -- server-only: {[string]: {price: number, shopPos: Vector3}}
local PlayerData = require(script.Parent.PlayerData) -- returns nil until data has loaded

local RequestBuy = ReplicatedStorage.Remotes.RequestBuy :: RemoteEvent
local CAPACITY, REFILL_PER_SEC, MAX_SHOP_DIST = 5, 0.5, 15
local buckets: {[Player]: {tokens: number, last: number}} = {}

local function take(player: Player): boolean
	local now = os.clock()
	local b = buckets[player] or {tokens = CAPACITY, last = now}
	buckets[player] = b
	b.tokens = math.min(CAPACITY, b.tokens + (now - b.last) * REFILL_PER_SEC)
	b.last = now
	if b.tokens < 1 then return false end
	b.tokens -= 1
	return true
end

RequestBuy.OnServerEvent:Connect(function(player: Player, itemId: unknown, qty: unknown)
	if not take(player) then return end
	if typeof(itemId) ~= "string" or #itemId > 32 then return end
	if typeof(qty) ~= "number" or not math.isfinite(qty) or qty % 1 ~= 0 then return end
	if qty < 1 or qty > 10 then return end
	local item = Catalog[itemId]
	if not item then return end
	local data = PlayerData.get(player)
	if not data then return end
	local char = player.Character
	local root = if char then char:FindFirstChild("HumanoidRootPart") :: BasePart? else nil
	if not root or (root.Position - item.shopPos).Magnitude > MAX_SHOP_DIST then return end
	local cost = item.price * qty -- price from the server catalog, never from the client
	if data.Coins < cost then return end
	data.Coins -= cost
	data.Items[itemId] = (data.Items[itemId] or 0) + qty
end)

Players.PlayerRemoving:Connect(function(p) buckets[p] = nil end)
```

## Common exploits and fixes

| Exploit | Fix |
|---|---|
| Speed, fly, teleport | **Option A:** set `Workspace.AuthorityMode = Server`. Server Authority reached full release on 2026-07-09. It's opt-in, and the server simulates movement from client inputs and rejects speed and fly hacks (official, 2026-07). It requires `StreamingEnabled`, `NextGenerationReplication`, `SignalBehavior = Deferred`, `UseFixedSimulation` and `PlayerScriptsUseInputActionSystem`, all set automatically; core logic must move to `RunService:BindToSimulation()` with `InputAction` input. Known limits at release: max 8 active animation tracks per Animator, 64 replicated attributes per instance, slightly higher server CPU (official, 2026-07). Best for competitive movement, vehicles and sports; skip it for casual games. **Option B:** every 0.25–0.5 s on the server, compare `HumanoidRootPart` displacement with `WalkSpeed × dt × 1.25 + 4` studs, track time airborne, and pull violators back to their last valid position (community pattern; numbers inferred). |
| Teleport false positives | When the server moves a player (spawn, teleport pad, cutscene), set a grace window and reset the last valid position. Exempt seats, vehicles, moving platforms and knockback, and allow more slack at high ping (community). |
| Noclip | Raycast with `Workspace:Raycast()` from the last valid position to the current one against static geometry only (a `RaycastParams` filter). On a hit, pull the player back (community). |
| Remote spam / server lag | Token bucket per remote. Cap payload sizes. Never let one call trigger unbounded work, such as cloning a large model per call (official, 2026-10). |
| Auto-farm, autoclickers | Server cooldowns per action. Server-computed rewards with a cap per minute. Require proximity to the resource. Log earn rates far above the 99th percentile for review, not auto-ban (inferred). AFK grinding that follows your rules is a design issue, not an exploit (inferred). |
| Currency or item injection | No remote takes an amount to grant. The server derives every reward from server state (official, 2026-10). |
| Dupes via trades | Both inventories are checked and swapped in one server-side step, then both players are saved right away. Reject the trade if either profile isn't loaded and locked. Make it all-or-nothing and roll back on any failure (official, 2026-10). See [trading](../../../../vault/patterns/trading.md). |
| Dupes via leave or rejoin timing, or a crash | Session-lock player data so a second server can't load stale data before the first saves (official, 2026-10). See [player data](../../../../vault/patterns/player-data.md). |
| Purchase spoofing | Grant developer products only in `MarketplaceService.ProcessReceipt` or `MarketplaceService:BindReceiptHandler()`, deduplicated by `PurchaseId`. `PromptProductPurchaseFinished` firing does not mean a purchase happened. Check passes on the server with `UserOwnsGamePassAsync` (official, 2026-10). See [monetization](../../../../vault/fundamentals/monetization.md). |
| Combat hit spoofing | The client sends shot origin, direction or hit position, and the claimed target. The server checks: origin near the server-side character (latency slack); hit point near the target part; a raycast for static obstructions only; fire rate, ammo, reload or sprint state, target alive, team (official, 2026-10). Melee: server range and angle check, server cooldown. See [ability kits](../../../../vault/patterns/ability-kits.md). |
| `Touched` spoofing | A client can fire `Touched` for parts it owns. Re-check distance and state on the server before rewarding (official, 2026-10). |
| ProximityPrompt / ClickDetector abuse | The server doesn't enforce `Enabled`, `MaxActivationDistance`, `HoldDuration` or line of sight; only `Triggered` gets a server distance check. ClickDetector gets none. Re-check enabled state, distance, alive status and a minimum hold time on the server (official, 2026-10). |
| Flinging other players or objects | Anchor critical parts, or call `SetNetworkOwner(nil)` on unanchored gameplay objects (official, 2026-10). |
| Deleting own character parts | Keep `Workspace.RejectCharacterDeletions` at `Default` (currently behaves as `Enabled`) (official, 2026-10). |

## Server checks vs client anti-cheat

- A client anti-cheat runs on the exploiter's machine, where they can delete, hook or skip it. At
  best it adds friction and cheap telemetry (official principle "never trust the client",
  2026-10).
- Server checks can't be bypassed, because they read only server state. Spend effort there
  first, and keep client detection to non-critical signals (inferred).
- Validate outcomes rather than inputs where you can. "Did this player gain more than X coins
  per minute?" catches exploits you didn't foresee (inferred).
- Before shipping a feature, ask what happens if a remote fires 1,000+ times a second, and
  whether it could hurt other players (official, 2026-10).

## Respond: drop, correct, log, kick, ban

1. **Drop** invalid calls silently. Don't tell the exploiter which check failed (inferred).
2. **Correct** state: rubber-band position, revert inventory (inferred).
3. **Log** strikes per player in memory, and save serious flags (for example to a `Flags`
   DataStore keyed by UserId) with context: remote, args summary, server JobId (inferred).
4. **Kick** with `player:Kick("reason")` for clear but non-fatal abuse (inferred).
5. **Ban** with `Players:BanAsync(config)` (official, 2026-10):
   - Fields: `UserIds` (max 50 per call), `Duration` in seconds (`-1` = permanent; `0` is
     invalid), `DisplayReason` (≤ 400 chars, filtered, shown to the user), `PrivateReason`
     (≤ 1,000 chars, never sent to clients), `ApplyToUniverse` (default true),
     `ExcludeAltAccounts` (default false, so suspected alts are banned too), `ApplyDeviceBlock`
     (blocks the device for 24 h).
   - Server only. It makes an HTTP call that can throttle or fail, so wrap it in `pcall` and retry.
     It's enabled by the `Players.BanningEnabled` property, set in Studio. Studio bans never
     reach production.
   - Escalate repeat offenders using `Players:GetBanHistoryAsync(userId)`. Undo with
     `Players:UnbanAsync`.
   - Post your rules and an appeal path (official, 2026-10). Auto-ban only on signals that are
     impossible in legitimate play, such as a remote argument no client code ever sends. Send
     heuristic hits (speed, earn rate) to review or temp bans (inferred).
   - Alt detection is best-effort, and evasion is reported (community, 2025-06).

## Review checklist for any RemoteEvent handler

- [ ] Handler lives in a server Script under `ServerScriptService`.
- [ ] Per-player rate limit, with buckets cleared on `PlayerRemoving`.
- [ ] Every parameter typed as `unknown` and checked with `typeof`.
- [ ] Numbers pass `math.isfinite`, integer and range checks. Strings are length-capped and valid
      UTF-8.
- [ ] No Instance, path or module name from the client is used without a whitelist or
      `IsDescendantOf` check.
- [ ] Ownership, alive state, data-loaded, distance, cooldown and cost checked from server state.
- [ ] No amount, price, damage or reward value is read from the client.
- [ ] Bounded work per call: no unbounded loops, clones or DataStore calls.
- [ ] Results replicated from server state. Raw input is never relayed.
- [ ] No `InvokeClient`. Any `OnServerInvoke` returns quickly.
- [ ] Failures drop silently and count a strike.

## Checklist for agents

### Do
- Name remotes after intents and keep all rules and values on the server.
- Run the validation pipeline in order, with one token bucket per remote.
- Use server-side distance and cooldown with latency slack, and reset the last valid position
  after server-initiated moves.
- Consider `AuthorityMode = Server` for competitive movement, sports or racing games.
- Grant purchases only through `ProcessReceipt`/`BindReceiptHandler`, keyed by `PurchaseId`.
- Session-lock data and save both sides immediately after trades.
- Log strikes and escalate from drop to kick to `BanAsync`, with an appeal path.

### Don't
- Don't trust client-sent amounts, prices, damage, positions-as-truth or "I hit X" without checks.
- Don't call `RemoteFunction:InvokeClient` from the server.
- Don't put secrets or server logic in `ReplicatedStorage` or LocalScripts.
- Don't rely on client anti-cheat, client cooldowns or disabled UI buttons for security.
- Don't use `PromptProductPurchaseFinished` to grant purchases.
- Don't auto-ban on a single noisy heuristic.

## Related

- [player-data.md](../../../../vault/patterns/player-data.md): session locking, dupe prevention
- [trading.md](../../../../vault/patterns/trading.md): atomic trades
- [monetization.md](../../../../vault/fundamentals/monetization.md): receipts and passes
- [ability-kits.md](../../../../vault/patterns/ability-kits.md): combat validation
- [performance-and-devices.md](../../roblox-map/references/performance-and-devices.md): network ownership and remote budgets

## Sources

1. https://create.roblox.com/docs/scripting/security/security-tactics: exploiter capabilities, "never trust the client", threat-model questions
2. https://create.roblox.com/docs/scripting/security/client-server-boundary: type, NaN, string and instance checks, token bucket sample, hit validation, ProximityPrompt/ClickDetector gaps, trade dupes
3. https://create.roblox.com/docs/scripting/events/remote: argument copying, InvokeClient failure modes
4. https://create.roblox.com/docs/reference/engine/classes/RemoteEvent: ~500 req/s per-client throttle
5. https://create.roblox.com/docs/reference/engine/classes/UnreliableRemoteEvent: separate pool, drop behavior
6. https://create.roblox.com/docs/physics/network-ownership: ownership exploits, SetNetworkOwner, Touched
7. https://create.roblox.com/docs/projects/server-authority: AuthorityMode, BindToSimulation, prerequisites
8. https://devforum.roblox.com/t/full-release-ship-fair-and-competitive-games-with-server-authority/4727993: full release 2026-07-09, limits
9. https://create.roblox.com/docs/reference/engine/classes/Players: BanAsync fields, limits, BanningEnabled, GetBanHistoryAsync
10. https://create.roblox.com/docs/reference/engine/classes/MarketplaceService: ProcessReceipt, BindReceiptHandler, PromptProductPurchaseFinished warning
11. https://create.roblox.com/docs/reference/engine/classes/Workspace: RejectCharacterDeletions
12. https://create.roblox.com/docs/reference/engine/libraries/math: math.isfinite
13. https://devforum.roblox.com/t/roblox-ban-api-being-bypassed/3753671: alt-detection evasion reports (2025-06)
14. https://devforum.roblox.com/t/hexolus-server-sided-anticheat/983706: server-side predict/measure/correct movement checks (2021-01)
15. https://devforum.roblox.com/t/server-sided-anticheat/2135105: velocity checks, raycast noclip, lenient thresholds, strikes, pull back before kick (2023-01)
16. https://itsfoss.com/news/roblox-linux-end/: Hyperion anti-cheat arrived with the 64-bit Windows client (2023-05)

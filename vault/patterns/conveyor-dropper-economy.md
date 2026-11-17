---
title: Conveyor and dropper economy
type: pattern
read-when: Adding droppers, conveyors, or collectors.
last-researched: 2026-10-22
---

# Conveyor and dropper economy

## What it is

The classic tycoon loop. A player owns a **plot**. Stepping on **purchase pads** (buttons) in a set
order builds the plot out. **Droppers** emit drops that ride **conveyors** through **upgraders**
(which raise each drop's value) into a **collector** (furnace), which adds the value to a plot bank.
The player collects the bank and buys the next pad. Sandbox tycoons (Miner's Haven) let players
place the machines freely, so the layout itself is the puzzle (community, 2019).

The key engineering choice: are drops **physical server parts** or **simulated values** with
client-only visuals?

## Why it works

- Every purchase is visible: the plot grows around the player, so progress reads at a glance and is
  easy to show to friends (inferred).
- The build order is a guided tutorial: the next pad is always the next goal, with no menus
  (inferred).
- Watching drops flow into the collector is a constant small reward between purchases (inferred).
- A finished plot sets up a [rebirth](rebirth-prestige.md): Miner's Haven destroys placed items on
  rebirth and starts the player over with a starter kit (community, 2019).

## Genres that use it

[Tycoon](../genres/tycoon.md) (core), [steal-a-x](../genres/steal-a-x.md) (bases with collect pads),
[idle/incremental](../genres/idle-incremental.md), [job sims](../genres/job-sims.md) (production
lines), [farming/growing](../genres/farming-growing.md) (plots and claim pads).

## Design rules

### Physical vs simulated drops

| | Physical server parts | Simulated value + client visuals (default) |
|---|---|---|
| Economy | `Touched` on upgraders and collector | Server tick: `income = Σ dropper rate × value × upgrader multipliers` |
| Network | Every drop replicates to every client | Nothing per drop; clients derive visuals from plot state |
| Server cost | Physics for every live drop | One loop over plots per tick |
| Exploits | Client-owned parts can fire `Touched` (official, 2026-10) | No client input in the economy |
| Visual count | Uncapped unless you cap it | Capped per client, nearby plots only |
| Use when | Layout is the gameplay (sandbox tycoon) | Fixed-layout button tycoons |

- **Load estimate:** live drops per plot ≈ droppers × drops per second × seconds on the belt. Ten
  droppers at 1 drop/s with a 15 s ride is 150 parts per plot; 8 plots is 1,200 physics parts
  replicated to every client (inferred arithmetic).
- A tycoon server froze for 4–5 s, then spat out a burst of bricks. Replies suggested spawning
  bricks only on clients, capped at about 200 rendered per client, with droppers on the server
  just adding money (community, 2019-11).
- If drops must be physical, anchor-free drops need `BasePart:SetNetworkOwner(nil)` so clients can't
  push them around (official, 2026-10), a hard cap per plot, and cleanup after a lifetime
  (`Debris:AddItem(drop, 20)`). A DevForum reply instead suggested making the plot owner the network
  owner; that lets the owner move drops into the collector, so don't (community suggestion; risk
  inferred).
- Mass spawning and removal at once (a player leaves and their whole plot is destroyed) causes lag
  spikes. Stagger it with small waits (community, 2019-11).

### Values and upgraders

- Drop value = `(base + Σ flat adds) × Π multipliers`. Apply adds before multipliers, and say so in
  the UI (inferred).
- Upgraders: ×1.5 to ×3 each, or +flat for early ones (inferred). Each drop gets each upgrader at most
  once. With physical drops, keep a per-drop set of upgrader IDs; looping belts through one upgrader
  is the classic infinite-value bug (inferred).
- Collector: adds value to the plot's `Bank`, not straight to the wallet. A **collect pad** makes the
  player walk back to the base, which steal-a-x games build their tension on (inferred). See
  [base defense and stealing](base-defense-and-stealing.md).
- An auto-collect game pass is the common upsell (inferred). The bank can also fill while offline,
  up to a cap; see [idle/offline income](idle-offline-income.md).

### Build order and pricing

- Buttons form a dependency graph: `id`, `price`, `requires` (IDs), `reveals` (template name). Show a
  pad only when all its `requires` are bought (inferred).
- Mix income buttons (droppers, upgraders) with non-income buttons (walls, stairs, decor). Price the
  non-income ones at about 30–60 s of current income so they never stall progress (inferred).
- Show the price on the pad in world space (BillboardGui) and dim it when unaffordable (inferred).
- **Worked example (inferred):** income buttons, price ×1.62 per button, income gain ×1.5 per button,
  first button 25 for +2/s:

| Button | Price | Income after | Wait to afford (s) |
|---|---|---|---|
| 1 | 25 | 2/s | — |
| 2 | 40.5 | 5/s | 20 |
| 3 | 65.6 | 9.5/s | 13 |
| 4 | 106 | 16.3/s | 11 |
| 5 | 172 | 26.4/s | 11 |
| 6 | 279 | 41.6/s | 11 |
| 7 | 452 | 64.3/s | 11 |
| 8 | 732 | 98.5/s | 11 |
| 9 | 1,186 | 150/s | 12 |
| 10 | 1,921 | 227/s | 13 |

  The wait settles near `6.25 × 1.08^(k−1)` seconds (1.62 / 1.5 = 1.08). At 60 buttons, the last
  wait is ~10 min and the whole build takes ~2.2 h: 2–3 sessions under the 60 min/day playtime
  cap (official cap, 2026-10; the rest inferred). Use [upgrade trees](upgrade-trees.md) for the
  general cost-curve rules.
- First pad affordable within ~10 s of claiming the plot, and the first dropper running within
  30 s (inferred, from the first-session bounce windows in
  [discovery](../fundamentals/discovery-algorithm.md)).

### Plots and claiming

- Plots = max players. Set the server size to the plot count (e.g., 6–8) (inferred).
- **Auto-assign** a free plot once the player's data loads. Claim doors cause fights over the best
  plot and leave plotless players (inferred).
- Store ownership on the plot: `plot:SetAttribute("OwnerUserId", player.UserId)`. All checks read
  server state, never a client claim.
- Build relative to the plot: store each template's offset from the plot pivot and place it with
  `model:PivotTo(plot:GetPivot() * offset)`, so every plot uses one layout (inferred).
- On leave: save, then clear the plot over a few frames and free it (community, 2019-11, for the
  staggering).
- Owner-only lasers or doors are fine as decoration. Don't let them kill or trap visitors by
  default (inferred).
- With `StreamingEnabled`, distant plots stream out on clients. A DevForum dev found drops arriving
  without their client-side setup and fixed it by running client setup when the base streamed in
  (community, 2025). Client visuals must start and stop as plot parts stream in and out. Setting the
  plot model's `ModelStreamingMode` so it streams as a unit is an option (unverified).

### Saving the built state

- Save **purchased button IDs**, not parts: `Purchased: {[string]: true}` or a list of IDs. Rebuild
  from templates in `ServerStorage` on load (community, 2021–2024).
- 200 buttons × ~10-character IDs is ~2 KB, far under DataStore limits (inferred; limits in
  [player data](player-data.md)).
- Button IDs never change. Removing or renaming one needs a migration (refund its price or map it to
  the new ID).
- Sandbox tycoons save per placed item: `{item, x, z, rot}` as integers on a grid, with a cap on item
  count (community for ID-plus-position saves; grid and cap inferred).
- Rebuild in dependency order. Spread big rebuilds over frames (e.g., `task.wait()` every 20 models)
  (inferred).
- A thread on dependent buttons reports pads re-locking or unlocking wrongly after load (community,
  2024). Derive pad visibility from `Purchased` + `requires` after every load and purchase. Never
  save pad visibility.

## Implementation outline (server-authoritative)

- **Server:** `PlotService` (assign, clear, rebuild), `PadService` (purchase validation), and
  `IncomeService` (one tick for all plots). Config of buttons, drop values and multipliers lives in
  server modules; the client gets a display copy.
- **Pads:** server `Touched` or `ProximityPrompt.Triggered`. Both need server checks: the player is
  the plot owner, the character is alive and within a few studs of the pad, the pad isn't bought,
  `requires` are met, and the price comes from server config. `Touched` can be spoofed for parts the
  client owns, and prompts get only a distance check on `Triggered` (official, 2026-10). See
  [security](../../.claude/skills/roblox-code/references/security.md).
- **Income:** cache each plot's income per second when a purchase changes it. The tick only adds.
- **Replication:** `Bank` and `Purchased` replicate as attributes or values. Each client spawns drop
  visuals for plots near its camera from that state, and the server never sends per-drop messages.
- **Visual drops:** pool parts with `CanCollide`, `CanTouch` and `CanQuery` off, anchored, and move
  them along the belt path with `Workspace:BulkMoveTo(parts, cframes, Enum.BulkMoveMode.FireCFrameChanged)`.
  BulkMoveTo is documented as "a very fast way to move large numbers of parts", worth using once
  movement is a bottleneck (official, 2026-10). See
  [performance and devices](../../.claude/skills/roblox-map/references/performance-and-devices.md).

```lua
--!strict
-- ServerScriptService/Tycoon: outline only, not drop-in
local Players = game:GetService("Players")
local PlayerData = require(script.Parent.PlayerData)  -- get(player): Data? (player-data.md)
local Buttons = require(script.Parent.ButtonConfig)   -- {[id]: {price, requires, reveals, income}}
local Plots = require(script.Parent.PlotService)      -- ownerOf(player): Model?, build(plot, id)

local PAD_RANGE = 12
local plotIncome: {[Player]: number} = {}

local function recompute(player: Player, data: PlayerData.Data)
	local total = 0
	for id in data.Purchased do total += Buttons[id].income or 0 end
	plotIncome[player] = total -- multipliers (rebirth, passes) applied here too
end

local function tryBuy(player: Player, pad: BasePart)
	local id = pad:GetAttribute("ButtonId")
	local cfg = if typeof(id) == "string" then Buttons[id] else nil
	local data = PlayerData.get(player)
	local plot = Plots.ownerOf(player)
	if not cfg or not data or not plot or not pad:IsDescendantOf(plot) then return end
	if data.Purchased[id] then return end
	for _, req in cfg.requires do if not data.Purchased[req] then return end end
	local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root or (root.Position - pad.Position).Magnitude > PAD_RANGE then return end
	if not (data.Cash >= cfg.price) then return end -- NaN-safe
	data.Cash -= cfg.price
	data.Purchased[id] = true
	Plots.build(plot, id)
	recompute(player, data)
end

task.spawn(function() -- one income tick for every plot
	while true do
		local dt = task.wait(1)
		for player, perSec in plotIncome do
			local data = PlayerData.get(player)
			if data then data.Bank += perSec * dt end
		end
	end
end)

Players.PlayerRemoving:Connect(function(p) plotIncome[p] = nil end) -- PlotService clears the plot
return {tryBuy = tryBuy, recompute = recompute}
```

Wire `tryBuy` to each pad's `Touched` (find the player with `Players:GetPlayerFromCharacter`) with
a short per-pad debounce, or to a `ProximityPrompt.Triggered`.

## Common bugs and exploits

| Bug or exploit | Cause | Fix |
|---|---|---|
| Server freeze, burst of bricks | Hundreds of physical drops per plot | Simulated income, client visuals capped ~150–200 (community, 2019-11) |
| Infinite drop value | Belt loops through one upgrader | Each upgrader applies once per drop, or a fixed path (inferred) |
| Fake collection | Client-owned drop touches the collector | Server network ownership or no physical economy (official, 2026-10) |
| Buying another player's pad | Pad handler checks only cash | Plot ownership + `IsDescendantOf(plot)` (official for `IsDescendantOf` checks, 2026-10) |
| Remote pad purchase from across the map | No distance check | Server distance check with a few studs slack (official, 2026-10) |
| Double purchase | `Touched` fires many times per step | Check `Purchased[id]` and mutate before any yield; per-pad debounce |
| Plot lost or doubled on rejoin | Plot state saved as parts, or loaded before data | Save IDs; assign the plot only after data loads |
| Pads re-lock after load | Pad visibility saved or computed once | Derive from `Purchased` + `requires` every time (community, 2024) |
| Lag spike on leave | Whole plot destroyed in one frame | Clear over several frames (community, 2019-11) |
| Visuals missing on far plots | `StreamingEnabled` streamed the plot out | Start visuals when plot parts stream in (community, 2025) |
| Rebirth keeps old machines | Reset misses placed models | Rebirth clears `Purchased` and rebuilds ([rebirth](rebirth-prestige.md)) |

## Checklist for agents

### Do
- Default to simulated income with client-only, pooled, capped drop visuals.
- Cache income per plot; run one server tick for all plots.
- Validate pads on the server: owner, distance, prerequisites, not yet bought, server price.
- Auto-assign plots after data loads; clear and free them over several frames on leave.
- Save purchased button IDs (or grid items for sandbox tycoons) and rebuild from templates.
- Price income buttons on a steady ratio (e.g., ×1.62 price vs ×1.5 income) and playtest total
  build time against 2–3 sessions.

### Don't
- Don't put the economy on `Touched` of client-owned parts.
- Don't replicate every drop from the server to every client.
- Don't save parts, CFrames of fixed builds, or pad visibility.
- Don't rename button IDs without a migration.
- Don't give plot owners network ownership of drops.

## Sources

1. https://devforum.roblox.com/t/tycoon-lag-how-to-fix/387741: server freeze from brick spawning; client-only bricks capped ~200; stagger plot removal (2019-11)
2. https://devforum.roblox.com/t/issue-with-streamingenabled-in-tycoon-game/3884084: drops and plots with StreamingEnabled; client setup on stream-in (2025)
3. https://devforum.roblox.com/t/issue-saving-an-entire-tycoon/1940698: save item IDs, not instances
4. https://devforum.roblox.com/t/how-to-make-a-saving-tycoon/1264934: classic tycoons save a list of purchases; sandbox tycoons add positions
5. https://devforum.roblox.com/t/need-help-with-tycoon-button-dependancy/2815462: dependent-button re-lock bugs (2024)
6. https://devforum.roblox.com/t/2643484: dropper slowdown with many players; network-owner suggestion
7. https://create.roblox.com/docs/reference/engine/classes/WorldRoot.md: `BulkMoveTo`, `BulkMoveMode`, performance note
8. https://create.roblox.com/docs/scripting/security/client-server-boundary: `Touched` spoofing, ProximityPrompt server checks
9. https://create.roblox.com/docs/physics/network-ownership: `SetNetworkOwner`, client-owned part exploits
10. https://github.com/berezaa/minershaven: Miner's Haven sandbox tycoon source; rebirth destroys placed items (2019)
11. https://create.roblox.com/docs/discovery: 60 min/day playtime cap, first-session bounce windows

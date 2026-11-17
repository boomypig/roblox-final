---
title: Pets and companions
type: pattern
read-when: Adding pets that follow, equip, or boost stats.
last-researched: 2026-10-22
---

# Pets and companions

## What it is

Collectible creatures that the player owns (saved as records), equips into a few slots, and sees
following their character. Equipped pets add stats, usually a multiplier on income or damage.
Duplicates feed fusing or evolving. Pets come from [eggs](rarity-tiers-and-eggs.md), live in
[inventory](inventory.md), and are often [traded](trading.md).

## Why it works

- A visible pet is a status display: other players see your rarest pets next to you all session
  (inferred; see [first-time experience](../fundamentals/first-time-experience.md), "seeing someone
  with a big pet shows where the game goes").
- Equipping best pets is a simple, satisfying optimization with a number that goes up (inferred).
- Fusing turns useless duplicates into progress, so every hatch has some value (inferred).
- Companions add personality to an otherwise empty grind loop (inferred).

## Genres that use it

[Pet and egg collection](../genres/pet-egg-collection.md), [simulator](../genres/simulator.md),
[roleplay life sim](../genres/roleplay-life-sim.md) (Adopt Me-style care pets),
[farming](../genres/farming-growing.md), [steal-a-x](../genres/steal-a-x.md),
[anime RPG](../genres/anime-rpg.md) (summons/familiars), [fishing](../genres/fishing.md).

## Design rules

### Following: pick the client-side model

| Approach | Who moves it | Verdict |
|---|---|---|
| Server moves pets every `Heartbeat` (CFrame lerp) | Server | Looks choppy for everyone and costs server time per pet (community, DevForum threads 2021–2024). Don't. |
| Server-created unanchored pet + `SetNetworkOwner(owner)` + `AlignPosition` | Owner's client | Smooth for the owner, laggy for others (community). The owner's exploit client controls the part and can fling with it (official: owners control their parts' physics). Don't. |
| **Each client renders every player's pets locally, anchored, moved by `PivotTo`/`CFrame` lerp on `RunService.PreRender`** | Every client, for its own view | Default. Zero server cost, smooth for everyone, nothing to exploit (community recommendation; inferred). |
| Client-local unanchored pet + `AlignPosition`/`AlignOrientation` | Every client | Use only if pets must physically bump into things. More physics cost per pet (inferred). |

- The server owns **state only**: which pet records are equipped. It replicates that list (e.g. a
  `Player` attribute `EquippedPets = "Cat,Dog,Dragon"`); attributes reach late joiners for free
  (inferred design).
- `RunService.PreRender` is the current per-frame event for visuals; it supersedes `RenderStepped`
  and runs on the client only (official, 2026-10). Keep the work small; rendering waits for it.
- Smoothing: `alpha = 1 - math.exp(-k * dt)` with `k ≈ 8–12` is frame-rate independent; a fixed
  alpha like 0.15 behaves differently at 30 and 60 FPS and is a common source of jitter
  (inferred; the fixed-alpha jitter is reported in community threads, 2024-12).
- Formation: an arc behind the player, 4–6 studs out, radius growing with pet count; flying pets
  bob with a small sine offset (community pattern; numbers inferred).
- Ground: raycast down from each target with `Workspace:Raycast` at ~10 Hz, not every frame, so
  walking pets don't float on ramps (community fix, 2023; rate inferred).
- Snap (teleport) a pet that ends up > 50 studs from its target, e.g. after the owner teleports
  (community idea; distance inferred).
- If you use `AlignPosition`: `Mode = OneAttachment` follows `Position`; `Responsiveness` accepts
  5–200; `RigidityEnabled = true` ignores the force limits (official API). `AlignOrientation`
  with `Mode = OneAttachment` follows its `CFrame` property (official API).

### Performance with many pets

- Worst case per client = players × equipped slots. 30 players × 6 pets = 180 moving models
  (inferred arithmetic). Budget from [performance and devices](../fundamentals/performance-and-devices.md):
  < 1,000 draw calls and < 1M triangles on the baseline device (official example, 2026-10).
- One `MeshPart` per pet species, ≤ ~2,000 triangles (inferred budget). Pets of the same species
  share a draw call when they use the same mesh and texture (official instancing rule).
- Every pet part: `Anchored = true`, `CanCollide = false`, `CanTouch = false`, `CanQuery = false`,
  `CastShadow = false` (official guidance for decoration; community confirms for pets).
- Cull: other players' pets beyond ~150 studs from the camera stop updating or hide; update
  mid-distance pets at a lower rate (community suggestion; distance inferred). Optional setting
  "Hide other players' pets" for low-end phones (inferred).
- Moving many single-part pets: `Workspace:BulkMoveTo(parts, cframes,
  Enum.BulkMoveMode.FireCFrameChanged)` cuts per-part property work. Roblox advises it only after
  profiling shows movement is the bottleneck (official, 2026-10).
- Never `FireAllClients` positions per frame (community warning; inferred cost).

### Equip slots and stat boosts

- Start at 3 equip slots; grow to 6–10 through levels, rebirths and a "+slots" game pass
  (inferred; extra pet slots are a standard capacity purchase, see
  [monetization](../fundamentals/monetization.md)).
- Stat model: each pet has a base `Power` per species × variant multiplier (e.g. Golden ×2,
  Rainbow ×5, inferred) × level bonus. Equipped pets **add**; the total multiplies income with
  other sources such as [rebirth](rebirth-prestige.md) (inferred).
- Keep the next tier ~2–3× stronger than the previous one so a new egg is an obvious upgrade
  (inferred; tune with [upgrade trees](upgrade-trees.md)).
- "Equip Best" button: the server sorts the player's own pets by power and equips the top N.
  Never accept a client-picked "best" list (inferred).
- Pets that "do" things (break coins, attack): the server assigns targets and computes damage per
  second from stats; clients animate. Never read pet positions from the client (inferred; see
  [security](../fundamentals/security-and-anti-exploit.md)).

### Fusing and evolving

- Adopt Me!: 4 full-grown pets of one species fuse into a Neon; 4 Neons fuse into a Mega Neon,
  so 16 base pets per Mega (press/wiki, 2026). Growth runs through six ages from Newborn to
  Full Grown, and rarer pets need more tasks per age (press, 2026).
- Pet Simulator 99 uses machines that turn several copies into Golden or Rainbow variants
  (community; exact input counts unverified).
- Fusing is a **sink**: it deletes duplicates, which protects trade values and stops storage
  bloat (inferred).
- Rules: same species (and same variant) in, one higher variant out; show the result before
  confirm; 100% success. A failure chance on a paid input is a paid random "enhancement item" and
  needs odds disclosure (official, paid random items policy).
- Server step: validate every input UID is owned, distinct, unlocked, not equipped, not in an
  open trade; then remove inputs and add the output with no yield in between (inferred).

### Storage limits

- Show `count / cap` everywhere pets appear. Start ~50–100, expand through progress and a pass
  (inferred). Hatching stops (before charging) when full; see
  [rarity tiers and eggs](rarity-tiers-and-eggs.md).
- A pet record is ~60–120 characters of JSON with a 36-character GUID, so 10,000 pets ≈ 1 MB of a
  4 MB key (inferred arithmetic; key limit official, see [player data](player-data.md)). Hard cap
  storage at a few thousand. Data model and sizes: [inventory](inventory.md).
- Offer **Lock** (can't delete, fuse or trade) and mass-delete by tier, so cleanup is safe and
  fast (inferred).

### Naming

- Filter on the server: `TextService:FilterStringAsync(text, ownerUserId)`, then
  `GetNonChatStringForBroadcastAsync()` for a name shown above the pet to the whole server
  (official). Wrap in `pcall`; on failure don't show the name and don't retry (the method retries
  internally) (official).
- Stored text such as pet names must be filtered when retrieved, so store the raw name and filter
  it again when the owner joins and before display (official guidance on stored text; re-filter
  on every load inferred).
- `FilterStringAsync` throws if `fromUserId` isn't in this server (official), so filter only while
  the owner is present; show the species name otherwise (inferred).
- Cap names at ~20 characters, require valid UTF-8, rate-limit renames (inferred; see the
  string checks in [security](../fundamentals/security-and-anti-exploit.md)).
- Games that skip filtering may be removed until it's added (official).

### Visuals without an artist

- One `MeshPart` per species, recolored for variants: Golden = gold `Color` + `Metal` material,
  Rainbow = hue cycled on the client, Shiny = `ParticleEmitter` sparkle (inferred).
- Sources, in order: (1) the user's Studio MCP `generate_mesh` / `generate_texture` tools at build
  time; (2) simple primitive pets (sphere body, eyes, ears) welded and exported as one mesh;
  (3) Creator Store models, checked for scripts and license (inferred). Runtime generation via
  `GenerationService:GenerateMeshAsync` exists but must be called from the server and has a
  per-minute cap (official, 2026-10); don't build your pet roster with it (inferred).
- Personality is cheap: a 2-frame squash bob when moving, a hop when the owner jumps, idle
  look-around, a heart emote on equip (inferred; see [game feel](../fundamentals/game-feel.md)).
- Size by tier: Common 1×, Legendary ~1.5×, chase tier 2–3× ("Huge" pets in PS99 are a whole
  tier built on size; community). Size reads from across the map (inferred).
- Never copy another game's pet designs, names or meshes (CONTRIBUTING rule).

## Implementation outline (server-authoritative)

- **Data** (per pet, keyed by GUID in [inventory](inventory.md)): `PetId`, `Tier`, `Variant`,
  `Level`, `XP`, `Name`, `Locked`. Session data: `Equipped: {string}` (UIDs), `EquipSlots`,
  `PetCap`.
- **Server-only config:** `ServerStorage/Config/PetStats` with power per species and variant
  multipliers. Clients get display stats through the inventory snapshot.
- **Remotes (C→S):** `EquipPet(uid)`, `UnequipPet(uid)`, `EquipBest()`, `RenamePet(uid, name)`,
  `FusePets(uids)`, `SetPetLocked(uid, locked)`. Validate with the
  [pipeline](../fundamentals/security-and-anti-exploit.md#remote-validation-pipeline); for
  `uids`, accept only an array of ≤ 10 strings of length ≤ 38 (GUID length, official).
- **Replication:** server sets `EquippedPets` (species list) on the `Player`; every client renders
  from it. Inventory changes go to the owner only (see [inventory](inventory.md)).

```lua
--!strict
-- ServerScriptService/PetServer: outline only (rate limiting omitted)
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")
local PlayerData = require(script.Parent.PlayerData) -- get(p) -> Data?
local PetStats = require(ServerStorage.Config.PetStats) -- Power {[petId]: number}, VARIANT {[number]: number}
local Trades = require(script.Parent.TradeServer)       -- isLocked(p, uid) -> boolean

local EquipPet = ReplicatedStorage.Remotes.EquipPet :: RemoteEvent
local power: {[Player]: number} = {} -- read by the income code; never from attributes

local function publish(player: Player, data: any)
	local names, total = {}, 0
	for _, uid in data.Equipped do
		local pet = data.Pets[uid]
		table.insert(names, pet.PetId)
		total += PetStats.Power[pet.PetId] * PetStats.VARIANT[pet.Variant] * (1 + pet.Level * 0.05)
	end
	power[player] = total
	player:SetAttribute("EquippedPets", table.concat(names, ",")) -- visuals for all clients
end

EquipPet.OnServerEvent:Connect(function(player: Player, uid: unknown)
	if typeof(uid) ~= "string" or #uid > 38 then return end
	local data = PlayerData.get(player)
	if not data or not data.Pets[uid] or Trades.isLocked(player, uid) then return end
	if table.find(data.Equipped, uid) or #data.Equipped >= data.EquipSlots then return end
	table.insert(data.Equipped, uid)
	publish(player, data)
end)
```

```lua
--!strict
-- StarterPlayerScripts/PetFollow (LocalScript): visuals only, outline. Spawning omitted:
-- on each Player's "EquippedPets" attribute change, clone anchored single-MeshPart models
-- from ReplicatedStorage.PetModels into rendered[player].
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local rendered: {[Player]: {BasePart}} = {}
local CULL, RADIUS, SPREAD = 150, 5, math.rad(120)

RunService.PreRender:Connect(function(dt: number)
	local cam = workspace.CurrentCamera.CFrame.Position
	local alpha = 1 - math.exp(-10 * dt) -- frame-rate independent
	local parts, cframes = {}, {}
	for owner, pets in rendered do
		local char = owner.Character
		local root = if char then char:FindFirstChild("HumanoidRootPart") :: BasePart? else nil
		if not root or (root.Position - cam).Magnitude > CULL then continue end
		for i, pet in pets do
			local a = if #pets == 1 then 0 else SPREAD * ((i - 1) / (#pets - 1) - 0.5)
			local goal = root.CFrame * CFrame.new(math.sin(a) * RADIUS, 0, math.cos(a) * RADIUS) -- +Z = behind
			goal += Vector3.new(0, math.sin(os.clock() * 4 + i) * 0.3, 0) -- bob; ground raycast at 10 Hz omitted
			local cur = pet.CFrame
			table.insert(parts, pet)
			table.insert(cframes, if (cur.Position - goal.Position).Magnitude > 50 then goal else cur:Lerp(goal, alpha))
		end
	end
	workspace:BulkMoveTo(parts, cframes, Enum.BulkMoveMode.FireCFrameChanged)
end)

Players.PlayerRemoving:Connect(function(p)
	for _, pet in rendered[p] or {} do pet:Destroy() end
	rendered[p] = nil
end)
```

## Common bugs and exploits

| Bug | Cause | Fix |
|---|---|---|
| Jittery pets | Server-side movement, or a fixed lerp alpha on `Heartbeat` | Client-side, `PreRender`, exponential smoothing (official event; community symptom) |
| Pets invisible to others | Each client renders only its own pets | Replicate equipped state; every client renders everyone's (community) |
| Fling exploit | Server pet network-owned by a player | Client-local visuals or anchored pets; `SetNetworkOwner(nil)` on anything physical (official) |
| Phone FPS drops in full servers | Hundreds of multi-part pets with shadows and collisions | Single MeshPart, anchored, no collide/touch/query/shadow, culling (official + community) |
| Equip more than slots | Client-side slot check only | Server checks `#Equipped < EquipSlots` (inferred) |
| Equip a traded-away pet | Pet still in `Equipped` after a trade or fuse | Remove UIDs from `Equipped` in the same step as removal; trades lock offered pets (inferred) |
| Fake power | Income read from a client-visible attribute | Server keeps power in a server table (inferred) |
| Fuse dupe | Same UID passed twice in `FusePets` | Reject duplicates; check ownership of each (inferred) |
| Unfiltered names | Raw name shown or saved name not re-filtered | `FilterStringAsync` + broadcast string, on rename and on load (official) |
| Pets left behind | Owner teleports; lerp takes seconds | Snap when > 50 studs away (inferred) |

## Checklist for agents

- [ ] Server holds pet records and equipped UIDs; clients render all pets locally from a replicated list.
- [ ] Follow loop on `RunService.PreRender`, frame-rate independent smoothing, arc formation, ground raycast ≤ 10 Hz, snap when far.
- [ ] Pet models: one MeshPart, anchored, `CanCollide/CanTouch/CanQuery/CastShadow = false`, ≤ ~2k triangles, culled past ~150 studs.
- [ ] Equip, unequip, equip-best, fuse, lock and rename validated on the server; pets in trades can't be equipped, fused or deleted.
- [ ] Power computed on the server from config; never from attributes or client values.
- [ ] Fusing is deterministic, 100% success, shows the result first, removes inputs atomically.
- [ ] Storage cap shown; hatching refuses before charging when full; lock and mass-delete exist.
- [ ] Names filtered with `TextService:FilterStringAsync` + `GetNonChatStringForBroadcastAsync`, re-filtered on load.
- [ ] Variants made by recolor/material/particles, not new models.

## Sources

1. https://create.roblox.com/docs/reference/engine/classes/RunService.md: PreRender supersedes RenderStepped, client-only, BindToRenderStep
2. https://create.roblox.com/docs/reference/engine/classes/AlignPosition.md: Mode, Responsiveness 5–200, RigidityEnabled, force limits
3. https://create.roblox.com/docs/reference/engine/classes/AlignOrientation.md: Mode, CFrame, AlignType, RigidityEnabled
4. https://create.roblox.com/docs/reference/engine/classes/WorldRoot.md: BulkMoveTo signature, BulkMoveMode, use only when profiling says so
5. https://create.roblox.com/docs/reference/engine/classes/TextService.md: FilterStringAsync, pcall, no retry, throws if user not in server
6. https://create.roblox.com/docs/ui/text-filtering: stored pet names must be filtered, broadcast vs per-user strings, removal for unfiltered games
7. https://create.roblox.com/docs/reference/engine/classes/HttpService.md: GenerateGUID 36/38 characters
8. https://create.roblox.com/docs/production/monetization/paid-random-items: enhancement and combination items need odds disclosure
9. https://devforum.roblox.com/t/pet-not-smooth-on-server/1103781: server-driven pets look choppy (2021)
10. https://devforum.roblox.com/t/how-do-i-make-pet-follow-system/3308281: fixed-alpha server lerp jitter, network ownership trade-off (2024-12)
11. https://devforum.roblox.com/t/help-with-renderstepped/2840968: turn off collide, shadows, touch, query on many pets
12. https://devforum.roblox.com/t/pet-following-system-problem/2586102: client-calculated pets for everyone, distance-based update rate
13. https://devforum.roblox.com/t/2387951: ramp floating fixed with a downward raycast
14. https://breezewiki.discard.no/adoptme/wiki/Neon_Cave: Adopt Me Neon and Mega Neon fusing (4 full-grown / 4 neon)
15. https://create.roblox.com/docs/reference/engine/classes/GenerationService.md: server-only runtime mesh generation

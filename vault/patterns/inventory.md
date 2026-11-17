---
title: Inventory
type: pattern
read-when: Adding an inventory, equipment, or item storage.
last-researched: 2026-10-22
---

# Inventory

## What it is

The saved record of what a player owns, plus the server code that adds, removes and equips
items, and the client UI that shows them. The save is plain data in the player's profile
([player data](player-data.md)); the client gets a copy it can display but never changes. Pets
and tradeable items sit on top of this: [pets](pets-companions.md), [trading](trading.md),
[eggs](rarity-tiers-and-eggs.md), [shops](shops.md).

## Why it works

- A full, sorted inventory is a progress display: players open it to admire, compare and plan
  (inferred).
- Capacity limits make players clean up (fuse, sell, delete), which is a resource sink, and give
  an honest thing to sell: more space (inferred; capacity purchases listed in
  [monetization](../fundamentals/monetization.md)).
- A fast, readable inventory on a phone is the difference between "I'll check my pets" and closing
  the game (inferred; see [UI/UX](../fundamentals/ui-ux.md)).

## Genres that use it

Nearly all: [simulator](../genres/simulator.md), [pet and egg collection](../genres/pet-egg-collection.md),
[farming](../genres/farming-growing.md), [fishing](../genres/fishing.md),
[survival](../genres/survival.md) (crafting materials), [anime RPG](../genres/anime-rpg.md),
[tower defense](../genres/tower-defense.md) (units), [shooter](../genres/shooter.md) (loadouts),
[fashion avatar](../genres/fashion-avatar.md) (outfits).

## Design rules

### Data model: stacks vs unique items

| Kind | Use when | Saved shape |
|---|---|---|
| **Stack** | Identical, fungible things: potions, seeds, ores, crates, consumable boosts | `Stacks: {[itemId]: number}` |
| **Unique** | Anything with its own state (level, XP, name, variant, lock) or anything tradeable and valuable | `Pets: {[uid]: Record}`, `Items: {[uid]: Record}`, uid from `HttpService:GenerateGUID(false)` |

- `GenerateGUID` returns a random version-4 UUID: 36 characters without braces, 38 with. The
  argument `wrapInCurlyBraces` defaults to **true**, so pass `false` (official). It works without
  `HttpEnabled` (official). Generate on the server only.
- **GUIDs never change**, not on trade and not on migration; a fuse output is a new item with a
  new GUID. That makes
  dupes detectable (one GUID in two profiles) and rollbacks exact (inferred; see
  [trading](trading.md#dupe-postmortems)).
- Shorter alternative: `"{UserId}-{counter}"` with a saved per-player `NextUid` counter. Globally
  unique, ~15 characters, and records who minted it. Use only if save size matters (inferred).
- **Dictionaries keyed by uid**, not arrays: O(1) lookup and remove, and no array holes. Keep keys
  non-numeric strings; DataStores and remotes reject mixed or gapped tables (official).
- Save only per-instance state: `ItemId` plus fields like `Level`, `Variant`, `Locked`, `Paid`,
  `Name`. Names, stats, prices and icons live in a `Catalog` module keyed by `ItemId`, so a
  balance patch updates every copy (inferred).
- Keep `PetCount`/`ItemCount` counters for cheap capacity checks, and **recount on load** so a
  bug can't leave them drifting (inferred).
- `Paid = true` on anything that came from Robux, kept through trades and fusing, for
  `IsPaidItemTradingAllowed` (official rule; flag design inferred; see [trading](trading.md)).
- Unknown `ItemId` on load (item removed from the catalog): keep the record, hide it, log it.
  Never delete it or crash the load. Map retired IDs to replacements in a migration
  (inferred; migrations in [player data](player-data.md)).

### Size limits and record cost

- Hard limit: 4,194,304 characters of JSON per key; aim for a typical save under 100 KB
  (official limit, inferred target; see [player data](player-data.md#current-limits-official-read-2026-10-22)).
  Experience storage is 500 MB + 1 MB per lifetime user, measured compressed (official, 2026-07).
- Rough cost (inferred arithmetic): a unique record with a GUID key and 5 short fields is ~80–120
  characters, so 1,000 pets ≈ 100 KB and 10,000 ≈ 1 MB. A stack entry is ~20 characters whatever
  the count.
- So: stack everything you can; cap unique storage in the low thousands; keep field names short
  (`L` not `PetLevel`) only once you're past ~1,000 records; log `#HttpService:JSONEncode(data)`
  on save and alert above 1 MB (inferred).
- Bound every list: trade history (30), mail (100), purchase IDs (100) (inferred; ProfileStore's
  example keeps 100 purchase IDs, community).

### Capacity

- Show `count / cap` on the inventory button and in the window header (inferred).
- Starting caps (inferred, tune with analytics): 50–100 pets, 100–200 gear, stacks capped per
  item (e.g. 999) only if a cap is part of the design.
- Check space **before** charging anything (hatch, buy, craft) and refuse with a clear message
  (inferred).
- **Never lose a Robux purchase or a gift to a full bag.** Purchased or gifted items may exceed
  the cap, or go to a mailbox the player claims from (inferred). `ProcessReceipt` must still grant
  ([player data](player-data.md#related-systems)).
- Sell capacity directly ("+50 slots") rather than making space a random reward (inferred).

### Sorting, filtering, UI

- Default sort for pets: power (descending), then tier, then newest. Also offer: tier, newest,
  name, level. Filters: tier, variant, equipped, locked, tradeable. A search box for 50+ items
  (inferred).
- Sorting and filtering run on the **client** over its copy; they change nothing on the server
  (inferred).
- Equipped items pinned first with a check mark; locked items show a padlock; new items show a
  "NEW" dot until viewed (inferred).
- Big grids: render only visible cells and reuse ~30–40 cell frames as the player scrolls, rather
  than one `Frame` per item; use 2D icon images per species, not a `ViewportFrame` per cell
  (inferred, performance).
- Batch actions: "Delete all Commons", "Lock", "Fuse duplicates", with a confirm dialog naming
  the count and skipping locked items (inferred).
- Mobile: cells ≥ 48 px, tap opens a detail panel with Equip / Lock / Delete, no hover-only info
  (inferred; touch target sizes in [UI/UX](../fundamentals/ui-ux.md)).

### Equip and unequip

- Gear slots as a map, `Gear = {Weapon = uid?, Hat = uid?}`; pets as an array of uids,
  `Equipped = {uid}`, with a slot count ([pets](pets-companions.md#equip-slots-and-stat-boosts))
  (inferred).
- Server checks: the uid exists in this player's bag, its catalog category fits the slot, it isn't
  in an open trade, and the player is in a state that allows swapping (not mid-round, not dead)
  (inferred; pipeline in [security](../fundamentals/security-and-anti-exploit.md#remote-validation-pipeline)).
- Removing an item (sell, delete, fuse, trade) also removes it from `Equipped` in the same step
  (inferred).

### Tools/Backpack vs custom inventory

| | Roblox `Backpack` with `Tool`s | Custom inventory (data) |
|---|---|---|
| What it is | Tools parented to the player's `Backpack` show as buttons at the bottom of the screen (official) | Records in the save; UI you build |
| Fits | A few held items (sword, rod, flashlight) | Dozens to thousands of items, stats, stacks, pets |
| Respawn | Backpack is destroyed and rebuilt from `StarterPack` and the player's `StarterGear` on each spawn (official) | Unaffected |
| Cost | Every Tool is a replicated Instance | One data table |

Recommended hybrid (inferred): the custom inventory is the source of truth. When the player
equips a holdable item, the server clones that one `Tool` from `ServerStorage` into the
`Backpack` (or the player's `StarterGear`, so it survives respawn) and may call
`Humanoid:EquipTool(tool)`. `Humanoid:UnequipTools()` returns held tools to the Backpack
(official). Set `Tool.CanBeDropped = false` unless dropping is a feature; when true, Backspace
drops it into Workspace (official). With a custom hotbar, hide the default one with
`StarterGui:SetCoreGuiEnabled(Enum.CoreGuiType.Backpack, false)` from a LocalScript (official
API). Never read "what does the player own" from the Backpack.

### Replicating to the client: snapshot, then deltas

- On load (after data is ready), send one **snapshot** of the player's own inventory. Then send
  **deltas** (`add`, `remove`, `update`, `stack`), batched per frame, each batch with a sequence
  number (inferred design).
- `RemoteEvent` is the reliable, ordered choice; `UnreliableRemoteEvent` is unordered, not resent,
  and drops payloads over 1,000 bytes, so never use it for inventory (official).
- No published size limit for a `RemoteEvent` payload (official page gives none). Split very large
  snapshots into pages of ~200 records to avoid one huge send (inferred).
- Client: apply a batch only if `seq == last + 1`; otherwise request a fresh snapshot (rate-limited
  remote). Rebuild only the changed cells (inferred).
- Send other players only what they can see: equipped pets as an attribute
  ([pets](pets-companions.md)) and items in an open trade window (inferred).
- `Folder` + `ValueBase` objects per item are simple for < ~100 items but cost an Instance each;
  use remotes beyond that (inferred). Libraries such as loleris's Replica do this for you
  (community).
- Remote tables lose metatables and functions, and mixed or holey tables break (official), so
  send plain records.

## Implementation outline (server-authoritative)

- **Modules:** `Catalog` (definitions, read by server; a display copy can replicate), `Inventory`
  (server: add/remove/equip, delta queue), client `InventoryClient` (holds the copy, sorts,
  renders).
- **Remotes (C→S):** `EquipItem(uid)`, `UnequipItem(slot)`, `DeleteItems(uids)` (≤ 50 strings ≤
  38 chars, no duplicates), `SetLocked(uid, locked)`, `RequestInventorySync()`. **(S→C):**
  `InventorySnapshot(seq, data)`, `InventoryDelta(seq, ops)`.
- No remote takes an item ID to **add**. Adds only come from server systems: eggs, shops,
  quests, trades, receipts.

```lua
--!strict
-- ServerScriptService/Inventory: outline only
local HttpService = game:GetService("HttpService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local Delta = ReplicatedStorage.Remotes.InventoryDelta :: RemoteEvent
local Snapshot = ReplicatedStorage.Remotes.InventorySnapshot :: RemoteEvent
type Bag = "Pets" | "Items"
local COUNT: {[Bag]: string} = {Pets = "PetCount", Items = "ItemCount"}
local CAP: {[Bag]: string} = {Pets = "PetCap", Items = "ItemCap"}

local pending: {[Player]: {{any}}} = {}
local seq: {[Player]: number} = {}

local function push(player: Player, op: {any})
	local q = pending[player] or {}
	pending[player] = q
	table.insert(q, op)
end

local Inventory = {}

function Inventory.recount(data: any) -- call on load
	for bag, key in COUNT do
		local n = 0
		for _ in data[bag] do n += 1 end
		data[key] = n
	end
end

function Inventory.addUnique(player: Player, data: any, bag: Bag, record: {[string]: any}, overCap: boolean?): string?
	if not overCap and data[COUNT[bag]] >= data[CAP[bag]] then return nil end -- callers check before charging
	local uid = HttpService:GenerateGUID(false) -- 36 chars, no braces
	data[bag][uid] = record
	data[COUNT[bag]] += 1
	push(player, {"add", bag, uid, record})
	return uid
end

function Inventory.addPet(player: Player, data: any, petId: string, tier: number): string?
	return Inventory.addUnique(player, data, "Pets", {ItemId = petId, Tier = tier, Level = 1, Locked = false})
end

function Inventory.removeUnique(player: Player, data: any, bag: Bag, uid: string): boolean
	local rec = data[bag][uid]
	if not rec or rec.Locked then return false end
	data[bag][uid] = nil
	data[COUNT[bag]] -= 1
	local i = table.find(data.Equipped, uid) -- pets: array of uids
	if i then table.remove(data.Equipped, i) end
	for slot, g in data.Gear do if g == uid then data.Gear[slot] = nil end end -- gear: slot map
	push(player, {"remove", bag, uid})
	return true
end

function Inventory.addStack(player: Player, data: any, itemId: string, n: number)
	assert(n % 1 == 0 and n > 0, "integer stack add")
	data.Stacks[itemId] = (data.Stacks[itemId] or 0) + n
	push(player, {"stack", itemId, data.Stacks[itemId]}) -- send the new total, not the change
end

function Inventory.snapshot(player: Player, data: any)
	pending[player] = nil
	seq[player] = (seq[player] or 0) + 1
	Snapshot:FireClient(player, seq[player], {Pets = data.Pets, Items = data.Items,
		Stacks = data.Stacks, Equipped = data.Equipped, Gear = data.Gear, PetCap = data.PetCap, ItemCap = data.ItemCap})
end

RunService.Heartbeat:Connect(function() -- one batched delta per player per frame
	for player, ops in pending do
		seq[player] = (seq[player] or 0) + 1
		Delta:FireClient(player, seq[player], ops)
	end
	table.clear(pending)
end)

game:GetService("Players").PlayerRemoving:Connect(function(p) pending[p] = nil; seq[p] = nil end)

return Inventory
```

Send stack **totals**, not increments, so a resync can't double-count (inferred).

## Common bugs and exploits

| Bug | Cause | Fix |
|---|---|---|
| Item injection | A remote like `GiveItem(itemId)` or a client-side add | Adds only from server systems ([security](../fundamentals/security-and-anti-exploit.md)) |
| GUID braces mismatch | `GenerateGUID()` default wraps in `{}`; some code strips them | Always `GenerateGUID(false)` (official default is true) |
| Lost save on load | Mixed table (array + string keys) or numeric-string keys in a bag | Dictionaries with non-numeric string keys only (official) |
| Counter drift | Count updated in one path but not another | Recount on load; one module owns all adds/removes (inferred) |
| Purchased item lost | Bag full at `ProcessReceipt` | Allow over cap or mailbox for purchases and gifts (inferred) |
| Delete equipped or traded item | Remove path skips `Equipped`/trade locks | Remove clears `Equipped`; trade-locked items can't be removed (inferred) |
| Mass delete of locked items | Batch path ignores `Locked` | Check `Locked` per item in every batch op (inferred) |
| Client desync | Missed or reordered deltas, or deltas applied before the snapshot | Sequence numbers; resync on a gap; reliable `RemoteEvent` only (official ordering + inferred) |
| Laggy inventory screen | One frame or `ViewportFrame` per item for 1,000 items | Virtualized grid, 2D icons (inferred) |
| Save grows forever | Unbounded logs, uncapped bags | Caps and size alert (official limit; inferred) |
| Tools vanish on death | Tools given at runtime to `Backpack` only | Re-give on `CharacterAdded` or use `StarterGear` (official respawn behavior) |
| Unknown item crashes load | Item removed from `Catalog` | Keep and hide unknown records; migrate IDs (inferred) |

## Checklist for agents

- [ ] Stacks for fungible items; unique records keyed by `GenerateGUID(false)` for anything with state or trade value.
- [ ] GUIDs never regenerated; `Paid` flag carried through trades and fusing.
- [ ] Definitions in a `Catalog`; saves hold only `ItemId` + per-instance state.
- [ ] Counters recounted on load; capacity checked before charging; purchases and gifts never lost to a full bag.
- [ ] Save size logged; bags and logs capped; typical save < 100 KB.
- [ ] No client remote can add items; equip, delete, lock validated on the server against ownership, locks and trades.
- [ ] Snapshot on load, then sequenced, batched deltas on a `RemoteEvent`; client resyncs on a gap.
- [ ] Client-side sort/filter/search; virtualized grid with 2D icons; mobile-sized cells.
- [ ] Tools only for the few held items, cloned from `ServerStorage` on equip; `CanBeDropped = false`; default backpack hidden if using a custom hotbar.

## Sources

1. https://create.roblox.com/docs/reference/engine/classes/HttpService.md: GenerateGUID format, 36/38 characters, `wrapInCurlyBraces` default true, no HttpEnabled needed; JSONEncode rules
2. https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits: 4,194,304-character value limit, storage formula
3. https://create.roblox.com/docs/scripting/events/remote: argument limits (mixed tables, nil gaps, metatables, functions)
4. https://create.roblox.com/docs/reference/engine/classes/RemoteEvent.md: ~500 requests/s per client, no stated payload limit
5. https://create.roblox.com/docs/reference/engine/classes/UnreliableRemoteEvent.md: unordered, not resent, 1,000-byte drop; use RemoteEvent for ordering and reliability
6. https://create.roblox.com/docs/reference/engine/classes/Backpack.md: Backpack UI, rebuilt from StarterPack and StarterGear on spawn
7. https://create.roblox.com/docs/reference/engine/classes/Humanoid.md: EquipTool, UnequipTools
8. https://create.roblox.com/docs/reference/engine/classes/Tool.md: CanBeDropped, RequiresHandle
9. https://create.roblox.com/docs/reference/engine/classes/StarterGui: SetCoreGuiEnabled for hiding the default backpack
10. https://github.com/MadStudioRoblox/ProfileStore: example caps purchase ID history at 100
11. https://about.roblox.com/community-standards: paid item trading rule behind the `Paid` flag

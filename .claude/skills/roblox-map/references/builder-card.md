---
title: Map-builder card
generated-by: python3 tools/build_cards.py (never hand-edit; rerun after editing a source)
built-from:
  - .claude/skills/roblox-map/references/studio-mcp.md | `execute_luau`: rules that keep Studio alive | sha256:86f013ef1003
  - .claude/skills/roblox-map/references/studio-mcp.md | Vetting Creator Store assets | sha256:42c2388f8543
  - .claude/skills/roblox-map/references/studio-mcp.md | Common build bugs | sha256:61ef84ab178a
  - .claude/skills/roblox-map/references/studio-mcp.md | Checklist for agents | sha256:c891bd1f6634
  - .claude/skills/roblox-map/references/visual-quality.md | "Does this look default?" checklist | sha256:02a5ab1e8972
  - .claude/skills/roblox-map/references/visual-quality.md | Checklist for agents | sha256:55d1e8a8b185
  - .claude/skills/roblox-map/references/performance-and-devices.md | Budget table | sha256:036ee86c4fd2
  - .claude/skills/roblox-map/references/performance-and-devices.md | Checklist for agents | sha256:bc17ef58e877
---

# Map-builder card

Everything the map-builder agent acts on during a run, copied word for word from the three
roblox-map references, with the place each part came from. Read this instead of the three full
files. Open a full reference only when a check fails or an item here is not enough to act on,
and then only the section named in that part's header.

Still read, every run: the map's state file, the approved art direction and map brief, the
genre file (`vault/genres/<genre>.md`) for dressing and props, and only the reference images
the brief links for the zone being built. The Luau checks are
`.claude/skills/roblox-map/scripts/luau/map_checks.lua`.

## Coverage

Every section below is copied whole. Items are checklist lines, bullets, numbered items
and table rows; the card holds the same count as its source (tests/test_cards.py).

| # | Source | Section | Lines | Items |
|---|---|---|---|---|
| 1 | `.claude/skills/roblox-map/references/studio-mcp.md` | `execute_luau`: rules that keep Studio alive | 54-126 | 8 |
| 2 | `.claude/skills/roblox-map/references/studio-mcp.md` | Vetting Creator Store assets | 190-218 | 10 |
| 3 | `.claude/skills/roblox-map/references/studio-mcp.md` | Common build bugs | 236-252 | 12 |
| 4 | `.claude/skills/roblox-map/references/studio-mcp.md` | Checklist for agents | 263-286 | 13 |
| 5 | `.claude/skills/roblox-map/references/visual-quality.md` | "Does this look default?" checklist | 252-266 | 10 |
| 6 | `.claude/skills/roblox-map/references/visual-quality.md` | Checklist for agents | 267-288 | 12 |
| 7 | `.claude/skills/roblox-map/references/performance-and-devices.md` | Budget table | 27-46 | 12 |
| 8 | `.claude/skills/roblox-map/references/performance-and-devices.md` | Checklist for agents | 208-236 | 17 |

## 1. `execute_luau`: rules that keep Studio alive

Source: `.claude/skills/roblox-map/references/studio-mcp.md`, lines 54-126.

- Code runs on Studio's main thread. Until it yields, Studio is frozen, the script can't be
  stopped, and the MCP connection may drop (official tool description, 2026-10).
- Split heavy work (bulk parts, terrain, big loops) into chunks of about 1,000 items, and call
  `task.wait()` once per chunk, not once per item (official tool description, 2026-10).
- Build each chunk in a container outside the DataModel and parent it before that chunk's
  `task.wait()`. A `.Parent` write costs time in proportion to the whole subtree, so parenting
  one giant container is itself a freeze (official tool description, 2026-10).
- Make each batch one undo step: `ChangeHistoryService:TryBeginRecording(name)` returns an ID,
  and `ChangeHistoryService:FinishRecording(id, Enum.FinishRecordingOperation.Commit)` closes
  it. It returns `nil` if a recording is already running or during a solo playtest, so check
  for `nil` (official, 2026-10). `SetWaypoint` is due to be deprecated in its favor (official,
  2026-10).
- Run the batch inside `pcall` and finish the recording on every path: `Commit` when it
  worked, `Cancel` when it threw. A batch that errors between `TryBeginRecording` and
  `FinishRecording` leaves the recording open, and every later `TryBeginRecording` then
  returns `nil` (official: a recording already in progress, 2026-10), so the rest of the
  session builds with no undo (inferred).
- Make batches safe to re-run: find-or-create by name instead of always creating, so a retry
  doesn't double the map (inferred).
- Return one short summary string (counts and paths), not a print per part. Tool output fills
  the agent's context (inferred).
- Build in `Edit`. Instances created inside a playtest's `Client` or `Server` datamodel are gone
  when the playtest stops (inferred).

```lua
--!strict
-- One batch: a row of greybox platforms. Built off the DataModel, parented once, one undo step,
-- and the recording is finished on every path: Commit if the batch worked, Cancel if it threw.
local ChangeHistoryService = game:GetService("ChangeHistoryService")
local CollectionService = game:GetService("CollectionService")

local SPACING = 20 -- studs between platform centers, from the map brief
local island = workspace:FindFirstChild("Island")
local layout = if island then island:FindFirstChild("Layout") else nil
if not layout then
	return "missing Workspace.Island.Layout; run the setup batch first"
end
if layout:FindFirstChild("Zone1") then
	return "Zone1 already exists; nothing built"
end

local recording = ChangeHistoryService:TryBeginRecording("GreyboxZone1", "Greybox zone 1")
local ok, result = pcall(function()
	local zone = Instance.new("Folder")
	zone.Name = "Zone1"
	for i = 1, 8 do
		local platform = Instance.new("Part")
		platform.Name = `Platform{i}`
		platform.Anchored = true
		platform.Size = Vector3.new(12, 2, 12)
		platform.Position = Vector3.new(0, 10, i * SPACING)
		platform.Color = Color3.fromRGB(120, 170, 90) -- palette: ground mid
		platform.Material = Enum.Material.Grass
		platform:SetAttribute("Surface", "grass")
		CollectionService:AddTag(platform, "Platform")
		platform.Parent = zone
	end
	zone.Parent = layout
	return `Zone1: {#zone:GetChildren()} platforms`
end)
if recording then
	-- Always finish what was begun. An open recording makes every later TryBeginRecording nil.
	ChangeHistoryService:FinishRecording(recording,
		if ok then Enum.FinishRecordingOperation.Commit else Enum.FinishRecordingOperation.Cancel)
end
if not ok then
	return `Zone1 failed{if recording then " and was undone" else " (no undo recording was open)"}: {result}`
end
return result .. (if recording then "" else " (no undo recording: TryBeginRecording returned nil)")
```

## 2. Vetting Creator Store assets

Source: `.claude/skills/roblox-map/references/studio-mcp.md`, lines 190-218.

- The Creator Store bans obfuscated code, hidden engine features (`getfenv()`, `setfenv()`) and
  loading remote assets (`require(assetId)`, `loadstring()`, `InsertService:LoadAsset()`). It
  warns that useful-looking assets "could load another 'virus' asset at runtime" (official,
  2026-10). Bans aren't guarantees, so vet anyway (inferred).
- An asset's details page lists its script count, and Explorer → right-click → **Disable Scripts**
  stops an object's scripts from running (official, 2026-10).
- Search results can be filtered by creator verification status (official, 2026-10). The MCP's
  `verifiedCreatorsOnly` option does this for `search_asset` (official tool schema, 2026-10).
- Community practice: treat free models as placeholders, strip their scripts after inserting,
  and be wary of new or bot-named creators (community, 2020-04).
  - Search the place for `require`, `loadstring`, `getfenv` and `setfenv` (community, 2020-04).
  - Some backdoors behave differently when they detect Studio (community, 2020-04).
  - Automatic scanners help, but new obfuscation can get past them (community, 2026-07).
- Inserting another owner's inventory asset shares it across owners, so the server's own
  guidance is to ask the user first (official tool schema, 2026-10). Restricted assets without
  permission don't load in Studio or at runtime (official, 2026-10).

After every insert, before moving on (inferred):
- [ ] Every `Script`, `LocalScript` and `ModuleScript` (`IsA("LuaSourceContainer")`) is deleted
      unless the brief wants its behavior, and each one is listed in the report.
- [ ] Every part is anchored and in `Dressing`, and decoration has `CanCollide`, `CanTouch` and
      `CanQuery` off.
- [ ] Its size (`Model:GetExtentsSize()`) is sane against the ~5-stud avatar, with no hidden parts
      far from the visible model.
- [ ] It's recolored to the palette where it allows, or swapped out.
- [ ] It isn't another game's signature asset. Describe designs; never copy assets.

## 3. Common build bugs

Source: `.claude/skills/roblox-map/references/studio-mcp.md`, lines 236-252.

| Symptom | Cause | Fix |
|---|---|---|
| Studio freezes, MCP disconnects | One huge unyielding batch or `.Parent` write | Chunks of ~1,000 with `task.wait()`, each parented separately (official tool description, 2026-10) |
| Map doubled after a retry | Batch always creates | Find-or-create by name; check before building (inferred) |
| Undo removes nothing, or one part at a time | No recording, or `TryBeginRecording` returned `nil` | Check the ID; finish every recording you start (official, 2026-10) |
| Every batch after a failed one has no undo | The failed batch threw before `FinishRecording`, so its recording stayed open | `pcall` the batch; `Commit` on success, `Cancel` on error (official: an open recording blocks new ones, 2026-10) |
| Flickering faces | Coplanar overlapping surfaces (z-fighting) | Offset one part ~0.01 stud or resize so they don't overlap; don't use unions as the fix (community, 2020-05) |
| Parts fall when play starts | Not anchored | `Anchored = true` on everything static (official, 2026-10) |
| Players blocked by invisible props | Decoration still collides | `CanCollide`, `CanTouch`, `CanQuery` off in `Dressing` (official, 2026-10) |
| A moved model comes apart | Moved part by part | `Model:PivotTo()` moves the whole model (official, 2026-10) |
| Studio edits vanish after `rojo serve` | Built inside a Rojo `$path` folder | Build outside mapped folders (community: Rojo docs, 2026-10) |
| Generated mesh is the wrong size | Generation size is approximate | Scale after generating (official, 2026-10) |
| Hand edits to a prop reset | It's a ProceduralModel that regenerated | Copy its parts into a plain Model first (inferred) |
| An inserted asset vanishes in game | Restricted asset without permission | Use another asset (official, 2026-10) |

## 4. Checklist for agents

Source: `.claude/skills/roblox-map/references/studio-mcp.md`, lines 263-286.

#### Do
- Check `get_studio_state` and read the tree before building. Never assume an empty place.
- Build in `Edit`, in batches of one structure (≤ ~1,000 instances), each one undo recording.
- Take sizes and spacing from the brief; put gameplay parts in `Layout` with glossary tags and
  decoration in `Dressing` with collisions off.
- Prefer parts, then procedural models, then vetted Creator Store assets, then generated meshes.
- Strip and report scripts in every inserted asset; recolor everything to the palette.
- Screenshot the brief's check views after each structure and at the end of a pass; run the
  phone view and scene analysis before reporting.
- List anything the user must set by hand (`LightingStyle`, `PrioritizeLightingQuality`,
  `Workspace.StreamingEnabled`).

#### Don't
- Don't run one giant unyielding script, or parent a huge subtree in one write.
- Don't build inside Rojo-mapped folders or create scripts during a map pass.
- Don't hand-edit inside a ProceduralModel you want to keep.
- Don't keep inserted scripts you haven't read, or insert another owner's inventory assets
  without asking.
- Don't search for or insert another game's assets to copy that game.
- Don't call a pass done from screenshots alone when the brief has gameplay numbers; ask for a
  playtest.

## 5. "Does this look default?" checklist

Source: `.claude/skills/roblox-map/references/visual-quality.md`, lines 252-266.

Fail the build if any answer is "no":
- [ ] `LightingStyle` and `PrioritizeLightingQuality` chosen on purpose, with a preset applied and
      tuned.
- [ ] An `Atmosphere`, a non-default `Sky`, and a `ColorCorrectionEffect` exist.
- [ ] No visible part is default gray `Plastic`, and the template `Baseplate` is gone.
- [ ] The palette is ≤ 5 hues plus neutrals and lives in one `Palette` module.
- [ ] In grayscale (`Saturation = -1`), hazards, path and collectibles are still distinct.
- [ ] Large shapes have bevels or trims, and props vary in size and rotation.
- [ ] The ground uses ≥ 2 materials or terrain, with transitions (edges, foliage, rocks).
- [ ] Each zone has a landmark visible from spawn.
- [ ] `Neon` is accent-only, and bloom doesn't wash out white surfaces.
- [ ] Screenshots on an entry-level phone profile look readable at low screen brightness.

## 6. Checklist for agents

Source: `.claude/skills/roblox-map/references/visual-quality.md`, lines 267-288.

#### Do
- Set `LightingStyle` and `PrioritizeLightingQuality` in Properties (not scriptable), and ask the user
  if the MCP can't.
- Start from one of the four presets, then tune `Brightness`/`ExposureCompensation` on a phone
  profile.
- Add `Atmosphere`, a custom `Sky`, and a `ColorCorrectionEffect`. Keep bloom thresholds ≥ 0.9.
- Keep a shared `Palette` module; give hazards, accents and safe ground fixed, distinct roles.
- Use built-in materials and `MaterialVariant` for consistency; use `SurfaceAppearance` only on
  hero meshes.
- Bevel, trim, layer props, and vary scale and rotation.

#### Don't
- Don't set or mention `Lighting.Technology` (deprecated) or rely on legacy fog with an
  `Atmosphere`.
- Don't ship fresh `DepthOfFieldEffect` or `SunRaysEffect` defaults, or use DOF in gameplay.
- Don't make shadows, sun rays, DOF or color alone carry gameplay information.
- Don't leave default gray `Plastic`, the template `Baseplate`, or the default sky.
- Don't use pure black darkness for horror; use fog, low ambient and local lights.
- Don't stack semi-transparent parts or use many unique large textures.

## 7. Budget table

Source: `.claude/skills/roblox-map/references/performance-and-devices.md`, lines 27-46.

| Budget | Target | Tag |
|---|---|---|
| Frame time, client and server | ≤ 16.67 ms per frame (60 FPS). Server heartbeat is capped at 60. | official, 2026-10 |
| Draw calls on your baseline device | < 1,000 (Roblox's own example budget) | official, 2026-10 |
| Triangles drawn on your baseline device | < 1,000,000 (same example) | official, 2026-10 |
| Triangles per mesh | ≤ 20,000 (hard limit) | official, 2026-10 |
| Texture resolution | ≤ 512×512 for most images, < 256×256 for minor ones | official, 2026-10 |
| Particles per emitter | Engine cap is 400/s on desktop and 100/s on mobile. Design for ≤ 50/s per emitter, ≤ 5 emitters in view. | official cap 2026-10; design target inferred |
| Remote calls per client | Engine throttle is ~500/s, shared by all RemoteEvents. Design for ≤ 20/s in total per client. | official throttle 2026-10; design target inferred |
| `UnreliableRemoteEvent` payload | < 1,000 bytes, or it's dropped | official, 2026-10 |
| Server memory | < 50% of (6.25 GiB + 100 MiB × peak players). 30 players gives ~9.18 GiB. Memory doesn't shrink when players leave. | official, 2026-10 |
| Crash rate (Creator Dashboard) | Investigate above 2–3% | official, 2026-10 |
| Whole-map part count | Old heuristics: ~4k parts for a fast FPS map, ~7k for slower round games, ≤ ~20k for low-end. These predate streaming, so use them only as a sanity ceiling. | community, 2019-06 |
| Shadow-casting lights | Only a few visible at once; turn `Shadows` off on the rest | inferred: no official cap, and each shadowed light adds shadow work |

Pick one baseline device early, check frame rate and memory on it throughout development, and
measure before and after each change (official, 2026-10).

## 8. Checklist for agents

Source: `.claude/skills/roblox-map/references/performance-and-devices.md`, lines 208-236.

#### Do
- Keep `StreamingEnabled` on, with `StreamOutBehavior = Opportunistic`,
  `ModelStreamingBehavior = Improved` and `StreamingIntegrityMode = PauseOutsideLoadedArea`.
- Put every client-scripted group in an `Atomic` model, and reach into the world with
  `WaitForChild(name, timeout)` or `FindFirstChild` plus a nil check.
- Set decoration to `Anchored`, `CanCollide/CanTouch/CanQuery = false`, and `CastShadow = false`
  when small, plus `CollisionFidelity = Box`.
- Reuse one mesh or texture asset ID per shape; keep textures ≤ 512².
- Keep visuals, tweens and NPC animation on the client. The server sends compact events only.
- Use `UnreliableRemoteEvent` (< 1,000 bytes) for high-rate cosmetic data, with sequence numbers.
- Disconnect connections, clear per-player tables on `PlayerRemoving`, and enable
  `PlayerCharacterDestroyBehavior`.
- Call `RequestStreamAroundAsync` before server teleports.
- Profile with the MicroProfiler and F9 memory before and after each big change, and test on a
  real low-end Android.

#### Don't
- Don't fire remotes every frame or send whole tables when one value changed.
- Don't run heavy logic in `Heartbeat` or `PreRender`, or tween on the server.
- Don't use `Persistent` models as a workaround for missing `WaitForChild` calls.
- Don't park big models or audio in `ReplicatedStorage`, where every client downloads them.
- Don't use `PreciseConvexDecomposition`, `RenderFidelity = Precise`, or partial transparency
  layers by default.
- Don't import a whole map as one file, which makes every duplicate mesh unique.
- Don't set `PhysicsSteppingMethod = Fixed` without a measured need.
- Don't trust Studio FPS or memory as proof that the game runs on phones.

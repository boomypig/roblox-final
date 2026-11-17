---
title: Building with the Studio MCP
type: fundamental
read-when: Building or dressing a map, props, terrain or lighting in Studio through the Studio MCP.
last-researched: 2026-10-26
---

# Building with the Studio MCP

## In one line

The AI builds by writing coordinates and calling generators, and it sees only screenshots and
the instance tree. So build gameplay layout from the brief's numbers, keep decoration in Studio
outside Rojo's folders, work in small undoable batches, screenshot after every structure, and
vet every outside asset before it stays.

## What the AI can and can't do here

- The Studio MCP server is built into Studio and runs locally over stdio. Turn it on in
  Assistant → **…** → **Manage MCP Servers** → **Enable Studio as MCP server** (official, 2026-10).
- Connected clients "can read and modify content in your open Roblox places", so only connect
  trusted clients (official, 2026-10).
- Every tool call takes a `studio_id`. Get it from `list_roblox_studios` (official, 2026-10).
- The AI has no hands or eyes in the viewport. It places by numbers, checks with
  `screen_capture`, and reads the tree with `search_game_tree` and `inspect_instance` (inferred).
  It does best with layouts described as numbers (radius, spacing, counts) and worst with
  free-form organic placement (inferred).
- The tool list changes between Studio versions. The docs list `subagent` types `explore` and
  `playtest`. A server queried on 2026-10-26 offered `explore`, `screen_capture` and `unit_test`,
  plus `generate_texture` and `segment_mesh`, which the docs page doesn't list (official docs vs
  the served tool list, 2026-10). Plan from the tools the server actually reports.

## Tools for building

| Tool | Use it for | Notes |
|---|---|---|
| `execute_luau` | Creating and editing parts, lighting, terrain | `datamodel_type` is `Edit`, `Client` or `Server`; build in `Edit` (official, 2026-10) |
| `search_game_tree`, `inspect_instance` | Reading what's already there | Flat JSON tree with depth limits; properties, attributes, children summary (official, 2026-10) |
| `generate_procedural_model` | Props made of primitive parts, with tunable attributes | Takes a reference image through `store_image` (official, 2026-10) |
| `generate_mesh` | One textured mesh from a text prompt | `maxTriangles` 12–20,000 and a bounding `size` (official tool schema, 2026-10) |
| `generate_material` | A `MaterialVariant` from a text description | Returns a base material and a variant name; set both `BasePart.Material` and `BasePart.MaterialVariant` (official tool schema, 2026-10) |
| `generate_texture` | Re-texturing an existing MeshPart or Model | Replaces the source in place (official tool schema, 2026-10) |
| `segment_mesh` | Splitting a mesh into named parts | Up to 5 part names per run (official, 2026-10) |
| `search_asset`, `insert_asset` | Creator Store and your inventory | Results include creator and a thumbnail URL (official tool schema, 2026-10) |
| `screen_capture` | Seeing the build | Optional `camera_position` and `look_at_position` (official, 2026-10) |
| `start_stop_play`, `character_navigation`, `get_console_output` | Walking the path in a playtest | Navigation runs in the `Client` datamodel (official tool schema, 2026-10) |
| `wait_job_finished` | Collecting async generation jobs | Start generations with `async: true` (official tool schema, 2026-10) |
| `skill` | Roblox's reference packs | `rbx-device-simulator-lua` (phone views), `rbx-scene-analysis` (counts, memory) (official tool schema, 2026-10) |

`upload_image` turns image URLs into assets on the account, so use it only when the brief asks
for a new decal or texture (official, 2026-10).

## `execute_luau`: rules that keep Studio alive

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
- Make batches safe to re-run: find-or-create by name instead of always creating, so a retry
  doesn't double the map (inferred).
- Return one short summary string (counts and paths), not a print per part. Tool output fills
  the agent's context (inferred).
- Build in `Edit`. Instances created inside a playtest's `Client` or `Server` datamodel are gone
  when the playtest stops (inferred).

```lua
--!strict
-- One batch: a row of greybox platforms. Built off the DataModel, parented once, one undo step.
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
	CollectionService:AddTag(platform, "Platform")
	platform.Parent = zone
end
zone.Parent = layout
if recording then
	ChangeHistoryService:FinishRecording(recording, Enum.FinishRecordingOperation.Commit)
end
return `Zone1: {#zone:GetChildren()} platforms`
```

## Where things go

- **Rojo.** In a project node with `$path`, `$ignoreUnknownInstances` defaults to `false`, so
  Rojo removes instances it doesn't know about inside that folder. Nodes without `$path` default
  to `true` (community: Rojo docs, 2026-10). The starter project maps only three script folders,
  so anything built in Workspace, ServerStorage or Lighting is safe. Anything built inside a
  mapped folder gets wiped on sync (inferred from those defaults).
- Rojo turns files into instances, including `.rbxm` and `.rbxmx` models (community: Rojo docs,
  2026-10). Its sync runs from files into Studio. Don't count on Studio edits flowing back into
  a file (inferred). Keep map backups in the repo but out of `default.project.json`, or a sync
  can overwrite Studio edits with the old file (inferred).
- **Two folders per map** (inferred):
  - `Layout`: what gameplay touches (floors, platforms, walls, hazards, checkpoints, spawn
    pads), tagged with the glossary's CollectionService tags.
  - `Dressing`: decoration only. Then the layout can be rebuilt or retuned without wiping the
    decoration, and code can ignore `Dressing` entirely.
- **Code-built greyboxes** are reproducible and reviewable in git, which suits testing a loop
  early. Once anyone dresses the map by hand, Studio is the source: regenerating from code would
  erase the dressing (inferred, from the first game's decision log).
- **ProceduralModels** rebuild their contents from a generator ModuleScript when `Size`, their
  attributes or the generator's source change. Generation runs in a temporary `GeneratedFolder`
  and the results replace the model's contents (official, 2026-10). So hand edits inside one can
  be lost on the next regeneration. To hand-edit a generated prop, copy its parts into a plain
  Model first (inferred).
- ProceduralModels can't become packages and don't generate inside `Actor`s. Ones inserted from
  the Creator Store get `Sandboxed = true` on their generator (official, 2026-10).
- **Packages** suit repeated kit pieces (a lamp, a tree set, a platform type). Right-click →
  **Convert to Package**. With `AutoUpdate` on the `PackageLink`, copies update when a place
  opens. Modified copies don't auto-update. Never delete or move the `PackageLink`, and pick the
  owner carefully, because ownership can't be transferred (official, 2026-10). The docs suggest
  greyboxing with placeholder packages that update when the detailed version is published
  (official, 2026-10).

## Choosing a source for each object

Use the cheapest source that matches the art direction, in this order (inferred):

1. **Parts.** Free, instant, exact sizes, and the palette is fully under control. Each axis can
   be 0.001–2,048 studs, and anything under 0.05 is simulated as 0.05 (official, 2026-10). Use
   wedges for bevels and trim ([visual-quality](visual-quality.md)).
2. **`generate_procedural_model`.** Props built from primitives, so they match a parts-built
   world (inferred). Assistant allows 50 procedural models per rolling 24 hours (official,
   2026-10). Treat that as the MCP tool's budget too (inferred). Generated models have up to
   8 named parts (official, 2026-10).
3. **Creator Store.** Huge variety, but each asset needs vetting (next section) and recoloring to
   the palette, and its style often doesn't match (inferred).
4. **`generate_mesh`.** For a hero object parts can't make. Assistant's default cap is 10,000
   triangles and the hard per-mesh limit is 20,000 ([performance](performance-and-devices.md))
   (official, 2026-10). Assistant takes a text prompt or an image, not both (official, 2026-10).
   Generated size is approximate, so scale it after (official, 2026-10).

- **Surfaces:** for one consistent custom surface (moss stone, painted wood), use
  `generate_material` once and reuse the variant everywhere. The Material Generator's
  **Studs Per Tile** and **Organic** options control tiling and repetition (official, 2026-10).
- **Terrain** for natural ground and water. Call `Terrain:FillBlock`, `Terrain:FillBall`,
  `Terrain:FillCylinder` or `Terrain:FillWedge` from `execute_luau`, and
  `Terrain:ReplaceMaterial` to repaint (official, 2026-10).
  - Voxels are 4 studs, and region methods need resolution 4 and grid-aligned regions
    (`Region3:ExpandToGrid(4)`) (official, 2026-10).
  - `Terrain:ReadVoxels` and `Terrain:WriteVoxels` handle at most 4,194,304 voxels per call, so
    chunk big areas (official, 2026-10).
  - `Terrain:SetMaterialColor` shifts a material toward the palette (official, 2026-10).

## Vetting Creator Store assets

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

## Seeing the build

- `screen_capture` grabs the edit viewport. Passing `camera_position` and `look_at_position`
  moves the camera only for that capture (official tool description, 2026-10). Reuse the brief's
  check views every pass, so before and after are directly comparable (inferred).
- Screenshots are the most expensive thing in an agent's context. Capture at decision points
  (after a structure, at the end of a pass), not after every part (inferred).
- Phone check: the `rbx-device-simulator-lua` skill switches Device Simulator profiles through
  `execute_luau` and `screen_capture` (official skill description, 2026-10).
- Counts and memory: the `rbx-scene-analysis` skill reads SceneAnalysisService for rendering,
  memory and instance composition (official skill description, 2026-10).
- Walk test: `start_stop_play`, then `character_navigation` (in `Client`) to each checkpoint,
  then `get_console_output`, then stop play (official, 2026-10). A walk proves a route exists. It
  doesn't prove a jump is fair at the game's speed, so playtest by hand too (inferred).
- Grayscale check: temporarily set a `ColorCorrectionEffect.Saturation` to -1, capture, then
  restore it ([visual-quality](visual-quality.md)).

## Common build bugs

| Symptom | Cause | Fix |
|---|---|---|
| Studio freezes, MCP disconnects | One huge unyielding batch or `.Parent` write | Chunks of ~1,000 with `task.wait()`, each parented separately (official tool description, 2026-10) |
| Map doubled after a retry | Batch always creates | Find-or-create by name; check before building (inferred) |
| Undo removes nothing, or one part at a time | No recording, or `TryBeginRecording` returned `nil` | Check the ID; finish every recording you start (official, 2026-10) |
| Flickering faces | Coplanar overlapping surfaces (z-fighting) | Offset one part ~0.01 stud or resize so they don't overlap; don't use unions as the fix (community, 2020-05) |
| Parts fall when play starts | Not anchored | `Anchored = true` on everything static (official, 2026-10) |
| Players blocked by invisible props | Decoration still collides | `CanCollide`, `CanTouch`, `CanQuery` off in `Dressing` (official, 2026-10) |
| A moved model comes apart | Moved part by part | `Model:PivotTo()` moves the whole model (official, 2026-10) |
| Studio edits vanish after `rojo serve` | Built inside a Rojo `$path` folder | Build outside mapped folders (community: Rojo docs, 2026-10) |
| Generated mesh is the wrong size | Generation size is approximate | Scale after generating (official, 2026-10) |
| Hand edits to a prop reset | It's a ProceduralModel that regenerated | Copy its parts into a plain Model first (inferred) |
| An inserted asset vanishes in game | Restricted asset without permission | Use another asset (official, 2026-10) |

## Saving and backups

- Map geometry isn't in git. Place **Version History** (Window → Version History) tracks saved
  and published versions. Restoring creates a new version rather than overwriting history, and
  **Open Local Copy** lets you inspect an old version first (official, 2026-10).
- Right-click an instance → **Save to File** writes an `.rbxm` (official, 2026-10: documented for
  animations; the same command exists for any instance (inferred)). At milestones, commit each
  map's `.rbxm` under `maps/`, outside the Rojo project (inferred).
- Save the place before a big pass so Version History has a clean point to return to (inferred).

## Checklist for agents

### Do
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

### Don't
- Don't run one giant unyielding script, or parent a huge subtree in one write.
- Don't build inside Rojo-mapped folders or create scripts during a map pass.
- Don't hand-edit inside a ProceduralModel you want to keep.
- Don't keep inserted scripts you haven't read, or insert another owner's inventory assets
  without asking.
- Don't search for or insert another game's assets to copy that game.
- Don't call a pass done from screenshots alone when the brief has gameplay numbers; ask for a
  playtest.

## Related

- [visual-quality.md](visual-quality.md): lighting presets, palette, materials, "does this look
  default?" checklist
- [performance-and-devices.md](performance-and-devices.md): budgets, streaming, collision fidelity
- [quality-bar.md](quality-bar.md): what "done" means for a build
- [first-time-experience.md](first-time-experience.md): spawn area and first minutes
- [checkpoints-and-respawn.md](../patterns/checkpoints-and-respawn.md): fall zones, spawn pads,
  `FallenPartsDestroyHeight`

## Sources

1. https://create.roblox.com/docs/studio/mcp: built-in MCP server, enabling it, tool list, `datamodel_type`, `studio_id`, trust warning (updated 2026-10-23)
2. Studio MCP server tool descriptions as served to a client on 2026-10-26 (no public URL): `execute_luau` chunking and `.Parent` cost, `screen_capture` camera options, `generate_material`, `generate_texture`, `segment_mesh`, `search_asset` cross-owner guidance, subagent types, `skill` list
3. https://create.roblox.com/docs/assistant/guide: 50 procedural models per rolling 24 h, `/generate_mesh` text or image and 10,000-triangle default, 8-part segmentation, screen capture subagent
4. https://create.roblox.com/docs/parts/procedural-models: generator module, regeneration, `GeneratedFolder`, sandboxing, no packages, no Actors
5. https://create.roblox.com/docs/reference/engine/classes/GenerationService: Cube 3D generation, approximate size, rate-limit errors
6. https://create.roblox.com/docs/reference/engine/classes/ChangeHistoryService: `TryBeginRecording`, `FinishRecording`, `nil` cases, `SetWaypoint` deprecation notice
7. https://create.roblox.com/docs/reference/engine/classes/BasePart: size limits, `Anchored`, `CanCollide`, `CanTouch`, `CanQuery`, `PivotTo`
8. https://create.roblox.com/docs/reference/engine/classes/Terrain: fill methods, 4-stud resolution, voxel limits, `SetMaterialColor`
9. https://create.roblox.com/docs/projects/assets/packages: converting, `AutoUpdate`, `PackageLink`, ownership, placeholder greyboxing
10. https://create.roblox.com/docs/production/creator-store: banned practices, script count, Disable Scripts, verification filter, restricted assets
11. https://create.roblox.com/docs/studio/material-generator: material variants from text, Studs Per Tile, Organic
12. https://create.roblox.com/docs/projects/version-history: Version History window, restore as new version, Open Local Copy
13. https://create.roblox.com/docs/education/build-it-play-it-island-of-move/sharing-animations: Save to File writes `.rbxm`
14. https://rojo.space/docs/v7/project-format/: `$ignoreUnknownInstances` defaults
15. https://rojo.space/docs/v7/sync-details/: `.rbxm`/`.rbxmx` support, file-to-instance rules
16. https://devforum.roblox.com/t/how-to-remove-backdoors-from-your-game: free models as placeholders, strip scripts, search strings, Studio-detecting backdoors (2020-04)
17. https://devforum.roblox.com/t/shieldscan-anti-backdoor-scanner-for-roblox-studio/4736119: scanners miss new obfuscation (2026-07)
18. https://devforum.roblox.com/t/glitchy-looking-blocks/566033/8: z-fighting fix by offset or resize, not unions (2020-05)

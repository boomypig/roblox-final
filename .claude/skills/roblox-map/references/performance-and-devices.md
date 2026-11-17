---
title: Performance and devices
type: fundamental
read-when: Building maps or effects that must run on low-end phones.
last-researched: 2026-10-22
---

# Performance and devices

## In one line

Build for an entry-level Android phone first. Stream the world, make decoration physics-free,
budget draw calls and texture memory, keep per-frame work and remote traffic small, and measure
on real hardware before calling anything done.

## Who the low end is

- In one game, Android crash rate held at 10–15% while iOS was ~2% and PC/console ~0%. Android
  memory averaged 1.2–1.4 GB at 27–33 FPS. The post calls phones with under 2 GB of RAM
  "particularly unstable" (community, 2024-10).
- Roblox can't use all of a device's memory, because the OS and other apps need some (official, 2026-10).
- Memory, not part count, is what crashes phones. Treat client memory as the main budget
  (inferred, from the two points above).
- Shadows turn off automatically below graphics quality level 4, so low-end players see the scene
  without them. Never use a shadow as a gameplay cue (official, 2026-10).

## Budget table

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

## Instance streaming

Streaming is the biggest single lever on client memory and join time (official, 2026-10).
`Workspace.StreamingEnabled` is on by default for new places, and it can only be set in Studio,
not from a script (official, 2026-10). Set these `Workspace` properties in Studio:

| Property | Default | Set to | Why |
|---|---|---|---|
| `StreamingMinRadius` | 64 | 64 | Lets the engine scale down for low-end devices. Raising it costs memory and server bandwidth (official, 2026-10). |
| `StreamingTargetRadius` | 1024 | 1024 for open maps; lower for dense maps | Lowering it is a documented way to stream more aggressively (official, 2026-10). |
| `StreamOutBehavior` | `Default` (behaves as `LowMemory`) | `Opportunistic` | Streams out content well beyond the target radius even without memory pressure, which helps prevent out-of-memory crashes (official, 2026-10). |
| `ModelStreamingBehavior` | `Legacy` | `Improved` | Under `Improved`, models are never sent during join (official, 2026-10). |
| `StreamingIntegrityMode` | — | `PauseOutsideLoadedArea` | Pauses the player instead of letting them walk into unloaded space (official, 2026-10). |
| `EnableSLIMAvatars` | engine rollout | `Enabled` | Distant avatars render as lightweight stand-ins (official, 2026-10). |
| `PredictiveStreamingMode` | `Default` (behaves as disabled) | `Enabled` for maps with frequent teleports | Pre-fetches spawn and teleport areas. It's skipped on constrained devices (official, 2026-10). |

`Model.ModelStreamingMode` per model (official, 2026-10):
- `Nonatomic` (default): follows `ModelStreamingBehavior`.
- `Atomic`: every initial descendant arrives together. `WaitForChild` the model only, not its parts.
  Use it for anything a client script walks through, such as a door with its parts or a shop stand.
- `Persistent`: sent after join, before `Workspace.PersistentLoaded` fires, and never streamed out.
  It permanently uses memory, so use it rarely.
- `PersistentPerPlayer`: persistent only for players added with `Model:AddPersistentPlayer()`.
  Undo with `Model:RemovePersistentPlayer()`.

Client-script rules under streaming (official, 2026-10):
- Never index `workspace.Map.Shop.Door` directly from a LocalScript. Use `WaitForChild(name, timeout)`
  when the script can't continue without the instance. Otherwise use `FindFirstChild` and check
  for nil.
- An instance that streams out is parented to `nil`, not destroyed. Local-only property changes
  are lost when it streams back in.
- `ChildAdded`, `ChildRemoved` and `CollectionService:GetInstanceAddedSignal()` /
  `GetInstanceRemovedSignal()` also fire on stream-in and stream-out. Don't treat them as spawn or
  death events on the client.
- Before a server-side teleport, call `player:RequestStreamAroundAsync(targetPosition)`. Use
  `Player:AddReplicationFocus()` sparingly: one player with nine moving foci costs about as much
  as ten players.
- Client-side physics only simulates inside streamed areas.
- `ReplicatedStorage` and `ReplicatedFirst` are not streamed. Everything in them downloads at
  join. Keep large or rarely used assets in `ServerStorage` and clone them into `Workspace` when
  needed. Keep `ReplicatedFirst` to the loading screen.
- `Model.LevelOfDetail = SLIM` fills in distant static models. It doesn't support animated or
  runtime-modified models. Keep each model's extent small; the docs suggest about 64 studs.
- Test with `StreamingTargetRadius = 64` and teleport across the whole map. Streaming bugs show up
  at edges and during transitions, often as `attempt to index nil` errors.

## Parts, meshes, physics

- **Decoration:** set `Anchored = true`, `CanCollide = false`, `CanTouch = false` and
  `CanQuery = false`. Parts with both `CanTouch` and `CanCollide` off skip collision computation.
  `CanQuery` only takes effect when `CanCollide` is false (official, 2026-10). A part with
  collisions on still holds collision geometry in memory (official, 2026-10).
- **`CollisionFidelity`:** use `Box` for small or non-interactive meshes; it has the lowest memory
  cost. Use `Hull` for small-to-medium interactive ones. For large complex meshes, add invisible
  simple parts as custom collision. Avoid `PreciseConvexDecomposition`. To find offenders, filter
  the Explorer by `CollisionFidelity=PreciseConvexDecomposition` (official, 2026-10).
- **`MeshPart.RenderFidelity`:** use `Automatic` or `Performance`. `Automatic` draws full detail
  under 250 studs, medium from 250–500, and lowest beyond 500. Too many `Precise` meshes is a
  documented frame-time problem (official, 2026-10).
- **Shadows:** set `CastShadow = false` on small, distant and moving parts, and `Light.Shadows = false`
  where no shadow is needed (official, 2026-10).
- **Instancing:** meshes with the same `MeshContent` and the same `SurfaceAppearance` or
  `TextureContent` share one draw call. Upload each mesh once and duplicate it in Studio; the
  importer doesn't de-duplicate, so a whole-map import makes every copy unique (official, 2026-10).
- **Unions vs meshes:** CSG results above 20,000 triangles are simplified, unions use box-mapped
  UVs, and runtime `UnionAsync`/`SubtractAsync` is asynchronous and costly (official, 2026-10).
  For repeated shapes, convert to one MeshPart and duplicate it (inferred: shared asset IDs are
  what instancing needs).
- **Transparency:** keep it at 0 or 1. Partial transparency causes overdraw, and stacked
  semi-transparent layers make it worse (official, 2026-10).
- **Physics:** leave `Workspace.PhysicsSteppingMethod` on `Default` (currently `Adaptive`:
  60/120/240 Hz per assembly). `Fixed` runs everything at 240 Hz (official, 2026-10). Anchor
  anything that doesn't need simulation, minimize constraints, and limit ragdoll self-collision
  (official, 2026-10).
- **NPCs:** use an `AnimationController` instead of a `Humanoid` for static NPCs. Disable unused
  states with `Humanoid:SetStateEnabled()` (for example `Climbing`). Pool NPC models instead of
  destroying and re-creating them, spawn them only near players, and play their animations on the
  client (official, 2026-10).

## Textures, particles, lights, audio

- Texture memory scales with pixel count, not file size. A 1024² texture costs four times a 512²
  one, and compression or dropping alpha doesn't help (official, 2026-10).
- Prefer built-in materials over custom textures (official, 2026-10). Tint one texture with
  `SurfaceAppearance.Color` instead of uploading colour variants. Use sprite sheets for UI with
  `ImageLabel.ImageRectOffset`/`ImageRectSize` (official, 2026-10).
- Particles: keep `Rate` as low as the look allows. Large particles cost fill-rate and overlapping
  particles cause overdraw (official, 2026-10). Changing `ParticleEmitter` properties at runtime
  can hurt performance badly, so don't animate emitter properties every frame (official, 2026-10).
- `ParticleEmitter:Emit(n)` bursts are reported to skip the engine's automatic graphics-quality
  scaling (community, 2020-10, unverified). Scale `n` on the client by
  `UserSettings():GetService("UserGameSettings").SavedQualityLevel`.
- Lights: limit PointLight/SpotLight `Range` and SpotLight `Angle`, use fewer lights, and disable
  lights outside the active area (official, 2026-10).
- Audio: load sounds when needed, not all at join (official, 2026-10).
- Preload with `ContentProvider:PreloadAsync()` only the loading screen, key menus and spawn-area
  assets, never all of `Workspace`. Offer a Skip button if preloading is long (official, 2026-10).

## Scripts: CPU and memory

- Keep heavy work out of `RunService.Heartbeat`, `PreSimulation`, `PostSimulation`, `PreRender`
  and `PreAnimation`. Reserve them for camera and true per-frame needs (official, 2026-10). Server
  game loops should tick every 0.1–1 s with `task.wait`, or be event-driven (inferred).
- Split big jobs across frames. A 100 ms task run every frame caps the game at 10 FPS; at ~5 ms
  per frame with `task.wait()` between chunks, it holds 60 FPS (official, 2026-10).
- Parallel Luau (Actors) suits work that doesn't touch the data model. `--!native` or `@native`
  speeds up numeric-heavy server scripts but adds compile time at server start, so don't put it on
  every script (official, 2026-10).
- Wrap suspect code in `debug.profilebegin("name")`/`debug.profileend()` so it shows in the
  MicroProfiler (official, 2026-10).
- Avoid deep-cloning or serializing large tables in hot paths (official, 2026-10).
- **Leaks:** call `RBXScriptConnection:Disconnect()`, or `Destroy()` the owning instance. Set
  `Workspace.PlayerCharacterDestroyBehavior = Enabled` so old characters and departed `Player`
  objects are destroyed. Clear per-player tables on `PlayerRemoving` (official, 2026-10). A steadily
  rising `LuaHeap` or `InstanceCount` means a leak (official, 2026-10).
- Never tween with `TweenService` on the server: the property replicates every frame. Tween on
  the client (official, 2026-10).

## Network and replication

- Replicate state when it changes, not every frame. Send IDs and deltas, for example the one item
  bought rather than the whole inventory (official, 2026-10).
- Visual effects run client-side; the server sends only what and where. First-person viewmodels
  stay client-side (official, 2026-10).
- Over the throttle, `RemoteEvent` queues excess client calls and `UnreliableRemoteEvent` drops
  them (official, 2026-10).
- Use `UnreliableRemoteEvent` for ephemeral high-rate data such as aim direction or cosmetic
  positions. Delivery is unordered and not guaranteed, so add a sequence number and drop stale
  messages (official, 2026-10).
- What survives a remote: functions become nil, metatables are stripped, and non-string keys are
  converted to strings. Don't mix array and dictionary keys. Instances the receiver can't see
  arrive as nil (official, 2026-10).
- Creating or destroying large instance trees replicates in bulk. Build maps in chunks across
  several frames (official, 2026-10).
- Avoid moving assemblies with very many instances, which cause network and CPU spikes
  (official, 2026-10).
- **Network ownership:** the engine hands unanchored parts near a player to that client. That
  saves server physics, but the client then controls those parts. Call `SetNetworkOwner(nil)` on
  gameplay-critical parts; it may add jitter. Anchored parts are always server-owned
  (official, 2026-10). See [security](../../roblox-code/references/security.md).

## Measuring

| Tool | Opens with | Use it for |
|---|---|---|
| Developer Console | F9 | **Memory**: PlaceMemory categories such as `GraphicsTexture`, `GraphicsMeshParts`, `Sounds`, `PhysicsParts`, plus `PlaceScriptMemory` and LuauHeap snapshots. **Network** lists only web calls (HttpService, DataStores), not remote traffic. **Server Jobs** shows heartbeat (official, 2026-10). |
| MicroProfiler | Ctrl+Alt+F6 | Frame spikes. Scopes include `physicsStepped`, `worldStep`, `ProcessPackets` (incoming), `Allocate Bandwidth and Run Senders` (outgoing), `ShadowMapSystem`, `updateInvalidatedFastClusters` (> 4 ms means avatar rebuilds) (official, 2026-10). |
| Performance Stats | Ctrl+Alt+F7 | Memory, CPU, GPU, network and ping overlay (official, 2026-10). |
| Render stats | Shift+F2 | Draw calls and triangles (official, 2026-10). |
| Network stats / streaming view | Shift+F3, then Shift+1 to cycle panels | Bandwidth and the streaming debug view (official, 2026-10). |
| Device Simulator (Studio) | Studio toolbar | Screen size, DPI, touch, safe areas. It has Flagship, Mid-range and Entry-level phone profiles (official, 2026-10). |
| Network Simulator (Studio) | Studio toolbar | Latency, jitter, packet loss (official, 2026-10). |
| Print Join Size Breakdown | Studio Settings | Largest instances sent at join (official, 2026-10). |
| Creator Dashboard → Performance | Web | Live client memory, FPS, server heartbeat and crash rate per device (official, 2026-10). |

- Studio numbers aren't device numbers: Studio runs client and server in one process, so the
  emulator can't show real memory (official, 2026-10). Before shipping, play 10 minutes on a real
  2–3 GB RAM Android phone in a full server, then check F9 memory and Shift+F5 FPS (inferred).
- Test with several clients through Studio's Server & Clients mode (up to 8) to see per-player
  costs (official, 2026-10).

## Checklist for agents

### Do
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

### Don't
- Don't fire remotes every frame or send whole tables when one value changed.
- Don't run heavy logic in `Heartbeat` or `PreRender`, or tween on the server.
- Don't use `Persistent` models as a workaround for missing `WaitForChild` calls.
- Don't park big models or audio in `ReplicatedStorage`, where every client downloads them.
- Don't use `PreciseConvexDecomposition`, `RenderFidelity = Precise`, or partial transparency
  layers by default.
- Don't import a whole map as one file, which makes every duplicate mesh unique.
- Don't set `PhysicsSteppingMethod = Fixed` without a measured need.
- Don't trust Studio FPS or memory as proof that the game runs on phones.

## Related

- [visual-quality.md](visual-quality.md): lighting and materials within these budgets
- [game-feel.md](../../roblox-vfx/references/game-feel.md): client-side effects and particles
- [ui-ux.md](../../roblox-ui/references/ui-ux.md): mobile layout, sprite sheets
- [audience.md](../../../../vault/fundamentals/audience.md): device mix of target players
- [security.md](../../roblox-code/references/security.md): network ownership, remote validation
- [quality-bar.md](../../build/references/quality-bar.md): "done" criteria, including performance

## Sources

1. https://create.roblox.com/docs/workspace/streaming: streaming properties, defaults, model modes, foci cost, debug keys
2. https://create.roblox.com/docs/workspace/streaming/techniques: recommended values, script patterns, SLIM, test-at-64 advice
3. https://create.roblox.com/docs/performance-optimization/improve: script, physics, rendering, network, asset memory and load-time guidance
4. https://create.roblox.com/docs/performance-optimization/design: baseline device, 1,000 draw calls / 1M triangles example, 16.67 ms budget, emulator memory caveat
5. https://create.roblox.com/docs/performance-optimization/identify: tools, shortcuts, server memory formula, crash-rate threshold
6. https://create.roblox.com/docs/reference/engine/classes/Workspace: property names and defaults
7. https://create.roblox.com/docs/reference/engine/enums/StreamOutBehavior: enum values
8. https://create.roblox.com/docs/reference/engine/enums/ModelStreamingBehavior: Legacy vs Improved
9. https://create.roblox.com/docs/reference/engine/enums/PhysicsSteppingMethod: Default = Adaptive, Fixed = 240 Hz
10. https://create.roblox.com/docs/reference/engine/classes/BasePart: CanCollide/CanTouch/CanQuery/CastShadow behavior
11. https://create.roblox.com/docs/reference/engine/classes/MeshPart: RenderFidelity distances
12. https://create.roblox.com/docs/parts/solid-modeling: CSG triangle cap, runtime cost, UVs
13. https://create.roblox.com/docs/art/modeling/specifications: 20,000 triangles per mesh
14. https://create.roblox.com/docs/effects/particle-emitters: 400/s desktop, 100/s mobile, fill-rate and overdraw
15. https://create.roblox.com/docs/physics/network-ownership: automatic ownership, SetNetworkOwner, exploit risk
16. https://create.roblox.com/docs/scripting/events/remote: argument limitations, unreliable ordering
17. https://create.roblox.com/docs/reference/engine/classes/RemoteEvent: ~500 requests/s per client throttle
18. https://create.roblox.com/docs/reference/engine/classes/UnreliableRemoteEvent: 1,000-byte limit
19. https://create.roblox.com/docs/studio/developer-console: Memory and Network tabs
20. https://create.roblox.com/docs/studio/optimization/memory-usage: PlaceMemory categories
21. https://create.roblox.com/docs/studio/device-simulator: device profiles
22. https://create.roblox.com/docs/studio/testing-modes: multi-client testing, Network Simulator
23. https://create.roblox.com/docs/luau/native-code-gen: `--!native`, `@native`, compile-time cost
24. https://devforum.roblox.com/t/android-crash-rates/3227626: Android crash rate and memory figures (2024-10)
25. https://devforum.roblox.com/t/reasonable-brick-counts/290266: 2019 part-count heuristics
26. https://devforum.roblox.com/t/performance-considerations-improvements-and-optimizations-when-making-a-game/817499: Emit() and quality-level scaling claim (2020)

---
title: Building sandbox
type: genre
read-when: Building a creation/physics sandbox (Build a Boat-likes, block building, vehicle builders, saved worlds).
last-researched: 2026-10-22
---

# Building sandbox

## In one line

Players assemble things from a fixed catalog of blocks on a plot they own, then test them
against physics: a course, a distance, a fight. Saved builds and showing them off keep players
coming back. Building tools, save size, griefing and moderation are where these games succeed or
fail (inferred).

## Core loop

- **Moment to moment:** pick a block, aim at a face, rotate, place; delete and undo. Then launch
  and watch it work or fall apart (inferred).
- **Session (Build a Boat-like):** build on your team's plot, launch down a course of stages,
  earn gold for distance, spend it on chests and blocks, build bigger. Gold buys chests of random
  materials, decorations and abilities (community, 2026-08). Badges mark 10, 20 and 30 stages
  completed (community, 2026-08).
- **Session (creation sandbox):** build planes, cars, boats, rockets, mechs or houses; fly or
  drive them; show them off, or battle in PvP or peaceful mode. Plane Crazy offers all of these
  (official game description, 2026-10).
- **Long term:** unlock rarer blocks, fill save slots with builds, beat the full course, get known
  for a build (inferred).

## Main verbs

place, rotate, delete, undo, paint from a palette, weld or bind (mechanisms to keys), launch or
test, save or load, show or vote (inferred).

| Variant | Goal that gives building a point | Example (data, 2026-10-22) |
|---|---|---|
| Build, then a physics course | distance down a hazard course, gold per stage | Build A Boat For Treasure 10.7K |
| Vehicle and machine builder | it flies, drives, fights | Plane Crazy 3.6K |
| Voxel world | survive, decorate; worlds saved per private server (official game description) | Steve the Craftsman 8.0K |
| Build plus idle | build a car, it drives offline and earns (official game description) | Build a Car 435 |
| Free build together | shared centre builds, saved bases | Build with Friends 695 |
| Destruction | crush or smash; free build tools only in private servers (official game description) | Car Crushers 2 1.4K |

## Why players come back

1. **The test is a goal.** A course, a distance or a fight turns "build anything" into "build
   something that does X" (inferred). Build a Boat's gold depends on how far the boat gets
   (community guide, 2026; unverified).
2. **Unlocks feed the next build.** Each chest tier adds blocks or abilities (community,
   2026-08).
3. **Saved creations.** Players invest hours in a build. Losing it is the fastest way to lose them
   (inferred).
4. **Showing off.** Others see your build in the server, at a launch, in PvP or on video
   (inferred).
5. **Friends build together** on one team plot (inferred from team plots).

## What separates top games from clones

### Building tools

- **Grid.** Snap in plot object space: `cell = math.round(localPos / GRID)`. Use 1 stud (0.5 for
  detail blocks). Store integers, never raw CFrames (inferred).
- **Rotation.** 90° steps only, stored as an orientation index 0–23 (the 24 axis-aligned
  orientations of a cube) (inferred).
- **Aim.** Raycast from the camera through the cursor or touch point
  (`Camera:ViewportPointToRay`, then `Workspace:Raycast`), and place on the hit face along its
  normal. A ghost preview is tinted green if valid and red if not (community, 2026; inferred).
- **Mobile.** Tap a face to place. Buttons for rotate, delete mode, undo and confirm sit on the
  right; camera orbit stays on the default controls. Avoid drag placement that needs precision
  ([ui-ux](../fundamentals/ui-ux.md)) (inferred).
- **Undo.** Keep a per-player stack on the server of the last ~50 actions (inferred).
- **Server validation for every placement** (community, 2024; inferred details):
  1. The request carries only integers: `blockId, x, y, z, rot, colorIndex`. Never accept a CFrame,
     Size or Instance from the client ([security](../fundamentals/security-and-anti-exploit.md)).
  2. Rate limit (token bucket), build phase active, player owns or is allowed on this plot.
  3. The block is in the server catalog and the player owns enough of it.
  4. Every cell of the block's footprint is inside the plot bounds and empty in a **server-side
     occupancy grid**, a map keyed by packed cell index. This is exact and cheap.
     `GetPartBoundsInBox` uses bounding boxes and gives false positives on meshes and
     surface-touching parts (community, 2024–2026).
  5. Under the per-player block cap. Only then does the server create the part, sized from the
     catalog.

### Physics tests

- Keep builds **anchored while building**. On launch, the server welds neighbours
  (`WeldConstraint` between adjacent cells), unanchors, and runs the test (inferred).
- **Mechanisms from a small set:** `HingeConstraint` (`ActuatorType = Motor` or `Servo`), a
  thruster via `VectorForce` or `LinearVelocity`, a `VehicleSeat` for steering. Cap them per build,
  e.g. ≤ 20 motors and ≤ 20 thrusters (inferred).
- Give the builder network ownership of their launched build, `SetNetworkOwner(player)`, so it's
  smooth for them. But pay rewards from **server-observed progress** (stage gates crossed, distance
  from the start), never from client reports ([racing](racing-driving.md) has the
  checkpoint method) (official ownership model; inferred).
- Partial credit: pay per stage or distance band, so a boat that sinks halfway still earns
  (inferred).
- Breakable builds: destroy welds whose blocks take damage above a threshold. It's satisfying, and
  it's the hook for explosives and hazards (inferred).

### Saving builds compactly

- DataStore values max out at 4,194,304 characters per key, with 4 MB/min write throughput per key
  (official, 2026-10). Saved strings must be valid UTF-8 ([player data](../patterns/player-data.md)).
- **One integer per block:** blockId 10 bits, x/y/z 8 bits each (a 256-cell plot), rot 5 bits,
  colour index 6 bits = 45 bits, under the 2^53 exact-integer limit of a Luau number. Save as a JSON
  array of numbers (inferred).
  - That is ~15 characters per block. A 2,000-block build is ~30 KB, and one key holds ~250K blocks
    (inferred arithmetic).
  - A palette index instead of RGB keeps colours to 6 bits (inferred).
- One key per slot (`build_<userId>_<slot>`) with a `version` field for migration. Keep the
  player profile small and load builds on demand (inferred; see
  [player data](../patterns/player-data.md)).
- Save on an explicit Save button and on leave, with `UpdateAsync`. Show "Saved ✓" with the time;
  players need to see it (inferred).
- `SerializationService` (`SerializeInstancesAsync`) carries the PluginOrOpenCloud capability, so
  don't plan on it in game servers (official reference; inferred consequence).
- Alternative: tie the world to a private server, as Steve the Craftsman does (official game
  description, 2026-10).

### Sharing creations

- **In the server:** a showcase moment at launch (camera on the build, name banner), a plot
  visitor mode, and a server vote for "build of the round" (inferred).
- **Build codes:** export a slot as a short code that others can load. These are still assembled
  3D assets, but filter any text inside (inferred).
- **To the player's inventory:** `AssetService` has in-experience creation. A server call opens a
  platform dialog. Packages can't contain scripts or private assets (official, 2026-10). The
  reference currently lists `PromptCreatePlatformContentAsync`, while the guide names
  `PromptCreateAssetAsync`. Check the reference before coding (unverified which is current).

### Moderation of user creations

- **The 16+ rule.** Free-form user creation is limited to players 16 and older (official, 2026-10).
  It covers:
  - freehand drawing, painting, writing or spray paint on any surface;
  - blank pixel canvases or grids where players can mark any cell;
  - per-round drawings others can see.

  **Exempt:** creations "players assemble with 3D assets, such as building a house", and anything
  that passes Roblox moderation first (official, 2026-10). See
  [metadata](../fundamentals/metadata-thumbnails-icons.md).
- So: block building from your catalog keeps all ages. A paint brush, a free-colour pixel wall, a
  flat "pixel art" grid of 1-stud tiles, or freehand signs would gate the game to 16+ (inferred
  from the official rule).
- Sign text goes through `TextService:FilterStringAsync`, displayed with
  `GetNonChatStringForBroadcastAsync` (official). Cap the length, and show nothing if filtering
  fails (inferred).
- Don't accept arbitrary decal, mesh or audio asset IDs from players (inferred).
- Blocks can still spell or draw offensive shapes. Add a report button on builds, a server-side
  "hide build" after N distinct reports, and an admin removal tool with logs (inferred).

### Griefing

- **Plot permissions** on the server: owner plus an allow-list of friends. Every place, delete or
  paint checks it (inferred).
- **Separate collision.** Register groups with `PhysicsService:RegisterCollisionGroup` and set
  `BasePart.CollisionGroup` so players and builds can't push other plots during the build phase
  (official APIs; use inferred).
- **PvP is opt-in.** Plane Crazy offers PvP and peaceful modes (official game description). Build a
  Boat hands out TNT barrels as a group perk (official game description). Explosives should hurt
  only opted-in players or your own build (inferred).
- **Lag machines:** cap blocks per player (start at ~1,000), mechanisms per build, and unanchored
  assemblies per server. Delete parts below a kill plane, and clear builds when the owner leaves
  (inferred).
- **Restrict risky tools to private servers.** Car Crushers 2 gives build tools only in private
  servers (official game description, 2026-10).

## Session shape

- **Typical session:** Build A Boat For Treasure averages 18.15 minutes (community: Rolimons, read
  2026-10-24). Its 7-player servers run near full (community: Rolimons and Bloxodes server
  lists; unverified; data: max 7).
- **First 60 s:** spawn on your plot with a few blocks and a seat already placed (community guide,
  2026). Place 5 blocks in the first minute, and launch within 2 minutes. Start from an editable
  starter build, not an empty plot (inferred).
- **First 10 min:** 2–3 launches, first gold, first chest, first new block type (inferred).
- **Day 7:** a saved build in each slot, chasing the next course section or a rare block
  (inferred).

## Social hooks

- Team plots where friends build one machine together (inferred).
- A launch is a spectacle: everyone watches a build race, sink or explode. Make it clip-worthy
  with a camera cut and slow-down ([social and virality](../fundamentals/social-and-virality.md))
  (inferred).
- Private servers for free-build groups ([private servers](../patterns/private-servers.md)).
- Build votes and showcases (inferred).

## Monetization that works here

- **Currency multiplier:** Build a Boat sells Gold Multiplier for 500 R$ (community: Rolimons,
  2026-10-24).
- **Cosmetic characters:** 250 R$ each (community: Rolimons, 2026-10-24).
- **Save slots:** Build a Boat's Saving Slot C, D and E passes are offsale now (community:
  Rolimons, 2026-10-24). Slots are a natural pass. Keep 2–3 free so nobody loses a build to a
  paywall (inferred).
- **Group perks:** +25% gold for members (official game description, 2026-10).
- **Block packs and themed sets** (inferred). If chests can be bought with Robux, even through
  currency, disclose paid random items ([monetization](../fundamentals/monetization.md)).
- **Private servers for builders**, a recurring sale in Steve the Craftsman's and Car Crushers 2's
  models (official game descriptions; inferred).

## Common failure modes

- **A blank plot and no goal.** "Build anything" games have short sessions without a test or
  target (inferred).
- **Fiddly placement on phones** (inferred).
- **Lost or corrupted builds:** no versioning, saves only on leave, keys over 4 MB (inferred;
  official limits).
- **Lag and crashes** from unanchored part counts, and welded builds that explode on launch
  (inferred).
- **Griefing** through shared collision, explosives or unprotected plots (inferred).
- **Accidental 16+ gating** from a paint tool or pixel board (official rule).
- **Client-authoritative placement:** exploiters spawn parts anywhere (official threat model).

## Saturation & opportunity

Single snapshot, so no growth claims.

- Sandbox subgenre: 13 games, 28K players. Build A Boat For Treasure holds 38% of it at 10.7K
  (data, 2026-10-22).
- The leaders are old: Build A Boat (2016, 5.24B visits) and Plane Crazy (2014). Steve the
  Craftsman (47 days, 8.0K, 71% likes) is the only new sandbox of size (data, 2026-10-22).
- Build A Boat's all-time peak was 89,627 on 2021-04-02 (community: Rolimons), so the format has
  faded from its peak rather than grown (inferred).
- The `building` theme reads "crowded" (19 games, 46K, 2.4K per game, median 1.5K; data,
  2026-10-22). But it is keyword-matched on "Build", so it mixes in "Build a ___ Empire" tycoons:
  Build An Ant Empire 6.7K, Build a Phone Empire 6.7K, Build a PC 5.7K (data, 2026-10-22). True
  sandboxes are fewer (inferred).
- Opening (inferred): a fresh physics-test theme (a course, a launch distance, a delivery, a
  derby), and a build-plus-idle hybrid like Build a Car's offline driving. Both suit a solo dev with
  no animator, because nothing needs character animation.

## Scope for a solo dev

**MVP:** one plot per player or team, 20–30 catalog blocks (cubes, wedges, seat, wheel, motor,
thruster, a few decor pieces), 1-stud grid, 24 rotations, a 32-colour palette, place, delete and
undo, server validation, one physics test with distance rewards, 3 save slots, part caps.

| Week | Build |
|---|---|
| 1 | Grid placement, ghost preview, server occupancy grid and validation, rate limits |
| 2 | Rotate, delete, undo, palette; mobile build controls; anchored builds with no cross-plot collision |
| 3 | Launch: weld, unanchor, test course, server-observed distance rewards, partial credit |
| 4 | Save and load (integer encoding, slot keys, versioning), block shop or chest |
| 5 | Mechanisms (motor hinge, thruster, seat steering) with caps; stability tuning |
| 6 | Anti-grief, perf test with full servers on a low-end phone, FTE starter build, playtest |

- **The hardest parts** are touch-friendly 3D placement and keeping welded player builds stable. No
  animation is needed, which suits the user (inferred).
- **Cut:** free scale and stretch tools, paint brushes, logic wiring, copy-paste and multi-select
  (later), build codes, voting, PvP, inventory publishing.

## Top examples

- Build A Boat For Treasure: team plots, launch down a staged course for gold, chests unlock
  blocks; 10.7K, 7 per server (data, 2026-10-22).
- Plane Crazy: block-built planes, cars, rockets and mechs, with PvP or peaceful mode; 3.6K (data,
  2026-10-22).
- Steve the Craftsman: voxel world saved per private server; 8.0K at 47 days (data, 2026-10-22).
- Car Crushers 2: physics destruction, build tools only in private servers; 1.4K (data,
  2026-10-22).
- Build a Car: build a vehicle that earns while you're offline; 435 (data, 2026-10-22).

## Build checklist for agents

### Do

- Accept only integer placement requests (`blockId, x, y, z, rot, colorIndex`). Validate the
  catalog, ownership, plot permission, bounds, occupancy, cap and rate on the server, then create
  the part there.
- Keep a server-side occupancy grid. Don't rely on physics queries for overlap.
- Keep builds anchored until launch, then weld and unanchor on the server.
- Pay test rewards from server-observed progress.
- Save each build slot as a versioned array of packed integers under its own key, with a visible
  save confirmation.
- Cap blocks, mechanisms and unanchored assemblies, and test a full server on a low-end phone.
- Use collision groups so players can't touch other plots, and make PvP and explosives opt-in.
- Filter all player text with `TextService` before others see it.
- Start new players from an editable starter build.

### Don't

- Don't accept CFrames, sizes, Instances or asset IDs for placement from the client.
- Don't ship freehand paint, pixel canvases or free-text signs unless the game is meant to be 16+.
- Don't save raw CFrames or RGB values per block.
- Don't let explosives or physics hit other players' builds without consent.
- Don't put the only save slots behind a paywall.
- Don't plan on `SerializationService` from game-server scripts.

## Sources

1. https://create.roblox.com/docs/production/promotion/content-maturity — free-form user creation is 16+, 3D-asset building exempt
2. https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits — 4,194,304-character values, per-key throughput, storage formula
3. https://create.roblox.com/docs/reference/engine/classes/SerializationService — SerializeInstancesAsync, PluginOrOpenCloud capability
4. https://create.roblox.com/docs/reference/engine/classes/AssetService — PromptCreatePlatformContentAsync listing
5. https://create.roblox.com/docs/projects/assets/in-experience-asset-creation — in-game asset creation, no scripts or private assets (search snippet; PromptCreateAssetAsync naming)
6. https://create.roblox.com/docs/physics/network-ownership — ownership model, exploit risk
7. https://devforum.roblox.com/t/block-placement-system/2994417 — validate placements on the server (2024)
8. https://devforum.roblox.com/t/inaccurate-spatial-queries-on-meshes/4529811 — GetPartBoundsInBox bounding-box false positives
9. https://devforum.roblox.com/t/placement-system-collides-with-objects-touching-the-surface-of-other-objects/3030730 — surface-contact overlap issue (2024)
10. https://devforum.roblox.com/t/save-models-in-datastores/33435 — grid cell index instead of coordinates
11. https://devforum.roblox.com/t/having-a-problem-with-datastore-key-size-limit/2386894 — 4 MB key limit, chunking
12. https://www.rolimons.com/game/537413528 — Build A Boat passes and prices, offsale save slots, peak 89,627 (2021-04-02), 18.15 min playtime (third-party tracker, read 2026-10-24)
13. https://bloxodes.com/wiki/build-a-boat-for-treasure — chests, 200-block catalog, stage badges, gold codes (fan wiki, 2026-08)
14. https://earnaldo.com/blog/build-a-boat-for-treasure-beginner-guide — spawn plot with wood blocks and a seat (guide; unverified)
15. Roblox game descriptions read via the tracker (2026-10-22): Build A Boat For Treasure, Plane Crazy, Steve the Craftsman, Build with Friends, Build a Car, Car Crushers 2
16. private/trends/latest.md and tools/trends queries — all (data, 2026-10-22) numbers

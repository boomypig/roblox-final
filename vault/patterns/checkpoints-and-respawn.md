---
title: Checkpoints and respawn
type: pattern
read-when: Building checkpoints, respawn, or stage progress.
last-researched: 2026-10-22
---

# Checkpoints and respawn

## What it is

Checkpoints are numbered parts along a course. When a living player's character touches the
next one, the server records the new stage. When the player dies or falls, they come back at
that stage within about a second. In a checkpoint obby, the stage is saved in the player's
profile. In a round-based race, it lasts only for the round.

## Why it works

- A checkpoint caps the cost of a mistake at one section, so players retry instead of
  quitting. Tower obbies remove checkpoints on purpose, and use a round timer to keep the
  stakes high (community, 2026-10; see [obby-tower](../genres/obby-tower.md)).
- "Stage 37" is a visible, savable number. It works as a progress bar, a leaderstat to show
  off, and a reason to come back (inferred).
- Respawn speed is felt on every death. In a hard obby a player may die hundreds of times, so a
  5 s respawn spends minutes of their session on a loading spinner (inferred).

## Genres that use it

[Classic and difficulty-chart obbies](../genres/obby-classic.md), [escape obbies](../genres/obby-escape.md),
[round-based races](../genres/round-based-races-and-survival.md) (per-round checkpoints),
[racing](../genres/racing-driving.md) (lap gates), [story games](../genres/story-games.md) (chapter
saves). Related loop: [round-system](round-system.md).

## Design rules

### Touch rules: which checkpoint counts

| Rule | Accepts | Pros | Cons |
|---|---|---|---|
| Next stage only | `stage == current + 1` | A teleport to the end gains nothing; easiest to reason about | One missed touch (lag, a fast jump past the pad) blocks all later checkpoints until the player goes back |
| Any higher stage | `stage > current` | Never stuck | One teleport to the last checkpoint completes the course |
| Window (default) | `current + 1 .. current + 2`, plus a minimum time and a distance check | Survives one missed touch; a teleport gains at most 2 stages, and the time check catches chains | Slightly more code |

Rules for every option (inferred unless tagged):
- Touching your current or an earlier checkpoint does nothing. That check is the debounce: no
  global `debounce` boolean, which would block every other player for its duration.
- Make checkpoints hard to miss: a full-width pad plus a tall invisible touch volume
  (`CanCollide = false`, `Transparency = 1`, `CanTouch = true`). `CanCollide = false` parts
  still fire `Touched` (official, 2026-10).
- Don't anchor-to-anchor test: two anchored parts never fire `Touched` on each other (official,
  2026-10). Touches come from characters, which are unanchored.
- A difficulty-chart obby lets players go back to any stage `<= MaxStage` through a stage
  selector, without lowering `MaxStage`. A community checkpoint kit exposes the same choices as
  `sequential` and `CanGoBackwards` settings (community, 2025-09).

### Respawn location: two approaches

| | `Player.RespawnLocation` | Custom spawning (`CharacterAutoLoads = false`) |
|---|---|---|
| How | One `SpawnLocation` per checkpoint; set `player.RespawnLocation` when the stage changes | Server calls `LoadCharacterAsync()` itself after data loads and after each death |
| Requirement | The `SpawnLocation` is in `Workspace` with `Neutral = true` or a matching `TeamColor` (official, 2026-10) | `Players.CharacterAutoLoads = false`; no character spawns until you call it (official, 2026-10) |
| Respawn delay | `Players.RespawnTime`, default 5.0 s, only applies when `CharacterAutoLoads` is true (official, 2026-10) | Your own `task.delay` after `Humanoid.Died` |
| Risk | A new player whose `RespawnLocation` isn't set yet spawns at a random eligible `SpawnLocation`: the engine picks randomly when several are eligible (official, 2026-10), so they can land on stage 80 (inferred) | You must handle every spawn path (join, death, reset, round end) |

Default for saved obbies: **custom spawning that sets `RespawnLocation`**. Turn off
`CharacterAutoLoads`, load the profile, set `RespawnLocation` to the saved stage's
`SpawnLocation`, then call `LoadCharacterAsync()`. No random first spawn, and no flash at stage 1
(inferred).

- `LoadCharacter` is superseded by `LoadCharacterAsync`, which also clears `Backpack` and
  `PlayerGui` (official, 2026-10). Give HUDs `ResetOnSpawn = false`.
- Don't call `LoadCharacterAsync` again for a player until `CharacterAppearanceLoaded` has fired
  (official, 2026-10). Guard death handlers so one death means one reload.
- `CharacterAdded` fires before the character is parented and moved to the spawn (official event
  order, 2026-10). A `PivotTo` inside `CharacterAdded` gets overwritten by spawn placement
  (inferred), which is why a "spawned at stage 1, then snapped to my checkpoint" bug is common.
  Use `RespawnLocation` instead.
- Set `SpawnLocation.Duration = 0` on checkpoints. The default is a 10 s ForceField (official,
  2026-10), which looks noisy and blocks `TakeDamage`-based hazards.
- Rejoining at a far stage: call `player:RequestStreamAroundAsync(spawn.Position, 5)` before
  `LoadCharacterAsync` so the area is there on arrival (official teleport advice, 2026-10; use
  here inferred). See [performance-and-devices](../../.claude/skills/roblox-map/references/performance-and-devices.md).

### Respawn speed and feel

- Obby devs set `RespawnTime` to 0 for instant respawns (community, 2020-10; 2025-09). Target
  under 1 s from death to control (inferred).
- **Soft reset (fastest):** for kill bricks and falls, don't kill at all. Zero
  `AssemblyLinearVelocity` and `PivotTo` the checkpoint, with a 0.2–0.3 s screen flash on the
  client. No character reload, no appearance reload, no GUI wipe (inferred). Mark the move as
  server-initiated for the anti-teleport check (see
  [security](../../.claude/skills/roblox-code/references/security.md)).
- **Real death:** keep it for damage-based hazards and combat. Respawn after 0–1 s in obbies,
  2–5 s in competitive modes where death should cost time (inferred).
- Give a reset path that doesn't need the Roblox menu: a "Back to checkpoint" button that fires
  a rate-limited remote. The server soft-resets the player to *their own* checkpoint, so it
  can't be abused (inferred).

### Kill bricks and fall zones

- Tag hazards with CollectionService (`KillBrick`), and have one server script handle
  `CollectionService:GetTagged("KillBrick")` plus `GetInstanceAddedSignal("KillBrick")` for
  parts added later (official API, 2026-10). No script per part.
- Kill with `humanoid.Health = 0`. `Humanoid:TakeDamage()` is blocked by a ForceField, and the
  docs say to set `Health` directly to bypass it (official, 2026-10).
- Kill-brick touches arrive from the client that owns the character, so the server sees them a
  little late. If the player sees themselves pass through a hazard, detect hazard touches on the
  client for instant response and send a reset request. The player can only cheat themselves
  out of dying, which they can do anyway by owning their physics (inferred).
- `Workspace.FallenPartsDestroyHeight` parents fallen parts and their models to `nil`; it's
  clamped to ±50,000 and can only be set in Studio, not by scripts (official, 2026-10). The
  default is -500 (community, 2022-03). If spawn geometry sits below it, players die on spawn in
  a loop (community, 2022-03).
- Falling 500 studs at the default gravity of 196.2 studs/s² takes ~2.3 s, plus the respawn
  delay (inferred math). Put invisible `FallZone` parts ~20–40 studs under each section, or
  set `FallenPartsDestroyHeight` just under a single-level course. Multi-level courses need
  per-level fall zones (community, 2020-10).

### Saving stage progress

- Profile fields: `Stage` (where you respawn), `MaxStage` (best reached), optionally
  `SkippedStages` and `BestTimeMs`. Keep them in the in-memory profile (see
  [player-data](player-data.md)); autosave and leave-save cover them. No DataStore write per
  checkpoint.
- Mirror `MaxStage` to a `leaderstats` `IntValue` named `Stage` for the player list (see
  [leaderboards](leaderboards.md)). The leaderstat is display only; never read progress back
  from it.
- Per-round checkpoints in races live in the round's table and are dropped at cleanup (see
  [round-system](round-system.md)).

### Feedback on reaching a checkpoint

- The server sets a `Stage` attribute on the Player. A LocalScript listens with
  `GetAttributeChangedSignal("Stage")` and plays the effects: chime, particle burst on the pad,
  a "Stage 12" toast, progress bar update, pad turns the "reached" color. No extra remote
  (inferred).
- Recolor pads locally from the `Stage` value each time a pad streams in: local property changes
  are lost when a part streams out (official, 2026-10).
- Bigger beats every 10 stages or at a new zone: louder sound, confetti, maybe a badge
  (inferred). See [game-feel](../../.claude/skills/roblox-vfx/references/game-feel.md).

### Skip-stage purchases

- Skip-stage products can read as pay-to-win; check them against your goals file
  (`private/goals.md`, when you keep one). Never sell skips in
  competitive or timed modes, and keep skipped runs off time leaderboards and completion badges
  (inferred). See [monetization](../fundamentals/monetization.md).
- If you sell them, sell **skip tokens**: the developer product adds `SkipTokens += 1` in
  `ProcessReceipt`, deduplicated by `PurchaseId` (see [player-data](player-data.md)). Spending a
  token is a separate validated remote. The purchase never depends on the player's stage, so
  buying at the final stage or while dead can't loop or double-apply (inferred).
- A DevForum skip-stage thread reports purchases advancing 2–3 stages at once (community,
  2021-12). Other threads report players stuck in a death loop after skipping at the last
  stage (community, unverified). A token model plus a `stage < FINAL` check on spend avoids
  both (inferred).
- Using a token: `Stage += 1`, `MaxStage = math.max(MaxStage, Stage)`, `SkippedStages += 1`,
  then soft-reset to the new checkpoint.

## Implementation outline (server-authoritative)

- `workspace.Checkpoints`: `SpawnLocation`s, each with a `Stage` number attribute and the
  `Checkpoint` tag, `Neutral = true`, `Duration = 0`, `Anchored = true`.
- Hazards: any parts tagged `KillBrick` or `FallZone`.
- `Players.CharacterAutoLoads = false` (set in Studio Properties).
- Remotes: `RequestReset()`, `RequestGoToStage(stage: number)`, `UseSkipToken()`. Each runs the
  validation pipeline and a token bucket.
- Anti-teleport: the window rule, a minimum time between checkpoints, and a distance check from
  the server's `HumanoidRootPart` position to the pad. Count rejections as strikes; never
  auto-ban on one (see [security](../../.claude/skills/roblox-code/references/security.md)).

### Luau sketch: checkpoints, kill bricks, respawn (outline)

```lua
--!strict
-- ServerScriptService/Checkpoints: outline only. Remotes, skip tokens, fall zones omitted.
local CollectionService = game:GetService("CollectionService")
local Players = game:GetService("Players")
local PlayerData = require(script.Parent.PlayerData) -- get(player) -> Data? (player-data.md)

local AHEAD, MIN_GAP, SLACK, RESPAWN_DELAY = 2, 1.0, 10, 0.5
local spawns: {[number]: SpawnLocation} = {}
local lastAt: {[Player]: number} = {}

for _, cp in CollectionService:GetTagged("Checkpoint") do
	local n = cp:GetAttribute("Stage")
	if cp:IsA("SpawnLocation") and typeof(n) == "number" then spawns[n] = cp end
end

local function living(hit: BasePart): (Player?, Model?, Humanoid?)
	local char = hit:FindFirstAncestorOfClass("Model") -- accessories sit one level down
	local player = if char then Players:GetPlayerFromCharacter(char) else nil
	local hum = if char then char:FindFirstChildOfClass("Humanoid") else nil
	if not player or not char or not hum or hum.Health <= 0 then return nil, nil, nil end
	return player, char, hum
end

local function onCheckpoint(cp: SpawnLocation, stage: number, hit: BasePart)
	local player, char = living(hit)
	if not player or not char then return end
	local data = PlayerData.get(player)
	if not data or stage <= data.Stage then return end -- old or current: the debounce
	if stage > data.Stage + AHEAD then return end -- too far ahead: count a strike
	local t = os.clock()
	if t - (lastAt[player] or 0) < MIN_GAP then return end
	local root = char:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root or (root.Position - cp.Position).Magnitude > cp.Size.Magnitude / 2 + SLACK then return end
	lastAt[player] = t
	data.Stage = stage
	data.MaxStage = math.max(data.MaxStage, stage)
	player.RespawnLocation = cp
	player:SetAttribute("Stage", stage) -- client plays feedback
end

for stage, cp in spawns do
	cp.Touched:Connect(function(hit) onCheckpoint(cp, stage, hit) end)
end

local function hookKill(part: Instance)
	if not part:IsA("BasePart") then return end
	part.Touched:Connect(function(hit)
		local _, _, hum = living(hit)
		if hum then hum.Health = 0 end -- TakeDamage would be blocked by a ForceField
	end)
end
for _, p in CollectionService:GetTagged("KillBrick") do hookKill(p) end
CollectionService:GetInstanceAddedSignal("KillBrick"):Connect(hookKill)

local function spawnPlayer(player: Player)
	local data = PlayerData.get(player)
	local cp = (data and spawns[data.Stage]) or spawns[1]
	player.RespawnLocation = cp
	pcall(function() player:RequestStreamAroundAsync(cp.Position, 5) end)
	if player.Parent == Players then player:LoadCharacterAsync() end
end

Players.PlayerAdded:Connect(function(player)
	player.CharacterAdded:Connect(function(char)
		local hum = char:WaitForChild("Humanoid") :: Humanoid
		hum.Died:Once(function()
			task.wait(RESPAWN_DELAY)
			if player.Parent == Players and player.Character == char then spawnPlayer(player) end
		end)
	end)
	while player.Parent == Players and not PlayerData.get(player) do task.wait(0.2) end
	if player.Parent == Players then spawnPlayer(player) end -- data loaded (or canSave=false defaults)
end)
Players.PlayerRemoving:Connect(function(p) lastAt[p] = nil end)
```

Soft reset for `FallZone` and `RequestReset` (outline): find the root, set
`root.AssemblyLinearVelocity = Vector3.zero`, `char:PivotTo(spawns[data.Stage].CFrame +
Vector3.yAxis * 4)`, open the anti-teleport grace window.

## Common bugs and exploits

| Bug | Cause | Fix |
|---|---|---|
| New player spawns at a random stage | Many neutral `SpawnLocation`s, `RespawnLocation` not set before first spawn | `CharacterAutoLoads = false`; set `RespawnLocation`, then `LoadCharacterAsync` (official spawn rule, 2026-10) |
| Spawns at stage 1, then snaps to checkpoint | `PivotTo` in `CharacterAdded`, before spawn placement | Use `RespawnLocation` (official event order, 2026-10) |
| Other players' touches ignored | Global debounce boolean | Per-player stage comparison |
| Checkpoint ignored with a hat on | `hit.Parent` is an Accessory | `hit:FindFirstAncestorOfClass("Model")` |
| Dead body or ragdoll advances stage | No alive check | `Humanoid.Health > 0` |
| Kill brick fails right after spawn | `TakeDamage` vs the 10 s spawn ForceField | `Health = 0`; `Duration = 0` on checkpoints (official, 2026-10) |
| Stuck: later checkpoints don't register | Next-only rule plus a missed touch | Window rule; tall touch volumes |
| Stage resets on rejoin | Progress kept only in `leaderstats` | Save in the profile; leaderstats mirror it |
| Falls take seconds to register | Relying on the -500 void | Fall zones or a raised `FallenPartsDestroyHeight` (community, 2020-10) |
| Infinite death loop on spawn | Spawn below `FallenPartsDestroyHeight` | Keep all geometry above it (community, 2022-03) |
| Double respawn, lost tools | Two paths call `LoadCharacterAsync` | One spawn function; check `player.Character == char` |
| Teleport-to-end exploit | Any-higher rule, no time or distance check | Window, minimum gap, distance from server position |
| Spoofed touch from far away | Client fires `Touched` on parts it owns | Distance check against the server's root position (official, 2026-10, see security) |
| Skip purchase adds 2–3 stages, or loops at the end | Stage logic inside `ProcessReceipt`, no cap | Skip tokens; cap at final stage (community, 2021-12) |
| Pad colors reset | Local recolor lost on stream-out | Recolor from `Stage` on stream-in (official, 2026-10) |

## Checklist for agents

- [ ] Checkpoints tagged and numbered by attribute, handled by one server script.
- [ ] Touch accepted only for a living player's character, within the window rule, after the
      minimum gap, and within distance of the server's root position.
- [ ] No global debounce; per-player stage comparison.
- [ ] `CharacterAutoLoads = false`; `RespawnLocation` set before every `LoadCharacterAsync`.
- [ ] Checkpoint `SpawnLocation`s: `Neutral = true`, `Duration = 0`.
- [ ] Respawn under 1 s in obbies; soft reset for falls and kill bricks.
- [ ] Kill bricks via CollectionService, killing with `Health = 0`.
- [ ] Fall zones under every level; nothing near `FallenPartsDestroyHeight`.
- [ ] `Stage`/`MaxStage` in the profile; `leaderstats` only mirrors them.
- [ ] Feedback driven by a `Stage` attribute on the client: sound, particles, toast.
- [ ] Skip purchases (if any) grant tokens via `ProcessReceipt`; skipped runs excluded from time
      boards; none in competitive modes.
- [ ] Every remote (`RequestReset`, `RequestGoToStage`, `UseSkipToken`) validated and
      rate-limited.

## Sources

1. https://create.roblox.com/docs/reference/engine/classes/Player: `RespawnLocation` requirements, `LoadCharacterAsync` (supersedes `LoadCharacter`, clears GUI, event order), `RequestStreamAroundAsync`
2. https://create.roblox.com/docs/reference/engine/classes/Players: `RespawnTime` default 5.0 s and its `CharacterAutoLoads` dependency
3. https://create.roblox.com/docs/reference/engine/classes/SpawnLocation: random choice among eligible spawns, `Duration` default 10 s, `Neutral`
4. https://create.roblox.com/docs/reference/engine/classes/Humanoid: `TakeDamage` blocked by ForceField, set `Health` to bypass, `Died`
5. https://create.roblox.com/docs/reference/engine/classes/Workspace: `FallenPartsDestroyHeight` behavior, ±50,000 clamp, Studio-only setting
6. https://create.roblox.com/docs/reference/engine/classes/CollectionService: `GetTagged`, `GetInstanceAddedSignal`, tag replication
7. https://create.roblox.com/docs/reference/engine/classes/BasePart: `CanTouch`, non-colliding parts still fire `Touched`, anchored pairs never touch
8. https://create.roblox.com/docs/workspace/streaming/techniques: pre-fetch before moving players
9. https://devforum.roblox.com/t/obby-fallingdown-dead/808144: fall zones vs void height, multi-level courses, `RespawnTime` 0 (2020-10)
10. https://devforum.roblox.com/t/character-keeps-dying-repeatedly-even-with-all-scripts-disabled/1731558: default -500, spawn-below-void death loop (2022-03)
11. https://devforum.roblox.com/t/obby-game-checkpoints-v20/3957159: sequential and go-backwards options, instant respawn (2025-09)
12. https://devforum.roblox.com/t/skip-stage-product/1578577: skip purchases advancing multiple stages (2021-12)
13. https://towerofhell.wiki/: tower obby with no checkpoints and a round timer (fan site)

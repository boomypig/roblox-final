---
title: Round system
type: pattern
read-when: Building lobby/intermission/match state.
last-researched: 2026-10-22
---

# Round system

## What it is

One server Script owns a loop of phases: **Waiting → Intermission (+ map vote) → Loading →
Countdown → Round → Results → Cleanup → Intermission…**. The server decides every transition
and publishes the phase and its end time as attributes on a `ReplicatedStorage` folder. Each
client draws its own countdown from that end time. Clients never advance the loop.

## Why it works

- A fixed rhythm gives every player a fresh start every few minutes. Losing costs one round,
  not a session, and a new joiner is never more than one intermission from playing (inferred).
- The countdown before a round and the results screen give a stakes-and-payoff beat that free
  play lacks. Results are the natural place for rewards, XP bars and "one more round" (inferred).
- Dead time kills the loop. Every second spent waiting (results + intermission + load +
  countdown) is a second the player can leave. The user's previous loop had about 30 s of
  downtime per round (5 + 20 + load + 3), which is a third of the session if rounds last
  60 s (inferred from its settings). That likely contributed to the flat feel of that
  prototype (inferred).

## Genres that use it

[Round-based races and survival](../genres/round-based-races-and-survival.md) (disasters,
deathruns, speed races), [tower obbies](../genres/obby-tower.md) (timed tower that resets),
[party minigames](../genres/party-minigames.md), [social deduction](../genres/social-deduction.md),
[asymmetric survival](../genres/asymmetric-survival.md), [fashion voting
rounds](../genres/fashion-avatar.md), [sports](../genres/sports.md) matches,
[shooter](../genres/shooter.md) match modes.

## Design rules

### Timing reference points

| Game / source | Numbers | Tag |
|---|---|---|
| Roblox Battle Royale tutorial `GameSettings` | intermission 5 s, match 10 s, transition 5 s, minimum players 2. These are test values, not tuning. | official, 2026-10 |
| Tower of Hell | ~8 min per tower, no checkpoints in standard rounds, the timer speeds up as players finish, Pro towers add ~2 min | community fan site, 2026-10 |
| Flee the Facility | 15 s head start for survivors before the hunter is released | community, 2026-10, unverified |
| Dress to Impress | 360 s dressing phase, then runway and 1–5 star voting | community wiki, 2026-10; see case study: dress-to-impress |
| The user's previous obby race | intermission 20 s, countdown 3 s, results 5 s, 45 s finish window after the first finisher, lives per map | task brief, 2026-10 |

### Tuning ranges (inferred unless tagged)

| Phase | Range | Advice for the user's loop |
|---|---|---|
| Waiting for players | 0 s for races | Never leave a solo player staring at "Waiting (1/2)". Races and survival work solo, so start the round with 1 player. Require 2+ only for PvP or hidden roles, and then give the waiting player something to do (practice course, lobby obby). |
| Intermission | 10–15 s without a vote, 15–20 s with one | Keep 20 s only with map voting. Cut to 5 s once every player has voted. The lobby must be playable: a practice course, shop, or last round's top-3 board. |
| Loading | ≤ 3 s target | Show a "Loading <map>" phase with its own `EndsAt`, not a frozen intermission at 0. |
| Countdown | 3 s | 3-2-1-GO is right. Hold players behind a barrier, not with `WalkSpeed = 0` (exploiters own their character's physics). |
| Round length (cap) | 1.5–3 min for short races; up to ~8 min for long towers | Set the cap at about 2× the median finish time from playtests, so most players finish and stragglers don't stall everyone. |
| Finish window after first finisher | 20–45 s, or relative to the winner | A flat 45 s is too long on a 40 s map and too short on a 4 min map. Use `clamp(0.5 × winnerTime, 20, 60)`, and end at once when every participant has finished or is out. Tower of Hell speeds its timer up as players finish (community, 2026-10), the same idea. |
| Results | 4–6 s | Keep 5 s. Show placement, reward, XP gained and the next map vote in the same screen. |
| Downtime share | ≤ 25% of the cycle | Results + intermission + load + countdown ≤ ~25 s for a 90 s round. |

### Lives, elimination and losing

- In a **race**, use checkpoints plus a time cost (respawn at the last checkpoint in 1–2 s, see
  [checkpoints-and-respawn](checkpoints-and-respawn.md)) instead of lives. Lives in a race turn
  the weakest players into spectators for the rest of the round (inferred).
- Use **lives** in survival or elimination. 1–3 lives per round. When a player is out, give
  them an instant choice: spectate, or go back to the lobby practice course (inferred).
- Never make eliminated players wait out a long timer with nothing to do. Sum "seconds idle
  while out" in analytics (see [analytics](../fundamentals/analytics.md)) (inferred).

### Win conditions and ties

- **Race:** placement = server finish order. The server records `os.clock()` at the validated
  finish touch. Equal times share a placement (inferred).
- **Survival:** everyone alive at the timer wins. If all players die, the round ends at once
  with no winner, which is a valid result, not an error (inferred).
- **Last one standing:** check `aliveCount <= 1`, never `== 1`. Two players dying in the
  same frame reach 0, and Roblox's own Battle Royale tutorial only ends on exactly 1 (official
  tutorial code, 2026-10).
- **Teams:** more alive or more points wins. Equal scores are a draw, and both teams get the
  participation reward (inferred).
- **Winner by forfeit:** if a 1v1 opponent leaves, award the win at a reduced reward so alt
  accounts can't farm wins by quitting (inferred).

### Map voting

- Offer 3 maps per vote, never the map just played. One vote per player, changeable. A tie
  picks randomly among the leaders; no votes picks randomly (inferred).
- Vote with one RemoteEvent, `CastVote(mapId: string)`, run through the validation pipeline in
  [security-and-anti-exploit](../fundamentals/security-and-anti-exploit.md): rate limit, string
  type and length, `mapId` in the current options, phase is `Intermission`. Publish tallies as
  attributes, never trust a client tally.

### Late joiners and leavers

- A player who joins mid-round spawns in the lobby (it's the only `SpawnLocation`), sees the
  current phase and its end time from the attributes, and joins the next round. For races,
  optionally let them enter during the first ~10 s of the round (inferred).
- Attribute values are replicated, so a late joiner reads the current state with no extra
  remote (official, 2026-10).
- `Players.PlayerRemoving` removes the player from the round's participant set and re-checks
  the win condition. Roblox's tutorial removes players only on death, so a leaver can hang a
  round that waits for everyone (official tutorial code, 2026-10).

### Rewards per round

- Compute rewards on the server at **Results** from server state: participation, placement,
  survival, first win of the day. Write them to the in-memory profile (see
  [player-data](player-data.md)). Don't save to DataStores per round; autosave covers it.
- Gate participation rewards on real effort (reached the first checkpoint, moved > ~50 studs,
  or survived > 20 s), so AFK players don't farm (inferred).
- Only players in the participant set at round start get round rewards; late joiners get none
  (inferred).
- Global stats (wins, best times) go to ordered stores on the cadence in
  [leaderboards](leaderboards.md), not at every round end.

### Spectating

- Spectating is client-side: `workspace.CurrentCamera.CameraSubject = targetHumanoid`. The
  server publishes who is in the round (a `InRound` attribute on each Player).
- Under streaming, the spectated area may not be loaded on the spectator's client. On the
  server, call `spectator:AddReplicationFocus(targetRootPart)` while they watch, and
  `RemoveReplicationFocus` when they switch or the round ends (official, 2026-10). Each extra
  focus costs roughly as much as an extra player (see
  [performance-and-devices](../fundamentals/performance-and-devices.md)), so allow one focus
  per spectator.
- Handle a target who leaves or dies: switch to the next alive participant (inferred).

## Implementation outline (server-authoritative)

### Data model

- `ReplicatedStorage.RoundState` (Folder, created in the Rojo project) with attributes:
  `Phase` (string), `EndsAt` (number, server Unix time from `workspace:GetServerTimeNow()`),
  `RoundId` (number), `MapName` (string), `AliveCount` (number), `Vote_<mapId>` (number).
- Clients compute `EndsAt - workspace:GetServerTimeNow()` every frame. That call returns the
  client's best approximation of the server's Unix time. It's monotonic, runs at the local
  clock's rate to within 0.6%, and throws if the client isn't connected (official, 2026-10).
  Don't use `os.time()`, `tick()` or `DistributedGameTime` for shared countdowns:
  `DistributedGameTime` is not synchronized between client and server (official, 2026-10).
- The docs call `GetServerTimeNow` unsuitable for timed rewards (official, 2026-10). The server
  decides every deadline; the client only displays it.
- One-shot events (your placement, reward toast) go through a server→client RemoteEvent.
  Continuous state goes through attributes.
- Maps live in `ServerStorage.Maps`, never `ReplicatedStorage`, which downloads to every
  client at join (official, 2026-10). Each map has a `Spawns` folder of plain anchored Parts.
  Don't put `SpawnLocation`s in maps: the engine picks randomly among eligible spawns
  (official, 2026-10), so respawning lobby players could land in the active map (inferred).

### Map load and teleport

1. `template:Clone()` while unparented: nothing replicates yet.
2. Parent it in batches. Detach the clone's children, parent the empty model to `workspace`,
   then re-parent children 10–20 at a time with `task.wait()` between batches. A DevForum dev
   reports 50k+ instance maps loading "a few seconds and without lag" this way (community,
   2023-02). Keep maps anchored and built from sections under ~64 studs, which also helps
   streaming (official, 2026-10).
3. For each player, in parallel: `player:RequestStreamAroundAsync(spawn.Position, timeout)`
   with a timeout of a few seconds. It yields, and with no timeout it waits effectively forever
   (official, 2026-10). Then `character:PivotTo(spawnCFrame)`.
4. Tell the anti-teleport check the move was server-initiated (grace window, reset last valid
   position) (see [security](../fundamentals/security-and-anti-exploit.md)).
5. Never make the server wait on a client signal ("map loaded", "cutscene done"). A client
   error left a DevForum round loop hanging on `:Wait()` forever (community, 2025-09). Use
   server deadlines; clients that aren't ready simply start late.
6. Under streaming, a client that waits for a whole runtime-cloned map hangs forever (official,
   2026-10). Client scripts `WaitForChild` only what they need, with a timeout.

### Returning players to the lobby

- Either `PivotTo` a lobby spawn (fast, keeps the character), or set `player.RespawnLocation` to
  the lobby `SpawnLocation` and call `player:LoadCharacterAsync()`. `LoadCharacter` is
  superseded by `LoadCharacterAsync`, which also clears `Backpack` and `PlayerGui`. Don't call
  it again for a player until `CharacterAppearanceLoaded` has fired (official, 2026-10).
- Because of that `PlayerGui` wipe, HUD `ScreenGui`s need `ResetOnSpawn = false` (inferred).
- `RespawnLocation` works only for a `SpawnLocation` in `Workspace` with `Neutral = true` or a
  `TeamColor` matching the player (official, 2026-10).

### Cleanup checklist (runs even when the round errors)

- Disconnect every connection made for the round (`Died`, `Touched`, `PlayerRemoving`) from one
  per-round list; a Trove/Maid object works too (community).
- Destroy the map clone, round-only tools in `Backpack`/character, and temporary effects.
  `Debris:AddItem(inst, t)` is fine for effects; anything else gets destroyed explicitly.
- Remove replication foci, clear `InRound`, reset per-round attributes and the vote tallies.
- Any `task.delay` callback checks `RoundId` before acting, so round N can't touch round N+1.
- Run the round body in `pcall`/`xpcall` and call cleanup afterwards no matter what. One error
  must not leave a map in `workspace` and the loop dead.

### Luau sketch: phase loop outline

```lua
--!strict
-- ServerScriptService/RoundServer: outline only. Voting, rewards, spectate omitted.
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")
local RunService = game:GetService("RunService")

local State = ReplicatedStorage:WaitForChild("RoundState") :: Folder
local Maps = ServerStorage:WaitForChild("Maps") :: Folder
local LOBBY_CF = (workspace:WaitForChild("LobbySpawn") :: SpawnLocation).CFrame + Vector3.yAxis * 4
local CFG = {
	MinPlayers = 1, -- races work solo; use 2 for PvP (and 1 when RunService:IsStudio())
	Intermission = 15, Countdown = 3, RoundCap = 150, Results = 5,
}

type Round = {id: number, map: Model, inRound: {[Player]: boolean}, finished: {Player},
	conns: {RBXScriptConnection}, firstFinish: number?}

local now = function() return workspace:GetServerTimeNow() end
local function setPhase(phase: string, duration: number)
	State:SetAttribute("Phase", phase)
	State:SetAttribute("EndsAt", now() + duration)
end
local function waitUntil(deadline: number, done: () -> boolean)
	while now() < deadline and not done() do task.wait(0.1) end
end

local function loadMap(template: Model): Model
	local map = template:Clone()
	local parts = map:GetChildren()
	for _, c in parts do c.Parent = nil end
	map.Parent = workspace
	for i, c in parts do
		c.Parent = map
		if i % 15 == 0 then task.wait() end -- spread replication over frames
	end
	return map
end

local function placeAll(r: Round)
	local spawns = (r.map:WaitForChild("Spawns") :: Folder):GetChildren()
	local pending = 0
	for i, p in Players:GetPlayers() do
		local char = p.Character
		if not char then continue end
		r.inRound[p] = true
		p:SetAttribute("InRound", true)
		local cf = (spawns[(i - 1) % #spawns + 1] :: BasePart).CFrame + Vector3.yAxis * 3
		pending += 1
		task.spawn(function()
			pcall(function() p:RequestStreamAroundAsync(cf.Position, 4) end)
			if p.Parent == Players and p.Character == char then char:PivotTo(cf) end
			pending -= 1
		end)
	end
	waitUntil(now() + 5, function() return pending == 0 end)
end

local function remaining(r: Round): number
	local n = 0
	for p in r.inRound do if not table.find(r.finished, p) then n += 1 end end
	return n
end

local function playRound(r: Round)
	setPhase("Countdown", CFG.Countdown)
	task.wait(CFG.Countdown)
	local barrier = r.map:FindFirstChild("StartBarrier")
	if barrier then barrier:Destroy() end
	local deadline = now() + CFG.RoundCap
	setPhase("Round", CFG.RoundCap)
	-- the finish touch handler (validated, see checkpoints file) appends to r.finished and sets
	-- r.firstFinish; it also shortens the deadline: clamp(0.5 * winnerTime, 20, 60)
	table.insert(r.conns, Players.PlayerRemoving:Connect(function(p) r.inRound[p] = nil end))
	waitUntil(deadline, function() return remaining(r) == 0 end) -- done early: end now
end

local function cleanup(r: Round)
	for _, c in r.conns do c:Disconnect() end
	for p in r.inRound do
		p:SetAttribute("InRound", false)
		local char = p.Character
		if p.Parent == Players and char then char:PivotTo(LOBBY_CF) end
	end
	r.map:Destroy()
end

local roundId = 0
while true do
	setPhase("Intermission", CFG.Intermission)
	waitUntil(now() + CFG.Intermission, function() return false end) -- voting ends early
	if #Players:GetPlayers() < CFG.MinPlayers then setPhase("Waiting", 0); task.wait(1); continue end
	roundId += 1
	State:SetAttribute("RoundId", roundId)
	local maps = Maps:GetChildren()
	local template = maps[math.random(#maps)] :: Model -- replace with the vote winner
	setPhase("Loading", 3)
	local r: Round = {id = roundId, map = loadMap(template), inRound = {}, finished = {}, conns = {}}
	State:SetAttribute("MapName", template.Name)
	local ok, err = pcall(function() placeAll(r); playRound(r) end)
	if not ok then warn("round failed", err) end
	setPhase("Results", CFG.Results) -- grant rewards from r.finished here, server-side
	task.wait(CFG.Results)
	cleanup(r)
end
```

Client side: one LocalScript reads `Phase`/`EndsAt` with `GetAttributeChangedSignal` and
renders `math.max(0, EndsAt - workspace:GetServerTimeNow())` on `RenderStepped`. It never fires
anything back to drive the loop.

### Testing

- Multiplayer behavior needs Studio's local server test with 2–3 clients; a single-player test
  never meets a minimum of 2 (official tutorial, 2026-10).
- Studio MCP playtests run solo, so set `MinPlayers = 1` under `RunService:IsStudio()`, and add
  server-only debug flags (shorter intermission, forced map) in a `ServerStorage` config module
  (inferred).
- Test: leave mid-countdown, leave as the last runner, die in the same frame as the last
  opponent, join during Loading, join during Results, server error inside a round.

## Common bugs and exploits

| Bug | Cause | Fix |
|---|---|---|
| Countdown jitters or differs between players | Server fires "seconds left" every second, or clients use `os.time()` | Publish `EndsAt`; clients use `GetServerTimeNow()` (official, 2026-10) |
| Round never ends | Leaver not removed; last two die together (`== 1`); server waits on a client signal | `PlayerRemoving` updates the set; `<= 1`; server deadlines only (official tutorial gaps, 2026-10; community, 2025-09) |
| Map and loop dead after one error | No `pcall` around the round; cleanup skipped | Always run cleanup; log the error |
| Round N's handlers fire in round N+1 | Connections never disconnected; `task.delay` without a round check | Per-round connection list; check `RoundId` |
| Players fall through the map or freeze on arrival | Teleport before the area streams in | `RequestStreamAroundAsync` with a timeout before `PivotTo` (official, 2026-10) |
| Respawns land inside the active map | `SpawnLocation`s inside maps | Plain spawn Parts in maps; only the lobby has `SpawnLocation`s (official, 2026-10) |
| HUD vanishes after returning to lobby | `LoadCharacterAsync` clears `PlayerGui` | `ResetOnSpawn = false` on HUD guis (official, 2026-10) |
| Server hitch at map load | Whole large map parented in one frame | Batch parenting with `task.wait()` (community, 2023-02) |
| Exploiter wins instantly | Finish decided by a client remote, or no stage-order check | Server `Touched` plus checkpoint order and minimum time (see [checkpoints](checkpoints-and-respawn.md)) |
| Exploiter starts early | Countdown freeze done with client-owned `WalkSpeed` | Physical barrier; reject finishes faster than a plausible minimum |
| Vote stuffing | Vote remote accepts any string or repeat calls | Validate against current options, one vote per player, rate limit |
| AFK reward farming | Participation reward with no effort gate | Require progress (checkpoint 1, distance, survival time) |
| Solo player quits | `MinPlayers = 2` in a game that works solo | Start solo rounds; lobby activity while waiting |

## Checklist for agents

- [ ] One server Script owns the phase loop. Clients only display state and send intents.
- [ ] State published as attributes on `ReplicatedStorage.RoundState`: `Phase`, `EndsAt` (from
      `workspace:GetServerTimeNow()`), `RoundId`, `MapName`.
- [ ] Clients render countdowns locally; no per-second remote.
- [ ] Rounds end early when everyone has finished or is out; `aliveCount <= 1` checks.
- [ ] `PlayerRemoving` updates participants and re-checks the win condition.
- [ ] Maps in `ServerStorage`, cloned and parented in batches, spawn Parts (not
      `SpawnLocation`s) inside maps.
- [ ] `RequestStreamAroundAsync` (with timeout) before every server teleport; anti-teleport
      grace after it.
- [ ] Map vote validated on the server; ties random; last map excluded.
- [ ] Rewards computed on the server at Results, gated on effort, written to the in-memory
      profile.
- [ ] Cleanup always runs: connections, map, tools, foci, attributes.
- [ ] `LoadCharacterAsync` (not `LoadCharacter`); HUD guis have `ResetOnSpawn = false`.
- [ ] Downtime per cycle ≤ ~25% of round time; the lobby has something to do.
- [ ] Solo start works for races; Studio uses `MinPlayers = 1`.

## Sources

1. https://create.roblox.com/docs/reference/engine/classes/Workspace: `GetServerTimeNow` (Unix time, monotonic, 0.6% rate, not for timed rewards), `DistributedGameTime` not synchronized
2. https://create.roblox.com/docs/reference/engine/classes/Player: `LoadCharacterAsync` (supersedes `LoadCharacter`, clears Backpack/PlayerGui, event order), `RespawnLocation` rules, `RequestStreamAroundAsync` timeout, `AddReplicationFocus`
3. https://create.roblox.com/docs/reference/engine/classes/SpawnLocation: random choice among eligible spawns, Neutral/TeamColor, ForceField `Duration`
4. https://create.roblox.com/docs/education/battle-royale-series/coding-the-game-loop: GameSettings values, minimum-players loop, multi-client testing
5. https://create.roblox.com/docs/education/battle-royale-series/timers-and-events: timer module, MatchStart/MatchEnd BindableEvents
6. https://create.roblox.com/docs/education/battle-royale-series/ending-matches: ends only when exactly one remains; death-only removal
7. https://create.roblox.com/docs/education/battle-royale-series/cleanup-and-reset: `RespawnLocation` + reload to lobby, weapon cleanup, transition time
8. https://create.roblox.com/docs/workspace/streaming/techniques: pre-fetch before teleports, runtime-cloned maps hang under streaming, model size
9. https://create.roblox.com/docs/studio/properties: attributes replicate to clients, supported types
10. https://devforum.roblox.com/t/cloning-stuff-lags/2188639: batch parenting, 50k-instance maps in a few seconds (2023-02)
11. https://devforum.roblox.com/t/how-should-i-interrupt-my-round-service-loop/3958997: function-per-phase structure, round counter, loop hung waiting on a client (2025-09)
12. https://devforum.roblox.com/t/countdown-to-match-system/1375705: client countdown vs per-second server updates tradeoff
13. https://towerofhell.wiki/: 8-minute towers, no checkpoints, timer speeds up as players finish, Pro towers longer (fan site)
14. https://www.bluestacks.com/blog/game-guides/roblox/rl-dress-to-impress-theme-guide-outfit-ideas-en.html: 360 s dressing phase (guide, unverified)
15. https://flee-the-facility.fandom.com/wiki/Beast: 15 s survivor head start (fan wiki snippet, unverified)

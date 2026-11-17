---
title: Boss fights and raids
type: pattern
read-when: Adding bosses, world bosses, raids, dungeons, boss waves, or any co-op PvE encounter with phases, telegraphs, party scaling or shared loot.
last-researched: 2026-10-25
---

# Boss fights and raids

## What it is

A boss is a server-owned NPC run by a **state machine** (intro → phases → enrage → dead or
reset) whose attacks are **telegraphed** on clients before the server applies damage. A raid
wraps one or more bosses in a **run**: a lobby queue, a party, an instance (an arena in the
same server or a reserved server), a timer, and per-player rewards paid on success *and* partly
on failure.

Player-side combat (M1 chains, hitboxes, animation budget) is in
[battlegrounds](../genres/battlegrounds.md); move data and cooldowns in
[ability kits](ability-kits.md); hit validation in
[security](../../.claude/skills/roblox-code/references/security.md). This file covers the boss and the run.

## Why it works

- **A shared enemy makes strangers allies.** Co-op bosses give players a reason to group and a
  reason to invite friends; intentional co-play days are a ranking signal (official, 2026-10;
  see [social](../fundamentals/social-and-virality.md)).
- **Readable danger is skill expression without PvP.** A telegraph that can be dodged turns
  "stats vs stats" into play, and makes a win feel earned (inferred).
- **Bosses are appointments.** A respawn timer or an hourly spawn gives a reason to be online at
  a time (inferred; Blox Fruits shows each boss's respawn timer at its spawn, community wiki
  2026-10; Steal an Egg runs Rift bosses every 30 min, community 2026-10).
- **Raids pay what solo play can't.** Blox Fruits' raids pay Fragments, the currency that
  awakens fruits; awakening every fruit takes 167,800 (community, wiki 2026-10). A separate
  currency keeps raids relevant after power creep (inferred).

## Genres that use it

[Anime RPG](../genres/anime-rpg.md) (island bosses, raids, dungeons),
[gacha raid](../genres/gacha-raid.md) (boss rushes, tower floors),
[tower defense](../genres/tower-defense.md) (boss waves),
[survival](../genres/survival.md) (night raids), [simulator](../genres/simulator.md) (world
bosses), [steal-a-x](../genres/steal-a-x.md) (timed event bosses),
[server events](server-events-admin-abuse.md) (admin-spawned bosses).

## Design rules

### Reference numbers (community wikis, read 2026-10-24/25)

| Game | Shape | Numbers |
|---|---|---|
| Blox Fruits raid | 5 islands in order, boss on the last; up to 4 players; entry chip 100,000 money or a fruit | Regular enemies 7,200–13,500 HP, "tanky" variants 18,500–33,750, raid boss 155,500 (Second Sea). Win: 300 + 4.5 × seconds left Fragments, capped at 1,000. Time out: 90 per island cleared. Dying: 0, and dead players can't rejoin. Idling alive on island 1 until time-out: 90 |
| Vanguards boss event | 30 waves, boss every 10th; solo or 4; weekly rotation; traits disabled | 200–250 gems per run; 2% boss unit drop, pity at 75 runs |
| Tower Defense Simulator | Party enemy HP scaling | +15% duo, +25% trio, +40% quad |
| Sailor Piece | Drop eligibility | ≥ 10% of boss HP dealt to qualify (guide site 2026, unverified) |
| Dig | Drop eligibility and despawn | 5–10% of damage; despawns after 30 min if not killed (guide site 2026, unverified) |

### Boss state machine

`Spawning → Intro → Phase1 → Transition → Phase2 (→ Phase3) → Enrage → Dead`, plus `Reset`
from any combat state.

- **Intro 2–3 s, invulnerable,** with the name card and health bar. Gives late players time to
  arrive (inferred).
- **Phases at HP thresholds** (66% / 33%, or 50% for two phases). Each transition: 1–2 s
  invulnerable, a visual change, one new attack. Never more than 2 new mechanics per phase
  (inferred).
- **Enrage** at the fight timer (e.g. 5 min for a world boss, the raid timer for a raid):
  faster attacks and +50% damage, so a fight can't stall forever (inferred).
- **Reset** when no living participant is inside the arena for 10–15 s, or the boss is pulled
  past its leash radius: full heal, back to spawn, contributions cleared (inferred).
- **Attack choice:** weighted random among attacks off cooldown for the current phase, never
  the same attack twice in a row, with a 0.5–1.5 s gap between attacks (inferred).

### Telegraphs

- Every damaging attack shows a warning first: ground decal or translucent part for AoE, a line
  for charges and beams, a glow on the boss for melee (inferred).
- **Warning time: 0.8–1.5 s** on normal difficulty, never under ~0.6 s on hard. Phone players
  react slower and see less of the screen (inferred; see [audience](../fundamentals/audience.md)).
- **The warning shows the true hit shape.** The server checks damage with the same shape and size
  the client drew; a lying telegraph reads as a bug (inferred).
- Pair each telegraph with a sound cue for players looking elsewhere
  ([game feel](../../.claude/skills/roblox-vfx/references/game-feel.md)).
- Sync by time, not by message arrival: the server sends `startsAt` from
  `workspace:GetServerTimeNow()`; the client draws until that moment (official API; method
  inferred, as in [round system](round-system.md)).

### Co-op scaling

- **Scale HP, not damage.** Damage per hit stays fixed so a solo player's dodging skill is
  still what matters (inferred).
- Action-combat default (each player adds roughly full DPS): HP multiplier ≈ `n ^ 0.85`
  → 1.0 / 1.8 / 2.5 / 3.2 for 1–4 players (inferred; tune with kill-time telemetry).
  TDS's much flatter +15/25/40% suits TD, where co-op splits one economy (community, above).
- Lock the multiplier at fight start. A player who joins mid-fight adds their share of HP; a
  player who leaves doesn't remove HP but the enrage timer doesn't move (inferred).
- Big world bosses (whole server): cap the multiplier (e.g. at 8 players' worth), or a full
  server melts it in seconds and nobody sees phase 2 (inferred).
- Target kill time: 60–120 s for an island/world boss, 3–6 min for a raid boss (inferred).

### Damage contribution and loot

- **Every eligible player gets their own roll.** Never one shared drop that players race for
  (inferred; [gacha raid](../genres/gacha-raid.md) co-op rules).
- **Eligibility:** dealt ≥ 25% of a fair share (`maxHP / participants × 0.25`) **or** was in
  the arena for ≥ 60% of the fight and landed ≥ 5 hits. A flat 10% bar (Sailor Piece, above)
  excludes the weaker half of a 12-player world boss (inferred).
- Count only damage that passed server validation. Track healing and damage taken for support
  roles if they exist (inferred).
- **Drops go straight to inventory** on the server, never as a world item others can grab
  (inferred).
- Rare boss-exclusive drops get a **pity counter** per player per boss (Vanguards: 2%, pity 75,
  community above; rules in [rarity tiers](rarity-tiers-and-eggs.md)).
- **Last hit** earns a cosmetic or title at most, never better loot; otherwise players hold
  damage for the last hit (inferred).
- Show a results card: damage %, rank, drops. Kill feed: "X dealt the final blow" (inferred).

### Raids: lobby, run, rewards

- **Queue pad** for a party of up to 4: a 20 s countdown that starts with the first player and
  skips to 5 s when full; a party leader can start early (inferred). Parties from
  `Player.PartyId` join together ([social](../fundamentals/social-and-virality.md)).
- **Where the run lives:**
  1. **MVP:** an arena in the same server, placed far from the map, streamed in with
     `Player:RequestStreamAroundAsync` before the teleport ([round system](round-system.md)).
  2. **Later:** a raid place in the same universe, reached with a reserved server (below).
- **Timer:** 8–15 min per raid with the time left visible; rooms or waves in order; the boss
  last (inferred; Blox Fruits uses a run timer, community).
- **Rewards scale with progress and speed** (Blox Fruits: base + per-second bonus, capped;
  time-out pays per room cleared, community). Death pays nothing in Blox Fruits; for a young
  audience, pay a reduced share to the dead if the party wins (inferred).
- **Entry cost** (soft currency or a token) limits alt farming and makes a run feel weighty.
  Never Robux-only entry (inferred).
- **Difficulty tiers** (Normal / Hard / Nightmare) are the cheap way to add content: same boss,
  new modifiers (inferred; [tower defense](../genres/tower-defense.md) modifier modes).

## Implementation outline (server-authoritative)

### The boss

- **Model:** anchored root moved by CFrame on the server (cheapest, no physics fights), or a
  `Humanoid` model with the root's network owner set to the server via `BasePart:SetNetworkOwner(nil)`
  so no client can move it (official, network ownership).
- **Health** in attributes `Health` and `MaxHealth` on the model, so every client's bar reads
  them with no remote (official: attributes replicate; method inferred).
- **Attacks as data** in a ModuleScript:
  `{Id, Phase, Weight, Cooldown, Telegraph = 1.0, Shape = "Circle", Size = 18, Damage = 40,
  Offset}`. Same module drives the client's telegraph drawing.
- **Damage to players:** at `startsAt`, the server runs `Workspace:GetPartBoundsInRadius` (or
  `Workspace:GetPartBoundsInBox`) with an `OverlapParams` include-list of character models and
  damages each player once (official APIs; see [battlegrounds](../genres/battlegrounds.md)).
- **Damage to the boss:** only through one server function `Boss.damage(player, amount)`
  called by the validated ability system. No remote names the boss or an amount.
- **VFX:** clients draw telegraphs, projectiles and impacts from compact events; the server
  simulates projectiles as data (position = origin + dir × speed × t) like
  [tower defense](../genres/tower-defense.md) enemies (inferred).

### Raids in reserved servers

Facts (official, engine reference read 2026-10-25):
- `TeleportService:ReserveServerAsync(placeId)` (server only) returns an access code **and** the
  server's `PrivateServerId`. Codes stay valid indefinitely; a server starts when the code is
  first used.
- Inside, `game.PrivateServerId ~= "" and game.PrivateServerOwnerId == 0` means "reserved
  server". `PrivateServerId` is stable across server instances; `JobId` isn't.
- `TeleportService:TeleportAsync(placeId, players, options)` is server-only, takes ≤ 50 players
  per call; set `TeleportOptions.ReservedServerAccessCode` (or `ShouldReserveServer = true`,
  which conflicts with an access code). Teleports fail sometimes: wrap in `pcall`, retry, and
  handle `TeleportService.TeleportInitFailed`, which hands back retry options.
- `TeleportOptions:SetTeleportData` is visible to the client and unencrypted: never put rewards
  or authority in it. Teleports don't work in Studio playtests.
- Set **Access Control for Places** to "Secure within universe only" when the raid place should
  only be reachable by server teleports.

Flow (inferred):
1. Lobby: reserve → write the roster `{userIds, difficulty, expires}` to a
   `MemoryStoreService:GetHashMap("Raids")` entry keyed by `PrivateServerId` (expiry 30 min) →
   `TeleportAsync` the party with the access code.
2. Raid server: on start, read its roster by `game.PrivateServerId`; kick anyone not on it.
   Teleport data may carry display hints only.
3. Grant rewards in the raid server's profile session at the kill, save, then teleport everyone
   back to the lobby place. Session locking makes the hop safe
   ([player data](player-data.md)).
4. A disconnect mid-raid can rejoin while the roster entry lives (same access code) unless dead.

### Luau sketch

```lua
--!strict
-- ServerScriptService/Boss: OUTLINE. One boss, phases, telegraphs, contributions. Loot omitted.
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Attacks = require(script.Parent.BossAttacks) -- {{Id: string, Phase: number, Weight: number, Cooldown: number, Telegraph: number, Size: number, Damage: number}}
local Telegraph = ReplicatedStorage.Remotes.BossTelegraph :: RemoteEvent

local boss = workspace:WaitForChild("Boss") :: Model
local root = boss.PrimaryPart :: BasePart
local BASE_HP, ARENA_RADIUS, LEASH_TIME = 50_000, 120, 12
local damageBy: {[Player]: number} = {}
local lastUsed: {[string]: number} = {}

local function participants(): {Player}
	local out = {}
	for _, p in Players:GetPlayers() do
		local hrp = p.Character and p.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
		if hrp and (hrp.Position - root.Position).Magnitude <= ARENA_RADIUS then table.insert(out, p) end
	end
	return out
end

local function phase(): number
	local frac = (boss:GetAttribute("Health") :: number) / (boss:GetAttribute("MaxHealth") :: number)
	return if frac > 0.66 then 1 elseif frac > 0.33 then 2 else 3
end

local function pickAttack(prev: string?): any
	local now, pool, total = os.clock(), {}, 0
	for _, a in Attacks do
		if a.Phase <= phase() and a.Id ~= prev and now - (lastUsed[a.Id] or -math.huge) >= a.Cooldown then
			table.insert(pool, a); total += a.Weight
		end
	end
	local roll = math.random() * total
	for _, a in pool do roll -= a.Weight; if roll <= 0 then return a end end
	return nil
end

local Boss = {}
function Boss.damage(player: Player, amount: number) -- called only by the validated ability system
	if boss:GetAttribute("State") ~= "Fight" then return end -- intro/transition: invulnerable
	local hp = math.max(0, (boss:GetAttribute("Health") :: number) - amount)
	damageBy[player] = (damageBy[player] or 0) + amount
	boss:SetAttribute("Health", hp)
end

task.spawn(function()
	local n = math.max(1, #participants())
	boss:SetAttribute("MaxHealth", math.floor(BASE_HP * n ^ 0.85)) -- locked at start
	boss:SetAttribute("Health", boss:GetAttribute("MaxHealth"))
	boss:SetAttribute("State", "Intro"); task.wait(2.5)
	boss:SetAttribute("State", "Fight")
	local prev: string?, emptyFor = nil, 0
	while (boss:GetAttribute("Health") :: number) > 0 do
		if #participants() == 0 then
			emptyFor += 1
			if emptyFor >= LEASH_TIME then boss:SetAttribute("State", "Reset"); break end -- heal, clear damageBy
			task.wait(1); continue
		end
		emptyFor = 0
		local a = pickAttack(prev)
		if a then
			prev, lastUsed[a.Id] = a.Id, os.clock()
			local center = root.Position
			local startsAt = workspace:GetServerTimeNow() + a.Telegraph
			Telegraph:FireAllClients(a.Id, center, startsAt) -- clients draw the true shape until startsAt
			task.wait(a.Telegraph)
			local params = OverlapParams.new()
			params.FilterType = Enum.RaycastFilterType.Include
			params.FilterDescendantsInstances = {workspace:WaitForChild("Characters")} -- live characters folder
			local hit: {[Model]: boolean} = {}
			for _, part in workspace:GetPartBoundsInRadius(center, a.Size, params) do
				local char = part:FindFirstAncestorOfClass("Model")
				local hum = char and char:FindFirstChildOfClass("Humanoid")
				if char and hum and not hit[char] then hit[char] = true; hum:TakeDamage(a.Damage) end
			end
		end
		task.wait(0.5 + math.random()) -- gap between attacks
	end
	-- Dead: compute eligibility from damageBy, roll loot per player on the server, save
end)

return Boss
```

## Common bugs and exploits

| Bug or exploit | Fix |
|---|---|
| Players stand where the boss can't reach (ledge, inside geometry) and kill it safely | Damage counts only from inside the arena region; boss has an AoE or gap-closer for out-of-reach targets; arena has no unreachable perches (inferred) |
| Pull the boss out of its arena, or onto terrain where it sticks | Leash radius → reset; anchored CFrame movement or server-owned root (official network ownership; inferred) |
| Client moves or deletes the boss | Server owns the root (`SetNetworkOwner(nil)`) or it's anchored (official) |
| Remote spam multiplies damage | No boss remote; damage only through the validated ability system with server cooldowns ([security](../../.claude/skills/roblox-code/references/security.md)) |
| Telegraph and damage disagree (lag, different shapes) | One attack data module for both; time by `startsAt`; server checks at server positions with 1–2 studs slack (inferred) |
| Players dodge after damage already landed on the server | Accept it; keep telegraphs ≥ 0.8 s so ping rarely matters (inferred) |
| AFK leeching in co-op | Eligibility needs a damage share or presence + hits (inferred); Blox Fruits pays idlers 90 vs 300+ (community) |
| Last-hit sniping and damage holding | Last hit gets cosmetics only; loot by eligibility (inferred) |
| Shared drops cause fights and stealing | Per-player server rolls straight to inventory (inferred) |
| Fight never ends (healer stall, timer stall) | Enrage at the timer; reset when empty (inferred) |
| Leave-and-rejoin to dodge death penalties or re-enter | Roster tracks deaths; dead can't rejoin (Blox Fruits pattern, community) |
| Rewards lost when a raid server shuts down | Grant and save at the kill, before the teleport back (inferred) |
| Raid place joined directly (deep link, follow) | "Secure within universe only" + roster check by `PrivateServerId` (official setting; roster inferred) |
| Teleport data edited to claim a harder difficulty | Teleport data is client-visible: read authority from the MemoryStore roster (official warning) |
| Phones lag at phase 3 | Client VFX only, particle caps, data-simulated projectiles ([performance](../../.claude/skills/roblox-map/references/performance-and-devices.md)) |

## Checklist for agents

- [ ] Boss logic is a server state machine: Intro, phases at HP thresholds, Transition, Enrage,
      Dead, Reset (empty arena or leash).
- [ ] Attacks are data shared by server and client; every damaging attack is telegraphed
      0.8–1.5 s with the true shape and a sound.
- [ ] Telegraph timing uses `startsAt` from `workspace:GetServerTimeNow()`.
- [ ] Boss root is anchored or server-owned; HP lives in replicated attributes.
- [ ] HP scales with party size (≈ `n ^ 0.85` for action combat), locked at fight start, capped
      for world bosses.
- [ ] Damage to the boss only via the validated ability system; contributions tracked per player.
- [ ] Per-player loot rolls into inventory; eligibility by fair-share damage or presence; pity
      on rare drops; last hit cosmetic only.
- [ ] Raids: party queue, visible timer, rewards scaled by progress and speed, partial pay on
      failure, entry cost in soft currency.
- [ ] Reserved-server raids: roster in MemoryStore keyed by `PrivateServerId`, secure place
      access, `pcall` + retry teleports, rewards saved before returning.
- [ ] Playtested with 1 and 4 clients in Studio; telegraphs readable on a phone.

## Sources

1. https://blox-fruits.fandom.com/wiki/Raids — 5 islands, enemy and boss HP, entry cost, Fragment formula and cap, time-out and death rules, no rejoin after death, idle payout (wiki API, read 2026-10-25)
2. https://blox-fruits.fandom.com/wiki/Bosses — respawn timer at the spawn, hourly Awakened Bosses (wiki API, read 2026-10-25)
3. https://animevanguards.fandom.com/wiki/Boss_Events — 30 waves, boss every 10, traits disabled, 2% drop with 75-run pity (via [gacha raid](../genres/gacha-raid.md))
4. https://tds.fandom.com/wiki/Fallen_Mode — party HP scaling 15/25/40% (via [tower defense](../genres/tower-defense.md))
5. https://allthings.how/every-sailor-piece-boss-spawn-locations-drop-tables-and-how-to-farm-them/ — 10% HP drop eligibility (search snippet, unverified)
6. https://deltiasgaming.com/?p=277469 — Dig boss 5–10% eligibility, 30-min despawn (search snippet, unverified)
7. https://create.roblox.com/docs/reference/engine/classes/TeleportService — ReserveServerAsync, reserved-server check, TeleportAsync 50-player limit, conflicting options, TeleportInitFailed, Studio limitation
8. https://create.roblox.com/docs/projects/teleport — retries, SetTeleportData is client-visible, Access Control for Places
9. https://create.roblox.com/docs/reference/engine/classes/DataModel — PrivateServerId vs JobId, PrivateServerOwnerId 0 for reserved servers
10. https://create.roblox.com/docs/physics/network-ownership — SetNetworkOwner(nil) for server-owned NPCs
11. https://create.roblox.com/docs/reference/engine/classes/WorldRoot — GetPartBoundsInRadius / GetPartBoundsInBox
12. https://create.roblox.com/docs/reference/engine/classes/Workspace — GetServerTimeNow
13. https://create.roblox.com/docs/cloud-services/memory-stores — hash maps, expiration (limits in [player data](player-data.md))
14. https://create.roblox.com/docs/discovery — intentional co-play days signal

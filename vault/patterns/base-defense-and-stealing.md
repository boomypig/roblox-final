---
title: Base defense and stealing
type: pattern
read-when: Adding bases that can be raided, locks, or stealing.
last-researched: 2026-10-22
---

# Base defense and stealing

## What it is

Each player in a small server owns a plot that holds items earning passive income. Other
players can walk in, pick up one item and carry it home, slowed down. The owner defends with a
timed lock, traps and knockback gear. A hit on the carrier sends the item back. The steal
commits only when the carrier reaches their own plot. This is the core of the
[steal-a-x genre](../genres/steal-a-x.md) (Steal a Brainrot (case study: steal-a-brainrot),
Steal An Egg (case study: steal-an-egg)).

## Why it works

- **Loss aversion makes idle income tense.** A tycoon base is just a number. A base someone
  can rob is something you guard, so players stay near it, re-lock it and come back to check on
  it (inferred).
- **Every steal is a chase.** The carrier is slow and visible. The owner gets an alarm and has
  a few seconds to catch them, and both players remember how it ended (inferred).
- **Underdogs can win.** A new player can grab one rare item from a rich base during an
  unlock window, which is a story worth telling a friend (inferred).
- **Built-in clips.** A last-second grab as the lock runs out, a trap catching the thief, a
  fling that sends the item home: short and readable with no context, which suits Moments and
  short video (inferred; Moments is 16+, see [retention](../fundamentals/retention.md)).
- **The flip side:** losing your best item to a stranger is the strongest rage-quit trigger
  in the genre. Every rule below either keeps that tension or limits the damage (inferred).

## Genres that use it

[Steal-a-x](../genres/steal-a-x.md) (core), [tycoon](../genres/tycoon.md) raids,
[idle-incremental](../genres/idle-incremental.md) with PvP, and
[pet-egg collection](../genres/pet-egg-collection.md) variants where eggs are carried home.
Pairs with [rebirth](rebirth-prestige.md) (lock time and floors per rebirth),
[trading](trading.md), [inventory](inventory.md) and
[server events](server-events-admin-abuse.md) (luck boosts, admin abuse).

## Design rules

### Reference numbers from live games

| Knob | Steal a Brainrot (community wiki, 2026-10) | Steal An Egg and others |
|---|---|---|
| Max players per server | 8 (data, 2026-10-22) | Steal An Egg 7, Break and Steal an Egg 7, Steal A DNA 5, Don't Steal My Eggs! 4 (data, 2026-10-22) |
| Base lock | 60 s, +10 s per rebirth (rebirth table lists +10 s at each tier), +10 s with the 499-Robux VIP pass | No player-base lock documented on the fan wiki (unverified) |
| Join protection | A "30 seconds anti-steal cooldown" after joining (community, unverified) | — |
| Carry penalty | Walk speed 34 → 20 (−41%), jump 7.2 → 4.32 (−40%), no gear while carrying | Bigger eggs are heavier and slow you more (community) |
| Owner alert | On-screen "Someone is stealing your ___" plus alarm sound, then a "stole your ___" message colored by rarity | — |
| Recovery | Any hit from the free starter Bat sends a carried item back to its slot | — |
| Traps | Freeze a thief 7 s, max 5 per player (placed + held) | Bear trap: 7 s, max 3, triggers only on egg carriers, can't be placed in the safe zone |
| Turret | Arms after 5 s, shoots players in range for up to 60 s, can be destroyed | — |
| Capacity | 10 slots on floor 1; more floors unlock at rebirths 2 and 10 | Eggs come from guarded PvE nests that reset every 5 min, plus other players' bases |

Steal An Egg's description lists both "steal eggs from pets" (PvE nests guarded by sleeping
monsters) and "steal eggs from other players" (official game page, 2026-10). The PvE source
teaches the carry verb without a human victim.

### Plots

- One plot per server slot: `MaxPlayers` = plot count. Use 6–8 players. Every base sits a short
  run from the center, and a phone screen can show the whole contest (data for sizes, rest
  inferred).
- Assign the plot on join and free it on leave. The plot is a *view* of saved data; items live
  in the player's save, never only in the workspace (inferred; see [player data](player-data.md)).
- Line plots along both sides of one shared lane, with the item source (shop belt, nests) at the
  middle or the end. Every steal then crosses open ground where defenders and traps can reach
  it (inferred).
- A safe zone at spawn and the shop: no traps, no knockback, no carrying through it (SAE bans
  traps there, community; rest inferred).

### Carrying

- The server holds carry state: one item per thief, and one thief per item.
- The item stays in the victim's save while it's carried. Ownership moves only on delivery to
  the thief's plot (inferred).
- Carry speed is 0.55–0.65× walk speed (Steal a Brainrot uses 0.59, community). Also cut jump
  and disable gear while carrying, so the defender wins a fair chase (inferred).
- **Return home on interruption** (Steal a Brainrot's rule, community): any defensive hit,
  death, reset, leaving, or the victim leaving puts the item back in its slot at once.
  Dropping it on the ground for anyone to grab makes more clips, but adds an ownerless state
  you must save and expire. Skip ground drops in an MVP (inferred).
- Make carrying loud: show the item model above the carrier's head, put a marker on the
  owner's screen, and play the alarm (community, Steal a Brainrot).

### Locks

- Start with a 60 s lock, add +10 s per progression tier, and cap it around 120 s (SAB numbers,
  community; the cap is inferred).
- **Re-locking needs the owner at the lock button after the timer ends.** No early stacking,
  no auto-relock. The walk back to the button is the open window that makes the game work, and
  it means you can't AFK-guard a base (community behavior; rule inferred).
- Auto-lock the base for 30–60 s when its owner joins or respawns into it, so nobody gets robbed
  while still loading (SAB's ~30 s, community, unverified; range inferred).
- The lock must be enforced on the server: the steal prompt refuses while locked. A laser wall
  is only feedback, and noclip goes straight through it (inferred; see
  [security](../../.claude/skills/roblox-code/references/security.md)).
- Show the countdown above the base and on the owner's HUD, driven by a `LockedUntil` attribute
  set from `Workspace:GetServerTimeNow()`, which is synced between server and clients
  (official API; sync quality community-reported).

### Paid lock time and fairness

- A paid lock bonus must stay small and capped: at most +10–15 s, or about 20% of the base lock.
  SAB's VIP adds +10 s to a 60 s base (community). Never sell permanent locks, longer locks you
  can stack, or anything that opens or freezes *another* player's base (inferred).
- Paid power that decides who wins a steal is the genre's main reputation risk.
  - SAB sells Robux-only fling gear: Laser Gun 749, Ban Hammer 1,499, and an Admin Panel at
    7,499 Robux (community wiki, 2026-10).
  - Steal An Egg sells speed multipliers from 3 Robux (x2) up to 1,375 Robux (x4K)
    (community wiki, 2026-10, unverified).
  - Follow [monetization](../fundamentals/monetization.md): paid power is capped or has an
    earnable equivalent.
- Sell instead: income passes, base skins, extra slots, cosmetic carry effects, server luck
  boosts (shared with the whole server, so they also feel social), cheap trap refills (inferred).

### Traps and defensive gear

- Every player gets a free defensive tool from minute one (SAB's Bat, community). A defender who
  can't fight back just quits (inferred).
- Traps freeze for 5–7 s (both reference games use 7 s, community). Cap them at 3–5 per player,
  counting placed plus held. Trigger only on carriers, so traps can't be used on passers-by
  (SAE rule, community).
- Defensive hits: give full effect (knockback and item return) on carriers, and reduced or no
  effect on non-carriers outside bases. SAB's community already treats hitting a thief as
  defense, not griefing (community; rule inferred).
- Turrets and area gear get a visible arm-up time (SAB: 5 s) and a lifetime (SAB: 60 s), so
  thieves can read and dodge them (community).
- Gear cooldowns live on the server (see [ability kits](ability-kits.md)).

### Protecting new and low-level players

- **Newbie shield:** nobody can steal from a player for their first 10–15 minutes of total
  playtime, or until their first rebirth. Stealing from someone else ends the shield early.
  Show a shield icon over their base (inferred; nothing documented in the reference games).
- **Level-gap rule:** players far ahead in rebirth tier can't steal from players far below it.
  Underdogs can still steal *up* (inferred).
- **A PvE steal source,** like Steal An Egg's guarded nests or a shop belt, lets new players
  earn by stealing without victimizing anyone (inferred from SAE's design).
- **Never steal from offline players.** The base and its items leave with the owner. Theft of
  idle progress while away is a reason to quit (see [retention](../fundamentals/retention.md)).
- Optional: 1–3 vault slots that can't be stolen, unlocked through progression and never sold.
  They cap the worst-case loss (inferred).

### Griefing, leaving and rage-quit

- **Owner leaves mid-steal:** cancel and return the item. This lets a victim escape by
  leaving, which is the kind-to-kids choice. It never creates an item that exists in two saves
  (inferred).
- **Thief leaves mid-carry:** cancel and return. **Thief leaves after delivery:** the steal
  already committed and both saves were written (inferred).
- Known abuse in SAB's private servers: blocking a target to force them out, then stealing.
  The 30 s join protection only partly fixes it (community, unverified). Cancelling on owner
  leave closes it fully (inferred).
- To soften losses (inferred):
  - one item per carry;
  - an alert, plus a fair chance to recover;
  - a "revenge" marker that points to the thief's base for 60 s;
  - stolen items keep their value, so they can be stolen back.
- **Measure it:** log `item_stolen` (tier, victim's playtime) and leave-within-120 s after
  being robbed. If newly robbed players leave much faster than average, widen protection
  (inferred; see [analytics](../fundamentals/analytics.md)).

### Clip appeal

- Make the moments readable at a glance:
  - an alarm plus the stolen item's name in rarity color;
  - a lock countdown visible from across the map;
  - big but brief knockback;
  - the slowed carrier with the item held high.
- Announce rare spawns server-wide so everyone runs for them. SAB announces its rarest belt
  spawns (community, wiki "Red Carpet"). Add a rival bid: SAB lets another player buy a walking
  item for 150% of its price (community). Both make contests at a known time and place.

## Implementation outline (server-authoritative)

- **Data** (in the session-locked profile): `Items: {[uid]: ItemRecord}`,
  `Slots: {[slotIndex]: uid}`, `Rebirths`, `PlaytimeSeconds`, `ShieldBroken: boolean`.
- **Runtime only:**
  - `plots[player] = {model, zone, lockButton, lockedUntil}`;
  - `carrying[thief] = {victim, uid, startedAt, lastPos, lastT}`;
  - `beingStolen[uid] = thief`.
- **Interaction:** a `ProximityPrompt` per slot and on the lock button, handled in
  `Triggered` on the server. Re-check distance, state and rate there. The engine doesn't
  enforce `HoldDuration` or line of sight (official; see
  [security](../../.claude/skills/roblox-code/references/security.md)).
- **Plot discovery:** tag plot models `"Plot"` and find them with
  `CollectionService:GetTagged("Plot")`.
- **No delivery remote.** The server checks every 0.2 s whether the carrier's
  `HumanoidRootPart` is inside their own plot's zone.
- **Transfer = trade:** remove from the victim and add to the thief in server memory in one
  step, then save both profiles right away. Refuse if either profile can't save (see
  [trading](trading.md), [player data](player-data.md)).
- **Speed:** set `Humanoid.WalkSpeed` on the server, but trust only the displacement check.
  Clients can change their own WalkSpeed.

```lua
--!strict
-- ServerScriptService/Stealing.server.lua: OUTLINE, not drop-in
local Players = game:GetService("Players")
local Workspace = game:GetService("Workspace")
local PlayerData = require(script.Parent.PlayerData) -- get(), transferItem() saves both now

local WALK, CARRY_WALK = 24, 14 -- carry ≈ 0.6× walk
local BASE_LOCK, PER_TIER, MAX_LOCK, STEAL_RANGE = 60, 10, 120, 10
type Plot = {model: Model, zone: BasePart, lockButton: BasePart, lockedUntil: number}
type Carry = {victim: Player, uid: string, startedAt: number, lastPos: Vector3, lastT: number}
local plots: {[Player]: Plot} = {}
local carrying: {[Player]: Carry} = {}
local beingStolen: {[string]: Player} = {}

local function now(): number return Workspace:GetServerTimeNow() end
local function root(p: Player): BasePart?
	local c = p.Character
	return if c then c:FindFirstChild("HumanoidRootPart") :: BasePart? else nil
end
local function inZone(zone: BasePart, pos: Vector3): boolean
	local o, h = zone.CFrame:PointToObjectSpace(pos), zone.Size / 2
	return math.abs(o.X) <= h.X and math.abs(o.Z) <= h.Z and math.abs(o.Y) <= h.Y + 8
end
local function setSpeed(p: Player, s: number)
	local h = p.Character and p.Character:FindFirstChildOfClass("Humanoid")
	if h then h.WalkSpeed = s end
end

local function endCarry(thief: Player, delivered: boolean)
	local c = carrying[thief]
	if not c then return end
	carrying[thief], beingStolen[c.uid] = nil, nil
	setSpeed(thief, WALK)
	if delivered and c.victim.Parent == Players then
		PlayerData.transferItem(c.victim, thief, c.uid) -- atomic move + save both (trading rules)
	end -- otherwise the item never left the victim's save: just re-show it in its slot
end

-- Slot ProximityPrompt.Triggered → tryStartSteal(thief, owner, uid, slotPart)
local function tryStartSteal(thief: Player, victim: Player, uid: string, slot: BasePart)
	if thief == victim or carrying[thief] or beingStolen[uid] then return end
	local plot, r = plots[victim], root(thief)
	if not plot or not r or now() < plot.lockedUntil then return end
	if (r.Position - slot.Position).Magnitude > STEAL_RANGE then return end
	local t, v = PlayerData.get(thief), PlayerData.get(victim)
	if not (t and v) or not v.Items[uid] then return end
	if PlayerData.isShielded(victim) or PlayerData.tierGapTooBig(thief, victim) then return end
	PlayerData.breakShield(thief) -- stealing ends your own newbie shield
	carrying[thief] = {victim = victim, uid = uid, startedAt = now(), lastPos = r.Position, lastT = os.clock()}
	beingStolen[uid] = thief
	setSpeed(thief, CARRY_WALK)
	-- FireClient(victim, "BeingStolen", uid); attach a cosmetic model to the thief
end

-- Lock button ProximityPrompt.Triggered → tryLock(owner)
local function tryLock(owner: Player)
	local plot, r, d = plots[owner], root(owner), PlayerData.get(owner)
	if not (plot and r and d) or now() < plot.lockedUntil then return end -- no early stacking
	if (r.Position - plot.lockButton.Position).Magnitude > 12 then return end
	local secs = math.min(MAX_LOCK, BASE_LOCK + PER_TIER * d.Rebirths + (if d.HasVIP then 10 else 0))
	plot.lockedUntil = now() + secs
	plot.model:SetAttribute("LockedUntil", plot.lockedUntil) -- clients draw the countdown
end

task.spawn(function() -- carry watchdog: speed, delivery, liveness
	while true do
		task.wait(0.2)
		for thief, c in carrying do
			local r = root(thief)
			if not r or c.victim.Parent ~= Players then endCarry(thief, false); continue end
			local t = os.clock()
			local flat = (r.Position - c.lastPos) * Vector3.new(1, 0, 1)
			if flat.Magnitude > CARRY_WALK * (t - c.lastT) * 1.25 + 4 then
				endCarry(thief, false); continue -- teleport or speed hack: fail + strike
			end
			c.lastPos, c.lastT = r.Position, t
			local own = plots[thief]
			if own and inZone(own.zone, r.Position) then endCarry(thief, true) end
		end
	end
end)

Players.PlayerRemoving:Connect(function(p)
	endCarry(p, false)
	for thief, c in carrying do if c.victim == p then endCarry(thief, false) end end
	plots[p] = nil
end)
-- Also: Humanoid.Died / Player.CharacterRemoving → endCarry(p, false);
-- defensive hit on a carrier (server-validated) → endCarry(target, false).
```

## Common bugs and exploits

| Bug or exploit | Fix |
|---|---|
| Teleport-steal: teleport to the slot, grab, teleport home | Prompt range check on the server, displacement check while carrying, and a minimum carry time (`now() - startedAt >= pathLength / (CARRY_WALK × 1.3)`) before delivery counts (inferred) |
| Speed hack while carrying | The server sets `WalkSpeed`, but trust the 0.2 s displacement check. A violation fails the steal and adds a strike (see [security](../../.claude/skills/roblox-code/references/security.md)) |
| Noclip through the lock wall | The lock lives in server state. The prompt refuses while `now() < lockedUntil` |
| Prompt or remote spam (lock, steal, trap) | Token bucket per remote and per prompt. One active carry per thief, one thief per item |
| Dupe: the item ends up in both saves | Commit only on delivery, by an in-memory move plus an immediate save of both profiles. Refuse if either can't save |
| Stolen item lost when the victim leaves mid-carry | The item never left the victim's data. Cancel the carry on `PlayerRemoving` |
| Owner forced out, then robbed (block or kick tricks in private servers) | Cancel the steal when the owner leaves; auto-lock on join (community-reported abuse) |
| Stealing from a base that is still loading | Auto-lock on join until the profile has loaded, plus 30–60 s |
| Traps or turrets griefing spawn | No placement in the safe zone. Traps trigger only on carriers |
| Lock bypass by joining as the timer ends | Re-lock needs the owner at the button. Clients only display `LockedUntil` |
| Remote that says "I delivered" | Don't have one. The server detects delivery itself |
| Robbed players quit en masse | Newbie shield, level-gap rule, vault slots, return-on-hit. Watch the leave-after-robbed metric |

## Checklist for agents

- [ ] One plot per player, `MaxPlayers` 6–8, items saved in the profile (not the workspace).
- [ ] The carried item stays in the victim's save until delivery. Delivery is detected on the
      server and moves the item atomically, then saves both profiles.
- [ ] Carry speed about 0.6× walk, jump reduced, no gear while carrying. Any defensive hit,
      death, leave or victim-leave returns the item.
- [ ] Lock: 60 s base, +10 s per tier, cap about 120 s. Re-lock only at the button after
      expiry. Auto-lock on join. Enforced on the server, countdown from `LockedUntil` via
      `Workspace:GetServerTimeNow()`.
- [ ] Paid lock bonus ≤ about 20% of the base lock. Nothing sold opens, freezes or controls
      another player's base.
- [ ] Free defensive tool at spawn. Traps 5–7 s, 3–5 per player, carriers only, banned in
      safe zones.
- [ ] Newbie shield (10–15 min playtime or first rebirth, broken by stealing), level-gap rule,
      a PvE steal source, and no stealing from offline players.
- [ ] Server checks: prompt distance, displacement while carrying, minimum carry time, rate
      limits, one carry per thief.
- [ ] Alarm, rarity-colored alert and visible carry model, for clips and fair play.
- [ ] `item_stolen` and leave-after-robbed analytics events before launch.

## Sources

1. https://stealabrainrot.fandom.com/wiki/Base — 60 s lock, +10 s per rebirth, +10 s VIP; floors and slots (read 2026-10-22)
2. https://stealabrainrot.fandom.com/wiki/Stealing — carry speed 34→20, jump 7.2→4.32, no gear, owner alerts
3. https://stealabrainrot.fandom.com/wiki/Gears — Bat returns carried item, Trap 7 s / max 5, sentry 5 s arm and 60 s life, gear can't be used while carrying
4. https://stealabrainrot.fandom.com/wiki/Rebirth — +10 s lock bonus per rebirth tier, floor unlocks
5. https://stealabrainrot.fandom.com/wiki/Robux_Shop — VIP 499 Robux (+10 s lock), Robux fling gear and Admin Panel prices, server luck
6. https://stealabrainrot.fandom.com/wiki/Methods_Of_Stealing — 30 s anti-steal cooldown, private-server block abuse, leave-after-steal tactics
7. https://stealabrainrot.fandom.com/wiki/Red_Carpet — weighted belt spawns, rival purchase at 150%, rare-spawn announcements
8. https://stealanegg.fandom.com/wiki/Boosts — bear trap max 3, 7 s, carriers only, not in safe zone; Robux speed multipliers
9. https://stealanegg.fandom.com/wiki/Eggs — guarded nests, 5-min egg reset, heavier eggs slow the carrier
10. https://www.roblox.com/games/107778070777162 — Steal An Egg description: steal from pets and from other players
11. https://games.roblox.com/v1/games — `maxPlayers` per game via tools/trends (data, 2026-10-22)
12. https://create.roblox.com/docs/reference/engine/classes/Workspace — `GetServerTimeNow`
13. https://devforum.roblox.com/t/about-how-accurate-is-getservertimenow/3926695 — community reports on GetServerTimeNow sync accuracy
14. https://create.roblox.com/docs/reference/engine/classes/ProximityPrompt — `Triggered`, `MaxActivationDistance`, `HoldDuration`
15. https://create.roblox.com/docs/reference/engine/classes/CollectionService — `GetTagged` for plot discovery
16. https://create.roblox.com/docs/scripting/security/client-server-boundary — server-side checks for prompts and movement

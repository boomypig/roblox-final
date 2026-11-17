---
title: Ability kits
type: pattern
read-when: Adding characters, classes or power sources with 3–4 abilities: move data, cooldowns, input buffering, server hit checks, client VFX, mobile buttons, balance and telemetry.
last-researched: 2026-10-25
---

# Ability kits

## What it is

A **kit** is a character's moveset: a basic attack (M1 chain), 3–4 skills on cooldowns, and
often a meter-gated ultimate. Every move is a **data record** run by one server ability runner;
clients play animation and VFX at once, the server decides what happened.

This file is the kit layer. The combat state machine, hitbox methods, netcode choice and
animation budget are in [battlegrounds](../genres/battlegrounds.md); the remote validation
pipeline is in [security](../../.claude/skills/roblox-code/references/security.md); button layout and the
Input Action System are in [UI/UX](../../.claude/skills/roblox-ui/references/ui-ux.md). Don't repeat them; follow them.

## Why it works

- **Identity in four buttons.** A kit is a fantasy players can learn in a minute and master over
  weeks; "which character do you main" is build talk (inferred).
- **Kits are the update unit.** Battlegrounds leaders ship a character per update and sell
  Early Access to it ([battlegrounds](../genres/battlegrounds.md), community 2026-10). A new kit
  is one data record + animations + VFX, not a new system (inferred).
- **Cooldowns pace spectacle.** Big moves on 13–20 s cooldowns make each one an event; M1s fill
  the gaps (community numbers below; inferred).
- **Counterplay keeps it fair.** Every move readable (windup), every strong move answerable
  (block, dodge, counter) (inferred; see battlegrounds' readable-fights rule).

## Genres that use it

[Battlegrounds](../genres/battlegrounds.md), [anime RPG](../genres/anime-rpg.md) (power sources
with 4 moves), [asymmetric survival](../genres/asymmetric-survival.md) (killer and survivor
kits), [sports](../genres/sports.md) (styles with abilities), [shooter](../genres/shooter.md)
(utility slots), [gacha raid](../genres/gacha-raid.md) (unit skills), and
[bosses](boss-fights-and-raids.md), whose attacks use the same move data.

## Design rules

### Reference: one leader's documented kits (community, JJS wiki, read 2026-10-25)

Base kits of two starter characters in Jujutsu Shenanigans:

| Slot | Cooldown | Damage | Notes |
|---|---|---|---|
| M1 chain (shared) | 2 s downtime after 4 hits | 3+3+4+4 = 14 | From [battlegrounds](../genres/battlegrounds.md) |
| Skills 1–4 | **13–20 s** | **10–17.5** per skill | Multi-hit totals; some "unblockable", "bypasses ragdoll", "bullet" |
| Special (R) | 2 s or 15 s | 0–8 | Cancels a windup with no endlag and keeps that move off cooldown (one kit) |
| Counter | 20 s | 8.5 | 0.6 s counter window |
| Variants | Same cooldown as the base move | — | Air, hold, "use twice", interruption variants share one slot |

What the numbers show (inferred arithmetic): skills deal ~0.55–1.25 damage per second of
cooldown, and one skill ≈ one full M1 chain. Damage moves sit at the top of that band, utility
and counters at the bottom.

### Kit anatomy (inferred unless tagged)

| Slot | Job | Rule |
|---|---|---|
| M1 | Constant pressure | Shared across kits; tune once |
| Skill 1 | Reliable damage or combo starter | Shortest cooldown (10–14 s), easiest to land |
| Skill 2 | Combo extender or ranged poke | Combos only off a confirmed hit |
| Skill 3 | Mobility or defense (dash strike, counter, armor) | Every kit needs one way out |
| Skill 4 | Signature finisher | Longest cooldown (16–25 s), biggest windup, clip moment |
| Ultimate | Awakening from a meter | Meter from damage dealt, not time; see battlegrounds numbers |

- Every kit has: a gap closer or zoning tool, a defensive option, and one block-breaker
  ([battlegrounds](../genres/battlegrounds.md) block rule).
- Variants (air, hold, use-twice) add depth without new buttons. Show them as tooltip tags; JJS
  labels HOLD, USE TWICE, RAGDOLL, TARGET (community, 2026-10).
- Ship 2 kits at launch; a third only after both are fun in a 10-player playtest
  ([battlegrounds](../genres/battlegrounds.md) scope).

### Move timing and cooldowns (inferred unless tagged)

- Each move has **Startup → Active → Recovery**. Skills: startup 0.2–0.6 s, active 0.05–0.3 s,
  recovery 0.3–0.8 s. Bigger payoff, longer startup.
- **The cooldown starts when the move commits** (first active frame). A move interrupted
  during startup doesn't go on cooldown. JJS's windup-cancel keeps the move "off cooldown"
  (community, 2026-10), consistent with this rule.
- **One action at a time.** The combat state (Attacking, Stunned, Blocking, Ragdolled…) gates
  every move ([battlegrounds](../genres/battlegrounds.md)). Cooldowns are per move, not global,
  plus a 0.2–0.3 s lockout after any skill so two skills can't land on one frame.
- **Never under ~2 s cooldown on a big move**, and no move without endlag
  ([battlegrounds](../genres/battlegrounds.md) don'ts).

### Input buffering and hold inputs (inferred)

- **One-slot buffer, 0.15–0.2 s:** an input pressed during the last 0.15–0.2 s of recovery
  fires on the first free frame. The latest press replaces the earlier one. Expired inputs are
  dropped, never queued.
- Buffer on the **client**, then send the intent. The server never queues: if the request
  arrives while the player is still busy (by server clock + ~0.1 s slack for latency), it's
  dropped.
- **Hold variants:** tap vs hold splits at ~0.25 s; show a charge ring on the button so phone
  players can see the hold registering.
- **Aim on touch:** soft-lock to the nearest enemy in a 30–45° cone in front of the camera when
  no target is selected; players on phones can't aim and press at once.

### Mobile and cross-platform buttons

- One `InputAction` per slot in an `InputContext`, each with a keyboard/gamepad `KeyCode`
  binding and a `UIButton` binding to your own `ImageButton`; listen to `InputAction.Pressed` and
  `InputAction.Released` (official; setup in [UI/UX](../../.claude/skills/roblox-ui/references/ui-ux.md)).
- Four skill buttons in an arc around the jump button, 56–70 px, ≥ 8 px apart (vault UI rule,
  [UI/UX](../../.claude/skills/roblox-ui/references/ui-ux.md)). M1 is the largest button.
- **Cooldown on the button:** a radial sweep plus whole seconds when > 3 s left, a flash when
  ready. Read the end time from a server attribute (below), not a local guess.
- Grey out buttons the current state can't use (stunned, ragdolled) so a tap never "does
  nothing" without a reason (inferred).
- Show keybind labels for the current `UserInputService.PreferredInput` (official API, see UI/UX).

### Balancing (inferred unless tagged)

- **Time-to-kill target** first (e.g. 15–25 s of focused combat at equal skill), then fit damage
  to it. Set player max HP and regen once for all kits.
- **Budget per kit:** sum of (damage ÷ cooldown) across skills within ±10% of the other kits.
  Utility (stun, armor, unblockable, ragdoll bypass, range) costs damage. A move with three
  utility flags should be a low-damage move.
- **Counterplay audit per move:** what beats it (block, dodge window, range, counter)? If
  "nothing", don't ship it.
- **Tune numbers live.** Keep damage, cooldowns and hitbox sizes overridable by
  `ConfigService` keys, refreshed between fights, so a hotfix doesn't need a publish
  ([live ops](../fundamentals/live-ops-and-updates.md)).
- Never sell a kit that stays paid and stronger; Early Access ends in a free release
  ([battlegrounds](../genres/battlegrounds.md), [monetization](../fundamentals/monetization.md)).

### Telemetry

- `AnalyticsService` allows **120 + 20 × CCU requests per minute**, 3 custom fields per event and
  100 event names (official, 2026-10; see [analytics](../fundamentals/analytics.md)). Don't log
  every cast.
- **Aggregate on the server:** per move, count casts, hits and damage in memory; every 10
  minutes log one `move_stats` custom event per move used (value = hit rate %, fields MoveId,
  Character) (inferred).
- Log **every kill** with fields Character, FinishingMove, VictimCharacter; log character pick
  on select (inferred).
- Read weekly (inferred):
  - Pick rate > 2× average **and** above-average kill share → nerf candidate.
  - A move with hit rate < 20% → hitbox too small, windup too readable, or the move is
    unclear; check before buffing damage.
  - A move that's > 40% of a kit's kills → the kit is one button; spread its power.

## Implementation outline (server-authoritative)

- **Shared move data** (`ReplicatedStorage.Shared.Moves`): `{Startup, Active, Recovery,
  Cooldown, Damage, Stun, Knockback, HitboxSize: Vector3, HitboxOffset: CFrame, MaxTargets,
  Blockable, Tags}`. The client reads it for animation timing and VFX; the server for rules.
  Damage values aren't secret, but the server never reads a client copy.
- **Kits** (server): `{[character] = {moveIds…}}`; the equipped character is a server-set
  attribute. The client sends a **slot number**, never a move ID.
- **Remotes:** `UseMove(slot, aimDir)` client→server (token bucket ~10/s burst 4);
  `MoveStarted(caster, moveId, t0)` server→all clients so others play the cast. Use an
  `UnreliableRemoteEvent` for cosmetic-only bursts (official API; see battlegrounds/security).
- **Animations:** the caster's client plays its own animation at once; animations started on a
  player's own character replicate to the server and other clients, while NPC animations must
  be played on the server (official, Animator reference). Load clips once per character.
- **Cooldown UI:** the server sets `player:SetAttribute("CD1", endTime)` with
  `workspace:GetServerTimeNow()` time; the button draws `endTime - GetServerTimeNow()` (official
  API; pattern from [round system](round-system.md)).
- **Hits:** detection per [battlegrounds](../genres/battlegrounds.md) (server-detects model
  recommended to start), validation per [security](../../.claude/skills/roblox-code/references/security.md).
  One `Combat.applyHit` handles block, i-frames, damage, stun and knockback for every move.
- **VFX on the client:** spawn from templates in `ReplicatedStorage`, cap particles per player,
  scale down on low graphics quality ([performance](../../.claude/skills/roblox-map/references/performance-and-devices.md)).

```lua
--!strict
-- ServerScriptService/AbilityServer: OUTLINE. Token bucket, block/i-frames, telemetry omitted.
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Moves = require(ReplicatedStorage.Shared.Moves) -- {[string]: MoveDef}, shared data
local Kits = require(script.Parent.Kits) -- server-only: {[string]: {string}} character → move IDs
local Combat = require(script.Parent.CombatState) -- canAct, setState, isState, applyHit

type MoveDef = {Startup: number, Active: number, Recovery: number, Cooldown: number,
	HitboxSize: Vector3, HitboxOffset: CFrame, MaxTargets: number}

local UseMove = ReplicatedStorage.Remotes.UseMove :: RemoteEvent
local MoveStarted = ReplicatedStorage.Remotes.MoveStarted :: RemoteEvent
local CharactersFolder = workspace:WaitForChild("Characters") :: Folder -- live characters only
local readyAt: {[Player]: {[string]: number}} = {}

local function now(): number return workspace:GetServerTimeNow() end

UseMove.OnServerEvent:Connect(function(player: Player, slot: unknown, aim: unknown)
	if typeof(slot) ~= "number" or slot % 1 ~= 0 or slot < 1 or slot > 4 then return end
	if typeof(aim) ~= "Vector3" then return end
	local flat = (aim :: Vector3) * Vector3.new(1, 0, 1)
	if flat.Magnitude ~= flat.Magnitude or flat.Magnitude < 0.1 then return end -- NaN or zero
	local kit = Kits[player:GetAttribute("Character") :: string]
	local moveId = kit and kit[slot]
	local move: MoveDef? = if moveId then Moves[moveId] else nil
	local char = player.Character
	local root = if char then char:FindFirstChild("HumanoidRootPart") :: BasePart? else nil
	if not (move and moveId and char and root and Combat.canAct(player)) then return end
	local cds = readyAt[player] or {}
	readyAt[player] = cds
	if now() < (cds[moveId] or 0) then return end -- server cooldown; client cooldown is UX only

	local t0 = now()
	Combat.setState(player, "Attacking", t0 + move.Startup + move.Active + move.Recovery)
	MoveStarted:FireAllClients(player, moveId, t0) -- caster's client already animated; others play it
	task.delay(move.Startup, function()
		if not Combat.isState(player, "Attacking") or player.Parent ~= Players then return end -- interrupted: no cooldown
		cds[moveId] = now() + move.Cooldown
		player:SetAttribute(`CD{slot}`, cds[moveId])
		local cf = CFrame.lookAt(root.Position, root.Position + flat.Unit) * move.HitboxOffset
		local params = OverlapParams.new()
		params.FilterType = Enum.RaycastFilterType.Include
		params.FilterDescendantsInstances = {CharactersFolder}
		local hit: {[Model]: boolean}, n = {}, 0
		for _, part in workspace:GetPartBoundsInBox(cf, move.HitboxSize + Vector3.one * 1.5, params) do -- lag slack
			local victim = part:FindFirstAncestorOfClass("Model")
			if victim and victim ~= char and not hit[victim] and n < move.MaxTargets then
				hit[victim], n = true, n + 1
				Combat.applyHit(player, victim, moveId) -- block, i-frames, damage, stun, knockback
			end
		end
	end)
end)

Players.PlayerRemoving:Connect(function(p) readyAt[p] = nil end)
```

## Common bugs and exploits

| Bug or exploit | Fix |
|---|---|
| Client sends a move ID from another kit, or a damage value | Client sends a slot; server maps it from the equipped kit; damage from server data (official principle) |
| Cooldown bypass by spamming the remote | Server `readyAt` per move + token bucket; client cooldowns are UX only (official, security) |
| NaN or huge aim vector breaks hitbox math | `typeof` check, flatten, NaN and zero-length rejection, use `.Unit` (official NaN guidance) |
| Two skills land on the same frame | State gate + 0.2–0.3 s post-skill lockout (inferred) |
| Cooldown burned when the caster is stunned in windup | Start cooldown at the active frame; check state after startup (inferred) |
| Buffered inputs fire long after the press ("ghost casts") | One slot, 0.15–0.2 s expiry, latest wins (inferred) |
| Hits through walls | Line-of-sight raycast against static geometry for ranged moves ([security](../../.claude/skills/roblox-code/references/security.md)) |
| Hitbox feels stolen at high ping | Server-detects model with 1–2 studs slack, or client-detects with validation ([battlegrounds](../genres/battlegrounds.md)) |
| Others don't see the cast | Caster animates its own character (replicates); VFX via `MoveStarted` to all clients (official Animator rule) |
| NPC/boss animations invisible to players | Play NPC animations on the server (official Animator rule) |
| Cooldown UI drifts | UI reads server end time from an attribute with `GetServerTimeNow()` (official API) |
| Leaks after leaving | Clear per-player tables on `PlayerRemoving` (official, security) |
| Analytics throttled during fights | Aggregate per move; log summaries and kills only (official rate limit) |
| Balance hotfix needs a publish | Damage/cooldown overrides in `ConfigService` (official) |

## Checklist for agents

- [ ] Every move is a data record (timings, cooldown, damage, stun, knockback, hitbox, tags)
      shared by client and server.
- [ ] Kits: M1 + 3–4 skills (+ ultimate); each has a closer or zoner, a defensive option, a
      block-breaker; variants shown as tooltip tags.
- [ ] Remote takes a slot and an aim vector only; validated per the security pipeline.
- [ ] Server cooldowns per move, started at the active frame; combat state gates all moves.
- [ ] Client: instant animation and VFX, one-slot 0.15–0.2 s input buffer, soft-lock aim on
      touch, hold indicator.
- [ ] Buttons via `InputAction` + `UIButton` bindings, arc around jump, cooldown sweep from a
      server-time attribute.
- [ ] Damage-per-cooldown budget within ±10% across kits; counterplay listed per move.
- [ ] Balance numbers overridable through `ConfigService`.
- [ ] Telemetry: kills with character and finishing move, character picks, per-move hit rate
      aggregated per server.
- [ ] Two kits fun in a 10-client playtest before a third is started.

## Sources

1. https://jujutsu-shenanigans.fandom.com/wiki/Vessel and https://jujutsu-shenanigans.fandom.com/wiki/Honored_One — skill cooldowns 13–20 s, damage 10–17.5, special 2/15 s, counter 0.6 s window on 20 s, variant and flag tags (wiki API, read 2026-10-25)
2. https://jujutsu-shenanigans.fandom.com/wiki/Controls_%26_Mechanics — M1 chain numbers, tooltip tags (via [battlegrounds](../genres/battlegrounds.md))
3. https://create.roblox.com/docs/reference/engine/classes/Animator — client-started character animations replicate; NPC animations must start on the server
4. https://create.roblox.com/docs/input/input-action-system — InputContext, InputAction, InputBinding.UIButton, Pressed/Released
5. https://create.roblox.com/docs/reference/engine/classes/AnalyticsService — custom events; limits summarized in [analytics](../fundamentals/analytics.md)
6. https://create.roblox.com/docs/scripting/security/client-server-boundary — type and NaN checks, server cooldowns, hit validation
7. https://create.roblox.com/docs/reference/engine/classes/WorldRoot — GetPartBoundsInBox, OverlapParams
8. https://create.roblox.com/docs/reference/engine/classes/ConfigService — live config values
9. https://create.roblox.com/docs/reference/engine/classes/Workspace — GetServerTimeNow

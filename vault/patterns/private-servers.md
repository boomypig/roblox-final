---
title: Private servers
type: pattern
read-when: Adding or pricing private (VIP) servers, owner commands, per-server settings, reserved servers for parties or custom matches, or deciding what to disable in private servers.
last-researched: 2026-10-25
---

# Private servers

## What it is

Three kinds of non-public server, all visible to scripts through two `DataModel` properties:

| Kind | Who creates it | `game.PrivateServerId` | `game.PrivateServerOwnerId` |
|---|---|---|---|
| Public | Matchmaking | `""` | `0` |
| **Private server** (Roblox's "VIP server") | A player, free or for a monthly Robux fee, from the game page | Non-empty | Owner's `UserId` |
| **Reserved server** | Your code, `TeleportService:ReserveServerAsync` | Non-empty | `0` |

(official, engine reference read 2026-10-25)

`PrivateServerId` stays the same across every instance of one private or reserved server;
`JobId` changes. Only one instance of a private server runs at a time; a new instance starts
when someone joins an empty one (official). Per-server settings therefore key on
`PrivateServerId`.

## Why it works

- **Co-play is a ranking signal.** "Intentional co-play days" counts days users return to play
  with friends through joins, invites **or private servers** (official, 2026-10; see
  [discovery](../fundamentals/discovery-algorithm.md)).
- **Groups need a room.** Roblox lists playing with friends, classes and parties, recording or
  streaming, and gathering resources as the reasons people buy them (official, 2026-10).
- **Owner tools turn players into hosts.** Roleplay groups, sports leagues and practice-focused
  players run their own sessions and bring their friends (inferred; examples below).
- **Revenue that also pays through Roblox Plus** (below).

## Genres that use it

[Roleplay](../genres/roleplay-life-sim.md) (owner moderation), [sports](../genres/sports.md)
(leagues, scrims), [tower obby](../genres/obby-tower.md) (practice settings),
[battlegrounds](../genres/battlegrounds.md) (combo labs, build mode),
[building sandbox](../genres/building-sandbox.md) (saved worlds, free-build tools),
[farming](../genres/farming-growing.md) and [tycoon](../genres/tycoon.md) (calm play),
[horror](../genres/horror.md) (friend groups, streamers),
[steal-a-x](../genres/steal-a-x.md) (with abuse risks).

## Design rules

### Platform facts (official, read 2026-10-25)

- Enable in Creator Dashboard → Audience → Access Settings → **Allow private servers**; the game
  must be public. Choose **free** or **Requires Robux** with a monthly price.
- **Changing the price cancels every active subscription** (players get an inbox message). Pick
  the price before launch and leave it.
- Private servers can't be combined with paid access.
- Players under 13 may be unable to join depending on privacy and parental-control settings.
- Revenue: Roblox's Plus example computes earnings as a **70% share** of the server price.
- Private-server prices are regionalized automatically (official, via
  [monetization](../fundamentals/monetization.md)).
- The help center describes billing as an upfront first payment, then monthly on the same date
  (help center via search snippet, unverified: the page refused direct fetch).
- **Don't read a game's private-server setting from the public games API.** On 2026-10-25,
  `createVipServersAllowed` came back `false` for all 50 top charted games, including
  Brookhaven, which sells private servers with owner tools (data). The field likely reflects the
  anonymous caller, not the game (inferred). Check the game page's Servers tab instead.

### Roblox Plus (official, 2026-04 to 2026-10)

- Plus subscribers get **paid** private servers free. You earn up to **100 Robux per subscriber
  per renewal**: 70% of your server price, capped at 100.
- Counts only the owner's time in the paid private server **they created** in your game: ≥ 60
  cumulative minutes over the 30 days before renewal, and your server must be among their top 5
  paid private servers across Roblox. Invited Plus guests don't count. Free servers earn nothing.
- **Price math (inferred):** 70% × price reaches the 100-Robux cap at ~143 Robux. Below that,
  each Plus owner pays you less; above it, Plus payouts don't grow but non-Plus buyers pay more.

### Free or paid: decision table (inferred unless tagged)

| Choose | When | Reference |
|---|---|---|
| **Free** | The game lives on groups: leagues, scrims, roleplay scenes, practice; co-play matters more than revenue | Realistic Street Soccer advertises free private servers with an admin panel (official game description, 2026-10) |
| **Paid, 150–250 Robux/month** | Single-player-friendly loops (farming, tycoon, obby practice) where privacy is a convenience | Tower of Hell: 250 Robux/month with tower-length and shop settings (community, wiki) |
| **Paid + perks pass** | Owners want game-specific tools beyond Roblox's server | TSB sells "Private Servers+" for 499 Robux (data, API 2026-10-23) |

- At ≥ 143 Robux a paid server earns the full Plus payout per qualifying Plus owner
  (arithmetic above).
- Free servers still need owner tools and abuse limits; "free" doesn't mean "unmanaged".

### Owner commands (inferred unless tagged)

Brookhaven's private servers offer prop saving, server music and announcements, removing or
locking props, setting admins, kick and temp-ban, and time/weather/theme controls (official
game description, 2026-10-24; via [roleplay](../genres/roleplay-life-sim.md)). A solid default
set:

| Command | Who | Notes |
|---|---|---|
| Kick / ban from this server | Owner, owner's mods | Ban list saved by `PrivateServerId`, enforced on join |
| Appoint / remove mods | Owner only | Mods can't appoint mods |
| Game settings | Owner, mods | Map, mode, round length, PvP on/off, time of day, weather |
| Announcements | Owner, mods | Filtered text ([UI/UX](../../.claude/skills/roblox-ui/references/ui-ux.md) and chat rules) |
| Reset map / clear props | Owner, mods | Rate-limited |

Never: commands that grant currency, items, XP or stats, edit saves, or affect other servers.
Owner tools change **this server's rules**, not anyone's progress.

### What to disable or change in private servers (inferred unless tagged)

- **Global leaderboard writes.** Records set alone or among friends (custom settings, easy
  maps, a cooperative "victim") don't belong on public boards. Write global stats from public
  servers only, or show private-server runs on a separate board
  ([leaderboards](leaderboards.md)).
- **Per-server rare spawns.** A world drop tuned for a full public server is a farm in a 1-player
  private server. Scale rare spawn and restock odds by players present (capped at the full-server
  rate), or keep server-wide drops public-only.
- **Trading farms.** Alts can trade freely in a private server. Keep the same trade rules
  everywhere: account-age and playtime gates, per-day limits, value checks ([trading](trading.md)).
  Never give trading bonuses in private servers.
- **Admin-event luck and boosts** apply the same as in public servers, so private servers aren't
  excluded, but per-player caps still hold ([server events](server-events-admin-abuse.md)).
- **Settings that make the game easier** (shorter towers, PvP off, custom rules) turn off badge
  awards and quest progress that assume normal rules (inferred; Tower of Hell's private-server
  towers are a practice tool, community).
- **Stealing games:** an owner can force a target out and then steal; cancel steals when the
  owner leaves and protect fresh joiners (community report, unverified; fix in
  [base defense](base-defense-and-stealing.md)).

### Reserved servers: parties, matches and free "custom servers"

Facts (official, engine reference read 2026-10-25):
- `TeleportService:ReserveServerAsync(placeId)` (server only) returns an access code and the
  reserved server's `PrivateServerId`. Codes stay valid indefinitely.
- Teleport with `TeleportService:TeleportAsync(placeId, players, options)` and
  `TeleportOptions.ReservedServerAccessCode`, or `TeleportOptions.ShouldReserveServer = true` to
  reserve and send in one call (the two conflict). ≤ 50 players per call; `pcall` and retry.
- Teleports don't work in Studio playtests. Console players with cross-play off can land in a
  separate instance with the same `PrivateServerId`; `game.MatchmakingType` tells them apart.
- `TeleportOptions:SetTeleportData` is client-visible and unencrypted.

Uses (inferred unless tagged):
- **Party matches and raids:** lobby pad → reserved server for the party
  ([boss fights and raids](boss-fights-and-raids.md), [tower defense](../genres/tower-defense.md)).
- **Free custom servers with join codes:** a player presses "Create server"; the server reserves
  one, stores `{accessCode, hostUserId}` under a short random code (6 characters, no
  look-alikes) in a MemoryStore hash map with an expiry (max 45 days, official quota), and shows
  the code. Friends type it in to join. Driving Empire shipped custom servers in beta on
  2026-10-16 (official game description, via [racing](../genres/racing-driving.md)).
- In a reserved server the "owner" is whoever your code says (the host's `UserId` from the
  MemoryStore record), since `PrivateServerOwnerId` is `0`.

## Implementation outline (server-authoritative)

- **Detect the kind once at startup**, publish it as a `workspace` attribute so clients can show
  the owner panel and a "Private server" tag.
- **Settings record:** DataStore `PrivateServerSettings`, key `PS_{PrivateServerId}`, value
  `{Mods = {userId}, Banned = {userId}, Settings = {...}}`. Only one instance runs at a time, so
  one writer: save on change (debounced to once per 60 s) and in `game:BindToClose`
  (official single-instance rule; design inferred). Keep it small; include no player progress.
- **Owner remote:** `OwnerCommand(command, arg)`: token bucket, command in a whitelist, `arg`
  type-checked, target must be in the server and not the owner, caller is owner or mod from
  server state ([security](../../.claude/skills/roblox-code/references/security.md)).
- **Gates** read `ServerKind` from one module: leaderboards, rare spawns, badges, quests.
- **Analytics:** log a `private_server_join` custom event with the kind as a field
  ([analytics](../fundamentals/analytics.md)).

```lua
--!strict
-- ServerScriptService/ServerKind: OUTLINE. Detect, load owner settings, gate global writes.
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local KIND = if game.PrivateServerId == "" then "Public"
	elseif game.PrivateServerOwnerId == 0 then "Reserved" else "Private"
workspace:SetAttribute("ServerKind", KIND)

type Settings = {Mods: {number}, Banned: {number}, PvP: boolean, Map: string}
local settings: Settings = {Mods = {}, Banned = {}, PvP = true, Map = "Default"}
local store = DataStoreService:GetDataStore("PrivateServerSettings")
local key = `PS_{game.PrivateServerId}`
local dirty = false

if KIND == "Private" then
	local ok, saved = pcall(function() return store:GetAsync(key) end)
	if ok and type(saved) == "table" then
		settings.Mods = if type(saved.Mods) == "table" then saved.Mods else {}
		settings.Banned = if type(saved.Banned) == "table" then saved.Banned else {}
		settings.PvP = saved.PvP ~= false
		settings.Map = if type(saved.Map) == "string" then saved.Map else "Default"
	end
end

local function isOwner(p: Player): boolean
	return KIND == "Private" and p.UserId == game.PrivateServerOwnerId
end
local function isMod(p: Player): boolean
	return isOwner(p) or (KIND == "Private" and table.find(settings.Mods, p.UserId) ~= nil)
end

Players.PlayerAdded:Connect(function(p)
	if table.find(settings.Banned, p.UserId) then p:Kick("You were removed from this private server.") end
end)

local OwnerCommand = ReplicatedStorage.Remotes.OwnerCommand :: RemoteEvent
OwnerCommand.OnServerEvent:Connect(function(p: Player, command: unknown, arg: unknown)
	-- token bucket here (roblox-code references/security.md)
	if not isMod(p) then return end
	if command == "Ban" and typeof(arg) == "Instance" and arg:IsA("Player") and arg.Parent == Players then
		local target = arg :: Player
		if target == p or isOwner(target) or (isMod(target) and not isOwner(p)) then return end
		table.insert(settings.Banned, target.UserId); dirty = true
		target:Kick("You were removed from this private server.")
	elseif command == "PvP" and typeof(arg) == "boolean" then
		settings.PvP = arg; dirty = true
		workspace:SetAttribute("PvP", arg)
	end -- Mod (owner only), Unban, Map: same shape, whitelisted
end)

task.spawn(function()
	while KIND == "Private" do
		task.wait(60)
		if dirty then dirty = false; pcall(function() store:SetAsync(key, settings) end) end
	end
end)
game:BindToClose(function()
	if KIND == "Private" and dirty then pcall(function() store:SetAsync(key, settings) end) end
end)

return {
	kind = KIND,
	writesGlobalStats = KIND == "Public", -- leaderboards, records
	rareSpawnScale = function(): number -- 1 player in a private server ≠ a full public server
		return if KIND == "Public" then 1 else math.min(1, #Players:GetPlayers() / Players.MaxPlayers * 2)
	end,
}
```

## Common bugs and exploits

| Bug or exploit | Fix |
|---|---|
| Reserved servers treated as player-owned (or the reverse) | Check both properties: reserved = `PrivateServerId ~= ""` and `PrivateServerOwnerId == 0` (official) |
| Settings keyed by `JobId` vanish when the server restarts | Key by `PrivateServerId`, stable across instances (official) |
| Mods ban the owner or appoint more mods | Owner-only for mod changes; owner can't be targeted (inferred) |
| Owner command remote used in public servers | Every command checks `KIND == "Private"` and the caller's role on the server (inferred) |
| Private-server records top the global leaderboard | Global writes from public servers only (inferred) |
| Rare spawns farmed alone in a private server | Scale odds by players present (inferred) |
| Alt trading farms | Same trade gates and limits in every server kind ([trading](trading.md)) |
| Price change wipes every subscriber | Set the price before launch; never change casually (official) |
| Join-code collisions or guessable codes | 6+ random characters, MemoryStore record with expiry, rate-limited lookups (inferred) |
| Teleport data used for authority (host, mode) | Read authority from a server-side store; teleport data is client-visible (official) |
| Testing reserved servers in Studio "does nothing" | Teleports don't work in Studio; test in a published test place (official) |
| Under-13 friends can't join | Expected for some accounts (official); don't make the core loop depend on private servers |

## Checklist for agents

- [ ] Server kind detected from `PrivateServerId` + `PrivateServerOwnerId` and published as an
      attribute.
- [ ] Free vs paid decided with the table; paid price ≥ ~143 Robux if Plus payouts matter;
      price set before launch.
- [ ] Owner panel: kick/ban, mods (owner only), game settings, announcements; nothing that grants
      progress or touches saves.
- [ ] Owner settings saved by `PrivateServerId`, debounced, saved in `BindToClose`.
- [ ] Owner remote whitelisted, typed, rate-limited, role-checked on the server.
- [ ] Global leaderboards and records written from public servers only.
- [ ] Rare spawns scaled by players present outside public servers; trade rules identical.
- [ ] Easier custom settings disable badge and quest progress that assumes normal rules.
- [ ] Reserved servers for parties/matches with `pcall` + retry teleports; custom-server join
      codes stored in MemoryStore with expiry.
- [ ] Private-server joins logged in analytics.

## Sources

1. https://create.roblox.com/docs/production/monetization/private-servers — free or monthly Robux, enabling steps, public-game requirement, price change cancels subscriptions, no paid access, under-13 join limits, use cases
2. https://create.roblox.com/docs/production/monetization/roblox-plus — Plus free paid servers, up to 100 Robux, 60 minutes, top 5 servers, owner-only time, 70% share example
3. https://create.roblox.com/docs/reference/engine/classes/DataModel — PrivateServerId and PrivateServerOwnerId semantics, one instance at a time, MatchmakingType
4. https://create.roblox.com/docs/reference/engine/classes/TeleportService — ReserveServerAsync, reserved-server check, cross-play note, TeleportAsync limits and conflicts, Studio limitation
5. https://create.roblox.com/docs/projects/teleport — retries, client-visible teleport data
6. https://create.roblox.com/docs/discovery — co-play days include private servers
7. https://en.help.roblox.com/hc/articles/205345050 — billing cadence (search snippet only; direct fetch refused, unverified)
8. https://create.roblox.com/docs/cloud-services/memory-stores — hash maps, 45-day max expiration
9. https://tower-of-hell.fandom.com/wiki/Private_Servers — 250 Robux/month, practice settings (via Tower of Hell (case study: tower-of-hell))
10. https://apis.roblox.com/game-passes/v1/universes/3808081382/game-passes — TSB "Private Servers+" 499 (via [battlegrounds](../genres/battlegrounds.md))
11. https://games.roblox.com/v1/games?universeIds=1686885941 — Brookhaven description with private-server owner tools (read 2026-10-24, via [roleplay](../genres/roleplay-life-sim.md))
12. https://games.roblox.com/v1/games?universeIds=… — read 2026-10-25: `createVipServersAllowed` returned false for all 50 top charted games, including ones known to sell private servers, so the field doesn't show a game's setting to anonymous callers (data; interpretation inferred)

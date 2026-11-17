---
title: Codes
type: pattern
read-when: Adding redeemable codes.
last-researched: 2026-10-22
---

# Codes

## What it is

A text box (usually under Settings or a "Codes" button) where players type a short string such
as `SPOOKY26`. The server normalizes it and looks it up in a server-only table. It checks that
the code has started, hasn't expired, hasn't been redeemed on this account, and that any
requirement (group membership, account age) is met. Then it grants the reward and records
the redemption in the same saved profile as the reward.

## Why it works

- **A return reason on update day.** A new code with each update gives lapsed players a
  concrete reason to open the game, and puts a boost in their hands that pulls them into the new
  content (inferred).
- **Cheap goodwill.** A free gift costs nothing per player and starts the session with a
  win (inferred).
- **A bridge to your channels.** Codes posted on the group or socials give players a reason to
  follow them (inferred). A DevForum reply says asking for likes and releasing a code at a like
  milestone isn't against the Terms of Use (community, unverified; not official policy).
- **External search traffic.** Code-list sites and video creators cover games that have codes,
  which is free visibility (inferred).
- **Codes are optional.** Steal An Egg, the #1 game by players on 2026-10-22, has no code
  system at all (community wiki, 2026-10; data for the rank). Don't build codes before the core
  loop works.

## Genres that use it

Most common where there's a currency or boost to give: [simulator](../genres/simulator.md),
[tycoon](../genres/tycoon.md), [anime RPG](../genres/anime-rpg.md),
[gacha/raid](../genres/gacha-raid.md), [tower defense](../genres/tower-defense.md),
[RNG aura](../genres/rng-aura.md), [pet-egg](../genres/pet-egg-collection.md),
[fishing](../genres/fishing.md). Rare in obbies, horror and story games, which have little to
grant (inferred). Plan codes alongside [live ops](../fundamentals/live-ops-and-updates.md).

## Design rules

### Code format and matching

- 4–20 characters, letters and digits only. Avoid look-alikes (`O`/`0`, `I`/`1`/`L`) in
  generated codes. Theme them to the update: `HALLOWEEN26`, `100KLIKES` (inferred).
- **Case-insensitive and whitespace-tolerant.** Normalize input with
  `string.upper(string.gsub(s, "%s+", ""))`, and store table keys already uppercased. Assert
  this at load so a lowercase key can't silently never match (inferred).
- Reject input over 32 characters, or invalid UTF-8 (`utf8.len(s) == nil`), before any lookup
  (official validation rules; see [security](../../.claude/skills/roblox-code/references/security.md)).
- Use distinct messages, which saves kids from retyping a dead code:
  "That code isn't valid", "That code has expired", "Already redeemed", "Still loading, try
  again". Keep expired codes in the table so you can say "expired" (inferred).

### What to give

- **Size:** about 5–15 minutes of play at the player's current tier, or a 15–30 minute boost
  (2× coins or luck). Boosts beat flat currency because they make players play *now* (inferred).
- **Scale to progress, with a cap.** "10 minutes of your current income, max X" stays useful
  for veterans without wrecking new players' early curve (inferred).
- **Good rewards:**
  - timed boosts;
  - consumables (spins, eggs, seeds);
  - an exclusive cosmetic for a launch or milestone code;
  - a starter bundle for a welcome code.
- **Bad rewards:**
  - anything that decides PvP or stealing;
  - tradeable rare items (alt accounts farm them and flood trades);
  - Robux or anything with real-money value (inferred; see
    [monetization](../fundamentals/monetization.md)).
- Code rewards are **untradeable** by default. For a valuable reward, also require
  `Player.AccountAge >= 7` days or so (official property; threshold inferred).

### Expiry and schedule

- Each code has an optional `startsAt` and `expiresAt` in UTC Unix seconds, checked against the
  server's `os.time()`. Never use client time (official: `os.time` defaults to UTC).
- Update codes last 1–3 weeks. One evergreen welcome code is fine (inferred).
- Pre-load next update's code with a future `startsAt`, so it goes live at announcement time
  without a publish (inferred).
- Don't use "first N players" codes. They need a cross-server counter (`MemoryStoreService`)
  and cause "the code doesn't work" complaints (inferred).

### Where players find codes

- **In the game itself first.** Many young players can't reach Discord or X, so show the current
  code on an update board near spawn, or in the Codes panel itself (inferred).
- **Experience description:** a line like "New code every update, open the Codes menu". Keep
  reward promises out of the title and thumbnail. Roblox doesn't prioritize metadata that
  implies monetary rewards (official, 2026-10; see
  [metadata](../fundamentals/metadata-thumbnails-icons.md)).
- **Update announcements** (max 60 characters, once every 3 days, sent to followers) can carry
  the code (official limits; use inferred).
- **Experience Notifications are for personal, actionable messages.** A generic "new code" blast
  fits badly with Roblox's rules and raises turn-off rates. Use update announcements instead
  (official rules; judgement inferred; see [retention](../fundamentals/retention.md)).
- **Group codes:** gate a code on `Player:IsInGroupAsync(groupId)`. `IsInGroup` is deprecated
  (official API, 2026-10). Group reward codes are a common DevForum pattern (community).
- **Socials:** use only the experience page's social links. Don't print off-platform handles or
  URLs inside the game (inferred; Roblox moderates off-platform direction).

### Codes and returns on update day

- Ship each update with: a new code in the update notes, an in-game board, an update
  announcement, and a boost that fits the new content ("2× luck for 20 min" for a new egg area)
  (inferred).
- Measure it: `AnalyticsService:LogCustomEvent(player, "code_redeemed")` with the code as a
  custom field, after the grant succeeds. Compare redemptions to returning-user DAU on update
  days (official API; see [analytics](../fundamentals/analytics.md)).
- A code isn't a substitute for content. If the update is thin, the returning players bounce,
  and a cohort that returns and bounces still counts in your play-days data (inferred; see
  [discovery](../fundamentals/discovery-algorithm.md)).

### Rate limiting and brute force

- Token bucket on the redeem remote: burst of 5, then 1 every 3 s. After 10 failed lookups in
  60 s, refuse for 60 s (inferred; pattern from
  [security](../../.claude/skills/roblox-code/references/security.md)).
- Brute force is hopeless against 6+ random characters: 32⁶ ≈ 1.07 billion combinations
  (inferred arithmetic). Themed codes are guessable, but they're public anyway. The real risk is
  **leaked unreleased codes**, so keep the table server-only.

### Filtering: lookup vs display

- **The lookup needs no filtering.** The typed string is only compared with your table and is
  never shown to anyone (inferred from the rule below).
- **Never display raw input to others.** Roblox's rule: you must filter any displayed text you
  don't control, including TextBox input (official, 2026-10).
  - Don't post "Bob redeemed <input>" in chat, and don't show the input on a billboard.
  - Echo your own canonical code name from the table ("Redeemed SPOOKY26!"). That text is
    developer-authored.
  - On failure, say "That code isn't valid" without repeating the input.
- If any feature does show player text, filter it with `TextService:FilterStringAsync`, then
  `TextFilterResult:GetNonChatStringForBroadcastAsync()` (whole server) or
  `GetNonChatStringForUserAsync()` (one user), in `pcall` (official, 2026-10).

## Implementation outline (server-authoritative)

- **Code table:**
  - Default: a ModuleScript in `ServerStorage`, never `ReplicatedStorage`. Exploiters read
    everything replicated, so unreleased codes would leak (official threat model).
  - Adding a code means publishing. Running servers keep the old table until they restart, so
    publish with "Migrate to latest update" (inferred).
  - **Remote config option:** `ConfigService:GetConfigAsync()` returns a `ConfigSnapshot`.
    Read a value with `GetValue(key)`, and listen for `UpdateAvailable`, then `Refresh()`
    (official API names, 2026-10). Supported value types and how fast updates propagate aren't
    documented (unverified). Test before relying on it for codes.
- **Saved data:** `Codes: {[string]: number}`, mapping canonical code to redemption time.
  Store it in the same profile as the reward, so the grant and the record save together. If the
  server dies before the save, both are lost and the player can just redeem again (inferred;
  see [player data](player-data.md)).
- **Remote:** `RedeemCode(text)` as a RemoteFunction returning `(ok, message)`.

```lua
--!strict
-- ServerScriptService/Codes.server.lua: OUTLINE, not drop-in
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")
local PlayerData = require(script.Parent.PlayerData) -- session-locked; get() → nil until loaded

type Code = {startsAt: number?, expiresAt: number?, minAgeDays: number?, groupId: number?,
	grant: (data: any) -> ()}
local CODES: {[string]: Code} = require(ServerStorage.CodeTable) -- keys are UPPERCASE
for k in CODES do assert(k == string.upper(k), `code key must be uppercase: {k}`) end

local CAP, REFILL, MAX_FAILS, LOCK_SECS = 5, 1 / 3, 10, 60
type Bucket = {tokens: number, last: number, fails: number, failStart: number, lockedUntil: number}
local buckets: {[Player]: Bucket} = {}
local pending: {[Player]: boolean} = {}

local function allow(p: Player): boolean
	local t = os.clock()
	local b = buckets[p] or {tokens = CAP, last = t, fails = 0, failStart = t, lockedUntil = 0}
	buckets[p] = b
	if t < b.lockedUntil then return false end
	b.tokens = math.min(CAP, b.tokens + (t - b.last) * REFILL)
	b.last = t
	if b.tokens < 1 then return false end
	b.tokens -= 1
	return true
end

local function fail(p: Player)
	local b, t = buckets[p], os.clock()
	if t - b.failStart > 60 then b.fails, b.failStart = 0, t end
	b.fails += 1
	if b.fails >= MAX_FAILS then b.lockedUntil = t + LOCK_SECS end
end

local Redeem = ReplicatedStorage.Remotes.RedeemCode :: RemoteFunction
Redeem.OnServerInvoke = function(player: Player, raw: unknown): (boolean, string)
	if pending[player] or not allow(player) then return false, "Slow down a little" end
	if typeof(raw) ~= "string" or #raw > 32 or utf8.len(raw) == nil then
		fail(player); return false, "That code isn't valid"
	end
	local key = string.upper((string.gsub(raw, "%s+", "")))
	local code, data, now = CODES[key], PlayerData.get(player), os.time()
	if not data then return false, "Still loading, try again" end
	if not code or (code.startsAt and now < code.startsAt) then
		fail(player); return false, "That code isn't valid" -- never echo the raw input
	end
	if code.expiresAt and now >= code.expiresAt then return false, "That code has expired" end
	if data.Codes[key] then return false, "Already redeemed" end
	if code.minAgeDays and player.AccountAge < code.minAgeDays then
		return false, "This code needs an older account"
	end
	if code.groupId then
		pending[player] = true -- the check below yields: block a second concurrent redeem
		local ok, inGroup = pcall(player.IsInGroupAsync, player, code.groupId)
		pending[player] = nil
		if not ok then return false, "Try again in a moment" end
		if not inGroup then return false, "Join the group first" end
		if data.Codes[key] then return false, "Already redeemed" end -- re-check after the yield
	end
	data.Codes[key] = now -- record and reward live in the same profile document
	code.grant(data)
	-- AnalyticsService:LogCustomEvent(player, "code_redeemed", 1, {[Enum.AnalyticsCustomFieldKeys.CustomField01.Name] = key})
	return true, `Redeemed {key}!` -- canonical name from our table, not raw input
end

Players.PlayerRemoving:Connect(function(p) buckets[p] = nil; pending[p] = nil end)
```

Client: a `TextBox` with `ClearTextOnFocus = false`, submitted on `FocusLost` with
`enterPressed` or on a Redeem button. Show the returned message in the panel. Disable the
button while waiting. That's UX only; the server enforces everything.

## Common bugs and exploits

| Bug or exploit | Fix |
|---|---|
| Double redeem from two fast requests while a check yields | `pending[player]` guard, plus re-check `data.Codes[key]` after any yield |
| Code works in lowercase but not uppercase (or the reverse) | Normalize input; store uppercase keys; assert at load |
| Unreleased codes leaked | Table in `ServerStorage` or a server-read config; never replicated |
| Redemption saved apart from the reward | Same profile document, same save |
| Expiry dodged with a device clock change | Server `os.time()` only |
| "Invalid" shown for an expired code | Keep expired entries; return "expired" |
| Brute-force spam lags the server | Token bucket + failure lockout; bounded string length |
| Raw input shown in chat or a billboard | Echo the canonical code from the table; filter any real user text |
| New code missing on old servers | Publish with migration, or read codes from `ConfigService` |
| Alts farm tradeable code rewards | Untradeable rewards; `AccountAge` gate on valuable codes |
| Code reward inflates the economy | Scale to tier with a cap; prefer timed boosts |
| Redeem before data loads, then the reward is overwritten | Refuse while `PlayerData.get` is nil ("Still loading") |

## Checklist for agents

- [ ] Code table server-only, uppercase keys, `startsAt`/`expiresAt` in UTC Unix seconds.
- [ ] Input type, length and UTF-8 checked, then normalized (upper, no whitespace) before lookup.
- [ ] Redemption stored in the player's profile next to the reward; one redemption per account.
- [ ] Rate limit with a failure lockout; concurrent-redeem guard around any yield.
- [ ] Distinct messages for invalid, expired, already redeemed and loading. Raw input never
      echoed to anyone.
- [ ] Rewards: boosts or consumables sized to about 5–15 min of play, untradeable, never PvP
      power or Robux.
- [ ] Group gating via `Player:IsInGroupAsync`; `AccountAge` gate on valuable codes.
- [ ] Current code visible in game; a new code with each update; no reward promises in title
      or thumbnail.
- [ ] `code_redeemed` logged after the grant; redemptions read against update-day returns.

## Sources

1. https://create.roblox.com/docs/ui/text-filtering — must filter displayed text you don't control (TextBox input); FilterStringAsync, GetNonChatStringForBroadcastAsync, GetNonChatStringForUserAsync
2. https://create.roblox.com/docs/reference/engine/classes/TextService — FilterStringAsync
3. https://create.roblox.com/docs/reference/engine/classes/Player — IsInGroupAsync (IsInGroup deprecated), AccountAge
4. https://create.roblox.com/docs/reference/engine/classes/ConfigService — GetConfigAsync, GetConfigForPlayerAsync
5. https://create.roblox.com/docs/reference/engine/classes/ConfigSnapshot — GetValue, Refresh, UpdateAvailable, Outdated
6. https://create.roblox.com/docs/scripting/security/client-server-boundary — string validation, token bucket, server-only secrets
7. https://create.roblox.com/docs/reference/engine/libraries/os — os.time defaults to UTC
8. https://create.roblox.com/docs/discovery — metadata implying monetary rewards isn't prioritized
9. https://create.roblox.com/docs/production/promotion/experience-events — update announcements: 60 characters, once every 3 days
10. https://create.roblox.com/docs/cloud-services/experience-notifications — notifications must be personal; banned dark patterns
11. https://devforum.roblox.com/t/asking-people-to-like-your-game-against-tos/3753529 — like-milestone codes said not to break the ToS (community reply)
12. https://devforum.roblox.com/t/join-group-prompt/2609702 — group reward systems are common
13. https://stealanegg.fandom.com/wiki/Codes — Steal An Egg has no code system (2026-10)

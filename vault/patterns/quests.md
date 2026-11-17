---
title: Quests, achievements and badges
type: pattern
read-when: Adding daily/weekly quests, missions, questlines, achievements, or Roblox badges.
last-researched: 2026-10-25
---

# Quests, achievements and badges

## What it is

One server-side quest engine with four uses:

| Kind | Resets | Typical count | Job |
|---|---|---|---|
| **Daily quests** | 00:00 UTC | 3 active | A reason to play today, and a tour of verbs the player skips |
| **Weekly quests** | Monday 00:00 UTC (or your update slot) | 3–5 active | Covers days 2–7; bigger goals across several sessions |
| **Achievements** | Never; tiered (10 / 100 / 1,000 / 10,000) | 20–60 at launch | Long-term goals over lifetime stats; some award a Roblox badge |
| **Questlines** | Never; ordered steps | 1 active per line | FTUE after the first loop, NPC chains, island gates ([anime RPG](../genres/anime-rpg.md)) |

Every quest is data: an event name, an optional filter, a target, and a reward. Gameplay
systems on the server report events ("Kill", "Harvest", "RoundWon"); the quest engine counts
them. Clients only display progress and ask to claim.

## Why it works

- **A told goal beats a found one.** "Win 2 rounds (1/2)" turns aimless play into a short task
  with a payoff, and points players at features they haven't tried (inferred). Roblox
  recommends short, mid and long-term goals visible in UI (official, 2026-10).
- **Resets map onto ranking windows.** Recommended for You counts play days per user over D1,
  D2–7 and D8–28 (official, 2026-10; see [retention](../fundamentals/retention.md)). Daily quests
  target tomorrow, weekly quests the rest of week 1, achievements and questlines weeks 2–4
  (inferred).
- **Fixed visible resets** are item 4 of the vault's retention checklist
  ([retention](../fundamentals/retention.md)).
- **Badges are public.** A badge shows on the player's profile and inventory (official,
  2026-10), so it's status other players can see off-game (inferred).
- **The risk is chores.** Quests that demand more than a normal session, or that need Robux,
  friends or luck, turn into obligation and get skipped (inferred).

## Genres that use it

Nearly all progression games: [simulator](../genres/simulator.md),
[tower defense](../genres/tower-defense.md), [gacha raid](../genres/gacha-raid.md),
[anime RPG](../genres/anime-rpg.md), [farming](../genres/farming-growing.md),
[fishing](../genres/fishing.md), [pet collection](../genres/pet-egg-collection.md). Round-based
games use lighter dailies ("play 3 rounds") ([round system](round-system.md)). Pairs with
[daily rewards](daily-rewards-and-streaks.md) (same UTC reset) and
[server events](server-events-admin-abuse.md) (event quests).

## Design rules

### What the leaders ship (reference)

| Game | Shape | Tag |
|---|---|---|
| Tower Defense Simulator | 4 daily quests (2 active), 2 weekly (1 active); refills sold for 50 and 120 Robux | community, TDS wiki 2026-10 |
| Vanguards | Challenges rotate every 30 min, 24 h and 7 days, capped at 20 completions a day | community, wiki 2026-10 |
| Blox Fruits | One active kill quest at a time from island NPCs, matched to level | community, wiki 2026-10 |
| Anime Dice | Quest claims are part of every session; weekly updates each bring a 3-day event | community, guides 2026-09 and bloxodes 2026-10 (via [gacha raid](../genres/gacha-raid.md)) |

### Sizing (inferred unless tagged)

- **Daily set:** 3 quests, total ~10–20 min of normal play. One easy (≤ 3 min), one medium, one
  that nudges a feature the player under-uses (shop, rebirth, trading, a new mode).
- **Weekly set:** 3–5 quests, ~2–4 h of play spread over the week. Never more than a typical
  player's weekly playtime; check analytics after launch.
- **Achievements:** tiers at ×10 steps (10 / 100 / 1,000 / 10,000) over lifetime stats. The first
  tier of 5+ achievements must fall inside the first session.
- **Targets scale with progress, then freeze.** `target = base × tierScale(level)`, rounded,
  computed **when the quest is rolled** and saved. Never recompute mid-quest, or a level-up moves
  the goalposts.
- **Objectives use verbs the player already does.** Kill, collect, earn, win, place, hatch,
  survive, visit. Never "buy with Robux", never "get a 1% drop" (pure RNG), never "play with a
  friend" without a solo alternative ([social rules](../fundamentals/social-and-virality.md)).
- **Filters stay broad.** "Defeat 20 enemies on Island 2" is fine; "defeat 20 Red Slimes" sends
  players hunting one spawn and crowds it.

### Rewards pacing (inferred)

- A quest pays ~1.5–2× what the same playtime earns unrewarded. That's the bonus for following
  direction. Completing all 3 dailies adds a bonus chest worth ~1 more quest.
- Quests are a **top-up, not the income.** All dailies together ≤ ~25% of a typical day's soft
  currency, or players log in, clear quests and leave.
- Weekly quests pay something the daily loop can't: premium soft currency, a cosmetic token, an
  egg or a reroll item.
- Achievement tiers pay one-time rewards that grow ×2–×3 per tier, plus a title or badge on
  milestone tiers.
- Every reward is shown before the quest is started, and the server grants exactly what was
  shown.

### Rerolls, refills and claiming

- **1 free reroll per day**, applied to one unclaimed, incomplete daily. Rerolled quests come
  from the same difficulty band and exclude the current set (inferred).
- **Paid refills** (TDS sells them, above) add *extra* quests; they never complete a quest or
  skip a wait. Keep them cheap and off the claim screen (inferred; Robux-skippable timers put
  Roblox players off, official 2026-10, see [monetization](../fundamentals/monetization.md)).
- **Manual claim** with a red-dot badge on the quest button and a short reward animation
  ([game feel](../../.claude/skills/roblox-vfx/references/game-feel.md)). At reset, a completed but unclaimed quest is
  **auto-granted**, never lost (inferred, kid-friendly default).
- **Missed days don't stack.** Yesterday's unfinished dailies expire; no "catch up 5 days of
  quests" backlog (inferred).

### Achievements

- Drive them from **lifetime counters** in the profile (`Stats.Kills`, `Stats.RoundsWon`), not
  from quest progress. An achievement added in a later update then evaluates against existing
  counters at join, so veterans get credit retroactively (inferred).
- Show locked achievements with their target and reward. Hide only true secrets, and give
  secrets a hint line (inferred).
- A collection index (units, fish, pets) is an achievement list with pictures; reward tiers at
  25/50/75/100% of each set (inferred; see [rarity tiers](rarity-tiers-and-eggs.md)).

### Roblox badges (BadgeService)

Facts (official, engine reference and badges guide, read 2026-10-25):
- Create badges in Creator Dashboard: **5 free per game per 24 h (GMT); each extra costs 100
  Robux.** Name, description and "enabled" are required; disabled badges can't be earned and
  don't show on the game page. Icon: 512×512, cropped to a circle.
- `BadgeService:AwardBadgeAsync(userId, badgeId)` returns a boolean. It works only if the player
  is **connected to this experience**, doesn't already own the badge, the call runs from a
  **server** script, the place belongs to the badge's experience, and the badge is enabled
  (`BadgeService:GetBadgeInfoAsync(badgeId).IsEnabled`). Rate limit `50 + 35 × users` per minute.
- `BadgeService:UserHasBadgeAsync(userId, badgeId)`: one badge, `50 + 35 × players` per minute.
  `BadgeService:CheckUserBadgesAsync` takes up to **10** IDs and returns owned IDs;
  `BadgeService:GetUserBadgesAsync` takes up to **100** and returns `BadgeId` + `AwardedDate`;
  both `10 + 5 × players` per minute per server.
- Players can **delete** a badge from their profile and be awarded it again. So the badge is not
  the record of progress: the profile is.
- `AwardBadge` and `UserHasBadge` (no Async) are deprecated. `AchievementService` appears in
  the API dump but is Roblox-internal (RobloxScriptSecurity), so game scripts can't call it
  (official API dump, 2026-10).
- Studio behavior: the deprecated `IsDisabled` docs say badges can only be tested in Studio
  while disabled; whether `AwardBadgeAsync` behaves the same isn't documented (unverified).
  Test awards in a separate test experience.

Design rules (inferred):
- Spend the 5 free daily badges on **meaningful moments**: first win, first boss, milestone
  tiers, secrets found, event attendance. A "Welcome" badge everyone gets carries no status.
- Ship 5–15 badges at launch and add 1–3 per update, inside the free quota.
- Event badges (attended the launch event, beat the Halloween boss) are the cheapest FOMO-free
  collectible: free, cosmetic, visible ([server events](server-events-admin-abuse.md)).

## Implementation outline (server-authoritative)

### Data model

- **Definitions:** `QuestDefs` ModuleScript, one entry per quest:
  `{Pool = "Daily" | "Weekly" | "Line:<name>", Event = "Kill", Filter = "Island2"?, Base = 20,
  Band = 1..3, Reward = {Coins = 150}}`. A display copy can replicate; the server reads only its
  own copy. Secret achievements stay in `ServerStorage` ([security](../../.claude/skills/roblox-code/references/security.md)).
- **Profile** (session-locked, see [player data](player-data.md)):
  - `Quests = {Day, Week, Rerolls, Daily = {Slot}, Weekly = {Slot}, Lines = {[line] = step}}`
  - `Slot = {Id, Target, Progress, Claimed}` (fixed-length array, no gaps)
  - `Stats = {[eventName] = count}`, `Achievements = {[id] = highestTierClaimed}`
  - `Badges = {[tostring(badgeId)] = true}` (string keys; DataStores reject mixed tables)
- **Days and weeks:** `day = math.floor(os.time() / 86400)` (UTC);
  `week = math.floor((day + 3) / 7)` starts weeks on Monday 00:00 UTC (1970-01-01 was a
  Thursday) (inferred arithmetic). Client countdown from `Workspace:GetServerTimeNow()` (official
  API; see [daily rewards](daily-rewards-and-streaks.md)).
- **Global quest of the day** (same for every player on every server): seed `Random.new(day)`
  and pick from the pool. Every server computes the same answer with no MessagingService or
  DataStore traffic (inferred). Per-player sets are rolled once and saved instead.

### Flow

1. Gameplay code calls `Quests.record(player, "Kill", 1, "Island2")` **after** its own
   validation (kill confirmed by server combat, harvest by server timer). No remote ever reports
   progress.
2. `record` refreshes the day/week (re-roll if stale), adds to matching slots (capped at
   target), bumps `Stats`, checks achievement thresholds, and queues a UI update.
3. Batch UI updates: one `QuestUpdate` RemoteEvent per player at most every 0.5 s with only the
   changed slots (inferred).
4. `ClaimQuest(pool, index)` and `RerollQuest(index)` are RemoteFunctions, token-bucketed,
   typed `unknown`, refused until data loads.
5. Analytics: `AnalyticsService:LogEconomyEvent` (`Source`, transaction type `Gameplay`,
   SKU `quest_<id>`) on every grant; `AnalyticsService:LogCustomEvent(player, "quest_claimed")`
   with the quest ID in custom fields (official API; see [analytics](../fundamentals/analytics.md)).
   Track completion rate per quest ID: under ~30% means the target is too high (inferred).

### Luau sketch

```lua
--!strict
-- ServerScriptService/Quests: OUTLINE. Claim/reroll remotes, achievements and UI push omitted.
local AnalyticsService = game:GetService("AnalyticsService")
local BadgeService = game:GetService("BadgeService")
local PlayerData = require(script.Parent.PlayerData) -- get(player): Data? (nil until loaded)
local Defs = require(script.Parent.QuestDefs) -- {[string]: {Pool: string, Event: string, Filter: string?, Base: number, Reward: number}}

type Slot = {Id: string, Target: number, Progress: number, Claimed: boolean}
local COUNTS = {Daily = 3, Weekly = 4}

local function utcDay(): number return math.floor(os.time() / 86400) end
local function utcWeek(): number return math.floor((utcDay() + 3) / 7) end -- Monday 00:00 UTC

local function roll(pool: string, count: number, level: number): {Slot}
	local ids = {}
	for id, def in Defs do if def.Pool == pool then table.insert(ids, id) end end
	table.sort(ids) -- dictionary order isn't stable; sort, then shuffle
	local rng, out = Random.new(), {} :: {Slot}
	for i = 1, math.min(count, #ids) do
		local j = rng:NextInteger(i, #ids)
		ids[i], ids[j] = ids[j], ids[i]
		local target = math.max(1, math.round(Defs[ids[i]].Base * (1 + level / 50))) -- frozen now
		table.insert(out, {Id = ids[i], Target = target, Progress = 0, Claimed = false})
	end
	return out
end

local function grant(player: Player, data: any, s: Slot)
	s.Claimed = true
	local reward = Defs[s.Id].Reward
	data.Coins += reward
	AnalyticsService:LogEconomyEvent(player, Enum.AnalyticsEconomyFlowType.Source, "Coins", reward,
		data.Coins, Enum.AnalyticsEconomyTransactionType.Gameplay.Name, `quest_{s.Id}`)
end

local function refresh(player: Player, data: any)
	local q = data.Quests
	for pool, period in {Daily = utcDay(), Weekly = utcWeek()} do
		local key = if pool == "Daily" then "Day" else "Week"
		if q[key] ~= period then
			for _, s: Slot in q[pool] do -- finished but unclaimed: grant, never lose
				if not s.Claimed and s.Progress >= s.Target then grant(player, data, s) end
			end
			q[key], q[pool] = period, roll(pool, COUNTS[pool], data.Level)
			if pool == "Daily" then q.Rerolls = 1 end
		end
	end
end

local Quests = {}

-- Server systems only, after their own validation. Never wired to a RemoteEvent.
function Quests.record(player: Player, event: string, amount: number, filter: string?)
	local data = PlayerData.get(player)
	if not data or amount <= 0 or amount ~= amount then return end
	refresh(player, data)
	for _, pool in {"Daily", "Weekly"} do
		for _, s: Slot in data.Quests[pool] do
			local def = Defs[s.Id]
			if def and def.Event == event and (def.Filter == nil or def.Filter == filter) then
				s.Progress = math.min(s.Target, s.Progress + amount)
			end
		end
	end
	data.Stats[event] = (data.Stats[event] or 0) + amount -- achievements read lifetime stats
end

function Quests.awardBadge(player: Player, data: any, badgeId: number)
	local key = tostring(badgeId)
	if data.Badges[key] then return end
	data.Badges[key] = true -- the profile is the record; the badge is a mirror
	task.spawn(function()
		local ok, err = pcall(function() BadgeService:AwardBadgeAsync(player.UserId, badgeId) end)
		if not ok then warn("badge award failed; join reconcile retries", badgeId, err) end
	end)
end

return Quests
```

**Badge reconcile at join (outline):** collect badge IDs for everything the profile says is
earned, call `GetUserBadgesAsync` once (≤ 100 IDs, inside `pcall`), and award the missing ones,
spaced out. That fixes failed awards without a call per badge (inferred; limits official).

## Common bugs and exploits

| Bug or exploit | Fix |
|---|---|
| A `QuestProgress` remote lets exploiters complete everything | Only server systems call `record`; no client-reported progress (official principle, [security](../../.claude/skills/roblox-code/references/security.md)) |
| Progress counts twice (damage *and* kill events, two scripts on one death) | One canonical event per action; record at the single server point that confirms it (inferred) |
| Kill quests farmed on alts or friends in PvP | Count PvP kills only against distinct victims, max N per victim per hour; prefer PvE targets (inferred) |
| Target jumps on level-up | Freeze `Target` at roll time (inferred) |
| Midnight crossing breaks a session | `refresh` on every record/claim; client countdown re-enables at 00:00 UTC (inferred) |
| Two claims from fast double-taps | Check `Claimed` and set it with no yield between; token bucket (inferred) |
| Reroll spam for the easiest quest | Rerolls counted in saved data, reset per day (inferred) |
| Quests rolled before data loads, then overwritten | Refuse everything while `PlayerData.get` is nil (official rule in [player data](player-data.md)) |
| Gapped `Daily` array or numeric badge keys fail to save | Fixed-length slot arrays; `tostring(badgeId)` keys (official DataStore rules) |
| `AwardBadgeAsync` from a LocalScript does nothing | Server only (official) |
| Badge award throws during an outage and is lost | `pcall`, profile flag, reconcile at join (inferred) |
| Gameplay gated on badge ownership breaks when a player deletes the badge | Gate on profile data, never on `UserHasBadgeAsync` (official: badges can be deleted) |
| Badge calls on every join for every badge hit rate limits | One batched `GetUserBadgesAsync` per join, only for earned-but-unconfirmed IDs (official limits) |
| New achievement ignores veterans' history | Evaluate thresholds against lifetime `Stats` at join (inferred) |

## Checklist for agents

- [ ] Quest definitions are data (event, filter, base target, band, reward) in one module.
- [ ] Progress comes only from server systems calling `record` after their own validation.
- [ ] 3 dailies (reset 00:00 UTC) and 3–5 weeklies with a visible reset countdown from
      `Workspace:GetServerTimeNow()`.
- [ ] Targets frozen at roll time; dailies total ~10–20 min of play; nothing needs Robux, RNG
      luck or a friend.
- [ ] All dailies together ≤ ~25% of a day's soft income; weeklies pay something dailies can't.
- [ ] 1 free reroll a day; paid refills (if any) add quests, never complete them.
- [ ] Completed-unclaimed quests auto-grant at reset.
- [ ] Achievements read lifetime `Stats` and evaluate at join.
- [ ] Badges: awarded from the server with `AwardBadgeAsync` in `pcall`, mirrored in the
      profile, reconciled once per join; 5 free per 24 h budgeted.
- [ ] Claim/reroll remotes: token bucket, `unknown` args checked, refused until data loads.
- [ ] `LogEconomyEvent` on every grant; completion rate tracked per quest ID.

## Sources

1. https://create.roblox.com/docs/reference/engine/classes/BadgeService — AwardBadgeAsync requirements, rate limits, CheckUserBadgesAsync (10) and GetUserBadgesAsync (100) batches, deletable badges, deprecated methods, IsDisabled Studio note
2. https://create.roblox.com/docs/production/publishing/badges — 5 free badges per 24 h then 100 Robux, 512×512 circular icon, enabled flag, IsEnabled check
3. https://create.roblox.com/docs/discovery — play days per user windows D1 / D2–7 / D8–28
4. https://create.roblox.com/docs/production/monetization — visible goals, Robux-skippable timers disliked
5. https://create.roblox.com/docs/reference/engine/classes/AnalyticsService — LogEconomyEvent, LogCustomEvent, Gameplay transaction type
6. https://create.roblox.com/docs/reference/engine/libraries/os — os.time in UTC
7. https://tds.fandom.com/wiki/How_to_Play — TDS daily/weekly quest counts and Robux refills (via [tower defense](../genres/tower-defense.md))
8. https://animevanguards.fandom.com/wiki/Gamemodes — challenge rotation and 20/day cap (via [tower defense](../genres/tower-defense.md))
9. https://blox-fruits.fandom.com/wiki/Quests — one active quest, level-matched NPC quests (via [anime RPG](../genres/anime-rpg.md))
10. https://devforum.roblox.com/t/daily-weekly-quest-system/3178725 — daily/weekly reset by stored time, cross-server sync problem for shared quests
11. https://devforum.roblox.com/t/globally-synced-data/1523846 — same-for-everyone daily quest approaches
12. https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/API-Dump.json — AchievementService is RobloxScriptSecurity; deprecated badge methods

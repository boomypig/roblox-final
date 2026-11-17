---
title: Daily rewards and streaks
type: pattern
read-when: Adding daily login rewards, streaks, or timed gifts.
last-researched: 2026-10-22
---

# Daily rewards and streaks

## What it is

Three related systems, all server-timed and saved in the player's profile:

1. **Daily reward calendar:** one free claim per day. Rewards climb along a 7- or 28-step
   calendar.
2. **Streak:** a count of consecutive claim days, with a grace rule for missed days.
3. **Playtime gifts:** small rewards at set minutes of play today, such as 5, 10, 15 and 30 min.

They're a "come back tomorrow" hook, one of the 10 items on the
[retention](../fundamentals/retention.md) checklist. They only work on top of a core loop that is
already fun.

## Why it works

- **A small sure thing.** "Tomorrow there's a chest waiting" is an easy reason to open the game,
  and once in, the player usually plays (inferred).
- **Visible progress.** A calendar showing day 5 of 7, with the big day-7 reward drawn, gives a
  goal for the week (inferred).
- **It moves the signal Roblox ranks on.** Recommended for You counts **play days per user** in
  windows of Day 1, Days 2–7 and Days 8–28, among players it sent (official, 2026-10; see
  [discovery](../fundamentals/discovery-algorithm.md)).
  - A 7-step calendar targets days 2–7. A 28-step calendar, with milestones at days 14, 21 and
    28, targets days 8–28 (inferred).
  - The signal counts days *played*, not rewards claimed. The reward only gets them in the door
    (inferred).
- **Playtime gifts lengthen the first session.** The first-session bounce buckets are under
  60 s and 61–180 s (official), so a gift at minute 5 is seen by players who stayed past the
  danger zone. Discovery stops counting playtime after 60 min per day (official), so gifts
  past 60 min don't help ranking (inferred).
- **The risk is pressure.** A streak that wipes on one missed day turns a gift into a threat.
  About 35% of age-checked players are under 13 (official, 2026-06), and parents can set daily
  screen-time limits that end play for the day (official, 2026-10). Missed days are normal and
  often not the child's choice (inferred).

## Genres that use it

Almost every progression game: [simulator](../genres/simulator.md),
[tycoon](../genres/tycoon.md), [pet-egg](../genres/pet-egg-collection.md),
[farming](../genres/farming-growing.md), [RNG aura](../genres/rng-aura.md),
[anime RPG](../genres/anime-rpg.md), [tower defense](../genres/tower-defense.md),
[fishing](../genres/fishing.md). Lighter versions fit round-based and social games (a daily
cosmetic token). Pairs with [quests](quests.md) (daily and weekly quests share the same UTC
reset) and [idle/offline income](idle-offline-income.md).

## Design rules

### Day boundary: use UTC days

- `today = math.floor(os.time() / 86400)` is the UTC day number on every server (`os.time`
  defaults to UTC, official; arithmetic inferred). Store day numbers, not date strings.
- **Why UTC and not local time.** Local midnight needs the client's time zone, which the client
  controls. Spoof it and you get two claims a day.
  - UTC midnight falls at a fixed local hour: 8 pm EDT, 5 pm PDT, 1 am BST, 9 am JST. Show
    "Resets in 3h 12m" so the hour doesn't matter (inferred).
  - Daily quests and leaderboards then share one visible reset time (retention checklist item 4).
- **Don't use a rolling 24 h cooldown.** Someone who plays at 7 pm and then 6:30 pm the next day
  gets blocked, which feels like a bug. If you must use rolling time, use a 20 h cooldown and a
  48 h streak window (inferred).
- The client draws the countdown from `Workspace:GetServerTimeNow()`, not the device clock
  (official API; device clocks drift, community).
- Which day boundary Roblox analytics uses for "play days" isn't documented here (unverified).
  It doesn't change this design.

### Calendar and rewards

- **7-step weekly loop** for most games. Days 1–6 are small (currency, a spin, a boost). Day 7
  is a chest, egg or cosmetic worth about 3× a normal day. Then it loops (inferred).
- **Optional 28-step monthly track:** milestones at 7, 14, 21 and 28, with a cosmetic at 28.
  It covers the days 8–28 window (inferred).
- **The calendar advances on claims, not on the date.** A player who misses Tuesday gets day 3's
  reward on Wednesday instead of skipping it. Calendar rewards are never lost by being away
  (inferred; kid-friendly default).
- **Size:** a normal day's reward is worth about 5–10 minutes of play at the player's tier,
  scaled with a cap. Never make dailies the main income, or the game becomes "log in, claim,
  leave" (inferred).
- Show the next 7 rewards and today's state (claimable, claimed, locked) in one panel.
- At session end, tell the player what's next: "Tomorrow: Golden Egg" (retention stopping-point
  rule, inferred).
- Claiming is manual: a glowing HUD button plus a short chest-open animation (see
  [game feel](../../.claude/skills/roblox-vfx/references/game-feel.md)).
  - Don't auto-open a modal over a new player's first minutes. The day-1 claim can be an
    onboarding step instead (see [FTUE](../fundamentals/first-time-experience.md)).
  - Never pop it over active play.

### Streaks and missed days

| Rule | Kid-friendly option (default) | Harsher option (avoid) |
|---|---|---|
| Missed 1 day | Grace: 1 free missed day per UTC week, streak continues | Reset to 0 |
| Missed 2+ days | Step back to the last 7-day checkpoint (streak 17 → 14) | Reset to 0 |
| Away 7+ days | Welcome-back gift scaled to time away, capped; the calendar resumes where it was | Calendar and streak wiped |
| Streak repair | A free catch-up quest ("play 10 min today to restore") | Sell streak repair for Robux |
| What the streak affects | A badge, title or small cosmetic multiplier (+1% per 7 days, capped) | Core rewards or income |

- Wiping a long streak over one missed day is a retention anti-pattern. Use grace days, a capped
  catch-up and a welcome-back bonus instead (inferred, from [retention](../fundamentals/retention.md)).
- **Don't sell streak freezes or repairs.** That's paying to avoid a loss you created, aimed at
  children. Roblox's guidance already rules out false time pressure and Robux-skippable waits
  (official principle; rule inferred).
- Language: "Day 5! Come back tomorrow for the egg." Never "Don't lose your streak!" or
  "Last chance!" (official honest-copy guidance in [monetization](../fundamentals/monetization.md)).

### Claim windows

- One claim per UTC day. An unclaimed day doesn't pile up, but the calendar never skips ahead,
  so nothing is lost (inferred).
- The claim stays available all day. Don't use "claim in the next 2 hours" windows, which are
  false urgency (official anti-pattern).
- Crossing midnight mid-session: the server checks the day on each claim, and the client
  countdown re-enables the button at 00:00 UTC.

### Playtime gifts (timed gifts in a session)

- **Ladder:** gifts at 5, 10, 15, 30, 45 and 60 minutes of playtime *today*, each a little
  better. Stop at 60 min, where discovery stops counting (official cap; ladder inferred).
- **Count per UTC day, not per session.** If the timer resets on rejoin, players rejoin to farm
  the 5-minute gift. Save `{day, seconds, claimed}` (inferred).
- Show the next gift and its countdown in a small HUD widget. Players claim manually, so the
  gift is felt (inferred).
- Don't design around AFK. Roblox disconnects players after 20 minutes idle (official), so
  gifts reward active sessions anyway.
- Gifts are free. Don't sell "claim all gifts now" (a Robux-skippable timer, official
  anti-pattern).

### Notifications

- Rules: opt-in prompt only for 13+, once per 30 days; at most 1 notification per user per
  experience per day; must be personal and actionable; false time pressure and bait-and-switch
  rewards are banned (official, 2026-10; details in [retention](../fundamentals/retention.md)).
- Ask for opt-in at a moment that needs it: right after the first claim, with "Want a reminder
  when tomorrow's chest is ready?" Never ask on join (inferred).
- Send a daily-reward notification only when it's true and worth it: the reward is waiting,
  the player has claimed at least 2 days in a row, and nothing more personal (an egg hatched)
  is queued that day. Skip it if they've already played today (inferred).
- Wording names the real reward: "Your Day 7 Golden Egg is ready". Never "Your streak is about
  to end!" (official ban on false pressure; wording inferred).
- Under-13s can't opt in, so the in-game calendar has to work alone (official eligibility).

### Monetization boundaries

- Daily rewards and gifts are always free. A "2× daily rewards" pass is acceptable permanent
  value, if the free track is still worth claiming (inferred).
- Don't attach a Robux offer to the daily reward screen. Don't run "today only" prices that recur
  daily, which a University of Sydney study flagged as misleading (press, 2026-05; see
  [monetization](../fundamentals/monetization.md)).

## Implementation outline (server-authoritative)

- **Saved data** (session-locked profile, see [player data](player-data.md)):
  - `Daily = {lastDay, calendarDay, streak, bestStreak, graceWeek, graceUsed}`, all integers.
  - `Playtime = {day, seconds, claimed: {boolean}}`.
- **Remotes:** `ClaimDaily()` and `ClaimGift(index)` as RemoteFunctions returning
  `(ok, rewardInfo)`. Both are token-bucketed. The client never sends a day, a time or a
  reward (see [security](../../.claude/skills/roblox-code/references/security.md)).
- **Analytics:** after each grant, `AnalyticsService:LogEconomyEvent` with transaction type
  `TimedReward`, and a `LogCustomEvent` for `daily_claimed` with the streak (official API; see
  [analytics](../fundamentals/analytics.md)).

```lua
--!strict
-- ServerScriptService/DailyRewards.server.lua: OUTLINE, not drop-in
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local PlayerData = require(script.Parent.PlayerData) -- get() → nil until loaded

local DAY, GRACE_PER_WEEK, CHECKPOINT = 86400, 1, 7
local CALENDAR: {(data: any) -> ()} = require(script.Parent.DailyCalendar) -- 7 or 28 grant fns
local GIFT_AT: {number} = {300, 600, 900, 1800, 2700, 3600} -- seconds played today
local GIFTS: {(data: any) -> ()} = require(script.Parent.PlaytimeGifts) -- same length as GIFT_AT

local function utcDay(): number return math.floor(os.time() / DAY) end
local function grantWelcomeBack(data: any, daysAway: number) end -- fill in: capped gift

local ClaimDaily = ReplicatedStorage.Remotes.ClaimDaily :: RemoteFunction
ClaimDaily.OnServerInvoke = function(player: Player): (boolean, number?)
	-- token bucket here (roblox-code references/security.md)
	local data = PlayerData.get(player)
	if not data then return false, nil end
	local d, today = data.Daily, utcDay()
	local gap = today - d.lastDay
	if gap <= 0 then return false, nil end -- already claimed today (or clock skew)
	local week = math.floor(today / 7)
	if d.graceWeek ~= week then d.graceWeek, d.graceUsed = week, 0 end
	if gap == 1 or d.lastDay == 0 then
		d.streak += 1
	elseif gap == 2 and d.graceUsed < GRACE_PER_WEEK then
		d.streak += 1; d.graceUsed += 1 -- one missed day forgiven
	else
		d.streak = math.floor(d.streak / CHECKPOINT) * CHECKPOINT + 1 -- step back, not to zero
		if gap >= 8 then grantWelcomeBack(data, gap) end -- capped, scaled to time away
	end
	d.bestStreak = math.max(d.bestStreak, d.streak)
	d.lastDay = today
	d.calendarDay += 1 -- advances per claim, never skips
	CALENDAR[(d.calendarDay - 1) % #CALENDAR + 1](data)
	return true, d.calendarDay
end

-- Playtime gifts: accumulate per UTC day on the server.
task.spawn(function()
	while true do
		task.wait(5)
		local today = utcDay()
		for _, p in Players:GetPlayers() do
			local data = PlayerData.get(p)
			if data then
				local pt = data.Playtime
				if pt.day ~= today then pt.day, pt.seconds, pt.claimed = today, 0, {} end
				pt.seconds = math.min(pt.seconds + 5, GIFT_AT[#GIFT_AT])
			end
		end
	end
end)

local ClaimGift = ReplicatedStorage.Remotes.ClaimGift :: RemoteFunction
ClaimGift.OnServerInvoke = function(player: Player, index: unknown): boolean
	if typeof(index) ~= "number" or index % 1 ~= 0 or index < 1 or index > #GIFT_AT then return false end
	local data = PlayerData.get(player)
	if not data then return false end
	local pt = data.Playtime
	if pt.day ~= utcDay() or pt.claimed[index] or pt.seconds < GIFT_AT[index] then return false end
	pt.claimed[index] = true
	GIFTS[index](data)
	return true
end
```

Notes:

- Calendar position and streak live in the same profile as the rewards they grant, so they save
  together. A crash before a save loses both, and the player claims again (inferred).
- `pt.claimed` is an array of booleans indexed 1..6. Fill it as `{false, false, …}` in the
  template, because DataStores reject gapped arrays (official; see
  [player data](player-data.md)).
- Seconds add up only while the profile is loaded. Rejoining doesn't reset them, because the day
  key does the reset.

## Common bugs and exploits

| Bug or exploit | Fix |
|---|---|
| Two claims a day by changing the device clock or time zone | Server `os.time()` UTC day only; the client sends nothing time-related |
| Double claim from two quick requests | The `lastDay == today` check and the update happen with no yield between them; add a token bucket |
| Rejoin farming of playtime gifts | Accumulate per UTC day in saved data, not per session |
| Streak wiped by a screen-time limit or a weekend away | Grace day per week, checkpoint step-back, calendar advances per claim |
| Claim lost because data wasn't loaded | Refuse while `PlayerData.get` is nil; the button shows "Loading…" |
| Countdown wrong on some devices | `Workspace:GetServerTimeNow()` on the client |
| Gapped `claimed` array fails to save | Fixed-length boolean array in the template, or a string-keyed map |
| Reward shown differs from reward granted | The client calendar is a display copy of the server table; the server returns what it granted |
| Notification sent when nothing is waiting | Check the claim state at send time; at most one per day; skip if they played today |
| Daily modal blocks a new player's first minute | No auto-modal in the first session; the HUD button glows instead |

## Checklist for agents

- [ ] UTC day number from `os.time()` on the server; reset countdown shown from
      `Workspace:GetServerTimeNow()`.
- [ ] 7-step calendar (optional 28-step track) that advances per claim and never skips or
      wipes.
- [ ] Streak with 1 grace day per week, checkpoint step-back, a welcome-back gift; affects only
      cosmetics or small capped bonuses.
- [ ] No paid streak repair, no Robux skip on timers, no offer on the claim screen, no
      "last chance" copy.
- [ ] Playtime gifts at 5/10/15/30/45/60 min of playtime *today*, saved per UTC day, capped at
      60 min.
- [ ] Remotes take no time or reward arguments; token-bucketed; refuse until data loads.
- [ ] Opt-in prompt after the first claim (13+ only); at most one true, specific daily-reward
      notification.
- [ ] `TimedReward` economy events and a `daily_claimed` counter logged after grants.

## Sources

1. https://create.roblox.com/docs/discovery — play days per user (D1, D2–7, D8–28), 60-min playtime cap, bounce buckets
2. https://devforum.roblox.com/t/recommended-for-you-algorithm-improvements-that-better-value-long-term-retention/4684575 — 28-day window (2026-06)
3. https://create.roblox.com/docs/cloud-services/experience-notifications — opt-in rules, 1 per user per day, banned dark patterns
4. https://create.roblox.com/docs/production/monetization — no fake urgency or restarting countdowns; Robux-skippable timers disliked; neutral copy for minors
5. https://create.roblox.com/docs/reference/engine/libraries/os — os.time defaults to UTC
6. https://create.roblox.com/docs/reference/engine/classes/Workspace — GetServerTimeNow
7. https://devforum.roblox.com/t/os-time-consistency/453603 — device clocks differ from the server
8. https://create.roblox.com/docs/reference/engine/classes/Player — Idled; 20-minute idle disconnect
9. https://about.roblox.com/parental-controls — daily screen-time limits for Kids and Select 9–12
10. https://www.sec.gov/Archives/edgar/data/0001315098/000162828026051059/ex991-robloxq22026earnin.htm — age mix of age-checked users (Q2 2026)
11. https://create.roblox.com/docs/reference/engine/classes/AnalyticsService — LogEconomyEvent, TimedReward transaction type, LogCustomEvent
12. https://www.sydney.edu.au/news-opinion/news/2026/05/17/inside-the-pay-to-play-world-of-roblox-targeting-children-.html — recurring "daily discounts" flagged as misleading

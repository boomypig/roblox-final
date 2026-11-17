---
title: Live ops and updates
type: fundamental
read-when: Planning updates, events, limited-time content, or codes.
last-researched: 2026-10-22
---

# Live ops and updates

## In one line

Ship on a fixed, sustainable weekly slot. Pre-deploy content behind experience configs and flip
it live at the slot. Move players to new servers with delayed restarts and
`ServerRestartScheduled`, not hard shutdowns. Use events to sync attendance without faking
scarcity or breaking the economy.

## Cadence: what Roblox and the top games do (dated)

- **Roblox's advice:** "A weekly cadence for updates is ideal," with monthly as the bare
  minimum. Theme each update, let players earn access to new content, and use limited-time
  items to create excitement (official, 2026-10).
- **Updates feed recommendations.** RFY's explore phase often shows a spike of new users from
  recommendations after a content update. If that cohort engages and spends, the game is shown
  to more similar users (official, 2026-10). See [discovery](discovery-algorithm.md).
- **Grow a Garden** shipped a new update every Saturday from launch at 14:00 UTC (10:00 EDT).
  Its "admin abuse" event usually ran about an hour before the drop (press, Sportskeeda 2025).
  Named weekly updates drove each of its peaks (press, see [trend lifecycle](trend-lifecycle.md)).
- **Even the leader found weekly events unsustainable.** In 2025-08 its creator said weekly
  events had become too hard to keep fresh. He moved the focus to deeper farm systems and kept
  events as a side feature (press, NME 2025-08-12).
- **Steal a Brainrot's** biggest days were events (admin war 2025-08-23, "Extinct Event"
  2025-09-13) (press, via [trend lifecycle](trend-lifecycle.md)).
- Games that stop updating fade within weeks (community, via [trend lifecycle](trend-lifecycle.md)).

**Takeaway** (inferred): at small scale, ship a small update every week and a bigger themed
drop every 3–5 weeks. A "weekly update" can be a balance pass, one new item, or an event
toggled through config. It doesn't have to be a new zone.

## Timing: day, hour, countdowns

- **Pick one fixed weekly slot and keep it.** Saturday at 14:00–15:00 UTC (morning in the US,
  afternoon in Europe) is the slot the 2025 hits used (press, Sportskeeda 2025). Store the time
  as UTC in code. Show local time on the client with `DateTime:FormatLocalTime` (official API).
  Daylight saving moves the US-local time, so decide which zone you anchor to (inferred).
- **Countdowns concentrate players.** Admin events "concentrate players into the same window,"
  which spikes concurrency (press, Tubefilter 2025-08-25). Combine (inferred):
  1. an in-game countdown board (lobby sign plus HUD chip) driven by a config timestamp;
  2. an **Experience Event** so offline players get "Notify Me" alerts at the start (below);
  3. an update announcement in the 60-character slot;
  4. a personalized Experience Notification ([retention](retention.md)).
- **Release with configs, not a Saturday publish.** Roblox's update guide says: for
  time-sensitive updates, publish early, hide new content behind a config, and flip the config
  to release (official, 2026-10). That way the code has been live and tested on real servers
  for a day before anyone sees it.

## Experience configs and experiments (the live-ops control panel)

- **What it does:** `ConfigService` gives server scripts key/value configs (string, number,
  boolean, JSON) that you edit in Creator Hub or Studio (File > Open Configs) without
  republishing (official, 2026-10). It's the tool for:
  - feature toggles and event start times;
  - drop rates, boss HP and prices (prices only for soft currency; Robux prices live on the
    product);
  - limited-time content.
- **Limits:** up to 1,000 active configs; strings and JSON up to 100,000 characters (official).
- **Publishing:** "Publish now" reaches servers in roughly 15 s–1 min. "Publish over 15 min"
  is a gradual rollout (official). Changes are staged first, and you can test them in Studio
  play sessions.
- **Snapshots don't update themselves.** `ConfigService:GetConfigAsync()` returns a
  `ConfigSnapshot`, and edits don't change an existing snapshot (official).
  - Connect `ConfigSnapshot.UpdateAvailable` to `ConfigSnapshot:Refresh()`, then react with
    `ConfigSnapshot:GetValueChangedSignal(key)`.
  - Refresh between rounds if mid-match changes would be unfair (official).
- **Errors:** if configs never loaded, `GetConfigAsync` throws, so wrap it in `pcall` and keep
  code defaults (official). Client scripts can't call `ConfigService`; replicate the values
  yourself.
- **Per-player values:** `ConfigService:GetConfigForPlayerAsync(player)` applies conditional
  values and experiments (official). Targeting covers country, language, new vs returning,
  source, tenure, payer status, engagement and platform spender status. Limits: 100 conditions
  per game, 20 per key (official).
- **History and testing:** History shows every change and can restore an old value.
  `ConfigService:SetTestingValue` overrides a value for testing, in Studio or live (official).
  "Publish As" copies configs from a staging experience to the live one (official).
- **Experiments:** A/B tests on config values, running 14–60 days with up to 2 variants plus a
  control. They report playtime, retention, payer conversion and ARPU (official, 2026-10). Use
  them for onboarding, pricing displays and drop rates. Small games may not reach significance;
  check the minimum detectable effect the tool shows (inferred).

## Shipping a new version: server restarts and migration

- **Publishing doesn't move players.** Running servers keep the `game.PlaceVersion` they
  started with (official).
- **Restart only outdated servers:** Creator Hub > Configurations > Server management >
  Restart Servers, choosing "Restart only servers with outdated versions" (official, 2026-10).
- **Use a delayed restart (bleed-off) of 1–60 minutes** (official):
  - Matchmaking stops sending new players to marked servers. Friends, invites and teleports
    still reach them.
  - At the deadline Roblox automatically teleports everyone to a replacement server on the new
    version. Players from the same old server land on the same new server.
- **Data format changes:** restart whenever the save format changes, so old servers can't write
  old-format data. Version your saves ([player data](../patterns/player-data.md)) (official +
  inferred).
- **`DataModel.ServerRestartScheduled(restartTime, source, attributes)`:**
  - Fires on every affected server when a *delayed* restart is scheduled. Immediate restarts
    send no notice (official, DevForum 2026-06-18).
  - Delivery is best-effort, usually within 1–2 s, with 99.9% success (official).
  - `source` is `Enum.CloseReason.DeveloperUpdate` for your restarts and `RobloxMaintenance`
    for Roblox's. `attributes` carries a custom payload you set when confirming the restart.
- **`game:BindToClose`:** all bound functions together get 30 s, run in parallel, and receive a
  `CloseReason` (official). Use it to save data, not to migrate players. Developers report
  teleports from `BindToClose` landing players in the start place instead of a sub-place
  (community, DevForum 2025). Prefer delayed restarts over a homemade soft-shutdown script
  (inferred).
- **Fully stopping play:** to keep players out, revoke public access. Restarting alone lets
  them reconnect (official).

```lua
--!strict
-- Server: warn players, finish the current round, then move everyone to a new-version server.
local Players = game:GetService("Players")
local TeleportService = game:GetService("TeleportService")
local Remotes = game:GetService("ReplicatedStorage"):WaitForChild("Remotes")
local RestartNotice = Remotes:WaitForChild("RestartNotice") :: RemoteEvent
local Round = require(script.Parent.Round) -- isRunning(): boolean, Ended: signal

local moving = false
local function moveEveryone()
	if moving then return end
	moving = true
	local players = Players:GetPlayers()
	if #players == 0 then return end
	-- Same PlaceId: matchmaking picks a server on the latest version. Saves run on PlayerRemoving.
	local ok, err = pcall(function()
		TeleportService:TeleportAsync(game.PlaceId, players)
	end)
	if not ok then
		warn("Restart teleport failed:", err)
		moving = false -- Roblox still migrates everyone at restartTime
	end
end

game.ServerRestartScheduled:Connect(function(restartTime: DateTime, source: Enum.CloseReason, attributes: {[string]: any})
	-- Client shows a countdown with DateTime.fromUnixTimestamp(t):FormatLocalTime("LT", locale)
	RestartNotice:FireAllClients(restartTime.UnixTimestamp, source.Name, attributes.message)
	if Round.isRunning() then
		Round.Ended:Once(moveEveryone) -- never yank players mid-round
	else
		task.delay(10, moveEveryone)
	end
end)
```

## Events

### Limited-time and seasonal content

- Theme it, give it a start and end, and make rewards earnable by playing. Roblox endorses
  limited-time items for excitement, but bans false scarcity and fake or restarting timers
  (official; see [monetization](monetization.md)).
- **Seasonal hooks** (inferred): Halloween, winter holidays, Lunar New Year, Easter, summer
  break. Plan art 2–3 weeks ahead, and run each event for 1–4 weeks with weekly parts so the
  update cadence carries through.
- **Server-wide events** (weather, meteor showers, admin abuse) are social draws in their own
  right. See [admin abuse](../patterns/server-events-admin-abuse.md) and
  [social](social-and-virality.md).
- **Roblox-wide events:** the Home "Live Events" sort lists games in limited-time events where
  players complete quests for rewards (official, 2026-10). The 2026-09 "The Hunt: Roblox 20"
  featured the most popular game from each year of Roblox's history, plus 20 "Year Infinity"
  games (press, GamesBeat 2026-09-16). Roblox picks the participants; no public application
  was found (unverified). Treat these as a bonus, not a plan.

### Experience Events (the Events & Updates feature)

- **Where:** Creator Dashboard > Engagement > Events & Updates. Up to **10** ongoing or
  upcoming events per game. Events appear on the game page ("Join Event" or "Notify Me"), on a
  shareable event page, and in the group's Events tab (official, 2026-10).
- **Alerts:** "Notify Me" sends an inbox notification when the event starts, with optional
  push (official).
- **Trending:** the "Trending Events in Experiences" chart needs **≥1,000 RSVPs** and a start
  within the last 7 days (official).
- **Off-Platform Featuring:** submit ≥7 days before the start. Roblox recommends events of
  7–30 days (official).
- **In-game:**
  - `SocialService:GetUpcomingExperienceEventsAsync()` finds event IDs at runtime; don't
    hard-code them.
  - `SocialService:PromptRsvpToEventAsync(eventId)` and
    `SocialService:GetEventRsvpStatusAsync(eventId)` (returns `Enum.RsvpStatus`) only work
    before the event starts.
  - `Player:GetJoinData().GameJoinContext.EventId` shows who joined through an event, so you
    can greet them with an event-specific prompt (official).
- Pattern (inferred): put an "RSVP for Saturday's event" button on the countdown board.

### Update announcements and notifications

- Update announcements are capped at **60 characters**, and you can post at most **once every
  3 days**. They go to players who turned on notifications for your game (official).
- Be concrete ("New Volcano zone + 5 lava pets"), not "bug fixes" (official guidance).
- Experience Notifications allow 1 per user per game per day, and personalized ones are 13+
  only. Rules and APIs: [retention](retention.md).

## Codes, update logs, and title tags

- **Codes:** release one with each update and announce it in the update log and on social
  channels. Expire them and validate on the server. See [codes](../patterns/codes.md).
- **In-game update log** (inferred):
  - Show a "What's new" panel once per version: store the last seen version in player data and
    compare it to a version string you set (in a config or in code).
  - List 3–6 bullets, put the newest first, and include the active code.
- **"[UPDATE]" title tags:**
  - Roblox's own name rules (official): keep the name consistent, because frequent renames
    hurt search by old name; one or two emojis are fine; repeated words can get the game
    demoted.
  - Editing the title marks the game as "Updated" even when only metadata changed (community,
    DevForum 2025).
  - If you use a prefix tag, use it only for a real update that week, remove it after about 7
    days, and never change the base name (inferred).
  - See [metadata](metadata-thumbnails-icons.md).

## A sustainable cadence for a solo developer (inferred)

- **Bank content before launch.** Have 3–4 small updates and 1 themed drop built or
  designed, so a bad week doesn't break the streak.
- **Make content data-driven.** Items, eggs, quests and drop tables live in ModuleScripts and
  configs, so a weekly update is data plus art, not new systems.
- **Weekly rhythm:**
  - Mon–Wed: build.
  - Thu: test in a staging copy, then "Publish As" its configs to live.
  - Fri: publish the place with new content hidden; restart outdated servers with a 15–30 min
    delay.
  - Sat at the slot: flip the config, post the announcement, run a short admin event.
  - Sun: read analytics and the feedback inbox.
- **Monthly:** one larger themed drop, and one week off-cycle that's only polish and fixes,
  announced as such.
- **Measure each update** against the previous four weekly slots: peak CCU, D1 of new users,
  and spend days ([analytics](analytics.md)). Cut event types that don't move them.
- **Cap the work:** if an update needs more than about 20 focused hours, split it. A missed
  slot costs more than a smaller update.

## Live-ops anti-patterns (reviewer: reject these)

- **Burnout cadence:** weekly *events* that each must top the last. The top game in 2025 called
  this unsustainable (press, NME 2025-08-12).
- **Constant FOMO:** overlapping timed events, restarting countdowns, "last chance" banners every
  login. These are banned or discouraged by Roblox's monetization rules (official) and hard on a
  young audience.
- **Economy breaks:**
  - Event currency that converts into main currency without a cap.
  - Each update's items making the last ones worthless (power creep).
  - Re-releasing "limited" items, which betrays collectors and trading prices.
  - Duplication exploits during events. Validate grants on the server and log them
    ([security](security-and-anti-exploit.md)).
- **Paid perks changed without notice.** Removing functionality buyers paid for without proper
  notice counts as a scam (official, Community Standards).
- **Hard shutdowns mid-round** or immediate restarts at peak time. Use delayed restarts and move
  players between rounds.
- **A Saturday publish with untested code.** Publish early with content hidden, and keep a
  rollback: restore config values from History (official), plus the previous place version from
  version history (unverified UI path).
- **Notification spam:** generic "come back!" messages. Delivery drops when engagement drops
  (official; [retention](retention.md)).

## Checklist for agents

### Do
- Define the weekly slot (UTC) and the first 4 updates before launch.
- Put event start/end times, drop rates and feature toggles in `ConfigService` configs. Refresh
  snapshots on `UpdateAvailable` and keep code defaults behind a `pcall`.
- Handle `game.ServerRestartScheduled`: countdown UI, then `TeleportService:TeleportAsync` to
  `game.PlaceId` between rounds.
- Save in `game:BindToClose` (30 s budget). Restart outdated servers whenever the save format
  changes.
- Create an Experience Event for every scheduled event, with an in-game RSVP button and an
  `EventId` greeting.
- Ship a "What's new" panel and a code with each update.

### Don't
- Hard-code event dates in place files you'd have to republish to change.
- Use immediate restarts or homemade `BindToClose` teleport soft-shutdowns as the main
  migration path.
- Run overlapping timed events, restarting timers, or re-released "limited" items.
- Rename the game every week or stack tags and emojis in the title.
- Promise a cadence you can't sustain for six months.

## Related

- [Retention](retention.md) (notifications, return reasons), [discovery](discovery-algorithm.md)
  (explore/expand after updates), [analytics](analytics.md)
- [Social](social-and-virality.md) (admin events as social draws), [monetization](monetization.md)
  (honest timers, scarcity)
- [Codes](../patterns/codes.md), [admin abuse](../patterns/server-events-admin-abuse.md),
  [daily rewards](../patterns/daily-rewards-and-streaks.md), [player data](../patterns/player-data.md)
- [Trend lifecycle](trend-lifecycle.md) (what drove the 2025 peaks),
  Grow a Garden (case study: grow-a-garden)

## Sources

1. https://create.roblox.com/docs/production/monetization — "weekly cadence is ideal", monthly minimum, limited-time content guidance
2. https://create.roblox.com/docs/discovery — explore/expand after content updates, Live Events sort
3. https://create.roblox.com/docs/projects/update-games — restart outdated servers, 1–60 min delay, auto-teleport, configs for timed releases
4. https://devforum.roblox.com/t/introducing-restart-notifications/4690885 — ServerRestartScheduled delivery, payloads, sample (2026-06-18)
5. https://create.roblox.com/docs/reference/engine/classes/DataModel — BindToClose 30 s, CloseReason, ServerRestartScheduled, PlaceVersion
6. https://devforum.roblox.com/t/gamebindtoclose-teleports-do-not-work-on-soft-shutdown-or-server-restart/4003952 — BindToClose teleport problems
7. https://create.roblox.com/docs/production/configs — experience configs, limits, publish timing, targeting, history, testing
8. https://create.roblox.com/docs/reference/engine/classes/ConfigService — GetConfigAsync / GetConfigForPlayerAsync behavior
9. https://create.roblox.com/docs/production/experiments — A/B experiments, 14–60 days, metrics
10. https://create.roblox.com/docs/production/promotion/experience-events — events limits, RSVPs, trending threshold, GameJoinContext.EventId, update announcements
11. https://create.roblox.com/docs/reference/engine/classes/SocialService — event and RSVP APIs
12. https://create.roblox.com/docs/production/publishing/publishing-experiences-and-places — game name rules
13. https://devforum.roblox.com/t/dont-mark-games-as-updated-when-altering-metadata/4069658 — metadata edits mark games "Updated"
14. https://www.sportskeeda.com/roblox-news/when-next-grow-garden-update — Grow a Garden Saturday 14:00 UTC cadence, admin abuse before drops
15. https://www.nme.com/news/gaming-news/roblox-grow-a-garden-major-changes-coming-update-cooking-3884432 — weekly events "too hard to keep fresh" (2025-08-12)
16. https://www.tubefilter.com/2025/08/25/roblox-grow-garden-steal-brainrot-admin-war-record/amp/ — admin events concentrate players into one window
17. https://gamesbeat.com/roblox-launches-20th-anniversary-event-the-hunt-roblox-20/ — The Hunt: Roblox 20 (2026-09)
18. https://about.roblox.com/community-standards — removing paid functionality without notice

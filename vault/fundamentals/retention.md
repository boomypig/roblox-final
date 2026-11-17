---
title: Retention
type: fundamental
read-when: Designing session goals, return reasons, or reading D1/D7/D28 numbers.
last-researched: 2026-10-22
---

# Retention

## In one line

Retention is the share of new players who come back on later days. On Roblox it is the main
health metric and, through "play days per user" over D1 / D2–7 / D8–28, a direct Home
recommendation signal. Every game must give a concrete reason to return tomorrow and next week.

## Definitions: use Roblox's, not generic ones

| Term | Where it appears | Definition | Notes |
|---|---|---|---|
| D1 retention | Creator Analytics > Retention | Share of new users who return the day after their first play | (official, 2026-10) |
| D7 retention | Creator Analytics | Share of new users who return on day 7, the 8th calendar day | (official, 2026-10) |
| D30 retention | Creator Analytics | Share of new users who return on day 30, the 31st day | (official, 2026-10) |
| Play days per user, D1 / D2–7 / D8–28 | Discovery (Recommended for You) | Average unique days played in each window, counting only users who joined organically from the Home sort | (official, 2026-10) |
| Intentional co-play days | Discovery | Average unique days users come back to play *with friends* (join, invite, private server) | (official, 2026-10) |
| Playtime per user | Discovery | Average time in game, capped at 60 min per user, per game, per day | (official, 2026-10) |

- Creator Analytics retention is **exact-day**: D7 counts a return on day 7 itself. Discovery
  counts **unique days inside a window**, so a player who skips day 7 but plays days 5 and 9 still
  helps D2–7 and D8–28 (official definitions; the comparison is inferred).
- "D28" in this vault means the discovery window (days 8–28). "D30" means the analytics retention
  chart. Don't compare the two directly (inferred).
- Cohorts are grouped by first play date. Daily cohorts show 10 days, weekly cohorts show 10 weeks.
  D7 data arrives 7 days late and D30 data 30 days late (official, 2026-10).
- Since 2025-10-16, D1/D7/D30 can be split by acquisition source. Players from "Other" (external
  links) retain worse than players from Home recommendations, so a shift in traffic mix can lower
  D1 without any change to the game (official, 2025-10).
- A large influx of new users usually lowers D1/D7/D30 for a while. Roblox calls this typical and
  temporary (official, 2026-10).
- In June 2026 the Recommended for You window grew from 7 to 28 days and now weighs D8–28 play
  days. This is why week-2-to-4 return reasons now affect distribution, not just revenue
  (official, 2026-06). Details: [discovery](discovery-algorithm.md).

## Benchmarks (all dated; none are official targets)

Roblox publishes no platform-wide retention median. Your Creator Analytics benchmark scorecard
shows the **50th–90th percentile** of "similar experiences" (what your players also play) or of
your genre. You can switch between the two sets. Benchmarks are for comparison only and do not
feed the algorithm (official, 2025-10).

- **Roblox docs example only:** a D1 band of 12.11%–18.73% means half of similar games are at or
  below 12.11% and 10% are at or above 18.73% (official, 2026-10). It is an illustrative example,
  not a published benchmark.
- **GameAnalytics 2025 Roblox report**: game-level percentiles from Jan 2023 to Jul 2025, covering
  games that make up about 47% of Roblox engagement (press, 2025):

| Avg session length | D1 p50 | D1 p75 | D1 p90 | D7 p50 | D7 p90 | D30 p50 | D30 p90 |
|---|---|---|---|---|---|---|---|
| 0–3 min | 4.3% | 7.4% | 9.3% | 0.4% | 1.8% | 0.13% | 0.6% |
| 4–6 min | 6.2% | 8.6% | 11.7% | 0.9% | 2.4% | 0.28% | 0.8% |
| 7–12 min | 7.9% | 9.8% | 11.6% | 0.9% | 2.0% | 0.24% | 0.8% |
| 13–18 min | 10.2% | 12.2% | 15.0% | 1.2% | 2.7% | 0.34% | 1.0% |
| 19–24 min | 11.5% | 13.6% | 18.2% | 1.6% | 5.2% | 0.46% | 1.4% |
| 25+ min | 10.8% | 12.3% | 18.9% | 1.8% | 5.9% | 0.50% | 1.5% |

- Same report, platform-wide (2025): median daily playtime per user is 16.8 min, p75 34.6 min and
  p90 64.9 min. Median average session is 6.6 min and p90 is 26.4 min (press, 2025).
- Retention rises with session length up to the 19–24 min tier, then levels off. The report calls
  25+ min "essentially the plateau" (press, 2025).
- Community data point: a game at 5.22% D1 sat at the 49th percentile of its Roblox benchmark set
  (community, 2024-12). This fits the GameAnalytics medians.
- "Aim for 20–25% D1" is often repeated on forums but has no traceable source (unverified).

**Vault targets for our games (inferred from the table above, about the p75 of the 13–24 min tiers):**

| Grade | D1 | D7 | D30 |
|---|---|---|---|
| Not ready (fix the first session first) | < 6% | < 0.8% | < 0.2% |
| Median, so iterate | 6–11% | 0.8–1.6% | 0.2–0.45% |
| Good, so scale up ads/updates | ≥ 12% | ≥ 2% | ≥ 0.5% |
| Top decile | ≥ 18% | ≥ 5% | ≥ 1.4% |

GameAnalytics' retention definitions may not match Roblox's exactly. Treat any gap under about 2
points as noise and trust your own benchmark scorecard first (inferred).

## What brings players back

Different time horizons need different hooks. Roblox's own guidance: D1 depends on the core loop,
the first session (FTUE) and performance. D7 depends on progression and variety. D30 depends on
regular updates and social systems (official, 2026-10).

### Tomorrow (D1)

- **A visible, unfinished goal at the moment they leave.** Show the next unlock and how close it
  is, such as "2 more eggs to complete the set". Roblox recommends short, mid and long-term goals
  that are visible in the world or UI (official, 2026-10).
- **Something finishes while they're away.** Crops, hatching, restocks or offline income that
  wait to be *claimed* on return (inferred). See
  [idle/offline income](../patterns/idle-offline-income.md). The timer has to *produce*
  something. Roblox says timers that block play and can be skipped with Robux put Roblox players
  off (official, 2026-10).
- **Daily reward or streak** with a grace rule. See
  [daily rewards and streaks](../patterns/daily-rewards-and-streaks.md).
- **Friends.** Intentional co-play days are a discovery signal (official, 2026-10). Reward bringing
  a friend and returning together. See [social and virality](social-and-virality.md).
- **A notification about something that matters to them**, such as "your egg hatched" or "a
  friend beat your score". See Experience Notifications below.

### Next week (D2–7)

- **Progression with variety:** new modes, items and social features, with difficulty tuned so
  players neither run out of content nor hit a wall. Track how many players sit at each
  progression level (official, 2026-10).
- **Weekly resets:** weekly quests and leaderboard seasons (inferred). See
  [quests](../patterns/quests.md) and [leaderboards](../patterns/leaderboards.md).
- **Scheduled moments:** events with "Notify Me" RSVPs, restock times and admin-abuse hours
  (official for the events feature, the rest inferred). See
  [server events](../patterns/server-events-admin-abuse.md).
- **A social reason:** a pending trade, a team that needs them, a friend's base to visit
  (inferred).

### Next month (D8–28 / D30)

- **Long-term goals:** collections, rebirth/prestige, mastery and rare items with social status
  (official for goals in general, inferred for the specific systems).
- **Social systems:** trading, parties, guilds, PvP, tournaments and leaderboards (official,
  2026-10).
- **Update cadence:** Roblox suggests small updates every 2–4 weeks and bigger feature updates every
  2–3 months (official, 2026-10). See [live ops](live-ops-and-updates.md).

## Session design

- **Aim for a 15–25 min average session.** Retention climbs with session length up to about 19–24
  min and then flattens (press, 2025). Discovery stops counting playtime after 60 min per user per
  day (official, 2026-10). Past about 60 min, an extra *day* is worth more than extra minutes
  (inferred).
- **Build natural stopping points:** end of a round, a harvest, a boss kill, a full inventory. At
  each one, show (a) what they earned, (b) the next goal, and (c) what will be ready next time
  (inferred).
- **Use "one more" loops on purpose:** short repeatable loops of 30 s to 3 min, each ending in a
  reward. Let a session end on a *started* goal, not a finished one (inferred).
- **Don't depend on AFK.** Roblox disconnects players idle for 20+ minutes. `Player.Idled` fires
  after about 2 minutes idle (official, 2026-10). Use offline progress, not "stay in the server"
  progress (inferred).
- **Expect sessions to end suddenly.** Parents can set daily screen-time limits for all Kids users
  and for Select users aged 9–12. Once the limit is hit, the child can't play for the rest of the day
  (official, 2026-10). Mobile apps also get killed in the background. Save on every meaningful
  change (see [player data](../patterns/player-data.md)) and never punish a mid-round quit with
  lost progress (inferred).
- Keep the core fun available from minute one. Roblox's engagement guidance says to give reasons
  to return "without gating off the fun" (official, 2026-10).

## Experience Notifications (current rules, verified 2026-10)

Experience Notifications are push and in-app notifications from your game to opted-in players.
They are the only direct "come back" channel you control (official, 2026-10).

- **Opt-in APIs** (in a LocalScript): `ExperienceNotificationService:CanPromptOptInAsync()` (it yields,
  so wrap it in `pcall`), then `ExperienceNotificationService:PromptOptIn()`. Listen to
  `ExperienceNotificationService.OptInPromptClosed` (official, 2026-10).
- **Who can be prompted:** users 13+ who haven't already opted in and haven't seen the prompt in
  the last 30 days. The prompt text is standard and can't be changed (official, 2026-10).
- **Game eligibility:** at least 100 visits and not under moderation (official, 2026-10).
- **Strings:** create them in Creator Dashboard > Engagement > Notifications. Each is at most 99
  characters with `{parameters}`. `{experienceName}` is available, and the game title becomes the
  notification title (official, 2026-10).
- **Sending (server):** use the Open Cloud Luau package's `OpenCloud.V2.UserNotification`
  `createUserNotification(userId, notification)` with `messageId` (the string's asset ID) and
  `type = "MOMENT"`. Optional `joinExperience.launchData` holds up to 200 bytes, which you read with
  `Player:GetJoinData()` on arrival (official, 2026-10).
- **Limits:** at most 1 per user per experience per day, plus an unpublished daily cap across all
  games. Delivery isn't guaranteed, and games with higher engagement get more delivered
  (official, 2026-10).
- **Analytics:** opted-in users, impressions, clicks, CTR, turn-off rate and dismiss rate, shown
  once you reach 100 impressions. To A/B test, create a new string instead of editing an old one
  (official, 2026-10).
- **Banned:** requiring opt-in to play or progress, disguised ads, false time pressure,
  bait-and-switch rewards and tricking players into purchases (official, 2026-10).
- **Good messages are personal and actionable.** Roblox's own examples: an egg hatched, a friend
  beat your record, "2 races away" from the weekly challenge (official, 2026-10).

**When to prompt (inferred):** you get one prompt per player per 30 days, so use it at a moment
that needs a future notification. Good moments: right after they start a timer ("Notify me when
my crops are ready?"), after they set a record a friend could beat, or after they RSVP to an event.
Never prompt on join or during the first 3 minutes.

### Other return channels

- **Events:** create time-based events on the game page. Players who tap "Notify Me" get an
  inbox notification when the event starts. You can have at most 10 ongoing or upcoming events.
  Trending Events needs 1,000+ RSVPs within the first 7 days. In game, use
  `SocialService:PromptRsvpToEventAsync(eventId)` and
  `SocialService:GetUpcomingExperienceEventsAsync()` (official, 2026-10).
- **Update announcements:** at most 60 characters, once every 3 days, sent to everyone who turned
  on notifications for your game. The stats include unfollow rate, so don't spam (official,
  2026-10).
- **Friend invites:** `SocialService:CanSendGameInviteAsync()` then
  `SocialService:PromptGameInvite(player, options)` with `ExperienceInviteOptions.LaunchData`
  (up to 200 characters). The invited friend reads it with `Player:GetJoinData()`, which can take a
  few seconds to arrive, so retry (official, 2026-10).
- **Moments:** short gameplay clips with a one-tap Join button. They are a Home tab rolling out
  globally from 2026-07-28, for age-checked users 16+ (official, 2026-07). Clip-worthy moments in
  your game feed this channel (inferred). See [social and virality](social-and-virality.md).

## Anti-patterns (reviewer: reject these)

About 35% of age-checked Roblox players are under 13 and 38% are 13–17 (official, 2026-06), so
pressure tactics land on children. Several are explicitly disallowed:

- **Fake urgency:** countdowns that are inaccurate or restart for the same item, and "almost
  sold out" or "short time only" claims that aren't true. Roblox's monetization docs say not to
  do either (official, 2026-10).
- **Robux-skippable waiting:** appointment timers you can pay to remove or bring forward. Roblox
  says its players dislike their fun ending early (official, 2026-10).
- **Punishing absence:** wiping a long streak on one missed day, decaying bases, pets that "run
  away", or losing crops. One missed day then means a *permanent* loss, which is a reason to quit
  (inferred). Use grace days, a capped catch-up, and a "welcome back" bonus instead.
- **Daily-discount theater:** "today only" prices that recur daily so the discount looks like the
  default. This was flagged as misleading in a University of Sydney study of 15 Roblox games, 14 of
  which used spending pressure (press, 2026-05).
- **Notification abuse:** generic ads, fake "your reward is waiting" when nothing is waiting, or
  sending every day without a reason. These are banned, and turn-offs reduce reach (official,
  2026-10).
- **Gating the core loop behind a daily limit** such as "3 plays per day" or energy bars. This
  cuts session length, and session length tracks D1 (press, 2025; the link is inferred).
- **Requiring friends to progress** solo past the tutorial. Make co-op a bonus, not a gate,
  because many players can't chat (see [audience](audience.md)) (inferred).

## Reading your retention numbers

1. **Check data volume and lag.** Ignore cohorts with under about 200 new users, and don't read
   D7/D30 for cohorts younger than 7/30 days (inferred from the official data lag).
2. **Split by acquisition source** before reacting. Ads, external links and Home traffic retain
   differently (official, 2025-10).
3. **D1 low:** fix the first session. Use the onboarding funnel and the 60 s / 180 s bounce
   windows. See [first-time experience](first-time-experience.md) (inferred).
4. **D1 fine, D7 low:** midgame. Look for a progression wall or nothing new after hour 1. Check the
   distribution of players across progression levels (official guidance, 2026-10).
5. **D7 fine, D30 low:** no long-term goals, social systems or update cadence (official
   guidance, 2026-10).
6. After each update, compare cohorts before and after, and check D1 together with average session
   time (official, 2026-10). Details: [analytics](analytics.md).

## "Reasons to come back tomorrow" checklist

Apply this to any game. A shippable game hits **at least 5 of these 10**, including #1 and #2
(inferred).

1. At session end the player can see an unfinished goal and how close it is.
2. Something accrues or completes while they're away and must be claimed in game.
3. A daily reward or streak exists, with grace for one missed day.
4. Daily and/or weekly quests reset at a fixed, visible UTC time.
5. A collection, index or bestiary shows the empty slots still to fill.
6. A friend hook: invite reward, shared progress, a gift, or a trade waiting.
7. The notification opt-in is shown at a timer or record moment, and at least one personal
   notification type is wired up.
8. A scheduled moment is visible in game, such as the next restock, event or admin hour.
9. A leaderboard or season resets weekly, so a new player can still place.
10. An update cadence is planned: a small drop every 2–4 weeks.

**Reviewer test:** after a 15-minute playtest, ask "what will you do next time you play, and when?"
If the tester can't answer in one sentence, the game fails retention review (inferred).

## Checklist for agents

### Do

- Report retention with Roblox's definitions: exact-day D1/D7/D30 in analytics, and play-day
  windows D1/D2–7/D8–28 for discovery.
- Design one hook each for tomorrow, next week and next month, and name them in the design doc.
- Make timers *produce* rewards that wait to be claimed. Show the time left in game.
- End every round or loop at a stopping point that shows earnings, the next goal and what will be
  ready next time.
- Target a 15–25 min average session. Plan short loops (30 s–3 min) inside it.
- Autosave on progress, and make quitting at any moment lose nothing important.
- Use `ExperienceNotificationService` only at a moment that needs a future notification, and only
  after `CanPromptOptInAsync()` returns true.
- Send personal, actionable notifications with `launchData` that drops the player right at the
  reason (read it with `Player:GetJoinData()`).
- Give streaks a grace rule and add a welcome-back reward for lapsed players.
- Split retention by acquisition source before changing the game.

### Don't

- Don't use fake or restarting countdowns, false scarcity, or "today only" prices that recur.
- Don't sell skips for waiting timers that block the core loop.
- Don't punish absence with permanent loss: decay, theft of idle progress, or full streak wipes.
- Don't require notification opt-in, friends, or chat to progress.
- Don't rely on AFK-in-server progress, because players are kicked after 20 minutes idle.
- Don't prompt notification opt-in on join or in the first session's first minutes.
- Don't judge D7/D30 on cohorts younger than 7/30 days, or on tiny cohorts.
- Don't chase session length past about 60 min/day at the expense of return days.

## Related

- [Discovery algorithm](discovery-algorithm.md): how play days and co-play feed recommendations.
- [First-time experience](first-time-experience.md): the biggest lever on D1.
- [Audience](audience.md): who your returning players are and what they can access.
- [Analytics](analytics.md): funnels, custom events and reading dashboards.
- [Live ops and updates](live-ops-and-updates.md): cadence, events and codes.
- [Social and virality](social-and-virality.md): co-play, invites and private servers.
- [Monetization](monetization.md): pricing without pressure tactics.
- Patterns: [daily rewards and streaks](../patterns/daily-rewards-and-streaks.md),
  [quests](../patterns/quests.md), [idle/offline income](../patterns/idle-offline-income.md),
  [leaderboards](../patterns/leaderboards.md), [player data](../patterns/player-data.md).

## Sources

1. https://create.roblox.com/docs/production/analytics/retention: D1/D7/D30 definitions, cohorts, data lag, per-horizon best practices, update cadence.
2. https://create.roblox.com/docs/discovery: Recommended for You signals (play days D1/D2–7/D8–28, 60-min playtime cap, co-play days, bounce).
3. https://devforum.roblox.com/t/recommended-for-you-algorithm-improvements-that-better-value-long-term-retention/4684575: 2026-06 change to a 28-day window; QPTR replaced by PTR and bounce.
4. https://devforum.roblox.com/t/analytics-view-retention-by-acquisition-source-and-select-your-benchmark-set/4010157: retention by source; similar vs genre benchmark sets (2025-10-16).
5. https://create.roblox.com/docs/production/analytics/analytics-dashboard: benchmark percentile ranges and the 12.11%–18.73% example.
6. https://create.roblox.com/docs/production/analytics/engagement: average session time, first-session retention chart, "without gating off the fun".
7. https://www.gameanalytics.com/reports/2025-roblox-report: D1/D7/D30 percentiles by session length; platform session and playtime percentiles.
8. https://devforum.roblox.com/t/improving-game-statistics-d1-retention/3307270: community data point (5.22% D1 = 49th percentile).
9. https://create.roblox.com/docs/cloud-services/experience-notifications: Experience Notifications APIs, eligibility, limits, banned dark patterns.
10. https://create.roblox.com/docs/reference/engine/classes/ExperienceNotificationService: API member names.
11. https://create.roblox.com/docs/production/promotion/experience-events: events, Notify Me, update announcements, limits.
12. https://create.roblox.com/docs/reference/engine/classes/SocialService.md: invite, RSVP and event API names.
13. https://create.roblox.com/docs/production/promotion/invite-prompts.md: ExperienceInviteOptions, LaunchData limit, GetJoinData retry.
14. https://create.roblox.com/docs/production/monetization.md: appointment timers disliked; no fake countdowns or scarcity.
15. https://create.roblox.com/docs/reference/engine/classes/Player.md: Idled event and the 20-minute idle disconnect; GetJoinData fields.
16. https://about.roblox.com/parental-controls: screen-time limits for Kids and Select 9–12.
17. https://www.sec.gov/Archives/edgar/data/0001315098/000162828026051059/ex991-robloxq22026earnin.htm: Q2 2026 shareholder letter, age-checked DAU mix, RFY retention change.
18. https://about.roblox.com/newsroom/2026/07/moments-new-homepage-unlocks-gaming-for-all: Moments tab, 16+ age-checked, Join from clips.
19. https://ia.acs.org.au/article/2026/roblox-sucking-up-money-from-young-players--study.html: University of Sydney study on misleading monetization (2026-05).

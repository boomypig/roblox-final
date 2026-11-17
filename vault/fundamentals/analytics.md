---
title: Analytics
type: fundamental
read-when: Adding analytics events or reading Creator Analytics after launch.
last-researched: 2026-10-22
---

# Analytics

## In one line

Instrument the first session (onboarding funnel), the economy and the shop before launch with
`AnalyticsService`. Then read new-user behavior (bounce, D1, session time, payer conversion)
against the similar-games benchmark band. Built-in dashboards cover the rest (official, 2026-10).

## Dashboards: what exists and when it unlocks

Full KPI access requires **>10 DAU and 10 play hours for 7 consecutive days**, a verified email,
2-step verification, and accepting the analytics terms (official, 2026-10).

| Page (Creator Hub) | Answers | Unlock |
|---|---|---|
| **Analytics Home** | Watchlist of up to 9 games: DAU, new users, session time, D1, daily revenue; avatar item sales; share-link visits | Any |
| **Overview** | Benchmark scorecards; **Insights** (big metric moves, updated daily); achievement panel | Scorecards and Insights need **100+ DAU** |
| AI analytics reports | Weekly/monthly drivers of DAU and revenue, outlier segments, feedback summary (built on Gemini 2.5) | **1,000+ DAU** |
| **Engagement** | DAU, WAU, MAU, average session time, playtime, **new-user first-session retention** (still playing X min after first join, vs. previous period) | Dashboard eligibility |
| **Retention** | D1/D7/D30 by first-play-date cohort; daily (10-day) and weekly (10-week) cohort tables with 7D playtime/user, 7D payer conversion, 7D and 30D revenue/user | Dashboard eligibility |
| **Monetization** | Revenue (hourly/daily, split by developer products, passes, commissions), conversion rate, paying users, ARPPU, ARPDAU; per-product pages | Dashboard eligibility |
| **Acquisition** | New/returning users with impressions and plays by source, PTR, cumulative new-user funnel, **Home Recommendations** tab (RFY signals), share links | Dashboard eligibility |
| **Demographics** | Age, gender, country, top 10 languages of MAU (groups <3 users hidden) | Dashboard eligibility |
| **Feedback** (Audience) | Up/down votes (since 2025-02-01), comments (since 2025-03-17); AI feedback report needs **20+ comments** | Any |
| **Economy / Funnel / Custom** + **Explore** | Your `AnalyticsService` events; Explore builds charts, formulas, tables | Unlocked by sending events |
| **Custom dashboards** | Your own pinned views, up to **20** per game | Any |
| **Performance** (Monitoring) | Client FPS, crash rate, memory, OOM exits; server CPU, FPS, memory; breakdown by place version | Charts need **100+ DAU** |
| **Crashes**, **Error report** | Server OOM snapshots (treemap); script errors | Any |
| **Alerts** | Threshold or week-over-week alerts on performance and data-store metrics; webhooks; up to **20** | **100+ DAU** |
| **Configs / Experiments** | Live tuning and A/B tests | See below |

All of the above are official as of 2026-10. **Open Cloud Analytics Query API**: query metrics
such as `DailyActiveUsers`, `ForwardD1Retention` and `RFYPlayThroughRate` by date range and
dimension, using an API key with `universe.analytics:read`. Most metrics keep 1,468 days of data
(official, 2026-10). A DevForum developer reported it as beta (community, 2026).

## Metric definitions (as Roblox defines them)

| Metric | Definition |
|---|---|
| **DAU** | Unique users who joined at least once that day (official) |
| **New users** | DAU who are first-time players (official) |
| **Session time** (average session time) | Total playtime ÷ number of sessions (official) |
| **Average playtime** | Playtime per DAU (`AveragePlayTimeMinutesPerDAU`) (official) |
| **Stickiness** | DAU ÷ MAU (official) |
| **D1 retention** | % of users who **first played on date X** and returned the next day (official) |
| **D7 / D30 retention** | % of that cohort who returned **on day 7 (the 8th day)** / **day 30 (the 31st day)** (official). The acquisition page words D7 as "played again on the 8th day (D8)", which is inconsistent. Treat these as *on-day*, not *within-N-days*, numbers (inferred) |
| **Play-through rate (PTR)** | % of users who played after an impression. On the Home Recommendations tab, RFY only (official) |
| **Qualified PTR** | Qualified plays ÷ impressions; used by thumbnail personalization (official) |
| **First-play bounce** | Share of first RFY sessions ending at 0–60 s and 61–180 s (official) |
| **Payer conversion rate** | % of DAU who are paying users (official) |
| **Paying users** | DAU who bought a game-related item (official) |
| **ARPPU** | Revenue ÷ paying users (official) |
| **ARPDAU** | Revenue ÷ DAU = conversion × ARPPU (official) |
| **ARPU** (experiments) | Revenue ÷ enrolled players, cumulative over the test (official) |
| **30D revenue/user** (acquisition) | Excludes subscriptions, engagement payouts and immersive ads (official) |
| **Client crash rate** | Crashes ÷ ended sessions. A dashed line means a noisy sample, so check crash count (official) |

**Segments** (filter or breakdown on every page; recalculated daily) (official, 2026-10):
- **Active payer status:** Top 15% (85–100th spend percentile in *your* game), Intermediate 35%,
  Casual 50%, Lapsed (no spend in 30 days), Never. On average the top 15% of payers bring
  ~50% of revenue (official, undated).
- **Platform spender:** Active = spent ≥$9.99 anywhere on Roblox in the last 60 days. Same
  definition as Creator Rewards.
- **In-experience activity:** Early (first 30 days), Active, Lapsed (no session in 30 days),
  Reactivated, Never played.
- **User engagement:** days played in the last 7 (0 / 1 / 2–3 / 4–7).
- **Platform activity** (60-day windows), **When user first played**, **Source**, age, gender,
  country, language, platform, OS, and memory group (performance only).
- Retention can be broken down **by acquisition source**, and the benchmark set toggles between
  "similar experiences" and "genre" (official, 2025-10-16).

**Daily Engagement Rewards:** 5 Robux per Active Spender who plays ≥10 minutes, if your game is
among the first three they launch that day (official, 2026-10). Check that average playtime of
active spenders clears 10 minutes. See [monetization](monetization.md).

## Benchmarks

- **Similar-game benchmarks** use games with similar players. They fall back to genre, then to
  all experiences, and draw only on games with ≥100 DAU. They update daily and show the
  **50th–90th percentile band**. Covered KPIs: all retention, average session time, ARPPU,
  ARPDAU, conversion, PTR (official, 2026-10).
- The docs' illustrative example band for D1 is 12.11%–18.73% (official, example only, undated).
  Roblox publishes no universal "good D1". Retention targets differ by genre (inferred).
- **Overall-success KPIs** compare against Top 200/500/1,000 tiers drawn from the top 1,000 games
  by 30-day playtime, excluding games under 30 days old (official).
- Benchmarks **never** feed the discovery algorithm (official, 2026-10).
- Heuristic (inferred): any KPI below the **50th percentile** of its band is the next thing to fix.
  Fix them in this order: bounce/D1/session time → D7 → conversion/ARPPU.

## Custom events (AnalyticsService)

Signatures were checked against the engine reference on 2026-10-22 (official). `?` = optional.

| Method | Parameters | Use |
|---|---|---|
| `AnalyticsService:LogOnboardingFunnelStepEvent` | `player: Player, step: int, stepName: string?, customFields: Dictionary?` | One-time FTUE funnel |
| `AnalyticsService:LogFunnelStepEvent` | `player, funnelName: string, funnelSessionId: string?, step: int, stepName: string?, customFields?` | Recurring funnels (shop, upgrades) and progression |
| `AnalyticsService:LogEconomyEvent` | `player, flowType: Enum.AnalyticsEconomyFlowType, currencyType: string, amount: float, endingBalance: float, transactionType: string, itemSku: string?, customFields?` | Every source and sink of soft currency |
| `AnalyticsService:LogCustomEvent` | `player, eventName: string, value: double = 1, customFields?` | Counters and valued events |
| `AnalyticsService:LogProgressionEvent` | `player, progressionPathName: string, status: Enum.AnalyticsProgressionType, level: int, levelName: string?, customFields?` | Level start/complete/fail |
| `LogProgressionStartEvent` / `LogProgressionCompleteEvent` / `LogProgressionFailEvent` | `player, progressionPathName, level, levelName?, customFields?` | Shortcuts for the above |
| `AnalyticsService:GetPlayerSegmentsAsync` | `player: Player` → dictionary | Read a player's segments at runtime |

- **Progression events "do not currently display in any Roblox-provided charts"** (official,
  2026-10). Track levels as a `LogFunnelStepEvent` funnel (e.g. `"Progression"`, step = level)
  until they do. Optionally log `LogProgressionEvent` as well, which costs rate limit.
- `Enum.AnalyticsProgressionType`: `Custom`, `Start`, `Fail`, `Complete`. Path names can't be
  empty or contain `,` `"` `'` or newlines (official).
- `Enum.AnalyticsEconomyTransactionType`: `IAP`, `Shop`, `Gameplay`, `ContextualPurchase`,
  `TimedReward`, `Onboarding`. Pass the `.Name` string. Custom strings are allowed, but the
  defaults enable Roblox insights (official).
- Custom fields: dictionary keys `Enum.AnalyticsCustomFieldKeys.CustomField01.Name` (also `02`,
  `03`); values must be **strings**; other keys are ignored (official).
- `GetPlayerSegmentsAsync` is server-only and yields. It is cached per player for the server's
  lifetime. On missing data it returns `HasData = false` with enums `Unknown` and doesn't throw.
  Fields: `ActivePayerStatus`, `WhenUserFirstPlayed`, `PlatformSpenderStatus`,
  `ExperienceActivationStatus`, `EngagementLevel`, `PlatformActivationStatus`,
  `UserNewReturningStatus`, `UserAcquisitionSource` (official). Use it, for example, to give
  first-30-day players extra guidance or show never-payers a starter offer.
- Deprecated methods you shouldn't use: `FireEvent`, `FireCustomEvent`,
  `FireInGameEconomyEvent`, `FireLogEvent`, `FirePlayerProgressionEvent` (official).

### Rules and limits (official, 2026-10)

- **Server scripts in published games only.** Calls from the client or Studio aren't recorded.
  Test in a private published place and use **View Events** (near real-time).
- Log **after** the action succeeds (purchase granted, step done), never on attempt.
- Charts appear up to **24 h** after events start. An event stops showing **90 days** after its
  last data.

| Limit | Value |
|---|---|
| Global rate | **120 + 20 × CCU** `AnalyticsService` requests per minute |
| Custom fields | 3 per event; 8,000 combined unique values, then grouped as "Other" |
| Economy currencies | **5** per the engine reference and economy guide; the event-types table says 10. Design for 5 |
| Economy transaction types / SKUs | 20 / 100, then "Other" |
| Economy amounts | `amount` always positive (sinks too); `endingBalance` ≥ 0 |
| Funnels | 10 funnels; steps 1–100 |
| Funnel behavior | Repeated steps ignored but still rate-limited; a skipped step auto-completes earlier steps; filters apply at step 1; cohort = entry date; a user's progress expires after 180 days without events; only the 10 most recent `funnelSessionId`s per user per funnel are tracked |
| Custom event names | 100. Put variants in custom fields (`PlantSeed` + field "Cabbage"), not in names |

### Sketch: server-side instrumentation outline

```lua
--!strict
-- ServerScriptService/Analytics (outline, not drop-in)
local AnalyticsService = game:GetService("AnalyticsService")
local Players = game:GetService("Players")

local STEPS = { "Joined", "FirstAction", "FirstReward", "FirstUpgrade", "LoopTwice", "FiveMinGoal" }
local reached: { [Player]: number } = {}

-- Called by server systems only, never straight from a RemoteEvent payload.
local function onboarding(player: Player, step: number)
	if step > #STEPS or step <= (reached[player] or 0) then return end
	reached[player] = step
	AnalyticsService:LogOnboardingFunnelStepEvent(player, step, STEPS[step])
end

-- Call after the server has changed the balance.
local function coins(player: Player, flow: Enum.AnalyticsEconomyFlowType, amount: number,
	balance: number, tx: Enum.AnalyticsEconomyTransactionType, sku: string?)
	AnalyticsService:LogEconomyEvent(player, flow, "Coins", amount, balance, tx.Name, sku)
end

Players.PlayerAdded:Connect(function(p) onboarding(p, 1) end)
Players.PlayerRemoving:Connect(function(p) reached[p] = nil end)
```

Skip onboarding logging for players whose saved data says they finished it, so you don't spend
the rate limit (inferred; see [player data](../patterns/player-data.md)). If a step completes on
the client, the server must validate the step number before logging. Roblox's own funnel guide
shows this exploit check (official).

## Experiments and configs

- **Configs:** `ConfigService:GetConfigAsync()` returns a global `ConfigSnapshot`;
  `ConfigService:GetConfigForPlayerAsync(player)` returns per-player values (conditions and
  experiments); `ConfigSnapshot:GetValue(key)` reads a value. Types: string, number, boolean,
  JSON (≤100,000 chars). Up to **1,000** active configs. Publishing takes ~15 s–1 min, or a
  gradual 15-min rollout. Staged values work in Studio playtests (official, 2026-10).
- **Experiments** (Creator Hub → Experiments) (official, 2026-10):
  - In-game experiments vary config values; matchmaking experiments vary matchmaking configs
    (one at a time).
  - Run **14–60 days**; up to **2 variants + control**; choose a rollout % and optional
    targeting (country, tenure, payer status…).
  - Tracked metrics: D1, D7, playtime, ARPU, ARPPU, payer conversion, session time.
  - **Early harm** (first 24 h, every 5 min): playtime −10%, ARPU −20%, conversion −20%. Harm
    verdicts need ≥10,000 players across variant + control.
  - The dashboard flags sample-ratio mismatch. Significance means the confidence interval
    excludes 0%.
  - `GetValue` on a per-player snapshot **enrolls** the player, so call it only when the
    player reaches the tested feature.
  - The config key is locked while the test runs.
  - "Games with fewer than **1,000 DAU** might struggle to get useful data." Check the minimum
    detectable effect before starting.
- **Thumbnail personalization** is the only metadata A/B tool (2–5 Home thumbnails) (official).
  There's no title or icon A/B tool (unverified). See [metadata](metadata-thumbnails-icons.md).
- **Below 1,000 DAU (inferred):** change one thing per update. Compare the daily cohort table
  (D1, 7D playtime, 7D conversion) for 7 days before vs. 7 days after. Use Explore's 7-day
  moving average and period-over-period overlays to remove weekly seasonality.

## Data freshness

| Data | Delay (official, 2026-10) |
|---|---|
| Core KPIs, benchmarks, Insights | Daily |
| D7 / D30 for a cohort | 7 / 30 days after the cohort's first-play date |
| Economy / funnel / custom charts | Up to 24 h (View Events is near real-time) |
| Revenue | Hourly and daily; Open Cloud has `ItemMonetizationRevenue` ("Robux Spent (Realtime)") |
| Performance dashboard | Up to the minute |
| Thumbnail Performance table | A few hours |
| Experiments | Daily; early-harm every 5 min for the first 24 h |
| Ads reporting | Impressions and clicks real-time; plays and earnings up to 48 h; 30-day attribution |
| Feedback ratings | End of each day |
| Sales CSV | Regenerated every 48 h; download link expires in 48 h |
| Chart CSV export | Unavailable in the first 48 h after enrolling |
| Discovery events | Logging pipeline changed 2026-10-12, so compare before/after separately |

## Before launch: what to instrument (solo dev)

1. **Onboarding funnel** (`LogOnboardingFunnelStepEvent`), 6–10 steps from join to the
   ~5-minute goal: joined → loaded/spawned → first core action → first reward → first upgrade
   → second loop → first session goal. Roblox wants new players at "the fun" within 5 minutes
   (official), so every step should land by then.
2. **Economy events** for every soft-currency source and sink, with a standard transaction
   type and a SKU for shop items and IAP bundles. Use ≤5 currencies.
3. **Shop funnel** (`LogFunnelStepEvent`, `funnelSessionId = HttpService:GenerateGUID()` per
   shop open): opened → viewed item → purchase prompted → granted. Log "granted" inside
   `MarketplaceService.ProcessReceipt` after the grant succeeds.
4. **Progression funnel:** stage/level/rebirth as steps 1..N (a funnel, because progression
   events don't chart yet).
5. **≤20 custom counters** for retention and social hooks: daily reward claimed, invite prompt
   shown/sent (`SocialService.GameInvitePromptClosed`), notification opt-in shown/accepted,
   private server join, deaths or fails per stage (custom field = stage), feature first-use.
6. **Custom fields plan:** field 1 = content id (map/stage/item category), field 2 = player
   class or mode, field 3 = reserved for your own variant flag. Platform, age and source are
   built-in filters already.
7. **In-game feedback:** `SocialService:PromptFeedbackSubmissionAsync` after a session goal
   feeds the Feedback dashboard (official).
8. Verify everything with **View Events** in a private published copy before going public.
9. At 100+ DAU: add an **Alert** for client crash rate (e.g. >5% for 5 min, the docs' example)
   with a Discord webhook.

## Week 1 after launch: what to look at

| When | Look at | Act if (inferred heuristics) |
|---|---|---|
| Day 0–1 | Performance (crash rate, memory % on phones), Error report, View Events | Crash or OOM spike on a new place version → roll back or fix before anything else |
| Day 0–1 | Onboarding funnel step churn; **New user first-session retention** at 1/5/10 min | Fix the single biggest drop first, usually the step right after join |
| Day 1–2 | Home Recommendations: PTR, bounce 0–60 s and 61–180 s | High 0–60 s → load time or first input; high 61–180 s → first reward too slow or goal unclear; low PTR → test thumbnails |
| Day 2 | D1 of the launch cohort vs. benchmark band, by platform and by source | Phone D1 far below desktop → mobile UI or performance ([performance](../../.claude/skills/roblox-map/references/performance-and-devices.md)) |
| Day 3–5 | Economy: sources − sinks, wallet trend; shop funnel; conversion, ARPPU | Wallets growing → add sinks; many shop opens but few prompts → value or visibility problem |
| Day 5–7 | Feedback comments, Engagement by "When user first played", daily cohort table | Recurring complaints → next patch |
| Day 8+ | First D7 for launch-day cohort; RFY D2–7 play days | Low D7 with good D1 → progression or return hooks ([retention](retention.md)) |

Ignore DAU swings by themselves. Check **Acquisition by source** first: an ad burst or a
YouTube video changes the mix, and the D1 of those cohorts differs from RFY cohorts (official).

## Checklist for agents

### Do
- Log every funnel step and economy event from the server, after success, in published builds.
- Put variants in custom fields, not event names. Respect 5 currencies, 10 funnels and 100
  custom names.
- Ship an onboarding funnel, an economy funnel, a shop funnel and a progression funnel with v1.
- Read new-user cohorts by source and platform, against the benchmark band.
- Use configs for tunable numbers so balance fixes don't need a publish.
- Mark update dates and compare 7-day windows before and after.

### Don't
- Don't log from LocalScripts or trust client-sent step numbers or amounts without validation.
- Don't log on purchase *attempt*, or log negative amounts.
- Don't rely on `LogProgressionEvent` for dashboards (not charted as of 2026-10).
- Don't use deprecated `Fire*` AnalyticsService methods.
- Don't run experiments under ~1,000 DAU expecting significance, or stop early on a novelty spike.
- Don't call `GetValue` on an experiment key before the player reaches the feature.
- Don't compare discovery metrics across the 2026-10-12 logging change.

## Related

- [discovery-algorithm.md](discovery-algorithm.md) · [retention.md](retention.md) ·
  [first-time-experience.md](first-time-experience.md) · [monetization.md](monetization.md)
- [metadata-thumbnails-icons.md](metadata-thumbnails-icons.md) ·
  [performance-and-devices.md](../../.claude/skills/roblox-map/references/performance-and-devices.md) ·
  [security.md](../../.claude/skills/roblox-code/references/security.md)
- [player-data](../patterns/player-data.md) · [shops](../patterns/shops.md) ·
  [daily-rewards-and-streaks](../patterns/daily-rewards-and-streaks.md)

## Sources

1. https://create.roblox.com/docs/production/analytics — Analytics Home, watchlist definitions, growth plan, benchmarks, GetPlayerSegmentsAsync
2. https://create.roblox.com/docs/production/analytics/analytics-dashboard — eligibility (>10 DAU, 10 h, 7 days), filters/segments, Explore, benchmarks, export
3. https://create.roblox.com/docs/production/analytics/get-started — DAU/MAU/session/D1/D7/D30/ARPDAU/conversion/ARPPU, top-15% ≈ 50% revenue, configs/experiments loop
4. https://create.roblox.com/docs/production/analytics/retention — cohort definitions, cohort table, 5-minute FTUE guidance
5. https://create.roblox.com/docs/production/analytics/engagement — session time, new-user first-session retention
6. https://create.roblox.com/docs/production/analytics/monetization — revenue, conversion, ARPPU, ARPDAU
7. https://create.roblox.com/docs/production/analytics/acquisition — sources, attribution metrics, D7 wording
8. https://create.roblox.com/docs/production/analytics/insights — Insights 100+ DAU, AI reports 1,000+ DAU, feedback reports 20+ comments
9. https://create.roblox.com/docs/production/analytics/event-types — View Events, rate and cardinality limits, 90-day roll-off
10. https://create.roblox.com/docs/production/analytics/funnel-events — onboarding/recurring funnels, funnelSessionId, repeated/skipped steps, exploit check
11. https://create.roblox.com/docs/production/analytics/economy-events — flow and transaction types, 5 currencies, positive amounts
12. https://create.roblox.com/docs/production/analytics/custom-events — counters, values, aggregations, 100 events
13. https://create.roblox.com/docs/production/analytics/custom-fields — 3 fields, string values, 8,000 combinations
14. https://create.roblox.com/docs/reference/engine/classes/AnalyticsService — method signatures, progression events not charted, deprecated methods
15. https://create.roblox.com/docs/reference/engine/enums/AnalyticsProgressionType — enum values
16. https://create.roblox.com/docs/reference/engine/enums/AnalyticsEconomyTransactionType — enum values
17. https://create.roblox.com/docs/production/experiments — experiment rules, metrics, early harm, MDE, <1,000 DAU warning
18. https://create.roblox.com/docs/production/configs — ConfigService usage, limits, publish timing
19. https://create.roblox.com/docs/production/analytics/performance — performance charts, 100+ DAU, crash rate definition
20. https://create.roblox.com/docs/production/analytics/alerts — alerts, 20 per game, 100+ DAU, webhooks
21. https://create.roblox.com/docs/production/analytics/custom-dashboards — 20 dashboards
22. https://create.roblox.com/docs/production/analytics/feedback — feedback data start dates, daily rating updates
23. https://create.roblox.com/docs/production/analytics/demographics — demographics fields, privacy hiding
24. https://create.roblox.com/docs/cloud/guides/analytics — Open Cloud Analytics Query API
25. https://create.roblox.com/docs/cloud/guides/analytics/metrics — metric names, data retention, RFY and thumbnail metrics
26. https://devforum.roblox.com/t/analytics-view-retention-by-acquisition-source-and-select-your-benchmark-set/4010157 — 2025-10-16 retention by source, benchmark toggle
27. https://devforum.roblox.com/t/open-cloud-analytics-query-api-is-live-beta-%E2%80%94-tested-documented-with-a-client/4753664 — community report that the query API is beta
28. https://devforum.roblox.com/t/improved-discovery-measurement-in-creator-analytics/4930122 — 2026-10-12 discovery logging change
29. https://create.roblox.com/docs/creator-rewards — Daily Engagement Rewards, Active Spender definition
30. https://create.roblox.com/docs/reference/engine/classes/SocialService — PromptFeedbackSubmissionAsync, GameInvitePromptClosed
31. https://create.roblox.com/docs/reference/engine/classes/ConfigService — GetConfigAsync, GetConfigForPlayerAsync

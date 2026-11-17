---
title: Discovery algorithm
type: fundamental
read-when: Deciding what to optimize for recommendations, or planning a launch.
last-researched: 2026-10-22
---

# Discovery algorithm

## In one line

Home's **Recommended for You (RFY)** ranks a game only on how the players RFY itself sent
behave, from the first session through day 28, as per-user averages. So the first 3 minutes,
reasons to return on days 2–28, and recurring small spends decide distribution. Metadata only
has to earn the click honestly (official, 2026-10).

## Where players come from

Acquisition sources as Creator Analytics names them (official, 2026-10):

| Source | What it is | Lever you control |
|---|---|---|
| Home recommendations | RFY sort, personalized | Signals below + custom thumbnail |
| Continue play | Returning players; first 2 slots fixed to the user's 2 most recent games since 2025-12 (official) | Play days, notifications |
| Today's Picks | Daily editorial pick on Home | Nominate via survey after each notable update (official) |
| Home other | Favorites, other Home sorts (Standout Games, Live Events, curated) | Standout: apply if novel; Live Events: run events |
| Friends | Friend activity on Home | Co-play, invites |
| Search | Search results + "similar games" on game detail pages | Accurate title/description/genre |
| Charts | All sorts on roblox.com/charts (formerly "Discover") | Relative DAU growth, see Charts |
| Sponsored ads / Search ads / Portal ads | Paid, via Ads Manager | Budget, creatives |
| Teleport | From another game | Partnerships |
| Other | External links, unattributed | Share links, socials |

Home is the usual source for "the vast majority" of players who find games (official).

## How Recommended for You works

- **Two stages** (official, 2026-10):
  - **Retrieval** picks a per-user candidate set using engagement, retention and monetization
    signals. It needs only "a very low minimum number of plays from any source", so plays from
    ads, search, charts, friends, teleports, notifications and social media help a game *enter*
    consideration.
  - **Ranking** depends *entirely* on users who first came to the game organically through RFY.
    Users first acquired by ads, curation, friends, search or social links never count toward
    RFY ranking, even if they later return through Home.
- Each user's Home narrows to roughly 100 games (official, 2026-10).
- **Explore → expand:** RFY shows the game to a small cohort. If that cohort engages and
  monetizes, it expands to similar cohorts. It retests daily on a moving window. A bad start
  carries no permanent penalty, and old games can grow again (official, 2026-10).
- **Per-user averages, not totals**, so a small game with engaged players isn't disadvantaged
  (official, 2026-10).
- **Genre isn't a ranking input.** The model learns which players retain on which games from
  behavior. Changing the genre tag doesn't change signals, but a wrong genre causes bounces
  (official, 2026-10).
- Finite and story games aren't penalized for genre-typical low day 8–28 retention (official, 2026-10).
- Games strong in only retention or only monetization still get impressions. Games strong in
  both get broader distribution (official, 2026-08).
- **Impression volume also moves with:** your updates; algorithm changes; Home traffic
  seasonality (weekly peak on **Saturday**, dips on weekdays; summer, back-to-school, holidays);
  and competitors improving faster than you, even if your own signals hold (official, 2026-10).

### Recent changes (dated)

- **2026-06-15:** Signal window extended from 7 days to 28 days (Day 1, Days 2–7, Days 8–28).
  Qualified play-through rate (QPTR) was removed as a ranking signal and replaced by
  play-through rate (PTR) + first-play bounce rate (official).
- **2026-08-20:** A "long-term player value" update went live. Roblox expected "minimal to no
  impact" on impressions for most games (official).
- **2026-10-12:** Impression, click and play logging for Home, Search and Charts moved to a more
  reliable pipeline. Recorded impressions and plays rose, and PTR reads "a bit lower". Ranking
  is unchanged (official). Creators then reported PTR drops of ~26–40% and bounce-rate spikes
  (community, unverified). Compare metrics only within the periods before and after 2026-10-12.

## Signals and the levers that move them

All signals count only users who joined organically from RFY (official, 2026-10). Per-user
signals are measured for **Day 1, Days 2–7 and Days 8–28**. The algorithm uses each window
separately and combined (official, 2026-10).

### Most important

| Signal | Roblox definition | Design levers |
|---|---|---|
| **Play-through rate (PTR)** | Rate at which users play after seeing the game in RFY | Thumbnail (RFY needs a custom one), title, icon; thumbnail personalization with 2–5 active; honest genre. See [metadata](metadata-thumbnails-icons.md) |
| **First-play bounce rate** (negative) | Share of first sessions that end in **<60 s** and in **61–180 s** | Fast load; first input within seconds; core verb in the first 30–60 s; no long cutscene or tutorial wall; no shop pop-up before the first reward. See [first-time experience](first-time-experience.md) |
| **Play days per user** | Average unique days played. For Days 2–7: how many of those 6 days the user played | Timers that finish tomorrow (crops, eggs, offline income), daily rewards and streaks, daily quests, notifications. See [retention](retention.md) |
| **Playtime per user** | Average time played, **capped at 60 min per user, per game, per day** | Session goals, progression pacing. Past 60 min/day it adds nothing to this signal |

PTR and bounce rate measure only the first session of RFY-acquired users. Returning traffic
comes through Continue and doesn't count as RFY impressions (official, 2026-10). PTR can dip
temporarily when impressions grow (official, 2026-10).

### Important

| Signal | Definition | Design levers |
|---|---|---|
| **Intentional co-play days per user** | Unique days users come back to play *with friends*: join, invites, private servers | `SocialService:PromptGameInvite` after a shared win, co-op goals, cheap private servers, party bonuses. See [social](social-and-virality.md), [private servers](../patterns/private-servers.md) |
| **Qualified play sessions per user** | "Meaningful" sessions from RFY; filters accidental clicks and quick bounces. The threshold isn't published (unverified) | Same as bounce rate + play days |
| **Spend days per user** | Unique days with Robux spend in the game | Cheap, repeatable purchases that are useful daily (refills, boosts, starter offers), not one big pass |
| **Robux spent per user** | Average Robux spent | Price ladder, passes, subscriptions. See [monetization](monetization.md) |

### What this means for design (inferred)

- **Getting a player back tomorrow is worth more than a 3-hour session.** Playtime caps at
  60 min/day, while play days count every day out to day 28. Design for daily return, not marathons.
- **The first 180 seconds are a ranking input.** Both bounce buckets (≤60 s, 61–180 s) count
  against you, so a player who quits at minute 2 hurts as much as an instant leaver. Get to
  the first reward and the first "I want the next one" moment before 3 minutes.
- **Monetize early and cheaply.** Spend days count from Day 1. A 25–50 Robux item that helps
  every session beats a single 799 Robux pass for this signal.
- **Co-play is its own signal.** Design at least one reason to bring a friend back on another day.
- **Avoid teleporting new players to another place in their first minute.** A creator
  suspected server teleports may count as bounces after the 2026-10-12 logging change
  (community, unverified).

### New games

Signals arrive in stages: PTR and bounce from the first session, then Day 1 (playtime, play
days, spend, co-play), then Days 2–7, then Days 8–28. A new game does not wait 28 days.
Early signals act immediately and later ones refine targeting (official, 2026-10).

### Reading the dashboard

**Creator Analytics → Acquisition → Home Recommendations** shows impressions, plays, every
signal per window, and a benchmark against similar games. Benchmarks never affect the
algorithm (official, 2026-10). Impression drops usually follow a drop in PTR, play days or
playtime, or a rise in bounce. Check the four most important signals first, then the rest
(official, 2026-10). Signals are also queryable through the Open Cloud Analytics API
(`RFYPlayThroughRate`, `RFYDuration0To60`, `RFYD2To7PlayDays`, …) (official). See
[analytics](analytics.md).

## What limits exposure

| Issue | Effect | Example |
|---|---|---|
| **Leading with giveaways**: metadata implying any monetary reward | Not prioritized for recommendations | Title "Robux! Play now!" (official) |
| **Mismatched metadata and content** | Not recommended; less visible in search | Dinosaur title and thumbnail, generic obby gameplay (official) |
| **Non-unique game**: metadata **and place files** closely resembling existing games | Not prioritized; lower in search; ad campaigns may get "no ad spend and no conversions" | Same title and visuals as an earlier game (official) |
| **No custom thumbnail** | Ineligible for RFY impressions | Default thumbnail only (official) |
| Community Standards or safety violations | Reduced reach or removal | (official) |

- Among indistinguishable games, Roblox surfaces the one that **first added** the unique
  metadata or place file, not the oldest game (official, 2024-12).
- The Creator Dashboard shows a banner on games with reduced exposure, updated daily. Quality
  is reclassified with every update. Report errors via Support → Bug Report with the Universe ID
  (official, 2026-10).
- Reusing your own thumbnails across your own games and groups is fine. Generic names like
  "Obby" are fine if the metadata is accurate (official, 2024-12).
- Roblox's rule for trends: "add your own spin to existing trends" in title, images,
  description and content (official). See [trend lifecycle](trend-lifecycle.md).
- **Audience → Advanced Settings → "Exclude from recommendations"** removes the game from RFY
  completely (official). Never enable it on a game you want to grow.

## Charts (roblox.com/charts)

Charts are non-personalized and statistics-based: every user sees the same lists, filterable by
device and country. Roblox tunes them for freshness, page-wide uniqueness and quality (safety
filters, DAU thresholds) (official, 2024-05). The tracker sees **26 chart sorts** (data,
2026-10-22). In-app tooltips (official, read 2026-10-22):

| Sort | Criteria |
|---|---|
| **Top Trending** | Largest *relative* increase in DAU over the past week. (The public charts page FAQ instead says "more time over the past two weeks"; the in-app tooltip is newer.) |
| **Up-and-Coming** | Published within the **last 28 days**, sorted by user growth |
| **Top Playing Now** | Current concurrent users |
| **Most Popular** | Daily users (gate*) |
| **Top Earning** | Total Robux spent in the last 7 days (gate*) |
| **Top Rated** | ≥5,000 daily users; high number *and* proportion of likes |
| **Top Revisited** | Proportion of users who return after a week (gate*) |
| **Fun with Friends** | Proportion of time spent in groups of friends (gate*) |
| **More When You Subscribe** | ≥5,000 daily users; time spent by subscribed users |
| **Top Paid Access** | Paid-access games by daily revenue |
| **Trending in {genre}** (14) | Same as Top Trending within one genre: RPG, Sports & Racing, Shooter, Action, Adventure, Entertainment, Obby & Platformer, Party & Casual, Puzzle, Roleplay & Avatar Sim, Shopping, Simulation, Strategy, Survival |
| **Trending Music Experiences** | ≥2,500 daily users; biggest relative rise in time spent over 2 weeks |
| **Learn & Explore** | Curated by the education team; apply; like ratio >50% and ≥15 CCU |

\*Gate: "at least 5,000 daily users, are within the top 10% of daily active users, or are
among the top 30 most played experiences" (official). A separate **Trending Events in
Experiences** sort lists public events that started within 7 days and have ≥1,000 RSVPs
(official, 2026-10).

What a small dev can actually reach (inferred):
- **Up-and-Coming** is the only chart built for new games, and the clock is 28 days from
  publish. What "published" means exactly (first public release vs. place creation) isn't
  documented (unverified). Release publicly only when the first-session loop is ready, then
  push growth inside those 28 days.
- **Trending and Trending in {genre}** rank *relative* week-over-week DAU growth, so a small
  game with a sharp spike can chart. Stack a major update, an event, an update announcement and
  any ad spend into the same week.
- **Genre sorts use your Roblox genre.** Choose it carefully: you can change it only once every
  3 months, and Roblox may override it (official). See [metadata](metadata-thumbnails-icons.md).
- Gated sorts (Top Rated, Top Revisited, Fun with Friends, Top Earning) are out of reach
  below ~5,000 DAU unless you rank in the top 10% of DAU.

## Search

- Search uses semantic, multilingual matching, so natural-language queries like "food games"
  work in all officially supported languages (official, 2026-10). A 2023 hybrid lexical+ML
  rollout raised plays from search in Japan by 15% (official, 2023-11).
- Mismatched metadata and clones rank lower in search (official). Repeated or irrelevant
  keywords can demote the game (official).
- Tags and hashtags in the description "are unused in our ranking algorithms" (official).
- Renaming often makes the game harder to find by its old name (official).
- Search ads sit at the top of results. For an exact game-name query, that game shows as an
  enlarged tile and ads follow (official).
- Levers (inferred): put the genre noun players type ("tower defense", "obby", "tycoon",
  "fishing") in the title or the first description sentence, keep the base name stable, and
  localize the name and description for your top languages.

## Ads (Sponsored and Search)

- **Ads Manager** is self-serve for ages 13+ with a verified email. Pay by card (18+) or by
  converting Robux to ad credits, which is **irreversible** (official, 2026-10).
- **Goals:** Plays; Earnings (limited); Engagement (beta, which targets "highly engaged players"
  for Kids/Select eligibility and costs more per play) (official, 2026-06).
- **Audiences:** All; New (never played, or not in 180+ days); Recent (last 30 days, needs
  ≥10,000 recent players); Lapsed (30–180 days, needs ≥20,000 lapsed) (official, 2026-10).
- **Cost model:** You set a daily or lifetime budget and auto-bidding picks bids. Reports show
  cost-per-play (CPP). The auction is second-price on an adjusted eCPM (official). The billing
  event (impression vs. play) isn't stated in the docs (unverified). Roblox says engaging games
  get "ads system discounts" (official).
- **Creatives:** Up to 10 thumbnails (16:9) per campaign, served evenly; an AI-generate option
  exists. Campaigns run on Home and in Search. Moderation targets ≤24 h. The first 24 h are a
  "Learning" phase. Plays and earnings can take 48 h to report, with up to 30-day attribution
  for new users (official, 2026-10).
- **Ads don't hurt RFY:** ad-acquired users are excluded from RFY signals and treated as
  "already acquired", so RFY impressions can dip while total players rise (official, 2026-10).
- Roblox reports a "150% lift in impressions", +24% plays and +16% playtime for games running
  ads (official marketing claim, undated).
- `Player:GetJoinData().LaunchData` can tag ad joins for custom onboarding or ad-only cosmetics
  (official).

When a solo dev should use ads (inferred):
1. **Not before** D1 retention and session time sit inside the similar-games benchmark band.
   Roblox's own growth plan says to fix retention, engagement and monetization *before* driving
   users (official). Ads into a leaky first session waste money and don't train RFY.
2. **Use a small Plays campaign** (a budget you can lose) to get the first cohorts. That data
   unlocks analytics (>10 DAU for 7 days, see [analytics](analytics.md)) and satisfies
   retrieval's minimum plays. Judge after 3–5 days (official guidance for Engagement campaigns).
3. **Use creatives as a cheap thumbnail test:** 10 creatives, evenly served, comparable CTR.
4. Never expect ads to buy RFY rank. They can't.

## Audience gating (Kids and Select)

RFY can only show your game to accounts allowed to play it. Since the global launch on
2026-06-16, new releases reach **only age-checked 16+ users** ("Content May Vary") unless the
creator meets all-ages requirements and the game passes evaluation (official). Roblox's core
audience is younger, so this gate can matter more than any signal (inferred). Current
requirements (official, docs 2026-10):
- ID verification (18+) or facial age estimation (<18); 2-step verification.
- Full Maturity & Compliance questionnaire with a Minimal, Mild or Moderate label.
- 2 consecutive months of Plus/Premium, or a 1,000 Robux refundable per-game fee.
- Evaluation: **250 unique plays by highly engaged, age-checked 16+ users within 60 days**,
  plus a safety review.
- Expedited review: 50,000 Robux, refundable.
- History: the 2026-06-16 launch post set **500** highly engaged players and a **100,000**
  Robux expedited review. Roblox lowered the threshold to 250 on 2026-08-19 (official), and the
  current docs list 50,000 Robux. Check the Audience Reach dashboard for your game's live numbers.

See [metadata](metadata-thumbnails-icons.md) for the questionnaire and [audience](audience.md).

## Events, updates, notifications

- **Experience events:** up to 5 thumbnails and a primary event type. Players tap "Notify Me" and
  get stream or push notifications at the start. `SocialService:PromptRsvpToEventAsync(eventId)`
  prompts an RSVP in-game for events that haven't started (official).
- **Off-Platform Featuring:** submit ≥7 days before start. Roblox says the best events run 7–30
  days. Selection uses DAU growth, playtime, retention and monetization (official, 2026-10).
- **Update announcements** reach followers. Max 60 characters, once every 3 days (official).
- **Experience notifications** go to opted-in 13+ users. Use
  `ExperienceNotificationService:CanPromptOptInAsync()` then `:PromptOptIn()`. The prompt can't
  repeat within 30 days (official). See [live-ops](live-ops-and-updates.md).
- Update cadence Roblox suggests: small updates every 2–4 weeks, larger features every 2–3
  months (official).

## Launch checklist

**Before public release**
- [ ] Custom icon + 2–5 custom Home thumbnails + accurate title, description, genre and
      subgenre ([metadata](metadata-thumbnails-icons.md)).
- [ ] Full maturity questionnaire done. Decide 16+ or all ages and start the requirements now.
- [ ] Join → first meaningful action in ≤30 s and first reward in ≤3 min, tested on a phone.
      Onboarding funnel instrumented ([analytics](analytics.md)).
- [ ] A reason to return tomorrow (timer, streak, daily quest) and one for days 2–7 and 8–28.
- [ ] Invite prompt at a shared moment; co-op or competitive reason to bring friends.
- [ ] At least one cheap, repeatable Robux purchase live on day 1.
- [ ] Notification opt-in prompt after the first success, not on join.
- [ ] Own name, own art, own place file (no uncopylocked or kit place republished as-is).
- [ ] "Exclude from recommendations" off.
- [ ] Launch event created with RSVP prompt; Today's Picks / Standout nomination sent if it fits.

**Launch week**
- [ ] Release Thursday or Friday so the first explore cohorts land on the Saturday peak (inferred).
- [ ] Seed plays: group, friends, socials via share links, an optional small Plays ad campaign.
- [ ] Daily: Home Recommendations (PTR, both bounce buckets), crash rate, onboarding funnel.
- [ ] Fix the biggest first-session drop before adding content. Up-and-Coming runs only 28 days.

**Every major update**
- [ ] New thumbnail set tested via personalization; title tag refreshed only if the update is real.
- [ ] Event + update announcement + notification in the same week to create a trending spike.

## Checklist for agents

### Do
- Optimize per-user behavior of *new* players: first 180 s, D1 return, days 2–28.
- Give every system a "come back tomorrow" hook; aim for ≤60 min/day of meaningful play.
- Ship cheap repeatable purchases and co-play reasons at launch.
- Treat thumbnails and title as a promise the first minute must keep.
- Read Home Recommendations signals by window (D1 vs D2–7 vs D8–28) before changing anything.
- Add a distinct twist (mechanic, theme, art) when following a trend.

### Don't
- Don't put Robux, "free", giveaways or reward promises in title, thumbnail or description.
- Don't republish a kit or a hit's clone with near-identical title, art or place file.
- Don't ship with the default thumbnail. It disqualifies the game from RFY.
- Don't expect ads, charts or YouTube traffic to raise RFY rank. Only RFY-acquired players count.
- Don't gate the core loop behind a tutorial longer than ~1 minute or a pre-reward shop pop-up.
- Don't rename the base title often or change genre casually (3-month lock).

## Related

- [retention.md](retention.md) · [first-time-experience.md](first-time-experience.md) ·
  [metadata-thumbnails-icons.md](metadata-thumbnails-icons.md) · [analytics.md](analytics.md)
- [social-and-virality.md](social-and-virality.md) · [monetization.md](monetization.md) ·
  [live-ops-and-updates.md](live-ops-and-updates.md) · [trend-lifecycle.md](trend-lifecycle.md)
- [audience.md](audience.md) · [performance-and-devices.md](performance-and-devices.md) ·
  the trends report (`private/trends/latest.md`)

## Sources

1. https://create.roblox.com/docs/discovery — RFY stages, signals, windows, 60-min cap, penalties, custom thumbnail rule, surfaces
2. https://create.roblox.com/docs/discovery-faq — ~100 games per Home, explore/expand, new-game staging, ads vs RFY, moving window, genre not a factor
3. https://devforum.roblox.com/t/recommended-for-you-algorithm-improvements-that-better-value-long-term-retention/4684575 — 2026-06-15: 7→28 days, QPTR → PTR + bounce
4. https://devforum.roblox.com/t/boost-your-discovery-by-building-games-people-want-to-play/4779042 — 2026-08 long-term value update, live 2026-08-20
5. https://devforum.roblox.com/t/improved-discovery-measurement-in-creator-analytics/4930122 — 2026-10-12 logging change, PTR lower; community reports
6. https://devforum.roblox.com/t/improving-user-experience-by-reducing-exposure-of-low-quality-content/3299107 — 2024-12 reduced-exposure rules, "first added" rule
7. https://devforum.roblox.com/t/testing-an-enhanced-discover-page-top-charts-and-new-sorts/2954676 — 2024-05 charts principles (freshness, uniqueness, quality)
8. https://apis.roblox.com/explore-api/v1/get-sorts — in-app chart tooltips (criteria), read 2026-10-22
9. https://www.roblox.com/charts/top-trending — public FAQ wording for Top Trending
10. https://devforum.roblox.com/t/introducing-top-playing-now-on-charts/3529809 — Top Playing Now = CCU (2025-03)
11. https://devforum.roblox.com/t/building-the-future-of-roblox-home-and-search-introducing-personalized-discovery/3432124 — Home layout, Continue slots, search tags (2025)
12. https://create.roblox.com/docs/production/analytics/acquisition — acquisition source list
13. https://create.roblox.com/docs/production/publishing/publish-games-and-places — Exclude from recommendations, release rules, naming best practices
14. https://create.roblox.com/docs/production/publishing/kids-and-select — Kids/Select requirements, 250 plays / 60 days
15. https://devforum.roblox.com/t/roblox-kids-and-select-global-launch-upcoming-updates-to-eligibility-ads-manager-and-expedited-review/4685717 — 2026-06-16 global launch, original 500 HEP / 100,000 Robux figures
15a. https://devforum.roblox.com/t/highly-engaged-player-threshold-drops-to-250/4820164 — threshold lowered 500 → 250 on 2026-08-19
16. https://create.roblox.com/docs/production/promotion/ads-manager — goals, audiences, auto-bidding, creatives, attribution
17. https://create.roblox.com/docs/production/promotion/search-ads — second-price eCPM auction, search ad placement
18. https://create.roblox.com/docs/production/promotion/advertise — Roblox ad lift claims
19. https://create.roblox.com/docs/production/promotion/experience-events — events, Trending Events sort, off-platform featuring, update limits
20. https://create.roblox.com/docs/production/promotion/experience-notifications — opt-in prompt rules
21. https://create.roblox.com/docs/creator-programs/standout-games — Standout criteria
22. https://create.roblox.com/docs/creator-programs/todays-picks-home — Today's Picks nominations
23. https://create.roblox.com/docs/creator-programs/learn-explore-sort — Learn & Explore eligibility
24. https://create.roblox.com/docs/production/publishing/experience-genres — genre change limit, genre sorts
25. https://create.roblox.com/docs/production/publishing/descriptions — tags/hashtags unused by ranking
26. https://about.roblox.com/newsroom/2023/11/inside-the-tech-solving-for-multilingual-semantic-search — semantic search, +15% Japan
27. https://create.roblox.com/docs/production/analytics/retention — update cadence guidance
28. https://create.roblox.com/docs/cloud/guides/analytics/metrics — Open Cloud RFY metric names
29. https://create.roblox.com/docs/reference/engine/classes/SocialService — PromptGameInvite, PromptRsvpToEventAsync
30. https://create.roblox.com/docs/reference/engine/classes/ExperienceNotificationService — CanPromptOptInAsync, PromptOptIn

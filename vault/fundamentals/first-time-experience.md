---
title: First-time experience
type: fundamental
read-when: Building spawn, tutorial, or anything in a new player's first 10 minutes.
last-researched: 2026-10-22
---

# First-time experience (FTUE)

## In one line

A new player has to load fast, see the goal, act within seconds and get a reward inside the first
minute, or they bounce. Roblox counts bounces under 60 s and from 61–180 s *against* your game in
Home recommendations.

## Why the first 60 s and 180 s matter

- **First-play bounce rate** is one of Roblox's "most important" Recommended for You signals. It is
  a *negative* signal measured in two buckets: sessions **under 60 seconds** and sessions of
  **61–180 seconds** (official, 2026-10). It counts only players who joined organically from the
  Recommended for You sort on Home (official, 2026-06).
- Bounce rate and play-through rate replaced the older "qualified play-through rate" in June 2026.
  Roblox says bounce measures what happens right after a player clicks your game (official,
  2026-06).
- **Qualified play sessions** filter out "accidental clicks or quick bounces" (official, 2026-10).
  Each bounce also adds nothing to playtime or play days. Full signal list:
  [discovery](discovery-algorithm.md).
- Roblox's own guidance: get users to the fun **in 5 minutes or less** (official, 2026-10), and new
  players decide whether they're interested "within minutes" (official, 2026-10).
- D1 retention is mostly decided by the first session. Roblox measures FTUE success by D1 and by
  completion of onboarding funnel steps (official, 2026-10). Benchmarks:
  [retention](retention.md).
- **New games start with an older audience.** A new all-ages game first plays only to
  **age-checked users 16+** (the "trial phase"). It reaches Roblox Kids (5–8) and Select (9–15)
  accounts only after **250 plays by "highly engaged" age-checked players within 60 days**, a
  threshold lowered from 500 on 2026-08-19 (official, 2026-08). A highly engaged player qualifies
  partly through playtime *in your game* (official, 2026-10). Your first session has to hold
  16+ players long enough to count, or the game never reaches under-16s (inferred). Details:
  [audience](audience.md).

## Target timeline (second by second)

These timings are our own targets, anchored to Roblox's 60 s and 180 s bounce windows and its
5-minute "fun" guidance (inferred). A reviewer can time them in a playtest.

| Time from clicking Play | Player must… | Build this |
|---|---|---|
| 0 → playable | Load in, ideally ≤ 10 s on a mid phone (inferred; no official number) | Streaming on, lean `ReplicatedFirst`/`ReplicatedStorage`, no full-world preload |
| Spawn +0–3 s | See where to go | Camera faces the first goal; a 3–6 word objective; a glowing target |
| +3–10 s | Do the first action | One verb (walk into, tap, click); `ProximityPrompt` or touch part |
| +10–20 s | Get feedback | Sound, particles, number pop, small camera kick. See [game feel](game-feel.md) |
| +20–45 s | Get the first reward | Currency, an item or a stat bump, shown flying into the HUD |
| +45–60 s | Close the first full loop | Earn → spend/upgrade → visibly stronger or faster. **Clears the < 60 s bucket** |
| +1–3 min | Repeat the loop with a choice | 2–3 upgrade options, a bigger target, other players doing cool things nearby. **Clears the 61–180 s bucket** |
| +3–5 min | Hit a "moment of joy" | Milestone reward with a celebration effect. Roblox recommends ending onboarding this way (official, 2026-10) |
| +5–10 min | See the long game | Preview of later zones, items or rebirth, plus a quest board. Roblox: show the range of content and short/mid/long-term goals (official, 2026-10) |
| +10–15 min | Leave with a reason to return | Unfinished goal, a running timer, a daily reward ready tomorrow. See [retention](retention.md) |

## Loading: time-to-playable

Roblox's own causes of slow loading, and their fixes (official, 2026-10):

- **Turn on instance streaming** (`Workspace.StreamingEnabled`, on by default for new places).
  It sends only the area near spawn first. Keep `StreamingMinRadius` at the default `64` and
  `StreamingTargetRadius` at `1024`. Use `ModelStreamingMode.Persistent` only rarely
  (official, 2026-10).
- **Keep `ReplicatedStorage` lean.** Everything in it replicates to every client before play.
  Move big models and audio to `ServerStorage` and send them when needed (official, 2026-10).
- **Keep `ReplicatedFirst` lean.** It replicates before everything else, so it should hold only
  the loading-screen UI and script (official, 2026-10).
- **Don't over-preload.** `ContentProvider:PreloadAsync` on the whole Workspace removes texture
  pop-in but "greatly" increases load time. Waiting on `ContentProvider.RequestQueueSize` is just
  as costly and unreliable. Preload only loading-screen images, key menu images and the starting
  area. Roblox recommends a **Skip Loading** button for large preloads (official, 2026-10).
- **Defer startup work.** Build UI panels when first opened, and spread initialization over
  several frames (official, 2026-10).
- Keep images to about 512×512 or smaller, and most minor images under 256×256 (official,
  2026-10). More: [performance and devices](performance-and-devices.md).

**Custom loading screen pattern (official, 2026-10):** a LocalScript in `ReplicatedFirst` parents
a `ScreenGui` (`IgnoreGuiInset = true`) to `PlayerGui`, calls
`ReplicatedFirst:RemoveDefaultLoadingScreen()`, waits for `game:IsLoaded()` / `game.Loaded`, then
destroys the screen. If anything is in `ReplicatedFirst`, the default screen is removed after 5 s
anyway (official, unverified: seen in a doc excerpt, not re-read).

- The docs' sample `task.wait(5)` "minimum display time" is an example value, not a rule (official,
  2026-10). **Don't add artificial waits.** Every second on a loading screen is a second toward the
  60 s bounce bucket (inferred).
- Don't show a purchase offer on the loading screen during the *first* load. Roblox says it may be
  inappropriate the first time and fine in later sessions (official, 2026-10).

## Spawn: show the goal immediately

- Spawn the player **facing** the first objective, ideally 10–30 studs away. Rotate the
  `SpawnLocation` and check in playtest (inferred).
- Mark the target with a `Highlight`, a `Beam` path or a bobbing arrow. Avoid paragraphs of text
  (inferred).
- Use one objective line at a time, at most about 8 words, such as "Collect 5 coins". Update it
  the moment it's done (inferred).
- Remove first-join blockers: no forced intro cutscene longer than about 5 s (or make it
  skippable), no name entry, no settings screen, no "like the game" pop-up, no update-log modal
  for brand-new players (inferred).
- Show other players. Seeing someone with a big pet or tall tower shows where the game goes
  (inferred). See [social and virality](social-and-virality.md).
- Don't teleport new players to another place in their first minute. A creator suspects
  teleports may count as bounces since a 2026-10-12 logging change (community, unverified).
  Keep the tutorial in the start place.
- Lobby-to-round games: put the new player in a round or a solo practice loop within 30 s. Don't
  make them wait out a full intermission (inferred). See [round system](../patterns/round-system.md).

## Teach by doing, not by reading

- Roblox: use a brief tutorial or tooltips, avoid long tutorials, and deliver a joyful moment
  after the first loop. Short contextual instructions plus starter items or currency work better
  than long tutorials (official, 2026-10).
- Roblox's funnel example: a farming game lost **70%** of players between "enter farm" and "plant
  seed". The suggested fixes were contextual indicators and making the first plant-and-grow
  required before free exploration (official, 2026-10).
- Teach **one verb at a time**, in the order the loop uses them. Introduce each new system the
  first time it's needed, not up front (inferred).
- Use world-space prompts (`ProximityPrompt` adapts its button hint to the player's input type)
  over screen text (inferred).
- Gate only the first loop. After it closes, let players roam and teach the rest with optional
  quests (inferred). See [quests](../patterns/quests.md).
- Keep early levels cheap. Roblox recommends low early XP thresholds so players level up fast,
  and tuning them live with Configs (official, 2026-10). See
  [upgrade trees](../patterns/upgrade-trees.md).
- A/B test tutorial variants, such as short dialogue against a guided arrow, with Roblox
  Experiments (official, 2026-10).

## First reward timing

- The first reward comes within **45 s** of spawn, and the first *spend* or upgrade within
  **60 s** (inferred, from the < 60 s bounce bucket).
- Give starter currency or items so the first purchase in the soft shop is instant. Roblox
  suggests testing starter amounts with Experiments (official, 2026-10).
- Make rewards visible: number pop, sound, and the item flying to the HUD or inventory
  (inferred). See [game feel](game-feel.md).

## First purchase prompt: when (and when not)

- **Never** call `MarketplaceService` prompts in the first 3 minutes of a player's first session.
  The 0–180 s window is the bounce window, and a modal over gameplay is a reason to leave
  (inferred).
- Roblox: time purchase offers so they don't hurt the session. Offer them at pauses
  (intermissions, pre-run shops). Don't stack modals. Remember the "buy Robux" flow takes several
  seconds (official, 2026-10).
- In the first session, purchases should be **player-initiated**: a shop button, or a lobby item
  they walk up to. The first *suggested* offer comes after the 3–5 min milestone, tied to what they
  just did, such as a 2× pass shown after their first upgrade (inferred).
- "Spend days per user" is a discovery signal (official, 2026-10). So have a cheap, useful item
  (about 25–50 Robux) *available* in the shop during the first session. Just don't interrupt the
  bounce window to push it (inferred). See [discovery](discovery-algorithm.md).
- "Tourists" who hop between games prefer items with immediate effects (official, 2026-10). So a
  first-session offer should be an instant, visible benefit, not a long-term subscription
  (inferred).
- Never block onboarding progress behind a purchase or behind a notification opt-in. Notification
  opt-in must not gate gameplay (official, 2026-10). Pricing, passes and receipts:
  [monetization](monetization.md).

## Mobile-first controls in the first minute

- About **80%** of Roblox DAUs were on mobile in 2024, 17% on PC and 3% on console (official,
  2025-04). Test the first minute on a phone first. Device data: [audience](audience.md).
- Roblox's default touch controls sit in the **bottom-left** (thumbstick) and **bottom-right**
  (jump) corners. Keep buttons and key info out of them. Position custom buttons relative to the
  jump button so they're reachable on phones *and* tablets. A button 40% down from the top edge
  is reachable on a phone but almost unreachable on a tablet (official, 2026-10).
- Set interactive `ScreenGui`s to `ScreenInsets = Enum.ScreenInsets.CoreUISafeInsets` so the
  notch and Roblox top-bar buttons don't cover them (official, 2026-10).
- Use **at most 1–2 custom on-screen buttons** in the first minute. Movement and one action
  button is enough (inferred).
- Read `UserInputService.PreferredInput` (`Touch` / `KeyboardAndMouse` / `Gamepad`) to show the
  right hints, such as "Tap" or "Press E" (official, 2026-10).
- For new projects, the Input Action System (`InputContext`, `InputAction`, `InputBinding` with
  `UIButton` for touch) gives each action touch, keyboard and gamepad bindings in one place
  (official, 2026-10). See [ui-ux](ui-ux.md).
- Make the first action work with taps alone. Don't require held or multi-touch gestures, precise
  aiming or camera dragging in the first 60 s (inferred).

## Social onboarding: joining friends

- Detect a player who came with someone: `Player.FollowUserId` (non-zero when they followed a
  friend in), `Player:GetJoinData().ReferredByPlayerId` (invite) and `Player.PartyId` (non-empty
  when in a party; list members with `SocialService:GetPlayersByPartyId`) (official, 2026-10).
- When a friend is present: spawn them together, put them on the same team, and let them skip
  solo-only tutorial steps that would split them up. The experienced friend is the tutorial
  (inferred).
- Invite links carry `LaunchData` (up to 200 characters). It can take seconds to arrive, so retry
  `GetJoinData()` before using it (official, 2026-10).
- **Many players can't chat.** Chat needs an age check, and players only chat with nearby age
  bands. Messages between players who can't chat are hidden (official, 2026-01). Never make
  onboarding depend on chat. Use `TextChannel:DisplaySystemMessage` for important announcements;
  it reaches everyone (official, 2026-01).
- If co-op needs coordination, use pings, emotes or preset callouts (inferred). Roblox announced
  creator-defined **Quick Words** phrase lists at RDC 2026 (press, 2026-09); the exact setup and
  limits are unverified.
- Show an invite button only after the first loop, not at spawn (inferred). Invites and rewards:
  [social and virality](social-and-virality.md).

## Instrument the funnel

Use `AnalyticsService:LogOnboardingFunnelStepEvent(player, step, stepName)`. Rules (official,
2026-10):

- Call it **from the server**, in published games only. It doesn't work from the client or Studio.
- The onboarding funnel is one-time per user. Only the first log of each step counts, but repeats
  still use up the analytics rate limit.
- Logging step N marks all earlier steps complete.
- Log step 1 in `Players.PlayerAdded`. A saved step expires after 180 days without events.
- Exploiters can fake client reports. Detect steps on the server, or validate any step a client
  reports.
- Use the **New User First Session Retention** chart (how many new users are still playing X
  minutes after joining) next to the funnel (official, 2026-10).

Suggested steps (inferred). Each one should be a server-observable fact:

`1 Joined → 2 FirstMove → 3 FirstAction → 4 FirstReward → 5 FirstUpgrade → 6 SecondLoop → 7 Milestone → 8 SessionEnd10Min`

```lua
--!strict
-- Server. Outline only: log steps the server can observe, once, in order, for new players.
local Players = game:GetService("Players")
local AnalyticsService = game:GetService("AnalyticsService")

local STEP_NAMES = { "Joined", "FirstMove", "FirstAction", "FirstReward",
	"FirstUpgrade", "SecondLoop", "Milestone", "SessionEnd10Min" }
local lastStep: { [Player]: number } = {}

local function logStep(player: Player, step: number)
	local last = lastStep[player]
	if last == nil or step ~= last + 1 then return end -- only new players, in order
	lastStep[player] = step
	AnalyticsService:LogOnboardingFunnelStepEvent(player, step, STEP_NAMES[step])
end

Players.PlayerAdded:Connect(function(player)
	-- isNewPlayer comes from your saved data (see patterns/player-data.md)
	local isNewPlayer = true
	if isNewPlayer then
		lastStep[player] = 0
		logStep(player, 1)
	end
end)
Players.PlayerRemoving:Connect(function(player) lastStep[player] = nil end)
-- Call logStep(player, 4) from the server code that grants the first reward, and so on.
```

How to read it: the biggest drop between two steps is the next thing to fix. After a change, set
the date range to start at the update (official, 2026-10). Full analytics setup:
[analytics](analytics.md).

## Common FTUE failures (reviewer: look for these)

- Black or loading screen longer than 15 s on a phone, caused by a full preload or a heavy
  `ReplicatedFirst` (inferred).
- Spawn faces a wall or empty map, so the goal isn't visible (inferred).
- A text-wall tutorial or more than 3 dialogue boxes before the first action (inferred).
- First reward after more than 60 s, or the first loop takes more than 2 min (inferred).
- A purchase or notification prompt in the first 3 min (inferred).
- Buttons under the thumbstick or jump area, or under the notch (official guidance, 2026-10).
- Onboarding that needs chat, a friend, or reading English (inferred).
- Steps logged from the client without validation, or steps that fire for returning players
  (official rules, 2026-10).

## Checklist for agents

### Do

- Hit the timeline: playable fast, first action within 10 s, first reward within 45 s, first full
  loop within 60 s, milestone celebration by 3–5 min.
- Enable streaming. Keep `ReplicatedFirst` and `ReplicatedStorage` lean, and preload only
  loading-screen and spawn-area assets.
- Spawn facing a clearly marked first objective with one short objective line.
- Teach one verb at a time through doing; use `ProximityPrompt` and world markers.
- Give starter currency so the first upgrade is immediate.
- Design and test the first minute on a phone: buttons away from the default thumbstick/jump
  corners and inside `CoreUISafeInsets`.
- Detect friends and parties (`FollowUserId`, `GetJoinData`, `PartyId`) and keep them together.
- Log 6–8 server-side onboarding funnel steps with `LogOnboardingFunnelStepEvent`, for new players
  only.
- End the first session with a visible unfinished goal and something that will be ready next time.

### Don't

- Don't add fixed waits to loading screens or show offers on the first-ever load.
- Don't preload the whole Workspace or wait on `RequestQueueSize`.
- Don't show `MarketplaceService` or `ExperienceNotificationService` prompts in the first 3 min.
- Don't gate the first loop behind chat, friends, a purchase, or reading a paragraph.
- Don't make new players wait through a full intermission before their first action.
- Don't put more than 2 custom buttons on screen in the first minute.
- Don't log funnel steps from the client or more than once per player.

## Related

- [Discovery algorithm](discovery-algorithm.md): bounce, play-through rate and qualified sessions.
- [Retention](retention.md): D1 benchmarks and return hooks after the first session.
- [Audience](audience.md): devices, ages, chat limits and the 16+ trial phase.
- [UI/UX](ui-ux.md), [game feel](game-feel.md), [performance and devices](performance-and-devices.md).
- [Analytics](analytics.md), [monetization](monetization.md), [social and virality](social-and-virality.md).
- Patterns: [player data](../patterns/player-data.md), [quests](../patterns/quests.md),
  [round system](../patterns/round-system.md), [checkpoints and respawn](../patterns/checkpoints-and-respawn.md).

## Sources

1. https://create.roblox.com/docs/discovery: first-play bounce buckets (< 60 s, 61–180 s), qualified play sessions, organic Home scope.
2. https://devforum.roblox.com/t/recommended-for-you-algorithm-improvements-that-better-value-long-term-retention/4684575: 2026-06 change adding bounce and PTR.
3. https://create.roblox.com/docs/production/analytics/retention: "fun in 5 minutes or less"; D1 best practices (brief tutorials, joyful moment).
4. https://create.roblox.com/docs/production/game-design/onboarding: FTUE goals, low early XP, starter items, moments of joy, Experiments.
5. https://create.roblox.com/docs/production/analytics/engagement: New User First Session Retention chart; avoid long tutorials.
6. https://create.roblox.com/docs/production/analytics/funnel-events: onboarding funnel rules (server-only, once per user, 180-day expiry, 70% drop example).
7. https://create.roblox.com/docs/reference/engine/classes/AnalyticsService: LogOnboardingFunnelStepEvent signature.
8. https://create.roblox.com/docs/performance-optimization/improve.md: load-time causes, preload guidance, Skip Loading button, texture sizes.
9. https://create.roblox.com/docs/workspace/streaming.md: streaming defaults (64 / 1024), Persistent caveats.
10. https://create.roblox.com/docs/players/loading-screens.md: custom loading screen pattern.
11. https://create.roblox.com/docs/reference/engine/classes/ReplicatedFirst: RemoveDefaultLoadingScreen; 5-second auto-removal (excerpt).
12. https://create.roblox.com/docs/reference/engine/classes/ContentProvider: PreloadAsync signature and behavior.
13. https://create.roblox.com/docs/production/game-design/contextual-purchases.md: purchase timing, no first-load loading-screen offers, no stacked modals.
14. https://create.roblox.com/docs/production/monetization.md: tourists vs locals.
15. https://create.roblox.com/docs/production/publishing/adaptive-design: reserved thumbstick/jump corners, phone vs tablet reach.
16. https://create.roblox.com/docs/reference/engine/enums/ScreenInsets.md: CoreUISafeInsets.
17. https://create.roblox.com/docs/reference/engine/classes/UserInputService.md: PreferredInput.
18. https://create.roblox.com/docs/input/input-action-system.md: InputContext / InputAction / InputBinding.UIButton.
19. https://create.roblox.com/docs/reference/engine/classes/Player.md: FollowUserId, GetJoinData fields.
20. https://create.roblox.com/docs/reference/engine/classes/SocialService.md: GetPlayersByPartyId, invites.
21. https://create.roblox.com/docs/production/promotion/invite-prompts.md: LaunchData limit and retry.
22. https://devforum.roblox.com/t/age-check-requirement-to-chat-now-live-globally/4226101: chat age bands, hidden messages, DisplaySystemMessage.
23. https://create.roblox.com/docs/production/publishing/kids-and-select: 16+ trial phase, highly engaged player evaluation.
24. https://devforum.roblox.com/t/highly-engaged-player-threshold-drops-to-250/4820164: threshold 500 → 250 (2026-08-19).
25. https://www.pocketgamer.biz/80-of-roblox-users-are-on-mobile-contributing-46-of-robux-revenue/: 2024 device split.
26. https://gamesbeat.com/roblox-is-adding-emojis-custom-quick-words-and-voice-calling-to-its-in-game-chat-rdc-2026/: Quick Words (RDC 2026).
27. https://create.roblox.com/docs/cloud-services/experience-notifications: opt-in must not gate gameplay.

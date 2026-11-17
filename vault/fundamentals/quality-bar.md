---
title: Quality bar
type: fundamental
read-when: Reviewing any build, or deciding if a feature is "done" to a high standard.
last-researched: 2026-10-23
---

# Quality bar

## In one line

A build is high quality when a new player on a phone reaches the fun in under a minute,
every action answers back, the world doesn't look default, there's a reason to return
tomorrow, purchases are honest and granted exactly once, and nothing trusts the client.
This file is the rubric. Each item links to the file that explains it.

## How to review with it

1. Pick the areas that apply. Every build gets A–E and H–J; monetization (G) only if anything
   is sold; K–M before a public release.
2. Check every **must**. One failed must scores the area 0, and the build isn't done.
3. Count the **shoulds** that pass.
4. Score each area: **0** = a must fails · **1** = all musts pass · **2** = all musts pass and
   at least 3/4 of the shoulds pass.
5. Report a table: area · score · each failed item with `file:line` or what you saw · evidence.

Evidence tags on each item:
- `[P]` needs a playtest. Use the Studio MCP (playtest, screenshot, console) or ask the user, and
  say which.
- `[C]` code reading. `[S]` Studio property or Explorer check. `[D]` design doc or spec.

Bars (inferred):
- **Prototype:** A, B, C, D, H at ≥ 1. This is the bar for showing friends.
- **Public launch:** no 0 in any applicable area, average ≥ 1.5, and K–M at ≥ 1.

## Why does it feel lackluster? (symptom → area)

Start here when a build "works but feels flat". This was the verdict on the user's first prototype.

| What a playtester says or does | Usually missing | Area |
|---|---|---|
| "What am I supposed to do?" / walks around for 20 s | Objective at spawn, first action within 10 s | A |
| Presses things and nothing seems to happen | ≥ 3 feedback channels per action | B |
| "It looks like a default baseplate" | Lighting preset, palette, materials, bevels, landmarks | C |
| Squints at the phone; mis-taps buttons | Safe insets, 48 px targets, text ≥ 12 px | D |
| Plays once and never returns | Tomorrow/next-week hooks, an unfinished goal at quit | E |
| Leaves when their friend leaves | A reason to play together; parties kept together | F |
| Waits a long time between turns or rounds | Something to do while waiting; a new player put in play within 30 s | A, E |
| Can't tell danger from floor | Danger color plus value contrast, passing the grayscale test | C |

## A. First session `[P]`

Details: [first-time-experience](first-time-experience.md), [discovery](discovery-algorithm.md).
Bounces under 60 s and from 61–180 s count against the game in Home recommendations (official).

Must:
- [ ] Playable within ~10 s on a mid phone profile, never more than 15 s; no artificial loading waits `[P]` (inferred targets)
- [ ] Spawn faces the first objective; one short objective line (≤ 8 words) `[P]`
- [ ] First action within 10 s, first reward within 45 s, first full loop closed within 60 s `[P]` (inferred)
- [ ] No purchase prompt or notification opt-in in the first 3 minutes `[C]`
- [ ] Lobby/round games put a new player into play (round or practice) within 30 s `[P]`

Should:
- [ ] A celebrated milestone by 3–5 minutes; the long game (later zones, rebirth, quests) visible by 10 minutes `[P]`
- [ ] Onboarding funnel of 6–8 steps logged server-side with `LogOnboardingFunnelStepEvent` `[C]`
- [ ] Friends and parties detected (`FollowUserId`, `GetJoinData`, `PartyId`) and kept together `[C]`
- [ ] No text wall: ≤ 3 dialogue boxes before the first action; teaching by doing `[P]`

## B. Game feel `[P][C]`

Details: [game-feel](game-feel.md).

Must:
- [ ] Every player action answers with ≥ 3 channels (visual, sound, motion/UI), scaled to its importance `[P]`
- [ ] Input feedback plays instantly on the client; outcome feedback only after the server confirms `[C]`
- [ ] Every `TweenInfo` has an explicit duration (UI 0.1–0.3 s); no 1 s default `[C]`
- [ ] No tweens, particles or camera effects driven from server scripts `[C]`
- [ ] Sounds go through `SoundGroup`s; SFX `Volume` ≤ 1; repeated sounds rate-limited `[C]`

Should:
- [ ] Pitch randomization on repeated sounds; burst `Emit(n)` sized to the moment `[C]`
- [ ] Camera shake/FOV kicks only for big moments, ≤ ~3°, off under `ReducedMotionEnabled` `[C]`
- [ ] Hit-stop and a `Highlight` flash on confirmed hits (combat games) `[P]`
- [ ] Long reveals are skippable by tap `[P]`

## C. Visual quality `[S][P]`

Details: [visual-quality](visual-quality.md). Run its "does this look default?" checklist in full.

Must:
- [ ] `LightingStyle` and `PrioritizeLightingQuality` set on purpose; one of the four presets applied and tuned. Never `Lighting.Technology` (deprecated) `[S]`
- [ ] An `Atmosphere`, a non-default `Sky` and a `ColorCorrectionEffect` exist `[S]`
- [ ] No visible default gray `Plastic`; template `Baseplate` removed `[S][P]`
- [ ] Hazards, path and collectibles stay distinct in grayscale (`Saturation = -1`) `[P]`
- [ ] Shadows, sun rays or color alone never carry gameplay information `[P]`

Should:
- [ ] Palette of ≤ 5 hues plus neutrals in one shared `Palette` module used by world and UI `[C]`
- [ ] Bevels/trim on large shapes; props vary in size and rotation; ≥ 2 ground materials `[P]`
- [ ] Each zone has a landmark visible from spawn `[P]`
- [ ] Screenshots on the entry-level phone profile are readable at low brightness `[P]`

## D. UI/UX and mobile `[C][P]`

Details: [ui-ux](ui-ux.md), [audience](audience.md). About 80% of players were on mobile in 2024 (official, via press).

Must:
- [ ] Interactive `ScreenGui`s use `ScreenInsets = CoreUISafeInsets`; top bar never hard-coded `[C]`
- [ ] Layout uses Scale and anchors, with `UIAspectRatioConstraint`/`UISizeConstraint` `[C]`
- [ ] Tap targets ≥ 48 px with ≥ 8 px gaps, outside the thumbstick and jump zones and the top-left corner `[P]`
- [ ] Text ≥ 12 px on a phone; scaled text capped with `UITextSizeConstraint` `[P]`
- [ ] Checked in the Device Simulator on an entry-level phone `[P]`

Should:
- [ ] Hints adapt to `UserInputService.PreferredInput`; the first button is selected for gamepad `[C]`
- [ ] Buttons have four states and a press pop with sound `[P]`
- [ ] No auto-opened shop, no stacked pop-ups, always a visible close button `[P]`
- [ ] Respects `PreferredTextSize`, `PreferredTransparency` and `ReducedMotionEnabled` `[C]`

## E. Retention hooks `[D][P]`

Details: [retention](retention.md), [daily rewards](../patterns/daily-rewards-and-streaks.md).
Play days on D1, D2–7 and D8–28 are top ranking signals; playtime counts only up to 60 min per
user per day (official).

Must:
- [ ] The design doc names one hook each for tomorrow, next week and next month `[D]`
- [ ] Every session ends at a stopping point showing earnings, the next goal, and what will be ready next time `[P]`
- [ ] Nothing important is lost by quitting at any moment; autosave on progress `[C]`
- [ ] No punishment for absence: no decay, no theft of idle progress, no full streak wipes `[D]`

Should:
- [ ] Timers produce rewards that wait to be claimed, with time left shown in game `[P]`
- [ ] Streaks have a grace rule; lapsed players get a welcome-back reward `[D]`
- [ ] Experience Notifications are offered only after `CanPromptOptInAsync()`, at a moment that needs one `[C]`
- [ ] Average session target of 15–25 min with 30 s–3 min loops inside it `[D]`

## F. Social `[D][P]`

Details: [social-and-virality](social-and-virality.md). Intentional co-play days are a ranking signal (official).

Should (the area scores 1 when the first two pass):
- [ ] At least one reason to return *with a friend* (co-op goal, shared base, friend bonus) `[D]`
- [ ] Invite entry point after a shared win, using `PromptGameInvite` with `LaunchData`; referral rewarded once via `ReferredByPlayerId` `[C]`
- [ ] Co-op works without chat or voice (pings, emotes, quick phrases) `[P]`
- [ ] At least one clip-worthy moment designed on purpose (server-wide reveal, comeback) `[D]`

## G. Monetization (if anything is sold) `[C]`

Details: [monetization](monetization.md), [player data](../patterns/player-data.md).

Must:
- [ ] Exactly one receipt path (`ProcessReceipt` and/or `BindReceiptHandler`) in one server script `[C]`
- [ ] Grants are idempotent on `PurchaseId`, stored in the same session-locked save as the reward; acknowledged only after the save succeeds `[C]`
- [ ] Returns `NotProcessedYet` when the player is absent, data isn't loaded, the product is unknown, or the save fails `[C]`
- [ ] Never grants from `PromptProductPurchaseFinished` or a client remote `[C]`
- [ ] Displayed prices come from `GetProductInfoAsync`; none hard-coded `[C]`
- [ ] Paid random items: odds shown as percentages before purchase, gated with `PolicyService` (`ArePaidRandomItemsRestricted`) `[C][P]`
- [ ] No fake or restarting timers, permanent "sales", false scarcity, or pushy copy `[P]`
- [ ] Free players can finish the core loop; in PvP/stealing games paid power is capped or matched by an earnable path `[D]`

Should:
- [ ] A cheap (25–99 Robux) repeatable or starter product live at launch `[D]`
- [ ] Pass checks handle `pcall` failure as "unknown", with a restore path `[C]`
- [ ] Purchase offers placed at natural pauses, never right after a loss `[P]`

## H. Security `[C]`

Details: [security-and-anti-exploit](security-and-anti-exploit.md). Run its RemoteEvent review checklist on every handler.

Must:
- [ ] Every remote handler runs the validation pipeline: rate limit, `typeof` checks, `math.isfinite`/range, ownership, state, distance, cooldown `[C]`
- [ ] No amount, price, damage, reward or position-as-truth is read from the client `[C]`
- [ ] Rules, prices and drop tables live in `ServerScriptService`/`ServerStorage` `[S]`
- [ ] No `RemoteFunction:InvokeClient`; `Touched`/`ProximityPrompt`/`ClickDetector` rewards re-checked on the server `[C]`

Should:
- [ ] Strikes logged; escalation drop → kick → `Players:BanAsync` with an appeal path `[C]`
- [ ] `Workspace.AuthorityMode = Server` considered for competitive movement, sports or vehicles `[D]`

## I. Player data `[C]`

Details: [player-data](../patterns/player-data.md).

Must:
- [ ] ProfileStore, or a hand-rolled store with session locks in `UpdateAsync` metadata `[C]`
- [ ] A failed or partial load never saves (`canSave = false`) and blocks purchases and trades `[C]`
- [ ] `SchemaVersion` field with ordered migrations; never downgrade `[C]`
- [ ] Saves after purchases and trades, on leave, and in `BindToClose` (30 s budget, in parallel) `[C]`

Should:
- [ ] Autosave every 180–300 s with jitter; save size well under 100 KB; lists capped `[C]`
- [ ] Studio testing kept out of live data (mock store or test place) `[C]`

## J. Performance `[S][P]`

Details: [performance-and-devices](performance-and-devices.md).

Must:
- [ ] `StreamingEnabled` on, with `StreamOutBehavior = Opportunistic` and `ModelStreamingBehavior = Improved`; client code uses `WaitForChild`/`FindFirstChild` into the world `[S][C]`
- [ ] Decoration is anchored with `CanCollide`/`CanTouch`/`CanQuery` off `[S]`
- [ ] No heavy per-frame work on the server; no server-side tweens; connections cleaned up `[C]`
- [ ] Played on the entry-level phone profile with no frame drops at the busiest moment `[P]`

Should:
- [ ] Textures ≤ 512²; meshes reused by asset ID; `CollisionFidelity = Box` on small meshes `[S]`
- [ ] Remote traffic ≤ ~20 calls/s per client; `UnreliableRemoteEvent` for cosmetic high-rate data `[C]`
- [ ] Checked on a real low-end Android before launch `[P]`

## K. Metadata and discovery (before publishing) `[S][P]`

Details: [metadata-thumbnails-icons](metadata-thumbnails-icons.md), [discovery](discovery-algorithm.md).

Must:
- [ ] Custom 512×512 icon and 2–5 custom 1920×1080 Home thumbnails showing real gameplay (no custom thumbnail = no Home recommendations, official) `[S]`
- [ ] No Robux/free/giveaway wording; no "Roblox"/"Blox" in the title `[S]`
- [ ] Maturity questionnaire answered for the most extreme content; audience decision (16+ vs all ages) made `[S]`
- [ ] Genre and subgenre match the primary loop `[S]`

Should:
- [ ] Description opens with a ≤ 160-character hook; no hashtags, URLs or control lists `[S]`
- [ ] Name and description localized for the top languages `[S]`

## L. Analytics and live-ops readiness (before publishing) `[C][D]`

Details: [analytics](analytics.md), [live-ops](live-ops-and-updates.md).

Should (the area scores 1 when the first two pass):
- [ ] Onboarding, economy and shop funnels logged from the server `[C]`
- [ ] Tunable numbers (prices, drop rates, event times) in `ConfigService` configs `[C]`
- [ ] Weekly update slot (UTC) and the first 4 updates planned `[D]`
- [ ] `ServerRestartScheduled` handled with a countdown and a teleport between rounds `[C]`

## M. Originality `[D]`

Details: [trend-lifecycle](trend-lifecycle.md).

Must:
- [ ] The spin fits in one sentence and changes what the player *does*, not just the theme `[D]`
- [ ] Own name, art, sounds and UI; no copied assets, characters or place files `[D][S]`
- [ ] Title and thumbnail aren't both near-copies of a charted game `[S]`

## Genre checklists

Each genre file ends with a "Build checklist for agents". Apply it on top of this rubric; its
numbers (stage spacing, steal timers, odds) are genre-specific musts.

## Related

- Every fundamental linked above; [CONTRIBUTING](../CONTRIBUTING.md) for vault file reviews
- [INDEX](../INDEX.md) to find the genre file for the build

## Sources

1. https://create.roblox.com/docs/discovery — bounce windows, play days, 60-min cap, co-play, custom thumbnail rule
2. https://create.roblox.com/docs/production/game-design/onboarding — FTUE guidance (via first-time-experience.md)
3. https://create.roblox.com/docs/production/monetization — honest presentation rules (via monetization.md)
4. https://create.roblox.com/docs/scripting/security/client-server-boundary — validation rules (via security-and-anti-exploit.md)
5. https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing — session locking and receipts (via player-data.md)
6. https://create.roblox.com/docs/performance-optimization/improve — performance rules (via performance-and-devices.md)
7. https://devforum.roblox.com/t/let-there-be-unified-light-unified-lighting-is-fully-live/3401512 — LightingStyle replaces Technology
8. https://www.pocketgamer.biz/80-of-roblox-users-are-on-mobile-contributing-46-of-robux-revenue/ — 2024 device split
9. Thresholds marked (inferred) are this vault's own targets, derived in the linked files.

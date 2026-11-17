---
title: Reviewer card
generated-by: python3 tools/build_cards.py (never hand-edit; rerun after editing a source)
built-from:
  - .claude/skills/build/references/quality-bar.md | How to review with it | sha256:469b1c7b42d0
  - .claude/skills/build/references/quality-bar.md | Why does it feel lackluster? (symptom → area) | sha256:2f1f5fcc264d
  - .claude/skills/build/references/quality-bar.md | A. First session `[P]` | sha256:1441fd8fba9a
  - .claude/skills/build/references/quality-bar.md | B. Game feel `[P][C]` | sha256:feeba0ef9e7b
  - .claude/skills/build/references/quality-bar.md | C. Visual quality `[S][P]` | sha256:86d16e995555
  - .claude/skills/build/references/quality-bar.md | D. UI/UX and mobile `[C][P]` | sha256:2dd0c2623b62
  - .claude/skills/build/references/quality-bar.md | E. Retention hooks `[D][P]` | sha256:468c099913f5
  - .claude/skills/build/references/quality-bar.md | F. Social `[D][P]` | sha256:0e8fdf9529bc
  - .claude/skills/build/references/quality-bar.md | G. Monetization (if anything is sold) `[C]` | sha256:aaa6677647cd
  - .claude/skills/build/references/quality-bar.md | H. Security `[C]` | sha256:bd92c7c4d928
  - .claude/skills/build/references/quality-bar.md | I. Player data `[C]` | sha256:a0b625685b85
  - .claude/skills/build/references/quality-bar.md | J. Performance `[S][P]` | sha256:a27e4414692a
  - .claude/skills/build/references/quality-bar.md | K. Metadata and discovery (before publishing) `[S][P]` | sha256:0b41e2bc94ae
  - .claude/skills/build/references/quality-bar.md | L. Analytics and live-ops readiness (before publishing) `[C][D]` | sha256:953d6f9ce35d
  - .claude/skills/build/references/quality-bar.md | M. Originality `[D]` | sha256:dc9ce3acf610
  - .claude/skills/build/references/quality-bar.md | Genre checklists | sha256:2a5e85b812ca
  - .claude/skills/roblox-code/SKILL.md | The five standing rules | sha256:d5d6e35b734e
  - .claude/skills/roblox-code/SKILL.md | Server authority | sha256:93e907b403ea
  - .claude/skills/roblox-code/SKILL.md | The traps that cost real days | sha256:b8b5f53458aa
  - .claude/skills/roblox-code/SKILL.md | Anti-patterns | sha256:94c0227ddb4c
  - .claude/skills/roblox-code/references/security.md | Review checklist for any RemoteEvent handler | sha256:adea1b40fa8b
  - .claude/skills/roblox-code/references/security.md | Checklist for agents | sha256:1307043be371
---

# Reviewer card

Everything the reviewer agent scores and checks against, copied word for word from the quality
bar, the roblox-code skill and its security reference, with the place each part came from.
Read this instead of the full files. Open a full reference only to cite it or when an item
here is not enough to judge, and then only the section named in that part's header.

Where the game keeps its remotes, pure rules and tunables is the game's own
`design/layout.json` when it exists. Read it first and check each rule below against those
paths; the rules name the roblox-code scaffold's defaults (`Net.luau`, `Core/`, `Config/`),
which apply only when there is no layout file.

## Coverage

Every section below is copied whole. Items are checklist lines, bullets, numbered items
and table rows; the card holds the same count as its source (tests/test_cards.py).

| # | Source | Section | Lines | Items |
|---|---|---|---|---|
| 1 | `.claude/skills/build/references/quality-bar.md` | How to review with it | 17-35 | 9 |
| 2 | `.claude/skills/build/references/quality-bar.md` | Why does it feel lackluster? (symptom → area) | 36-50 | 8 |
| 3 | `.claude/skills/build/references/quality-bar.md` | A. First session `[P]` | 51-68 | 9 |
| 4 | `.claude/skills/build/references/quality-bar.md` | B. Game feel `[P][C]` | 69-85 | 9 |
| 5 | `.claude/skills/build/references/quality-bar.md` | C. Visual quality `[S][P]` | 86-102 | 9 |
| 6 | `.claude/skills/build/references/quality-bar.md` | D. UI/UX and mobile `[C][P]` | 103-119 | 9 |
| 7 | `.claude/skills/build/references/quality-bar.md` | E. Retention hooks `[D][P]` | 120-137 | 8 |
| 8 | `.claude/skills/build/references/quality-bar.md` | F. Social `[D][P]` | 138-147 | 4 |
| 9 | `.claude/skills/build/references/quality-bar.md` | G. Monetization (if anything is sold) `[C]` | 148-166 | 11 |
| 10 | `.claude/skills/build/references/quality-bar.md` | H. Security `[C]` | 167-180 | 6 |
| 11 | `.claude/skills/build/references/quality-bar.md` | I. Player data `[C]` | 181-194 | 6 |
| 12 | `.claude/skills/build/references/quality-bar.md` | J. Performance `[S][P]` | 195-209 | 7 |
| 13 | `.claude/skills/build/references/quality-bar.md` | K. Metadata and discovery (before publishing) `[S][P]` | 210-223 | 6 |
| 14 | `.claude/skills/build/references/quality-bar.md` | L. Analytics and live-ops readiness (before publishing) `[C][D]` | 224-233 | 4 |
| 15 | `.claude/skills/build/references/quality-bar.md` | M. Originality `[D]` | 234-242 | 3 |
| 16 | `.claude/skills/build/references/quality-bar.md` | Genre checklists | 243-247 | 0 |
| 17 | `.claude/skills/roblox-code/SKILL.md` | The five standing rules | 37-62 | 5 |
| 18 | `.claude/skills/roblox-code/SKILL.md` | Server authority | 63-93 | 4 |
| 19 | `.claude/skills/roblox-code/SKILL.md` | The traps that cost real days | 172-244 | 0 |
| 20 | `.claude/skills/roblox-code/SKILL.md` | Anti-patterns | 245-259 | 8 |
| 21 | `.claude/skills/roblox-code/references/security.md` | Review checklist for any RemoteEvent handler | 192-207 | 11 |
| 22 | `.claude/skills/roblox-code/references/security.md` | Checklist for agents | 208-227 | 13 |

## 1. How to review with it

Source: `.claude/skills/build/references/quality-bar.md`, lines 17-35.

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

## 2. Why does it feel lackluster? (symptom → area)

Source: `.claude/skills/build/references/quality-bar.md`, lines 36-50.

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

## 3. A. First session `[P]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 51-68.

Details: [first-time-experience](../../../../vault/fundamentals/first-time-experience.md), [discovery](../../../../vault/fundamentals/discovery-algorithm.md).
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

## 4. B. Game feel `[P][C]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 69-85.

Details: [game-feel](../../roblox-vfx/references/game-feel.md).

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

## 5. C. Visual quality `[S][P]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 86-102.

Details: [visual-quality](../../roblox-map/references/visual-quality.md). Run its "does this look default?" checklist in full.

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

## 6. D. UI/UX and mobile `[C][P]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 103-119.

Details: [ui-ux](../../roblox-ui/references/ui-ux.md), [audience](../../../../vault/fundamentals/audience.md). About 80% of players were on mobile in 2024 (official, via press).

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

## 7. E. Retention hooks `[D][P]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 120-137.

Details: [retention](../../../../vault/fundamentals/retention.md), [daily rewards](../../../../vault/patterns/daily-rewards-and-streaks.md).
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

## 8. F. Social `[D][P]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 138-147.

Details: [social-and-virality](../../../../vault/fundamentals/social-and-virality.md). Intentional co-play days are a ranking signal (official).

Should (the area scores 1 when the first two pass):
- [ ] At least one reason to return *with a friend* (co-op goal, shared base, friend bonus) `[D]`
- [ ] Invite entry point after a shared win, using `PromptGameInvite` with `LaunchData`; referral rewarded once via `ReferredByPlayerId` `[C]`
- [ ] Co-op works without chat or voice (pings, emotes, quick phrases) `[P]`
- [ ] At least one clip-worthy moment designed on purpose (server-wide reveal, comeback) `[D]`

## 9. G. Monetization (if anything is sold) `[C]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 148-166.

Details: [monetization](../../../../vault/fundamentals/monetization.md), [player data](../../../../vault/patterns/player-data.md).

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

## 10. H. Security `[C]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 167-180.

Details: [security](../../roblox-code/references/security.md). Run its RemoteEvent review checklist on every handler.

Must:
- [ ] Every remote handler runs the validation pipeline: rate limit, `typeof` checks, `math.isfinite`/range, ownership, state, distance, cooldown `[C]`
- [ ] No amount, price, damage, reward or position-as-truth is read from the client `[C]`
- [ ] Rules, prices and drop tables live in `ServerScriptService`/`ServerStorage` `[S]`
- [ ] No `RemoteFunction:InvokeClient`; `Touched`/`ProximityPrompt`/`ClickDetector` rewards re-checked on the server `[C]`

Should:
- [ ] Strikes logged; escalation drop → kick → `Players:BanAsync` with an appeal path `[C]`
- [ ] `Workspace.AuthorityMode = Server` considered for competitive movement, sports or vehicles `[D]`

## 11. I. Player data `[C]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 181-194.

Details: [player-data](../../../../vault/patterns/player-data.md).

Must:
- [ ] ProfileStore, or a hand-rolled store with session locks in `UpdateAsync` metadata `[C]`
- [ ] A failed or partial load never saves (`canSave = false`) and blocks purchases and trades `[C]`
- [ ] `SchemaVersion` field with ordered migrations; never downgrade `[C]`
- [ ] Saves after purchases and trades, on leave, and in `BindToClose` (30 s budget, in parallel) `[C]`

Should:
- [ ] Autosave every 180–300 s with jitter; save size well under 100 KB; lists capped `[C]`
- [ ] Studio testing kept out of live data (mock store or test place) `[C]`

## 12. J. Performance `[S][P]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 195-209.

Details: [performance-and-devices](../../roblox-map/references/performance-and-devices.md).

Must:
- [ ] `StreamingEnabled` on, with `StreamOutBehavior = Opportunistic` and `ModelStreamingBehavior = Improved`; client code uses `WaitForChild`/`FindFirstChild` into the world `[S][C]`
- [ ] Decoration is anchored with `CanCollide`/`CanTouch`/`CanQuery` off `[S]`
- [ ] No heavy per-frame work on the server; no server-side tweens; connections cleaned up `[C]`
- [ ] Played on the entry-level phone profile with no frame drops at the busiest moment `[P]`

Should:
- [ ] Textures ≤ 512²; meshes reused by asset ID; `CollisionFidelity = Box` on small meshes `[S]`
- [ ] Remote traffic ≤ ~20 calls/s per client; `UnreliableRemoteEvent` for cosmetic high-rate data `[C]`
- [ ] Checked on a real low-end Android before launch `[P]`

## 13. K. Metadata and discovery (before publishing) `[S][P]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 210-223.

Details: [metadata-thumbnails-icons](../../../../vault/fundamentals/metadata-thumbnails-icons.md), [discovery](../../../../vault/fundamentals/discovery-algorithm.md).

Must:
- [ ] Custom 512×512 icon and 2–5 custom 1920×1080 Home thumbnails showing real gameplay (no custom thumbnail = no Home recommendations, official) `[S]`
- [ ] No Robux/free/giveaway wording; no "Roblox"/"Blox" in the title `[S]`
- [ ] Maturity questionnaire answered for the most extreme content; audience decision (16+ vs all ages) made `[S]`
- [ ] Genre and subgenre match the primary loop `[S]`

Should:
- [ ] Description opens with a ≤ 160-character hook; no hashtags, URLs or control lists `[S]`
- [ ] Name and description localized for the top languages `[S]`

## 14. L. Analytics and live-ops readiness (before publishing) `[C][D]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 224-233.

Details: [analytics](../../../../vault/fundamentals/analytics.md), [live-ops](../../../../vault/fundamentals/live-ops-and-updates.md).

Should (the area scores 1 when the first two pass):
- [ ] Onboarding, economy and shop funnels logged from the server `[C]`
- [ ] Tunable numbers (prices, drop rates, event times) in `ConfigService` configs `[C]`
- [ ] Weekly update slot (UTC) and the first 4 updates planned `[D]`
- [ ] `ServerRestartScheduled` handled with a countdown and a teleport between rounds `[C]`

## 15. M. Originality `[D]`

Source: `.claude/skills/build/references/quality-bar.md`, lines 234-242.

Details: [trend-lifecycle](../../../../vault/fundamentals/trend-lifecycle.md).

Must:
- [ ] The spin fits in one sentence and changes what the player *does*, not just the theme `[D]`
- [ ] Own name, art, sounds and UI; no copied assets, characters or place files `[D][S]`
- [ ] Title and thumbnail aren't both near-copies of a charted game `[S]`

## 16. Genre checklists

Source: `.claude/skills/build/references/quality-bar.md`, lines 243-247.

Each genre file ends with a "Build checklist for agents". Apply it on top of this rubric; its
numbers (stage spacing, steal timers, odds) are genre-specific musts.

## 17. The five standing rules

Source: `.claude/skills/roblox-code/SKILL.md`, lines 37-62.

These came out of a v1 post-mortem on a real game that had to be rebuilt. They
are not style preferences.

**1. Disk is the only source of truth.** Studio connects via `rojo serve`. Never
edit a script inside Studio, never `set_script_source` over MCP. MCP is for
geometry, inspection and screenshots. (v1 died of Studio-to-disk drift.)

**2. Pure logic lives in `src/shared/Core/`, Instances live at the edges.** If a
function can be written without touching an Instance, it must be. That is the
only reason any of this is testable at all.

**3. Gameplay and cross-client paths go through one `Net.luau`** of plain
RemoteEvents, every name declared in one place. Knit is lifecycle and DI
scaffolding, not transport. When you cannot watch the game run, the most
primitive debuggable transport wins.

**4. Cosmetics can never break gameplay.** Effects resolve async, fail inert,
every one pcall-isolated. (v1's grapple was killed by a tracer.)

**5. Every tunable lives in `src/shared/Config/`.** A balance pass must be a data
edit, never a code edit.

---

## 18. Server authority

Source: `.claude/skills/roblox-code/SKILL.md`, lines 63-93.

> The server owns the game. Clients own the display.

| Responsibility | Lives on |
|---|---|
| Game state: health, inventory, score, ownership | **Server** |
| Game logic: damage, purchases, spawning, scoring | **Server** |
| Validation and anti-cheat | **Server** |
| Input, camera, local UI, visual feedback | Client |

Every value that arrives from a client is a **request**. Validate type, then
range, then ownership, before it changes anything:

```lua
remote.OnServerEvent:Connect(function(player: Player, target: unknown)
	if typeof(target) ~= "Vector3" then return end
	local char = player.Character
	if not char or not char.PrimaryPart then return end
	if (target - char.PrimaryPart.Position).Magnitude > MAX_REACH then return end
	-- only now is it a fact
end)
```

The exception worth naming: movement in a fast first-person game is usually
client-authoritative because server-authoritative movement feels awful. That is
a deliberate, documented trade, not an oversight - but it means the *consequences*
of movement (scoring, elimination, rewards) must stay on the server.

---

## 19. The traps that cost real days

Source: `.claude/skills/roblox-code/SKILL.md`, lines 172-244.

Full detail with symptoms in `references/traps.md`. The short list, because
knowing these exist is most of the value:

**A remote payload has THREE ends.** Sender, server relay, receiver. Change the
arguments at one and the untouched middle silently drops every packet - no error
anywhere. Grep the arity across all three before believing a fix.

**Two Rojo connections duplicate every new file.** Two plugin connections create
each new ModuleScript twice, `Knit.AddControllers` then throws on the duplicate
name, and every controller dies at once. One server, one connect.

**ROJO OWNS ITS SUBTREE. A RUNTIME CHILD OF ONE IS DELETED ON THE NEXT CONNECT.**
Anything that must survive a sync has to live in the SOURCE Rojo serves - not in
code that creates it at runtime. This is not intermittent; it is what
reconciliation *is*. Measured 2026-09-09: a service dressed the map at runtime,
replacing 897 prop boxes with MeshParts. It worked - correct kinds, correct
placement, the map finally looked like a map. Then Rojo reconnected and every
tree vanished, because `Workspace.Map` is sourced from a file, and 897 instances
that are in the game and in no source file are, correctly, stale instances to
remove. It reads exactly like "Rojo is broken" and it is the opposite.

The trap underneath it: **`MeshId` is not settable from a Rojo `.model.json`
property table**, which is what pushes people to a runtime step in the first
place. The way out is not runtime - it is `.rbxmx`, Roblox's own XML model
format, where `MeshId` and `TextureID` are ordinary `<Content>` properties:

```xml
<Item class="MeshPart" referent="RBX1"><Properties>
  <Vector3 name="InitialSize"><X>5</X><Y>8.2</Y><Z>5</Z></Vector3>
  <Vector3 name="size"><X>10</X><Y>16.4</Y><Z>10</Z></Vector3>
  <Content name="MeshId"><url>rbxassetid://MESH_ID</url></Content>
  <Content name="TextureID"><url>rbxassetid://IMAGE_ID</url></Content>
</Properties></Item>
```

`InitialSize` is the mesh's NATURAL size and is what Roblox scales `size`
against; omit it and the mesh is stretched by whatever the importer guessed.
And **edit an rbxmx with an XML parser, never a regex** - a part carrying a
PointLight has a nested `<Item>`, so a flat scan produces unbalanced XML.
`rojo build` catches that, and is the reason to run it after any file rewrite.

**`ScaleTo` is a `Model` method, not a `MeshPart` one.** A MeshPart scales by
setting `.Size`. `clone:ScaleTo(n)` on a MeshPart throws on the first one it
touches - and no static check sees it, because it is a runtime member lookup.

**An established TCP connection is not a synced session.** An unaccepted "Would
you like to connect?" prompt blocked syncing for an entire session while
everything looked connected. That is what the build stamp in the boot scripts is
for: if that exact line is not in Output, Studio is not running your code and no
edit you make can possibly matter.

**A Knit method named the same as its cache field returns the function.** Silent,
type-checks fine, and the value you get back is a function rather than data.

**A bare `pcall` hides the throw.** Always capture and warn the error, or the
failure becomes invisible and you debug the wrong layer for an hour.

**A grounded Humanoid brakes scripted velocity to a stop.** Setting WalkSpeed to
0 is itself a brake, and `ChangeState(Freefall)` loses to the 240Hz state
machine. `SetStateEnabled(Running, false)` with a guaranteed restore is the only
thing that holds.

**`execute_luau` drops all output if the script yields.** Split it into two
calls, or schedule with `task.delay` and return immediately.

**A verifier that cannot find its target must FAIL, not pass.** A check scoped to
the wrong name reported green while 361 defects shipped underneath it. "Not
found" is a failure result.

---

## 20. Anti-patterns

Source: `.claude/skills/roblox-code/SKILL.md`, lines 245-259.

| Anti-pattern | Why it bites | Instead |
|---|---|---|
| `wait()`, `spawn()`, `delay()` | Deprecated scheduler, imprecise | `task.wait/spawn/delay/defer` |
| A number hardcoded in a Service | Balance passes become code changes | `src/shared/Config/` |
| Remote names as bare strings | Typos fail silently | Declared in `Net.luau` |
| Knit auto-remotes for gameplay | Undebuggable when play mode is opaque | `Net.luau` |
| Client-stored state | Exploitable by definition | Server |
| `require` inside a loop | Repeated resolution | Cache the reference |
| Deep `require` chains | Circular dependency hell | Knit's service locator |
| Unbounded `RunService.Heartbeat` work | Frame cost scales with players | Budget it, or use tags |

---

## 21. Review checklist for any RemoteEvent handler

Source: `.claude/skills/roblox-code/references/security.md`, lines 192-207.

- [ ] Handler lives in a server Script under `ServerScriptService`.
- [ ] Per-player rate limit, with buckets cleared on `PlayerRemoving`.
- [ ] Every parameter typed as `unknown` and checked with `typeof`.
- [ ] Numbers pass `math.isfinite`, integer and range checks. Strings are length-capped and valid
      UTF-8.
- [ ] No Instance, path or module name from the client is used without a whitelist or
      `IsDescendantOf` check.
- [ ] Ownership, alive state, data-loaded, distance, cooldown and cost checked from server state.
- [ ] No amount, price, damage or reward value is read from the client.
- [ ] Bounded work per call: no unbounded loops, clones or DataStore calls.
- [ ] Results replicated from server state. Raw input is never relayed.
- [ ] No `InvokeClient`. Any `OnServerInvoke` returns quickly.
- [ ] Failures drop silently and count a strike.

## 22. Checklist for agents

Source: `.claude/skills/roblox-code/references/security.md`, lines 208-227.

#### Do
- Name remotes after intents and keep all rules and values on the server.
- Run the validation pipeline in order, with one token bucket per remote.
- Use server-side distance and cooldown with latency slack, and reset the last valid position
  after server-initiated moves.
- Consider `AuthorityMode = Server` for competitive movement, sports or racing games.
- Grant purchases only through `ProcessReceipt`/`BindReceiptHandler`, keyed by `PurchaseId`.
- Session-lock data and save both sides immediately after trades.
- Log strikes and escalate from drop to kick to `BanAsync`, with an appeal path.

#### Don't
- Don't trust client-sent amounts, prices, damage, positions-as-truth or "I hit X" without checks.
- Don't call `RemoteFunction:InvokeClient` from the server.
- Don't put secrets or server logic in `ReplicatedStorage` or LocalScripts.
- Don't rely on client anti-cheat, client cooldowns or disabled UI buttons for security.
- Don't use `PromptProductPurchaseFinished` to grant purchases.
- Don't auto-ban on a single noisy heuristic.

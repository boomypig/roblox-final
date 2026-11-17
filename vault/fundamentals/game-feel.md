---
title: Game feel
type: fundamental
read-when: Adding feedback to an action: tweens, sound, particles, camera.
last-researched: 2026-10-22
---

# Game feel

## In one line

Every player action gets an instant response on at least three channels: motion, sound, and one
of particles, camera or haptics. Scale the response to how much the moment matters, and run all of
it on the client once the server has confirmed the result.

## Principles

- The talk "Juice it or lose it" takes one Breakout prototype from flat to lively without changing
  the rules. The changes are tweens with easing, squash and stretch, particles, sound, and screen
  shake (community, 2012). A prototype that "works but feels lackluster" usually lacks these
  layers, not features (inferred).
- Contrast beats volume. Routine actions get small feedback, so that rare moments can be loud
  (inferred). If everything shakes and flashes, nothing reads as special.
- Responses have three phases. Anticipation is a short wind-up or build. The action itself is fast.
  Follow-through is overshoot, lingering particles, then settling (community: classic animation
  principles, as used in the talks cited below).
- Easing: most UI motion belongs in 100–500 ms. Small feedback is ~100 ms, panels 200–300 ms, and
  long moves up to 400 ms; 500 ms starts to drag. Use ease-out for things entering or responding,
  and make exits shorter than entries (community: NN/g, 2020-02).

## Server vs client

- The server decides outcomes, and the client renders effects. The server sends a compact event
  (`RemoteEvent:FireClient(player, "Collect", pos, amount)`, or `FireAllClients` for shared moments).
  Use `UnreliableRemoteEvent` (< 1,000 bytes) for high-rate cosmetic broadcasts (official,
  2026-10). Never tween on the server, because the property replicates every frame
  (official, 2026-10).
- Give **input feedback** instantly on the client: button press, swing animation, whoosh sound.
  Give **outcome feedback** only after the server confirms it: coins added, hit landed, item
  bought. A wrong celebration is worse than a 100 ms delay (inferred).
- Use one client module, for example `ReplicatedStorage.Shared.FX`, with a table of presets:
  `FX.play("Collect", position, amount)`. Every system calls it, so tuning happens in one file
  (inferred). Keep templates (sounds, emitters) small in `ReplicatedStorage`; see
  [performance](performance-and-devices.md).
- The camera, `HapticEffect`, `SoundService:PlayLocalSound` and `GuiButton` events are client-only
  (official, 2026-10).

## Tweens: easing and durations

`TweenInfo.new(time, style, direction, repeatCount, reverses, delayTime)` defaults to
1 s, `Quad`, `Out` (official, 2026-10). Always pass time and style explicitly, because 1 s is too
slow for almost every feedback.

| Use | Time (s) | `EasingStyle` / `EasingDirection` |
|---|---|---|
| Button press-in (UIScale 1 → 0.92) | 0.05–0.08 | `Quad` / `Out` |
| Button release, pop (→ 1.0, overshoot) | 0.12–0.2 | `Back` / `Out` |
| Counter "punch" (1 → 1.15 → 1) | 0.08 up, 0.15 down | `Quad` / `Out`, then `Back` / `Out` |
| Panel open (scale 0.85 → 1 + fade in) | 0.2–0.3 | `Back` or `Quint` / `Out` |
| Panel close | 0.12–0.2 | `Quad` / `In` |
| Toast in / out | 0.2 / 0.15 | `Back` / `Out`, then `Quad` / `In` |
| Number count-up | 0.3–0.6 | `Quad` / `Out` (tween a `NumberValue`) |
| Idle bob, pulse, glow loops | 1–2 per cycle | `Sine` / `InOut`, `repeatCount = -1`, `reverses = true` |
| Celebration-only bounce | 0.4–0.7 | `Bounce` or `Elastic` / `Out`: rare drops only |
| Fades, progress bars, spins | any | `Linear` |

All times above are starting points (inferred); the enum names are official (2026-10).
- Prefer `Back` for pops, `Quint`/`Exponential` for snappy moves, and `Sine` for anything
  ambient. Never use `Elastic` or `Bounce` on routine UI; they read as sluggish (inferred).
- `Cancel()` the previous tween on the same property before starting a new one, or they fight
  (inferred).
- For per-frame custom curves (camera, shake decay), use
  `TweenService:GetValue(alpha, style, direction)` (official, 2026-10).
- `GuiObject:TweenSize`/`TweenPosition` are deprecated; use `TweenService` (official, 2026-10).
- If `GuiService.ReducedMotionEnabled` is true, set UI tween times to 0 or use fades only
  (official, 2026-10).

## Squash and scale pops

- Put a `UIScale` in every animated button, counter and panel, and tween `UIScale.Scale`, not `Size`.
  It doesn't reflow layouts, and strokes and corners scale with it (official API; rule inferred).
- 3D pickups and props: tween `Model:ScaleTo()` through a `NumberValue`, or tween a part's `Size`
  on the client. Squash on landing or impact is X/Z 1.15 and Y 0.85 for 0.06 s, then back with
  `Back`/`Out` 0.2 s. Keep the volume roughly constant (inferred).
- Collect pop: the item scales 1 → 1.3 → 0 over 0.15 s while a particle burst plays (inferred).

## Particles

- Burst emitters: set `Enabled = false` on the template, then call `emitter:Emit(n)`.
  `Emit()` with no count emits 16 (official, 2026-10). Parent emitters to an `Attachment` at the
  effect point, and reuse pooled emitters instead of cloning per hit (inferred).
- Starting values (inferred):

  | Burst | `Emit(n)` | `Lifetime` | `Speed` | Other |
  |---|---|---|---|---|
  | Collect / click | 8–15 | 0.3–0.6 | 8–15 | `Drag = 5`, `Size` shrinks to 0, `LightEmission = 0.5` |
  | Hit spark | 6–10 | 0.15–0.3 | 20–30 | `SpreadAngle = (40, 40)`, `LightEmission = 1` |
  | Level up / rebirth | 30–50 across 2 emitters | 0.6–1.2 | 10–25 | Ring and sparkles, `Acceleration = (0, 10, 0)` |
  | Rare reveal | 60–100 across 3 emitters | 0.8–1.5 | 15–35 | Plus a `Beam` or light flash |

- Budgets: emitters are capped at 100 particles/s on mobile. `Emit()` bursts may skip
  quality scaling, so scale `n` by quality level. Don't animate emitter properties every frame.
  Details are in [performance-and-devices](performance-and-devices.md) (official/community,
  2026-10).

## Sound

- `Sound.Volume` defaults to 0.5, with a max of 10 (official, 2026-10). Never exceed 1.0 for
  any SFX (inferred).
- `SoundGroup.Volume` (0–10) multiplies every sound assigned via the `Sound.SoundGroup` property
  (not by parenting), and groups stack multiplicatively. A `SoundEffect` parented to a group applies
  to every sound in it (official, 2026-10).
- Setup (volumes inferred): put groups under `SoundService`:
  - `Master` 1.0
  - `Music` 0.3
  - `SFX` 0.6
  - `UI` 0.5
  - `Ambient` 0.4

  Add a settings menu with sliders for each; the docs ask for separate volume controls
  (official, 2026-10). Optional: a `CompressorSoundEffect` on `Master` stops stacked peaks
  (inferred).
- Per-sound volume (inferred): UI clicks 0.2–0.4, pickups 0.3–0.5, hits 0.4–0.6, big rewards
  0.6–0.8.
- Pitch variety: for any repeated sound, set `PlaybackSpeed = rng:NextNumber(0.92, 1.08)` with
  `local rng = Random.new()`. Combo pitch-up adds 0.05 per collect within 0.5 s, capped at 1.4, then
  resets (inferred). `PlaybackSpeed` raises pitch and speed together (official, 2026-10).
- Rate limit (inferred) to stop collecting 50 coins in one frame from blowing out ears:
  - The same sound plays at most once per 0.05 s.
  - At most 4 overlapping copies of it.
  - Extra triggers are dropped.
- 2D one-shots: `SoundService:PlayLocalSound(sound)` plays a copy for this client only
  (official, 2026-10).
- 3D sounds: parent to a part or `Attachment`. `RollOffMinDistance`/`RollOffMaxDistance` are in
  studs (official, 2026-10). Use a max distance of 60–150 for gameplay SFX (inferred).
- Preload the first-click UI sounds with `ContentProvider:PreloadAsync`, so the first press isn't
  silent (inferred; preloading rules in [performance](performance-and-devices.md)).
- Pair every meaningful sound with a visual, because some players play muted
  (official, 2026-10).

## Camera: FOV kicks and shake

- `Camera.FieldOfView` defaults to 70 and is clamped to 1–120. The docs warn that extremes
  disorient players (official, 2026-10).
- FOV kick (dash, boost, hit confirm, rebirth): +4 to +8 over 0.06 s `Quad`/`Out`, then back over
  0.25 s `Sine`/`Out`. Never sustain more than ~90 in gameplay (inferred).
- Shake runs on the client only. Bind with
  `RunService:BindToRenderStep("Shake", Enum.RenderPriority.Camera.Value + 1, fn)` (Camera = 200)
  so it applies after the default camera module. Then do
  `camera.CFrame *= CFrame.Angles(pitch, yaw, roll)` with small random angles (API official; pattern
  community, 2026-10). `Humanoid.CameraOffset` is a simpler positional alternative (official API).
- Use the "trauma" model. Hits add trauma (0–1), offset = max angle × trauma², and trauma decays at
  ~1.5/s (community: GDC "Juicing Your Cameras With Math", 2016).
- Max angles (inferred):
  - Light hit: 0.4°
  - Heavy hit: 1.2°
  - Explosion or boss slam: 2.5°
  - Never above 3°
- Never shake for clicks, collects or UI.
- If `GuiService.ReducedMotionEnabled` is true, skip shake and FOV kicks, and add a "Camera shake"
  toggle in settings (inferred extension of the official reduced-motion guidance).

## Hit-stop

- On a confirmed hit, freeze the attacker's and victim's local animations: call
  `AnimationTrack:AdjustSpeed(0)`, then restore after 0.05 s (light), 0.08 s (medium) or 0.12 s
  (heavy/final blow). Do it client-side only, and never pause server simulation (API official;
  values inferred). The pause on impact is a fighting-game staple (press, 2022-08).
- Layer it with a white `Highlight` flash and a hit spark at the moment of the freeze (inferred).

## Highlights

- `Highlight` properties: `Adornee`, `DepthMode` (`AlwaysOnTop` or `Occluded`), `FillColor`,
  `FillTransparency`, `OutlineColor`, `OutlineTransparency`, `Enabled`. Only 255 highlights display
  at once, and extras are silently ignored. Disabled ones still count, so `Destroy()` finished ones
  (official, 2026-10).
- Values (inferred):

  | Use | `DepthMode` | Fill | Outline |
  |---|---|---|---|
  | Hover or interact target | `Occluded` | `FillTransparency = 1` | White, `OutlineTransparency = 0` |
  | Hit flash | `Occluded` | White, 0.2 → 1 over 0.12 s | `OutlineTransparency = 1` |
  | Objective or teammate through walls | `AlwaysOnTop` | 0.75 | Team color |

## Floating numbers

Per number (all inferred):
- A `BillboardGui` on an `Attachment` with `AlwaysOnTop = true` and `LightInfluence = 0`.
- `Size = UDim2.fromScale(4, 1.5)` (studs) and `MaxDistance = 80`.
- A Builder Sans ExtraBold `TextLabel` with a 2 px `UIStroke`.

Motion:
1. At spawn, pop `UIScale` 0.6 → 1.2 → 1 over 0.15 s.
2. Add random X jitter of ±0.5 stud.
3. Rise: tween `StudsOffset` +2.5 studs over 0.7 s `Quad`/`Out`.
4. Fade `TextTransparency` over the last 40%.

Color and limits:
- White for normal, yellow and 1.4× scale for crits, green for heals, the currency color for
  rewards.
- Merge ticks within 0.2 s on the same target.
- Cap at 15 live numbers and pool them.

## Haptics

- Use `HapticEffect` (`Type`: `UIHover`, `UIClick`, `UINotification`, `GameplayCollision`,
  `GameplayExplosion`, `Custom` via `SetWaveformKeys`; `Play()`, `Stop()`, `Looped`). It works on
  most iPhone, Pixel and Galaxy phones, PlayStation and Xbox pads, and Quest controllers. It
  supersedes `HapticService` for new work (official, 2026-10).
- Buttons take `GuiButton.PressHapticEffect` and `HoverHapticEffect` (official, 2026-10).
- Mapping (inferred):
  - `UIClick` on primary buttons.
  - `GameplayCollision` when taking damage or landing hard.
  - `GameplayExplosion` for boss slams and rebirth.
  - `UINotification` for rare drops.
- Never use haptics for routine collects.

## Feedback table per action

All values are starting points (inferred). "Confirm" means the moment the server's event arrives.

| Action | Visual | Sound | Camera / haptic | Timing |
|---|---|---|---|---|
| Click / collect | Item pops 1 → 1.3 → 0, 8–15 sparkle burst, icon flies to counter, counter punch + count-up | Pickup blip, vol 0.3–0.5, pitch ±8%, combo pitch-up | None | Burst on confirm, fly 0.35 s `Quad`/`In`, punch 0.08 + 0.15 s |
| Buy (confirmed) | Card flashes white, item icon pops into slot, "Purchased!" toast, currency counts down | Register "cha-ching", 0.6 | `UIClick` | Celebrate only after server grant; total < 1 s |
| Level up / rebirth | Full-screen radial flash (`ImageLabel`, 0.4 → 1 transparency), ring + sparkle burst on character, big title text pops (`Back`) | Rising arpeggio or fanfare, 0.7; duck music 50% for 1.5 s | FOV +6 kick; `GameplayExplosion` on rebirth | Title holds 1.2 s; whole sequence ≤ 2 s; skippable by tap |
| Rare drop / hatch reveal | Anticipation: egg shakes, accelerating over 0.8–1.5 s, screen dims to 0.5. Reveal: white flash, rarity-colored light rays, item pops `Back`/`Out`, name in rarity color + rarity label text | Build-up riser, then rarity-tiered sting (bigger for rarer) | Shake 0.5–1° on reveal (Legendary+ only); `UINotification` | Common reveals ≤ 1 s total; Legendary 2–3 s; tap skips |
| Hit / damage dealt | Hit spark, white `Highlight` flash 0.12 s, damage number | Impact thud, pitch ±10% | Hit-stop 0.05–0.12 s; shake 0.4–1.2° on heavy | Spark and sound on confirm; swing whoosh on input |
| Damage taken | Red screen-edge vignette (fades 0.3 s), character flash, health bar drains with a lagging white "ghost" segment | Grunt or thud, 0.5 | Shake 0.4°; `GameplayCollision` | Vignette and sound within 1 frame of the event |
| Death / respawn | Ragdoll or dissolve; desaturate world via `ColorCorrectionEffect` `Saturation` → -0.6 over 0.4 s; "Respawning 3…" | Low "whomp", music duck | Slow FOV +5 drift | Respawn ≤ 3 s; fade in 0.3 s, restore color 0.5 s |
| Checkpoint | Checkpoint part changes to the success color + `Neon`, upward particle column, "Stage 12!" toast | Bright chime, 0.5 | `UIClick` | Instant on touch confirm; toast 2 s |
| UI open / close | Panel scale 0.85 → 1 + fade in; background `BlurEffect` (in `Camera`) `Size` 0 → 12 | Soft whoosh or click, 0.3 | None | Open 0.25 s, close 0.15 s |
| Error / denied | Button shakes horizontally ±6 px 3 times, price text flashes red, toast says the fix ("Need 250 more Coins") | Short low "bonk", 0.4 | None (no shake) | Shake 0.25 s total; never a modal |

## Code sketch

```lua
--!strict
-- ReplicatedStorage/Shared/FX (client). Outline only.
local TweenService = game:GetService("TweenService")
local SoundService = game:GetService("SoundService")
local GuiService = game:GetService("GuiService")

local FX = {}
local rng = Random.new()
local lastPlayed: {[Sound]: number} = {}

function FX.pop(gui: GuiObject)
	local scale = gui:FindFirstChildOfClass("UIScale") :: UIScale?
	if not scale or GuiService.ReducedMotionEnabled then return end
	scale.Scale = 0.9
	TweenService:Create(scale, TweenInfo.new(0.15, Enum.EasingStyle.Back, Enum.EasingDirection.Out),
		{Scale = 1}):Play()
end

function FX.sound(template: Sound)
	local now = os.clock()
	if now - (lastPlayed[template] or 0) < 0.05 then return end -- rate limit
	lastPlayed[template] = now
	template.PlaybackSpeed = rng:NextNumber(0.92, 1.08)
	SoundService:PlayLocalSound(template)
end

return FX
```

Wire it up by connecting a `RemoteEvent.OnClientEvent` (server-confirmed outcomes) to `FX`
presets. Wire `GuiButton.Activated` to `FX.pop` and `FX.sound` for instant input feedback.

## Checklist for agents

### Do
- Give every action ≥ 3 feedback channels, scaled by importance: routine small, rare big.
- Play input feedback instantly on the client, and outcome feedback on server confirmation.
- Use explicit `TweenInfo` times (0.1–0.3 s for UI), `Back`/`Out` for pops, and `UIScale` for scaling.
- Use burst emitters with `Emit(n)` sized to the moment and scaled by quality level.
- Route all sounds through `SoundGroup`s with player sliders; randomize pitch; rate-limit repeats.
- Keep camera shake and FOV kicks on the client, small, and off under `ReducedMotionEnabled`.
- Use hit-stop plus a `Highlight` flash on confirmed hits, and `Destroy()` used highlights.
- Make long reveals skippable by tap.

### Don't
- Don't run tweens, particles or camera effects from server scripts.
- Don't celebrate purchases or rewards before the server confirms them.
- Don't use `TweenInfo`'s 1 s default, or `Elastic`/`Bounce` on routine UI.
- Don't set any SFX `Volume` above 1, or let identical sounds stack unlimited.
- Don't shake the camera for clicks, collects or menus, or exceed ~3°.
- Don't put a modal or toast on every coin; animate the counter instead.
- Don't rely on sound or color alone to signal an outcome.

## Related

- [ui-ux.md](ui-ux.md): button states, toasts, layout
- [visual-quality.md](visual-quality.md): rarity colors, post effects used in feedback
- [performance-and-devices.md](performance-and-devices.md): particle caps, remote budgets
- [rarity-tiers-and-eggs.md](../patterns/rarity-tiers-and-eggs.md): hatch-reveal design
- [ability-kits.md](../patterns/ability-kits.md): combat feedback
- [quality-bar.md](quality-bar.md): feel criteria in review

## Sources

1. https://www.youtube.com/watch?v=Fy0aCDmgnxg: "Juice it or lose it", Jonasson and Purho (2012): layering tweens, particles, sound, shake
2. https://www.youtube.com/watch?v=AJdEqssNZ-U: "The art of screenshake", Jan Willem Nijman, INDIGO Classes 2013
3. https://www.youtube.com/watch?v=tu-Qe66AvtY: "Math for Game Programmers: Juicing Your Cameras With Math" (GDC 2016): trauma-based shake
4. https://eventhubs.com/news/2022/aug/24/masahiro-sakurai-youtube-channel-games: Sakurai's video on hit stop (2022-08)
5. https://www.nngroup.com/articles/animation-duration/: 100–500 ms UI animation ranges, ease-out (2020-02)
6. https://create.roblox.com/docs/reference/engine/datatypes/TweenInfo: constructor defaults
7. https://create.roblox.com/docs/reference/engine/enums/EasingStyle: easing styles
8. https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter: Emit default count, properties
9. https://create.roblox.com/docs/reference/engine/classes/Sound: Volume range and default, PlaybackSpeed, roll-off
10. https://create.roblox.com/docs/reference/engine/classes/SoundGroup: multiplier volume, effects on groups
11. https://create.roblox.com/docs/reference/engine/classes/SoundService: PlayLocalSound
12. https://create.roblox.com/docs/reference/engine/classes/Camera: FieldOfView default and clamp
13. https://create.roblox.com/docs/reference/engine/enums/RenderPriority: Camera = 200
14. https://devforum.roblox.com/t/ez-camera-shake-ported-to-roblox/98482: community shake module and render-step pattern
15. https://create.roblox.com/docs/reference/engine/classes/Highlight: properties, 255 limit
16. https://create.roblox.com/docs/reference/engine/classes/HapticEffect: haptic effect API, device support
17. https://create.roblox.com/docs/reference/engine/enums/HapticEffectType: effect types
18. https://create.roblox.com/docs/reference/engine/classes/HapticService: superseded by HapticEffect
19. https://create.roblox.com/docs/reference/engine/classes/GuiButton: Activated, PressHapticEffect
20. https://create.roblox.com/docs/reference/engine/classes/GuiObject: TweenSize/TweenPosition deprecated
21. https://create.roblox.com/docs/production/publishing/accessibility: reduced motion, sound non-reliance, volume controls
22. https://create.roblox.com/docs/performance-optimization/improve: no server tweens, client-side effects, particle costs
23. https://create.roblox.com/docs/production/game-design/ui-ux-design: feedback examples (button states, purchase sound)

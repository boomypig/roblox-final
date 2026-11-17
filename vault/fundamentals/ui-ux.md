---
title: UI and UX
type: fundamental
read-when: Building any UI: HUD, shop, menus, notifications; mobile layout.
last-researched: 2026-10-22
---

# UI and UX

## In one line

Lay out for a landscape phone first. Keep everything inside the safe area, size it with Scale plus
constraints, and keep targets big and within thumb reach, clear of the thumbstick and jump button.
Give each screen one job, and make every button answer with a state change, a sound and motion.

## Ground truth

- ~80% of Roblox daily users played on mobile in 2024, 17% on PC and 3% on console
  (press, 2025-04). Build and review the phone layout first; desktop is the variant.
- The phone UI space is small. On the docs' sample phone the full screen is ~851×392 GUI px, and
  the area that clears the top bar and notch (`CoreUISafeInsets`) is 733×313 (official, 2026-10). GUI
  offset pixels on phones behave like logical points, not physical pixels (inferred from those
  sample sizes). So 48 offset px is about one fingertip.
- All API names and defaults below were checked against the engine reference on 2026-10-22.
  There is **no `UIFlexLayout` class**: flex layout is `UIListLayout` plus `UIFlexItem`
  (official, 2026-10).

## Safe areas and the top bar

| `ScreenGui` property | Default | Rule |
|---|---|---|
| `ScreenInsets` | `CoreUISafeInsets` | Keep this on every ScreenGui that has buttons. It stays clear of the Roblox top-bar buttons and device cutouts (official, 2026-10). |
| `ScreenInsets = None` | — | Only for non-interactive full-bleed layers such as fades, vignettes and backgrounds. UI here can sit under core UI or notches (official, 2026-10). |
| `ScreenInsets = DeviceSafeInsets` | — | Clear of notches, but not of the top bar. Setting `IgnoreGuiInset = true` switches `CoreUISafeInsets` to this (official, 2026-10). |
| `ScreenInsets = TopbarSafeInsets` | — | The strip in the top-bar row to the right of Roblox's buttons, for one small HUD item. On the docs' sample phone it is 58 px tall (official, 2026-10). |
| `IgnoreGuiInset` | `false` | Legacy switch. Set `ScreenInsets` explicitly instead (official, 2026-10). |
| `ClipToDeviceSafeArea` | `true` | Leave it on. It's ignored when `ScreenInsets = None` (official, 2026-10). |
| `SafeAreaCompatibility` | `FullscreenExtension` | Auto-patches old full-screen UI. The docs say not to rely on it for new work (official, 2026-10). |
| `ResetOnSpawn` | `true` (from `LayerCollector`) | Set `false` on HUD, shop and menu ScreenGuis, or they are rebuilt on every respawn and lose state (official behavior; rule inferred). |
| `DisplayOrder` | 0 | Convention: HUD 0, menus 10, modals 20, toasts 30, full-screen fades 100 (inferred). |

- Never hardcode the top-bar height. It was 36 px in older UI and is 58 px in current docs
  samples (community/official, 2026-10). Read `GuiService:GetGuiInset()`, or read
  `GuiService.TopbarInset` (a `Rect`) and listen with
  `GuiService:GetPropertyChangedSignal("TopbarInset")`, because it changes at runtime
  (official, 2026-10).
- `GuiService:GetInsetArea(Enum.ScreenInsets.CoreUISafeInsets)` returns the usable `Rect` for any
  inset type. Use it to place things precisely (official, 2026-10).
- Top-left belongs to Roblox: the menu and chat buttons, plus the optional global **Shop** button
  that Roblox recommends enabling (official, 2026-10). Never put your own UI there.

## Phone layout map (landscape)

Reserved by default controls (keep interactive UI out):
- **Bottom-left, the thumbstick.** The dynamic thumbstick's touch frame covers the left 40% of the
  width × the bottom 2/3 of the height in landscape (community: Roblox PlayerModule source mirror,
  2026-10). Keep the lower-left ~40% × lower ~45% free of buttons (inferred).
- **Bottom-right, the jump button.** It is 70 px when the screen's short side is ≤ 500 px, else
  120 px. On small screens it sits ~25–95 px from the right edge and ~20–90 px from the bottom
  (community: PlayerModule source, 2026-10). The docs reserve both bottom corners
  (official, 2026-10).
- **Bottom-center:** the default Backpack hotbar, if you keep it.
- **Top-right:** the player list when it is open.

| Element | Place | Size on a ~390-px-tall phone |
|---|---|---|
| Currency/stat counters | Top-left under the top bar, or upper left edge; `AnchorPoint = (0, 0)` | Height ~8% of screen (≈30 px), text 20–28 px |
| Menu buttons (Shop, Pets, Rebirth…) | One narrow column on the left edge, vertically centered (y 30–60%). This is the common simulator pattern (inferred) | ≥ 48 px square, 8 px gaps |
| Gameplay action buttons | Arc around the jump button. The docs' sample uses 0.8× the jump size, 20 px apart (official, 2026-10) | 56–70 px |
| Timer, round status, quest tracker | Top-center or top-right, below the top bar | Text 18–24 px |
| Toasts | Top-center, below the top bar | Max 3 stacked |
| Modals (shop, inventory) | Centered | ≤ 80% width × 85% height of the safe area |

- Thumb reach differs by device: a button 40% down from the top is reachable on a phone but not on
  a tablet. The docs' fix is to position custom buttons relative to the jump button, found with
  `PlayerGui:FindFirstChild("JumpButton", true)` (official, 2026-10).
- Show context buttons only when relevant. For example, use a `ProximityPrompt` for "Open" near a
  chest instead of a permanent button (official, 2026-10).
- Minimum tap target: 48×48 px with ≥ 8 px between targets. This follows Android's 48×48 dp
  (~9 mm) guidance (community: platform guideline, 2026-10).

## Sizing: Scale first, then constrain

1. Position with Scale, and set `AnchorPoint` to the edge the element hugs (`(1, 0)` for
   top-right, `(0.5, 1)` for bottom-center), so it grows inward (official, 2026-10).
2. Size from the screen's short side. `Size = UDim2.fromScale(1, 0.12)` plus a
   `UIAspectRatioConstraint` (`AspectRatio = 1`, `AspectType = FitWithinMaxSize`) gives a square that
   is 12% of the parent's height. That's ≈47 px on a 392-px phone (inferred from documented
   constraint behavior).
3. Cap big screens with `UISizeConstraint.MaxSize`, for example 110×110 for HUD buttons. A 75%-wide
   panel is huge on a 4K TV (official, 2026-10).
4. Constraints override `UIListLayout`/`UIGridLayout` sizing, so check layouts after adding them
   (official, 2026-10).
5. Adapt by device class with `GuiService.ViewportDisplaySize` (`Small` = phones and tablets,
   `Medium` = laptops and monitors, `Large` = TVs), not by guessing from pixels (official, 2026-10).
   Example: a root `UIScale.Scale` of 1 on Small and Medium, 1.25 on Large (inferred).
6. `UIScale` multiplies everything under it, including `UIStroke` and `UICorner`. Use it for pops
   and whole-panel scaling instead of tweening `Size` (official, 2026-10).
7. Layout: use `UIListLayout` with `Padding`, `SortOrder = LayoutOrder`, and optionally
   `HorizontalFlex`/`VerticalFlex` (`Enum.UIFlexAlignment`: `None`, `Fill`, `SpaceAround`,
   `SpaceBetween`, `SpaceEvenly`), `Wraps`, and `ItemLineAlignment`. A child `UIFlexItem` with
   `FlexMode = Grow/Shrink/Fill/Custom` (`GrowRatio`, `ShrinkRatio`) controls each item. Use
   `UIGridLayout` for item grids, inside a `ScrollingFrame` with `AutomaticCanvasSize`
   (official, 2026-10).
8. Use `AutomaticSize = Y` for anything holding variable text, such as localized strings and
   descriptions (official, 2026-10).

## Text

- Font: Builder Sans (`Enum.Font.BuilderSans`, `BuilderSansMedium`, `BuilderSansBold`,
  `BuilderSansExtraBold`). Set it via `FontFace = Font.fromEnum(Enum.Font.BuilderSansBold)`.
  Gotham was removed on 2024-05-28 (official, 2024-05). Use at most 2 font families per game
  (inferred).
- Sizes on a ~390-px-tall phone, as starting points: HUD numbers 20–28 px, button labels 16–20,
  body 14–16, never below 12 (inferred). The docs' floor is `MinTextSize` ≥ 9 (official, 2026-10).
- For short labels (buttons, counters), use `TextScaled = true` plus a `UITextSizeConstraint`
  (`MinTextSize = 14`, `MaxTextSize = 36`). Its defaults are 1 and 1000 (official, 2026-10).
- For sentences, use a fixed `TextSize`, `TextWrapped = true` and `AutomaticSize = Y`.
  `TextScaled` ignores the player's text-size setting (official, 2026-10).
- Text over the 3D world gets a `UIStroke` (`ApplyStrokeMode = Contextual`): black or a dark palette
  color, `Thickness` 1.5–2.5, or `StrokeSizingMode = ScaledSize` so it follows font size
  (API official; values inferred). Don't tween a text stroke's `Thickness`; it re-renders glyphs
  every frame (official, 2026-10).
- Abbreviate big numbers (1,234 → 1.2K → 3.4M → 5.6B) and keep the suffix style the same
  everywhere (inferred).

## Visual language

- `UICorner.CornerRadius`: use Scale 0.15–0.25 for cards and buttons. A Scale ≥ 0.5 makes a pill at
  any size. Per-corner radii exist (`TopLeftRadius` etc.) (official API; values inferred).
- On a non-text object, `UIStroke` draws a border. `BorderStrokePosition` is `Inner`, `Center` or
  `Outer` (official, 2026-10). Use 2–3 px darker-shade borders on buttons for the chunky Roblox
  look (inferred).
- `UIGradient`: `Color`, `Transparency`, `Rotation` and `Offset` are stable. `Type`, `Scale` and
  `TileMode` need Studio's "Upgraded UIGradients" beta (official, 2026-10), so don't use them in
  shipping UI.
- Follow Roblox's documented conventions (official, 2026-10):
  - X closes a dialog.
  - Gray means unusable.
  - A lock icon means locked.
  - One color per stat everywhere (e.g. health = green in text, icon and bar).
  - Unaffordable prices show in red.
  - Headers are bigger and bolder than body text.
  - Buttons sit on a contrasting container.
  - Vibrant colors mark key elements; muted colors mark everything else.
  - Write the rules down in a style guide.
- Icon language: one icon set, one stroke weight, one perspective, and the same icon for the same
  concept everywhere. A currency icon goes beside every price and every counter (inferred).
- Keep colors and sizes as tokens in one place: a `UIConfig` ModuleScript, or UI styling
  (`StyleSheet` with tokens, `StyleRule` with selectors such as `".ButtonPrimary"`, and a
  `StyleLink` on the ScreenGui) (official, 2026-10).

## Buttons and states

- Handle `GuiButton.Activated`, which fires for mouse, touch and gamepad A, not
  `MouseButton1Click`. Button events are client-only (official, 2026-10).
- Show four states: idle, hover (desktop), pressed, and disabled. Disable with
  `GuiObject.Interactable = false`, which sets `GuiState` to `NonInteractable`; render it gray with a
  lock icon or a reason (official API; style inferred).
- Press feedback: `UIScale` 1 → 0.92 on press, back to 1 with `Back`/`Out` over 0.15 s, plus a click
  sound and `GuiButton.PressHapticEffect` (a `HapticEffect` with `Type = UIClick`)
  (API official; values inferred). Timings are in [game-feel](game-feel.md).
- Set `AutoButtonColor = false` when you animate states yourself (inferred).
- Lock the button while waiting on the server. Show a spinner if the reply takes > 0.3 s, and
  never let a double tap send two requests (inferred).

## Input type and mobile buttons

- Detect input with `UserInputService.PreferredInput` (`Enum.PreferredInput.Touch`,
  `KeyboardAndMouse`, `Gamepad`). Read it at start and on
  `GetPropertyChangedSignal("PreferredInput")`. The docs prefer it over
  `TouchEnabled`/`KeyboardEnabled`/`GamepadEnabled`/`GetLastInputType()` for cross-platform UI
  (official, 2026-10).
- Show prompts for the current input: `InputActionLabel` (beta), or
  `UserInputService:GetImageForKeyCode()` / `GetStringForKeyCode()` (official, 2026-10). Hide key
  hints like "[E]" on touch.
- New on-screen action buttons use the **Input Action System**: an `InputContext` holds an
  `InputAction` (`Type = Bool`), which holds `InputBinding`s with `KeyCode` (keyboard/gamepad) and
  `UIButton` (your own `ImageButton`). Listen on `InputAction.Pressed`/`Released` (official, 2026-10).
- Legacy alternative: `ContextActionService:BindAction(name, fn, true, ...)` creates a touch button
  in `ContextActionGui`; style it with `SetPosition`, `SetImage` and `SetTitle` (official, 2026-10).
  Use one system per action, never both.
- `GuiService.TouchControlsEnabled = false` hides the default thumbstick and jump button. Only do
  this if you replace them (official, 2026-10).

## Gamepad and console

- When a menu opens and `PreferredInput == Gamepad`, call `GuiService:Select(menuFrame)`. It focuses
  the selectable descendant with the lowest `SelectionOrder`. On close, set
  `GuiService.SelectedObject = nil` (official, 2026-10).
- Set `Selectable = true` only on real buttons. Set explicit `NextSelectionUp/Down/Left/Right` where
  auto-navigation picks wrong, for example the last item in a grid row (official, 2026-10).
- Trap focus in a modal with `SelectionGroup = true` and
  `SelectionBehaviorUp/Down/Left/Right = Enum.SelectionBehavior.Stop` (official, 2026-10).
- `ButtonB` cancels or closes and `ButtonA` confirms (official, 2026-10). Map Escape/B to the same
  close function as the X button.
- For a custom focus ring, use `SelectionImageObject`. Detect TVs by
  `ViewportDisplaySize == Large`, not `IsTenFootInterface()` (official, 2026-10).

## Shop UX that converts without annoying

- **Entry:** one Shop button in a fixed HUD spot, with icon and label, one tap to open. The close X
  is ≥ 48 px in the panel's top-right. A background tap and B/Escape also close it (inferred).
- **Card:** icon, name, one benefit line ("2× Coins forever"), price with the Robux glyph, and one
  CTA. Mark the best-value item with extra size or padding and a ribbon. The docs cite a game that
  enlarges its top coin bundle (official, 2026-10). Show "Owned" for owned passes, checked with
  `MarketplaceService:UserOwnsGamePassAsync`.
- **Prices:** never hardcode them. Read them at runtime with
  `MarketplaceService:GetProductInfoAsync` (`GetProductInfo` is deprecated), because regional
  pricing for developer products can differ per player (official, 2025). Display only; the server
  validates.
- Robux glyph in text: `utf8.char(0xE002)` renders the Robux icon (community, unverified). Check it
  at small sizes or use an `ImageLabel`.
- **Flow:** the client calls `PromptProductPurchase`/`PromptGamePassPurchase`. The server grants in
  `ProcessReceipt`. Celebrate only on the server's confirmation, never on
  `PromptProductPurchaseFinished` (official, 2026-10). See [monetization](monetization.md) and
  [shops](../patterns/shops.md).
- **Restraint** (inferred):
  - No shop or offer pop-up in the first 3 minutes of a session.
  - At most one contextual offer per ~10 minutes, and only at a natural pause (after a death, at a
    locked area, when out of currency).
  - Never stack modals, and never open one over active gameplay.
  - "Not now" is always visible.
  - Only one modal is open at a time.
- Roblox's own Shop surface lists all passes and listed products and is on by default in the
  in-game menu. Keep it on unless your own shop fully replaces it
  (`StarterGui:SetCoreGuiEnabled(Enum.CoreGuiType.ExperienceShop, false)`) (official, 2026-10).

## Notifications and toasts

- Toasts go top-center below the top bar: max 3 visible, newest on top, 2.5–4 s on screen.
  Animate in over 0.2 s (`Back`/`Out`) and fade out over 0.15 s (inferred).
- Merge duplicates: three "+5 Coins" toasts become one "+15 Coins" with a pop (inferred).
- Priority: rare drops and errors interrupt; routine gains only animate the counter, not a
  toast (inferred).
- Error text says what is missing and the fix: "Need 250 more Coins", not "Error" or
  "Purchase failed" (inferred).
- Never use a full-screen modal for information a toast can carry (inferred).

## Accessibility

- `GuiService.PreferredTextSize` is `Medium` (default), `Large`, `Larger` or `Largest`. Fixed
  `TextSize` text respects it; `TextScaled` text doesn't (official, 2026-10). Test at `Largest`.
- `GuiService.PreferredTransparency` (1 = default, 0 = opaque): multiply panel
  `BackgroundTransparency` by it (official, 2026-10).
- `GuiService.ReducedMotionEnabled`: when true, set tween time to 0, or fade a `CanvasGroup`'s
  `GroupTransparency` instead of moving the element (official, 2026-10).
- Over 5% of people have some color blindness (official, 2026-10). Pair every color signal with an
  icon, shape or text, and avoid red-vs-green-only pairs (official rule; pair inferred).
- Use high text/background contrast. The docs give no ratio; aim for WCAG's 4.5:1 for body text
  (inferred).
- Never signal with sound alone, and offer separate SFX, music and UI volume sliders
  (official, 2026-10).

## Testing with the Device Simulator

1. In Studio's Device Simulator toolbar, pick **Phone** and an **Entry level** profile in landscape,
   with **Display scaling** = **Actual resolution** (official, 2026-10). Some builds need
   **File > Beta Features > New Device Simulator** (official, 2026-10).
2. Play-test: all text readable, no overlap with the thumbstick, jump button or top bar, every
   button ≥ 48 px, and every modal closable with one tap.
3. Repeat on a flagship phone, then a tablet, **Desktop**, and **Console** with the Controller
   Emulator. Navigate every menu with the gamepad only (official, 2026-10).
4. Set the player Text Size to Largest and Reduced Motion on, and recheck.
5. The simulator doesn't model phone performance; see
   [performance-and-devices](performance-and-devices.md).

## Checklist for agents

### Do
- Set `ScreenInsets = CoreUISafeInsets` and `ResetOnSpawn = false` on every interactive ScreenGui.
- Position with Scale and anchors. Size with Scale plus `UIAspectRatioConstraint`, capped with
  `UISizeConstraint`.
- Make every tap target ≥ 48 px with ≥ 8 px gaps, outside the thumbstick and jump zones.
- Use Builder Sans, `UITextSizeConstraint` on scaled text, and `UIStroke` on text over 3D.
- Use `Activated`, four button states, and a `UIScale` press pop with sound.
- Adapt to `PreferredInput` and `ViewportDisplaySize`, and select the first button for gamepad.
- Fetch prices with `GetProductInfoAsync`, use one CTA per card, and grant purchases server-side.
- Respect `PreferredTextSize`, `PreferredTransparency` and `ReducedMotionEnabled`.
- Test in the Device Simulator on an entry-level phone before calling UI done.

### Don't
- Don't hardcode the top-bar height (36 or 58) or design at desktop size and shrink it to phones.
- Don't put buttons in the top-left, lower-left or bottom-right corners.
- Don't use `UIFlexLayout` (it doesn't exist), deprecated `TweenSize`/`TweenPosition`, or beta
  gradient types.
- Don't convey state by color alone, or put text below 12 px on a phone.
- Don't auto-open the shop, stack pop-ups, or hide the close button.
- Don't hardcode Robux prices or grant on `PromptProductPurchaseFinished`.

## Related

- [game-feel.md](game-feel.md): button pops, toast motion, sounds and haptics
- [visual-quality.md](visual-quality.md): palette shared between UI and world
- [performance-and-devices.md](performance-and-devices.md): sprite sheets, texture budgets, devices
- [first-time-experience.md](first-time-experience.md): HUD in the first minutes
- [monetization.md](monetization.md) and [shops](../patterns/shops.md): purchase code
- [quality-bar.md](quality-bar.md): "done" criteria

## Sources

1. https://www.pocketgamer.biz/80-of-roblox-users-are-on-mobile-contributing-46-of-robux-revenue/: 80/17/3% device split, 2024 data (2025-04)
2. https://create.roblox.com/docs/reference/engine/classes/ScreenGui: ScreenInsets, IgnoreGuiInset, ClipToDeviceSafeArea, SafeAreaCompatibility defaults
3. https://create.roblox.com/docs/ui/on-screen-containers: CoreUISafeInsets default and purpose
4. https://create.roblox.com/docs/reference/engine/classes/GuiService: TopbarInset, GetGuiInset, GetInsetArea sample rects, ViewportDisplaySize, Select, accessibility properties
5. https://devforum.roblox.com/t/screenguiscreeninsets-topbarinsets-regression/4047230: 58 px top-bar inset in practice
6. https://create.roblox.com/docs/ui/cross-platform-design: reserved corners, thumb zones, jump-relative button sample
7. https://create.roblox.com/docs/projects/cross-platform: ViewportDisplaySize, PreferredInput, 4K scaling, input prompts, emulators
8. https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/scripts/PlayerScripts/StarterPlayerScripts/PlayerModule.module/ControlModule/TouchJump.lua: jump button size and position
9. https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/scripts/PlayerScripts/StarterPlayerScripts/PlayerModule.module/ControlModule/DynamicThumbstick.lua: thumbstick touch area
10. https://support.google.com/accessibility/android/answer/7101858: 48×48 dp targets, 8 dp spacing
11. https://create.roblox.com/docs/ui/size-modifiers: UIScale, UIAspectRatioConstraint, UISizeConstraint, UITextSizeConstraint, AutomaticSize
12. https://create.roblox.com/docs/ui/appearance-modifiers: UIStroke, UICorner, UIGradient beta properties
13. https://create.roblox.com/docs/reference/engine/enums/StrokeSizingMode: FixedSize vs ScaledSize
14. https://create.roblox.com/docs/reference/engine/classes/UIListLayout: flex properties and enums
15. https://create.roblox.com/docs/reference/engine/classes/UIFlexItem: FlexMode, ratios
16. https://create.roblox.com/docs/reference/engine/classes/UITextSizeConstraint: defaults, min 9
17. https://devforum.roblox.com/t/2868222: Builder font family, Gotham removal date
18. https://create.roblox.com/docs/reference/engine/enums/Font: BuilderSans enum items
19. https://create.roblox.com/docs/reference/engine/classes/GuiButton: Activated, haptic properties
20. https://create.roblox.com/docs/reference/engine/classes/GuiObject: Interactable, selection properties, deprecated TweenSize/TweenPosition
21. https://create.roblox.com/docs/reference/engine/classes/GuiBase2d: SelectionGroup and SelectionBehavior
22. https://create.roblox.com/docs/reference/engine/classes/UserInputService: PreferredInput and recommendations
23. https://create.roblox.com/docs/input/input-action-system: InputContext/InputAction/InputBinding, UIButton
24. https://create.roblox.com/docs/reference/engine/classes/ContextActionService: BindAction touch buttons
25. https://create.roblox.com/docs/input/gamepad: ButtonA accept, ButtonB cancel
26. https://create.roblox.com/docs/ui/styling: StyleSheet, StyleRule, StyleLink, tokens
27. https://create.roblox.com/docs/production/game-design/ui-ux-design: conventions, consistency, hierarchy, feedback
28. https://create.roblox.com/docs/production/publishing/accessibility: text size, transparency, reduced motion, color and sound non-reliance
29. https://create.roblox.com/docs/production/monetization/shop: Roblox Shop surface, global Shop button, ExperienceShop CoreGuiType
30. https://create.roblox.com/docs/reference/engine/classes/MarketplaceService: GetProductInfoAsync, deprecations, ProcessReceipt rule
31. https://create.roblox.com/docs/production/monetization/regional-pricing: fetch prices at runtime
32. https://devforum.roblox.com/t/introducing-regional-pricing-for-developer-products/3971235: regional pricing announcement
33. https://devforum.roblox.com/t/how-to-use-built-in-robux-icons/3081879: Robux glyph U+E002
34. https://create.roblox.com/docs/studio/device-simulator: profiles, scaling modes, beta flag

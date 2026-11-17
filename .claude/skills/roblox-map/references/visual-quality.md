---
title: Visual quality
type: fundamental
read-when: Setting lighting/atmosphere, choosing materials and colors, building maps.
last-researched: 2026-10-22
---

# Visual quality

## In one line

Pick a lighting preset on day one: `LightingStyle`, `Atmosphere`, a real `Sky` and restrained post
effects. Then build with a limited palette, real materials, beveled and varied shapes, and
readable hazards and landmarks. Lighting does half the work, but it can't save default gray blocks.

## Lighting: `LightingStyle` replaced `Technology`

- `Lighting.Technology` is **deprecated**. Unified Lighting went fully live on 2025-07-23 and
  replaced it with `Lighting.LightingStyle` (`Realistic` or `Soft`) and
  `Lighting.PrioritizeLightingQuality` (official, 2025-07). Never write `Technology = Future` in a
  new build.

  | Old `Technology` | `LightingStyle` | `PrioritizeLightingQuality` |
  |---|---|---|
  | `Future` | `Realistic` | `true` |
  | `ShadowMap` | `Soft` | `true` |
  | `Voxel` | `Soft` | `false` |

  (official, 2025-07)
- **Neither property is scriptable** (official, 2025-07). Set them in Studio's Properties panel. If
  the MCP's Luau can't set them, ask the user to set them, and list it in your report (inferred).
- New places start on `Soft` (official, 2026-10).
  - Use `Realistic` whenever local lights matter (night, interiors, neon arenas) or for
    high-fidelity scenes.
  - Use `Soft` for the flat classic Roblox look (official, 2025-07).
- `PrioritizeLightingQuality = true` keeps shadows and shaders and lowers draw distance first on
  weaker devices (official, 2025-07). Use `true` for horror, night and interiors, and `false` for big
  open simulators where far visibility matters (inferred).
- `ShadowSoftness` (0 = hard, 1 = soft; reference default 0.2) only applies under `Realistic`
  (official, 2026-10).
- Shadows switch off below graphics quality level 4, so never make a shadow the only cue for a
  gameplay object (official, 2026-10).

| Property | Reference default | What it does / rule |
|---|---|---|
| `Brightness` | — | Sun/moon intensity; higher = more lit-vs-shadow contrast. The docs' examples are 0.5–3.75 (official, 2026-10). |
| `Ambient` | (0, 0, 0) | Light color where the sky is blocked (indoors, under overhangs) (official, 2026-10). |
| `OutdoorAmbient` | (127, 127, 127) | Light color outdoors; fills shadows (official, 2026-10). |
| `EnvironmentDiffuseScale` | 0 | Ambient light taken from the sky. When raising it, lower `Ambient`/`OutdoorAmbient` (official, 2026-10). |
| `EnvironmentSpecularScale` | 0 | Sky reflections on smooth or metal surfaces. Near 1 looks realistic (official, 2026-10). Use 0.2–0.5 for cartoon styles (inferred). |
| `ExposureCompensation` | 0 (−5 to 5) | +1 = 2× exposure, −1 = half (official, 2026-10). |
| `ClockTime` / `TimeOfDay` | — | Time in hours, e.g. 14 = 14:00. Doesn't advance unless a script changes it (official, 2026-10). |
| `GeographicLatitude` | — | Moves the sun path without changing time; use it to angle shadows (official, 2026-10). |
| `ColorShift_Top` / `_Bottom` | — | Tint on surfaces facing toward / away from the sun (official, 2026-10). |
| `GlobalShadows` | `true` | Sun shadows on or off (official, 2026-10). |

- Local lights (`PointLight`, `SpotLight`, `SurfaceLight`) default to `Brightness = 1`
  (official, 2026-10). Keep `Range` ≤ 60 studs. The reference now says light range clamps at 120,
  but older posts report 60 (official/community, 2026-10). Set `Shadows = true` only on the few
  lights that need them; budgets are in [performance](performance-and-devices.md).

## Atmosphere, Sky, Clouds

- Every outdoor map gets an `Atmosphere` in `Lighting`. Its presence hides the legacy
  `FogStart`/`FogEnd`/`FogColor` (official, 2026-10).
- `Density` controls how much distance is obscured (class default ≈ 0.395) (community, 2026-10).
  `Offset` raises it to silhouette distant objects against the sky, or lowers it to blend them in.
  Too low an `Offset` lets the skybox ghost through terrain; too high shows LOD popping
  (official, 2026-10).
- `Haze` adds haze above the horizon and in the distance; tint it with `Color`. `Glare` (sun glow)
  needs `Haze` > 0. `Decay` (hue away from the sun) needs both `Haze` and `Glare` > 0
  (official, 2026-10).
- `Sky`: replace the default skybox with six `Skybox*` faces (`SkyboxBk/Dn/Ft/Lf/Rt/Up`) that suit
  the style. `SunAngularSize` defaults to 21 and is clamped 0–60. `StarCount`, `MoonAngularSize`,
  `CelestialBodiesShown` and `SkyboxOrientation` are also available (official, 2026-10). A default
  sky signals "unfinished" (inferred).
- A `Clouds` object under `Terrain` has `Cover` (0–1), `Density` (0–1) and `Color`
  (official, 2026-10). Use it for cheap depth on open maps (inferred).

## Post effects

- Parent effects to `Lighting` for everyone, or to `Workspace.CurrentCamera` for one player, e.g. a
  blur behind an open menu (official, 2026-10).
- The class defaults are too strong for gameplay. A fresh `BloomEffect` is `Intensity 0.4`,
  `Size 24`, `Threshold 0.95`. `SunRaysEffect` is `Intensity 0.25`, `Spread 1`. A fresh
  `DepthOfFieldEffect` (`FarIntensity 0.75`, `FocusDistance 0.05`, `InFocusRadius 10`,
  `NearIntensity 0.75`) blurs everything past ~10 studs (community, 2026-10).
- `BloomEffect.Threshold = 1` blooms only pure white (official, 2026-10). Neon only glows through
  bloom: `Neon` parts don't light anything, so add a `PointLight` if they should (inferred).
- `ColorCorrectionEffect` is neutral at `Brightness = 0`, `Contrast = 0`, `Saturation = 0`,
  `TintColor = (255, 255, 255)`. `Saturation = -1` is grayscale, and `TintColor` multiplies the
  channels (official, 2026-10).
- `ColorGradingEffect.TonemapperPreset`: `Default` is the vivid post-2019 look, and `Retro` is the
  flatter pre-2019 look (official, 2026-10).
- `DepthOfFieldEffect` stays off during gameplay. Use it only for menus, shops and cutscenes
  (inferred). Low-end devices may render it differently (official, 2026-10).

## Four presets (starting points)

All values are starting points to tune (inferred), not tested defaults. Apply one, screenshot on
an entry-level phone profile in the Device Simulator, and adjust `Brightness`/`ExposureCompensation`
first. Colors are RGB 0–255.

| Property | Bright cartoon day | Golden hour | Night / horror | Stylized neon arena |
|---|---|---|---|---|
| `LightingStyle` | `Soft` | `Realistic` | `Realistic` | `Realistic` |
| `PrioritizeLightingQuality` | `false` | `true` | `true` | `true` |
| `Brightness` | 3 | 2.5 | 0.6 | 1 |
| `ClockTime` | 14 | 17.6 | 0 | 21 |
| `GeographicLatitude` | 35 | 40 | 30 | 30 |
| `Ambient` | (70, 70, 85) | (60, 45, 40) | (8, 8, 14) | (30, 15, 45) |
| `OutdoorAmbient` | (140, 140, 155) | (150, 105, 80) | (30, 35, 55) | (50, 35, 80) |
| `ColorShift_Top` | (0, 0, 0) | (255, 180, 110) | (0, 0, 0) | (0, 0, 0) |
| `EnvironmentDiffuseScale` | 0.5 | 1 | 0.3 | 0.5 |
| `EnvironmentSpecularScale` | 0.25 | 0.6 | 0.5 | 1 |
| `ExposureCompensation` | 0 | 0.2 | −0.2 | 0 |
| `ShadowSoftness` | — (Soft ignores) | 0.15 | 0.3 | 0.2 |
| Atmosphere `Density` | 0.25 | 0.35 | 0.5 | 0.3 |
| Atmosphere `Offset` | 0.25 | 0.1 | 0 | 0 |
| Atmosphere `Color` | (200, 220, 255) | (255, 200, 150) | (40, 45, 65) | (120, 80, 200) |
| Atmosphere `Decay` | (140, 160, 200) | (180, 110, 90) | (20, 20, 30) | (40, 20, 80) |
| Atmosphere `Glare` | 0 | 1.5 | 0 | 0 |
| Atmosphere `Haze` | 0.5 | 1.8 | 2.5 | 1.5 |
| Bloom `Intensity` / `Size` / `Threshold` | 0.5 / 24 / 1.6 | 0.8 / 30 / 1.2 | 0.4 / 24 / 1.5 | 1.2 / 32 / 0.9 |
| ColorCorrection `Brightness` / `Contrast` / `Saturation` | 0.02 / 0.08 / 0.15 | 0 / 0.1 / 0.1 | −0.02 / 0.15 / −0.35 | 0 / 0.15 / 0.25 |
| ColorCorrection `TintColor` | (255, 255, 255) | (255, 240, 225) | (210, 220, 255) | (255, 245, 255) |
| SunRays `Intensity` / `Spread` | 0.05 / 0.5 | 0.12 / 0.8 | disabled | disabled |
| DepthOfField | off | off | off | off |

Notes per preset (inferred):
- **Bright cartoon day** (obby, simulator, tycoon): saturated palette, `SmoothPlastic` or light
  materials, and a stylized sky. Keep `OutdoorAmbient` high so shadows never go black on phones.
- **Golden hour** (hangouts, adventure hubs, trailers): low sun gives long shadows, so face
  landmarks toward the sun. Warm key light, cool shadows.
- **Night / horror**: darkness from fog and low ambient, not from black screens. Keep
  `OutdoorAmbient` ≥ (25, 25, 35) so phone players at low screen brightness can still read the floor.
  Light the path with a few warm `PointLight`s (`Range` 12–20, `Brightness` 1–2) and a player
  `SpotLight` flashlight.
- **Neon arena** (shooters, battlegrounds, rhythm): dark, slightly reflective floors
  (`SmoothPlastic`/`Metal` with `Reflectance` 0.1–0.2), `Neon` trim in 2 team colors, and bloom
  `Threshold` < 1 so `Neon` glows. Add a few `SurfaceLight`s to cast the colors.

## Materials

- Use built-in 2022 materials before custom textures; they are the cheapest (official, 2026-10).
  `Enum.Material` includes:
  - Stone: `Concrete`, `Brick`, `Cobblestone`, `Slate`, `Granite`, `Basalt`, `Limestone`,
    `Sandstone`, `Marble`, `Pavement`, `Asphalt`
  - Wood and metal: `Wood`, `WoodPlanks`, `Metal`, `DiamondPlate`, `CorrodedMetal`, `Foil`
  - Nature: `Grass`, `LeafyGrass`, `Ground`, `Mud`, `Sand`, `Snow`, `Ice`, `Glacier`, `Rock`,
    `Pebble`, `Salt`, `CrackedLava`
  - Interiors: `Fabric`, `Carpet`, `Leather`, `Plaster`, `CeramicTiles`, `ClayRoofTiles`,
    `RoofShingles`, `Cardboard`, `Rubber`
  - Specials: `SmoothPlastic`, `Plastic`, `Neon`, `Glass`, `ForceField`

  (official, 2026-10)
- Style rules (inferred):
  - **Stylized/cartoon:** mostly `SmoothPlastic` plus 2–3 textured materials for ground, wood and
    stone.
  - **Grounded:** textured materials everywhere, with `Color` tuned toward the palette.
  - `Neon` only for emissive accents (≤ ~5% of what's on screen).
  - `Glass` and `ForceField` sparingly: partial transparency costs overdraw (official, 2026-10).
- `MaterialVariant` (inside `MaterialService`) is identified by `Name` + `BaseMaterial`. It has
  `ColorMap`, `NormalMap`, `RoughnessMap`, `MetalnessMap`, `StudsPerTile` and emissive settings.
  Assign it per part with `BasePart.MaterialVariant = "Name"`, or game-wide by naming it in a
  `MaterialService` override (e.g. `PlasticName`) or with `MaterialService:SetBaseMaterialOverride`
  (official, 2026-10). Use variants to fix tiling scale (`StudsPerTile`) or to restyle a material
  everywhere at once (inferred).
- `SurfaceAppearance` (PBR maps for `MeshPart`s only): its `Color` tints the `ColorMap`, so one
  texture serves many colors. Most of its properties can't be changed at runtime (official,
  2026-10). Texture size and instancing rules are in [performance](performance-and-devices.md).
- `Terrain`: paint ground with ≥ 2 materials (path vs field). `Terrain.Decoration` gives animated
  grass (`GrassLength` 0.1–1), and `Terrain:SetMaterialColor()` shifts a terrain material toward
  your palette (official, 2026-10).

## Color and palette

- Use a limited palette (inferred):
  - 1 ground/neutral family (3 values: light, mid, dark)
  - 2 supporting hues for structures and zones
  - 1 **accent** reserved for interactables and rewards
  - 1 **danger** color reserved for hazards

  That's ≤ 5 hues plus neutrals, stored as `Color3` constants in a shared `Palette` ModuleScript
  that the UI also uses.
- Value contrast first: walkable surfaces are mid-value, hazards and collectibles differ from them
  in **brightness**, not just hue. Check it by temporarily setting `ColorCorrectionEffect.Saturation`
  to -1. If you can't tell lava from floor in grayscale, change values (method inferred; property
  official).
- Saturation hierarchy: the background is desaturated, and gameplay objects are saturated. This
  mirrors Roblox's UI guidance of vibrant colors for crucial elements and muted ones for the rest
  (official principle, 2026-10; world application inferred).
- Avoid pure white (255, 255, 255) on large surfaces, because it blooms and flattens. Avoid pure
  black, because it hides shape on phones (inferred).

## Readability

- **Hazards** look the same game-wide: the danger color, a distinct material (`Neon` or
  `CrackedLava`), and motion (pulse or spin) or a spiky shape. Never use red/orange on safe
  surfaces. Never signal danger by color alone or by shadow alone (inferred; shadow rule official,
  2026-10).
- **Safe ground** is neutral and calm. Lead the main path with a lighter or brighter material
  strip, light, or particles (inferred).
- **Collectibles and interactables** use the accent color. Add a `Sine` bob and spin, a sparkle
  emitter, and a `ProximityPrompt` or hover `Highlight` (inferred). Feedback is in
  [game-feel](../../roblox-vfx/references/game-feel.md).
- **Silhouettes:** keep characters and enemies readable against mid-value backgrounds, and
  separate depth layers with `Atmosphere` (inferred).
- **Landmarks:** each zone gets one tall, unique silhouette visible from spawn, and its own hue.
  Roblox's environment-art curriculum color-codes zones, gives each area a unique hue, and uses
  floor material to separate indoors from outdoors (official, 2026-10).
- **Scale:** avatars are ~5 studs tall. Use doorways ≥ 8 studs tall, corridors ≥ 8 studs wide, and
  obby jumps tuned to the default jump, not eyeballed (inferred). See the genre files.

## Making parts not look default

- No visible part keeps the default gray `Plastic` look (`Medium stone grey`, 163, 162, 165).
  Every part takes a palette color and a chosen material (inferred).
- Delete or retexture the template `Baseplate`. Replace the default `Sky` (inferred).
- Bevel or chamfer hero edges with `WedgePart`/`CornerWedgePart` strips or a beveled `MeshPart`.
  Put trim on building tops, bases and corners in a darker or lighter shade (inferred).
- Vary scale and rotation: repeat props at 2–3 sizes, rotate ±15°, and break up grids. Never
  place the same rock 20 times at the same size (inferred).
- Layer detail: a big shape, then medium parts (windows, beams, ledges), then small props (crates,
  lamps, plants, signs). Every 10×10-stud area of the play path should have one point of interest
  (inferred).
- Ground: use terrain or ≥ 2 materials, plus paths, edges, foliage and rocks where walls meet the
  floor (inferred).
- Block out first (greybox), test the gameplay, then dress it (official, 2026-10). For shapes
  Studio parts can't make well, use meshes from Blender or the Creator Store instead of stacking
  blocks (community, 2019-05).
- Lighting does ~50% of the look: apply a preset before judging any build (inferred).

## Performance caveats on mobile

Budgets and reasons are in [performance-and-devices](performance-and-devices.md). Visual-specific
rules (inferred unless tagged):
- `Realistic` + `PrioritizeLightingQuality = true` is the richest setup. Keep it, but limit
  shadowed local lights and set `CastShadow = false` on small and decorative parts
  (official, 2026-10).
- `Atmosphere`, `ColorCorrectionEffect` and `Clouds` are cheap (inferred).
  `SunRaysEffect` is reported to fade or vanish at low graphics levels (community, ~2021,
  unverified), and `DepthOfFieldEffect` may render differently on low-end devices
  (official, 2026-10). Never make them carry information.
- `Glass`, `ForceField` and partial `Transparency` cause overdraw; keep transparency at 0 or 1
  (official, 2026-10).
- Prefer built-in materials; use few unique `SurfaceAppearance`/`MaterialVariant` textures at
  ≤ 512² (official, 2026-10).
- `Terrain.Decoration` grass and dense foliage cost on low-end phones; test on the entry-level
  profile and with a real device.

## "Does this look default?" checklist

Fail the build if any answer is "no":
- [ ] `LightingStyle` and `PrioritizeLightingQuality` chosen on purpose, with a preset applied and
      tuned.
- [ ] An `Atmosphere`, a non-default `Sky`, and a `ColorCorrectionEffect` exist.
- [ ] No visible part is default gray `Plastic`, and the template `Baseplate` is gone.
- [ ] The palette is ≤ 5 hues plus neutrals and lives in one `Palette` module.
- [ ] In grayscale (`Saturation = -1`), hazards, path and collectibles are still distinct.
- [ ] Large shapes have bevels or trims, and props vary in size and rotation.
- [ ] The ground uses ≥ 2 materials or terrain, with transitions (edges, foliage, rocks).
- [ ] Each zone has a landmark visible from spawn.
- [ ] `Neon` is accent-only, and bloom doesn't wash out white surfaces.
- [ ] Screenshots on an entry-level phone profile look readable at low screen brightness.

## Checklist for agents

### Do
- Set `LightingStyle` and `PrioritizeLightingQuality` in Properties (not scriptable), and ask the user
  if the MCP can't.
- Start from one of the four presets, then tune `Brightness`/`ExposureCompensation` on a phone
  profile.
- Add `Atmosphere`, a custom `Sky`, and a `ColorCorrectionEffect`. Keep bloom thresholds ≥ 0.9.
- Keep a shared `Palette` module; give hazards, accents and safe ground fixed, distinct roles.
- Use built-in materials and `MaterialVariant` for consistency; use `SurfaceAppearance` only on
  hero meshes.
- Bevel, trim, layer props, and vary scale and rotation.

### Don't
- Don't set or mention `Lighting.Technology` (deprecated) or rely on legacy fog with an
  `Atmosphere`.
- Don't ship fresh `DepthOfFieldEffect` or `SunRaysEffect` defaults, or use DOF in gameplay.
- Don't make shadows, sun rays, DOF or color alone carry gameplay information.
- Don't leave default gray `Plastic`, the template `Baseplate`, or the default sky.
- Don't use pure black darkness for horror; use fog, low ambient and local lights.
- Don't stack semi-transparent parts or use many unique large textures.

## Related

- [performance-and-devices.md](performance-and-devices.md): budgets behind every caveat above
- [studio-mcp.md](studio-mcp.md): how to build all this through the Studio MCP
- [game-feel.md](../../roblox-vfx/references/game-feel.md): highlights, particles and rarity reveals
- [ui-ux.md](../../roblox-ui/references/ui-ux.md): shared palette and contrast rules
- [metadata-thumbnails-icons.md](../../../../vault/fundamentals/metadata-thumbnails-icons.md): screenshots and thumbnails need this look
- [quality-bar.md](../../build/references/quality-bar.md): visual "done" criteria
- [horror.md](../../../../vault/genres/horror.md), [obby-classic.md](../../../../vault/genres/obby-classic.md): genre-specific looks

## Sources

1. https://devforum.roblox.com/t/let-there-be-unified-light-unified-lighting-is-fully-live/3401512: Unified Lighting live 2025-07-23, Technology mapping, not scriptable; a commenter's 60-stud light range report
2. https://create.roblox.com/docs/reference/engine/classes/Lighting: property defaults, Technology deprecated, ShadowSoftness, light range note
3. https://create.roblox.com/docs/reference/engine/enums/LightingStyle: Realistic vs Soft
4. https://create.roblox.com/docs/environment/lighting: property meanings and example values
5. https://create.roblox.com/docs/environment/atmosphere: Atmosphere property guidance and examples
6. https://create.roblox.com/docs/reference/engine/classes/Atmosphere: Glare/Decay/Haze dependencies, Offset trade-offs, fog hidden
7. https://robloxapi.github.io/ref-temp/class/Atmosphere.html: Density class default
8. https://robloxapi.github.io/ref-temp/class/BloomEffect.html: Bloom class defaults
9. https://robloxapi.github.io/ref-temp/class/SunRaysEffect.html: SunRays class defaults
10. https://robloxapi.github.io/ref-temp/class/DepthOfFieldEffect.html: DOF class defaults
11. https://create.roblox.com/docs/reference/engine/classes/Sky: Sky properties, SunAngularSize clamp
12. https://create.roblox.com/docs/environment/post-processing-effects: effect placement, ColorGradingEffect presets
13. https://create.roblox.com/docs/reference/engine/classes/BloomEffect: Threshold meaning
14. https://create.roblox.com/docs/reference/engine/classes/ColorCorrectionEffect: Brightness/Contrast/Saturation/TintColor behavior
15. https://create.roblox.com/docs/reference/engine/enums/TonemapperPreset: Default vs Retro
16. https://create.roblox.com/docs/reference/engine/classes/DepthOfFieldEffect: low-end rendering note
17. https://create.roblox.com/docs/reference/engine/classes/PointLight: Brightness default
18. https://create.roblox.com/docs/reference/engine/classes/MaterialService: override names (material list), variant lookup
19. https://create.roblox.com/docs/reference/engine/classes/MaterialVariant: variant properties
20. https://create.roblox.com/docs/reference/engine/classes/SurfaceAppearance: PBR maps, Color tint, runtime limits
21. https://create.roblox.com/docs/reference/engine/classes/Terrain: Decoration, GrassLength, SetMaterialColor
22. https://create.roblox.com/docs/tutorials/curriculums/environmental-art/construct-your-world: Soft start default, Clouds, zone colors, materials, wayfinding
23. https://create.roblox.com/docs/tutorials/curriculums/environmental-art: greybox-first workflow
24. https://create.roblox.com/docs/performance-optimization/improve: shadows, quality level 4, overdraw, textures
25. https://create.roblox.com/docs/production/game-design/ui-ux-design: vibrant vs muted hierarchy
26. https://devforum.roblox.com/t/building-tips-andor-advice/284825: use Blender or plugins for shapes parts can't make (2019-05)
27. https://devforum.roblox.com/t/sunrays-not-working-in-my-game/1341727: sun rays reduced at low graphics levels

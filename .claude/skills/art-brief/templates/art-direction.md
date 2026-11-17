# Art direction
Status: draft   <!-- draft | approved -->

## In the user's words
> "..."

## References
| Image | Take from it | Leave out |
|---|---|---|
| [ref-1.png](../images/ref/ref-1.png) | | |

## Style in one line
<e.g. "Bright cartoon islands, chunky rounded shapes, soft shadows, saturated accents.">

## Lighting
- Preset: <Bright cartoon day | Golden hour | Night / horror | Stylized neon arena>
  (vault/fundamentals/visual-quality.md)
- Set by hand in Studio Properties (not scriptable): `LightingStyle` = <Soft | Realistic>,
  `PrioritizeLightingQuality` = <true | false>
- Changes from the preset:

| Property | Value | Why |
|---|---|---|
| | | |

- Sky: <look; custom Skybox faces or a generated texture>

## Palette
| Role | Name | RGB | Used on |
|---|---|---|---|
| Ground light | | | |
| Ground mid | | | |
| Ground dark | | | |
| Support 1 | | | |
| Support 2 | | | |
| Accent (interactables, rewards) | | | |
| Danger (hazards only) | | | |

Grayscale check (`ColorCorrectionEffect.Saturation = -1`): <path, hazards and collectibles still distinct?>

## Materials
| Surface | `Enum.Material` | Palette role | Notes |
|---|---|---|---|
| Main ground | | | |
| Paths | | | |
| Structures | | | |
| Hazards | | | |

## Shapes and detail
- Edges: <wedge bevels and trim | beveled meshes | sharp blocks on purpose>
- Prop density: <e.g. one point of interest per 10×10 studs along the path>
- Variation: <sizes and rotation range for repeated props>
- Built from, per object type: <parts | generate_procedural_model | Creator Store | generate_mesh>

## UI look (details in ui.md)
- Font: Builder Sans <weight>. Panel color and transparency. Corner radius. Button style.

## Not this
-

## Assumptions
-

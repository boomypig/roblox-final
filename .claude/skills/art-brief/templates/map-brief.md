# Map: <Name>
Status: draft   <!-- draft | approved | built -->
Art direction: [art-direction.md](../art-direction.md)

## In the user's words
> "..."

## References
| Image | Take from it | Leave out |
|---|---|---|
| [<name>-sketch.png](../../images/ref/<name>-sketch.png) | Layout | |

## Layout
- Overall size: <x × z studs>, height range <y to y>
- Spawn: <where, and what the player sees first>
- Main path: <route through the zones, width in studs>
- Lives in Studio at: <Workspace.<Name> | ServerStorage.Maps.<Name>>, with folders `Layout`
  (gameplay parts) and `Dressing` (decoration)

## Zones
| # | Zone | Purpose | Size (studs) | Landmark | Hue | Notes |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

## Gameplay geometry (`Layout`)
The numbers the build must hit, from the genre file and the specs. Tags come from docs/glossary.md.

| Element | Size / spacing (studs) | Tag | Notes |
|---|---|---|---|
| | | | |

## Dressing
- Per zone: props, ground materials and transitions, local lights
- Sources: <parts | generate_procedural_model prompts | Creator Store search terms | generate_mesh>

## Check views
Camera spots the map-builder screenshots after each pass.

| View | Camera at → looking at | Must show |
|---|---|---|
| Spawn | | Zone 1's landmark and the start of the main path |
| Top-down | | The layout matches the sketch |

## Budgets
From vault/fundamentals/performance-and-devices.md: <part count ceiling, shadow-casting lights,
triangles per mesh ≤ 20,000, textures ≤ 512²>

## Build order
1. Greybox zone 1 `Layout` → the user playtests → approve
2. Dress zone 1
3. <next zones>

## Not this
-

## Assumptions
-

## Open questions
-

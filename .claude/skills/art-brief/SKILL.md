---
name: art-brief
description: Turn the user's reference images and descriptions of how a Roblox game, map or UI should look into a build-ready brief with real values (lighting preset, palette RGB, materials, scale in studs, landmarks, screens). Use when the user shares inspiration images or describes a look, and before any map or UI is built.
argument-hint: "[art | map <name> | ui]"
---

# Art brief

Turn references and the user's own words into a brief that the map-builder agent and `/build` can
follow without guessing. Brief to write: **$ARGUMENTS** (empty = ask which one).

| Argument | Writes, in the game repo | Template |
|---|---|---|
| `art` | `docs/design/art-direction.md` (once per game) | [templates/art-direction.md](templates/art-direction.md) |
| `map <name>` | `docs/design/maps/<name>.md` | [templates/map-brief.md](templates/map-brief.md) |
| `ui` | `docs/design/ui.md` | [templates/ui-brief.md](templates/ui-brief.md) |

Run this from a game repo with roblox-final added to the session. A map or UI brief builds on
the art direction: if `docs/design/art-direction.md` is missing or not approved, say so and
offer to write it first.

## 1. Gather

- References must be files in `docs/images/ref/` (png or jpg). Images pasted into chat can't be
  seen by the map-builder or by later sessions, so ask the user to save them there first. Sketches
  count: a phone photo of a top-down map on paper is one of the most useful references.
- Read every image the user points to, the user's description, `docs/pitch.md`, and (for a map or UI
  brief) the approved art direction.
- Vault: `../roblox-final/vault/` from a game repo, or `vault/` inside roblox-final. Read
  `INDEX.md`, then:
  - `art`: `fundamentals/visual-quality.md`, `fundamentals/audience.md`, the genre file
  - `map`: `fundamentals/visual-quality.md`, `fundamentals/performance-and-devices.md`,
    `fundamentals/first-time-experience.md`, the genre file, and any pattern the map depends on
    (e.g. `patterns/checkpoints-and-respawn.md`, `patterns/round-system.md`)
  - `ui`: `fundamentals/ui-ux.md`, `fundamentals/game-feel.md`, and
    `fundamentals/monetization.md` + `patterns/shops.md` if there's a shop

## 2. Read the references back

For each image, write 2–4 lines: what you see, what to take from it, and what to leave out.
Stick to things you can name: shapes, palette, lighting, time of day, prop density, scale, mood.
Never take another game's assets, names, characters or logos. Show this to the user and confirm
you read it right before drafting. It catches misreadings before anything gets built.

## 3. Ask

Ask up to 5 questions, only ones whose answers change the build. Use AskUserQuestion when the
answers are choices. Good ones:
- When two references disagree, which one wins?
- Should it feel tight and busy, or wide and open?
- What must a new player notice first from spawn?
- What time of day and mood: bright noon, golden hour, night?
- Is there anything in these references you don't want?

## 4. Turn adjectives into values

Every word the user uses becomes something the builder can apply and the reviewer can check.
Examples (tune per game):

| The user says | The brief says |
|---|---|
| "cozy, warm" | Golden hour preset; `WoodPlanks` + `Brick`; warm ground neutrals; low prop spacing |
| "big and open" | Main paths ≥ 16 studs wide; landmarks tall enough to see from spawn; Atmosphere `Density` near the low end |
| "spooky but readable" | Night / horror preset; `OutdoorAmbient` ≥ (25, 25, 35); warm `PointLight`s along the path |
| "clean UI" | Builder Sans Bold; ≤ 2 panel colors; buttons ≥ 48 px; one call to action per card |

Rules:
- **Lighting:** start from one of the four presets in `visual-quality.md` and list only the
  changes. `LightingStyle` and `PrioritizeLightingQuality` get set by hand in Studio; say which.
- **Palette:** ≤ 5 hues plus neutrals, as RGB, each with one role: ground (light/mid/dark),
  2 supporting hues, 1 accent (interactables and rewards only), 1 danger (hazards only). Check
  the grayscale rule from `visual-quality.md`.
- **Scale:** in studs, measured against the ~5-stud avatar. Gameplay numbers (gaps, path
  widths, heights) come from the genre file's rules, not from the picture.
- **Check views:** name the camera spots the map-builder screenshots after each pass (spawn,
  top-down, each landmark).
- **Not this:** a short list of what to avoid. It's the best guard against generic output.
- **Source per object type:** plain parts, `generate_procedural_model` (it can take one
  reference image per prop), Creator Store search terms, or `generate_mesh` for a hero object.
  Prefer parts and generated props unless the goals file (`private/goals.md` in the toolkit,
  when it exists) says the game has an artist.

## 5. Write

- Fill the template. Put the user's own words in a quote at the top, and link each reference image.
- Mark every guess **Assumption:**. Set `Status: draft`. Never mark a brief approved; the user does.
- Keep it a checklist, not an essay: about 60–150 lines.

## 6. Hand off

Tell the user what to check (assumptions, palette, scale, the "Not this" list), and that approving
means setting `Status: approved`. Then name the next step:
- map: "use the map-builder agent to greybox zone 1 of docs/design/maps/<name>.md"
- ui: write the UI as a mechanic spec and run `/build`, or ask for the map-builder's help with
  in-world signs and billboards

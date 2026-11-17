---
name: art-brief
description: Turn the user's reference images and descriptions of how a Roblox game, map or UI should look into a build-ready brief with real values (lighting preset, palette RGB, materials, scale in studs, landmarks, screens). Use when the user shares inspiration images or describes a look, and before any map or UI is built.
argument-hint: "[art | map <name> | ui]"
---

# Art brief

Turn references and the user's own words into a brief that the map-builder agent and `/build` can
follow without guessing. Brief to write: **$ARGUMENTS** (empty = `art` when the game has no
approved art direction; otherwise list the briefs that exist and end, because a map brief
needs a name).

| Argument | Writes, in the game repo | Template |
|---|---|---|
| `art` | `docs/design/art-direction.md` (once per game) | [templates/art-direction.md](templates/art-direction.md) |
| `map <name>` | `docs/design/maps/<name>.md` | [templates/map-brief.md](templates/map-brief.md) |
| `ui` | `docs/design/ui.md` | [templates/ui-brief.md](templates/ui-brief.md) |

Run this from a game repo with roblox-final added to the session. A map or UI brief builds on
the art direction: if `docs/design/art-direction.md` is missing or not approved, say so, write
the art direction instead, and end there.

This skill follows the operating policy (`docs/workflow.md` in the toolkit): one draft, no questions on the way,
every open call decided and marked, and the user approves once at the end.

## 1. Gather

- References must be files in `docs/images/ref/` (png or jpg). Images pasted into chat can't be
  seen by the map-builder or by later sessions, so ask the user to save them there first (the
  one ask this skill makes: only they can do it). Sketches count: a phone photo of a top-down
  map on paper is one of the most useful references.
- Read every image the user points to, the user's description, `docs/pitch.md`, and (for a map or UI
  brief) the approved art direction.
- Research, from the toolkit folder (`../roblox-final/` from a game repo). `vault/INDEX.md`
  lists the vault; `S` below is `.claude/skills`:
  - `art`: `S/roblox-map/references/visual-quality.md`, `vault/fundamentals/audience.md`, the
    genre file
  - `map`: `S/roblox-map/references/visual-quality.md`,
    `S/roblox-map/references/performance-and-devices.md`,
    `vault/fundamentals/first-time-experience.md`, the genre file, and any pattern the map
    depends on (e.g. `vault/patterns/checkpoints-and-respawn.md`, `vault/patterns/round-system.md`)
  - `ui`: `S/roblox-ui/references/ui-ux.md`, `S/roblox-vfx/references/game-feel.md`, and
    `vault/fundamentals/monetization.md` + `vault/patterns/shops.md` if there's a shop

## 2. Read the references back

For each image, write 2–4 lines: what you see, what to take from it, and what to leave out.
Stick to things you can name: shapes, palette, lighting, time of day, prop density, scale, mood.
Never take another game's assets, names, characters or logos. Write the read-back into the
brief's References table ("Take from it", "Leave out"), where the user checks it when
approving. A misreading caught there costs nothing; do not wait for a confirmation.

## 3. Decide the open calls

Do not ask. For each thing the references and the description leave open, take the reading
closest to them, write it under **Assumptions**, most build-changing first, and keep
drafting. The calls that most often need one:
- Two references disagree: which one wins.
- Tight and busy, or wide and open.
- What a new player must notice first from spawn.
- Time of day and mood: bright noon, golden hour, night.
- What in the references to leave out.

Put under **Open questions** only what the user alone can answer and the build does not
depend on yet.

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
- Run the gate and fix what it reports:
  `python3 ~/roblox-final/.claude/skills/art-brief/scripts/check_brief.py <brief file>`.

## 6. Hand off

Tell the user what to check (assumptions first, then palette, scale, the "Not this" list), and
that approving means setting `Status: approved`. Then name the next step:
- map: "use the map-builder agent to greybox zone 1 of docs/design/maps/<name>.md"
- ui: write the UI as a mechanic spec and run `/build`, or ask for the map-builder's help with
  in-world signs and billboards

## Rules

- One draft, no questions on the way (operating policy, `docs/workflow.md`). The one ask is
  for reference images to be saved to `docs/images/ref/`.
- Every adjective becomes a value the builder can apply and the reviewer can check.
- Never take another game's assets, names, characters or logos from a reference.
- Never set `Status: approved`. The user does.

## Gate

`scripts/check_brief.py <brief file>` must print `PASS` before you hand off. It checks the
Status line, that no template placeholder is left, that every linked reference image exists on
disk, the "Not this" list, and per kind: palette RGB values and the hue limit, the lighting
preset and `LightingStyle` (art); size, zones, geometry numbers, check-view camera coordinates
and budgets (map); screens and HUD positions (UI).

## References

| File | Used for | Source of its facts |
|---|---|---|
| `.claude/skills/roblox-map/references/visual-quality.md` | the four lighting presets, palette and grayscale rules, the "does this look default?" checklist | its Sources list (Creator Docs lighting and materials pages, dated) |
| `.claude/skills/roblox-map/references/performance-and-devices.md` | the budgets a map brief states | its Sources list |
| `.claude/skills/roblox-ui/references/ui-ux.md`, `.claude/skills/roblox-vfx/references/game-feel.md` | UI sizes, touch targets, press feedback | their Sources lists |
| `vault/genres/<genre>.md`, `vault/fundamentals/audience.md`, `first-time-experience.md` | gameplay numbers, who the look is for, what a new player must see | their Sources lists |
| `templates/` | the shape of each brief | this skill |

## Traps

- **No art direction before building.** The first game built with this toolkit had none: its
  map started as grey code-built geometry and got cosmetics late, and the build "worked but
  felt flat". That is why a map or UI brief refuses to start without an approved art direction.
- **References pasted into chat.** The map-builder and later sessions cannot see them. Only
  files in `docs/images/ref/` count, and the gate fails a link to an image that is not there.
- **Gameplay sizes read off a picture.** Gap widths, path widths and heights come from the
  genre file's rules; a reference image has no scale.
- **`LightingStyle` and `PrioritizeLightingQuality` in a script.** They cannot be set from
  Luau; the brief names them for the user to set by hand
  (roblox-map `references/visual-quality.md`).
- **A brief that is an essay.** The builder follows checklists. 60 to 150 lines.

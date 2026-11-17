# Who reads each research file

The evidence behind the research library's shape (decision D17). For each file: the step of
the skill or agent that names it, and what was decided. A file a build step reads moved to the
skill that enforces it; a file a design step reads stayed in the vault; a file no step reads
would go to `private/archive/`.

Collected on 2026-11-17 by searching every skill, agent, starter doc and script for each file
name. "By name in the index" means the step loads `vault/INDEX.md` and then the files whose
name matches its task, so the file is reachable without being named in the step.

## Fundamentals

| File | Named by (step) | Kind of step | Decision |
|---|---|---|---|
| `building-with-studio-mcp.md` | `map-builder` "Before building" 3, "How to build"; `create-roblox-game` intro | build | moved to `roblox-map/references/studio-mcp.md` |
| `visual-quality.md` | `map-builder` "Before building" 3, "Check after each structure"; `/art-brief` 1 (art, map) and 4; art-direction template | build and design | moved to `roblox-map/references/visual-quality.md`: the builder's checks enforce it, the brief only picks from it |
| `performance-and-devices.md` | `map-builder` "Before building" 3; `/art-brief` 1 (map); map-brief template "Budgets" | build and design | moved to `roblox-map/references/performance-and-devices.md`: the builder stays inside its budgets |
| `security-and-anti-exploit.md` | `/build` 1 (any remote handler); `reviewer` 4 "Security" | build | moved to `roblox-code/references/security.md` |
| `ui-ux.md` | `/art-brief` 1 (ui); ui-brief template "Look" | build (UI) | moved to `roblox-ui/references/ui-ux.md` |
| `game-feel.md` | `/art-brief` 1 (ui); ui-brief template "Look" | build (feedback) | moved to `roblox-vfx/references/game-feel.md` (one owner; no skill was given new required reading) |
| `quality-bar.md` | `reviewer` 2 and 4; `/build` 1; `/pitch` 1.4; `create-roblox-game` section 5 | build (review) | moved to `build/references/quality-bar.md`, the skill that owns the spec, build, review loop |
| `discovery-algorithm.md` | `/pitch` 1.4; `goals.template.md` (audience gate) | design | stays |
| `trend-lifecycle.md` | `/pitch` 1.4 | design | stays |
| `audience.md` | `/art-brief` 1 (art); `goals.template.md`; `starter/CLAUDE.md` (phone first) | design | stays |
| `first-time-experience.md` | `/art-brief` 1 (map) | design | stays |
| `monetization.md` | `/art-brief` 1 (ui, when there is a shop) | design | stays |
| `metadata-thumbnails-icons.md` | `starter/docs/backlog.md` (M3) | design | stays |
| `retention.md` | by name in the index: `spec-writer` 1, `create-roblox-game` section 1 | design | stays |
| `social-and-virality.md` | by name in the index: `spec-writer` 1, section 1 | design | stays |
| `live-ops-and-updates.md` | by name in the index: `spec-writer` 1, section 1 | design | stays |
| `analytics.md` | by name in the index: `spec-writer` 1, section 1 | design | stays |

## Genres (31 files) and patterns (21 files)

| Files | Named by (step) | Decision |
|---|---|---|
| `vault/genres/*.md` | `/pitch` 1.5 (the shortlist only); `/art-brief` 1 and 4 ("the genre file": gameplay numbers); `map-builder` "Before building" 3 (dressing and props); `create-roblox-game` section 1; `spec-writer` 1 by name | stay, one library |
| `vault/patterns/*.md` | `/art-brief` 1 (map: `checkpoints-and-respawn`, `round-system`; ui: `shops`); `spec-writer` 1 and section 1 by name | stay, one library |

## Index and rules

| File | Named by | Decision |
|---|---|---|
| `vault/INDEX.md` | `/pitch` 1.2; `spec-writer` 1; `/build` 1; `create-roblox-game` section 1; `starter/CLAUDE.md`; `CLAUDE.md` | stays at the same path, now the short form (4.7 KB, from 11.7 KB) |
| `vault/CATALOG.md` | `vault/INDEX.md`; `tools/vault_lint.py` | new: the full read-when line and status of every file |
| `vault/CONTRIBUTING.md` | `CLAUDE.md`; `create-roblox-game/references/pipeline.md` step 1; `tools/vault_lint.py` | stays |

## Private

| Was | Named by | Decision |
|---|---|---|
| The trend reports, `latest.md` and `history/` (old path in `docs/migration.md`) | `/pitch` 1.3; section 1; genre files' Sources | `private/trends/` (generated from the user's own data; may not exist, and each reader carries on without market numbers) |
| The case studies (old path in `docs/migration.md`) | `/pitch` 1.5; section 1; genre files' "Top examples" | `private/case-studies/`, cited as `(case study: <slug>)`; when it is missing the genre file's "Top examples" has the summary |

## Files no step reads

None in the vault: every remaining file is named by a step or reachable by name through the
index. Nothing was archived and nothing was deleted. `private/archive/` exists for the first
file that stops being read.

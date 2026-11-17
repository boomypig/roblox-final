---
title: Classic and difficulty-chart obby
type: genre
read-when: Building a checkpoint obby or difficulty-chart obby, or tuning jumps, stages, checkpoints and respawn for any obby.
last-researched: 2026-10-22
---

# Classic and difficulty-chart obby

## In one line

A linear run of numbered stages with a checkpoint after each. The player's stage number is the
progress bar, the score and the brag. Difficulty-chart obbies sort stages into named, colored
difficulty tiers. The genre is cheap to build and crowded, so it only works with tight movement,
fair readable hazards, a smooth difficulty curve and a spin.

## Core loop

- **Moment to moment (5–60 s):** read a stage, attempt, die, respawn at the stage start, retry.
- **Session (15–30 min):** clear 10–40 stages, see the stage counter climb, reach the next tier
  color, maybe buy or watch an ad to skip one stuck stage (inferred).
- **Long term:** finish the chart; badges per tier; trails/cosmetics; a stage leaderboard; return
  when new stages are added (inferred).

## Main verbs

Jump, run, wrap around corners, truss-climb, time movers, ride conveyors, wall-hop (advanced),
use stage gimmicks (vehicles, carry objects, tethered partner in co-op obbies).

## Movement tuning and jump-gap math

Lock movement before building any stage: every gap is sized against these numbers, and changing
`WalkSpeed` later breaks the whole map (inferred).

| Setting | Default | Obby value |
|---|---|---|
| `StarterPlayer.CharacterWalkSpeed` | 16 studs/s (official, 2026-10) | 16 |
| `StarterPlayer.CharacterUseJumpPower` | `true` (official, 2026-10) | `false`, so heights are explicit |
| `StarterPlayer.CharacterJumpHeight` | 7.2 studs (official, 2026-10) | 7.2 |
| `StarterPlayer.CharacterJumpPower` | 50 (official, 2026-10) | unused when the above is false |
| `Workspace.Gravity` | 196.2 studs/s² (official, 2026-10) | 196.2 |
| `StarterPlayer.CharacterMaxSlopeAngle` | 89° (official, 2026-10) | 89; make "unclimbable" slopes steeper than this or kill parts |
| `Players.RespawnTime` | 5 s (official, 2026-10) | 0.5–1 s (inferred) |
| `SpawnLocation.Duration` (spawn force field) | 10 s (official, 2026-10) | 0 |

With `UseJumpPower = true`, JumpPower 50 gives a rise of 50² / (2 × 196.2) ≈ 6.4 studs, not 7.2
(community, DevForum; arithmetic checked). Mixing the two modes is the most common reason "the
same jump" works in one place and not another (inferred).

**Jump math** (inferred, projectile physics with the obby values above; verify with a playtest):
`v0 = sqrt(2 × g × JumpHeight) ≈ 53.2 studs/s`. Air time to land Δy above take-off is
`t = (v0 + sqrt(v0² − 2 × g × Δy)) / g`. Horizontal travel is `WalkSpeed × t`.

| Landing height vs take-off | Air time | Root travel at 16 studs/s |
|---|---|---|
| +6 studs | 0.38 s | 6.1 studs |
| +4 | 0.45 s | 7.2 |
| +2 | 0.50 s | 8.0 |
| 0 (flat) | 0.54 s | 8.7 |
| −4 | 0.61 s | 9.7 |
| −10 | 0.69 s | 11.0 |

- The clearable **edge-to-edge** gap is root travel plus the character's footprint, about 1–2
  studs (inferred). Community guides report 10–12 studs as the plain-jump limit (community,
  unverified). **Measure your own max** with a Studio MCP playtest (step the gap 0.5 studs at a
  time) and write it into the design doc.
- The max step-up is just under 7.2 studs of rise. Use ≤ 5 for routine steps (inferred).
- Gap bands as a share of the measured flat max (inferred starting values):

| Band | Gap | Platform width | Use |
|---|---|---|---|
| Easy | ≤ 60% (about 5–6 studs) | ≥ 4 studs | First 10–15 stages, all of the first tier |
| Medium | 60–80% | 2–4 studs | Mid tiers |
| Hard | 80–95% | 1–2 studs | Late tiers, skill checks |
| Never | > 95% | — | Frame-perfect; reads as unfair |

- Mobile thumbsticks are less precise. Keep 1-stud beams and camera-dependent wraparounds out of
  the first 20 stages (inferred). Consider `StarterPlayer.AutoJumpEnabled = false`, since auto-jump
  fires on touch devices when walking into obstacles (official behavior; disabling it is inferred).
- Optional feel upgrade: allow a jump for about 0.1 s after walking off a ledge ("coyote time")
  by calling `Humanoid:ChangeState(Enum.HumanoidStateType.Jumping)` from the client (inferred;
  no built-in equivalent found).

## Stage design and difficulty curve

- **Introduce, then combine.** Show each new obstacle alone in a safe stage, then mix it with known
  ones. Community reviewers flag difficulty spikes and "kill brick spam" as the main complaints
  (community, DevForum).
- **Sawtooth ramp:** 5–8 stages of rising difficulty, then 1–2 easy "breather" stages, repeated.
  Never put the hardest stage of a tier first (inferred).
- **Stage length:** 15–60 s for a player who knows it; more than 3 obstacles between checkpoints
  only in late tiers (inferred).
- **Variety per 10 stages:** at least 4 obstacle types (gaps, movers, conveyors, trusses,
  vanishing, wraparounds, gimmicks). Every jump should feel distinct (community, DevForum).
- **Readable hazards** (inferred unless tagged):
  - One kill style everywhere: bright red with `Material = Neon`. Never use red or neon on safe
    parts.
  - Make the kill hitbox slightly smaller than its visual so near misses survive. Use an
    invisible kill part inside a non-touchable visual shell.
  - Telegraph movers and vanishing parts: flash or play a sound 0.5–1 s before they act.
  - Don't use shadows as cues; they are off below graphics quality 4 (official, 2026-10).
    Avoid partial transparency, which costs fill-rate on phones (official, 2026-10).
  - Next-checkpoint direction must be visible from the respawn point.
- **Moving platforms** that carry players: physics-driven (`PrismaticConstraint` servo or
  `AlignPosition`). Tweening an anchored part's position doesn't carry characters (community,
  DevForum 2021).

## Checkpoints and respawn feel

Full implementation: [checkpoints and respawn](../patterns/checkpoints-and-respawn.md).

- **Fall-to-control under about 1 s.** Five seconds of default respawn across 20 deaths a session
  is wasted time (inferred). Set `Players.RespawnTime`, or set `Players.CharacterAutoLoads = false`
  and call `Player:LoadCharacterAsync()` yourself (`LoadCharacter` is deprecated) (official, 2026-10).
- **Spawn facing the stage** with the camera behind the character. A spawn force field
  (`SpawnLocation.Duration`, default 10 s) is visual noise in an obby; set it to 0 (official
  default; inferred choice).
- **Respawn at the checkpoint**, either through `Player.RespawnLocation` (the SpawnLocation must be
  `Neutral` or match the player's team; official) or by pivoting the new character to the stage
  pad on `CharacterAdded`. Multiple eligible spawns are picked at random, so give each stage one
  (official).
- **Advance only to stage current + 1** on the server, and check the root part is actually on the
  pad. A client can fake `Touched` on parts it owns (official, 2026-10;
  [security](../../.claude/skills/roblox-code/references/security.md)).
- Keep the Roblox reset button: stuck players use it.
- Save the stage on change and on leave ([player data](../patterns/player-data.md)). Show it as
  a `leaderstats` value named `Stage` so it appears on the player list (official convention).
- A stage selector for already-cleared stages lets friends play together (community, DevForum
  open-source obby kits).

## Difficulty-chart obbies

- **What they are:** 100–300+ stages grouped into named tiers, each with its own color, with the
  tier shown on every stage. Example: [HELL] Spiral Difficulty Chart Obby lists 260 stages and
  claims "only 0.1%" finish; 3,474 players (data, 2026-10-22).
- **Where the ladder comes from:** Juke's/Eternal Towers of Hell's difficulty names (Easy, Medium,
  Hard, Difficult, Challenging, Intense, Remorseless, Insane, Extreme, Terrifying, Catastrophic,
  later Effortless and more), set between 2018-03 and 2019. Its color ramp runs green → yellow →
  orange → red → dark red → near-black → magenta → blues → white (community, wiki). Chart obbies
  reuse the words; there is no fixed color standard (community, DevForum).
- **Why they persist (inferred):** stages are a few parts each, so content is cheap; the stage
  number is a universal brag; "can you beat the hardest obby" fits video and clip titles; and each
  update is just "+20 stages".
- **Tier sizing (inferred):** 10–20 stages per tier, with tier 1 trivially easy (first win within
  60 s), and a visible color change plus sound and badge at each new tier.

## Why players come back

An unfinished stage count ("87/260") saved where they left off; new stages announced as updates;
tier badges; friends at a different stage; co-op variants that need a partner (inferred).

## What separates top games from clones

Locked movement and measured gaps; no unfair or hidden kills; sawtooth curve; fast respawn;
a gimmick that changes what the player *does* (tethered partner, vehicle, carried object); clear
tier colors; skip and ad options that never block the free path (inferred).

## Session shape

- **Typical session:** 15–30 min (inferred).
- **First 60 s:** spawn on stage 1 facing the course; first jump within 5 s; stage 2 reached
  within 30 s; no popups (inferred; see [first-time experience](../fundamentals/first-time-experience.md)).
- **First 10 min:** first tier cleared (10–20 stages), first badge, first trail unlocked by
  progress (inferred).
- **Day 7:** mid-chart; a "new stages" update to return to (inferred; see
  [retention](../fundamentals/retention.md)).

## Social hooks

Stage on the player list; tier-reached chat messages; stage selector to play with friends;
2–5 player co-op obbies (tethered, carry-together) where progress needs a partner; spectate a
friend (inferred). See [social and virality](../fundamentals/social-and-virality.md).

## Monetization that works here

| Product | Notes |
|---|---|
| Skip stage (developer product) | Granted in `MarketplaceService.ProcessReceipt`; +1 stage (community, DevForum). Price low, about R$15–25 (inferred). |
| Free skip via rewarded video ad | `AdService:ShowRewardedVideoAdAsync` (server) with `CreateAdRewardFromDevProductId`; check `GetAdAvailabilityNowAsync` on the client first. Rewards must be developer products, not random; Roblox suggests rewards worth about R$3–10 and placements "after losing a life". Needs ≥ 2,000 monthly unique visitors (official, 2026-10). |
| Trails, colors, death effects | Cosmetic, no fairness issue |
| Speed/gravity coil passes | Make the course easier; label them clearly and exclude them from "legit" leaderboards (inferred) |
| VIP / 2× rewards | Only if there is a currency (inferred) |

**Is selling skips fair?** In a solo-progress obby a skip hurts no one else (inferred). Rules:
offer it only after 5+ deaths or 60+ s on the same stage; always pair it with the free ad skip;
mark skipped stages and don't count them for tier badges or "completed" leaderboards; never sell
skips in races or towers where others compete (inferred).

## Common failure modes

- Gaps sized by eye, then `WalkSpeed` changed later, so half the stages break.
- Kill parts that look like floor; hazards hidden by camera angle or darkness.
- Difficulty spikes, the hardest stage at a tier start, or no breathers.
- 5 s respawn, a spawn force field, or spawning facing the wrong way.
- Skip prompts on every death; ads or purchases blocking the next attempt.
- Checkpoints that accept any stage number (exploit) or don't save on leave (rage quit).
- 300 copy-pasted stages: no variety, low ratings (community, DevForum).

## Saturation & opportunity

Single snapshot (data, 2026-10-22); no growth claims.

- `obby` theme: 26 charted games, 46K players, median 952 per game, labeled **crowded**.
  Obby & Platformer is 1.7% of charted players (41 games, 119K).
- Classic Obby subgenre: only 3 games, 6.0K players.
- **Co-op obbies** (2–5 players tethered or carrying something): Carry the Glass Together 4,540,
  Grapple Cart Obby 2,642, Blockies 2,579, Webbed! 2,435, Fart Obby 1,562, Chained 1,265, Chained
  Together 763: 7 games, 15.8K players, likes 74–96%.
- **"Obby but you're on a ___" / vehicle obbies:** Scooter 2,994, Kart Of Hell 2,635, Board Of Hell
  2,254, Bike 763, Dangerous ATV Driving 681, Skateboard 644: 6 games, about 10K players.
- Read (inferred): a plain checkpoint obby is the most crowded slot on the chart. The players are
  in obbies whose gimmick changes the verb (a partner, a vehicle). Pick a spin from
  [trend lifecycle](../fundamentals/trend-lifecycle.md#how-to-add-a-spin) before stage 1.

## Scope for a solo dev

**MVP (3–4 weeks, primitives and built-in materials, no artist; inferred):**
- Locked movement values and a measured jump table.
- Server checkpoint system, saved stage, `leaderstats` Stage, stage selector.
- 60 stages in 4 tiers with colors, a sawtooth ramp and tier badges.
- One gimmick that is the spin (co-op tether, vehicle or carried object), used in at least 1 of
  every 3 stages.
- Skip product, rewarded-ad skip once eligible, 3–5 trails.

| Week | Build |
|---|---|
| 1 | Movement lock and jump test course; checkpoints, respawn, save; 15 stages |
| 2 | The gimmick; 25 stages; tier colors and badges |
| 3 | 20 stages; skip product and ad; trails; stage selector |
| 4 | Phone playtests of every stage, performance pass, icon/thumbnail, launch |

**Cut:** pets, rebirths, currencies beyond what trails need, a lobby hub, custom characters.
**After launch:** +15–20 stages every 2 weeks as the update (inferred).

## Top examples

- [HELL] Spiral Difficulty Chart Obby: 260-stage chart, 3,474 players (data, 2026-10-22).
- Carry the Glass Together!: 2-player carry obby, created 2026-06-29, 4,540 players (data, 2026-10-22).
- Chained [2 Player Obby]: tethered co-op, 443M visits (data, 2026-10-22).
- Obby But You're on a Scooter: vehicle gimmick, 2,994 players (data, 2026-10-22).
- Tower of Hell (case study: tower-of-hell): the no-checkpoint alternative; see [obby-tower](obby-tower.md).
- Escape/story obbies: see [obby-escape](obby-escape.md).

## Build checklist for agents

### Do

- Set `CharacterUseJumpPower = false`, `CharacterJumpHeight = 7.2`, `CharacterWalkSpeed = 16`,
  `Gravity = 196.2` before stage 1, and record the measured flat max gap in the design doc.
- Size gaps by band: easy ≤ 60% of max with ≥ 4-stud platforms; hard ≤ 95%.
- Introduce every obstacle alone before combining it; add a breather every 5–8 stages.
- Use one kill style (red `Neon`) and nothing else red; telegraph movers 0.5–1 s ahead.
- Respawn in ≤ 1 s at the current checkpoint, facing the course, with `SpawnLocation.Duration = 0`.
- Advance stages server-side only from current to current + 1 with a position check; save on change.
- Show the stage in `leaderstats`, the tier color on the HUD, and a badge plus sound per tier.
- Offer skip only after 5 deaths or 60 s stuck; grant it in `ProcessReceipt`; offer the
  rewarded-ad alternative where eligible.
- Playtest each stage on a phone-sized viewport with Studio MCP; it must be cleared 3 times in
  a row by the tester before shipping.
- Build ridden movers with constraints, not tweened anchored parts.

### Don't

- Don't change `WalkSpeed`, `JumpHeight` or gravity globally after stages exist.
- Don't use gaps above 95% of max, invisible kill parts, or hazards that depend on shadows or
  partial transparency.
- Don't place 1-stud beams or camera-dependent wraparounds in the first 20 stages.
- Don't prompt a purchase on the first death or block retry behind any popup.
- Don't count skipped stages for badges or completion leaderboards.
- Don't trust a client `Touched` alone to advance a stage.
- Don't copy another obby's stages, names, tier art or thumbnails.

## Sources

1. https://create.roblox.com/docs/reference/engine/classes/StarterPlayer — CharacterWalkSpeed 16, CharacterJumpHeight 7.2, CharacterJumpPower 50, CharacterUseJumpPower true, CharacterMaxSlopeAngle 89, AutoJumpEnabled
2. https://create.roblox.com/docs/reference/engine/classes/Humanoid — JumpHeight/UseJumpPower behavior, MaxSlopeAngle, ChangeState
3. https://create.roblox.com/docs/reference/engine/classes/Workspace — Gravity 196.2
4. https://create.roblox.com/docs/reference/engine/classes/Players — RespawnTime 5 s, CharacterAutoLoads
5. https://create.roblox.com/docs/reference/engine/classes/Player — LoadCharacterAsync, LoadCharacter deprecated, RespawnLocation rules
6. https://create.roblox.com/docs/reference/engine/classes/SpawnLocation — Duration default 10, Neutral, random choice among spawns
7. https://create.roblox.com/docs/reference/engine/classes/AdService — rewarded video API names and server/client rules
8. https://create.roblox.com/docs/production/promotion/rewarded-video-ads — eligibility, reward rules, R$3–10 reward value, placements
9. https://create.roblox.com/docs/players/leaderboards — leaderstats convention
10. https://devforum.roblox.com/t/how-to-set-player-jump-height/2505890 — JumpPower² / (2 × Gravity) height formula
11. https://devforum.roblox.com/t/thoughts-on-this-hard-obby/225844 — difficulty spikes, kill-brick spam, introducing obstacles
12. https://devforum.roblox.com/t/the-hardest-obby-on-roblox/1545564 — community feedback on unique jumps and fairness
13. https://devforum.roblox.com/t/platform-moves-while-character-doesnt/1051218 — tweened platforms don't carry players
14. https://devforum.roblox.com/t/help-with-a-skip-stage/406152 — skip-stage developer product handling
15. https://devforum.roblox.com/t/eol-wolfites-obby-system-easily-make-an-obby/1594327 — open-source obby kit: stage selector, skip setting
16. https://devforum.roblox.com/t/robloxs-difficulty-chart-obby-hard/2531746 — chart-obby tier ladder as used by creators
17. https://jtoh.fandom.com/wiki/Difficulty — origin and dates of the difficulty ladder and color ramp
18. https://noping.com/blog/how-to-long-jump-in-roblox — 10–12 stud plain-jump claim (low-quality source, unverified)
19. private/trends/latest.md and its 2026-10-22 dated copy — obby theme, subgenre, co-op and vehicle obby numbers, game descriptions (data)

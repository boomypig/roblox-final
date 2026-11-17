---
title: Shooter (arena FPS and duels)
type: genre
read-when: Building a shooter/FPS.
last-researched: 2026-10-22
---

# Shooter (arena FPS and duels)

## In one line

Short, skill-based gunfights (1v1 duels to small-team rounds) with crisp hit feedback,
fair netcode, and cosmetic weapon skins as the economy. On Roblox in 2026 the winning shape is
the duel arena, not the large military shooter.

## Core loop

- **Moment to moment (1–5 s):** peek → aim → fire → hit marker and sound → kill or reposition
  → reload.
- **Round / match (20 s–5 min):** spawn with a loadout → win the round → first to N rounds wins
  (RIVALS: first to 5, 1v1 to 5v5) (community, game page, 2026-10-23).
- **Meta (weeks):** earn currency or keys per match → unlock weapons and skins → ranked rating
  and win streak → seasonal pass and events (community, game page, 2026-10-23; inferred).

## Main verbs

Aim, shoot, aim down sights (ADS), reload, swap weapon, slide/crouch, jump, throw utility
(grenade, smoke, flash), melee, emote/inspect. Mobile adds auto-shoot and aim assist
(press, 2025-03).

## Formats on Roblox now

| Format | Examples (players, max per server; data 2026-10-22) | Notes |
|---|---|---|
| Duel arena, lobby + duel pads, 1v1–5v5, first to 5 | RIVALS 138K, 40 | Step on a pad to challenge; loadout of 4 (primary, secondary, melee, utility) (community, game page 2026-10-23; guide site, unverified) |
| Small FFA arena, one weapon class | One Tap 12K, 8 (one-shot snipers); Deagle Arena 7.3K, 8; Sniper Arena 9K, 20 | Tiny scope, created 2025-12 to 2026-04 (data) |
| Classic modes + abilities | Hypershot 21K, 17 (TDM, CTF, FFA, Gun Game, 1v1/2v2 duels, abilities) | Coins and gems unlock weapons, skins, abilities (community, game page 2026-10-23) |
| Revolver/knife duels | Murderers VS Sheriffs 74K, 30 (labeled Battlegrounds & Fighting); Murder Duels 8.9K | Hidden-role weapons reused as a duel game (data) |
| Tactical / military | BloxStrike 8K; Phantom Forces 2.3K; Arsenal 2.7K; Cold War 3.7K (80 max) | 2015-era leaders now small (data) |
| Team competitive | Tribes 3v3 10.8K, created 2026-09-28, 63% likes | Custom loadouts, "not for casual players" (data; game page) |

## Gun feel

Feel is mostly client-side presentation over server-authoritative results. See
[game feel](../../.claude/skills/roblox-vfx/references/game-feel.md) for general juice.

- **Recoil:** drive camera kick and viewmodel kick with springs, not tweens or camera lerps;
  tweens snap and camera lerps look skippy (community, 2021–2023). Starting values
  (inferred): vertical kick 0.5–2° per shot, small random horizontal, recovery 0.15–0.3 s.
  First shot should go where the crosshair is in duel games (inferred).
- **Spread:** hip-fire bloom that grows per shot and decays in ~0.3 s; ADS cuts spread to near zero
  for rifles and pistols; shotguns use fixed pellet patterns so players can learn them (inferred).
- **Hit markers:** show a crosshair tick and a hit sound on the shooter's client the same frame
  the local ray hits (prediction); show damage numbers and kill confirmation only on the server's
  reply. Distinct sounds for body hit, headshot and kill (inferred).
- **Sound:** layered fire sound (close shot + tail), reload stages, distinct enemy footsteps.
  Positional `Sound` objects parented to the character; cap simultaneous voices (inferred).
- **Viewmodel:** first-person arms and gun are client-only (official, 2026-10). Lock the camera
  with `Player.CameraMode = Enum.CameraMode.LockFirstPerson`; zoom by tweening
  `Camera.FieldOfView` on the client (inferred).
- **TTK:** 100 HP; target 0.3–0.6 s body-shot TTK for automatic rifles in duel games and a
  headshot multiplier of 1.5–2× (inferred). One Tap's whole identity is one-shot snipers and
  "two-shot" secondaries, one to the head (community, game page, 2026-10-23): TTK is the design.
- **Fire rate:** server enforces per-weapon minimum interval (e.g. 0.1 s for a 600 RPM rifle) with
  ~10% slack for jitter (inferred).

## Hitscan vs projectiles

| | Hitscan | Projectile |
|---|---|---|
| What | Instant ray, `Workspace:Raycast` | Simulated travel with drop/speed, usually stepped raycasts per frame |
| Fits | Rifles, pistols, SMGs, laser tag (Roblox's own tutorial calls beams "near-infinite velocity") (official, 2026-08) | Rockets, grenades, bows, slow plasma, dodgeball-like throws (official, 2026-08) |
| Netcode | Easy to validate: origin, direction, target distance, obstruction | Harder: server simulates or validates the client's trajectory |
| Libraries | None needed | FastCast (Redux) is the long-standing library; its author is reported to have left Roblox and it is unmaintained (community, 2023, unverified). Writing a small stepped-raycast module is ~100 lines (inferred). |

Roblox's Laser Tag tutorial shows the validation flow: client raycasts and sends per-ray
results (destination `CFrame` + tagged player) and the origin; the server re-computes expected
directions and rejects angles past `BLAST_ANGLE_SANITY_CHECK_TOLERANCE_DEGREES`, checks shooter
near origin and target near destination with `DISTANCE_SANITY_CHECK_TOLERANCE_STUDS`, rejects
obstructed paths, blocks friendly fire by `Team`, and applies damage with `Humanoid:TakeDamage()`
(official, 2026-08). Full hit-spoofing rules: [security](../../.claude/skills/roblox-code/references/security.md).

## Lag compensation on Roblox

- **There is no engine rewind API.** Server Authority's "latency compensation" is client-side
  prediction and rollback of the player's own simulation; it doesn't validate hits against past
  positions (official, 2026-10). Its templates are racing, soccer and laser tag (official, 2026-10).
- **Default: favor the shooter, then sanity-check.** The client detects the hit; the server
  accepts it if the target was plausibly there (distance from the server's target position
  ≤ target speed × (ping + ~100 ms buffer) + 3–4 studs) and the path is clear (inferred,
  consistent with the official tutorial's tolerance approach).
- **Rewind (advanced):** keep ~1 s of each character's root `CFrame` history on a fixed tick,
  stamp shots with `Workspace:GetServerTimeNow()`, rewind to that time, validate against the
  rewound box (community, 2024-12; Valve's 1 s buffer quoted there). Cap rewind at ~250 ms so
  high-ping players can't shoot around corners (inferred). Roblox's internal replication buffer
  can exceed measured ping, so ping-only rewind under-corrects (community, 2024-12).
- Send aim direction and cosmetic tracers on an `UnreliableRemoteEvent` (< 1,000 bytes); send
  shots and hits on a reliable `RemoteEvent` (official, 2026-10).
- Server Authority (`Workspace.AuthorityMode = Server`) stops speed and fly hacks for
  competitive movement; consider it for ranked shooters (see security file) (official, 2026-07).

## Maps

- Duel and arena maps are small and symmetric: 3 lanes, clear sightlines, cover every
  10–15 studs, spawns out of each other's sight (inferred).
- RIVALS has ~30 maps and an "Experimental Maps" system for testing new ones (press, 2026-03,
  unverified); ranked uses a smaller competitive pool and lets each side ban one map
  (press, 2025-03).
- Build maps from simple anchored geometry with `CollisionFidelity = Box` on props; bullets
  should hit what players see (inferred). See [visual quality](../../.claude/skills/roblox-map/references/visual-quality.md).

## Modes and ranked

- Ship one mode first: 1v1 duels on pads in a shared lobby (no matchmaking service needed) or FFA
  in 8-player servers (inferred from RIVALS and One Tap).
- RIVALS ranked as documented in 2025-03 (press): separate 1v1, 2v2, 3v3 queues; unlock by
  winning 10 duels, level 30 and a 14-day-old account; 10 placement matches; map ban plus two
  weapon bans (core weapons can't be banned); one free daily "ELO shield"; third person off,
  aim assist at 50%, auto-shoot limited, 2 loadout swaps per match; 7 tiers from Bronze
  (0–599) to Nemesis (3,600+) in 600-point steps; season-end rewards.
- By 2026-03 entry reportedly needed level 50 plus a verification step, with a top tier
  "Archnemesis" (press, 2026-03, unverified). Gate ranked behind play time and account age to
  slow alt-account cheaters (inferred).

## Mobile and controller

- Roblox has no engine aim assist; games build their own (no official API found, unverified).
  Typical pieces (inferred): slow camera rotation near a target (friction), gentle pull toward
  a target while moving (magnetism), and a max assist angle of ~5–8°. Scale it down in ranked
  (RIVALS: 50%) (press, 2025-03).
- **Auto-shoot** (fire when the crosshair is over an enemy) is a mobile staple; RIVALS limits it
  in ranked (press, 2025-03). Deagle Arena uses "hold Shoot to aim, release to shoot" on mobile
  (community, game page, 2026-10-23).
- At 200+ ms ping, client-side assist tracks where the enemy *was* (guide site, unverified).
- Bind actions with the Input Action System (`InputContext`, `InputAction`, `InputBinding`);
  an `InputBinding.UIButton` links a touch button to the same action as the key or trigger
  (official, 2026-10).
- RIVALS uses input-based matchmaking (press, 2026-03, unverified): match touch players with
  touch players in casual queues (inferred).

## Why players come back

- Mastery: aim improves visibly; win streak shown publicly (community, game page, 2026-10-23).
- Unlock tracks: keys earned by playing unlock weapons and skins (community, game page).
- Contracts (daily/weekly challenges) and a seasonal pass (community, game page; press, 2026-03).
- Frequent numbered updates: 19 major updates in 21 months for RIVALS (press, 2026-03,
  unverified), each with a weapon, map or event.

## What separates top games from clones

- Hit registration players trust (favor-the-shooter with tight server checks).
- Every weapon viable in some range; balance patches announced with the update (inferred).
- Short time from join to first shot: RIVALS drops players in a lobby and fights start by
  stepping on a pad (community, game page).
- Cross-device parity: mobile aim assist, controller support, and touch-tuned UI
  (RIVALS supports desktop, phone, tablet, Xbox, PS5 per its page) (community, game page).
- Visible anti-cheat: permanent bans stated up front (community, game page).

## Session shape

- **First 60 s:** spawn in lobby with a free default loadout, one prompt ("step on a pad"), and a
  bot or open pad to fight (inferred).
- **First 10 min:** 3–6 duels, first key or currency reward, see one skin on another player
  (inferred).
- **Typical session:** 20–45 min of back-to-back matches (inferred).
- **Day 7:** owns 2–3 unlocked weapons, has a favorite loadout, checks contracts, eyes ranked
  (inferred).

## Social hooks

- Party duels (2v2–5v5) with friends; challenge a specific player by pad (community, game page).
- Kill-cam, finishers and emotes give clip moments (inferred).
- Leaderboards for win streaks; ranked seasons; tournaments run through third-party organizers
  for RIVALS (press, 2026-03, unverified).
- See [social and virality](../fundamentals/social-and-virality.md).

## Monetization that works here

- **Cosmetics only.** Weapon skins, wraps, charms, finishers, emotes, kill effects, name tags
  (One Tap and RIVALS pages) (community, game pages, 2026-10-23). Never sell damage.
- **Weapons free via play.** Keys earned in matches unlock weapons; bundles shortcut this
  (community, game page). RIVALS passes on 2026-10-23: Starter 59, RPG 95, Medkit 289, Exogun 649,
  Standard Weapons 849, Classic 865, Energy 975, Heavy Duty 1,425 Robux (data, API 2026-10-23).
- **Skin cases** are the high-volume item (RIVALS: 249 Robux per case, press 2026-03,
  unverified). Before offering any paid random item, call
  `PolicyService:GetPolicyInfoForPlayerAsync` in `pcall` and hide paid cases when
  `ArePaidRandomItemsRestricted` is true (official, 2026-10). Hypershot's page notes that bundles
  omit cases in countries that ban them (community, game page). Publish odds.
- **Season pass** with skins, keys and currency, designed to pay back more than its cost in
  rewards (press, 2026-03, unverified).
- Cheap repeatable buys (keys, single cases) for spend days; see
  [monetization](../fundamentals/monetization.md).

## Common failure modes

- **Server-only hit detection with no compensation:** shots that clearly hit don't count at 100+
  ms (community, 2024-12).
- **Client-trusting damage:** aimbots, silent aim and wall shots (official, 2026-10).
- **Pay-to-win guns** or paid stat upgrades (inferred).
- **Big maps with few players:** long walks, no fights (inferred; milsim titles hold 2–4K now).
- **No mobile tuning:** tiny buttons, no assist; phones are most of Roblox (inferred).
- **Cheaters left unbanned** in ranked; no account-age or play-time gate (inferred).
- **Viewmodel and VFX on the server:** replication lag and network cost (official, 2026-10).

## Saturation & opportunity

- **Shooter genre: 35 charted games, 274K players, 3.9% share; Deathmatch Shooter: 24 games,
  254K** (data, 2026-10-22). Theme `shooter`: 8 games, 162K, RIVALS holds 85%; tagged "one game
  dominates" (data, 2026-10-22).
- RIVALS alone: 138K players, #1 top-trending, #1 top-earning, #1 trending-in-shooter (data,
  2026-10-22). Competing head-on with a duel arena means competing with it (inferred).
- **But small scoped shooters chart:** One Tap (12K, created 2025-12), Sniper Arena (9K,
  2026-01), Murder Duels (8.9K, 2026-01), Deagle Arena (7.3K, 2026-04), AirDrop Arena (4.9K,
  2026-04, 97% likes), Tribes 3v3 (10.8K, 25 days old) (data, 2026-10-22). Each is one weapon
  class or one format, 8–20 players.
- Murderers VS Sheriffs (74K) sits in Battlegrounds & Fighting but is a revolver-and-knife duel
  game; the duel format is bigger than the Shooter numbers show (data, 2026-10-22; inferred).
- **Opportunity (inferred):** a one-gimmick arena (one weapon class, one movement trick, or one
  odd theme) with RIVALS-grade hit feel and mobile parity. Avoid a full multi-weapon duel clone.
  See [trend lifecycle](../fundamentals/trend-lifecycle.md).

## Scope for a solo dev

Shooters need fewer animations than fighters: no third-person combat animations beyond
aim/hold poses, which Roblox's default tool animations partly cover. The viewmodel needs fire,
reload, equip and inspect clips per weapon (inferred). R15 avatars allow video-captured
animations through Live Animation Creator (official, 2026-10).

**MVP (inferred):** one 8-player FFA or 1v1-pad lobby, 3 weapons (rifle, pistol, sniper),
1 utility, 2 maps, hitscan only, hit markers + sounds, kill feed, streak leaderboard, keys for
skins, 10 skins, one bundle pass, mobile aim assist and auto-shoot.

**Build order (one developer with Claude Code, inferred):**

1. **Week 1:** client weapon controller (first-person lock, viewmodel, fire, reload), server
   weapon config module (damage, fire interval, mag, range falloff, headshot multiplier),
   reliable fire remote with validation, damage.
2. **Week 2:** recoil and spread springs, hit markers, sounds, kill feed, respawn; Studio MCP
   playtests with 2–4 clients plus the Network Simulator at 150–250 ms.
3. **Week 3:** duel pads or FFA round loop, 2 maps, mobile controls and aim assist, controller.
4. **Week 4:** progression: XP, keys, skins shop, data save; anti-cheat strike logging.
5. **Week 5:** polish: viewmodel animations for 3 weapons, VFX, performance on a phone, launch.
6. **Weeks 6–8:** second mode, ranked only if DAU supports queues (≥ a few hundred concurrent)
   (inferred).

**Cut:** projectiles (except one grenade), ranked at launch, custom matchmaking service,
lag-comp rewind (start with favor-the-shooter checks), more than 3 weapons, destructible maps,
paid cases (start with direct-buy skins).

## Top examples

- RIVALS (case study: rivals): the 2024–2026 leader; duel pads, keys, cases, ranked,
  cross-platform.
- Hypershot, One Tap, Deagle Arena: smaller arenas showing that one gimmick plus good feel can
  hold 7–21K (data, 2026-10-22).
- Murder Mystery 2 (case study: murder-mystery-2): the cosmetics economy behind the
  revolver/knife duel spin-offs.

## Build checklist for agents

### Do
- Keep weapon stats in a server ModuleScript; the client gets a display copy.
- Hitscan with `Workspace:Raycast` and `RaycastParams`; validate origin, angle, target distance
  and obstruction on the server with explicit tolerances, as in Roblox's Laser Tag tutorial.
- Enforce fire interval, magazine, reload and alive state on the server with ~10% jitter slack.
- Show hit markers and sounds instantly on the client; show damage and kills from server replies.
- Use springs for recoil; keep viewmodels and tracers client-only.
- 100 HP, 0.3–0.6 s body-shot TTK for autos, 1.5–2× headshots; one-shot weapons need a long
  fire interval or a scope delay.
- Servers of 8–20 for arenas; matches decided in under 5 minutes.
- Mobile: aim assist (friction + magnetism, ≤ 8°), auto-shoot option, large fire button,
  `InputBinding.UIButton` for touch; reduce assist in ranked.
- Gate paid random items with `ArePaidRandomItemsRestricted`; publish odds.
- Stamp shots with `Workspace:GetServerTimeNow()` so rewind can be added later.
- Test at 150–250 ms with Studio's Network Simulator before calling hit-reg done.

### Don't
- Don't trust client damage, hit positions without checks, or fire rate.
- Don't sell weapons with better stats than free ones.
- Don't put viewmodels, recoil or tracers on the server.
- Don't build a 30+ player military map as a first shooter.
- Don't ship without controller and touch support.
- Don't rewind more than ~250 ms or rely on ping alone for rewind.
- Don't copy RIVALS's maps, weapon names, skins, UI or its "first to 5 on duel pads" presentation
  wholesale; change the format or the gimmick.

## Sources

1. private/trends/latest.md and the trends database — genre/subgenre totals, per-game players, max players, created dates (data, 2026-10-22)
2. https://www.roblox.com/games/17625359962 — RIVALS page: 1v1–5v5, first to 5, duel pads, keys, contracts, platforms, anti-cheat note (read 2026-10-23)
3. https://www.roblox.com/games/17516596118 — Hypershot modes, abilities, case disclaimer (read 2026-10-23)
4. https://www.roblox.com/games/9294074907 — One Tap: one-shot snipers, two-shot secondaries, cases, kill effects (via tracker DB, 2026-10-22)
5. https://www.roblox.com/games/10057403337 — Deagle Arena controls, mobile hold-to-aim (via tracker DB)
6. https://apis.roblox.com/game-passes/v1/universes/6035872082/game-passes — RIVALS bundle prices (read 2026-10-23)
7. https://www.sportskeeda.com/roblox-news/rivals-ranked-guide — ranked queues, unlocks, bans, restrictions, ELO tiers (2025-03-03)
8. https://rowatcher.com/news/rivals-how-roblox-s-top-shooter-built-a-nearly-million-player-empire — maps, weapons, update cadence, case price, season pass, ranked changes (2026-03)
9. https://create.roblox.com/docs/tutorials/curriculums/gameplay-scripting/detect-hits — hitscan vs physical, ray validation, tolerances, TakeDamage (2026-08)
10. https://create.roblox.com/docs/projects/server-authority — latency compensation is prediction/rollback; no hit rewind
11. https://devforum.roblox.com/t/server-sided-hit-detection-with-lag-compensation/3322386 — snapshot history, 1 s buffer, buffer-vs-ping caveat (2024-12)
12. https://devforum.roblox.com/t/lag-compensated-gun-system-with-server-authority/4023578 — rewind experiment on Server Authority (2025-10)
13. https://devforum.roblox.com/t/alternatives-to-fastcast/2630169 — FastCast maintenance status (2023)
14. https://devforum.roblox.com/t/recoil-using-springs/1495471 — spring-based recoil
15. https://devforum.roblox.com/t/how-can-i-create-smooth-recoil/1100842 — tween/lerp recoil problems
16. https://create.roblox.com/docs/input/input-action-system — InputContext, InputAction, InputBinding, UIButton
17. https://create.roblox.com/docs/reference/engine/classes/PolicyService — GetPolicyInfoForPlayerAsync, ArePaidRandomItemsRestricted
18. https://create.roblox.com/docs/reference/engine/classes/UnreliableRemoteEvent — 1,000-byte payload limit
19. https://create.roblox.com/docs/animation/capture — Live Animation Creator, R15 only
20. https://marix.app/library/games/rivals-mobile-aim-assist-broken — aim assist at 200+ ms ping (unverified guide)

---
title: Vault catalog
type: meta
read-when: A name in INDEX.md is not enough to decide whether a file matches your task.
last-researched: 2026-11-17
---

# Vault catalog

One row per file, with its full read-when line and status. `INDEX.md` is the short form: load
that first and open this only when a name there is not enough. `tools/vault_lint.py` reads its
list of files from here. Status: `done` = reviewed and final, `draft` = written but not
reviewed, `todo` = planned. Writing rules: [CONTRIBUTING.md](CONTRIBUTING.md).

## Fundamentals

| File | Read when | Status |
|---|---|---|
| [discovery-algorithm.md](fundamentals/discovery-algorithm.md) | Deciding what to optimize for recommendations, or planning a launch. | done |
| [retention.md](fundamentals/retention.md) | Designing session goals, return reasons, or reading D1/D7/D28 numbers. | done |
| [first-time-experience.md](fundamentals/first-time-experience.md) | Building spawn, tutorial, or anything in a new player's first 10 minutes. | done |
| [metadata-thumbnails-icons.md](fundamentals/metadata-thumbnails-icons.md) | Writing a title, description, icon, or thumbnail, or before publishing. | done |
| [monetization.md](fundamentals/monetization.md) | Adding any game pass, developer product, subscription, or purchase code. | done |
| [social-and-virality.md](fundamentals/social-and-virality.md) | Designing co-play, invites, private servers, or clip-worthy moments. | done |
| [live-ops-and-updates.md](fundamentals/live-ops-and-updates.md) | Planning updates, events, limited-time content, or codes. | done |
| [trend-lifecycle.md](fundamentals/trend-lifecycle.md) | Deciding whether to join a trend or clone wave, and how to add a spin. | done |
| [audience.md](fundamentals/audience.md) | Choosing target players, devices, languages, or pricing. | done |
| [analytics.md](fundamentals/analytics.md) | Adding analytics events or reading Creator Analytics after launch. | done |

## Genres

| File | Read when | Status |
|---|---|---|
| [obby-classic.md](genres/obby-classic.md) | Building a checkpoint obby or difficulty-chart obby. | done |
| [obby-tower.md](genres/obby-tower.md) | Building a no-checkpoint tower obby. | done |
| [obby-escape.md](genres/obby-escape.md) | Building an "escape the ___" obby. | done |
| [round-based-races-and-survival.md](genres/round-based-races-and-survival.md) | Building a lobby → round → results game (races, disasters, deathruns). | done |
| [tycoon.md](genres/tycoon.md) | Building a tycoon (droppers, build-out). | done |
| [simulator.md](genres/simulator.md) | Building a clicker/stat simulator. | done |
| [pet-egg-collection.md](genres/pet-egg-collection.md) | Building pet collection, eggs, or hatching as the main loop. | done |
| [idle-incremental.md](genres/idle-incremental.md) | Building an idle/incremental game or offline progress. | done |
| [steal-a-x.md](genres/steal-a-x.md) | Building a base-raiding idle game ("steal a ___"). | done |
| [plus-one-stat.md](genres/plus-one-stat.md) | Building a "+1 speed/stat every second" or keyboard-escape game. | done |
| [job-sims.md](genres/job-sims.md) | Building a restaurant, store, or "sell ___" work sim. | done |
| [farming-growing.md](genres/farming-growing.md) | Building a farming/growing game. | done |
| [fishing.md](genres/fishing.md) | Building a fishing game. | done |
| [tower-defense.md](genres/tower-defense.md) | Building a tower defense game. | done |
| [battlegrounds.md](genres/battlegrounds.md) | Building an anime fighting / battlegrounds game. | done |
| [anime-rpg.md](genres/anime-rpg.md) | Building an anime RPG/adventure with levels and zones. | done |
| [gacha-raid.md](genres/gacha-raid.md) | Building dice/unit/character gacha with raids or bosses. | done |
| [rng-aura.md](genres/rng-aura.md) | Building a rolling/RNG aura game. | done |
| [shooter.md](genres/shooter.md) | Building a shooter/FPS. | done |
| [horror.md](genres/horror.md) | Building chase, story, or co-op horror. | done |
| [survival.md](genres/survival.md) | Building a survival game (nights, forest, crafting). | done |
| [social-deduction.md](genres/social-deduction.md) | Building a hidden-role game (Murder Mystery-like). | done |
| [asymmetric-survival.md](genres/asymmetric-survival.md) | Building killer-vs-survivors with character rosters. | done |
| [roleplay-life-sim.md](genres/roleplay-life-sim.md) | Building a roleplay or life sim town. | done |
| [social-hangout.md](genres/social-hangout.md) | Building a hangout or chill social space. | done |
| [fashion-avatar.md](genres/fashion-avatar.md) | Building a dress-up, fashion, or avatar-creator game. | done |
| [sports.md](genres/sports.md) | Building a soccer, volleyball, basketball, or other sports game. | done |
| [racing-driving.md](genres/racing-driving.md) | Building a racing or driving game. | done |
| [party-minigames.md](genres/party-minigames.md) | Building minigame rotations or hide and seek. | done |
| [story-games.md](genres/story-games.md) | Building a chapter-based story game. | done |
| [building-sandbox.md](genres/building-sandbox.md) | Building a creation/physics sandbox. | done |

## Patterns

| File | Read when | Status |
|---|---|---|
| [player-data.md](patterns/player-data.md) | Saving anything: DataStores, session locking, data migration. | done |
| [round-system.md](patterns/round-system.md) | Building lobby/intermission/match state. | done |
| [checkpoints-and-respawn.md](patterns/checkpoints-and-respawn.md) | Building checkpoints, respawn, or stage progress. | done |
| [rebirth-prestige.md](patterns/rebirth-prestige.md) | Adding rebirth/prestige resets and multipliers. | done |
| [rarity-tiers-and-eggs.md](patterns/rarity-tiers-and-eggs.md) | Adding eggs, gacha rolls, rarity tiers, or odds. | done |
| [pets-companions.md](patterns/pets-companions.md) | Adding pets that follow, equip, or boost stats. | done |
| [trading.md](patterns/trading.md) | Adding player-to-player trading. | done |
| [base-defense-and-stealing.md](patterns/base-defense-and-stealing.md) | Adding bases that can be raided, locks, or stealing. | done |
| [idle-offline-income.md](patterns/idle-offline-income.md) | Adding passive or offline income. | done |
| [conveyor-dropper-economy.md](patterns/conveyor-dropper-economy.md) | Adding droppers, conveyors, or collectors. | done |
| [upgrade-trees.md](patterns/upgrade-trees.md) | Adding upgrade paths, cost curves, or skill trees. | done |
| [daily-rewards-and-streaks.md](patterns/daily-rewards-and-streaks.md) | Adding daily login rewards, streaks, or timed gifts. | done |
| [quests.md](patterns/quests.md) | Adding quests, missions, or achievements. | done |
| [codes.md](patterns/codes.md) | Adding redeemable codes. | done |
| [leaderboards.md](patterns/leaderboards.md) | Adding in-game or global leaderboards. | done |
| [boss-fights-and-raids.md](patterns/boss-fights-and-raids.md) | Adding bosses, raids, or co-op PvE encounters. | done |
| [ability-kits.md](patterns/ability-kits.md) | Adding characters with ability kits, cooldowns, combat. | done |
| [shops.md](patterns/shops.md) | Adding an in-game shop (soft or Robux currency). | done |
| [inventory.md](patterns/inventory.md) | Adding an inventory, equipment, or item storage. | done |
| [server-events-admin-abuse.md](patterns/server-events-admin-abuse.md) | Adding server-wide events, weather, or "admin abuse" sessions. | done |
| [private-servers.md](patterns/private-servers.md) | Adding or pricing private (VIP) servers. | done |

## Build references

Knowledge a build step uses lives with the skill that enforces it, in that skill's
`references/`. The files keep the vault's rules (frontmatter, claim tags, dated numbers, a
Sources list) and are linted with the vault.

| File | Owner | Read when | Status |
|---|---|---|---|
| [quality-bar.md](../.claude/skills/build/references/quality-bar.md) | `build` | Reviewing any build, or deciding if a feature is "done" to a high standard. | done |
| [ui-ux.md](../.claude/skills/roblox-ui/references/ui-ux.md) | `roblox-ui` | Building any UI: HUD, shop, menus, notifications; mobile layout. | done |
| [game-feel.md](../.claude/skills/roblox-vfx/references/game-feel.md) | `roblox-vfx` | Adding feedback to an action: tweens, sound, particles, camera. | done |
| [visual-quality.md](../.claude/skills/roblox-map/references/visual-quality.md) | `roblox-map` | Setting lighting/atmosphere, choosing materials and colors, building maps. | done |
| [performance-and-devices.md](../.claude/skills/roblox-map/references/performance-and-devices.md) | `roblox-map` | Building maps or effects that must run on low-end phones. | done |
| [studio-mcp.md](../.claude/skills/roblox-map/references/studio-mcp.md) | `roblox-map` | Building or dressing a map, props, terrain or lighting in Studio through the Studio MCP. | draft |
| [security.md](../.claude/skills/roblox-code/references/security.md) | `roblox-code` | Writing any RemoteEvent/RemoteFunction handler or server validation. | done |

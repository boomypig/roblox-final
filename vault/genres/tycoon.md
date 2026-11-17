---
title: Tycoon
type: genre
read-when: Building a tycoon (claim a plot, buy buttons, droppers/conveyors/collectors, build-out, rebirth).
last-researched: 2026-10-22
---

# Tycoon

## In one line

Claim a plot, step on buy buttons that build machines (droppers, conveyors, upgraders) that make
money, use the money to buy more buttons until the base is complete, then rebirth to rebuild
faster. The classic "___ Tycoon" title is crowded, but its build-out-and-income core now powers
most of Roblox's biggest Simulation games: Roblox files Steal An Egg and Steal a Brainrot under
the Tycoon subgenre (data, 2026-10-22).

## Core loop

**Moment to moment (5–30 s):** money ticks in from droppers or collectors. Walk to the next
lit button, buy it, and watch the piece build itself in. The classic dropper spawns a part that
rides a conveyor into a collector that pays out (community, Roblox fan wiki / guides).

**Session (15–30 min):** buy 10–30 buttons in a fixed tree. Each one adds income or opens the
next floor or wing, and the path leads to visibly bigger pieces. (inferred)

**Long term (days):** finish the base, rebirth for a permanent multiplier and restart. Advanced
tycoons add prestige, unlock trees and new areas (community, creation.dev glossary). Theme
variants turn the build into a business: restaurants, car dealerships, pet stores, military
bases (data, chart titles 2026-10-22).

## Main verbs

Claim, collect, buy (button), build, upgrade, decorate, defend (PvP variants), rebirth.

## Why players come back

- **The goal is the building.** An empty plot that fills up is a progress bar you can walk
  around in. (inferred)
- **Visible wealth.** Neighbours see your base. Small servers (median 6 per Tycoon-subgenre
  game, data 2026-10-22) keep the comparison personal.
- **Long tails.** Old tycoons still hold players: War Tycoon (created 2020) 5.1K, Car Dealership
  Tycoon (2018) 4.8K with 2.54B visits, Lumber Tycoon 2 (2009) 1.9K (data, 2026-10-22).
- **Speed is easy to sell.** Passes that speed up progression have an obvious value, which is why
  the genre monetizes well (community, guides; unverified).
- **Offline income** turns a finished base into a reason to return. See
  [idle-offline-income](../patterns/idle-offline-income.md). (inferred)

## What separates top games from clones

1. **A theme that changes what you do.** Restaurant Tycoon 3 (customers and service), Car
   Dealership Tycoon (driving the cars you sell), War Tycoon (18-player PvP around the base)
   (data, 2026-10-22; designs inferred from titles and server sizes). Kit tycoons only change the
   paint.
2. **Something to do besides waiting.** The 2026 hits put an active verb on top of the base:
   stealing ([steal-a-x](steal-a-x.md)), riding or chopping ([idle-incremental](idle-incremental.md)),
   serving ([job-sims](job-sims.md)). (inferred)
3. **Pieces that look different as you climb.** Each wing is a new silhouette, not a bigger
   copy of the first dropper. (inferred)
4. **No physics money.** Smooth on phones with 6–8 bases loaded. See Do list. (inferred)
5. **Updates.** Long-lived tycoons carry update tags ([KF-41], [UPDATE 3]) and seasonal labels
   (data, 2026-10-22). See [live-ops-and-updates](../fundamentals/live-ops-and-updates.md).

## Session shape

- **First 60 s (inferred targets):** the player owns a plot on spawn (auto-assigned, no door to
  find). The first button costs 0 or under 5 s of starting cash. The first dropper pays within
  5 s of being built.
- **First 10 min (inferred targets):** 10–15 buttons bought, the first floor or wing done, and
  the price of the next big piece shown on screen.
- **Base completion (inferred target):** 60–120 min of play over 2–4 sessions, so the first
  rebirth lands on day 2 or 3.
- **Day 7 (inferred targets):** 2–4 rebirths, cosmetic customization unlocked, a weekly event
  or new wing to chase.
- Session length target 15–25 min (press, GameAnalytics 2025; see
  [retention](../fundamentals/retention.md)).

## Social hooks

- **Neighbours.** 6–8 plots side by side make every base a showroom. (inferred)
- **Visiting and rating** friends' bases. (inferred)
- **PvP tycoons.** War Tycoon runs 18 per server, Car Dealership Tycoon 15 (data, 2026-10-22):
  more players when the game is about fighting or driving, not just building.
- **Stealing** turned the tycoon's neighbours into rivals; that is the
  [steal-a-x](steal-a-x.md) genre.
- **Two-player co-op tycoons** exist ("2 Player Battle Tycoon", 69 players, data 2026-10-22)
  but don't chart well right now.

## Monetization that works here

- **2× cash pass.** The default first pass in income games; dated prices in
  [steal-a-x](steal-a-x.md).
- **Auto-collect pass** for games with a collect step. (inferred)
- **Robux buttons:** a premium dropper or wing sold next to the normal ones. Keep the
  free path complete. (inferred)
- **Timed boosts** (2× for 15–30 min, 25–50 R$) for spend days, a discovery signal (official
  signal, 2026-10; prices inferred). See
  [discovery-algorithm](../fundamentals/discovery-algorithm.md).
- **Cosmetics** for the base: skins, colors, decorations. They don't touch the economy and
  show off to neighbours. (inferred)
- **Private servers** for building in peace. See [private-servers](../patterns/private-servers.md).
- Rules for products and passes: [monetization](../fundamentals/monetization.md).

## Common failure modes

- **Kit clones.** Tycoon kits let many people make tycoons with little effort (community, Roblox
  fan wiki). A kit look reads as stale and as non-unique to discovery (official, 2026-10; see
  [discovery-algorithm](../fundamentals/discovery-algorithm.md)).
- **Physics money lag.** Every dropped part is a simulated part. Unanchored parts cost physics
  time, and many of them hurt performance (community, DevForum). With 6–8 bases that is
  hundreds of parts on a phone. (inferred) See
  [performance-and-devices](../../.claude/skills/roblox-map/references/performance-and-devices.md).
- **Spoofable collectors and buttons.** A client can fire `Touched` for parts it owns, so
  touch-based collectors and buy pads must be re-checked on the server (official, 2026-10). See
  [security](../../.claude/skills/roblox-code/references/security.md).
- **Dead waits.** 2+ minutes with nothing affordable and nothing to do. (inferred)
- **Base wiped on rebirth with no visible gain.** Show the multiplier and the faster rebuild
  before confirming. (inferred)
- **Plot loss on rejoin.** The base must rebuild from saved data on any server. (inferred)
- **"Tycoon" in the title as the pitch.** See saturation below.

## Saturation & opportunity

All (data, 2026-10-22, single snapshot, so no growth claims):

| Measure | Games | Players | Median | Leader | Report label |
|---|---|---|---|---|---|
| `tycoon` theme ("tycoon" in the name) | 22 | 55K | 1.4K | Storage Hunters: Open World 11.7K (21%) | **crowded** |
| Roblox subgenre Tycoon | 83 | 1.46M (20.8% of charted) | 1.9K | Steal An Egg 877K (~60%) | – |

- "Crowded" means 15+ games with a median at or below the median charted game (~1.5K) (data,
  report definition).
- Named tycoons charting: Pet Store Tycoon 8.8K (created 2026-06-06), Restaurant Tycoon 3 6.5K,
  War Tycoon 5.1K, Car Dealership Tycoon 4.8K, Army Commander Tycoon 4.3K (created 2026-09-28),
  Mansion Tycoon 2.3K, Lumber Tycoon 2 1.9K (data, 2026-10-22).
- Build-out games without "Tycoon" in the name do as well or better: Sell Lemons 25.5K, Build An
  Ant Empire 6.7K, Build a Phone Empire 6.7K, Build a PC 5.7K, Run a Restaurant! 4.4K at 99%
  likes (data, 2026-10-22).
- Reading (inferred): the label "tycoon" is crowded; the mechanics are not. Use the build-out
  base as the meta layer under a verb players can do, and name the game after the verb.
- Spins with room (inferred): a tycoon whose base is attacked by waves you defend (mix with
  [tower-defense](tower-defense.md)); a business tycoon where serving customers is the core
  verb ([job-sims](job-sims.md)); a base others visit and rate ([social-hangout](social-hangout.md)).

## Scope for a solo dev

A good first project: one plot model, a button tree and an income system cover most of it.
(inferred)

**MVP** (inferred)
- 6 plots per server, auto-assigned on join, cleared on leave.
- A button tree of 25–40 buttons in 3 wings; each button reveals a pre-built model.
- Income per machine computed on the server; drops are cosmetic, client-side.
- One collect method (auto or a pad), offline income with a cap.
- Rebirth (×1.5 income, keeps cosmetics), autosave of bought button IDs.
- 2× cash pass, auto-collect pass, 2 timed boosts, one Robux button.

**Build order** (one developer with Claude Code; rough weeks, inferred)

| Week | Build |
|---|---|
| 1 | Plot assignment, button system, income tick, save and rebuild from IDs ([player-data](../patterns/player-data.md)) |
| 2 | Three wings of pieces (primitives or Studio MCP `generate_procedural_model`), cosmetic drops, collect, rebirth |
| 3 | Theme verb on top (serve, defend, drive), shop and passes, FTUE arrows |
| 4 | Mobile and performance pass with 6 full bases, icon/thumbnail, launch |
| 5+ | Weekly: a new wing or machine set plus one event |

**No artist:** build pieces from primitives with a strict palette per wing; let scale, color and
particles show tier. Never reuse a tycoon kit's models or another game's look. (inferred)

**Cut from v1:** PvP, trading, base decorating, multiple floors per wing, cross-server events,
pets. (inferred)

## Top examples

- Steal a Brainrot (case study: steal-a-brainrot) and
  Steal An Egg (case study: steal-an-egg): tycoon bases plus stealing; both filed as
  Simulation / Tycoon (data, 2026-10-22).
- Grow a Garden (case study: grow-a-garden): a farming plot that Roblox also files under
  Tycoon (data, 2026-10-22).
- Sell Fries! (case study: sell-fries): a small 2026 sell/job loop with build-out.
- Restaurant Tycoon 3, War Tycoon, Car Dealership Tycoon: long-running themed tycoons with
  update tags (data, 2026-10-22).

## Build checklist for agents

Numbers are starting values to tune unless tagged otherwise. (inferred)

### Do

- Server size 6–8, one plot per player slot (Tycoon-subgenre median 6, data 2026-10-22).
- Auto-assign a plot on `Players.PlayerAdded`; free it on `Players.PlayerRemoving`.
- Save the set of bought button IDs plus cash and rebirths, never the built parts. Rebuild the
  base from IDs on join.
- Compute income on the server per machine per tick (1 Hz is enough). Drops and conveyor parts
  are client-side visuals only.
- If any money part must be physical: anchor what you can, call `BasePart:SetNetworkOwner(nil)`
  on unanchored ones, clean up with `Debris:AddItem` (≤ 10 s lifetime), and cap live parts per
  base (e.g. 30).
- Button prices: each step ×1.15–1.35 the previous, with early buttons paying back in 20–60 s
  and late ones in 3–5 min. Full base in 60–120 min of play.
- Rebirth: ×1.5–2 income per rebirth, show the rebuild time it saves, keep cosmetics.
- Handle buy pads and collectors on the server: check plot owner, cash, button prerequisites
  and distance. Treat `Touched` and `ProximityPrompt.Triggered` as requests (official, 2026-10).
- Pay offline income on join with a 2–8 h cap and a claim screen.
- Tag buttons and machines with `CollectionService` and drive them from one server module, not
  one script per button.
- Grant Robux purchases only in `MarketplaceService.ProcessReceipt`; check passes with
  `MarketplaceService:UserOwnsGamePassAsync`.
- Profile a server with 6 finished bases on a low-end phone before launch.

### Don't

- Don't use a free tycoon kit or copy another tycoon's layout, models or names.
- Don't put "Tycoon" alone in the title as the hook; name the verb or the business.
- Don't spawn unanchored money parts per dropper per second.
- Don't one-script-per-button (hundreds of scripts and connections).
- Don't make the player walk to a door to claim a plot before they can play.
- Don't leave more than 2 min with nothing affordable in the first hour.
- Don't trust client-sent prices, button IDs without prerequisite checks, or collect amounts.
- Don't wipe cosmetics or bought Robux items on rebirth.

## Sources

1. https://roblox.fandom.com/wiki/Tycoon — genre origin (2008), 2015 resurgence, tycoon kits (community)
2. https://www.creation.dev/glossary/tycoon — dropper model, rebirth and unlock trees (community, low-confidence)
3. https://devforum.roblox.com/t/is-there-a-part-limit/755095 — unanchored parts cost physics time; MeshParts vs Unions (community)
4. https://devforum.roblox.com/t/too-many-parts-in-a-game/1284342 — high part counts and mitigation (community)
5. https://create.roblox.com/docs/physics/network-ownership — Touched spoofing and SetNetworkOwner
6. https://create.roblox.com/docs/scripting/security/client-server-boundary — ProximityPrompt and Touched validation
7. https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i — exponential cost growth for buy ladders
8. https://www.gameanalytics.com/reports/2025-roblox-report — session length vs retention
9. private/trends/latest.md — tycoon theme, Tycoon subgenre, players, server sizes (data, 2026-10-22)

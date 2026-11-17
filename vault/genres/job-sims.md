---
title: Job sims (restaurant, store, "sell ___")
type: genre
read-when: Building a restaurant, store, "sell ___" or work-shift sim, including the 2026 night-shift "(Anomaly)" hybrid.
last-researched: 2026-10-24
---

# Job sims (restaurant, store, "sell ___")

## In one line

Do a real job's steps by hand (fetch, prepare, serve, get paid), then buy machines and staff
that do each step for you until you're the manager of a growing shop. The 2026 variant puts
night-shift anomaly horror on top: earn by day, survive the strange customers or patients by
night.

Related: build-out bases and droppers are in [tycoon](tycoon.md) and
[conveyor-dropper-economy](../patterns/conveyor-dropper-economy.md); offline earnings in
[idle-offline-income](../patterns/idle-offline-income.md); anomaly horror (lighting, scares,
maturity) is in [horror](horror.md), which this file links rather than repeats.

## Core loop

- **Moment to moment (2–10 s):** one station action: grab stock, run a prep minigame (peel,
  cook, X-ray), hand the order over, collect cash.
- **Shift / session (15–30 min):** serve customers before their patience runs out, buy the next
  machine, automate one step after another, expand or decorate the shop.
- **Long term:** new products or recipes, bigger premises, staff tiers, offline income. In the
  anomaly variant: shift streaks, classes and new anomalies.

| Variant | Examples (players, data 2026-10-22) | Loop | Server |
|---|---|---|---|
| "Sell ___" production chain | Sell Lemons 25.5K (created 2025-03-17), Sell Ores 1.4K | Sell → cash → powers and deals; "100% of your income offline" (data, description) | 6–10 |
| Restaurant build-out | Restaurant Tycoon 3 6.5K, Run a Restaurant! 4.4K (99% likes), My Chiikawa Restaurant 3.5K | Cook, serve, build and decorate, hire staff, offline money (data, descriptions) | 6 |
| Co-op role job | Work at a Pizza Place 2.7K, 5.62B visits since 2008 | Team fills orders; pay buys house upgrades (data, description) | 12 |
| Hands-on trade | Wash the Car 7.6K, Firefighting Sim 5.9K, Welding Simulator 1.1K (80% likes) | One physical task done well, upgraded tools | 6–8 |
| Night-shift anomaly | Animal Hospital (Anomaly) 31.6K, Sell Fries! 30.1K, Clone Baby Care 15.9K, Airport Security 4.5K | Work by day or shift, spot what's wrong, survive | 16–30 |

**The automation ladder is the spine.** In Sell Fries! each purchase removes one manual step:
Conveyor $60, Auto Peeler $500, Potato Robots $1,000, Auto Fryer $6,000, then Fries Shooter
$12,000, which serves customers and defends the window (community, games.gg 2026-10-18). Each
step costs about 2–8× the one before, and each one replaces a chore the player has just been
doing by hand (inferred).

## Main verbs

Fetch, prepare (minigame), serve, charge, upgrade (station), automate or hire, expand,
decorate. The anomaly variant adds inspect, deny or expel, repair (power box), hide and
survive.

## Why players come back

- **The chore-to-manager arc.** Doing a step by hand for 3 minutes makes the machine that
  replaces it feel earned (inferred).
- **A job kids recognize.** Fries, pizza, a vet, airport security. The fantasy needs no
  explanation (inferred). Work at a Pizza Place has kept players since 2008 (data).
- **Something earned while away.** Sell Lemons, Run a Restaurant! and Restaurant Tycoon 3 all
  advertise offline income (data, descriptions 2026-10-22).
- **Gentle time pressure.** Sell Fries! customers wait about 50 seconds (community, games.gg
  2026-10-18): enough to rush, not enough to fail hard.
- **Anomaly variant: the streak.** Animal Hospital shows "Total Shifts" above your avatar in
  the lobby, and a new game restarts at day one (press, GosuGamers 2026). One more shift is the
  return hook, as with the night counter in 99 Nights in the Forest (press, same article).

## What separates top games from clones

1. **A tactile step at each station.** Sell Fries! makes you clear every bit of peel before a
   potato will cook (community, games.gg 2026-10-18). A click-to-collect clone has no job to
   automate away (inferred).
2. **A second tension on the work.** Night anomalies (Sell Fries!, Animal Hospital),
   dine-and-dashers and lazy staff to catch (My Chiikawa Restaurant), or teammates covering
   roles (Pizza Place) (data, descriptions). Without one, a job sim is a slow tycoon (inferred).
3. **A detailed inspection kit (anomaly variant).** Airport Security checks ID and photo,
   X-rays bags, body-scans for "wrong skeletons", watches cameras and runs lie-detector,
   brain, eye and fingerprint tests (data, description 2026-10-22). Many distinct checks mean
   many distinct anomalies, and that's the content (inferred).
4. **Sanity instead of HP.** Animal Hospital and Airport Security drop the health bar for a
   fear or sanity meter (press, GosuGamers; data, description). Mistakes build up instead of
   killing in one hit (inferred).
5. **Party-sized co-op.** Animal Hospital and Airport Security take parties of up to 4 (press;
   data). Shifts are designed around splitting stations (inferred).
6. **Weekly anomalies or recipes.** New anomalies and classes keep Animal Hospital changing
   (press, GosuGamers). Each one is a small, cheap content drop (inferred).

## Session shape

Targets are (inferred) unless tagged.

- **First 60 seconds:** first order served with the station steps shown as highlighted
  prompts; first cash pop; the first automation's price visible and reachable in 1–2 minutes
  (Sell Fries!'s $60 conveyor against $20–22 orders; community, 2026-10-18).
- **First 10 minutes:** 2–3 automations bought; the player has switched from doing to
  managing at least one station. In the anomaly variant, the first night starts by about
  minute 5–8 (Sell Fries! night starts at 8 p.m. game time; community).
- **Session:** a build-out session of 15–30 minutes, or one anomaly run of several in-game
  days, ending in a win or a wipe.
- **Day 7:** shop expanded or several runs won; chasing a rare class, a new product line or a
  shift-streak record.

## Social hooks

- **Station splitting.** One fetches, one preps, one serves. That's Pizza Place's whole
  design, and Sell Fries! guides call solo runs harder than team runs (data; community,
  allthings.how 2026-10-13).
- **Team buffs and revives.** Sell Fries!'s rarest class gives the team +50% money and revives
  a teammate once a day (community, games.gg 2026-10-18).
- **Shared shop.** Automate a Restaurant lets friends build and automate one restaurant
  together (data, description).
- **Comic friction.** "Tase your coworkers" (Airport Security, data). It gives friends a
  harmless way to mess with each other, and that makes clips (inferred; see
  [social-and-virality](../fundamentals/social-and-virality.md)).
- **Status in the lobby:** the shift-streak counter above the avatar (press, GosuGamers).

## Monetization that works here

- **Classes or roles with income bonuses.** Sell Fries! spins classes for 25 gems (one free
  ad spin a day): Common +5% money at 40% odds up to Divine +100% at 0.2% (community, games.gg
  2026-10-18). Animal Hospital sells some classes only for Robux (press, GosuGamers). If gems
  can be bought, a gem spin is a paid random item: show odds and gate it with `PolicyService`
  ([rarity-tiers-and-eggs](../patterns/rarity-tiers-and-eggs.md)).
- **Carry capacity.** Sell Fries!: Bucket 3 potatoes ($100), Vacuum 8 ($1,000), Golden Vacuum
  20 ($9,800 or 54 gems) (community, 2026-10-18). Sell bigger hands, not the ending.
- **Income multipliers and timed boosts.** Money Potion x1.5 for $13,000 in Sell Fries!
  (community). Use passes for permanent 2x and products for 15-minute boosts
  ([monetization](../fundamentals/monetization.md)).
- **Staff and automation passes:** an extra worker, faster robots, an auto-serve.
- **Rewarded ads** for a free daily spin: `AdService:ShowRewardedVideoAdAsync` (official; see
  [idle-incremental](idle-incremental.md) for the setup).
- **Offline cap upgrades** ([idle-offline-income](../patterns/idle-offline-income.md)).
- **Don't sell night skips as the main product.** Sell Fries! has a Shop Clock that skips to
  morning (community). If skips cost Robux, the horror half becomes something to pay your
  way out of (inferred).

## Common failure modes

- **Chores that never get automated.** Manual prep is fun for minutes, not hours (inferred).
- **NPC customers as full Humanoids with server pathfinding.** Dozens per server lag phones.
  Keep the customer queue as data on the server, and draw simple customer models on each
  client, moved with `TweenService` or `PVInstance:PivotTo` (inferred; see
  [performance](../fundamentals/performance-and-devices.md)).
- **Unanchored physics props** (potatoes, boxes, plates) piling up in every shop (inferred).
- **Client-trusted carry and serve.** The client says "I hold 20 potatoes" or "I served 50
  fries". Exploit scripts are advertised for Sell Fries! auto-farming (community, bo3.gg
  2026-10). The server must own stock, prep state and payouts
  ([security](../fundamentals/security-and-anti-exploit.md)).
- **Station hogging** in shared kitchens: one player blocks the only fryer. Give every
  player their own stations, or let several players use one at once (inferred).
- **Unreadable anomalies.** If the "wrong" detail can't be seen on a phone screen, deaths feel
  random (inferred). Read [horror](horror.md) for scare and lighting rules.
- **The fast decay of a viral anomaly game.** Animal Hospital peaked at 736,948 on
  2026-07-05 (press, GosuGamers citing Rolimon's). It had 31.6K on 2026-10-22, about 4% of
  that peak (data; calculated).
- **"Sell ___" as a title with nothing new to do.** The name is not the spin
  ([trend-lifecycle](../fundamentals/trend-lifecycle.md)).

## Saturation & opportunity

One tracker snapshot (data, 2026-10-22).

| Theme | Games | Players | Median | Leader (share) | Rising | Label |
|---|---|---|---|---|---|---|
| `sell-job` | 10 | 83K | 2.1K | Sell Fries! (36%) | 2 | mixed |
| `cooking-food` | 11 | 50K | 1.1K | Sell Fries! (60%) | 2 | – |
| `anomaly` | 6 | 84K | 10K | Animal Hospital (37%) | 4 | mixed |

- **The anomaly wave is young and not consolidated.** Its rising entries were created
  2026-09-21 to 2026-10-09 (Sell Fries!, Clone Baby Care, Airport Security, WRONG WAY!), and the
  leader holds 37%, well under the 60% "one game dominates" line (data). Clone Baby Care
  reached 15.9K 13 days after creation (data). Animal Hospital (created 2026-05-10) started the
  wave (inferred from creation dates).
- **The `anomaly` tag spreads past job sims.** WRONG WAY! puts anomalies on a co-op rally
  game: one player drives, one navigates (data, description). The anomaly layer works on top
  of almost any loop (inferred).
- **Calm restaurant games rate well but stay small.** Run a Restaurant! 99% likes at 4.4K,
  Automate a Restaurant 99% at 391 (data). The audience likes them; discovery doesn't push them
  far without a hook (inferred).
- **Chore sims are a neighbouring wave.** Clean the House! 5.2K, Clean Everything 4.8K, Clean
  all the Leaves 4.3K with 231M visits (data). Clean all the Leaves pairs a rake-and-sell loop
  with a 100% completion goal (press, Player.One 2026-08).
- **Read (inferred):** the best opening is a job players know, with 3–5 inspection or prep
  verbs and a night anomaly layer, in a 1–4 party. That hybrid is at stage 3 of a wave
  ([trend-lifecycle](../fundamentals/trend-lifecycle.md)). Pick a job not yet used (vet,
  fries, airport, babysitting are taken) and ship within 4 weeks.

## Scope for a solo dev

Good fit: stations are simple parts with `ProximityPrompt`s, customers can be simple shapes,
and the anomaly layer is mostly lighting and swapped models. Week counts are (inferred).

**MVP (calm job sim):** one shop, a 3–4 step product chain, customers with patience timers,
5 automation upgrades, 2 carry tiers, one expansion, offline income with a claim screen,
saving, 2x-income pass, timed boost.

**MVP (anomaly variant), adds:** a day/night cycle on `Lighting.ClockTime`, 4–6 anomalies
with clear counters, a run win condition, lobby → reserved-server party run
([round-system](../patterns/round-system.md)), a run-reward currency, 4–6 classes.

| Week | Build |
|---|---|
| 1 | Server-owned station state machine (stock → prepped → cooked → served); `ProximityPrompt` interactions with `HoldDuration`; one prep minigame; save ([player-data](../patterns/player-data.md)) |
| 2 | Customer queue (server data, client-rendered NPCs), patience and payouts, automation ladder from one tuning module ([upgrade-trees](../patterns/upgrade-trees.md)) |
| 3 | Expansion/decoration, offline income, passes and `ProcessReceipt`; anomaly variant: night phase, 3 anomalies |
| 4 | Anomaly variant: 2–3 more anomalies, win condition, party lobby, classes; phone test, maturity questionnaire, icon/thumbnail, launch |
| 5+ | Weekly: one new anomaly or product line; a seasonal night |

**Cut from v1:** farming side-loops, staff AI that walks around, multiple shop locations,
free-form furniture placement, trading.

## Top examples

- Sell Fries! (case study: sell-fries): fries chain, automation ladder, night
  anomalies and a find-the-key win; 30.1K at 31 days old (data, 2026-10-22).
- Animal Hospital (Anomaly) (no case study): the anomaly-job leader; check-in, treat, spot
  anomalies, sanity meter, shift streaks (press, GosuGamers).
- Airport Security (Anomaly) (no case study): the most detailed inspection kit in the wave
  (data, description).
- Work at a Pizza Place (no case study): the 2008 co-op role job, still charting (data).
- Run a Restaurant! (no case study): calm cook-serve-hire build-out at 99% likes (data).

## Build checklist for agents

### Do

- Keep stock, prep state, carry count, cash and payouts on the server. The client sends
  "interact with station X", and the server checks distance and state.
- Make every automation replace exactly one manual step, priced about 2–8× the previous one
  (Sell Fries! ladder: $60 → $500 → $1,000 → $6,000 → $12,000; community, 2026-10-18).
- Make the first automation affordable within 1–2 minutes of the first sale (inferred).
- Give each station a distinct, phone-friendly action: a hold prompt, a short swipe or tap
  minigame, a timing bar (inferred; see [ui-ux](../fundamentals/ui-ux.md)).
- Set customer patience at about 40–60 s, with a visible timer over each customer (inferred
  from the ~50 s in Sell Fries!).
- Render customers on the client from a server queue; keep at most 6–10 on screen per shop
  (inferred).
- Anomaly variant: give each anomaly one readable tell and one counter (shutter, hold-to-scare,
  leave the circle, fix the power box), as Sell Fries! does (community, 2026-10-18).
- Anomaly variant: use a sanity or fear meter instead of one-hit deaths, and raise the anomaly
  count each night (community; press).
- Anomaly variant: run parties of 1–4 in reserved servers from a lobby, and show the streak in
  the lobby.
- Fill out the maturity questionnaire honestly for jumpscares ([horror](horror.md)).

### Don't

- Don't let the client report items carried, orders served or money earned.
- Don't use unanchored physics parts for stock or food.
- Don't put more than one shared fryer or till on a map where several players work.
- Don't sell the night skip or the run's win item for Robux.
- Don't copy another job game's job and anomaly set, or its names, art or sounds. Fries, a vet
  hospital, an airport and babysitting are taken.
- Don't paste other games' names into your description as search tags (the Sell Fries! page
  lists other titles; inferred risk: it reads as spam to players and to discovery).
- Don't build farming, staff AI or multiple locations before launch.

## Sources

1. private/trends/latest.md and tools/trends lookups — themes, players, visits, likes, created, server sizes, descriptions (data, 2026-10-22)
2. https://games.gg/roblox/guides/sell-fries-beginners-guide/ — Sell Fries! chain, upgrade prices, customer patience, classes and odds, anomalies (2026-10-18)
3. https://allthings.how/?p=266774 — Sell Fries! walkthrough: day/night, perks, teams, win condition (2026-10-13)
4. https://www.gosugamers.net/entertainment/news/78741-animal-hospital-becomes-roblox-s-latest-horror-sensation-here-s-everything-you-need-to-know — Animal Hospital loop, sanity, shifts, party of 4, peak 736,948 on 2026-07-05 (Rolimon's)
5. https://www.roblox.com/games/108334808788078 — Airport Security (Anomaly) description: inspection tools, party of 4, fear meter
6. https://www.roblox.com/games/79268393072444 — Sell Lemons description: offline income
7. https://www.roblox.com/games/77843161404023 — Run a Restaurant! description: cook, serve, build, hire, offline
8. https://www.roblox.com/games/192800 — Work at a Pizza Place description: team orders, house upgrades
9. https://www.player.one/clean-all-leaves-suddenly-one-robloxs-biggest-games-why-are-players-raking-leaves-163958 — chore-sim loop and completion goal (2026-08)
10. https://bo3.gg/de/articles/sell-fries-scripts — exploit scripts advertised for Sell Fries! (evidence of client-side farming attempts)
11. https://create.roblox.com/docs/reference/engine/classes/ProximityPrompt — Triggered, HoldDuration
12. https://create.roblox.com/docs/reference/engine/classes/Lighting — ClockTime
13. https://create.roblox.com/docs/reference/engine/classes/AdService — rewarded video ads

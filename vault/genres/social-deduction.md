---
title: Social deduction
type: genre
read-when: Building a hidden-role round game (Murder Mystery-like murderer/sheriff/innocents), role odds, detection, or a knife/gun cosmetics economy.
last-researched: 2026-10-24
---

# Social deduction

## In one line

Short rounds where one secret killer hunts a crowd, one secret protector has the only gun, and
everyone else survives by watching who acts strangely. The round is free entertainment; the
cosmetic weapons you collect and trade are the long-term game. The genre on Roblox is
Murder Mystery 2 (case study: murder-mystery-2), #2 on the platform with 675K players
(data, 2026-10-22). List it as **Survival / 1 vs All** (data). Visible killer-vs-team rounds
with rosters live in [asymmetric-survival](asymmetric-survival.md).

## Core loop

- **Moment to moment (5–30 s):** innocent: grab coins, stay in sight lines, watch hands and
  movement, run from a drawn knife. Murderer: blend in, isolate a target, stab or throw, break
  line of sight. Sheriff: shadow the crowd, wait for proof, take one careful shot.
- **Round (1–3 min, inferred):** lobby with map vote → roles revealed privately → murderer's
  knife arrives 10 s after start (community wiki, MM2) → kills, a sheriff shot, maybe a dropped
  gun picked up by a "Hero" → results with XP and coins.
- **Session (20–60 min, inferred):** many rounds in one server; the chance to be the killer
  rises every round you aren't (community wiki, MM2).
- **Meta (months to years):** coins → boxes → weapon skins in rarity tiers → trading for rarer
  ones; seasonal events with battle passes and limited items (community wiki, MM2).

## Main verbs

Innocent: collect, watch, hide, run, warn, pick up the gun. Murderer: blend, stalk, stab,
throw, fake, use a power. Sheriff/Hero: observe, track, aim, shoot. Everyone: vote for a map,
spectate, trade, show off.

## Why players come back

- **A role lottery every round.** Any round might make you the killer or the gun. Rare roles
  feel like a reward, and pity weighting makes them arrive (inferred; MM2 raises murderer odds
  each round you miss, community wiki).
- **Tiny commitment.** Rounds are minutes long and dead players spectate, so "one more round"
  is cheap (inferred).
- **Collection and trading.** MM2's description pitches "Collect and trade hundreds of knives"
  (data, game description 2026-10-22). Weapon skins have no gameplay effect, so value is pure
  rarity and taste (press, RoWatcher guide 2026).
- **Events.** MM2's Halloween 2025 event peaked at 603,346 (press, RoWatcher, unverified); its
  Summer 2026 event set a 1,349,555 record (press, StudioKrew 2026-08, unverified).
- **Friends and creators:** chaos with friends and YouTube creators keep it visible (press,
  RoWatcher guide).

## What separates top games from clones

- **Wrong accusations cost the accuser.** In MM2, a sheriff or hero who shoots an innocent dies
  too (community wiki). Without that rule the gun holder shoots everyone and deduction dies
  (inferred).
- **One gun, transferable.** The sheriff's gun drops on death and any innocent can become the
  Hero (community wiki). A second chance keeps innocents engaged after the protector falls
  (inferred).
- **Readable, slightly slow weapons.** MM2's gun reloads after every shot; the knife can be
  thrown after a wind-up (community wiki). Every attack is a tell someone might see (inferred).
- **Deduction without talking.** Many players can't chat: chat needs an age check since
  2026-01, and Select accounts (9–15) without one have chat off (official, see
  [social](../fundamentals/social-and-virality.md#voice-and-chat-constraints-2026)). MM2's clues
  are visual (a drawn knife, a body, someone following the sheriff), so it works silently
  (inferred).
- **An economy that outlives the rounds.** Limited event items go off sale and stay tradeable
  (official game-pass API 2026-10-24: 28 GODLY passes, nearly all off sale). Clones copy rounds
  and lack the inventory players already own (inferred).

## Roles and odds

| Role | Count (12 players) | Goal | Tool |
|---|---|---|---|
| Murderer | 1 | Eliminate everyone | Knife (stab, throw), one power |
| Sheriff | 1 | Shoot the murderer | Gun with reload |
| Hero | 0 at start | Innocent who picked up the dropped gun | Same gun |
| Innocent | 10 | Survive, or become the Hero | None |

MM2 facts (community wiki, 2026-10): max 12 per server (data); murderer chance starts low and
rises each round you aren't picked; sheriff odds depend only on player count.

Rules (inferred):
- **Weighted murderer pick:** `weight = 1 + roundsSinceMurderer` over players in the round;
  then a uniform sheriff pick from the rest. Reset on pick. With 12 players everyone gets a
  turn within roughly 12–20 rounds, instead of a 1-in-12 coin flip forever.
- **No back-to-back murderer**, no murderer and sheriff in the same party (friends would
  cooperate), exclude AFK players and anyone who joined in the last 5 s.
- **Minimum 3 players** (murderer, sheriff, one innocent). Below that, run a lobby minigame or a
  1v1 duel mode rather than an empty round.
- Scale above 12: add a second murderer per ~10 innocents only with team rules (they can't hurt
  each other).

## Clue and detection design

Every clue source needs an owner and a counter (inferred):

| Clue | Who reads it | Counter for the murderer |
|---|---|---|
| Drawn weapon in hand | Everyone nearby | Draw only when alone; quick stab |
| Kill witnessed | Anyone with line of sight | Isolate targets; corners |
| Body or ragdoll left behind | Passers-by | Kill far from crowds |
| Movement: following, lingering | Sheriff, innocents | Act like an innocent, collect coins |
| Footprint trails | MM2 murderer's free "Footsteps" power, to track others (community wiki) | — |
| Unique kill effect (burning bodies) | Everyone | Don't equip it (MM2 tip, community wiki) |

- **Disguise mode** removes avatar clues: MM2's Disguises renames players by the NATO alphabet,
  makes avatars look alike and turns off pets and radios (community wiki). With no artist this
  is cheap and makes the game about behavior (inferred).
- **Murderer powers** (MM2: ghost 5 s, x-ray 4 s, traps freezing 4 s, sprint +50% for 5 s,
  fake gun, decoys; coin-bought) add variety but each must have a tell or a cooldown (community
  wiki; inferred).
- Keep ambient light high: deduction needs sight. Dark maps belong to [horror](horror.md)
  (inferred).

## Round flow and tuning

See [round-system](../patterns/round-system.md) for phase machines, map voting, late joiners
and spectating. Starting values (inferred):
- Intermission 15–20 s with a 3-map vote; role reveal 3 s, shown only to the owner.
- Murderer weapon after 10 s (MM2, community wiki) so the crowd can scatter.
- Round cap 2–3 min; most rounds should end early by a shot or a wipe. Log median round length.
- Sheriff gun: one shot, 2–3 s reload, hitscan from the head with a server check.
- Knife: stab range 5–7 studs, 1 s cooldown; throw after a 0.5–1 s wind-up, visible projectile.
- Murderer walks at default 16; a speed power adds ≤10% (MM2 Haste: +10%, community wiki).
- Coins: capped per round so AFK farming is pointless (MM2: 40, or 50 with the Elite pass,
  community wiki).
- Results: winner side, survivors, XP; dead players spectate and return in under 10 s.

## Server authority and anti-exploit

- **Roles are server secrets.** Never put a role in a Player attribute, `Team`, `leaderstats` or
  any replicated value; send each player only their own role with `RemoteEvent:FireClient`
  (inferred; "role ESP" scripts read anything replicated). Keep the knife and gun in
  `ServerStorage` until the role holder equips them.
- **Hits are server decisions:** distance and cooldown for stabs; server raycast for shots and
  throws with a small tolerance; the wrong-shot penalty runs on the server
  ([security](../../.claude/skills/roblox-code/references/security.md)).
- Ban speed and teleport exploits with server checks; `Players:BanAsync` with an appeal path
  (official API; see security file).
- Rate-limit every remote, including the map vote ([round-system](../patterns/round-system.md#map-voting)).

## Session shape

- **First 60 seconds:** join → lobby (playable, shop visible) → if a round is running,
  spectate it with a role explainer; next round within ~30 s (inferred).
- **First 10 minutes:** 4–6 rounds as an innocent, at least one as murderer or sheriff (pity
  weighting), first coins toward a 1,000-coin box (MM2 box price, community wiki) (inferred).
- **Day 7:** level 10 (MM2's trading gate since 2021-12-28, community wiki), a first Godly or
  event item, first trades (inferred).

## Social hooks

Join friends' servers; parties never split into murderer and sheriff (inferred); private
servers with a "lobby mode" that holds rounds (MM2, community wiki); trading in the lobby;
emotes and radios (MM2 Radio pass 475 Robux, official API 2026-10-24); clip-ready moments: the
last-second Hero shot, a knife throw across the map (inferred);
`SocialService:PromptGameInvite` after a win ([social](../fundamentals/social-and-virality.md)).

## Monetization that works here

- **Cosmetic weapons** (knife and gun skins, kill effects, pets): no gameplay effect (press,
  RoWatcher).
- **Event battle passes** with event currency earned in rounds: MM2 Halloween 2026 has a
  30-tier pass ending in an Ancient gun (press, Timesaver 2026-10, unverified).
- **Limited Robux bundles** sold only during an event (MM2 Mortal Bundle 3,399 Robux, on sale
  2026-10-24, official API). Scarcity drives trade value (inferred).
- **A perk pass:** MM2 Elite 499 Robux gives 1.5× XP and a 50-coin cap (official API).
- **Boxes with premium currency:** MM2 boxes cost 1,000 coins or 100 diamonds (community wiki).
  Any box bought with Robux-bought currency is a **paid random item**: show odds summing to 100%
  and gate with `PolicyService` ([monetization](../fundamentals/monetization.md#paid-random-items-eggs-crates-spins-luck-boosts-pity)).
- Tradeable Robux items need `IsPaidItemTradingAllowed` checks; real-money trading and item
  gambling are banned ([trading](../patterns/trading.md#roblox-rules-official-community-standards-and-creator-docs-2026-10)).
- Don't sell gameplay power for Robux only (bigger hitbox, faster reload) (inferred).

## Common failure modes

- **Gun holder sprays** because wrong shots are free (inferred).
- **Murderer wipes the server in 15 s:** knife too fast, no wind-up, map too small (inferred).
- **Roles leak:** role stored in a replicated value; exploiters ruin every round (inferred).
- **Empty servers:** a 12-player design that needs 6+ to be fun at 50 CCU (inferred).
- **Teaming and griefing:** friends split roles and cooperate; murderer AFK. Fix with party
  rules and AFK swaps ([asymmetric-survival](asymmetric-survival.md#toxicity-and-afk-handling)).
- **Dupes and scams** once items have value (MM2's wiki lists duping, scams and data loss as
  trading risks, community). Ship trading late ([trading](../patterns/trading.md)).

## Saturation & opportunity

All (data, 2026-10-22) unless tagged:
- **1 vs All:** 843K across 8 games, MM2 80%. **`murder-mystery` theme:** 5 games, 767K,
  "one game dominates" (MM2 88%), **0 rising**.
- **The 675K is an event number.** MM2 reached 1.80M and #1 on 2026-10-25 03:24 UTC (data,
  second snapshot). Its Halloween 2026 event started 2026-10-18 (press, Timesaver, unverified);
  its typical level was ~153K earlier in 2026 (press, RoWatcher, unverified). Expect a fall
  after the event ends 2026-11-16 (inferred).
- **The other "murder" games are duels, not deduction:** Murderers VS Sheriffs 74.3K (Action /
  Battlegrounds, 30 per server, created 2025-02-09), Murder Duels 8.9K (Shooter, knife and
  revolver skins, trading), MVSD 7.8K. They keep the knife/gun skins and drop the hidden roles.
- No other hidden-role game is charted in our snapshot (data); small ones may exist below the
  chart cut-off (Rolimons off).
- **Opportunity (inferred):** competing head-on with a 12-year inventory economy is a losing bet.
  Better: (1) a duel or arena mode with a skin economy, the lane with the youngest charted
  entries (Murderers VS Sheriffs created 2025-02, Murder Duels 2026-01, data); (2) a
  deduction twist MM2 doesn't do: tasks with information rewards, a detective with limited
  scans, a theme (ship, train, school play) with Mild rating; (3) small 6–8 player servers that
  fill at low CCU.

## Scope for a solo dev

**MVP (5–7 weeks, one dev with Claude Code, no artist) (inferred):** 8–12 player server, lobby
with a 3-map vote, 3 small maps, murderer/sheriff/hero/innocent with weighted roles, knife stab
and throw, gun with reload and wrong-shot penalty, coins capped per round, spectate, results,
XP levels, one box of ~12 cosmetic skins with an odds screen, saving.

| Week | Build |
|---|---|
| 1 | Round phases, map vote, weighted role pick, private role reveal ([round-system](../patterns/round-system.md)) |
| 2 | Knife (stab, throw) and gun (hitscan, reload, penalty, drop and Hero pickup), all server-side |
| 3 | 3 greybox maps with sight lines and loops; coins; spectate |
| 4 | Results, XP, coin save ([player-data](../patterns/player-data.md)); AFK and party rules |
| 5 | Cosmetic skins, box with odds, equip UI ([inventory](../patterns/inventory.md)) |
| 6–7 | Phone controls (tap-to-shoot, throw button), onboarding, metadata, Disguises-style mode |

- **No artist:** skins as color, `Material` and `Neon` swaps on one knife and one gun mesh, plus
  `Trail` and particle effects (inferred).
- **Cut:** trading (add after dupes are impossible), crafting, murderer powers, pets, radios,
  event passes, extra modes (inferred).

## Top examples

- Murder Mystery 2 (case study: murder-mystery-2): the genre; 675K, 12 per server, 91%
  likes, 12.8 years old (data, 2026-10-22).
- Murderers VS Sheriffs: team duels with MM2-style weapons; 74.3K (data, 2026-10-22).
- Murder Duels: first-person 1v1–4v4 duels, knife + revolver with abilities, skin trading;
  8.9K (data, 2026-10-22).
- Forsaken (case study: forsaken) and Flee the Facility: visible killer rounds, see
  [asymmetric-survival](asymmetric-survival.md).

## Build checklist for agents

### Do
- Make a wrong shot kill the shooter too; let the dropped gun make a Hero.
- Pick the murderer with pity weights; never repeat back to back; keep parties off opposite roles.
- Keep roles and weapons out of every replicated value until visible in the world.
- Decide stabs, throws and shots on the server with distance, raycast and cooldown checks.
- Delay the murderer's weapon ~10 s; give every attack a visible tell (draw, wind-up, reload).
- Cap coins per round; pay XP for surviving and correct shots, not idle time.
- Design clues that work without chat (visible weapons, bodies, movement).
- Start rounds at 3 players; scale map size to the player count.
- Show odds summing to 100% before any box opens; gate paid boxes and paid-item trading with
  `PolicyService`.
- Log round length, murderer win rate (target 40–60%) and wrong-shot rate.

### Don't
- Don't use `Team` objects, Player attributes or `leaderstats` for hidden roles.
- Don't trust a client "I hit him" or client hit detection.
- Don't sell stat or hitbox advantages; cosmetics only (powers for soft currency at most).
- Don't ship trading before GUID items, session locking and dupe checks ([trading](../patterns/trading.md)).
- Don't build chat- or voice-dependent deduction.
- Don't reuse MM2's names (Godly, Chroma, Seer, item names), maps, knife designs or title pattern.

## Sources

1. private/trends/latest.md, `trends lookup` and the tracker DB — 1 vs All, murder-mystery theme, per-game numbers, server sizes, descriptions (data, 2026-10-22)
2. https://murder-mystery-2.fandom.com/wiki/Murderer — rising murderer odds, knife after 10 s, powers usage (community wiki, read via API 2026-10-24)
3. https://murder-mystery-2.fandom.com/wiki/Sheriff — sheriff odds by player count, reload, wrong-shot penalty
4. https://murder-mystery-2.fandom.com/wiki/Hero — dropped gun, Hero rules
5. https://murder-mystery-2.fandom.com/wiki/Coins — 40-coin cap, 50 with Elite
6. https://murder-mystery-2.fandom.com/wiki/Powers — murderer powers, durations, cooldowns, prices
7. https://murder-mystery-2.fandom.com/wiki/Disguises — disguise mode rules
8. https://murder-mystery-2.fandom.com/wiki/Trading — level-10 gate since 2021-12-28, trade rules, risks
9. https://murder-mystery-2.fandom.com/wiki/Mystery_Box_2 — box price and tier odds
10. https://rowatcher.com/news/what-is-murder-mystery-2-a-guide-to-roblox-s-legendary-social-deduction-game — 12 players, cosmetics without gameplay effect, community value sites, Halloween 2025 peak, typical CCU, longevity reasons (third-party, 2026)
11. https://studiokrew.com/blog/top-roblox-games-august-2026/ — Summer 2026 record 1,349,555 (third-party, unverified)
12. https://timesaver.gg/blog/mm2-halloween-event — Halloween 2026 dates, 30-tier pass, box (unverified)
13. https://apis.roblox.com/game-passes/v1/universes/66654135/game-passes — Elite, Radio, Mortal Bundle prices; off-sale GODLY passes (read 2026-10-24)
14. https://create.roblox.com/docs/production/monetization/paid-random-items — odds disclosure and policy gating

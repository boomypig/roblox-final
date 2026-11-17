---
title: Party and minigame games
type: genre
read-when: Building a minigame rotation, an elimination gauntlet (Squid Game-likes), hide and seek or tag, a 1v1 party duel, or a framework to make many small games cheaply.
last-researched: 2026-10-25
---

# Party and minigame games

## In one line

Short rounds of simple rules, 30–90 s each, that change every round so nobody masters the game
and anyone can win one. Roblox files them as **Party & Casual** (subgenres Minigame, Childhood
Game, Quiz, Coloring & Drawing) (data). Three shapes chart today:

| Shape | Example (data, 2026-10-25) | What wins a round |
|---|---|---|
| **Rotation** of many minigames between lobby breaks | Epic Minigames: "142 unique minigames" plus a party board-game mode (data, description); 2,175 players, 12 per server, created 2015 | Survive, finish, or score in that minigame |
| **Elimination gauntlet**: a fixed series of deadly tests, last ones standing win | Squid Game X 22.5K (80 per server); Ink Game 14.8K (100 per server, "3 endings"); DON'T GET ELIMINATED 4.2K (50 per server, players vote others out) | Not being cut |
| **One mechanic, polished** | Hot Potato 7.0K, Knockout! 3.2K, Hide In Pixels 7.0K, Duck Duck (Tag) 3.2K, 1v1 Minigame Duel 2.7K | Last alive, or best of 3 |

The user's round loop is in [round-system](../patterns/round-system.md); obby races and disaster
survival are in [round-based-races-and-survival](round-based-races-and-survival.md).

## Core loop

- **Moment to moment (5–20 s):** read the rule banner → move, dodge, push, hide or answer →
  watch someone else fail.
- **Round (30–90 s, inferred):** intermission → minigame announced with a one-line rule →
  3-2-1 → play → winners flash → back to lobby. Epic Minigames' Treacherous Tiles is won by
  surviving a whole minute (community wiki).
- **Match / session (15–45 min, inferred):** 10–30 rounds; in a gauntlet, 5–8 games with cuts
  until a final duel; coins and XP every round.
- **Meta (weeks):** levels, coins → cosmetics, gear, pets and effects (Epic Minigames, data,
  description); new minigames as updates.

## Main verbs

Run, jump, dodge, push, grab, hide, seek, tag, pass, guess, vote, survive, spectate.

## Why players come back

- **Variety without depth.** A new rule every minute; a bad round is over fast (inferred).
- **Everyone wins sometimes.** Free-for-all minigames reward every survivor, so weak players
  still win rounds (community wiki: Epic Minigames' free-for-all games have "multiple
  winners").
- **Big moments with friends:** last-second escapes, betrayals, being voted out (inferred).
- **Show tie-ins:** Ink Game peaked around 514K on 2025-09-21, months after a TV season aired
  (third-party RoWatcher, unverified). Squid Game X, created 2021-09-24, still updates (data,
  updated 2026-10-22). IP waves fade; the mechanics remain (inferred).

## What separates top games from clones

- **Readable rules in one line and one look.** The map shows the rule (red-flashing tiles sink
  next, community wiki); new players understand within 3 s (inferred).
- **Mixed win types.** Epic Minigames sorts its games into free-for-all (many winners), team
  (red vs blue), solo winner (draw if several remain) and 1 vs everyone (one player controls
  the hazards) (community wiki).
- **One mechanic, several maps.** Many Epic Minigames entries list 2–4 maps (original plus
  e.g. glacier, candylands) (community wiki). Doubling content by reskinning a mechanic is the
  genre's main cost trick (inferred).
- **The eliminated stay busy:** spectate, lobby toys, side games or bets (inferred; see
  [round-system](../patterns/round-system.md#lives-elimination-and-losing)).
- **Hard cheat stance** in big servers: Ink Game's description warns cheaters of permanent bans
  (data, 2026-10-25). One flyer ruins 99 players' round (inferred).

## Minigame framework: how to make many games cheaply

Rules (inferred unless tagged):
- **One ModuleScript per minigame** in `ServerScriptService.Minigames`, all with the same
  shape: `Name`, `Rule` (one line), `Kind` (`FFA` | `Team` | `Solo` | `OneVsAll`), `MinPlayers`,
  `MaxPlayers`, `Duration`, `Maps` (list), and functions `Setup(map, players)`, `Start()`,
  `OnPlayerOut(player)`, `GetWinners()`, `Cleanup()`.
- **The round controller owns everything else:** intermission, pick, map load, countdown, end
  check, results, rewards, cleanup ([round-system](../patterns/round-system.md)). A minigame
  never touches currency, data stores or UI phases.
- **Pick rule:** filter by player count; weighted random; never one of the last 3 played; a
  new minigame gets extra weight in its first week. Optional vote among 3, as for maps.
- **Shared kit**, so a new minigame is 50–200 lines plus a map: kill zones, falling/sinking
  tiles, timed hazard spawner, projectile launcher, push/knockback, zone-capture counter, team
  splitter, "last N alive" tracker, collectible spawner, `CollectionService` tags for hazards.
- **Maps** are Models in `ServerStorage.Minigames.<Name>`, cloned in and destroyed after; every
  map has a `Spawns` folder and a bounding box for out-of-bounds checks.
- **Cleanup is the bug farm.** Track every connection, clone and attribute a minigame creates
  in one cleanup object and destroy it on end, on error (`pcall` around `Start`) and on server
  shutdown. Reset `WalkSpeed`, `JumpHeight`, tools and teams on every player.
- **Timeouts:** every minigame ends by `Duration` even if its own win check never fires.
- **Test harness:** a Studio command that runs any minigame with 1–4 test players, so each one
  is playtested alone via Studio MCP before entering the rotation.
- **Build order for new minigames:** a survival FFA (cheapest, ~1 day), a race, a team
  capture, a 1-vs-all controller, then hide and seek (most tuning).

## Elimination gauntlets

- **Structure (inferred):** 5–8 tests per match; each test cuts a share (survival tests cut
  whoever fails; scored tests cut the bottom 20–40%); a final 1v1 or 2-player test; winner
  gets the big reward, everyone gets XP per test survived.
- Squid Game X lists 16 modes, from light-and-movement tests and a dalgona-style cut-out to tug
  of war, a glass bridge and hide and seek "with keys and knives" (data, description
  2026-10-25). Ink Game offers "rebel" and alternate finales, so players can fight the game
  instead of each other (data, description).
- **Players voting each other out** adds drama with no art (DON'T GET ELIMINATED, data); cap it
  so friends can't farm strangers (one vote per player, hidden until close) (inferred).
- **Scale:** gauntlets chart with 50–100 servers (data). At low CCU, fill to 12–20 and scale
  cut sizes to the count (inferred).
- **IP:** don't use the show's name, doll, guards, uniforms, songs or game names; theme the
  gauntlet on something original (hard rule).
- **Maturity:** deaths by gunfire or falls read as violence. Keep defeats cartoonish (ragdoll,
  poof) to stay Mild ([audience](../fundamentals/audience.md)).

## Hide and seek and tag

Charted: Squid Game X's hide and seek mode (data); Chameleon! (paint yourself to match the map,
15 per server) 3.3K; Hide In Pixels (paint your character block by block to match a picture,
1v1, best of 3) 7.0K; Duck Duck (Tag) 3.2K (data, 2026-10-25). Epic Minigames includes hide
modes in its list (community wiki).

Rules (inferred):
- **Ratio** 1 seeker per 5–6 hiders; seekers frozen and blinded for 15–30 s while hiders hide.
- **Round cap 2–3 min.** Anti-stalemate: from the halfway mark, ping a random hider's area
  every 20–30 s; hiders that never move get pinged first.
- **Found hiders join the seekers** (snowball) or spectate; never wait out the timer idle.
- **Server-side tagging:** distance plus line-of-sight check on the server; client "I tagged him"
  is ignored ([security](../fundamentals/security-and-anti-exploit.md)).
- **Paint-to-hide is free-form creation:** freehand painting or pixel grids others see are
  16+ only (official, 2026-10; see [audience](../fundamentals/audience.md)). A fixed palette of
  preset camo skins avoids that (inferred).
- **Map:** many medium hiding spots, no unreachable holes; seal clip-through gaps; test with a
  bot that flags spots a seeker can't reach (inferred).

## Session shape

- **First 60 seconds:** spawn in a lobby with toys; the next minigame starts within 20 s; a
  one-line rule banner plus a 3 s preview (inferred; see
  [first-time experience](../fundamentals/first-time-experience.md)).
- **First 10 minutes:** 6–8 minigames, at least one win (free-for-all survival is likely), first
  coins and a level-up (inferred).
- **Day 7:** a favorite minigame, a cosmetic bought, a few gauntlet finals reached (inferred).
- **Downtime share ≤ 25%** of the cycle ([round-system](../patterns/round-system.md#tuning-ranges-inferred-unless-tagged)).

## Social hooks

Team minigames that split friends or put them together; 1-vs-all controller roles; vote-outs;
spectating with emotes; private servers with a minigame picker (Knockout! gives private-server
owners admin commands, data); `SocialService:PromptGameInvite` after a win; clip moments: a
last-second save, a betrayal, a 100-player cut
([social](../fundamentals/social-and-virality.md)). Rules must work without chat.

## Monetization that works here

- **Cosmetics:** skins, trails, titles, win and death effects (Hot Potato, data; Epic
  Minigames gear, pets, effects, data). 1v1 Minigame Duel advertises that paid items "never make
  you stronger" (data, description 2026-10-25).
- **VIP / private servers** with minigame choice and admin tools (data, Knockout!; see
  [private-servers](../patterns/private-servers.md)).
- **Coin multipliers** and daily rewards ([daily-rewards](../patterns/daily-rewards-and-streaks.md)).
- **Avoid:** paid revives in an elimination match, paid immunity, or buying the next minigame
  for everyone. They sell, but they decide who wins (inferred).
- Gear bought with Robux that changes outcomes (speed coil, gravity) belongs only in casual
  rotations, never in gauntlet finals (inferred).

## Common failure modes

- **One-note rotation:** 5 minigames that are all "dodge falling things" (inferred).
- **Minigame leaks:** leftover hazards, a player stuck at 0 `WalkSpeed`, a team color that
  stays; caused by missing cleanup (inferred).
- **Needs 8 players to be fun** at 30 CCU. Every minigame needs a 1–2 player version or a
  bot (1v1 Minigame Duel plays vs the CPU when nobody's around, data).
- **Long waits for the eliminated** in 100-player gauntlets (inferred).
- **Exploits** in big servers: flying over hazards, teleporting to finish; validate on the
  server ([security](../fundamentals/security-and-anti-exploit.md)).
- **IP takedown risk** from show-branded games (inferred).

## Saturation & opportunity

All (data, 2026-10-25) unless tagged:
- **Party & Casual: 47 charted games, 181K players, 1.6% share** (−0.3 pts vs 2026-10-22).
  Subgenres: none set 18 games 96.6K; Minigame 14 games 58.2K; Coloring & Drawing 2, 12.7K;
  Childhood Game 3, 7.0K; Quiz 10, 6.4K.
- **The `party-minigames` theme (4 games, 5.4K, +222%) undercounts the genre.** It matches name
  keywords, so Squid Game X and Ink Game (37K together) are untagged; the +222% comes from a
  tiny base and 1v1 Minigame Duel entering the charts between snapshots.
- **Big gauntlets are older:** Squid Game X (2021), Ink Game (2024-12-31). Both rose 12.9K →
  22.5K and 9.8K → 14.8K between snapshots (time of day and weekend; data).
- **New entries are single-mechanic games:** Ball VS Ball 31.1K (2026-08-12, auto-battle with
  collectible balls, a new breakout), Hot Potato (2026-06-27), Color My Flag 7.3K (2026-08-04),
  Hide In Pixels (2026-09-25), Paint a Pancake 5.7K (2026-09-23), Stick Wars 4.4K (2026-10-02),
  Choose the Stronger Animal 3.7K (2026-09-21). Collections of 100+ minigames are not what's
  charting new (Epic Minigames 2.2K).
- **Opportunity (inferred):** one polished party mechanic with a twist and 1–2 minute rounds,
  playable at 2 players, with cosmetics; or a curated 10–15 minigame rotation built on the
  framework above, with a weekly new minigame as the update. Avoid show IP and paint-to-hide
  (16+).

## Scope for a solo dev

**MVP (5–6 weeks, inferred):** lobby with toys; framework; 8 minigames (3 FFA survival, 1 race,
2 team, 1 one-vs-all, 1 hide and seek), one map each; coins, XP, levels; cosmetic shop with 10
trails and effects; results screen; 12–16 player servers; bots or solo versions for 1–2 players.

| Week | Build |
|---|---|
| 1 | Round controller ([round-system](../patterns/round-system.md)), minigame module contract, pick rule, cleanup object, test harness |
| 2 | Shared kit (kill zones, tiles, spawner, knockback, teams); 3 FFA survival minigames |
| 3 | Race, 2 team minigames, 1-vs-all controller UI |
| 4 | Hide and seek; spectate; results and rewards; saves ([player-data](../patterns/player-data.md)) |
| 5 | Shop and cosmetics ([shops](../patterns/shops.md)); phone controls; one-line rule banners |
| 6 | Playtests at 1, 4 and 12 players; anti-exploit checks; metadata; launch |

- **After launch:** 1 new minigame or map variant per week (inferred; see
  [live-ops](../fundamentals/live-ops-and-updates.md)).
- **Cut:** a board-game mode, 100-player gauntlets, voting-out, trading, pets, gear that
  changes outcomes (inferred).

## Top examples

- Epic Minigames: 142 minigames, four win types, map variants, a party board mode; 2.36B visits,
  91% likes (data, 2026-10-25; community wiki).
- Squid Game X: 16-mode elimination gauntlet, 80 per server; 22.5K, 94% likes (data, 2026-10-25).
- Ink Game: 100-player gauntlet with three finales and a combat practice mode; 14.8K, 79% likes
  (data, 2026-10-25).
- Hot Potato: pass-the-bomb tag, final-2 duel; 7.0K, 12 per server (data, 2026-10-25).
- 1v1 Minigame Duel: table games vs a friend or the CPU; 2.7K (data, 2026-10-25).

## Build checklist for agents

### Do
- Give every minigame the same module contract and let the round controller own phases,
  rewards and data.
- Destroy every clone, connection and attribute in one cleanup path, also on error and timeout.
- Reset movement, tools and teams on every player after each minigame.
- Show the rule in one line plus a 3 s preview; start the next minigame within 20 s.
- Mix win types (FFA, team, solo, 1-vs-all) and never repeat one of the last 3 minigames.
- Make every minigame playable with 1–2 players, or fall back to bots.
- Keep the eliminated busy: spectate, lobby toys, quick side games.
- Decide tags, hits, falls and finishes on the server.
- Reuse each mechanic across 2–3 map variants before writing a new mechanic.

### Don't
- Don't sell revives, immunity or minigame picks in competitive matches.
- Don't let freehand painting or pixel canvases in unless you accept 16+.
- Don't use a TV show's or another game's names, characters, songs or minigame names
  (no Squid Game, Red Light Green Light, glass bridge branding).
- Don't let a minigame hang a round; every one ends at `Duration`.
- Don't design rules that need chat to explain.

## Sources

1. private/trends/latest.md, `trends lookup` and the tracker DB — Party & Casual subgenres, party-minigames theme, per-game players, server sizes, created dates, descriptions (data, 2026-10-22 and 2026-10-25)
2. https://epic-minigames.fandom.com/wiki/Free-For-All, https://epic-minigames.fandom.com/wiki/Team, https://epic-minigames.fandom.com/wiki/Solo_Winner, https://epic-minigames.fandom.com/wiki/1_vs._Everyone — win types and map variants (community wiki, read via API 2026-10-25)
3. https://epic-minigames.fandom.com/wiki/Minigames and https://epic-minigames.fandom.com/wiki/Treacherous_Tiles — minigame list, one-minute survival rule
4. https://epic-minigames.fandom.com/wiki/The_Lobby and https://epic-minigames.fandom.com/wiki/Shop — lobby for the eliminated, coin shop
5. https://rowatcher.com/games/7008097940 — Ink Game peak ~514K on 2025-09-21 (third-party, unverified; from search summary)
6. https://create.roblox.com/docs/production/promotion/content-maturity — free-form creation (painting, pixel grids) 16+
7. https://devforum.roblox.com/t/modular-round-system/3670738 — base round module with per-mode modules (community discussion)

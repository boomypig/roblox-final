---
title: +1 stat games (and keyboard escapes)
type: genre
read-when: Building a "+1 speed/stat every step, second, click or kill" game, a keyboard/speed escape course, or judging the 2026 "+1 ___" wave.
last-researched: 2026-10-24
---

# +1 stat games (and keyboard escapes)

## In one line

Every step, second, click or kill adds +1 (times your multipliers) to one stat, and that stat is
the key that opens the next stage, enemy or zone. You can lose your position but never the
stat, so a failed run still made you stronger. It is a [simulator](simulator.md) with the
upgrade shop removed: the stat ticks up as you play, and the shop sells multipliers on it.

Related: cost curves and the "Verb a Noun" wave are in [idle-incremental](idle-incremental.md);
the rebirth math is in [rebirth-prestige](../patterns/rebirth-prestige.md); multiplier shops
are in [upgrade-trees](../patterns/upgrade-trees.md); escape obbies without a stat are in
[obby-escape](obby-escape.md).

## Core loop

- **Moment to moment (1 s):** move, click, swing or shoot. A "+1" pops and the stat counter
  ticks. In escape variants the character visibly gets faster.
- **Run (30 s – 5 min):** push into the course, arena or zone until the stat isn't enough
  (you fall, die or stop short). Bank the second currency at the furthest gate you reached,
  then go back to spawn with a bigger stat and try again.
- **Session (15–30 min):** spend the second currency (usually called Wins) on multipliers:
  trails, auras, pets, weapons. Stand on a treadmill to train while idle. Rebirth when the
  button appears.
- **Long term:** rebirth multipliers, later stages and worlds, pet or weapon tiers, the
  server leaderboard.

**The stat gates the zones.** In +1 Speed Keyboard Escape the course has 13 stages. Wins come
only from yellow pads in the safe zone after a stage, and stepping on one banks the Wins and
sends you back to spawn (community, allthings.how 2026-06-18). The run always ends in a
reset, so the next run has to be faster to get further (inferred).

**Variants in the 2026 wave** (data, 2026-10-22; loop details are from each game's own
description):

| What adds +1 | What the stat beats | Example (players) | Extra layer |
|---|---|---|---|
| Each step (Speed) | Obstacle course stages | +1 Speed Keyboard Escape 50.3K; +1 Speed Monkey Escape 4.2K | Trails, treadmills, rebirth |
| Each click (Strength) | Enemies, stages | +1 Assassin Leveling 9.0K; +1 Venom Evolution 18.4K | Daggers or evolutions, pets, Wins |
| Each bounce (Skill) | Distance zones | +1 Stone Skipping 13.1K | Thrown objects, pets, rebirth |
| Each swing | Blocks between areas | +1 Pickaxe Swing for Eggs 6.8K | Eggs, animals earning offline cash, base |
| Each shot / click | Zombies, bosses | +1 Gun Forge 4.1K; +1 Loot To Forge 9.9K | Forge 53 guns from Common to Mythic; ores, gear |
| Each kill (gear step) | Other players (PvP) | +1 Upgrade Per Kill 2.9K, 62% likes | Death resets gear to zero; 8 classes |
| Each revive | Monsters on a "death road" | +1 DMG Per Revive 1.4K | Death works as the power-up |

## Main verbs

Move, click or swing (the +1 verb), fail, bank (Wins pad, kill, distance), buy a multiplier,
train (treadmill), rebirth, hatch (pets, in most 2026 entries), race.

## Why players come back

- **No-loss failure.** Falling costs your position, never your stat. Every attempt pays out,
  which removes the frustration that drives players out of hard [obbies](obby-classic.md)
  (inferred).
- **The stat is always moving.** The number goes up every second you play, even while you're
  stuck. There's never a dead minute (inferred).
- **Readable in one second.** The title is the tutorial: "+1 Speed", "SHOOT = +1 POWER"
  (data, descriptions 2026-10-22). Players know the verb before they spawn (inferred).
- **Power fantasy you can see.** In escape variants the avatar goes from walking pace to a
  blur, and the gap you couldn't cross 5 minutes ago becomes trivial (inferred).
- **Idle training.** Treadmills keep the stat rising while the player watches or chats.
  Keyboard Escape's free treadmill gives x1; the paid Diamond and Admin treadmills give x9
  and x100 (community, allthings.how 2026-06-18).
- **High ratings.** Most charted +1 games sit at 96–99% likes, Keyboard Escape at 97% (data,
  2026-10-22). Players rate a gentle loop with no fail punishment highly (inferred).

## What separates top games from clones

1. **A course that is fun at every speed.** The leader's world is themed keyboard keys with
   click sounds and an "ASMR" pitch (data, description 2026-10-22). The stat changes how the
   same map feels, so 13 stages last for hours (inferred).
2. **The verb is the spin.** The wave keeps the +1 → gate → Wins → multiplier → rebirth
   skeleton and swaps the verb (venom, stone skipping, pickaxe, gun forge). That is spin type 2
   in [trend-lifecycle](../fundamentals/trend-lifecycle.md) (inferred).
3. **A second loop by minute 10.** The bigger 2026 entries add pets or eggs, a weapon ladder
   or an offline-earning base on top of the stat (data, descriptions 2026-10-22). A bare stat
   and course is the clone baseline (inferred).
4. **Constant name tags.** The leader's name label has rotated through [S15], [X6], [X7],
   [X15], [X20], [X50], [X100], [G2], [1HR] and emoji tags (community, RoWatcher page slugs,
   2026). It read [X50] on 2026-10-22 and [🎵] on 2026-10-24 (data). The "X" tags look like
   timed multiplier events (inferred, unverified).
5. **Large servers for racing.** Keyboard Escape and Monkey Escape both run 22 per server.
   Fight and tycoon variants run 5–16 (data, 2026-10-22). On a course, other players are
   people to race. In a fight or tycoon variant they compete for the same space (inferred).

## Session shape

Targets are (inferred) from the loop timing above; no official session data exists for the
genre.

- **First 10 seconds:** the stat ticks from the first step, with a "+1" pop above the head.
  No menu before movement.
- **First 60 seconds:** stage 1 cleared, first Wins banked, the next stage visibly harder.
- **First 10 minutes:** first multiplier bought (Keyboard Escape's Green Trail costs 500 Wins
  for x1.5; community, allthings.how 2026-06-18), treadmill found, rebirth requirement on screen.
- **Session:** 15–30 minutes, ending on a rebirth, a new stage or an idle kick on the treadmill.
- **Day 7:** several rebirths, top-tier free multiplier, chasing the last stage or world 2.

## Social hooks

- **Racing on one course.** "Race against friends" and "become the FASTEST on the server"
  are the leader's social pitch (data, description 2026-10-22).
- **Friend boosts.** +1 Assassin Leveling gives +10% Strength per friend in the server (data,
  description 2026-10-22).
- **Visible stat.** Overhead stat and a server leaderboard by stat or rebirths
  ([leaderboards](../patterns/leaderboards.md)).
- **Group and like rewards.** Keyboard Escape gives 15,000 Speed for liking and joining the
  group, plus 15,000 for a one-time social code from its Discord (press, PocketGamer
  2026-10-24). No engine API tells you whether a player liked the game, so a like reward runs
  on trust. Group membership can be checked with `Player:IsInGroupAsync` (official).
- See [social-and-virality](../fundamentals/social-and-virality.md).

## Monetization that works here

Sell multipliers on the +1 and shortcuts past gates. Never sell the stat itself as the only
route.

- **Multiplier trails.** Keyboard Escape: Green x1.5 (500 Wins or 19 R$), Blue x2 (1,500 Wins
  or 29 R$), Purple x3 (5,000 Wins or 59 R$), Red x4 (25,000 Wins or 139 R$), Rainbow x5
  (100,000 Wins or 249 R$), Robux-only Galaxy x10 (399 R$) and Choco x20 (499 R$) (community,
  allthings.how 2026-06-18; unverified). Each tier can be earned or bought, and only the top
  two are Robux-only.
- **Stage teleports.** 2 Wins or 3 R$ for stage 2, rising to 20,000 Wins or 99 R$ for stage 13
  (community, allthings.how 2026-06-18; unverified). That's a cheap impulse product at every
  gate.
- **Treadmill tiers** (x9, x100) as passes or products: idle speed with no fail risk
  (community, 2026-06-18).
- **Timed boosts** (x2 for 15 minutes) and auto-click for click variants. See
  [monetization](../fundamentals/monetization.md) for pass versus product rules.
- **Pets and eggs** where the variant has them: odds disclosure and `PolicyService` checks
  apply ([rarity-tiers-and-eggs](../patterns/rarity-tiers-and-eggs.md)).

## Common failure modes

- **Format exhaustion.** Early entries kept their visits but lost their players:
  +1 Health Per Click has 62.6M visits and 110 players, +1 Speed Wings Escape 60.2M visits
  and 70 players (data, 2026-10-22). The leader was down 44.9% over 30 days to 2026-10-24,
  with a 30-day average of 114K against an all-time peak of 7.3M on 2026-07-18 (community,
  RoWatcher fetched 2026-10-24; unverified).
- **Clone-on-clone naming.** RoWatcher lists many "+1 Speed ___ Keyboard Escape" titles
  (Slime, Ninja, Backflip, Honey, Hug) (community, 2026). Roblox deprioritizes games whose
  title and visuals closely match an existing game (official, discovery docs).
- **Physics breaks at high speed.** If the stat maps straight to `Humanoid.WalkSpeed`
  (default 16; official), late-game characters overshoot platforms, clip through thin parts
  and make phones stutter (inferred). Map the stat through a curve with a cap.
- **Punishing loss mechanics.** +1 Upgrade Per Kill resets gear to zero on death and sits
  at 62% likes, the lowest in the theme (data, 2026-10-22). The genre's appeal is that you
  never lose the stat, so a mode where you do loses it too (inferred).
- **Dead time between gates.** If the next gate needs 10× the current stat with no new
  multiplier available, the run becomes treadmill-waiting (inferred).
- **AFK promises.** `Player.Idled` fires after about 2 minutes, and Roblox disconnects
  idle players after 20 (official). Treadmill time ends at the idle kick. Don't fight it; add
  offline income instead ([idle-offline-income](../patterns/idle-offline-income.md)).
- **Client-trusted steps.** The client owns its character's physics, so steps or distance
  counted on the client (or a client-set WalkSpeed) are free to exploit
  ([security](../fundamentals/security-and-anti-exploit.md)).

## Saturation & opportunity

One tracker snapshot (data, 2026-10-22) unless noted.

| Theme | Games | Players | Median | Leader (share) | Label |
|---|---|---|---|---|---|
| `plus-one` | 15 | 124K | 4.1K | +1 Speed Keyboard Escape (41%) | mixed |
| `speed` | 6 | 57K | 913 | Keyboard Escape (88%) | – |
| `keyboard` | 2 | 63K | 32K | Keyboard Escape (79%) | – |

- **Still being joined.** Five rising +1 games were created between 2026-09-18 and 2026-10-05:
  Venom Evolution, Assassin Leveling, Pickaxe Swing for Eggs, Gun Forge, Upgrade Per Kill.
  Venom Evolution, 17 days old, sits at up-and-coming #12 and trending-in-simulation #19.
  Live it had 24.8K players on 2026-10-24 (data, games API).
- **The escape sub-format is consolidated.** Speed-escape titles other than the leader total
  under 4.3K players (data, 2026-10-22). Keyboard Escape had 96.9K on Saturday 2026-10-24 (data,
  games API), but it is down 45% over 30 days (community, unverified). Third-party trackers
  show it at global #1 in early July 2026 (community, Bloxodes; unverified).
- **Where the wave moved:** combat and collection verbs (strength, venom, guns, pickaxes) with
  pets and Wins, not more escape courses (inferred from the rising list).
- **Read (inferred):** stage 3–4 of a wave ([trend-lifecycle](../fundamentals/trend-lifecycle.md)).
  A reskinned keyboard course is late. A fresh verb on the +1 skeleton is still viable as a
  short bet (≤ 3 weeks). The strongest entry would join the +1 spine to a second proven loop,
  the way Steal An Egg (case study: steal-an-egg) trains Speed on a treadmill to gate
  its biomes.

## Scope for a solo dev

The cheapest genre in the vault: one stat, one map, no AI. Week counts are (inferred) for one
developer with Rojo and Studio MCP playtests.

**MVP:** one +1 verb, one stat, 8–10 gates (stages or enemy tiers), Wins pads, 5 multiplier
items (trails or pets) buyable with Wins, 1 free treadmill, 1 rebirth tier, server
leaderboard, saving, 1 pass (2x stat), stage-teleport products, one timed boost.

| Week | Build |
|---|---|
| 1 | Server stat tick (step distance or click) with caps; stat → WalkSpeed/damage curve; save ([player-data](../patterns/player-data.md)); number pops and overhead stat |
| 2 | Course of 8–10 stages from reusable modules ([checkpoints-and-respawn](../patterns/checkpoints-and-respawn.md)); Wins pads; trail shop; treadmill; rebirth |
| 3 | Passes and products (`ProcessReceipt`), tuning simulation, FOV/feel pass, mobile UI, icon and thumbnail, launch |
| 4+ | Weekly: 2–3 new stages or a world, one new multiplier tier, a timed x2 event |

**Cut from v1:** pets and eggs (add in update 1), world 2, PvP, codes beyond one launch
code, custom character models.

## Top examples

- +1 Speed Keyboard Escape (case study: plus-one-speed-keyboard-escape): the format
  leader; 6.54B visits in 277 days (data, 2026-10-22).
- +1 Venom Evolution (no case study): the fastest-rising 2026 entry; click-train and fight
  stages for Wins and evolutions (data, 2026-10-22).
- +1 Stone Skipping (no case study): a distance variant; each bounce is +1, farther zones pay
  more Wins; top-earning #50 (data, 2026-10-22).
- Steal An Egg (case study: steal-an-egg): uses a treadmill-trained Speed stat as the
  gate inside a bigger loop.

## Build checklist for agents

### Do

- Count the +1 on the server. For steps, sample the `HumanoidRootPart` position each
  `RunService.Heartbeat`, count horizontal distance only, and cap the distance per tick at
  about `WalkSpeed × dt × 1.25` so teleports don't count (inferred).
- Gain per action = 1 × trail × pet × rebirth × boost. Show the full product on the HUD
  ("+1 ×12 = +12").
- Map stat to movement with a curve, e.g. `WalkSpeed = math.min(16 + 4 * math.log10(1 + stat) ^ 2, cap)`.
  Pick `cap` (around 150–300) by playtesting the last stage on a phone (inferred).
- Raise `Camera.FieldOfView` from 70 (default; official) toward about 90 as speed rises, on
  the client only (inferred; see [game-feel](../fundamentals/game-feel.md)).
- Make the gate requirement grow about ×3–×10 per stage. Time to the next gate should start at
  about 30 s and grow to about 5–10 minutes before rebirth (inferred). The leader's teleport
  costs grow ×1.5–×4 per stage (community, 2026-06-18).
- Send the player to spawn after banking Wins, and offer a teleport (Wins or Robux) to the
  furthest stage reached.
- Keep the stat on failure. Respawn at the last safe zone with no stat loss.
- Keep trails, pets and passes through rebirth. Reset only the stat and Wins
  ([rebirth-prestige](../patterns/rebirth-prestige.md)).
- Let every multiplier tier except the top one or two be earnable with Wins.
- Format the stat with suffixes (K, M, B, T…) and store it as a number, not an `IntValue`.
- Simulate 2 hours of play in a headless Luau script before launch and report time to each
  gate and the first rebirth ([idle-incremental](idle-incremental.md)).
- Run 12–24 players per server for course variants, and 6–12 for fight or tycoon variants.

### Don't

- Don't let the client send step counts, distance, click totals or a WalkSpeed value.
- Don't map the raw stat straight to `WalkSpeed` or `JumpPower`.
- Don't take the stat away on death or failure as the core rule.
- Don't build a keyboard or candy course, or use a "+1 Speed ___ Keyboard Escape" title. That
  copies the leader's title and visuals, which is what discovery deprioritizes (official).
- Don't make the "x100" treadmill or Robux trails the only route to the last stage.
- Don't bypass the 20-minute idle kick, and don't advertise overnight AFK training.
- Don't ship without a second loop planned for update 1. The bare format is exhausted.

## Sources

1. private/trends/latest.md and tools/trends lookups — themes, players, visits, likes, creation dates, server sizes, descriptions (data, 2026-10-22); games API recheck 2026-10-24
2. https://www.roblox.com/games/95082159892680 — +1 Speed Keyboard Escape page: "Every step = +1 Speed", keyboard-key world, races, ASMR pitch
3. https://allthings.how/1-speed-keyboard-escape-how-to-build-speed-farm-wins-and-rebirth/ — 13 stages, Wins pads, teleport and trail prices, treadmill multipliers (2026-06-18)
4. https://www.pocketgamer.com/roblox/1-speed-keyboard-escape-codes/ — social code and like/group rewards, treadmills (2026-10-24)
5. https://rowatcher.com/games/9584852943/x20-1-speed-keyboard-escape-candy-chocolate/dying — 7.3M peak 2026-07-18, 30-day −44.9%, averages (third-party tracker)
6. https://bloxodes.com/stats/games/1-speed-keyboard-escape-candy-chocolate-9584852943 — best global rank #1 in early July 2026 (third-party tracker)
7. https://rowatcher.com/games/10127090395/w3-1-speed-slime-keyboard-escape — example of the keyboard-escape clone titles
8. https://www.roblox.com/games/116448925875915 — +1 Venom Evolution description
9. https://www.roblox.com/games/120731410233153 — +1 Assassin Leveling: +1 Strength per click, +10% per friend
10. https://www.roblox.com/games/111543903102439 — +1 Stone Skipping: +1 per bounce, distance zones
11. https://www.roblox.com/games/113273588963037 — +1 Upgrade Per Kill: death resets gear
12. https://create.roblox.com/docs/reference/engine/classes/Humanoid — WalkSpeed default 16, JumpPower
13. https://create.roblox.com/docs/reference/engine/classes/Player — Idled event, 20-minute idle disconnect, IsInGroup
14. https://create.roblox.com/docs/reference/engine/classes/Camera — FieldOfView default 70
15. https://create.roblox.com/docs/discovery — similar title and visuals deprioritized

---
title: Racing and driving
type: genre
read-when: Building a racing or driving game (track racing, open-world driving, drift, wheelie, co-op rally).
last-researched: 2026-10-22
---

# Racing and driving

## In one line

Sell the feel of one vehicle and one trick that pays. On Roblox most players are in open-world
and novelty driving sims (wheelies, drifting, co-op rally, mudding), not in lap racing (data,
2026-10-22).

## Core loop

- **Moment to moment:** steer, throttle, brake or handbrake, boost, and hold the trick that pays:
  drift angle, wheelie balance, a near miss in traffic, staying on the road blind (inferred).
- **Session:** drive, earn cash per distance, trick or race, then buy or tune a vehicle, then
  try a harder map or race. Bike Universe pays for riding, wheelies and tricks, then sells new
  bikes and tuning (official game description, 2026-10).
- **Long term:** a garage to collect (Driving Empire lists 300+ cars and boats), customization
  (rims, tires, smoke color, bodykits), limited vehicles, leaderboard times, car meets (official
  game descriptions, 2026-10).

## Main verbs

| Format | Verbs | Example (data, 2026-10-22) |
|---|---|---|
| Open-world driving and RP | cruise, race friends, customize, show off at meets | Driving Empire 18.9K, Kukirin Life 16.6K |
| Trick for cash | wheelie, stunt, drift; tune the trick | Bike Universe 34.5K, How To Drift 2.4K |
| Traffic cutting | weave through highway traffic at speed | Ghost Driver 8.9K, Midnight Chasers 2.0K |
| Off-road | mud runs, towing, hauling | Southern Mudding 10.7K, American Plains Mudding 8.9K |
| Co-op rally | the driver can't see the road; a partner calls the turns | Backseat Rally 21.3K, Rally Panic! 5.1K |
| Survival road trip | drive, scavenge, repair | a dusty trip 6.2K (2.6B visits) |
| Destruction | crush, derby | Car Crushers 2 1.4K |
| Track racing | qualify, race laps, beat a time | Formula Apex Racing 531 |

## Why players come back

1. **The next vehicle.** A garage is a collection. Bike Universe sorts its bikes into dirt,
   electric and pedal classes (official game description, 2026-10).
2. **Skill that pays.** Drifting or wheelies earn currency, so practice is progress (official
   game descriptions, 2026-10). Drag Drive Simulator added five wheelie styles with tunable speed
   and angle as a headline update (official game description, 2026-10).
3. **Rotating content.** How To Drift added races that rotate weekly "to come back" for
   (official game description, 2026-10-20).
4. **Friends.** Car meets, roleplay servers, and two-role co-op (driver and navigator).
5. **Limited vehicles.** Ghost Driver and Drag Drive Simulator headline limited cars (data:
   game names, 2026-10-22).

## What separates top games from clones

### Car feel: the constraint chassis

Start from Roblox's racing template car. It's a dune buggy tuned through attributes, and checkpoints
are named Checkpoint1…N in a Race folder with min/max players and laps (official, 2024-01). For
competitive racing, use the Racing-Server-Authority-Template instead (official, 2026-07). If you
build your own:

| Part | Setup (property names official; values inferred starting points) |
|---|---|
| Input | Read `VehicleSeat.ThrottleFloat` and `SteerFloat` (−1…1). `Throttle`/`Steer` are deprecated (official). `VehicleSeat` alone can drive motor hinges it detects (`AreHingesDetected`), but `MaxSpeed`/`Torque`/`TurnSpeed` give little control |
| Chassis | One invisible root box carries the mass. Set `Massless = true` on every cosmetic part so the centre of mass stays low. Most flips come from a high centre of mass (inferred) |
| Drive wheel | `CylindricalConstraint`: `AngularActuatorType = Motor`, `AngularVelocity = ThrottleFloat × topSpeed / wheelRadius`, `MotorMaxTorque` tuned to the car's mass |
| Suspension | Same constraint: `LimitsEnabled = true`, `LowerLimit`/`UpperLimit` about ±0.5–1 stud of travel, plus a `SpringConstraint` (`Stiffness`, `Damping`, `FreeLength`). Too little damping makes the car bounce; too much makes it skip (inferred) |
| Steering | A knuckle part on a `HingeConstraint` with `ActuatorType = Servo`, `TargetAngle = SteerFloat × 30–35°`, high `ServoMaxTorque`, `AngularSpeed` ~ 3–6 rad/s. Reduce the angle at high speed |
| Grip and drift | Per-wheel `CustomPhysicalProperties` friction. On handbrake, lower rear friction and add a little yaw. Arcade drift is a scripted assist, not emergent physics (inferred) |

- Hinge-only cars are the old pattern. Experienced devs point to cylindrical-constraint suspension
  as the more realistic build (community, 2020).
- Arcade alternative: one body, four downward raycasts per physics step, and spring forces at
  each corner. It's easier to tune and stable on bumps, but every behaviour is your code
  (inferred).
- Resizing a chassis means retuning forces and limits (community, 2018).
- The racing template had a known fling with the aerodynamics beta on (official, 2024-01). Test
  with every beta you ship with.

### Network ownership

- The driver's client simulates the car. If a passenger sits first, they own the whole car and
  the driver's inputs lag. The docs' fix: on `VehicleSeat.Occupant` change, call
  `SetNetworkOwner(player)` for the driver and `SetNetworkOwnershipAuto()` when the seat empties.
  Give loose parts on the car to the same client (official, 2026-10).
- A client that owns the car can teleport or speed it up, and can fire `Touched` on checkpoints it
  owns (official, 2026-10). Lap-time checks must read server-side positions (below).
- Server Authority (`Workspace.AuthorityMode = Server`) is Roblox's answer for fair vehicles: the
  server simulates, and clients predict and roll back (official, 2026-07). See
  [security](../../.claude/skills/roblox-code/references/security.md). Casual cruising games can skip it
  (inferred; Roblox notes many popular games stay client-authoritative, official 2026-07).

### Lap times and anti-cheat

- The server tracks each racer's checkpoints in order, from the car's server-side position at
  ~10 Hz: distance to a gate plane or `Workspace:GetPartBoundsInBox`. Don't use client `Touched`
  (official principle; method inferred).
- The server starts and stops the timer with `workspace:GetServerTimeNow()`. Never accept a time
  from the client (official principle).
- Plausibility checks: sector time ≥ sector length ÷ (top speed × 1.1), and per-sample displacement
  ≤ top speed × dt × 1.2 + a few studs. Reset the baseline after respawns and boost pads
  (community pattern; numbers inferred).
- Validate the outcome: a completion time beats catching each cheat method (community, 2025).
- Store top times in an `OrderedDataStore` ([leaderboards](../patterns/leaderboards.md)). For the
  top 100 per track, keep a 10 Hz position trace so suspicious records can be reviewed, and flag
  rather than auto-ban (inferred).

### Camera, sound, feedback

- FOV from 70 to ~85 with speed, light shake near top speed, speed-line particles at boost, off
  under `GuiService.ReducedMotionEnabled` ([game feel](../../.claude/skills/roblox-vfx/references/game-feel.md)) (inferred).
- Engine `Sound.PlaybackSpeed` mapped from ~0.8 to 1.6 by speed or RPM, a tire screech plus `Trail`
  skid marks when sideways slip passes a threshold, and a thump on landing (inferred).
- Give drift or wheelie score a live counter and a combo multiplier. Bank it on a clean finish and
  lose it on a crash (inferred).

### Mobile controls

- Put a gas and a brake/reverse button on the right, steering on the left (stick or two arrow
  buttons), and one more button for handbrake or boost. That's 3–4 targets of ≥ 56 px
  ([ui-ux](../../.claude/skills/roblox-ui/references/ui-ux.md)) (inferred).
- Build them with `InputAction` and write into your own throttle and steer values, so keyboard,
  gamepad triggers and touch share one path (official system; use inferred).
- The camera should auto-follow behind the car on touch. Players can't steer and orbit the camera
  at once (inferred).

## Session shape

- **First 60 s:** in a vehicle and moving within 20 s. Teach the trick with one prompt ("hold
  Space to drift") and pay out the first cash within a minute (inferred).
- **First 10 min:** first upgrade or second vehicle, first time on a leaderboard (inferred).
- **Day 7:** chasing one named vehicle or a top-100 time. Weekly rotating races give a reason to
  return (official How To Drift description, 2026-10-20).

## Social hooks

- **Two-role co-op:** in Backseat Rally a friend sees the road and the driver doesn't. Solo
  players get an AI co-driver using a friend's avatar (official game description, 2026-10). In
  Rally Panic! the navigator holds the map in first person (official game description, 2026-10).
  These are "fun with friends" formats with a clip-worthy failure built in (inferred).
- **Car meets and showcases:** Driving Empire and Midnight Chasers both advertise meetups
  (official game descriptions, 2026-10).
- **Custom and private servers:** Driving Empire shipped custom servers in beta on 2026-10-16
  (official game description). See [private servers](../patterns/private-servers.md).
- **Replays:** How To Drift sells a Replays pass for recording runs (official game description,
  2026-10). Recordings are free marketing on video platforms (inferred).

## Monetization that works here

- **Vehicles:** Robux-only or limited cars. Ghost Driver and Drag Drive Simulator headline limited
  vehicles (data: game names, 2026-10-22).
- **Cash multipliers:** Midnight Chasers gives a 50% cash boost with a VIP pass and 25% for joining
  its group (official game description, 2026-10).
- **Customization:** tires, rims, smoke color, bodykits (Southern Mudding's 2026-10-16 update; Junk
  Mechanics) (official game descriptions, 2026-10).
- **Convenience passes:** replays, garage slots, a favourite-vehicle spawner (official game
  descriptions, 2026-10).
- Don't sell top speed in a ranked race. Sell it in open-world or trick games (inferred).
- Details in [monetization](../fundamentals/monetization.md).

## Common failure modes

- Cars that flip, fling or bounce: high centre of mass, mass in cosmetic parts, undamped springs
  (inferred).
- Driver input lag from a passenger owning the car (official, 2026-10).
- Track races with empty lobbies. A race needs 2+ players, so ship time trials and ghosts first
  (inferred).
- Leaderboards full of impossible times from client-owned cars (official threat model).
- Big open maps that stall phones. Fast cars outrun streaming, so tune `StreamingTargetRadius` and
  keep vehicle models light ([performance](../../.claude/skills/roblox-map/references/performance-and-devices.md)) (inferred).
- **Real brands without a licence.** Driving Empire's Lamborghini, McLaren and Porsche are licensed
  (official game description, 2026-10). Many small games use real names with a "trademarks are
  property of their owners" disclaimer. That disclaimer doesn't grant rights. The Kukirin
  e-scooter wave uses a real scooter brand's name (community guides, 2026-09; inferred risk).

## Saturation & opportunity

Single snapshot, so no growth claims.

- Vehicle Sim subgenre: 53 games, 145K players (2.1% share). The Racing subgenre is only 7 games
  and 10K. Most of the 272K in Sports & Racing is sports (data, 2026-10-22).
- `racing-cars` theme: 22 games, 62K, 2.8K per game, median 1.7K. Driving Empire holds 30%, so it's
  mixed (data, 2026-10-22). Its three rising games are Wash the Car, Catastrophic Horse Racing and
  How To Drift (data, 2026-10-22).
- Breakouts: Bike Universe 34.5K at 25 days (top-trending #11, up-and-coming #2) and Backseat Rally
  21.3K at 17 days (top-trending #8, up-and-coming #4) (data, 2026-10-22). Backseat Rally peaked at
  28K in 2026-10 (community: RoWatcher).
- **Unlabeled waves the tracker misses** (inferred from data, 2026-10-22):
  - Two-player rally: Backseat Rally, Rally Panic! (5.1K) and WRONG WAY! (1.9K), all created
    2026-10-01 → 10-05.
  - E-scooters: Kukirin Life 16.6K, Escooter Life 3.9K, Drive A Kukirin 1.9K, Wheelie a Kukirin
    0.7K.
  - Bike Universe and Backseat Rally carry no tracker theme, and Backseat Rally has no Roblox genre
    set.
- Long-runners prove depth retains: Driving Empire (2019) 18.9K, American Plains Mudding (2021)
  8.9K (data, 2026-10-22).
- Opening (inferred): one trick, done with great feel, plus a co-op or rotating-race hook. Avoid
  competing on car count with Driving Empire.

## Scope for a solo dev

**MVP:** one vehicle class, one compact map (a track or a small loop with jumps), one trick that
pays, 4–6 vehicles with 3 upgrade stats, a time trial with a server-validated leaderboard. Two-
player co-op or races come second.

| Week | Build |
|---|---|
| 1 | Chassis from the racing template. Tune feel on PC and a real phone, and at 200 ms latency |
| 2 | Trick scoring (drift angle × speed, or wheelie seconds), combo UI, sound and camera |
| 3 | Map blockout with streaming, checkpoints, server timer, leaderboard |
| 4 | Garage, upgrades, shop, saving ([player data](../patterns/player-data.md)) |
| 5 | Mobile controls, FTE, anti-cheat checks, polish |
| 6 | Playtest; add co-op or head-to-head races only if lobbies fill |

- **Physics tuning is the main cost.** Expect days of iteration on springs, friction and torque.
  Lock the feel before making content (inferred).
- **Vehicle models without an artist:** stylized part-built or low-poly cars, or Creator Store
  models. Check their licence and strip any scripts (inferred).
- **Cut:** realistic sim handling, damage models, traffic AI, 50+ cars, large open worlds,
  licensed brands, AI opponents. Use ghost replays of top times instead of AI.

## Top examples

- Driving Empire: open-world driving and RP with 300+ licensed cars; 18.9K (data, 2026-10-22).
- Bike Universe: ride, wheelie and trick for cash, collect bike classes; 34.5K at 25 days (data,
  2026-10-22).
- Backseat Rally: blind driver plus a navigator who sees the road; 7 cars, 5 stages; 21.3K at 17
  days (data, 2026-10-22).
- How To Drift: drift for cash, 7 maps, weekly rotating races, replay pass; 2.4K (data,
  2026-10-22).
- Southern Mudding: off-road trucks with deep tire customization; 10.7K (data, 2026-10-22).
- a dusty trip: survival road trip; 6.2K and 2.6B visits (data, 2026-10-22).

## Build checklist for agents

### Do

- Start from the Roblox racing template or a documented constraint chassis. Put mass in one root
  part, make cosmetic parts `Massless`, and keep the centre of mass low.
- Read `ThrottleFloat`/`SteerFloat`, not deprecated `Throttle`/`Steer`.
- On `VehicleSeat.Occupant` change, `SetNetworkOwner(driver)`; when empty,
  `SetNetworkOwnershipAuto()`.
- Run checkpoints, timers and lap validation on the server from server-side positions and
  `workspace:GetServerTimeNow()`.
- Reject lap or sector times faster than physically possible, and reset baselines after respawns
  and boosts.
- Use `AuthorityMode = Server` (or the Server Authority racing template) for ranked or competitive
  racing.
- Give every vehicle speed feedback: FOV, engine pitch, skid sound and marks.
- Add mobile gas, brake and steer buttons with `InputAction`; test on a real phone.
- Ship a time trial with a global leaderboard before multiplayer races.

### Don't

- Don't accept lap times, speeds or checkpoint hits from the client.
- Don't put mass in cosmetic body parts or tall bodies on narrow wheelbases.
- Don't rely on `VehicleSeat.MaxSpeed`/`Torque` alone for a game whose selling point is feel.
- Don't use real car or scooter brand names, logos or models without a licence.
- Don't build a large open world before the vehicle feels good on a small test map.
- Don't sell raw speed in competitive modes.

## Sources

1. https://create.roblox.com/docs/reference/engine/classes/VehicleSeat — ThrottleFloat/SteerFloat, deprecated Throttle/Steer, AreHingesDetected
2. https://create.roblox.com/docs/reference/engine/classes/CylindricalConstraint — AngularActuatorType, AngularVelocity, MotorMaxTorque, InclinationAngle
3. https://create.roblox.com/docs/reference/engine/classes/SlidingBallConstraint — LimitsEnabled, LowerLimit, UpperLimit (inherited by CylindricalConstraint)
4. https://create.roblox.com/docs/reference/engine/classes/HingeConstraint — ActuatorType, TargetAngle, AngularSpeed, ServoMaxTorque
5. https://create.roblox.com/docs/physics/network-ownership — passenger ownership bug, Occupant fix, SetNetworkOwnershipAuto, Touched spoofing
6. https://devforum.roblox.com/t/new-studio-racing-template/2805745 — racing template: dune buggy via attributes, checkpoint naming, aerodynamics fling (2024-01-23)
7. https://devforum.roblox.com/t/full-release-ship-fair-and-competitive-games-with-server-authority/4727993 — Racing-Server-Authority-Template, vehicles (2026-07-09)
8. https://create.roblox.com/docs/projects/server-authority — prediction and rollback model
9. https://devforum.roblox.com/t/how-to-make-a-simple-car/783456 — hinge cars dated; cylindrical-constraint suspension series recommended
10. https://devforum.roblox.com/t/constraint-chassis/221717 — open-source constraint chassis; retune when resized
11. https://devforum.roblox.com/t/good-anti-cheat-for-an-obby/3576031 — validate completion times, Touched delay (2025)
12. https://devforum.roblox.com/t/roblox-anticheats/2952846 — displacement-over-time speed check and its false positives
13. https://rowatcher.com/games/10769543742/backseat-rally — Backseat Rally peak 28K (2026-10)
14. https://allthings.how/drive-a-kukirin-guide-how-to-earn-cash-fast-and-use-every-control/ — Kukirin game uses real scooter models; wheelie payouts (2026-09)
15. Roblox game descriptions read via the tracker (2026-10-22): Bike Universe, Backseat Rally, How To Drift, Driving Empire, Rally Panic!, Midnight Chasers, Ghost Driver, Drag Drive Simulator, Southern Mudding
16. private/trends/latest.md and tools/trends lookups — all (data, 2026-10-22) numbers

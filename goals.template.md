# Goals and constraints for game pitches

Copy this file to `private/goals.md` (create the `private/` folder if it is missing) and fill
it in. `/pitch` judges every idea against it, and
section 1 of `create-roblox-game` judges every design call against it. `private/` is ignored by
git, so what you write stays on your machine.

Lines marked **Assumption:** are defaults the toolkit uses until you replace them. Every `TBD`
you leave is reported as an assumption in each pitch, because it changes the scores.

## Who's building
- TBD: solo or a team; what each person is good at.
- TBD: is there an artist, modeler, animator or composer? **Assumption:** none. Visuals come
  from Studio parts and materials, lighting, free Creator Store assets, and the toolkit's
  generated meshes, textures, animation, VFX and sound. Each generated asset costs sessions.
- Workflow: `/pitch` → `tools/new_game.py` → `create-roblox-game`, one section per session
  (docs/workflow.md).

## What success means right now
- TBD: learning, a small polished release, or a commercial target.
- **Assumption:** a "win" is a published game with real players and measurable D1/D7
  retention, not a top-chart hit. TBD: concrete targets (CCU, D1 %).

## Lessons from earlier games
- TBD: what worked, what felt flat, and what to do differently. Add to this after every game:
  it is the part of this file that improves the next pitch most.

## Constraints
- Time: TBD weeks to a public launch; TBD hours per week.
- Scope: **Assumption:** one core loop done well beats many systems; prefer content that can
  be made with parts and code.
- Platform: **Assumption:** phone first, since most Roblox players are on mobile
  (vault/fundamentals/audience.md).
- Ad budget: TBD (Robux for sponsored ads, if any).
- Audience gate: a new game reaches only age-checked 16+ players unless the creator meets the
  all-ages requirements (vault/fundamentals/discovery-algorithm.md, "audience gating"). TBD:
  will you meet them for launch, or launch 16+ only? This decides the reachable audience.
- Team: TBD: open to a collaborator?

## Values
- Server-authoritative design: never trust the client for progress, rewards or purchases.
- **Assumption:** fair monetization for a young audience: no pay-to-win in competitive modes,
  no paid random items aimed at kids, cosmetics and convenience first.
- Add an original spin; no straight clones (discovery also deprioritizes near-copies).

## Preferences
- TBD: genres you enjoy playing and would enjoy building for months; genres you won't touch.
- TBD: target age range.
- TBD: join a current trend wave, or evergreen genres only?

## Out of scope for pitches
- **Assumption:** anything that needs a team, a custom 3D art pipeline, or heavy live-ops from
  day one.
- TBD

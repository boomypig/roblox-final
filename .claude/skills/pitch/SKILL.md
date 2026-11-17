---
name: pitch
description: Write 5 scored Roblox game pitches from your goals file, the vault, and the latest trends report
argument-hint: "[constraints, e.g. solo dev, 4 weeks, obby-adjacent]"
---

Write five game pitches for the user into `private/pitches/YYYY-MM-DD.md` (today's date; if
the file exists, add `-2`, `-3`; create the folder if it is missing). Extra constraints for this
run: **$ARGUMENTS** (empty = use the goals file as is). Constraints here override the goals file
where they conflict; say so in the pitch file.

Every path below is inside the toolkit folder (`~/roblox-final`: `private/`, `vault/`,
`tools/trends/`), even when this runs from a game repo with the toolkit added. `private/` holds
the user's own notes and is not part of the public toolkit, so any file in it can be missing.
Each step below says what to do then. Never stop because a private file is absent.

## 1. Load context, in this order, and nothing else unless a step says so

1. `private/goals.md`: goals, constraints, values, preferences. Every pitch must fit it. For
   each `TBD` that affects a pitch, state the assumption you made.
   **Missing:** copy `goals.template.md` to `private/goals.md`, say you did, and ask once
   whether the user wants to fill it in first. If they say go on (or `$ARGUMENTS` already
   carries the constraints), pitch against the template's defaults and list every one of them
   under Context as an assumption.
2. `vault/INDEX.md`.
3. `private/trends/latest.md`. Note its `date`, `snapshot-count` and `days-of-history`. If the
   date is more than 3 days old, say so at the top of the pitch file and recommend running
   `python -m trends collect` + `report` first. With fewer than 8 days of history, there are no
   7-day risers: say that trend evidence is limited to the Up-and-Coming chart, breakouts and
   creation dates.
   **Missing:** say so at the top of the pitch file, name the two commands that create it
   (tools/trends/README.md), and continue. Trend evidence is then the dated `(data)` numbers
   inside the genre files only, and Trend momentum is capped at 3 for every pitch.
4. `vault/fundamentals/trend-lifecycle.md`, `vault/fundamentals/discovery-algorithm.md`
   (signals, what limits exposure, audience gating) and `vault/fundamentals/quality-bar.md`
   if it's marked done in INDEX.
5. Shortlist 8–10 candidate genres from the trends report (themes, clone waves, saturation,
   breakouts) and the goals file's preferences. Read **only** those genre files, plus a case
   study when a pitch leans on one game: `private/case-studies/<slug>.md`, where the genre file
   says `(case study: <slug>)`. **Missing:** use the genre file's "Top examples" line for that
   game and say the case study was not available. Skip files INDEX marks `todo`.
6. For numbers on a specific game, run from WSL:
   `cd ~/roblox-final/tools/trends && .venv/bin/python -m trends lookup "<name>"`.
   **No database yet:** the command says so and exits 1; cite the genre file's numbers instead.

## 2. Generate, then filter

- Draft about 10 ideas. Drop:
  - straight clones: the same core loop *and* theme as a charted game, which discovery
    deprioritizes;
  - anything the goals file rules out, or that needs art, animation or live-ops beyond a solo dev;
  - anything that can't reach its intended audience under the maturity/age-gate rules.
- Keep 5, with variety: at most 2 from one genre; at least 1 evergreen idea that doesn't depend
  on a current wave; at least 1 that uses the user's stated preferences.

## 3. Write the file

Start with frontmatter:

```yaml
---
title: Game pitches — YYYY-MM-DD
type: pitches
constraints: "<$ARGUMENTS or 'goals file defaults'>"
trends-report: <date from latest.md>, <snapshot-count> snapshots, <days-of-history> days (or "none")
---
```

Then a short **Context** paragraph: the constraints used, the trend data's age and limits, and
the assumptions made for `TBD`s.

Then, for each pitch:

```markdown
## N. <Working title> — <one-line hook>

- **Genre + themes:** <vault genre> (Roblox genre / subgenre); themes from themes.yaml
- **Core loop:** moment-to-moment → session → long-term
- **Unique spin:** one sentence on what the player *does* differently from the reference games
- **Reference games:** 2–3, each with what to learn and what not to copy (name the case study slug when one exists)
- **Why now:** trend evidence with numbers, cited as (data, <report date>); say when evidence is thin
- **Target audience:** ages, devices (mobile-first?), 16+ only or all ages, and the maturity label it needs
- **Monetization:** passes, products and subscriptions that fit the genre and the goals file's values; no pay-to-win in competitive modes
- **Solo-dev scope:** MVP feature list, build order with rough weeks, what to cut
- **Risks:** the 3 biggest, including the trend-lifecycle stage if it rides a wave
- **Scores:**

| Trend momentum | Saturation (inverse) | Uniqueness | Solo feasibility | Retention potential | Total /25 |
|---|---|---|---|---|---|
| n | n | n | n | n | n |

One line per score explaining it.
```

### Scoring rubric (1–5)

| Score | 5 | 3 | 1 |
|---|---|---|---|
| Trend momentum | Theme is a forming clone wave or has 7-day risers, with numbers | Stable or mixed evidence | Falling, or no evidence. With < 8 days of history, cap at 4 unless Up-and-Coming shows 3+ games |
| Saturation (inverse) | "few games, high demand" | "mixed" | "crowded" or "one game dominates" |
| Uniqueness | The spin changes the core verb or social shape | New combination of familiar loops | Reskin of a charted game |
| Solo feasibility | MVP ≤ 3 weeks with parts, code, free assets and the toolkit's generated props; at most a few authored animations | 4–6 weeks, some custom art or animation | Needs an art/animation team or heavy live-ops from day 1 |
| Retention potential | Day-1 hook + day 2–28 reasons + co-play (see discovery signals) | Some return reasons | One-session novelty |

End with:
- **Summary table**: all 5 pitches, their scores and totals, sorted by total.
- **What I'd prototype first and why** `(inferred)`: one pitch, plus a 1-week paper/greybox test
  that would prove or kill it (what to measure: first-session bounce, D1, session length).
- **What would change these scores**: e.g. more trend history, answers to the goals file's `TBD`s.

## Rules

- Never claim a pitch will succeed. Every judgment that isn't a cited number is `(inferred)`.
- Cite every trend number with its date. Don't call anything "rising" from a single snapshot;
  say "on Up-and-Coming" or "new breakout" instead.
- Describe reference games' designs; never reuse their names, characters, art or sounds.
- Don't edit any file except the new pitch file. No external AI API is needed: this command runs
  inside Claude Code.
- Asset skills in roblox-final (roblox-3d-model, roblox-animation, roblox-vfx, roblox-ui) make
  generated meshes, a handful of authored animations and VFX reachable solo, but each costs
  sessions: score a pitch that needs many of them lower on feasibility.
- When done, reply with the file path and the summary table, and name the next step: copy the
  chosen pitch into a new game with `python3 ~/roblox-final/tools/new_game.py "<Title>"`, then
  "complete the research and plan stage" (create-roblox-game section 1).

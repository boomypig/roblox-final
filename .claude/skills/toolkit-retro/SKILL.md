---
name: toolkit-retro
description: Turn the lessons inbox (private/lessons-inbox.md, filled by each game's Stop hook) into tested edits to the toolkit - one edit per lesson, in the skill that owns the rule, trap or script, each with a test that fails without it. Run only when the user asks for a retro or types /toolkit-retro; never during a game build.
disable-model-invocation: true
argument-hint: "[lesson id, or nothing for every open lesson]"
---

# Toolkit retro

Every game session ends at a boundary, and `create-roblox-game/scripts/session.py` appends what
went wrong in it to `private/lessons-inbox.md`: gate failures, stalls, fallbacks, interventions
and handoff debts. This skill is the other half of that loop. It runs in the toolkit
(`~/roblox-final`), only when the user asks, and works through the inbox one lesson at a time.

## Rules

- **One lesson, one edit, one test.** Each lesson becomes exactly one change to the skill that
  owns the rule: a line in its rules, a row in its traps, or a fix to its script. The edit
  comes with a test that fails on the tree before it and passes after. No edit without a test;
  no lesson closed without an edit, except as below.
- **The owner, not the nearest file.** Find the owner in `docs/redundancy-map.md` (which file
  owns a rule) and `docs/structure.md` (where a skill keeps its rules, traps and scripts). A
  design lesson goes in the vault (`vault/CONTRIBUTING.md`); a tool lesson goes in that skill's
  traps (`CLAUDE.md`, "Editing this toolkit").
- **A game's own debt is not a toolkit lesson.** "The coin mesh is a placeholder" is the game's
  backlog. Close it with `inbox.py skip <id> --reason "..."`, saying why no toolkit change is
  needed. A debt that shows a toolkit gap ("no skill could make the coin mesh") is a lesson.
- **Don't slow the build skills.** An edit to a build skill's body is a bug fix or glue, adds no
  required reading or approval step, and is logged in `private/upstream-changes.md` (the
  toolkit's working rule since the rework). Never shorten a skill to make room.
- **Decide; don't ask** (`docs/workflow.md`, "Operating policy"). Log each non-obvious call in
  `docs/decisions.md`. The one ask: a lesson whose fix would change what a gate accepts is a
  gate change; make it, mark it **Gate change** in `CHANGELOG.md`, and list it in the report.
- **Never write a private path, a game's name or the user's name into a tracked file.** A
  lesson is described by what failed, not by which game it failed in.

## Steps

1. `python3 .claude/skills/toolkit-retro/scripts/inbox.py list`. With an id as the argument,
   take that lesson only; otherwise take them in order.
2. For one lesson: find the owner (Rules above), read only that file's relevant section, and
   decide the one edit. Several lessons with the same cause share one edit: close each against
   it.
3. Write the test first, in `tests/`, and run it on the tree as it is: it must fail. Then make
   the edit and run it again: it must pass. A test file's docstring names the defect.
4. Close the lesson:
   `inbox.py done <id> --owner <skill or tool> --edit <path> --test <tests/test_x.py>`.
5. After the last lesson, run the gate. Commit in categorized groups (`fix(<skill>): ...`,
   `docs: ...`) as the toolkit's commits are; do not push.
6. Report: each lesson, its owner, the edit, the test, and every lesson closed without a change
   with its reason.

## Gate

All of these pass:

```bash
python3 .claude/skills/toolkit-retro/scripts/inbox.py check
python3 -m unittest discover -s tests
python3 tools/vault_lint.py
python3 tools/toolkit_lint.py
python3 tools/build_cards.py --check
python3 tools/smoke.py
```

## References

| File | Used for |
|---|---|
| `docs/redundancy-map.md` | which file owns a rule |
| `docs/structure.md` | where a skill keeps its rules, traps, scripts and gate |
| `docs/workflow.md` | the operating policy and the session boundaries that fill the inbox |
| `scripts/inbox.py` | listing and closing lessons; the record is `private/lessons-done.md` |
| `create-roblox-game/scripts/session.py` | what writes the inbox, and what each line means |

## Traps

- **Fixing the symptom in the game.** The retro runs in the toolkit; a fix to one game's files
  is not a toolkit edit and leaves the next game to fail the same way. (Why the inbox lives in
  the toolkit's `private/`, not in a game.)
- **A rule added in a second place.** The lint fails on a sentence that appears in two files
  (`tools/toolkit_lint.py`, `dup`); put the rule in its owner and point at it.
- **A test that passes before the edit.** It proves nothing. Run it on the old tree first
  (step 3); the toolkit's phase work proved every new test this way.

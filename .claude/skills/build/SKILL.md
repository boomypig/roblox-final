---
name: build
description: Implement an approved mechanic spec in a Roblox game repo
argument-hint: "<spec name, e.g. checkpoints>"
---

Implement the spec docs/design/mechanics/$ARGUMENTS.md.

1. Read CLAUDE.md, the spec, `design/layout.json` (where this game keeps its pure rules,
   tunables and remotes; without it, the roblox-code scaffold's layout), docs/glossary.md,
   docs/tech/architecture.md and docs/tech/conventions.md. Read the `roblox-code` skill
   (`~/roblox-final/.claude/skills/roblox-code/SKILL.md`): its five standing rules and traps
   apply to every line. Then read ../roblox-final/vault/INDEX.md and the vault files the spec
   needs; always this skill's `references/quality-bar.md`, and roblox-code's
   `references/security.md` for any RemoteEvent or RemoteFunction handler.
2. Run `python3 ~/roblox-final/.claude/skills/build/scripts/check_spec.py <spec> --require-approved`.
   If the spec isn't `Status: approved`, or the gate fails, say so and end: nothing is built
   from a draft or from a spec with no checkable criteria.
3. If something in the spec is ambiguous, don't ask. Take the reading closest to the spec and
   the glossary, log it in docs/decisions.md as "(Claude's judgment call)", list it in the
   report, and keep building (the operating policy (`docs/workflow.md` in the toolkit)). End early only when two
   approved docs contradict each other; say which lines.
4. Implement it following the architecture. Build only what the spec asks for. The paths below
   are the layout map's fields (roblox-code `references/layout.md`); the scaffold's are in
   brackets.
   - Pure rules go in a `pure` path [`src/shared/Core/`] with a `<tests>/<Name>.spec.luau`
     [`tests/`] that pins the boundaries the spec cares about. Tunables go in `config`
     [`src/shared/Config/`]. New remotes go where `remotes` says: declared in its module for
     `net-module` [`src/shared/Net.luau`], or created by the owning service under its folder
     for `per-service`; either way validated server-side (type, range, ownership). Follow the
     game's layout even where it differs from the scaffold; moving code onto the scaffold's
     layout is a refactor the user asks for, not part of a build.
   - Map geometry isn't built here; that's roblox-map plus the map-builder agent. UI, meshes,
     animation, VFX and sound come from their own skills; this code only loads them.
5. Run the gates from WSL and fix until all four are green:
   `python3 ~/roblox-final/.claude/skills/roblox-code/scripts/check.py`
   (rojo build, lune tests, selene, stylua). If the toolchain isn't installed, say so.
6. The session ends here, so write its handoff. Mark the boundary, write the short handoff and
   fill every TODO line in it (files changed, the gates' result line, what needs a playtest,
   judgment calls, the next step):
   `python3 ../roblox-final/.claude/skills/create-roblox-game/scripts/session.py mark build --what <spec>`
   `python3 ../roblox-final/.claude/skills/create-roblox-game/scripts/section.py handoff --light build --what <spec>`
   Inside a create-roblox-game section, skip this step: the section's own handoff covers it.
   The game's Stop hook refuses to end the session at this boundary without the handoff.
7. Report: files changed, gate results, each acceptance criterion (met / needs playtest), and any
   judgment calls. Log real decisions in docs/decisions.md. Suggest running the reviewer agent.
8. Don't commit. I'll playtest first.

## Rules

- Build only what the approved spec asks for; no questions on the way (operating policy,
  `docs/workflow.md`). Judgment calls go in docs/decisions.md and the report.
- The code rules are roblox-code's five standing rules; this skill does not restate them.
- Don't commit. The user playtests first.

## Gate

The four code gates, all green: `roblox-code/scripts/check.py` (rojo build, lune test, selene,
stylua; it reads `design/layout.json` for which folders to check). Before that, the spec's own
gate: `scripts/check_spec.py <spec> --require-approved`. After it, outside a section, a filled
`HANDOFF.md` (the Stop hook, `create-roblox-game/scripts/session.py`).

## References

This skill owns the spec → build → review loop, so the references its two agents use live
here.

| File | Used by | Source of its facts |
|---|---|---|
| `references/quality-bar.md` | `/build` step 1, the `reviewer` agent, section 5 of `create-roblox-game` | its Sources list (Creator Docs, dated) |
| `scripts/check_spec.py` | the `spec-writer` agent (draft gate), `/build` step 2 | this skill |
| `.claude/skills/roblox-code/SKILL.md`, `references/patterns.md`, `references/traps.md`, `references/security.md` | every line of code written here | roblox-code |
| `.claude/skills/roblox-code/references/layout.md` | step 4: where each kind of code goes in this game | roblox-code |

## Traps

- **Building from a draft.** A spec that is not `Status: approved` is a design nobody agreed
  to. `check_spec.py --require-approved` refuses it.
- **Acceptance criteria that cannot be checked.** With none, the review passes by default.
  The gate refuses a spec with no checkbox criteria.
- **A guess nobody knew was a guess.** An unclear point that is neither asked nor written
  down. Every reading you chose goes in docs/decisions.md and the report.
- **Building what the spec did not ask for.** The reviewer lists it; remove it rather than
  explain it.
- **Code traps** (a remote that fires but nothing happens, runtime children under a
  Rojo-managed folder, a bare `pcall`): owned by `roblox-code/references/traps.md`.

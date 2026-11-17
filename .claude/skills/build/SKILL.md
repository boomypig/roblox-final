---
name: build
description: Implement an approved mechanic spec in a Roblox game repo
argument-hint: "<spec name, e.g. checkpoints>"
---

Implement the spec docs/design/mechanics/$ARGUMENTS.md.

1. Read CLAUDE.md, the spec, docs/glossary.md, docs/tech/architecture.md and
   docs/tech/conventions.md. Read the `roblox-code` skill
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
4. Implement it following the architecture. Build only what the spec asks for.
   - Pure rules go in `src/shared/Core/` with a `tests/<Name>.spec.luau` that pins the
     boundaries the spec cares about. Tunables go in `src/shared/Config/`. New remotes are
     declared in `src/shared/Net.luau` and validated server-side (type, range, ownership).
   - Map geometry isn't built here; that's roblox-map plus the map-builder agent. UI, meshes,
     animation, VFX and sound come from their own skills; this code only loads them.
5. Run the gates from WSL and fix until all four are green:
   `python3 ~/roblox-final/.claude/skills/roblox-code/scripts/check.py`
   (rojo build, lune tests, selene, stylua). If the toolchain isn't installed, say so.
6. Report: files changed, gate results, each acceptance criterion (met / needs playtest), and any
   judgment calls. Log real decisions in docs/decisions.md. Suggest running the reviewer agent.
7. Don't commit. I'll playtest first.

## Rules

- Build only what the approved spec asks for; no questions on the way (operating policy,
  `docs/workflow.md`). Judgment calls go in docs/decisions.md and the report.
- The code rules are roblox-code's five standing rules; this skill does not restate them.
- Don't commit. The user playtests first.

## Gate

The four code gates, all green: `roblox-code/scripts/check.py` (rojo build, lune test, selene,
stylua). Before that, the spec's own gate: `scripts/check_spec.py <spec> --require-approved`.

## References

This skill owns the spec → build → review loop, so the references its two agents use live
here.

| File | Used by | Source of its facts |
|---|---|---|
| `references/quality-bar.md` | `/build` step 1, the `reviewer` agent, section 5 of `create-roblox-game` | its Sources list (Creator Docs, dated) |
| `scripts/check_spec.py` | the `spec-writer` agent (draft gate), `/build` step 2 | this skill |
| `.claude/skills/roblox-code/SKILL.md`, `references/patterns.md`, `references/traps.md`, `references/security.md` | every line of code written here | roblox-code |

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

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
   needs; always fundamentals/quality-bar.md, and fundamentals/security-and-anti-exploit.md
   for any RemoteEvent or RemoteFunction handler.
2. If the spec isn't `Status: approved`, stop and tell me.
3. If anything is ambiguous, ask before writing code.
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

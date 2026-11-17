# Toolkit decisions

Why the toolkit is built the way it is. Newest section last. Each entry: the decision, the
reason, and what was rejected. Game decisions go in the game's own `docs/decisions.md`.

## Private material and the public tree (2026-11-17)

**D1. Personal material lives in `private/`, a gitignored folder that is its own local git repo.**
Goals, pitches, generated trend reports, the tracker database, the case studies of named games,
planning history and maintenance notes are one person's working notes. Keeping them in one
ignored folder means a single `.gitignore` line protects all of them and one test can prove
nothing leaked. Rejected: a separate sibling folder (every reader would need a second path
setting) and per-file ignore rules (one forgotten rule publishes a note).

**D2. `ROBLOX_FINAL_PRIVATE` moves the folder.** Scripts read the variable and fall back to
`<toolkit>/private`. It lets the tests point every reader at an empty folder to prove the
missing-file behaviour, and lets a user keep notes on another drive.

**D3. Every reader of a private file says what to do when it is missing, and never stops.**
The rule is stated where the reader looks: in the skill step, in `vault/INDEX.md` for vault
files, in `CLAUDE.md` for everything else. A goals file is the one thing only the user can
supply, so `/pitch` asks once; everything else continues with a stated assumption.
`tests/test_private_optional.py` is the coverage check.

**D4. What "no private path in a tracked file" means.** A tracked file may name a private
*slot* (`private/goals.md`, `private/trends/latest.md`), because readers need the path. It may
not contain a machine path (a home folder, a Windows user folder), a name or email, or a path
to one *specific* private file (a dated pitch, a note). `tests/test_public_tree.py` enforces
all three. The repository's own address is the single place an owner handle may appear.

**D5. Names to search for are listed in `private/identity.txt`, not in the test.** Writing the
names into a tracked test would publish them; hashing them would not hide a first name from a
dictionary. Generic patterns (any email address, any home folder) run everywhere, including CI;
the literal terms run wherever the private file exists.

**D6. Case studies are cited as `(case study: <slug>)`, not linked.** A link into `private/`
is dead for every visitor. The marker reads as plain text, the lint resolves it when the notes
are present, and the genre file's "Top examples" line still carries the summary. Rejected:
keeping the links pointed at `private/` (72 dead links on GitHub).

**D7. The tracker's data moved with its reports.** "The code is public; the data and reports
are private." The database, cache and scheduled-run log are in `private/trends/data/`, and the
tracker creates the folder on first run, so a fresh clone works with no setup step. The API
dump used by `vault_apicheck.py` is a public file, so it is a cache (`tools/.cache/`), not
private data.

**D8. The tracker's User-Agent names the tool, not a person.** A public tool should not send
its author's address from every user's machine. `TRENDS_CONTACT` adds contact details for
those who want to be reachable.

**D9. `~/roblox-final` is the documented install location, not a machine path.** The skill
docs give script paths from there. Rewriting every path would change the build skills' bodies
for no gain in behaviour; the README says to clone there.

**D10. `NOTICE.md` lists only what someone using the toolkit has to act on.** The fonts the UI
skill ships and their licence, the terms of the tools and models the skills call, how the design
library treats other games, and where the tracker's data stays. Each is a thing a user can get
wrong by not knowing it.

**D11. `starter/.mcp.json` keeps `/mnt/c/Windows/system32/cmd.exe`.** It is the fixed WSL path
to a Windows system binary, the same on every WSL machine, and it is how a WSL session starts
the Studio MCP. It names no user.

**D12. The public history starts from one commit.** The earlier history held the private
files. It is saved as a git bundle inside `private/` and the public branch begins with a single
commit of the cleaned tree; later work is committed on top.

**D13. Public commits carry the repository handle and a GitHub no-reply address.** The machine's
global git identity is a real name and a personal address, and commit metadata is as public as
file contents. The toolkit repo sets a local identity instead; the private repo keeps the global
one. This is a local setting and can be changed before the first push.

## One toolkit (2026-11-17)

**D14. One operating policy, owned by `docs/workflow.md`.** The user approves a brief, spec or
section once; inside a task nobody stops to ask; open details are decided and logged as
assumptions; the gate is the only stopping point. The exceptions are an action that cannot be
undone or leaves the machine, something only the user can know, and something purely
mechanical. Every skill and agent applies it in a line or two and does not restate it.
Rejected: a policy file per side (the conflict this removes) and a policy inside one skill
(agents and the starter could not point at it).

**D15. `/art-brief` and the spec-writer draft once instead of asking first.** Their questions
became `**Assumption:**` lines, most build-changing first, which the user settles while
approving. The read-back of the references is written into the brief's References table. The
one ask left in `/art-brief` is saving reference images to disk, which only the user can do.

**D16. One workflow doc; a game does not carry a copy.** `starter/docs/workflow.md` is gone and
`starter/CLAUDE.md` points at the toolkit's `docs/workflow.md`. A copied doc goes stale in
every game the day the toolkit changes. The spec, build, review loop is the same path at the
size of one feature ("Change"), not a second way to build.

**D17. Build knowledge lives with the skill that enforces it; design research stays one
library.** Decided on evidence (`docs/vault-readers.md`): seven fundamentals are read by a
build step and moved to that skill's `references/` with sources and dates kept; fifty-two genre
and pattern files and ten fundamentals are read by `/pitch`, the spec-writer and section 1 and
stay in `vault/`. No file had zero readers, so nothing was archived. `visual-quality.md` and
`performance-and-devices.md` went to `roblox-map` rather than `art-brief` because the builder's
checks enforce them and the brief only picks from them.

**D18. `vault/INDEX.md` is the short index; `vault/CATALOG.md` is the full table.** Five steps
load the index first. It went from 11.7 KB to 4.7 KB by listing names with a few words each;
the full read-when lines and statuses moved to the catalog, which the lint reads. The lint
fails if a catalogued file is not named in the short index, and it lints the moved build
references with the vault's rules, so moving a file did not lower its bar.

**D19. Names follow how a thing is started, and nothing was renamed.** Commands the user types
are short verbs; skills Claude loads for a domain are `roblox-<domain>`; agents asked for by
role are role names; orchestrator workers are `roblox-asset-<domain>`. A uniform prefix would
have needed an alias skill for each renamed command, and every alias is a line in every
session's skill list for no change in behaviour.

**D20. An agent is a thin entry; its knowledge belongs to an owning skill.** `spec-writer` and
`reviewer` are owned by `build` (the spec, build, review loop); `map-builder` by `roblox-map`;
the `roblox-asset-*` workers by their domain skill; `roblox-asset-sfx` and
`roblox-market-scout` by `roblox-build-orchestrator`, which holds their briefs. A fact is never
in an agent and a skill at once. Rejected: a references folder beside each agent (files under
`.claude/agents/` risk being loaded as agents).

**D21. The design-side steps got gates.** `check_pitch.py`, `check_brief.py` and
`check_spec.py` end the pitch, brief and spec steps the way `check.py` ends a build. Each fails
its own unfilled template. Run on the four pitch files that existed, the pitch gate found an
undated `(data)` number in every one; that is the first entry in the pitch skill's traps.

**D22. Traps are only written from failures that happened.** Each new trap names where it was
seen (a gate's output, the tracker's README, the first game). Where a skill has no recorded
failure yet, its traps section is short rather than padded.

**D23. Three overlaps are consolidated by later phases, not twice.** The two `new_game.py`
become one when the starter is rebuilt (phase 4); the map-builder's restated checklists become
the builder card (phase 3); the reviewer's restated code rules become the reviewer card and
the layout map (phases 3 and 4). `docs/redundancy-map.md` marks each. Doing them now would
mean rewriting the same files again a phase later.

**D24. `tools/migrate_game.py` shows changes by default and applies them with `--write`.** It
runs in someone's game repo, so the safe default is to change nothing. It rewrites only paths
that carry the toolkit's folder name or a full vault path, and lists ambiguous ones.

## Bugs and agents (2026-11-17)

**D25. `check.py` detects an unpinned rokit shim by its message, for every tool.** The shim
prints "Failed to find tool ... in any project manifest" and exits 0, so the exit code cannot be
trusted. Matching the message covers rojo and lune as well as the selene and stylua lines the
bug was reported against. The fix message names `rokit.toml`, or `aftman.toml` when that is the
only manifest. Rejected: inspecting the shim's path (a shim and a real binary can share it).

**D26. A scaffold marker is `TODO` alone, `TODO:` or `TODO` glued to a capitalised name.**
Matching "starts with TODO" alone would still reject "TODO List Tycoon", the case the bug was
about. Every marker `new_game.py` writes fits the narrower pattern (a test checks them all).
`validate.py` owns the pattern and `section.py` imports it.

**D27. Agent cards are generated, word for word, with a coverage table and source hashes.** A
hand-written card is a second copy of the rules that drifts. `tools/build_cards.py` copies the
sections whole; the test compares every source line to the card, recounts every item, and
fails when a source changes until the card is rebuilt. The builder card is 18 KB against the
63 KB of references the map-builder read before; the reviewer card is 29 KB and replaces the
whole quality bar plus the whole roblox-code skill. The vetting section and the `execute_luau`
rules were added to the builder card beyond the four sections named, because the agent's own
instructions send it to both.

**D28. The map checks are one Luau file with a parameter block, not a Python tool.** The
map-builder has no shell, only the Studio MCP. It copies the state file's "Check parameters"
block between the file's marker lines and runs it through `execute_luau`; `map_checks.py` does
the same splice for people and tests. The checks never yield, because `execute_luau` drops the
output of a script that yields, so the floor grid widens instead.

**D29. "Every walkable part has Surface" means a `Surface` string attribute.** The task did not
define it. A walkable part is a collidable, visible part with a face within `walkableNormalY` of
straight up and at least 2 studs across; footsteps and effects can read the attribute. The
attribute name is a parameter (`surfaceAttribute`), so a game that means something else changes
one value.

**D30. Decoration may collide only when it says so.** A `Dressing` part with collisions on fails
unless it carries `Collides = true`, which the agent sets when the brief says players stand on
it. Without an explicit flag the check could not tell intent from a forgotten default.

**D31. The batch example refuses nothing when `TryBeginRecording` returns nil.** It still builds,
and says that no undo recording was open. Refusing would block every build in a session where
recordings are unavailable (one unverified report blames a connected Rojo plugin), and the
`pcall` now prevents the main cause the docs give: an earlier recording left open.

**D32. The spec-writer has Bash, for its gate only.** It was told to run `check_spec.py` without
a tool that can run it. Adding Bash, limited by instruction to that one command, is the smallest
change that lets the step end on its gate. Rejected: leaving the gate to the caller (the step
would end before its gate).

**D33. The map-builder writes only its state file.** It gets Write and Edit, limited by
instruction to `docs/design/maps/<name>.state.md`; a test checks the instruction is there.

**D34. The one new-game command lives in `tools/`; the contract stays with its owner.** D23 put
the single `new_game.py` in create-roblox-game. Building it showed the command needs the
starter, which is a toolkit folder, not a skill's, while the contract (`game.json`, the stage
stubs, `BUILD.md`) is read by create-roblox-game's own `validate.py`, `section.py` and now
`adopt.py`. So `tools/new_game.py` is the command and create-roblox-game's `new_game.py` holds
the contract and forwards its old command there. Rejected: moving the starter into the skill
(a skill would then own every game's CLAUDE.md and docs).

**D35. roblox-code owns the layout map.** `design/layout.json` says where the roblox-code rules
apply in one game, so its schema is `roblox-code/references/layout.md` and its only reader is
`roblox-code/scripts/layout.py`, which fills in the scaffold's values for any missing field. A
game with no file is read as the scaffold, so every existing game keeps working unchanged.

**D36. Three boundaries, each detected where it happens.** `section.py close` marks a section
boundary when it passes. `/build` marks a build boundary as its step 6, after its gates. The
map-builder has no shell, so a map boundary is read from its state file: a Pass log row newer
than the last boundary and an empty "Run in progress". Inside a section only the section
boundary counts, so the hook can never interrupt a section; a /build or map pass there is
part of the section and its handoff.

**D37. The hook lets go after three refusals and records a debt.** A hook that blocks forever
traps a session that cannot write a handoff (a full disk, a broken tool). Three blocks is
enough for any session that can; after that the stop goes through and the lessons inbox gets
"the session stopped after a <kind> boundary with no up-to-date HANDOFF.md". Rejected: relying
on `stop_hook_active`, which allows the second stop and so enforces nothing.

**D38. The hook command branches on `$OSTYPE`, and the 100 ms budget is the script's.** In WSL
or Linux it runs `python3` directly: about 20 ms. Claude Code on Windows runs hooks in Git
Bash, where `python3` is the Store stub; the command then runs `wsl.exe -e python3`, about
150 ms in total, of which the crossing into WSL is about 130 ms and cannot be removed without
Python on Windows. Rejected: `python3 … || wsl.exe …`, which first starts the stub (about
250 ms in total).

**D39. smoke.py runs the gate tools as real binaries.** A rokit shim runs whatever version the
game pins and fails when that version is not installed, so a smoke run would test the
machine's install instead of the toolkit. smoke.py links the real binaries (from
`ROBLOX_TOOLS_BIN`, rokit's tool storage, or PATH) into a temp folder. Without Wally it stubs
an empty `Packages/` and says so; CI installs Rojo 7.4.4, Lune 0.8.9, Selene 0.28.0, StyLua
0.20.0 and Wally 0.3.2 from their releases and runs `wally install` for real.

**D40. `adopted` is a ledger status that needs no start, and only section 1 accepts it.** An
adopted game's research and design were done before the toolkit, so there is no span to time.
Section 1's close counts an `end --status adopted` for its two stages (gate change 2);
`validate.py` is still required, because the contract is what every later stage reads. Every
other section ignores an adopted end: its work happens under the toolkit and is bracketed.

**D41. Adoption writes only new files and never touches code.** `adopt.py` is read-only by
default. `--write` creates files that do not exist (the layout map, the contract skeleton, the
starter's files, an adoption handoff) and never writes under `src/` or `tests/`; `--force`
replaces only the two layout files. A reformat during adoption would hide behavior changes in
a diff nobody can read (`references/adopt.md`).

**D42. A light handoff has five headings and its own marker.** One /build or one map pass needs
where things are, what was done and verified, what is unproven, the debts and the next step;
not the ledger, the place or the section rules. It carries `<!-- handoff: build|map -->`, and
any earlier handoff is copied to `design/handoffs/` with a timestamp before it is replaced.

**D43. A new game's gate is the four code gates; `validate.py` refuses it on purpose.** The
workflow said both pass on an empty game, which was never true: the contract ships with TODO
markers so section 1 cannot be skipped. The Start row now says so, and smoke.py checks both
halves (refused fresh, passed once filled).

**D44. A placeholder says who fills it.** Every `<...>` in a made game's Markdown, outside code,
comments and `_template` files, reads `<fill in at section N: ...>`. The templates are copied
before use and say so in a first-line comment. `smoke.py` and `tests/test_new_game.py` fail on
any other placeholder.

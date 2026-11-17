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
